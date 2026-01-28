from datetime import datetime, timedelta
from typing import List, Optional

import httpx
from pytrends.request import TrendReq

from ..schemas.trends import (
    TrendClassification,
    TrendingTopic,
    TrendingTopicsInput,
    TrendingTopicsOutput,
)
from ..services.cache_manager import CacheManager
from ..services.entity_clusterer import EntityClusterer
from ..services.rate_limiter import RateLimiter
from ..utils.logger import logger


class TrendClassifier:
    """Classifies trends into established/emerging/fleeting/evergreen."""

    AUTHORITY_WEIGHTS = {
        "news_coverage": 0.30,
        "wikipedia_exists": 0.20,
        "days_trending": 0.20,
        "search_volume_stability": 0.15,
        "academic_mentions": 0.15,
    }

    THRESHOLDS = {
        "established_authority": 70,
        "established_days": 7,
        "emerging_growth": 200,
        "emerging_news": 5,
        "fleeting_authority": 40,
        "evergreen_history_days": 365,
    }

    async def classify(
        self,
        keyword: str,
        trend_data: dict,
        news_data: Optional[dict] = None,
        historical_data: Optional[dict] = None,
    ) -> tuple[TrendClassification, int, dict]:
        factors = {}

        news_count = news_data.get("total_results", 0) if news_data else 0
        factors["news_coverage_count"] = news_count
        news_score = min(news_count / 20, 1.0)

        has_wikipedia = await self._check_wikipedia(keyword)
        factors["has_wikipedia"] = has_wikipedia
        wiki_score = 1.0 if has_wikipedia else 0.0

        days_trending = self._calculate_days_trending(trend_data)
        factors["days_trending"] = days_trending
        days_score = min(days_trending / 30, 1.0)

        stability = self._calculate_stability(trend_data)
        factors["search_volume_stability"] = stability

        authority_score = int(
            (
                news_score * self.AUTHORITY_WEIGHTS["news_coverage"]
                + wiki_score * self.AUTHORITY_WEIGHTS["wikipedia_exists"]
                + days_score * self.AUTHORITY_WEIGHTS["days_trending"]
                + stability * self.AUTHORITY_WEIGHTS["search_volume_stability"]
                + 0 * self.AUTHORITY_WEIGHTS["academic_mentions"]
            )
            * 100
        )

        volume_change = trend_data.get("volume_change_percent", 0)
        factors["volume_change_24h"] = volume_change
        factors["social_velocity"] = trend_data.get("social_velocity", 0)

        classification = self._decide_classification(
            authority_score=authority_score,
            days_trending=days_trending,
            volume_change=volume_change,
            news_count=news_count,
            has_historical=historical_data is not None and len(historical_data.get("data", [])) > 0,
        )

        return classification, authority_score, factors

    def _decide_classification(
        self, authority_score: int, days_trending: int, volume_change: float, news_count: int, has_historical: bool
    ) -> TrendClassification:
        if has_historical and authority_score > 60:
            return TrendClassification.EVERGREEN
        if (
            authority_score >= self.THRESHOLDS["established_authority"]
            and days_trending >= self.THRESHOLDS["established_days"]
        ):
            return TrendClassification.ESTABLISHED
        if volume_change >= self.THRESHOLDS["emerging_growth"] and news_count >= self.THRESHOLDS["emerging_news"]:
            return TrendClassification.EMERGING
        if authority_score < self.THRESHOLDS["fleeting_authority"]:
            return TrendClassification.FLEETING
        return TrendClassification.EMERGING

    async def _check_wikipedia(self, keyword: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={"action": "query", "titles": keyword, "format": "json"},
                    timeout=5.0,
                )
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                return "-1" not in pages
        except Exception:
            return False

    def _calculate_days_trending(self, trend_data: dict) -> int:
        timeline = trend_data.get("timeline", [])
        if not timeline:
            return 1
        consecutive_days = 0
        for point in reversed(timeline):
            if point.get("value", 0) > 0:
                consecutive_days += 1
            else:
                break
        return max(consecutive_days, 1)

    def _calculate_stability(self, trend_data: dict) -> float:
        timeline = trend_data.get("timeline", [])
        if not timeline or len(timeline) < 2:
            return 0.5
        values = [p.get("value", 0) for p in timeline]
        mean = sum(values) / len(values)
        if mean == 0:
            return 0.0
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        stddev = variance**0.5
        cv = stddev / mean if mean > 0 else 1
        return round(max(0, 1 - cv), 2)


