from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class VideoPrivacy(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class ShortsConfig(BaseModel):
    is_short: bool = True
    disable_remix: bool = True


class PublishVideoInput(BaseModel):
    video_path: str = Field(description="Local video file path")
    title: str = Field(max_length=100)
    description: str = Field(max_length=5000)
    tags: List[str] = Field(default_factory=list)
    category_id: str = Field(default="22")
    privacy: VideoPrivacy = VideoPrivacy.PRIVATE
    localized_metadata: Optional[Dict[str, dict]] = None
    shorts_config: Optional[ShortsConfig] = None
    chapters: Optional[str] = None
    scheduled_publish_time: Optional[datetime] = None
    thumbnail_path: Optional[str] = None
    auto_comment: Optional[str] = None
    channel_id: Optional[str] = None


class PublishVideoOutput(BaseModel):
    success: bool
    video_id: Optional[str] = None
    video_url: Optional[str] = None
    shorts_url: Optional[str] = None
    thumbnail_set: bool = False
    comment_posted: bool = False
    comment_id: Optional[str] = None
    error: Optional[str] = None
    upload_duration_seconds: float = 0.0
    file_size_bytes: int = 0
