import asyncio
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional

from ..utils.logger import logger


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: int = 300
    half_open_max_requests: int = 3
    success_threshold: int = 2


@dataclass
class CircuitBreakerState:
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    half_open_request_count: int = 0


class CircuitBreaker:
    """Circuit breaker: CLOSED -> OPEN -> HALF_OPEN -> CLOSED."""

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitBreakerState()
        self._lock = asyncio.Lock()

    @property
    def state(self) -> CircuitState:
        return self._state.state

    @property
    def is_available(self) -> bool:
        return self._state.state != CircuitState.OPEN or self._should_attempt_recovery()

    def _should_attempt_recovery(self) -> bool:
        if self._state.state != CircuitState.OPEN:
            return False
        if self._state.last_failure_time is None:
            return True
        elapsed = datetime.utcnow() - self._state.last_failure_time
        return elapsed.total_seconds() >= self.config.recovery_timeout

    async def call(self, func: Callable, *args, **kwargs) -> tuple[Any, Optional[str]]:
        async with self._lock:
            if self._state.state == CircuitState.OPEN:
                if self._should_attempt_recovery():
                    self._transition_to_half_open()
                else:
                    logger.warning("Circuit breaker OPEN, rejecting", breaker=self.name)
                    return None, "downgraded"
            if self._state.state == CircuitState.HALF_OPEN:
                if self._state.half_open_request_count >= self.config.half_open_max_requests:
                    logger.warning("Circuit breaker HALF_OPEN limit", breaker=self.name)
                    return None, "downgraded"
                self._state.half_open_request_count += 1

        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result, None
        except Exception as e:
            await self._record_failure(e)
            raise

    async def _record_success(self):
        async with self._lock:
            self._state.failure_count = 0
            if self._state.state == CircuitState.HALF_OPEN:
                self._state.success_count += 1
                if self._state.success_count >= self.config.success_threshold:
                    self._transition_to_closed()

    async def _record_failure(self, error: Exception):
        async with self._lock:
            self._state.failure_count += 1
            self._state.last_failure_time = datetime.utcnow()
            self._state.success_count = 0
            logger.warning(
                "Circuit breaker failure", breaker=self.name, failure_count=self._state.failure_count, error=str(error)
            )
            if self._state.state == CircuitState.HALF_OPEN:
                self._transition_to_open()
            elif self._state.failure_count >= self.config.failure_threshold:
                self._transition_to_open()

    def _transition_to_open(self):
        self._state.state = CircuitState.OPEN
        self._state.half_open_request_count = 0
        logger.error("Circuit breaker OPENED", breaker=self.name, recovery_in_seconds=self.config.recovery_timeout)

    def _transition_to_half_open(self):
        self._state.state = CircuitState.HALF_OPEN
        self._state.half_open_request_count = 0
        self._state.success_count = 0
        logger.info("Circuit breaker HALF_OPEN", breaker=self.name)

    def _transition_to_closed(self):
        self._state.state = CircuitState.CLOSED
        self._state.failure_count = 0
        self._state.success_count = 0
        self._state.half_open_request_count = 0
        logger.info("Circuit breaker CLOSED", breaker=self.name)

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "state": self._state.state.value,
            "failure_count": self._state.failure_count,
            "last_failure": self._state.last_failure_time.isoformat() if self._state.last_failure_time else None,
            "is_available": self.is_available,
        }


class CircuitBreakerRegistry:
    def __init__(self):
        self._breakers: dict[str, CircuitBreaker] = {}

    def get_or_create(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name, config)
        return self._breakers[name]

    def get_all_status(self) -> dict:
        return {name: breaker.get_status() for name, breaker in self._breakers.items()}


circuit_registry = CircuitBreakerRegistry()

BREAKER_CONFIGS = {
    "youtube_upload": CircuitBreakerConfig(failure_threshold=3, recovery_timeout=600, half_open_max_requests=1),
    "youtube_analytics": CircuitBreakerConfig(failure_threshold=5, recovery_timeout=300),
    "google_trends": CircuitBreakerConfig(failure_threshold=5, recovery_timeout=300),
    "google_search": CircuitBreakerConfig(failure_threshold=10, recovery_timeout=180),
}
