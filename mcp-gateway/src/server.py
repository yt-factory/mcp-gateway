"""YT-Factory MCP Gateway Server.

This module provides the main FastMCP server with all registered tools
for YouTube content creation, safety checking, monetization optimization,
and analytics.
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastmcp import FastMCP

from .schemas.analytics import AnalyticsInput
from .schemas.trends import TrendingTopicsInput
from .schemas.youtube import PublishVideoInput, ShortsConfig
from .services.ad_keywords import ad_keywords_service
from .services.ad_scorer import ad_scorer
from .services.affiliate_manager import affiliate_manager
from .services.aio_tracker import aio_tracker
from .services.auth_manager import PreemptiveAuthManager
from .services.cache_manager import CacheManager
from .services.circuit_breaker import (
    BREAKER_CONFIGS,
    CircuitBreakerConfig,
    circuit_registry,
)
from .services.compliance import compliance_checker
from .services.content_safety import content_safety
from .services.entity_clusterer import EntityClusterer
from .services.monetization_dashboard import monetization_dashboard
from .services.publish_scheduler import (
    AudienceRegion,
    ContentType,
    PublishScheduler,
)
from .services.rate_limiter import RateLimiter
from .services.regional_safety import regional_safety
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
# CORE MCP TOOLS
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
    language: str = "en",
    auto_safety_check: bool = True,
    auto_compliance: bool = True,
    has_ai_voice: bool = True,
    has_affiliate_links: bool = False,
) -> dict:
    """
    Upload video to YouTube with comprehensive safety and compliance checks.

    Features:
    - Content safety validation (blocks risky content)
    - AI disclosure compliance (auto-inject)
    - Affiliate disclosure (auto-inject)
    - Main videos and Shorts support
    - Auto #Shorts tag
    - Thumbnail setting
    - Auto pinned comment with affiliate links
    - Smart publish window with competition avoidance
    - Pre-emptive auth for long uploads
    - Circuit breaker protection
    """

    async def _upload():
        working_title = title
        working_description = description
        working_tags = list(tags)

        # ============================================
        # Step 1: Content Safety Check
        # ============================================
        safety_info = None
        if auto_safety_check:
            safety_result = content_safety.check_content(
                working_title,
                working_description,
                working_tags,
                language,
            )

            safety_info = {
                "level": safety_result.level.value,
                "is_safe": safety_result.is_safe_to_publish,
                "issues": safety_result.issues,
                "warnings": safety_result.warnings,
                "flagged_terms": safety_result.flagged_terms,
                "cpm_impact": safety_result.estimated_cpm_impact,
            }

            # Block if unsafe
            if not safety_result.is_safe_to_publish:
                return {
                    "success": False,
                    "error": "CONTENT_SAFETY_BLOCK",
                    "safety_info": safety_info,
                    "message": f"Content blocked due to {safety_result.level.value} level safety issues",
                    "suggestions": safety_result.suggestions,
                }

            # Apply auto-fixes if available
            if safety_result.fixed_title:
                working_title = safety_result.fixed_title
            if safety_result.fixed_description:
                working_description = safety_result.fixed_description
            if safety_result.fixed_tags:
                working_tags = safety_result.fixed_tags

            safety_info["auto_fixed"] = bool(safety_result.changes_made)
            safety_info["changes_made"] = safety_result.changes_made

        # ============================================
        # Step 2: Compliance Check & Injection
        # ============================================
        compliance_info = None
        if auto_compliance:
            # Get compliant description with all required disclosures
            working_description = compliance_checker.get_full_compliant_description(
                working_description,
                working_title,
                working_tags,
                language,
                has_ai_voice=has_ai_voice,
                has_ai_visuals=False,  # Could be parameterized
                has_affiliate_links=has_affiliate_links,
            )

            compliance_result = compliance_checker.check_compliance(
                working_title,
                working_description,
                working_tags,
                language,
                has_ai_voice=has_ai_voice,
                has_ai_visuals=False,
                has_affiliate_links=has_affiliate_links,
            )

            compliance_info = {
                "is_compliant": compliance_result.is_compliant,
                "synthetic_content_flags": compliance_result.synthetic_content_flags,
            }

        # ============================================
        # Step 3: Affiliate Comment Generation
        # ============================================
        affiliate_comment = None
        if has_affiliate_links or auto_comment:
            # Extract affiliate entities
            matches = affiliate_manager.extract_affiliate_entities(
                working_title,
                working_description,
                working_tags,
            )

            if matches:
                comment_result = affiliate_manager.generate_affiliate_comment(
                    matches,
                    language,
                    include_disclosure=True,
                )
                affiliate_comment = comment_result.comment_text

        # Use provided auto_comment or generated affiliate comment
        final_comment = auto_comment or affiliate_comment

        # ============================================
        # Step 4: Optimal Publish Time
        # ============================================
        publish_time = None
        publish_window_info = None
        if use_optimal_time and privacy != "private":
            ct = ContentType.SHORTS if is_short else ContentType.MAIN_VIDEO
            audience = AudienceRegion(target_audience)
            window = await publish_scheduler.get_optimal_publish_time(
                channel_id=channel_id, content_type=ct, target_audience=audience
            )
            publish_time = window.optimal_time
            publish_window_info = {
                "optimal_time": window.optimal_time.isoformat(),
                "window_start": window.window_start.isoformat(),
                "window_end": window.window_end.isoformat(),
                "confidence": window.confidence,
                "rationale": window.rationale,
            }
            logger.info(
                "Optimal publish time calculated",
                time=publish_time.isoformat(),
                confidence=window.confidence,
            )

        # ============================================
        # Step 5: Pre-emptive Auth
        # ============================================
        estimated_upload_minutes = os.path.getsize(video_path) / (5 * 1024 * 1024)
        await auth_manager.ensure_valid_for_upload(
            service="youtube",
            channel_id=channel_id,
            estimated_upload_minutes=int(estimated_upload_minutes) + 10,
        )

        # ============================================
        # Step 6: Execute Upload
        # ============================================
        shorts_config = ShortsConfig(is_short=True) if is_short else None

        input_data = PublishVideoInput(
            video_path=video_path,
            title=working_title,
            description=working_description,
            tags=working_tags,
            privacy=privacy,
            shorts_config=shorts_config,
            thumbnail_path=thumbnail_path,
            auto_comment=final_comment,
            channel_id=channel_id,
            scheduled_publish_time=publish_time,
        )

        result = await youtube_publisher.publish_video(input_data)

        # Add extra info to result
        result_dict = result.model_dump() if hasattr(result, "model_dump") else result
        result_dict["safety_info"] = safety_info
        result_dict["compliance_info"] = compliance_info
        result_dict["publish_window"] = publish_window_info

        return result_dict

    result, status = await youtube_breaker.call(_upload)

    if status == "downgraded":
        return {
            "success": False,
            "status": "downgraded",
            "message": "YouTube API temporarily unavailable. Please retry later.",
            "error": "Circuit breaker open - too many recent failures",
        }

    return result


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


# ============================================
# SAFETY & COMPLIANCE TOOLS
# ============================================


@mcp.tool()
async def check_content_safety(
    title: str,
    description: str,
    tags: list,
    language: str = "en",
    target_regions: list = None,
    auto_fix: bool = False,
) -> dict:
    """
    Check content safety to prevent YouTube demonetization.

    Returns:
    - level: blocked/restricted/caution/safe/ad_friendly
    - is_safe_to_publish: Whether content can be published
    - violations: Detailed violation information
    - flagged_terms: Terms that triggered flags
    - safe_alternatives: Suggested replacements
    - required_disclaimers: Disclaimers needed for the content
    - ad_friendly_keywords_found: Keywords that boost CPM
    - estimated_cpm_impact: Expected CPM level (high/medium/low/blocked)
    - fixed_content: Auto-fixed content (if auto_fix=True)
    """
    result = content_safety.check_content(
        title,
        description,
        tags,
        language,
        target_regions,
        auto_fix,
    )

    response = {
        "level": result.level.value,
        "is_safe_to_publish": result.is_safe_to_publish,
        "violations": [
            {
                "term": v.term,
                "category": v.category,
                "level": v.level.value,
                "context": v.context,
                "suggestion": v.suggestion,
            }
            for v in result.violations
        ],
        "issues": result.issues,
        "warnings": result.warnings,
        "suggestions": result.suggestions,
        "flagged_terms": result.flagged_terms,
        "safe_alternatives": result.safe_alternatives,
        "required_disclaimers": result.required_disclaimers,
        "ad_friendly_keywords_found": result.ad_friendly_keywords_found,
        "estimated_cpm_impact": result.estimated_cpm_impact,
    }

    if auto_fix and result.changes_made:
        response["fixed_content"] = {
            "title": result.fixed_title,
            "description": result.fixed_description,
            "tags": result.fixed_tags,
            "changes_made": result.changes_made,
        }

    return response


@mcp.tool()
async def check_regional_safety(
    title: str,
    description: str,
    tags: list,
    target_regions: list = None,
) -> dict:
    """
    Check content safety for specific regions.

    Detects cultural sensitivities, political taboos, and legal issues:
    - Japan (JP): WWII historical sensitivity
    - Germany (DE): Nazi/Holocaust-related restrictions
    - China (CN): Political sensitivities
    - Middle East (SA): Religious restrictions
    - India (IN): Religious/caste sensitivities
    - South Korea (KR): Japan-related historical issues
    - Russia (RU): Political restrictions

    Returns:
    - safe_regions: Regions where content is safe
    - blocked_regions: Regions where content may be blocked/illegal
    - warning_regions: Regions requiring caution
    - violations: Detailed violation information
    - recommendations: Suggestions for improvement
    """
    result = regional_safety.check_regional_safety(title, description, tags, target_regions)

    return {
        "safe_regions": result.safe_regions,
        "blocked_regions": result.blocked_regions,
        "warning_regions": result.warning_regions,
        "regional_warnings": result.regional_warnings,
        "violations": [
            {
                "term": v.term,
                "region": v.region,
                "category": v.category,
                "severity": v.severity,
                "reason": v.reason,
                "suggestion": v.suggestion,
            }
            for v in result.violations
        ],
        "recommendations": result.recommendations,
        "overall_safe": result.overall_safe,
    }


@mcp.tool()
async def check_compliance(
    title: str,
    description: str,
    tags: list,
    language: str = "en",
    has_ai_voice: bool = True,
    has_ai_visuals: bool = False,
    has_affiliate_links: bool = False,
) -> dict:
    """
    Check content for YouTube 2026 AI compliance requirements.

    Checks:
    - AI disclosure requirements
    - Financial/health/legal disclaimers
    - Affiliate disclosures
    - Synthetic content flags for YouTube API

    Returns:
    - is_compliant: Whether content meets all requirements
    - missing_disclosures: Disclosures that need to be added
    - required_disclaimers: Disclaimer texts to add
    - synthetic_content_flags: Flags for YouTube API
    - updated_description: Description with injected disclosures (if needed)
    """
    # Check compliance
    result = compliance_checker.check_compliance(
        title,
        description,
        tags,
        language,
        has_ai_voice,
        has_ai_visuals,
        has_affiliate_links,
    )

    # Generate compliant description if needed
    updated_description = None
    if not result.is_compliant:
        updated_description = compliance_checker.get_full_compliant_description(
            description,
            title,
            tags,
            language,
            has_ai_voice,
            has_ai_visuals,
            has_affiliate_links,
        )

    return {
        "is_compliant": result.is_compliant,
        "missing_disclosures": result.missing_disclosures,
        "required_disclaimers": result.required_disclaimers,
        "synthetic_content_flags": result.synthetic_content_flags,
        "warnings": result.warnings,
        "updated_description": updated_description,
    }


# ============================================
# MONETIZATION TOOLS
# ============================================


@mcp.tool()
async def get_ad_suitability_score(
    title: str,
    description: str,
    tags: list,
    script_outline: str = None,
    target_regions: list = None,
) -> dict:
    """
    Get pre-score for ad suitability before content generation.

    Use this before generating full scripts to ensure content direction
    will result in monetizable videos.

    Returns:
    - score: 0-100 numeric score
    - level: excellent/good/moderate/poor/blocked
    - ad_friendly_keywords: Keywords that boost CPM
    - estimated_cpm_range: Estimated CPM range (min, max)
    - best_regions: Best regions for this content
    - demonetization_risks: Identified risk terms
    - optimization_suggestions: How to improve the score
    - should_proceed: Whether to proceed with content generation
    """
    result = ad_scorer.calculate_ad_suitability(
        title,
        description,
        tags,
        script_outline,
        target_regions,
    )

    return {
        "score": result.score,
        "level": result.level.value,
        "ad_friendly_keywords": result.ad_friendly_keywords,
        "high_cpm_signals": result.high_cpm_signals,
        "estimated_cpm_range": {
            "min": result.estimated_cpm_range[0],
            "max": result.estimated_cpm_range[1],
        },
        "best_regions": result.best_regions,
        "demonetization_risks": result.demonetization_risks,
        "risk_categories": result.risk_categories,
        "caution_factors": result.caution_factors,
        "optimization_suggestions": result.optimization_suggestions,
        "alternative_keywords": result.alternative_keywords,
        "should_proceed": result.should_proceed,
        "score_breakdown": result.score_breakdown,
        "predicted_ad_revenue_multiplier": result.predicted_ad_revenue_multiplier,
    }


@mcp.tool()
async def get_ad_friendly_suggestions(
    topic: str,
    target_regions: list = None,
    content_type: str = "tutorial",
    language: str = "en",
) -> dict:
    """
    Get ad-friendly keyword and title suggestions for a topic.

    Returns high-CPM keywords, title templates, and CPM estimates
    to optimize content for maximum ad revenue.

    Returns:
    - keywords: List of ad-friendly keywords with CPM estimates
    - title_templates: High-CPM title templates
    - estimated_cpm_by_region: CPM estimates per region
    - optimization_tips: Tips for maximizing ad revenue
    - category_match: Detected content category
    - confidence: Confidence in category match
    """
    result = ad_keywords_service.get_ad_friendly_suggestions(
        topic,
        target_regions,
        content_type,
        language,
    )

    return {
        "keywords": [
            {
                "keyword": k.keyword,
                "category": k.category,
                "avg_cpm": k.avg_cpm,
                "best_regions": k.best_regions,
                "usage_tip": k.usage_tip,
            }
            for k in result.keywords
        ],
        "title_templates": [
            {
                "template": t.template,
                "category": t.category,
                "estimated_cpm_boost": t.estimated_cpm_boost,
                "example": t.example,
            }
            for t in result.title_templates
        ],
        "estimated_cpm_by_region": result.estimated_cpm_by_region,
        "optimization_tips": result.optimization_tips,
        "category_match": result.category_match,
        "confidence": result.confidence,
    }


@mcp.tool()
async def extract_affiliate_links(
    title: str,
    description: str,
    tags: list,
    script: str = None,
    language: str = "en",
) -> dict:
    """
    Extract affiliate-matchable entities and generate affiliate comment.

    Automatically detects mentioned products/tools and matches them
    to the affiliate database.

    Returns:
    - matches: List of matched affiliate products
    - comment_text: Generated affiliate comment (ready to pin)
    - potential_commission: Estimated commission potential
    """
    matches = affiliate_manager.extract_affiliate_entities(title, description, tags, script)

    comment_result = None
    if matches:
        comment_result = affiliate_manager.generate_affiliate_comment(matches, language)

    commission_estimate = affiliate_manager.calculate_potential_commission(matches)

    return {
        "matches": [
            {
                "name": m.link.name,
                "url": m.link.url,
                "category": m.link.category,
                "matched_keyword": m.matched_keyword,
                "confidence": m.confidence,
                "discount_code": m.link.discount_code,
                "commission_rate": m.link.commission_rate,
            }
            for m in matches
        ],
        "comment_text": comment_result.comment_text if comment_result else None,
        "has_disclosure": comment_result.has_disclosure if comment_result else False,
        "potential_commission": commission_estimate,
    }


# ============================================
# AIO (AI OVERVIEW) TOOLS
# ============================================


@mcp.tool()
async def check_aio_status(
    video_id: str,
    video_title: str,
    faq_items: list,
    topic_keywords: list = None,
) -> dict:
    """
    Check video's AI Overview attribution status.

    Analyzes whether video FAQs are being cited in Google AI Overviews
    and provides optimization suggestions.

    Returns:
    - attributions: List of detected AIO citations
    - total_attributions: Number of citations found
    - estimated_aio_traffic: Estimated traffic from AIO
    """
    attributions = await aio_tracker.check_aio_attribution(
        video_id,
        video_title,
        faq_items,
        topic_keywords,
    )

    return {
        "attributions": [
            {
                "query": a.query,
                "faq_matched": a.faq_item_matched,
                "position": a.position,
                "estimated_traffic": a.estimated_traffic,
            }
            for a in attributions
        ],
        "total_attributions": len(attributions),
        "estimated_aio_traffic": sum(a.estimated_traffic for a in attributions),
    }


@mcp.tool()
async def get_aio_optimization_feedback(
    video_ids: list = None,
) -> dict:
    """
    Get AIO optimization feedback for the orchestrator.

    Provides data-driven recommendations for improving FAQ generation
    to maximize AI Overview citations.

    Returns:
    - top_performing_patterns: FAQ patterns that get cited most
    - recommended_question_formats: Best question formats to use
    - high_attribution_topics: Topics with high AIO visibility
    - underperforming_faqs: FAQ patterns to avoid
    - suggestions: Actionable optimization suggestions
    - optimal_faq_length: Recommended FAQ answer length
    - optimal_faq_count: Recommended number of FAQs per video
    """
    # Generate reports if video_ids provided
    if video_ids:
        await aio_tracker.generate_aio_report(video_ids)

    feedback = aio_tracker.get_optimization_feedback()

    return {
        "top_performing_patterns": feedback.top_performing_patterns,
        "recommended_question_formats": feedback.recommended_question_formats,
        "high_attribution_topics": feedback.high_attribution_topics,
        "underperforming_faqs": feedback.underperforming_faqs,
        "suggestions": feedback.suggestions,
        "optimal_faq_length": feedback.optimal_faq_length,
        "optimal_faq_count": feedback.optimal_faq_count,
    }


# ============================================
# SYSTEM TOOLS
# ============================================


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
        channel_id=channel_id,
        content_type=ct,
        target_audience=audience,
    )

    return {
        "optimal_time": window.optimal_time.isoformat(),
        "window_start": window.window_start.isoformat(),
        "window_end": window.window_end.isoformat(),
        "confidence": window.confidence,
        "rationale": window.rationale,
        "alternatives": [t.isoformat() for t in (window.alternative_times or [])],
    }


# ============================================
# MONETIZATION DASHBOARD TOOLS
# ============================================


@mcp.tool()
async def get_monetization_dashboard(
    channel_id: str = None,
    include_weekly: bool = True,
    include_trends: bool = True,
    include_recommendations: bool = True,
) -> dict:
    """
    Get comprehensive monetization dashboard report.

    Monitors 7 core metrics:
    - AVD: Average View Duration (target: 7 min)
    - CTR: Click-Through Rate (target: 8%)
    - CPM: Cost Per Mille (target: $10)
    - RPM: Revenue Per Mille (target: $6)
    - AIO_RATE: AI Overview Attribution Rate (target: 10%)
    - SUB_RATE: Subscriber Conversion Rate (target: 5%)
    - SHORTS_CONV: Shorts to Main Video Conversion (target: 3%)

    Args:
        channel_id: Optional channel ID for multi-channel support
        include_weekly: Include weekly performance summary
        include_trends: Include trend analysis for all metrics
        include_recommendations: Include optimization recommendations

    Returns:
        Comprehensive dashboard report with metrics, trends, and recommendations
    """
    report = await monetization_dashboard.get_dashboard_report(
        channel_id=channel_id,
        include_weekly=include_weekly,
        include_trends=include_trends,
        include_recommendations=include_recommendations,
    )

    # Convert to dict for JSON serialization
    result = {
        "generated_at": report.generated_at.isoformat(),
        "overall_health": report.overall_health.value,
        "realtime": {
            "active_viewers": report.realtime.active_viewers,
            "today_revenue": report.realtime.today_revenue,
            "today_views": report.realtime.today_views,
            "current_cpm": report.realtime.current_cpm,
            "top_performing_video": report.realtime.top_performing_video,
            "top_video_views": report.realtime.top_video_views,
        },
        "underperforming_videos": report.underperforming_videos,
    }

    if report.weekly_summary:
        result["weekly_summary"] = {
            "week_start": report.weekly_summary.week_start.isoformat(),
            "week_end": report.weekly_summary.week_end.isoformat(),
            "total_revenue": report.weekly_summary.total_revenue,
            "total_views": report.weekly_summary.total_views,
            "total_watch_time_hours": report.weekly_summary.total_watch_time_hours,
            "average_cpm": report.weekly_summary.average_cpm,
            "average_rpm": report.weekly_summary.average_rpm,
            "subscriber_growth": report.weekly_summary.subscriber_growth,
            "metrics": [
                {
                    "name": m.name,
                    "current_value": m.current_value,
                    "target_value": m.target_value,
                    "unit": m.unit,
                    "performance_level": m.performance_level.value,
                    "trend": m.trend.value,
                    "change_percent": m.change_percent,
                    "optimization_tips": m.optimization_tips,
                }
                for m in report.weekly_summary.metrics
            ],
        }

    if report.trend_analysis:
        result["trend_analysis"] = [
            {
                "metric_name": t.metric_name,
                "current_value": t.current_value,
                "previous_value": t.previous_value,
                "change_percent": t.change_percent,
                "trend": t.trend.value,
                "forecast_next_week": t.forecast_next_week,
                "confidence": t.confidence,
                "factors": t.factors,
            }
            for t in report.trend_analysis
        ]

    if report.recommendations:
        result["recommendations"] = [
            {
                "priority": r.priority,
                "category": r.category,
                "title": r.title,
                "description": r.description,
                "expected_impact": r.expected_impact,
                "action_items": r.action_items,
            }
            for r in report.recommendations
        ]

    return result


@mcp.tool()
async def get_metric_details(
    metric_name: str,
    channel_id: str = None,
    days: int = 30,
) -> dict:
    """
    Get detailed analysis for a specific monetization metric.

    Args:
        metric_name: One of AVD, CTR, CPM, RPM, AIO_RATE, SUB_RATE, SHORTS_CONV
        channel_id: Optional channel ID
        days: Number of days to analyze (default: 30)

    Returns:
        Detailed metric analysis including history, trends, and optimization tips
    """
    return await monetization_dashboard.get_metric_details(
        metric_name=metric_name,
        channel_id=channel_id,
        days=days,
    )


# ============================================
# Entry point
# ============================================

if __name__ == "__main__":
    mcp.run()
