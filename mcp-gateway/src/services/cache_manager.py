import asyncio
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import aiofiles

from ..utils.logger import logger


class CacheManager:
    """Local file cache manager with TTL support."""

    def __init__(self, cache_dir: str = "./.cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        cache_file = self._get_cache_file(key)
        if not cache_file.exists():
            return None
        try:
            async with aiofiles.open(cache_file, "r") as f:
                content = await f.read()
                data = json.loads(content)
            expires_at = datetime.fromisoformat(data["expires_at"])
            if datetime.utcnow() > expires_at:
                cache_file.unlink()
                return None
            return data["value"]
        except Exception as e:
            logger.error("Cache read error", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        cache_file = self._get_cache_file(key)
        try:
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            data = {
                "value": value,
                "expires_at": expires_at.isoformat(),
                "created_at": datetime.utcnow().isoformat(),
            }
            async with self._lock:
                async with aiofiles.open(cache_file, "w") as f:
                    await f.write(json.dumps(data, default=str))
            return True
        except Exception as e:
            logger.error("Cache write error", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        cache_file = self._get_cache_file(key)
        if cache_file.exists():
            cache_file.unlink()
            return True
        return False

    async def clear_expired(self):
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                async with aiofiles.open(cache_file, "r") as f:
                    content = await f.read()
                    data = json.loads(content)
                expires_at = datetime.fromisoformat(data["expires_at"])
                if datetime.utcnow() > expires_at:
                    cache_file.unlink()
                    count += 1
            except Exception:
                pass
        logger.info("Cache cleanup completed", cleared=count)

    def _get_cache_file(self, key: str) -> Path:
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