class TrendsService:
    """Google Trends service with caching and rate limiting."""

    def __init__(
        self, cache_manager: CacheManager, rate_limiter: RateLimiter, entity_clusterer: Optional[EntityClusterer] = None
    ):
        self.cache = cache_manager
        self.rate_limiter = rate_limiter
        self.classifier = TrendClassifier()
        self.entity_clusterer = entity_clusterer
        self.pytrends = TrendReq(hl="en-US", tz=360)

    async def get_trending_topics(
        self, input_data: TrendingTopicsInput, include_clusters: bool = True
    ) -> TrendingTopicsOutput:
        cache_key = f"trends:{input_data.category}:{input_data.geo}:{input_data.timeframe}"

        cached = await self.cache.get(cache_key)
        if cached:
            logger.info("Trends cache hit", cache_key=cache_key)
            return TrendingTopicsOutput(
                topics=[TrendingTopic(**t) if isinstance(t, dict) else t for t in cached["topics"]],
                cache_hit=True,
                cache_expires_at=cached.get("expires_at"),
                api_quota_remaining=self.rate_limiter.get_remaining("trends"),
                clusters=cached.get("clusters"),
            )

        await self.rate_limiter.acquire("trends")

        try:
            self.pytrends.build_payload(
                kw_list=[input_data.category], cat=0, timeframe=input_data.timeframe, geo=input_data.geo
            )

            trending_searches = self.pytrends.trending_searches(pn=input_data.geo.lower())

            topics: List[TrendingTopic] = []
            for idx, row in trending_searches.head(input_data.max_results).iterrows():
                keyword = row.iloc[0] if hasattr(row, "iloc") else str(row)

                trend_data = await self._get_keyword_trend_data(keyword, input_data)
                news_data = await self._get_news_coverage(keyword)

                classification, authority_score, factors = await self.classifier.classify(
                    keyword=keyword, trend_data=trend_data, news_data=news_data
                )

                suggested_angles = self._generate_angles(keyword, classification)

                topics.append(
                    TrendingTopic(
                        keyword=str(keyword),
                        search_volume=trend_data.get("search_volume", 0),
                        volume_change_percent=trend_data.get("volume_change_percent", 0),
                        classification=classification,
                        authority_score=authority_score,
                        classification_factors=factors,
                        related_queries=trend_data.get("related", [])[:5],
                        related_entities=[],
                        suggested_angles=suggested_angles,
                    )
                )

            # Entity clustering
            clusters = None
            if include_clusters and self.entity_clusterer and len(topics) >= 2:
                trend_dicts = [{"keyword": t.keyword, "authority_score": t.authority_score} for t in topics]
                cluster_results = await self.entity_clusterer.cluster_trends(trend_dicts)
                clusters = [
                    {
                        "primary_keyword": c.primary_keyword,
                        "related_keywords": c.related_keywords,
                        "cluster_score": c.cluster_score,
                        "suggested_title": c.suggested_title,
                        "combined_authority": c.combined_authority,
                        "rationale": c.rationale,
                    }
                    for c in cluster_results
                ]

            cache_expires = datetime.utcnow() + timedelta(hours=1)
            await self.cache.set(
                cache_key,
                {
                    "topics": [t.model_dump() for t in topics],
                    "expires_at": cache_expires.isoformat(),
                    "clusters": clusters,
                },
                ttl=3600,
            )

            return TrendingTopicsOutput(
                topics=topics,
                cache_hit=False,
                cache_expires_at=cache_expires,
                api_quota_remaining=self.rate_limiter.get_remaining("trends"),
                clusters=clusters,
            )

        except Exception as e:
            logger.error("Trends API error", error=str(e))
            raise

    async def _get_keyword_trend_data(self, keyword: str, input_data: TrendingTopicsInput) -> dict:
        try:
            self.pytrends.build_payload(kw_list=[keyword], timeframe=input_data.timeframe, geo=input_data.geo)
            interest_over_time = self.pytrends.interest_over_time()
            if interest_over_time.empty:
                return {"search_volume": 0, "volume_change_percent": 0, "timeline": []}

            values = interest_over_time[keyword].tolist()
            if len(values) >= 2:
                recent = values[-1]
                previous = values[-2] if values[-2] > 0 else 1
                change = ((recent - previous) / previous) * 100
            else:
                change = 0

            return {
                "search_volume": int(values[-1]) if values else 0,
                "volume_change_percent": round(change, 1),
                "timeline": [{"value": v} for v in values],
                "related": [],
            }
        except Exception:
            return {"search_volume": 0, "volume_change_percent": 0, "timeline": []}

    async def _get_news_coverage(self, keyword: str) -> dict:
        return {"total_results": 0}

    def _generate_angles(self, keyword: str, classification: TrendClassification) -> List[str]:
        base_angles = {
            TrendClassification.ESTABLISHED: [
                f"Deep dive: The complete guide to {keyword}",
                f"10 expert tips for {keyword}",
                f"2026 {keyword} trends and predictions",
            ],
            TrendClassification.EMERGING: [
                f"Breaking: Latest {keyword} updates",
                f"Why {keyword} is suddenly trending",
                f"5 things you need to know about {keyword}",
            ],
            TrendClassification.FLEETING: [
                f"Quick take: {keyword} sparks debate",
                f"The {keyword} story explained",
            ],
            TrendClassification.EVERGREEN: [
                f"{keyword}: Beginner to expert tutorial",
                f"The ultimate {keyword} guide",
                f"{keyword} FAQ answered",
            ],
        }
        return base_angles.get(classification, [])
