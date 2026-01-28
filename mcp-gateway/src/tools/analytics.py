from datetime import date, timedelta
from typing import List

from googleapiclient.discovery import build

from ..schemas.analytics import AnalyticsInput, AnalyticsOutput, VideoMetrics
from ..services.auth_manager import PreemptiveAuthManager
from ..utils.logger import logger


class AnalyticsService:
    """YouTube Analytics service with A/B testing support."""

    def __init__(self, auth_manager: PreemptiveAuthManager):
        self.auth = auth_manager
        self._analytics_service = None

    def _get_analytics_service(self):
        if not self._analytics_service:
            creds = self.auth._load_credentials("youtube_analytics", None)
            self._analytics_service = build("youtubeAnalytics", "v2", credentials=creds)
        return self._analytics_service

    async def get_analytics(self, input_data: AnalyticsInput) -> AnalyticsOutput:
        end_date = input_data.end_date or date.today()
        start_date = input_data.start_date or (end_date - timedelta(days=28))

        videos_metrics: List[VideoMetrics] = []

        for video_id in input_data.video_ids:
            try:
                analytics = self._get_analytics_service()
                response = (
                    analytics.reports()
                    .query(
                        ids="channel==MINE",
                        startDate=start_date.isoformat(),
                        endDate=end_date.isoformat(),
                        metrics=",".join(input_data.metrics),
                        filters=f"video=={video_id}",
                    )
                    .execute()
                )

                if response.get("rows"):
                    row = response["rows"][0]
                    metrics_data = dict(zip([h["name"] for h in response["columnHeaders"]], row))

                    views = metrics_data.get("views", 0)
                    likes = metrics_data.get("likes", 0)
                    comments = metrics_data.get("comments", 0)
                    shares = metrics_data.get("shares", 0)

                    engagement_rate = 0.0
                    if views > 0:
                        engagement_rate = (likes + comments + shares) / views * 100

                    avg_view_percentage = metrics_data.get("averageViewPercentage", 0)
                    retention_score = min(avg_view_percentage / 100, 1.0)

                    video_metrics = VideoMetrics(
                        video_id=video_id,
                        views=views,
                        likes=likes,
                        comments=comments,
                        shares=shares,
                        watch_time_minutes=metrics_data.get("estimatedMinutesWatched", 0),
                        average_view_duration_seconds=metrics_data.get("averageViewDuration", 0),
                        average_view_percentage=avg_view_percentage,
                        engagement_rate=round(engagement_rate, 2),
                        retention_score=round(retention_score, 2),
                    )

                    if input_data.include_demographics:
                        video_metrics.demographics = await self._get_demographics(video_id, start_date, end_date)
                    if input_data.include_traffic_sources:
                        video_metrics.traffic_sources = await self._get_traffic_sources(video_id, start_date, end_date)

                    videos_metrics.append(video_metrics)

            except Exception as e:
                logger.error("Analytics error for video", video_id=video_id, error=str(e))

        total_views = sum(v.views for v in videos_metrics)
        total_watch_time = sum(v.watch_time_minutes for v in videos_metrics)
        best_video = max(videos_metrics, key=lambda v: v.views) if videos_metrics else None

        ab_analysis = None
        if len(videos_metrics) == 2:
            ab_analysis = self._analyze_ab_test(videos_metrics[0], videos_metrics[1])

        return AnalyticsOutput(
            videos=videos_metrics,
            total_views=total_views,
            total_watch_time_minutes=total_watch_time,
            best_performing_video=best_video.video_id if best_video else None,
            ab_analysis=ab_analysis,
        )

    async def _get_demographics(self, video_id: str, start_date: date, end_date: date) -> dict:
        try:
            analytics = self._get_analytics_service()
            response = (
                analytics.reports()
                .query(
                    ids="channel==MINE",
                    startDate=start_date.isoformat(),
                    endDate=end_date.isoformat(),
                    metrics="viewerPercentage",
                    dimensions="ageGroup,gender",
                    filters=f"video=={video_id}",
                )
                .execute()
            )
            demographics: dict = {"age": {}, "gender": {}}
            for row in response.get("rows", []):
                age_group, gender, percentage = row
                demographics["age"][age_group] = demographics["age"].get(age_group, 0) + percentage
                demographics["gender"][gender] = demographics["gender"].get(gender, 0) + percentage
            return demographics
        except Exception as e:
            logger.error("Demographics error", video_id=video_id, error=str(e))
            return {}

    async def _get_traffic_sources(self, video_id: str, start_date: date, end_date: date) -> dict:
        try:
            analytics = self._get_analytics_service()
            response = (
                analytics.reports()
                .query(
                    ids="channel==MINE",
                    startDate=start_date.isoformat(),
                    endDate=end_date.isoformat(),
                    metrics="views",
                    dimensions="insightTrafficSourceType",
                    filters=f"video=={video_id}",
                )
                .execute()
            )
            sources = {}
            for row in response.get("rows", []):
                source, views = row
                sources[source] = views
            return sources
        except Exception as e:
            logger.error("Traffic sources error", video_id=video_id, error=str(e))
            return {}

    def _analyze_ab_test(self, variant_a: VideoMetrics, variant_b: VideoMetrics) -> dict:
        winner_views = "A" if variant_a.views > variant_b.views else "B"
        winner_engagement = "A" if variant_a.engagement_rate > variant_b.engagement_rate else "B"
        winner_retention = "A" if variant_a.retention_score > variant_b.retention_score else "B"

        views_improvement = 0.0
        if min(variant_a.views, variant_b.views) > 0:
            better = max(variant_a.views, variant_b.views)
            worse = min(variant_a.views, variant_b.views)
            views_improvement = ((better - worse) / worse) * 100

        return {
            "winner_overall": winner_views,
            "winner_by_metric": {
                "views": winner_views,
                "engagement": winner_engagement,
                "retention": winner_retention,
            },
            "improvement_percent": {"views": round(views_improvement, 1)},
            "recommendation": (
                f"Variant {winner_views} performed better overall. Consider using similar elements for future videos."
            ),
        }
