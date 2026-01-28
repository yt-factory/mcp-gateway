from typing import Optional

import httpx

from ..utils.logger import logger


class WebhookService:
    """Sends completion notifications via webhook."""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url

    async def notify(self, event: str, data: dict) -> bool:
        if not self.webhook_url:
            return False
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.webhook_url, json={"event": event, "data": data}, timeout=10.0)
                return response.status_code < 400
        except Exception as e:
            logger.error("Webhook notification failed", event=event, error=str(e))
            return False
