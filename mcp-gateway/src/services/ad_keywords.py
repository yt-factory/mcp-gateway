"""Ad-Friendly Keywords Service for CPM optimization.

This module provides:
- Ad-friendly keyword suggestions by category
- CPM boost patterns for high-value content
- Regional CPM multipliers
- Title templates for maximum ad revenue
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AdKeywordSuggestion:
    """Suggestion for ad-friendly keywords."""

    keyword: str
    category: str
    avg_cpm: float
    best_regions: List[str]
    usage_tip: str


@dataclass
class TitleTemplate:
    """High-CPM title template."""

    template: str
    category: str
    estimated_cpm_boost: float
    example: str


@dataclass
class AdFriendlySuggestions:
    """Complete ad-friendly suggestions for content."""

    keywords: List[AdKeywordSuggestion]
    title_templates: List[TitleTemplate]
    estimated_cpm_by_region: Dict[str, float]
    optimization_tips: List[str]
    category_match: str
    confidence: float


class AdKeywordsService:
    """Service for ad-friendly keyword suggestions and CPM optimization."""

    # ============================================
    # AD-FRIENDLY KEYWORDS BY CATEGORY
    # ============================================

    AD_FRIENDLY_KEYWORDS = {
        "finance": {
            "keywords": [
                "investment strategy",
                "portfolio management",
                "retirement planning",
                "wealth building",
                "financial literacy",
                "passive income ideas",
                "stock market analysis",
                "dividend investing",
                "real estate investing",
                "index funds",
                "budgeting tips",
                "saving money",
                "debt payoff",
                "credit score improvement",
                "tax optimization",
                "personal finance",
                "money management",
                "401k strategies",
                "roth ira guide",
                "compound interest",
            ],
            "avg_cpm": 25.0,
            "best_regions": ["US", "UK", "AU", "CA"],
            "content_tips": [
                "Focus on educational content, not financial advice",
                "Use disclaimers about not being a financial advisor",
                "Target high-income demographics",
                "Include portfolio examples without specific stock picks",
            ],
        },
        "b2b_saas": {
            "keywords": [
                "business software",
                "enterprise solution",
                "productivity tools",
                "project management",
                "team collaboration",
                "workflow automation",
                "crm software",
                "erp system",
                "cloud computing",
                "data analytics",
                "business intelligence",
                "saas comparison",
                "software review",
                "tool tutorial",
                "integration guide",
                "api walkthrough",
                "no-code tools",
                "business automation",
            ],
            "avg_cpm": 22.0,
            "best_regions": ["US", "UK", "DE", "AU"],
            "content_tips": [
                "Create detailed software comparisons",
                "Include pricing breakdowns",
                "Show real use cases and workflows",
                "Target decision-makers and professionals",
            ],
        },
        "ai_tech": {
            "keywords": [
                "artificial intelligence",
                "machine learning",
                "ai tools",
                "automation software",
                "chatgpt tutorial",
                "ai productivity",
                "coding tutorial",
                "programming",
                "web development",
                "app development",
                "tech review",
                "software comparison",
                "claude ai",
                "midjourney tutorial",
                "stable diffusion",
                "llm guide",
                "prompt engineering",
                "ai workflow",
                "developer tools",
            ],
            "avg_cpm": 18.0,
            "best_regions": ["US", "JP", "DE", "UK"],
            "content_tips": [
                "Focus on practical tutorials and use cases",
                "Compare different AI tools objectively",
                "Show productivity gains and time savings",
                "Target developers and tech professionals",
            ],
        },
        "education": {
            "keywords": [
                "online course",
                "tutorial",
                "how to learn",
                "study tips",
                "exam preparation",
                "certification",
                "skill development",
                "career advancement",
                "professional development",
                "learning guide",
                "complete course",
                "beginner to advanced",
                "step by step",
                "masterclass",
                "bootcamp",
                "curriculum",
            ],
            "avg_cpm": 12.0,
            "best_regions": ["US", "IN", "UK", "CA"],
            "content_tips": [
                "Create comprehensive, structured content",
                "Include actionable exercises",
                "Show learning outcomes clearly",
                "Target career-focused learners",
            ],
        },
        "health_wellness": {
            "keywords": [
                "fitness tips",
                "workout routine",
                "healthy eating",
                "nutrition guide",
                "mental health awareness",
                "stress management",
                "sleep improvement",
                "meditation",
                "yoga practice",
                "wellness journey",
                "healthy lifestyle",
                "exercise guide",
                "home workout",
                "mindfulness",
            ],
            "avg_cpm": 15.0,
            "best_regions": ["US", "UK", "AU", "CA"],
            "content_tips": [
                "Avoid medical claims - use 'may help with'",
                "Always include health disclaimers",
                "Focus on lifestyle rather than treatments",
                "Show before/after with context",
            ],
            "caution": "Avoid medical claims, always include disclaimers",
        },
        "real_estate": {
            "keywords": [
                "real estate investing",
                "property investment",
                "house buying guide",
                "rental property",
                "real estate market",
                "home buying tips",
                "mortgage guide",
                "property management",
                "real estate agent",
                "house flipping",
            ],
            "avg_cpm": 28.0,
            "best_regions": ["US", "UK", "AU", "CA"],
            "content_tips": [
                "Focus on market analysis and trends",
                "Provide educational content about processes",
                "Include regional market insights",
                "Target first-time buyers and investors",
            ],
        },
        "insurance": {
            "keywords": [
                "insurance comparison",
                "life insurance guide",
                "health insurance",
                "car insurance tips",
                "home insurance",
                "insurance explained",
                "coverage guide",
                "insurance savings",
            ],
            "avg_cpm": 35.0,
            "best_regions": ["US", "UK"],
            "content_tips": [
                "Compare different providers objectively",
                "Explain complex terms simply",
                "Target life events (marriage, home buying)",
                "Include cost-saving strategies",
            ],
        },
        "legal": {
            "keywords": [
                "legal guide",
                "contract explained",
                "business law",
                "intellectual property",
                "trademark guide",
                "legal tips",
                "rights explained",
                "legal process",
            ],
            "avg_cpm": 30.0,
            "best_regions": ["US", "UK"],
            "content_tips": [
                "Always include legal disclaimers",
                "Focus on educational content",
                "Explain processes, not give advice",
                "Target business owners and creators",
            ],
        },
    }

    # ============================================
    # CPM BOOST PATTERNS
    # ============================================

    CPM_BOOST_PATTERNS = {
        "high_value_prefixes": [
            "best",
            "top",
            "ultimate",
            "complete guide",
            "professional",
            "enterprise",
            "premium",
            "advanced",
            "expert",
            "comprehensive",
        ],
        "buyer_intent": [
            "review",
            "comparison",
            "vs",
            "alternative",
            "pricing",
            "cost",
            "worth it",
            "should you buy",
            "best for",
            "recommended",
            "top picks",
        ],
        "year_markers": ["2026", "2025", "latest", "updated", "new"],
        "high_cpm_combinations": [
            "{tool} tutorial for beginners",
            "{tool} vs {tool} comparison {year}",
            "best {category} software {year}",
            "how to {action} with {tool}",
            "{tool} complete guide {year}",
            "top 10 {category} tools {year}",
            "{tool} review: is it worth it?",
            "best {category} for {audience}",
            "{category} masterclass: beginner to pro",
            "ultimate {category} guide {year}",
        ],
    }

    # ============================================
    # REGIONAL CPM MULTIPLIERS
    # ============================================

    REGION_CPM_MULTIPLIERS = {
        "US": 1.5,
        "UK": 1.2,
        "AU": 1.1,
        "CA": 1.0,
        "DE": 0.9,
        "JP": 1.3,
        "FR": 0.8,
        "NL": 0.85,
        "SE": 0.9,
        "NO": 1.0,
        "CH": 1.4,
        "SG": 0.7,
        "KR": 0.6,
        "BR": 0.3,
        "MX": 0.25,
        "IN": 0.2,
        "ID": 0.15,
        "PH": 0.15,
        "VN": 0.1,
    }

    # ============================================
    # TITLE TEMPLATES BY CATEGORY
    # ============================================

    TITLE_TEMPLATES = {
        "finance": [
            TitleTemplate(
                template="{topic} Investment Strategy: Complete Guide {year}",
                category="finance",
                estimated_cpm_boost=1.3,
                example="Dividend Investment Strategy: Complete Guide 2026",
            ),
            TitleTemplate(
                template="How I Built a ${amount} Portfolio with {strategy}",
                category="finance",
                estimated_cpm_boost=1.4,
                example="How I Built a $100K Portfolio with Index Funds",
            ),
            TitleTemplate(
                template="{topic} for Beginners: Start Investing Today",
                category="finance",
                estimated_cpm_boost=1.2,
                example="Stock Market for Beginners: Start Investing Today",
            ),
        ],
        "b2b_saas": [
            TitleTemplate(
                template="{tool} vs {tool2}: Which is Better for {use_case}?",
                category="b2b_saas",
                estimated_cpm_boost=1.35,
                example="Notion vs Obsidian: Which is Better for Note-Taking?",
            ),
            TitleTemplate(
                template="Best {category} Software {year}: Top {n} Picks Compared",
                category="b2b_saas",
                estimated_cpm_boost=1.4,
                example="Best Project Management Software 2026: Top 5 Picks Compared",
            ),
            TitleTemplate(
                template="{tool} Tutorial: From Beginner to Power User",
                category="b2b_saas",
                estimated_cpm_boost=1.25,
                example="Airtable Tutorial: From Beginner to Power User",
            ),
        ],
        "ai_tech": [
            TitleTemplate(
                template="{ai_tool} Tutorial: {n} {result} You Need to Know",
                category="ai_tech",
                estimated_cpm_boost=1.3,
                example="ChatGPT Tutorial: 10 Prompts You Need to Know",
            ),
            TitleTemplate(
                template="Build {project} with {tool}: Complete Tutorial",
                category="ai_tech",
                estimated_cpm_boost=1.35,
                example="Build a Website with Claude: Complete Tutorial",
            ),
            TitleTemplate(
                template="{tool} vs {tool2}: Which AI is Better for {task}?",
                category="ai_tech",
                estimated_cpm_boost=1.4,
                example="Claude vs ChatGPT: Which AI is Better for Coding?",
            ),
        ],
        "education": [
            TitleTemplate(
                template="Learn {skill} in {time}: Complete Course for Beginners",
                category="education",
                estimated_cpm_boost=1.2,
                example="Learn Python in 4 Hours: Complete Course for Beginners",
            ),
            TitleTemplate(
                template="{skill} Certification: Everything You Need to Know",
                category="education",
                estimated_cpm_boost=1.3,
                example="AWS Certification: Everything You Need to Know",
            ),
        ],
    }

    def __init__(self):
        """Initialize the ad keywords service."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for keyword matching."""
        self._category_patterns = {}
        for category, config in self.AD_FRIENDLY_KEYWORDS.items():
            self._category_patterns[category] = [
                re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE) for kw in config["keywords"]
            ]

    def get_ad_friendly_suggestions(
        self,
        topic: str,
        target_regions: Optional[List[str]] = None,
        content_type: str = "tutorial",
        language: str = "en",
    ) -> AdFriendlySuggestions:
        """Get ad-friendly keyword suggestions for a topic.

        Args:
            topic: Content topic or description
            target_regions: List of target regions
            content_type: Type of content (tutorial, review, comparison, etc.)
            language: Content language

        Returns:
            AdFriendlySuggestions with keywords, templates, and CPM estimates
        """
        topic_lower = topic.lower()
        regions = target_regions or ["US", "UK", "AU", "CA"]

        # Find matching category
        best_category = self._find_best_category(topic_lower)
        category_config = self.AD_FRIENDLY_KEYWORDS.get(best_category, self.AD_FRIENDLY_KEYWORDS["education"])

        # Generate keyword suggestions
        keywords = self._generate_keyword_suggestions(topic_lower, best_category, category_config)

        # Get title templates
        templates = self._get_title_templates(best_category, topic)

        # Calculate CPM estimates by region
        base_cpm = category_config["avg_cpm"]
        cpm_by_region = {
            region: round(base_cpm * self.REGION_CPM_MULTIPLIERS.get(region, 0.5), 2) for region in regions
        }

        # Generate optimization tips
        tips = self._generate_optimization_tips(best_category, category_config, content_type)

        # Calculate confidence based on keyword matches
        confidence = self._calculate_confidence(topic_lower, best_category)

        return AdFriendlySuggestions(
            keywords=keywords,
            title_templates=templates,
            estimated_cpm_by_region=cpm_by_region,
            optimization_tips=tips,
            category_match=best_category,
            confidence=confidence,
        )

    def _find_best_category(self, topic: str) -> str:
        """Find the best matching category for a topic."""
        best_category = "education"
        best_score = 0

        for category, patterns in self._category_patterns.items():
            score = sum(1 for p in patterns if p.search(topic))
            if score > best_score:
                best_score = score
                best_category = category

        return best_category

    def _generate_keyword_suggestions(
        self,
        topic: str,
        category: str,
        config: dict,
    ) -> List[AdKeywordSuggestion]:
        """Generate keyword suggestions based on topic and category."""
        suggestions = []
        keywords = config["keywords"]
        avg_cpm = config["avg_cpm"]
        best_regions = config["best_regions"]

        # Find keywords that match or relate to the topic
        for keyword in keywords[:10]:  # Top 10 keywords
            relevance = self._calculate_keyword_relevance(topic, keyword)
            if relevance > 0.3 or len(suggestions) < 5:
                suggestions.append(
                    AdKeywordSuggestion(
                        keyword=keyword,
                        category=category,
                        avg_cpm=avg_cpm * (0.8 + relevance * 0.4),
                        best_regions=best_regions,
                        usage_tip=f"Include '{keyword}' in title or description for better ad targeting",
                    )
                )

        return suggestions

    def _calculate_keyword_relevance(self, topic: str, keyword: str) -> float:
        """Calculate relevance score between topic and keyword."""
        topic_words = set(topic.lower().split())
        keyword_words = set(keyword.lower().split())

        if keyword.lower() in topic.lower():
            return 1.0

        common = topic_words & keyword_words
        if common:
            return len(common) / max(len(keyword_words), 1)

        return 0.0

    def _get_title_templates(self, category: str, topic: str) -> List[TitleTemplate]:
        """Get title templates for a category."""
        templates = self.TITLE_TEMPLATES.get(category, self.TITLE_TEMPLATES.get("education", []))
        return templates[:5]  # Return top 5 templates

    def _generate_optimization_tips(
        self,
        category: str,
        config: dict,
        content_type: str,
    ) -> List[str]:
        """Generate optimization tips for the content."""
        tips = []

        # Category-specific tips
        if "content_tips" in config:
            tips.extend(config["content_tips"][:3])

        # Content type specific tips
        if content_type == "tutorial":
            tips.append("Include step-by-step instructions for better engagement")
            tips.append("Add timestamps/chapters to improve watch time")
        elif content_type == "review":
            tips.append("Include pros and cons for balanced perspective")
            tips.append("Show real usage scenarios and results")
        elif content_type == "comparison":
            tips.append("Create a clear comparison table or summary")
            tips.append("Include pricing information when available")

        # Caution if present
        if "caution" in config:
            tips.append(f"IMPORTANT: {config['caution']}")

        # General high-CPM tips
        tips.append("Target Tier 1 countries (US, UK, AU, CA) for highest CPM")
        tips.append("Include year in title for freshness signals")

        return tips

    def _calculate_confidence(self, topic: str, category: str) -> float:
        """Calculate confidence score for category match."""
        patterns = self._category_patterns.get(category, [])
        matches = sum(1 for p in patterns if p.search(topic))

        # Base confidence on match ratio
        base_confidence = min(matches / 3, 1.0)  # 3+ matches = 100%

        return round(max(base_confidence, 0.3), 2)  # Minimum 30%

    def estimate_cpm(
        self,
        category: str,
        regions: List[str],
        has_buyer_intent: bool = False,
        is_comparison: bool = False,
    ) -> Dict[str, float]:
        """Estimate CPM for given parameters.

        Args:
            category: Content category
            regions: Target regions
            has_buyer_intent: Whether content has buyer intent keywords
            is_comparison: Whether content is a comparison

        Returns:
            Dict of region -> estimated CPM
        """
        base_cpm = self.AD_FRIENDLY_KEYWORDS.get(category, {"avg_cpm": 10.0})["avg_cpm"]

        # Apply modifiers
        if has_buyer_intent:
            base_cpm *= 1.25
        if is_comparison:
            base_cpm *= 1.15

        return {region: round(base_cpm * self.REGION_CPM_MULTIPLIERS.get(region, 0.5), 2) for region in regions}

    def get_high_cpm_title_suggestions(
        self,
        topic: str,
        tool: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[str]:
        """Generate high-CPM title suggestions.

        Args:
            topic: Main topic
            tool: Optional tool/product name
            category: Optional category

        Returns:
            List of suggested titles
        """
        suggestions = []
        year = "2026"

        # Use patterns to generate titles
        for pattern in self.CPM_BOOST_PATTERNS["high_cpm_combinations"][:5]:
            title = pattern.format(
                tool=tool or topic,
                category=category or topic,
                action="use",
                year=year,
                audience="beginners",
            )
            # Clean up any remaining placeholders
            title = re.sub(r"\{[^}]+\}", topic, title)
            suggestions.append(title)

        return suggestions


# Global instance
ad_keywords_service = AdKeywordsService()
