import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from ..utils.logger import logger

SCOPES = {
    "youtube": [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/youtubepartner",
    ],
    "youtube_analytics": [
        "https://www.googleapis.com/auth/yt-analytics.readonly",
    ],
    "search": [
        "https://www.googleapis.com/auth/customsearch",
    ],
    "knowledge_graph": [],
}


class PreemptiveAuthManager:
    """Multi-account OAuth2 manager with pre-emptive token refresh."""

    PREEMPTIVE_REFRESH_MINUTES = 10
    MIN_TOKEN_VALIDITY_MINUTES = 30

    def __init__(
        self,
        credentials_dir: str = "./credentials",
        client_secrets_file: str = "./credentials/client_secrets.json",
    ):
        self.credentials_dir = Path(credentials_dir)
        self.client_secrets_file = Path(client_secrets_file)
        self._credentials_cache: Dict[str, Credentials] = {}
        self._token_expiry_cache: Dict[str, datetime] = {}
        self._refresh_lock = asyncio.Lock()

    async def get_credentials(
        self,
        service: str,
        channel_id: Optional[str] = None,
        min_validity_minutes: Optional[int] = None,
    ) -> Credentials:
        cache_key = f"{service}:{channel_id or 'default'}"
        min_validity = min_validity_minutes or self.PREEMPTIVE_REFRESH_MINUTES

        async with self._refresh_lock:
            if cache_key in self._credentials_cache:
                creds = self._credentials_cache[cache_key]
                if self._needs_preemptive_refresh(cache_key, min_validity):
                    logger.info("Pre-emptive token refresh", service=service, channel_id=channel_id)
                    creds = await self._refresh_credentials(creds, service, channel_id)
                    self._credentials_cache[cache_key] = creds
                    self._update_expiry_cache(cache_key, creds)
                elif creds.valid:
                    return creds
                elif creds.expired and creds.refresh_token:
                    creds = await self._refresh_credentials(creds, service, channel_id)
                    self._credentials_cache[cache_key] = creds
                    self._update_expiry_cache(cache_key, creds)
                    return creds

            creds = self._load_credentials(service, channel_id)
            if creds:
                if self._needs_preemptive_refresh_for_creds(creds, min_validity):
                    creds = await self._refresh_credentials(creds, service, channel_id)
                self._credentials_cache[cache_key] = creds
                self._update_expiry_cache(cache_key, creds)
                return creds

            creds = await self._authorize(service, channel_id)
            self._credentials_cache[cache_key] = creds
            self._update_expiry_cache(cache_key, creds)
            return creds

    def _needs_preemptive_refresh(self, cache_key: str, min_validity_minutes: int) -> bool:
        if cache_key not in self._token_expiry_cache:
            return False
        expiry = self._token_expiry_cache[cache_key]
        return (expiry - datetime.utcnow()).total_seconds() < min_validity_minutes * 60

    def _needs_preemptive_refresh_for_creds(self, creds: Credentials, min_validity_minutes: int) -> bool:
        if not creds.expiry:
            return False
        return (creds.expiry - datetime.utcnow()).total_seconds() < min_validity_minutes * 60

    def _update_expiry_cache(self, cache_key: str, creds: Credentials):
        if creds.expiry:
            self._token_expiry_cache[cache_key] = creds.expiry

    async def _refresh_credentials(self, creds: Credentials, service: str, channel_id: Optional[str]) -> Credentials:
        try:
            creds.refresh(Request())
            self._save_credentials(service, channel_id, creds)
            logger.info(
                "Token refreshed", service=service, new_expiry=creds.expiry.isoformat() if creds.expiry else None
            )
            return creds
        except Exception as e:
            logger.error("Token refresh failed", error=str(e))
            raise

    async def ensure_valid_for_upload(
        self,
        service: str,
        channel_id: Optional[str] = None,
        estimated_upload_minutes: int = 30,
    ) -> Credentials:
        min_validity = estimated_upload_minutes + self.PREEMPTIVE_REFRESH_MINUTES
        return await self.get_credentials(service=service, channel_id=channel_id, min_validity_minutes=min_validity)

    def _load_credentials(self, service: str, channel_id: Optional[str]) -> Optional[Credentials]:
        token_file = self._get_token_file_path(service, channel_id)
        if not token_file.exists():
            return None
        try:
            with open(token_file, "r") as f:
                token_data = json.load(f)
            creds = Credentials(
                token=token_data["token"],
                refresh_token=token_data.get("refresh_token"),
                token_uri=token_data.get("token_uri"),
                client_id=token_data.get("client_id"),
                client_secret=token_data.get("client_secret"),
                scopes=token_data.get("scopes"),
            )
            if "expiry" in token_data and token_data["expiry"]:
                creds.expiry = datetime.fromisoformat(token_data["expiry"])
            return creds
        except Exception as e:
            logger.error("Failed to load credentials", error=str(e))
            return None

    def _save_credentials(self, service: str, channel_id: Optional[str], credentials: Credentials):
        token_file = self._get_token_file_path(service, channel_id)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        token_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": list(credentials.scopes) if credentials.scopes else [],
            "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
        }
        with open(token_file, "w") as f:
            json.dump(token_data, f)
        logger.info("Credentials saved", service=service, channel_id=channel_id)

    async def _authorize(self, service: str, channel_id: Optional[str]) -> Credentials:
        scopes = SCOPES.get(service, [])
        if not scopes:
            raise ValueError(f"Unknown service: {service}")
        flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets_file), scopes=scopes)
        credentials = flow.run_local_server(port=0)
        self._save_credentials(service, channel_id, credentials)
        logger.info("New authorization completed", service=service)
        return credentials

    def _get_token_file_path(self, service: str, channel_id: Optional[str]) -> Path:
        filename = f"token_{service}"
        if channel_id:
            filename += f"_{channel_id}"
        filename += ".json"
        return self.credentials_dir / filename

    def get_token_status(self, service: str, channel_id: Optional[str] = None) -> dict:
        cache_key = f"{service}:{channel_id or 'default'}"
        if cache_key not in self._credentials_cache:
            return {"status": "not_loaded", "service": service}
        creds = self._credentials_cache[cache_key]
        expiry = self._token_expiry_cache.get(cache_key)
        minutes_remaining = None
        if expiry:
            minutes_remaining = int((expiry - datetime.utcnow()).total_seconds() / 60)
        return {
            "status": "valid" if creds.valid else "expired",
            "service": service,
            "channel_id": channel_id,
            "expiry": expiry.isoformat() if expiry else None,
            "minutes_remaining": minutes_remaining,
            "needs_refresh": self._needs_preemptive_refresh(cache_key, self.PREEMPTIVE_REFRESH_MINUTES),
        }
