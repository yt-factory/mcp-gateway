"""Monetization Dashboard for centralized revenue intelligence.

This module provides real-time monetization monitoring, performance tracking,
and optimization recommendations for YouTube content.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional

from ..utils.logger import logger


class MetricTrend(str, Enum):
    """Trend direction for metrics."""

    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"


class PerformanceLevel(str, Enum):
    """Performance level classification."""

    EXCELLENT = "excellent"  # Above target
    GOOD = "good"  # At target
    NEEDS_IMPROVEMENT = "needs_improvement"  # Below target
    CRITICAL = "critical"  # Significantly below target


@dataclass
class MetricTarget:
    """Target configuration for a metric."""

    name: str
    target_value: float
    unit: str
    optimization_tips: List[str]


@dataclass
class MetricValue:
    """Current value for a metric."""

    name: str
    current_value: float
    target_value: float
    unit: str
    performance_level: PerformanceLevel
    trend: MetricTrend
    change_percent: float  # vs previous period
    optimization_tips: List[str]


@dataclass
class RealtimeMetrics:
    """Real-time dashboard metrics."""

    active_viewers: int
    today_revenue: float
    today_views: int
    current_cpm: float
    top_performing_video: Optional[str]
    top_video_views: int
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class WeeklySummary:
    """Weekly performance summary."""

    week_start: datetime
    week_end: datetime
    total_revenue: float
    total_views: int
    total_watch_time_hours: float
    average_cpm: float
    average_rpm: float
    subscriber_growth: int
    best_performing_day: str
    worst_performing_day: str
    top_videos: List[Dict]
    metrics: List[MetricValue]


@dataclass
class TrendAnalysis:
    """Trend analysis results."""

    metric_name: str
    current_value: float
    previous_value: float
    change_percent: float
    trend: MetricTrend
    forecast_next_week: float
    confidence: float
    factors: List[str]


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation."""

    priority: int  # 1 = highest
    category: str
    title: str
    description: str
    expected_impact: str
    action_items: List[str]


@dataclass
class MonetizationDashboardReport:
    """Complete monetization dashboard report."""

    generated_at: datetime
    realtime: RealtimeMetrics
    weekly_summary: Optional[WeeklySummary]
    trend_analysis: List[TrendAnalysis]
    recommendations: List[OptimizationRecommendation]
    underperforming_videos: List[Dict]
    overall_health: PerformanceLevel


