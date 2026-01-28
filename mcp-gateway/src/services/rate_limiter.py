import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict

from ..utils.logger import logger


@dataclass
class RateLimit:
    requests_per_day: int
    requests_per_minute: int
    current_day_count: int = 0
    current_minute_count: int = 0
    last_day_reset: datetime = field(default_factory=datetime.utcnow)
    last_minute_reset: datetime = field(default_factory=datetime.utcnow)


API_LIMITS = {
    "trends": RateLimit(requests_per_day=1000, requests_per_minute=60),
    "search": RateLimit(requests_per_day=10000, requests_per_minute=100),
    "youtube_upload": RateLimit(requests_per_day=50, requests_per_minute=5),
    "youtube_analytics": RateLimit(requests_per_day=10000, requests_per_minute=100),
    "knowledge_graph": RateLimit(requests_per_day=10000, requests_per_minute=100),
}


class RateLimitExceeded(Exception):
    def __init__(self, message: str, wait_seconds: float):
        super().__init__(message)
        self.wait_seconds = wait_seconds


class RateLimiter:
    """API rate limiter with daily and per-minute quotas."""

    def __init__(self):
        self.limits: Dict[str, RateLimit] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        for api, limit in API_LIMITS.items():
            self.limits[api] = RateLimit(
                requests_per_day=limit.requests_per_day,
                requests_per_minute=limit.requests_per_minute,
                last_day_reset=datetime.utcnow(),
                last_minute_reset=datetime.utcnow(),
            )
            self._locks[api] = asyncio.Lock()

    async def acquire(self, api: str) -> bool:
        if api not in self.limits:
            return True
        async with self._locks[api]:
            limit = self.limits[api]
            now = datetime.utcnow()
            if now - limit.last_day_reset > timedelta(days=1):
                limit.current_day_count = 0
                limit.last_day_reset = now
            if now - limit.last_minute_reset > timedelta(minutes=1):
                limit.current_minute_count = 0
                limit.last_minute_reset = now
            if limit.current_day_count >= limit.requests_per_day:
                wait_seconds = (limit.last_day_reset + timedelta(days=1) - now).total_seconds()
                logger.warning("Daily rate limit reached", api=api, wait_seconds=wait_seconds)
                raise RateLimitExceeded(f"Daily limit for {api}", wait_seconds)
            if limit.current_minute_count >= limit.requests_per_minute:
                wait_seconds = (limit.last_minute_reset + timedelta(minutes=1) - now).total_seconds()
                logger.warning("Minute rate limit reached", api=api, wait_seconds=wait_seconds)
                await asyncio.sleep(wait_seconds)
                limit.current_minute_count = 0
                limit.last_minute_reset = datetime.utcnow()
            limit.current_day_count += 1
            limit.current_minute_count += 1
            return True

    def get_remaining(self, api: str) -> int:
        if api not in self.limits:
            return -1
        limit = self.limits[api]
        return limit.requests_per_day - limit.current_day_count
