import os
from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..services.auth_manager import PreemptiveAuthManager
from ..utils.logger import logger


class SearchFactsInput(BaseModel):
    query: str = Field(description="Search query")
    purpose: Literal["fact_check", "entity_research", "competitor_analysis"] = Field(default="fact_check")
    num_results: int = Field(default=10, ge=1, le=20)
    include_snippets: bool = Field(default=True)
    include_entities: bool = Field(default=True)


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_authority: Literal["high", "medium", "low"]
    publish_date: Optional[datetime] = None


class Entity(BaseModel):
    name: str
    type: str
    description: str
    wiki_url: Optional[str] = None
    related_entities: List[str] = Field(default_factory=list)


class SearchFactsOutput(BaseModel):
    results: List[SearchResult]
    entities: List[Entity]
    knowledge_panel: Optional[dict] = None
    fact_check_summary: Optional[str] = None


class SearchService:
    """Google Search + Knowledge Graph service."""

    HIGH_AUTHORITY_DOMAINS = [
        "wikipedia.org",
        "gov.",
        "edu.",
        "bbc.com",
        "nytimes.com",
        "reuters.com",
        "ap.org",
        "nature.com",
        "sciencedirect.com",
    ]
    MEDIUM_AUTHORITY_DOMAINS = [
        "medium.com",
        "forbes.com",
        "techcrunch.com",
        "wired.com",
    ]

    def __init__(self, auth_manager: PreemptiveAuthManager):
        self.auth = auth_manager
        self._search_service = None
        self._kg_service = None

    def _get_search_service(self):
        if not self._search_service:
            from googleapiclient.discovery import build

            creds = self.auth._load_credentials("search", None)
            self._search_service = build("customsearch", "v1", credentials=creds)
        return self._search_service

    def _get_kg_service(self):
        if not self._kg_service:
            from googleapiclient.discovery import build

            api_key = os.getenv("GOOGLE_API_KEY")
            self._kg_service = build("kgsearch", "v1", developerKey=api_key)
        return self._kg_service

    async def search_facts(self, input_data: SearchFactsInput) -> SearchFactsOutput:
        results: List[SearchResult] = []
        entities: List[Entity] = []
        knowledge_panel = None

        try:
            search_service = self._get_search_service()
            search_response = (
                search_service.cse()
                .list(q=input_data.query, cx=os.getenv("GOOGLE_CSE_ID"), num=input_data.num_results)
                .execute()
            )

            for item in search_response.get("items", []):
                authority = self._assess_source_authority(item.get("link", ""))
                results.append(
                    SearchResult(
                        title=item.get("title", ""),
                        url=item.get("link", ""),
                        snippet=item.get("snippet", ""),
                        source_authority=authority,
                        publish_date=None,
                    )
                )

            if "knowledge_graph" in search_response:
                knowledge_panel = search_response["knowledge_graph"]

        except Exception as e:
            logger.error("Search API error", error=str(e))

        if input_data.include_entities:
            entities = await self._extract_entities(input_data.query)

        fact_summary = None
        if input_data.purpose == "fact_check":
            fact_summary = self._generate_fact_summary(results)

        return SearchFactsOutput(
            results=results,
            entities=entities,
            knowledge_panel=knowledge_panel,
            fact_check_summary=fact_summary,
        )

    async def _extract_entities(self, query: str) -> List[Entity]:
        try:
            kg_service = self._get_kg_service()
            response = kg_service.entities().search(query=query, limit=10, languages=["en"]).execute()

            entities = []
            for item in response.get("itemListElement", []):
                result = item.get("result", {})
                raw_type = result.get("@type", ["Unknown"])
                entity_type = raw_type[0] if isinstance(raw_type, list) else raw_type
                entities.append(
                    Entity(
                        name=result.get("name", ""),
                        type=entity_type,
                        description=result.get("description", ""),
                        wiki_url=result.get("detailedDescription", {}).get("url"),
                        related_entities=[],
                    )
                )
            return entities
        except Exception as e:
            logger.error("Knowledge Graph error", error=str(e))
            return []

    def _assess_source_authority(self, url: str) -> Literal["high", "medium", "low"]:
        for domain in self.HIGH_AUTHORITY_DOMAINS:
            if domain in url:
                return "high"
        for domain in self.MEDIUM_AUTHORITY_DOMAINS:
            if domain in url:
                return "medium"
        return "low"

    def _generate_fact_summary(self, results: List[SearchResult]) -> str:
        high_auth_count = sum(1 for r in results if r.source_authority == "high")
        if high_auth_count >= 3:
            return f"Found {high_auth_count} high-authority sources supporting this topic."
        elif high_auth_count >= 1:
            return f"Limited high-authority sources ({high_auth_count}). Recommend additional verification."
        else:
            return "No high-authority sources found. Treat claims with caution."
