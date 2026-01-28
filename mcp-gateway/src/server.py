import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastmcp import FastMCP

from .schemas.analytics import AnalyticsInput
from .schemas.trends import TrendingTopicsInput
from .schemas.youtube import PublishVideoInput, ShortsConfig
from .services.auth_manager import PreemptiveAuthManager
from .services.cache_manager import CacheManager
from .services.circuit_breaker import (
    BREAKER_CONFIGS,
    CircuitBreakerConfig,
    circuit_registry,
)
from .services.content_safety import content_safety
from .services.entity_clusterer import EntityClusterer
from .services.publish_scheduler import (
    AudienceRegion,
    ContentType,
    PublishScheduler,
)
from .services.rate_limiter import RateLimiter
from .tools.analytics import AnalyticsService
from .tools.comments import CommentsService, ManageCommentsInput
from .tools.search import SearchFactsInput, SearchService
from .tools.trends import TrendsService
from .tools.youtube import YouTubePublisher
from .utils.logger import setup_logger

load_dotenv()

logger = setup_logger()

mcp = FastMCP("yt-factory-gateway")

# Initialize services
auth_manager = PreemptiveAuthManager()
cache_manager = CacheManager()
rate_limiter = RateLimiter()
entity_clusterer = EntityClusterer()
publish_scheduler = PublishScheduler()

trends_service = TrendsService(cache_manager, rate_limiter, entity_clusterer)
search_service = SearchService(auth_manager)
youtube_publisher = YouTubePublisher(auth_manager, rate_limiter)
analytics_service = AnalyticsService(auth_manager)
comments_service = CommentsService(auth_manager)

# Initialize circuit breakers
youtube_breaker = circuit_registry.get_or_create("youtube_upload", BREAKER_CONFIGS["youtube_upload"])
trends_breaker = circuit_registry.get_or_create("google_trends", BREAKER_CONFIGS["google_trends"])


# ============================================
# MCP Tools
# ============================================


@mcp.tool()
async def get_trending_topics(
    category: str,
    geo: str = "US",
    timeframe: str = "now 7-d",
    max_results: int = 10,
    include_related: bool = True,
    include_clusters: bool = True,
) -> dict:
    """
    Get real-time trending topics with intelligent classification.

    Classifications:
    - established: Stable trend, good for deep content
    - emerging: Rising trend, good for quick follow-up
    - fleeting: Short-lived, higher risk
    - evergreen: Perennial topic, long-term value

    Includes entity clustering to suggest topic merges.
    Circuit breaker protected.
    """

    async def _fetch():
        input_data = TrendingTopicsInput(
            category=category,
            geo=geo,
            timeframe=timeframe,
            max_results=max_results,
            include_related=include_related,
        )
        return await trends_service.get_trending_topics(input_data, include_clusters)

    result, status = await trends_breaker.call(_fetch)

    if status == "downgraded":
        return {
            "status": "downgraded",
            "message": "Trends API temporarily unavailable. Using cached data or retry later.",
            "topics": [],
            "clusters": [],
        }

    return result.model_dump() if hasattr(result, "model_dump") else result


@mcp.tool()
async def search_facts(
    query: str,
    purpose: str = "fact_check",
    num_results: int = 10,
    include_snippets: bool = True,
    include_entities: bool = True,
) -> dict:
    """
    Search and verify facts with entity data.

    Purposes:
    - fact_check: Fact verification
    - entity_research: Entity research
    - competitor_analysis: Competitor analysis
    """
    input_data = SearchFactsInput(
        query=query,
        purpose=purpose,
        num_results=num_results,
        include_snippets=include_snippets,
        include_entities=include_entities,
    )
    result = await search_service.search_facts(input_data)
    return result.model_dump()


