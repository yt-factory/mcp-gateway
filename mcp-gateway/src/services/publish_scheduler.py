from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional


class ContentType(str, Enum):
    MAIN_VIDEO = "main_video"
    SHORTS = "shorts"


class AudienceRegion(str, Enum):
    US = "US"
    UK = "UK"
    EU = "EU"
    ASIA = "ASIA"
    GLOBAL = "GLOBAL"


@dataclass
class PublishWindow:
    optimal_time: datetime
    window_start: datetime
    window_end: datetime
    confidence: float
    rationale: str
    alternative_times: Optional[List[datetime]] = None


@dataclass
class AudienceInsight:
    peak_hours: List[int]
    peak_days: List[int]
    timezone: str
    avg_session_length_minutes: float


class PublishScheduler:
    """Calculates optimal publish times based on audience analysis."""

    DEFAULT_PEAK_HOURS = {
        ContentType.MAIN_VIDEO: [14, 15, 16, 17, 18],
        ContentType.SHORTS: [11, 12, 19, 20, 21],
    }
    DEFAULT_PEAK_DAYS = [1, 2, 3, 4]

    TIMEZONE_OFFSETS = {
        AudienceRegion.US: -5,
        AudienceRegion.UK: 0,
        AudienceRegion.EU: 1,
        AudienceRegion.ASIA: 8,
        AudienceRegion.GLOBAL: -5,
    }

    def __init__(self, analytics_service=None):
        self.analytics = analytics_service
        self._audience_cache: Dict[str, AudienceInsight] = {}

    async def get_optimal_publish_time(
        self,
        channel_id: Optional[str] = None,
        content_type: ContentType = ContentType.MAIN_VIDEO,
        target_audience: AudienceRegion = AudienceRegion.GLOBAL,
        earliest_publish: Optional[datetime] = None,
    ) -> PublishWindow:
        earliest = earliest_publish or datetime.utcnow()
        audience = await self._get_audience_insight(channel_id, target_audience)
        optimal = self._calculate_optimal_time(content_type, audience, earliest)
        window_start = optimal - timedelta(hours=1)
        window_end = optimal + timedelta(hours=2)
        alternatives = self._generate_alternatives(optimal, content_type, audience, 3)
        confidence = self._calculate_confidence(channel_id, audience)
        rationale = self._generate_rationale(optimal, content_type, audience)

        return PublishWindow(
            optimal_time=optimal,
            window_start=window_start,
            window_end=window_end,
            confidence=confidence,
            rationale=rationale,
            alternative_times=alternatives,
        )

    async def _get_audience_insight(self, channel_id: Optional[str], region: AudienceRegion) -> AudienceInsight:
        cache_key = f"{channel_id or 'default'}:{region.value}"
        if cache_key in self._audience_cache:
            return self._audience_cache[cache_key]

        default_insight = AudienceInsight(
            peak_hours=self.DEFAULT_PEAK_HOURS[ContentType.MAIN_VIDEO],
            peak_days=self.DEFAULT_PEAK_DAYS,
            timezone=f"UTC{self.TIMEZONE_OFFSETS[region]:+d}",
            avg_session_length_minutes=8.0,
        )
        self._audience_cache[cache_key] = default_insight
        return default_insight

    def _calculate_optimal_time(
        self, content_type: ContentType, audience: AudienceInsight, earliest: datetime
    ) -> datetime:
        tz_offset = self._parse_timezone_offset(audience.timezone)
        local_now = earliest + timedelta(hours=tz_offset)
        peak_hours = audience.peak_hours or self.DEFAULT_PEAK_HOURS[content_type]
        peak_days = audience.peak_days or self.DEFAULT_PEAK_DAYS

        for days_ahead in range(7):
            check_date = local_now + timedelta(days=days_ahead)
            if check_date.weekday() not in peak_days:
                continue
            for hour in sorted(peak_hours):
                candidate_time = check_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                optimal_utc = candidate_time - timedelta(hours=tz_offset)
                if optimal_utc >= earliest:
                    return optimal_utc

        tomorrow = local_now + timedelta(days=1)
        first_peak = sorted(peak_hours)[0]
        fallback = tomorrow.replace(hour=first_peak, minute=0, second=0)
        return fallback - timedelta(hours=tz_offset)

    def _generate_alternatives(
        self, optimal: datetime, content_type: ContentType, audience: AudienceInsight, count: int
    ) -> List[datetime]:
        alternatives = []
        peak_hours = audience.peak_hours or self.DEFAULT_PEAK_HOURS[content_type]
        for delta_days in [0, 1, 2]:
            for hour in peak_hours:
                alt = optimal.replace(hour=hour) + timedelta(days=delta_days)
                if alt != optimal and alt > datetime.utcnow():
                    alternatives.append(alt)
                if len(alternatives) >= count:
                    return alternatives
        return alternatives

    def _calculate_confidence(self, channel_id: Optional[str], audience: AudienceInsight) -> float:
        base = 0.5
        if channel_id:
            base += 0.2
        if audience.avg_session_length_minutes > 0:
            base += 0.1
        if len(audience.peak_hours) > 2:
            base += 0.1
        return min(base, 0.95)

    def _generate_rationale(self, optimal: datetime, content_type: ContentType, audience: AudienceInsight) -> str:
        day_name = optimal.strftime("%A")
        hour = optimal.strftime("%I %p")
        content_desc = "video" if content_type == ContentType.MAIN_VIDEO else "Short"
        return (
            f"Recommended to publish this {content_desc} on {day_name} at {hour} "
            f"({audience.timezone}). This aligns with audience peak activity hours "
            f"({', '.join(f'{h}:00' for h in audience.peak_hours[:3])}...)."
        )

    def _parse_timezone_offset(self, timezone: str) -> int:
        if timezone.startswith("UTC"):
            try:
                return int(timezone[3:])
            except ValueError:
                return 0
        return 0
