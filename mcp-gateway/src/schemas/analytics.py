from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalyticsInput(BaseModel):
    video_ids: List[str] = Field(description="Video ID list")
    metrics: List[str] = Field(
        default=["views", "likes", "comments", "shares", "estimatedMinutesWatched", "averageViewDuration"],
    )
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    include_demographics: bool = False
    include_traffic_sources: bool = False


class VideoMetrics(BaseModel):
    video_id: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    watch_time_minutes: float = 0.0
    average_view_duration_seconds: float = 0.0
    average_view_percentage: float = 0.0
    engagement_rate: float = 0.0
    retention_score: float = 0.0
    demographics: Optional[dict] = None
    traffic_sources: Optional[dict] = None


class AnalyticsOutput(BaseModel):
    videos: List[VideoMetrics]
    total_views: int = 0
    total_watch_time_minutes: float = 0.0
    best_performing_video: Optional[str] = None
    ab_analysis: Optional[dict] = None
