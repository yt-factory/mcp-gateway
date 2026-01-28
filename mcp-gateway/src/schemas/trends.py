from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TrendClassification(str, Enum):
    ESTABLISHED = "established"
    EMERGING = "emerging"
    FLEETING = "fleeting"
    EVERGREEN = "evergreen"


class TrendingTopicsInput(BaseModel):
    category: str = Field(description="Content category: technology, finance, health, entertainment, etc.")
    geo: str = Field(default="US", description="Geo code: US, GB, CN, JP, etc.")
    timeframe: str = Field(default="now 7-d", description="Timeframe: now 1-H, now 4-H, now 1-d, now 7-d, today 1-m")
    max_results: int = Field(default=10, ge=1, le=25, description="Number of results")
    include_related: bool = Field(default=True, description="Include related queries")


class TrendingTopic(BaseModel):
    keyword: str
    search_volume: int
    volume_change_percent: float
    classification: TrendClassification
    authority_score: int
    classification_factors: dict = Field(default_factory=dict)
    related_queries: List[str] = Field(default_factory=list)
    related_entities: List[str] = Field(default_factory=list)
    suggested_angles: List[str] = Field(default_factory=list)


class TrendingTopicsOutput(BaseModel):
    topics: List[TrendingTopic]
    cache_hit: bool
    cache_expires_at: Optional[datetime] = None
    api_quota_remaining: int
    clusters: Optional[list] = None