@mcp.tool()
async def publish_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    privacy: str = "private",
    is_short: bool = False,
    thumbnail_path: str = None,
    auto_comment: str = None,
    channel_id: str = None,
    use_optimal_time: bool = True,
    target_audience: str = "GLOBAL",
) -> dict:
    """
    Upload video to YouTube.

    Features:
    - Main videos and Shorts support
    - Auto #Shorts tag
    - Thumbnail setting
    - Auto pinned comment
    - Smart publish window with competition avoidance
    - Pre-emptive auth for long uploads
    - Circuit breaker protection
    """

    async def _upload():
        publish_time = None
        if use_optimal_time and privacy != "private":
            ct = ContentType.SHORTS if is_short else ContentType.MAIN_VIDEO
            audience = AudienceRegion(target_audience)
            window = await publish_scheduler.get_optimal_publish_time(
                channel_id=channel_id, content_type=ct, target_audience=audience
            )
            publish_time = window.optimal_time
            logger.info(
                "Optimal publish time calculated",
                time=publish_time.isoformat(),
                confidence=window.confidence,
            )

        # Ensure token validity for upload duration
        estimated_upload_minutes = os.path.getsize(video_path) / (5 * 1024 * 1024)
        await auth_manager.ensure_valid_for_upload(
            service="youtube",
            channel_id=channel_id,
            estimated_upload_minutes=int(estimated_upload_minutes) + 10,
        )

        shorts_config = ShortsConfig(is_short=True) if is_short else None

        input_data = PublishVideoInput(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            privacy=privacy,
            shorts_config=shorts_config,
            thumbnail_path=thumbnail_path,
            auto_comment=auto_comment,
            channel_id=channel_id,
            scheduled_publish_time=publish_time,
        )
        return await youtube_publisher.publish_video(input_data)

    result, status = await youtube_breaker.call(_upload)

    if status == "downgraded":
        return {
            "success": False,
            "status": "downgraded",
            "message": "YouTube API temporarily unavailable. Please retry later.",
            "error": "Circuit breaker open - too many recent failures",
        }

    return result.model_dump() if hasattr(result, "model_dump") else result


@mcp.tool()
async def get_analytics(
    video_ids: list,
    metrics: list = None,
    include_demographics: bool = False,
    include_traffic_sources: bool = False,
) -> dict:
    """
    Get video performance data.

    Features:
    - Multi-video batch query
    - A/B test analysis
    - Demographics data
    - Traffic source analysis
    """
    input_data = AnalyticsInput(
        video_ids=video_ids,
        metrics=metrics or ["views", "likes", "comments", "estimatedMinutesWatched"],
        include_demographics=include_demographics,
        include_traffic_sources=include_traffic_sources,
    )
    result = await analytics_service.get_analytics(input_data)
    return result.model_dump()


@mcp.tool()
async def manage_comments(
    action: str,
    video_id: str,
    comment_text: str = None,
    comment_id: str = None,
    reply_to_comment_id: str = None,
) -> dict:
    """
    Manage video comments.

    Actions: post, reply, delete, hide
    """
    input_data = ManageCommentsInput(
        action=action,
        video_id=video_id,
        comment_text=comment_text,
        comment_id=comment_id,
        reply_to_comment_id=reply_to_comment_id,
    )
    return await comments_service.manage_comments(input_data)


