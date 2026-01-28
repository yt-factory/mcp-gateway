"""Services module for MCP Gateway.

This module exports all service classes and their singleton instances.
"""

from .ad_keywords import (
    AdFriendlySuggestions,
    AdKeywordsService,
    AdKeywordSuggestion,
    TitleTemplate,
    ad_keywords_service,
)
from .ad_scorer import (
    AdScorer,
    AdSuitabilityLevel,
    AdSuitabilityScore,
    ad_scorer,
)
from .affiliate_manager import (
    AffiliateCommentResult,
    AffiliateConfig,
    AffiliateLink,
    AffiliateManager,
    AffiliateMatch,
    affiliate_manager,
)
from .aio_tracker import (
    AIOAttribution,
    AIOFeedbackForOrchestrator,
    AIOPerformanceReport,
    AIOTracker,
    aio_tracker,
)
from .auth_manager import PreemptiveAuthManager
from .cache_manager import CacheManager
from .circuit_breaker import (
    BREAKER_CONFIGS,
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerRegistry,
    CircuitState,
    circuit_registry,
)
from .compliance import (
    ComplianceChecker,
    ComplianceCheckResult,
    compliance_checker,
)
from .content_safety import (
    ContentSafetyFilter,
    SafetyCheckResult,
    SafetyLevel,
    SafetyViolation,
    content_safety,
)
from .entity_clusterer import EntityClusterer, TrendCluster
from .publish_scheduler import (
    AudienceInsight,
    AudienceRegion,
    ContentType,
    PublishScheduler,
    PublishWindow,
)
from .rate_limiter import RateLimiter, RateLimitExceeded
from .regional_safety import (
    RegionalSafetyFilter,
    RegionalSafetyResult,
    RegionalViolation,
    regional_safety,
)

__all__ = [
    # Auth
    "PreemptiveAuthManager",
    # Cache
    "CacheManager",
    # Rate Limiting
    "RateLimiter",
    "RateLimitExceeded",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerRegistry",
    "CircuitState",
    "circuit_registry",
    "BREAKER_CONFIGS",
    # Content Safety
    "ContentSafetyFilter",
    "SafetyLevel",
    "SafetyViolation",
    "SafetyCheckResult",
    "content_safety",
    # Ad Keywords
    "AdKeywordsService",
    "AdKeywordSuggestion",
    "TitleTemplate",
    "AdFriendlySuggestions",
    "ad_keywords_service",
    # Compliance
    "ComplianceChecker",
    "ComplianceCheckResult",
    "compliance_checker",
    # Regional Safety
    "RegionalSafetyFilter",
    "RegionalViolation",
    "RegionalSafetyResult",
    "regional_safety",
    # Ad Scorer
    "AdScorer",
    "AdSuitabilityLevel",
    "AdSuitabilityScore",
    "ad_scorer",
    # Affiliate Manager
    "AffiliateManager",
    "AffiliateLink",
    "AffiliateConfig",
    "AffiliateMatch",
    "AffiliateCommentResult",
    "affiliate_manager",
    # AIO Tracker
    "AIOTracker",
    "AIOAttribution",
    "AIOPerformanceReport",
    "AIOFeedbackForOrchestrator",
    "aio_tracker",
    # Entity Clusterer
    "EntityClusterer",
    "TrendCluster",
    # Publish Scheduler
    "PublishScheduler",
    "PublishWindow",
    "ContentType",
    "AudienceRegion",
    "AudienceInsight",
]