class MonetizationDashboard:
    """Centralized monetization intelligence dashboard.

    Monitors and optimizes 7 core metrics:
    - AVD: Average View Duration (target: 7 minutes)
    - CTR: Click-Through Rate (target: 8%)
    - CPM: Cost Per Mille (target: $10)
    - RPM: Revenue Per Mille (target: $6)
    - AIO_RATE: AI Overview Attribution Rate (target: 10%)
    - SUB_RATE: Subscriber Conversion Rate (target: 5%)
    - SHORTS_CONV: Shorts to Main Video Conversion (target: 3%)
    """

    # ============================================
    # METRIC TARGETS
    # ============================================

    METRIC_TARGETS = {
        "AVD": MetricTarget(
            name="Average View Duration",
            target_value=7.0,
            unit="minutes",
            optimization_tips=[
                "Add smart subtitles for better retention",
                "Use emotion effects at key moments",
                "Create compelling hooks in first 30 seconds",
                "Add chapter markers for navigation",
                "Optimize video pacing and editing",
            ],
        ),
        "CTR": MetricTarget(
            name="Click-Through Rate",
            target_value=8.0,
            unit="%",
            optimization_tips=[
                "A/B test thumbnails with different styles",
                "Use hot keywords in titles",
                "Create curiosity gaps in titles",
                "Ensure thumbnail-title consistency",
                "Test different color schemes",
            ],
        ),
        "CPM": MetricTarget(
            name="Cost Per Mille",
            target_value=10.0,
            unit="$",
            optimization_tips=[
                "Target high-value regions (US, UK, AU)",
                "Focus on Q4 for seasonal boost",
                "Create content in high-CPM verticals",
                "Optimize for advertiser-friendly content",
                "Increase video length for more ad slots",
            ],
        ),
        "RPM": MetricTarget(
            name="Revenue Per Mille",
            target_value=6.0,
            unit="$",
            optimization_tips=[
                "Diversify revenue streams",
                "Add affiliate links in descriptions",
                "Enable channel memberships",
                "Promote merchandise",
                "Create sponsored content opportunities",
            ],
        ),
        "AIO_RATE": MetricTarget(
            name="AI Overview Attribution Rate",
            target_value=10.0,
            unit="%",
            optimization_tips=[
                "Optimize FAQ structure for featured snippets",
                "Use clear question-answer format",
                "Target long-tail keywords",
                "Include structured data markup",
                "Create comprehensive topic coverage",
            ],
        ),
        "SUB_RATE": MetricTarget(
            name="Subscriber Conversion Rate",
            target_value=5.0,
            unit="%",
            optimization_tips=[
                "Add compelling CTAs at optimal moments",
                "Create end screens with subscribe buttons",
                "Offer value propositions for subscribing",
                "Engage with comments to build community",
                "Create series content for return viewers",
            ],
        ),
        "SHORTS_CONV": MetricTarget(
            name="Shorts to Main Video Conversion",
            target_value=3.0,
            unit="%",
            optimization_tips=[
                "Add emotion hooks linking to main content",
                "Use Shorts as teasers for longer videos",
                "Include clear CTAs to watch full video",
                "Create complementary Shorts content",
                "Pin comments with links to main videos",
            ],
        ),
    }

    # ============================================
    # PERFORMANCE THRESHOLDS
    # ============================================

    PERFORMANCE_THRESHOLDS = {
        "excellent": 1.2,  # 120% of target
        "good": 0.9,  # 90% of target
        "needs_improvement": 0.6,  # 60% of target
        # Below 60% = critical
    }

    def __init__(self, analytics_service=None):
        """Initialize the monetization dashboard.

        Args:
            analytics_service: Optional analytics service for real data
        """
        self.analytics = analytics_service
        self._metrics_cache: Dict[str, List[MetricValue]] = {}
        self._history: List[MonetizationDashboardReport] = []

    async def get_dashboard_report(
        self,
        channel_id: Optional[str] = None,
        include_weekly: bool = True,
        include_trends: bool = True,
        include_recommendations: bool = True,
    ) -> MonetizationDashboardReport:
        """Generate comprehensive dashboard report.

        Args:
            channel_id: Optional channel ID for multi-channel support
            include_weekly: Include weekly summary
            include_trends: Include trend analysis
            include_recommendations: Include optimization recommendations

        Returns:
            MonetizationDashboardReport with all requested data
        """
        # Get realtime metrics
        realtime = await self._get_realtime_metrics(channel_id)

        # Get weekly summary if requested
        weekly = None
        if include_weekly:
            weekly = await self._get_weekly_summary(channel_id)

        # Get trend analysis if requested
        trends = []
        if include_trends:
            trends = await self._analyze_trends(channel_id)

        # Get recommendations if requested
        recommendations = []
        if include_recommendations:
            recommendations = await self._generate_recommendations(realtime, weekly, trends)

        # Get underperforming videos
        underperforming = await self._get_underperforming_videos(channel_id)

        # Calculate overall health
        overall_health = self._calculate_overall_health(weekly)

        report = MonetizationDashboardReport(
            generated_at=datetime.utcnow(),
            realtime=realtime,
            weekly_summary=weekly,
            trend_analysis=trends,
            recommendations=recommendations,
            underperforming_videos=underperforming,
            overall_health=overall_health,
        )

        # Store in history
        self._history.append(report)

        logger.info(
            "Dashboard report generated",
            overall_health=overall_health.value,
            recommendations_count=len(recommendations),
        )

        return report

    async def get_metric_details(
        self,
        metric_name: str,
        channel_id: Optional[str] = None,
        days: int = 30,
    ) -> Dict:
        """Get detailed analysis for a specific metric.

        Args:
            metric_name: One of AVD, CTR, CPM, RPM, AIO_RATE, SUB_RATE, SHORTS_CONV
            channel_id: Optional channel ID
            days: Number of days to analyze

        Returns:
            Detailed metric analysis
        """
        if metric_name not in self.METRIC_TARGETS:
            return {"error": f"Unknown metric: {metric_name}"}

        target = self.METRIC_TARGETS[metric_name]

        # Get historical data (simulated)
        history = await self._get_metric_history(metric_name, channel_id, days)

        # Calculate statistics
        if history:
            current_value = history[-1]
            avg_value = sum(history) / len(history)
            min_value = min(history)
            max_value = max(history)

            # Calculate trend
            if len(history) >= 7:
                recent_avg = sum(history[-7:]) / 7
                previous_avg = sum(history[-14:-7]) / 7 if len(history) >= 14 else avg_value
                change = ((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
            else:
                change = 0
        else:
            current_value = 0
            avg_value = 0
            min_value = 0
            max_value = 0
            change = 0

        performance = self._classify_performance(current_value, target.target_value)

        return {
            "metric_name": metric_name,
            "display_name": target.name,
            "unit": target.unit,
            "target_value": target.target_value,
            "current_value": round(current_value, 2),
            "average_value": round(avg_value, 2),
            "min_value": round(min_value, 2),
            "max_value": round(max_value, 2),
            "change_percent": round(change, 1),
            "performance_level": performance.value,
            "days_analyzed": days,
            "optimization_tips": target.optimization_tips,
            "history": [round(v, 2) for v in history[-30:]],  # Last 30 days
        }

    async def _get_realtime_metrics(
        self,
        channel_id: Optional[str],
    ) -> RealtimeMetrics:
        """Get real-time metrics."""
        # In production, this would call YouTube Analytics API
        # For now, return simulated data

        return RealtimeMetrics(
            active_viewers=0,
            today_revenue=0.0,
            today_views=0,
            current_cpm=0.0,
            top_performing_video=None,
            top_video_views=0,
        )

    async def _get_weekly_summary(
        self,
        channel_id: Optional[str],
    ) -> WeeklySummary:
        """Get weekly performance summary."""
        now = datetime.utcnow()
        week_start = now - timedelta(days=7)

        # Calculate metrics
        metrics = []
        for metric_name, target in self.METRIC_TARGETS.items():
            current_value = await self._get_current_metric_value(metric_name, channel_id)
            previous_value = await self._get_previous_metric_value(metric_name, channel_id)

            if previous_value > 0:
                change = ((current_value - previous_value) / previous_value) * 100
            else:
                change = 0

            trend = self._determine_trend(change)
            performance = self._classify_performance(current_value, target.target_value)

            metrics.append(
                MetricValue(
                    name=metric_name,
                    current_value=round(current_value, 2),
                    target_value=target.target_value,
                    unit=target.unit,
                    performance_level=performance,
                    trend=trend,
                    change_percent=round(change, 1),
                    optimization_tips=target.optimization_tips[:2],  # Top 2 tips
                )
            )

        return WeeklySummary(
            week_start=week_start,
            week_end=now,
            total_revenue=0.0,
            total_views=0,
            total_watch_time_hours=0.0,
            average_cpm=0.0,
            average_rpm=0.0,
            subscriber_growth=0,
            best_performing_day="",
            worst_performing_day="",
            top_videos=[],
            metrics=metrics,
        )

    async def _analyze_trends(
        self,
        channel_id: Optional[str],
    ) -> List[TrendAnalysis]:
        """Analyze trends for all metrics."""
        trends = []

        for metric_name, target in self.METRIC_TARGETS.items():
            current = await self._get_current_metric_value(metric_name, channel_id)
            previous = await self._get_previous_metric_value(metric_name, channel_id)

            if previous > 0:
                change = ((current - previous) / previous) * 100
            else:
                change = 0

            trend = self._determine_trend(change)

            # Simple forecast (linear projection)
            forecast = current * (1 + change / 100) if change != 0 else current

            # Identify factors affecting the metric
            factors = self._identify_trend_factors(metric_name, trend, change)

            trends.append(
                TrendAnalysis(
                    metric_name=metric_name,
                    current_value=round(current, 2),
                    previous_value=round(previous, 2),
                    change_percent=round(change, 1),
                    trend=trend,
                    forecast_next_week=round(forecast, 2),
                    confidence=0.7 if abs(change) < 20 else 0.5,
                    factors=factors,
                )
            )

        return trends

    async def _generate_recommendations(
        self,
        realtime: RealtimeMetrics,
        weekly: Optional[WeeklySummary],
        trends: List[TrendAnalysis],
    ) -> List[OptimizationRecommendation]:
        """Generate prioritized optimization recommendations."""
        recommendations = []
        priority = 1

        if not weekly:
            return recommendations

        # Analyze each metric and generate recommendations
        for metric in weekly.metrics:
            if metric.performance_level in [
                PerformanceLevel.NEEDS_IMPROVEMENT,
                PerformanceLevel.CRITICAL,
            ]:
                target = self.METRIC_TARGETS.get(metric.name)
                if target:
                    rec = OptimizationRecommendation(
                        priority=priority,
                        category=metric.name,
                        title=f"Improve {target.name}",
                        description=(
                            f"Current {metric.name} is {metric.current_value}{metric.unit}, "
                            f"below target of {metric.target_value}{metric.unit}."
                        ),
                        expected_impact=self._estimate_impact(metric.name, metric.current_value, target.target_value),
                        action_items=target.optimization_tips[:3],
                    )
                    recommendations.append(rec)
                    priority += 1

        # Add trend-based recommendations
        for trend in trends:
            if trend.trend == MetricTrend.DECLINING and trend.change_percent < -10:
                target = self.METRIC_TARGETS.get(trend.metric_name)
                if target:
                    rec = OptimizationRecommendation(
                        priority=priority,
                        category=trend.metric_name,
                        title=f"Address Declining {target.name}",
                        description=(
                            f"{trend.metric_name} has declined {abs(trend.change_percent):.1f}% "
                            f"from {trend.previous_value} to {trend.current_value}."
                        ),
                        expected_impact="Stabilize metric and prevent further decline",
                        action_items=trend.factors + target.optimization_tips[:2],
                    )
                    recommendations.append(rec)
                    priority += 1

        # Sort by priority
        recommendations.sort(key=lambda r: r.priority)

        return recommendations[:10]  # Top 10 recommendations

    async def _get_underperforming_videos(
        self,
        channel_id: Optional[str],
    ) -> List[Dict]:
        """Get list of underperforming videos that need attention."""
        # In production, this would analyze video performance
        return []

    def _calculate_overall_health(
        self,
        weekly: Optional[WeeklySummary],
    ) -> PerformanceLevel:
        """Calculate overall monetization health."""
        if not weekly or not weekly.metrics:
            return PerformanceLevel.NEEDS_IMPROVEMENT

        performance_scores = {
            PerformanceLevel.EXCELLENT: 4,
            PerformanceLevel.GOOD: 3,
            PerformanceLevel.NEEDS_IMPROVEMENT: 2,
            PerformanceLevel.CRITICAL: 1,
        }

        total_score = sum(performance_scores.get(m.performance_level, 2) for m in weekly.metrics)
        avg_score = total_score / len(weekly.metrics)

        if avg_score >= 3.5:
            return PerformanceLevel.EXCELLENT
        elif avg_score >= 2.5:
            return PerformanceLevel.GOOD
        elif avg_score >= 1.5:
            return PerformanceLevel.NEEDS_IMPROVEMENT
        else:
            return PerformanceLevel.CRITICAL

    def _classify_performance(
        self,
        current: float,
        target: float,
    ) -> PerformanceLevel:
        """Classify performance level based on current vs target."""
        if target == 0:
            return PerformanceLevel.NEEDS_IMPROVEMENT

        ratio = current / target

        if ratio >= self.PERFORMANCE_THRESHOLDS["excellent"]:
            return PerformanceLevel.EXCELLENT
        elif ratio >= self.PERFORMANCE_THRESHOLDS["good"]:
            return PerformanceLevel.GOOD
        elif ratio >= self.PERFORMANCE_THRESHOLDS["needs_improvement"]:
            return PerformanceLevel.NEEDS_IMPROVEMENT
        else:
            return PerformanceLevel.CRITICAL

    def _determine_trend(self, change_percent: float) -> MetricTrend:
        """Determine trend based on change percentage."""
        if change_percent > 5:
            return MetricTrend.IMPROVING
        elif change_percent < -5:
            return MetricTrend.DECLINING
        else:
            return MetricTrend.STABLE

    def _identify_trend_factors(
        self,
        metric_name: str,
        trend: MetricTrend,
        change: float,
    ) -> List[str]:
        """Identify factors affecting a metric trend."""
        factors = []

        if trend == MetricTrend.DECLINING:
            factors.append(f"Review recent content changes for {metric_name} impact")
            factors.append("Check for seasonal patterns")
            factors.append("Analyze competitor activity")
        elif trend == MetricTrend.IMPROVING:
            factors.append("Identify successful content patterns")
            factors.append("Scale winning strategies")
        else:
            factors.append("Maintain current strategy")
            factors.append("Test incremental optimizations")

        return factors

    def _estimate_impact(
        self,
        metric_name: str,
        current: float,
        target: float,
    ) -> str:
        """Estimate impact of improving a metric."""
        gap = target - current
        gap_percent = (gap / target * 100) if target > 0 else 0

        impact_estimates = {
            "CPM": f"Potential ${gap:.2f} increase per 1000 views",
            "RPM": f"Potential ${gap:.2f} increase in revenue per 1000 views",
            "CTR": f"Potential {gap:.1f}% more clicks from impressions",
            "AVD": f"Potential {gap:.1f} minutes more watch time per view",
            "AIO_RATE": f"Potential {gap:.1f}% more search visibility",
            "SUB_RATE": f"Potential {gap:.1f}% more subscriber conversions",
            "SHORTS_CONV": f"Potential {gap:.1f}% more main video traffic from Shorts",
        }

        return impact_estimates.get(metric_name, f"Potential {gap_percent:.1f}% improvement")

    async def _get_current_metric_value(
        self,
        metric_name: str,
        channel_id: Optional[str],
    ) -> float:
        """Get current value for a metric (simulated)."""
        # In production, this would fetch from YouTube Analytics
        # Return simulated baseline values
        baselines = {
            "AVD": 5.5,
            "CTR": 6.2,
            "CPM": 8.5,
            "RPM": 4.8,
            "AIO_RATE": 7.5,
            "SUB_RATE": 3.8,
            "SHORTS_CONV": 2.1,
        }
        return baselines.get(metric_name, 0.0)

    async def _get_previous_metric_value(
        self,
        metric_name: str,
        channel_id: Optional[str],
    ) -> float:
        """Get previous period value for a metric (simulated)."""
        # In production, this would fetch from YouTube Analytics
        baselines = {
            "AVD": 5.2,
            "CTR": 6.0,
            "CPM": 8.2,
            "RPM": 4.5,
            "AIO_RATE": 7.0,
            "SUB_RATE": 3.5,
            "SHORTS_CONV": 1.9,
        }
        return baselines.get(metric_name, 0.0)

    async def _get_metric_history(
        self,
        metric_name: str,
        channel_id: Optional[str],
        days: int,
    ) -> List[float]:
        """Get historical values for a metric (simulated)."""
        import random

        base = await self._get_current_metric_value(metric_name, channel_id)
        # Generate simulated history with some variance
        history = []
        for i in range(days):
            variance = random.uniform(-0.15, 0.15)
            value = base * (1 + variance)
            history.append(max(0, value))
        return history


# Global instance
monetization_dashboard = MonetizationDashboard()