@mcp.tool()
async def get_system_status() -> dict:
    """
    Get MCP Gateway system status.

    Returns circuit breaker states with cooldown estimates,
    token status with refresh recommendations,
    and API quota remaining with recovery times.
    """
    circuit_status = {}
    for name, breaker in circuit_registry._breakers.items():
        status = breaker.get_status()
        if status["state"] == "open":
            config = BREAKER_CONFIGS.get(name, CircuitBreakerConfig())
            if breaker._state.last_failure_time:
                elapsed = (datetime.utcnow() - breaker._state.last_failure_time).total_seconds()
                remaining = max(0, config.recovery_timeout - elapsed)
                status["cooldown_seconds"] = int(remaining)
                status["estimated_recovery_time"] = (datetime.utcnow() + timedelta(seconds=remaining)).isoformat()
                status["recommendation"] = f"Wait {int(remaining / 60)} minutes before retry."
            else:
                status["cooldown_seconds"] = config.recovery_timeout
        else:
            status["cooldown_seconds"] = 0
            status["recommendation"] = "Service available"
        circuit_status[name] = status

    token_status = {}
    for service in ["youtube", "youtube_analytics"]:
        ts = auth_manager.get_token_status(service)
        if ts.get("minutes_remaining"):
            if ts["minutes_remaining"] < 30:
                ts["recommendation"] = "Token expiring soon. Will auto-refresh before next call."
            elif ts["minutes_remaining"] < 60:
                ts["recommendation"] = "Token healthy but monitor for long operations."
            else:
                ts["recommendation"] = "Token healthy."
        token_status[service] = ts

    quota_status = {}
    for api in ["trends", "youtube_upload", "search"]:
        remaining = rate_limiter.get_remaining(api)
        limit = rate_limiter.limits.get(api)
        quota_info: dict = {
            "remaining": remaining,
            "limit_per_day": limit.requests_per_day if limit else "unknown",
        }
        if remaining <= 0 and limit:
            reset_time = limit.last_day_reset + timedelta(days=1)
            quota_info["resets_at"] = reset_time.isoformat()
            quota_info["recommendation"] = f"Daily quota exhausted. Resets at {reset_time.strftime('%H:%M UTC')}"
        elif remaining < 10:
            quota_info["recommendation"] = "Quota running low."
        else:
            quota_info["recommendation"] = "Quota healthy."
        quota_status[api] = quota_info

    overall_health = "healthy"
    issues = []
    for name, status in circuit_status.items():
        if status["state"] == "open":
            overall_health = "degraded"
            issues.append(f"{name} circuit is open")
    for api, quota in quota_status.items():
        if quota["remaining"] <= 0:
            overall_health = "degraded"
            issues.append(f"{api} quota exhausted")

    return {
        "overall_health": overall_health,
        "issues": issues,
        "circuit_breakers": circuit_status,
        "tokens": token_status,
        "rate_limits": quota_status,
        "timestamp": datetime.utcnow().isoformat(),
    }


@mcp.tool()
async def get_optimal_publish_time(
    content_type: str = "main_video",
    target_audience: str = "GLOBAL",
    channel_id: str = None,
) -> dict:
    """
    Get optimal publish time recommendation.

    Args:
        content_type: main_video or shorts
        target_audience: US, UK, EU, ASIA, GLOBAL
        channel_id: Optional, for personalized analysis
    """
    ct = ContentType(content_type)
    audience = AudienceRegion(target_audience)

    window = await publish_scheduler.get_optimal_publish_time(
        channel_id=channel_id, content_type=ct, target_audience=audience
    )

    return {
        "optimal_time": window.optimal_time.isoformat(),
        "window_start": window.window_start.isoformat(),
        "window_end": window.window_end.isoformat(),
        "confidence": window.confidence,
        "rationale": window.rationale,
        "alternatives": [t.isoformat() for t in (window.alternative_times or [])],
    }


@mcp.tool()
async def check_content_safety(
    title: str,
    description: str,
    tags: list,
    language: str = "en",
    auto_fix: bool = False,
) -> dict:
    """
    Check content safety to prevent YouTube demonetization.

    Returns safety level (safe/caution/restricted/blocked),
    flagged terms, and safe alternatives.
    Optionally auto-fixes content.
    """
    result = content_safety.check_content(title, description, tags, language)

    response: dict = {
        "level": result.level.value,
        "is_safe": result.level.value == "safe",
        "issues": result.issues,
        "suggestions": result.suggestions,
        "flagged_terms": result.flagged_terms,
        "safe_alternatives": result.safe_alternatives,
    }

    if auto_fix and result.level.value != "safe":
        fixed_title, title_changes = content_safety.sanitize_content(title, language)
        fixed_desc, desc_changes = content_safety.sanitize_content(description, language)

        response["fixed_content"] = {
            "title": fixed_title,
            "description": fixed_desc,
            "changes_made": title_changes + desc_changes,
        }

        recheck = content_safety.check_content(fixed_title, fixed_desc, tags, language)
        response["fixed_level"] = recheck.level.value
        response["remaining_issues"] = recheck.issues

    return response


# ============================================
# Entry point
# ============================================

if __name__ == "__main__":
    mcp.run()
