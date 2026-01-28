import os
from typing import List, Optional

from ..utils.logger import logger


class KnowledgeGraphService:
    """Knowledge Graph API wrapper for entity lookup."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        self._service = None

    def _get_service(self):
        if not self._service:
            from googleapiclient.discovery import build

            self._service = build("kgsearch", "v1", developerKey=self.api_key)
        return self._service

    async def search_entities(self, query: str, limit: int = 10, languages: Optional[List[str]] = None) -> List[dict]:
        try:
            service = self._get_service()
            response = service.entities().search(query=query, limit=limit, languages=languages or ["en"]).execute()
            entities = []
            for item in response.get("itemListElement", []):
                result = item.get("result", {})
                raw_type = result.get("@type", ["Unknown"])
                entity_type = raw_type[0] if isinstance(raw_type, list) else raw_type
                entities.append(
                    {
                        "name": result.get("name", ""),
                        "type": entity_type,
                        "description": result.get("description", ""),
                        "detailed_description": result.get("detailedDescription", {}).get("articleBody", ""),
                        "wiki_url": result.get("detailedDescription", {}).get("url"),
                        "score": item.get("resultScore", 0),
                    }
                )
            return entities
        except Exception as e:
            logger.error("Knowledge Graph search error", error=str(e))
            return []
