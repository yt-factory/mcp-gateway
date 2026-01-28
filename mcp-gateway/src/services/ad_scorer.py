"""Ad Suitability Pre-Scorer for monetization prediction.

This module provides pre-scoring of content for ad suitability before
full content generation, enabling the orchestrator to make informed
decisions about content direction.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class AdSuitabilityLevel(str, Enum):
    """Ad suitability levels for content monetization."""

    EXCELLENT = "excellent"  # 90-100 score - High CPM potential
    GOOD = "good"  # 70-89 score - Normal monetization
    MODERATE = "moderate"  # 50-69 score - May have limited ads
    POOR = "poor"  # 30-49 score - Significant ad restrictions
    BLOCKED = "blocked"  # 0-29 score - Cannot monetize


@dataclass
class AdSuitabilityScore:
    """Comprehensive ad suitability score result."""

    score: int  # 0-100
    level: AdSuitabilityLevel

    # Positive factors
    ad_friendly_keywords: List[str]
    high_cpm_signals: List[str]
    estimated_cpm_range: Tuple[float, float]
    best_regions: List[str]

    # Negative factors
    demonetization_risks: List[str]
    risk_categories: List[str]
    caution_factors: List[str]

    # Recommendations
    optimization_suggestions: List[str]
    alternative_keywords: Dict[str, str]
    should_proceed: bool

    # Detailed breakdown
    score_breakdown: Dict[str, int] = field(default_factory=dict)
    predicted_ad_revenue_multiplier: float = 1.0


class AdScorer:
    """Pre-scorer for ad suitability assessment.

    Used by orchestrator to evaluate content monetization potential
    before generating full scripts, ensuring 100% ad-friendly output.
    """

    # ============================================
    # SCORING WEIGHTS
    # ============================================

    SCORING_WEIGHTS = {
        "ad_friendly_keywords": 0.30,  # Presence of ad-friendly keywords
        "no_demonetization_risk": 0.25,  # Absence of risky terms
        "high_cpm_category": 0.20,  # High CPM vertical
        "regional_safety": 0.15,  # Safe for Tier 1 regions
        "content_quality_signals": 0.10,  # Quality indicators
    }

    # ============================================
    # HIGH CPM CATEGORIES
    # ============================================

    HIGH_CPM_CATEGORIES = {
        "insurance": {"base_cpm": 35.0, "keywords": ["insurance", "coverage", "policy", "premium"]},
        "legal": {"base_cpm": 30.0, "keywords": ["attorney", "lawyer", "legal", "lawsuit", "court"]},
        "real_estate": {"base_cpm": 28.0, "keywords": ["real estate", "property", "mortgage", "house"]},
        "finance": {"base_cpm": 25.0, "keywords": ["investment", "portfolio", "trading", "stock", "crypto"]},
        "b2b_saas": {"base_cpm": 22.0, "keywords": ["software", "enterprise", "saas", "business tool"]},
        "ai_tech": {"base_cpm": 18.0, "keywords": ["ai", "artificial intelligence", "machine learning", "automation"]},
        "health": {"base_cpm": 15.0, "keywords": ["fitness", "workout", "nutrition", "wellness"]},
        "education": {"base_cpm": 12.0, "keywords": ["tutorial", "course", "learn", "certification"]},
        "general": {"base_cpm": 8.0, "keywords": []},
    }

    # ============================================
    # AD-FRIENDLY KEYWORDS
    # ============================================

    AD_FRIENDLY_KEYWORDS = [
        "tutorial",
        "guide",
        "how to",
        "review",
        "comparison",
        "best practices",
        "tips",
        "step by step",
        "complete guide",
        "professional",
        "enterprise",
        "business",
        "productivity",
        "beginner",
        "advanced",
        "comprehensive",
        "ultimate",
    ]

    # ============================================
    # HIGH CPM SIGNALS
    # ============================================

    HIGH_CPM_SIGNALS = [
        "vs",
        "comparison",
        "review",
        "best",
        "top",
        "alternative",
        "pricing",
        "cost",
        "worth it",
        "should you buy",
        "2026",
        "2025",
        "updated",
        "latest",
    ]

    # ============================================
    # DEMONETIZATION RISK TERMS
    # ============================================

    DEMONETIZATION_RISKS = {
        "high": [
            "explicit",
            "violence",
            "drug",
            "weapon",
            "hate",
            "racist",
            "adult",
            "nsfw",
            "pirated",
            "hack",
            "cheat",
            "exploit",
        ],
        "medium": [
            "controversy",
            "conspiracy",
            "shocking",
            "banned",
            "censored",
            "secret",
            "gambling",
            "betting",
            "alcohol",
            "smoking",
        ],
        "low": [
            "cure",
            "treatment",
            "guaranteed",
            "free money",
            "get rich quick",
            "weight loss",
            "diet pill",
        ],
    }

    # ============================================
    # CAUTION CATEGORIES
    # ============================================

    CAUTION_CATEGORIES = [
        "health_claims",
        "financial_advice",
        "political_content",
        "religious_content",
        "adult_themes",
        "violence_references",
        "substance_references",
    ]

    def __init__(self):
        """Initialize the ad scorer."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for matching."""
        self._ad_friendly_patterns = [
            re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE) for kw in self.AD_FRIENDLY_KEYWORDS
        ]

        self._high_cpm_patterns = [re.compile(rf"\b{re.escape(sig)}\b", re.IGNORECASE) for sig in self.HIGH_CPM_SIGNALS]

        self._risk_patterns = {}
        for level, terms in self.DEMONETIZATION_RISKS.items():
            self._risk_patterns[level] = [re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE) for term in terms]

    def calculate_ad_suitability(
        self,
        title: str,
        description: str,
        tags: List[str],
        script_outline: Optional[str] = None,
        target_regions: Optional[List[str]] = None,
    ) -> AdSuitabilityScore:
        """Calculate comprehensive ad suitability score.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            script_outline: Optional script outline for deeper analysis
            target_regions: Target regions for regional scoring

        Returns:
            AdSuitabilityScore with detailed analysis
        """
        full_text = f"{title} {description} {' '.join(tags)}"
        if script_outline:
            full_text += f" {script_outline}"

        regions = target_regions or ["US", "UK", "AU", "CA"]

        # Calculate component scores
        scores = {}

        # 1. Ad-friendly keywords score (0-100)
        ad_keywords_found = self._find_ad_friendly_keywords(full_text)
        scores["ad_friendly_keywords"] = min(len(ad_keywords_found) * 15, 100)

        # 2. No demonetization risk score (0-100)
        risks_found, risk_categories = self._find_demonetization_risks(full_text)
        risk_penalty = len([r for r in risks_found if r[1] == "high"]) * 40
        risk_penalty += len([r for r in risks_found if r[1] == "medium"]) * 20
        risk_penalty += len([r for r in risks_found if r[1] == "low"]) * 10
        scores["no_demonetization_risk"] = max(100 - risk_penalty, 0)

        # 3. High CPM category score (0-100)
        category, category_score = self._identify_category(full_text)
        scores["high_cpm_category"] = category_score

        # 4. Regional safety score (0-100)
        regional_score = self._calculate_regional_score(full_text, regions)
        scores["regional_safety"] = regional_score

        # 5. Content quality signals (0-100)
        quality_signals = self._find_quality_signals(full_text)
        scores["content_quality_signals"] = min(len(quality_signals) * 20, 100)

        # Calculate weighted total score
        total_score = 0
        for component, weight in self.SCORING_WEIGHTS.items():
            total_score += scores.get(component, 0) * weight

        total_score = int(total_score)

        # Determine level
        level = self._score_to_level(total_score)

        # Calculate CPM estimate
        base_cpm = self.HIGH_CPM_CATEGORIES.get(category, {"base_cpm": 8.0})["base_cpm"]
        cpm_multiplier = total_score / 100
        cpm_range = (round(base_cpm * cpm_multiplier * 0.8, 2), round(base_cpm * cpm_multiplier * 1.2, 2))

        # Generate suggestions
        suggestions = self._generate_suggestions(scores, risks_found, ad_keywords_found)

        # Get alternative keywords for risky terms
        alternatives = self._get_alternatives([r[0] for r in risks_found])

        # Determine best regions
        best_regions = self._get_best_regions(category, regions)

        return AdSuitabilityScore(
            score=total_score,
            level=level,
            ad_friendly_keywords=ad_keywords_found,
            high_cpm_signals=quality_signals,
            estimated_cpm_range=cpm_range,
            best_regions=best_regions,
            demonetization_risks=[r[0] for r in risks_found],
            risk_categories=risk_categories,
            caution_factors=[r[0] for r in risks_found if r[1] in ["low", "medium"]],
            optimization_suggestions=suggestions,
            alternative_keywords=alternatives,
            should_proceed=level not in [AdSuitabilityLevel.BLOCKED, AdSuitabilityLevel.POOR],
            score_breakdown=scores,
            predicted_ad_revenue_multiplier=cpm_multiplier,
        )

    def _find_ad_friendly_keywords(self, text: str) -> List[str]:
        """Find ad-friendly keywords in text."""
        found = []
        for pattern in self._ad_friendly_patterns:
            matches = pattern.findall(text)
            found.extend(matches)
        return list(set(found))

    def _find_quality_signals(self, text: str) -> List[str]:
        """Find high CPM quality signals in text."""
        found = []
        for pattern in self._high_cpm_patterns:
            matches = pattern.findall(text)
            found.extend(matches)
        return list(set(found))

    def _find_demonetization_risks(self, text: str) -> Tuple[List[Tuple[str, str]], List[str]]:
        """Find demonetization risk terms.

        Returns:
            Tuple of (list of (term, severity), list of categories)
        """
        risks = []
        categories = set()

        for level, patterns in self._risk_patterns.items():
            for pattern in patterns:
                matches = pattern.findall(text)
                for match in matches:
                    risks.append((match, level))
                    # Map to category
                    if match.lower() in ["drug", "alcohol", "smoking"]:
                        categories.add("substance_references")
                    elif match.lower() in ["explicit", "adult", "nsfw"]:
                        categories.add("adult_themes")
                    elif match.lower() in ["violence", "weapon", "hate", "racist"]:
                        categories.add("violence_references")
                    elif match.lower() in ["cure", "treatment", "weight loss", "diet pill"]:
                        categories.add("health_claims")
                    elif match.lower() in ["guaranteed", "free money", "get rich quick"]:
                        categories.add("financial_advice")

        return risks, list(categories)

    def _identify_category(self, text: str) -> Tuple[str, int]:
        """Identify the content category and score.

        Returns:
            Tuple of (category_name, category_score)
        """
        text_lower = text.lower()
        best_category = "general"
        best_matches = 0

        for category, config in self.HIGH_CPM_CATEGORIES.items():
            matches = sum(1 for kw in config["keywords"] if kw.lower() in text_lower)
            if matches > best_matches:
                best_matches = matches
                best_category = category

        # Score based on category CPM potential
        category_cpm = self.HIGH_CPM_CATEGORIES[best_category]["base_cpm"]
        max_cpm = max(c["base_cpm"] for c in self.HIGH_CPM_CATEGORIES.values())

        # Normalize to 0-100
        score = int((category_cpm / max_cpm) * 100)

        return best_category, score

    def _calculate_regional_score(self, text: str, regions: List[str]) -> int:
        """Calculate regional safety score.

        For now, returns 100 if no obvious regional issues.
        Full implementation would integrate with RegionalSafetyFilter.
        """
        # Simple check for obvious regional issues
        regional_red_flags = [
            "tiananmen",
            "tibet",
            "taiwan independence",
            "nazi",
            "hitler",
            "holocaust denial",
        ]

        text_lower = text.lower()
        issues = sum(1 for flag in regional_red_flags if flag in text_lower)

        return max(100 - (issues * 25), 0)

    def _score_to_level(self, score: int) -> AdSuitabilityLevel:
        """Convert numeric score to level."""
        if score >= 90:
            return AdSuitabilityLevel.EXCELLENT
        elif score >= 70:
            return AdSuitabilityLevel.GOOD
        elif score >= 50:
            return AdSuitabilityLevel.MODERATE
        elif score >= 30:
            return AdSuitabilityLevel.POOR
        else:
            return AdSuitabilityLevel.BLOCKED

    def _generate_suggestions(
        self,
        scores: Dict[str, int],
        risks: List[Tuple[str, str]],
        ad_keywords: List[str],
    ) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = []

        # Low ad-friendly keywords
        if scores.get("ad_friendly_keywords", 0) < 50:
            suggestions.append("Add more ad-friendly keywords like 'tutorial', 'guide', 'review', 'comparison'")

        # High risk terms
        high_risks = [r[0] for r in risks if r[1] == "high"]
        if high_risks:
            suggestions.append(f"Remove or replace high-risk terms: {', '.join(high_risks)}")

        # Medium risk terms
        medium_risks = [r[0] for r in risks if r[1] == "medium"]
        if medium_risks:
            suggestions.append(f"Consider replacing caution terms: {', '.join(medium_risks)}")

        # Low category score
        if scores.get("high_cpm_category", 0) < 50:
            suggestions.append("Consider focusing on higher-CPM verticals: finance, insurance, B2B software")

        # Missing quality signals
        if scores.get("content_quality_signals", 0) < 40:
            suggestions.append("Add buyer-intent signals: 'review', 'comparison', 'vs', 'best', 'top'")

        # Year markers
        if "2026" not in " ".join(ad_keywords) and "2025" not in " ".join(ad_keywords):
            suggestions.append("Include year (2026) in title for freshness signal")

        if not suggestions:
            suggestions.append("Content looks well-optimized for ad revenue!")

        return suggestions

    def _get_alternatives(self, risky_terms: List[str]) -> Dict[str, str]:
        """Get safe alternatives for risky terms."""
        alternatives = {
            "shocking": "surprising",
            "secret": "lesser-known",
            "banned": "controversial",
            "hack": "tip",
            "free": "no-cost",
            "cure": "may help with",
            "treatment": "approach",
            "guaranteed": "potential",
            "get rich quick": "wealth building",
        }

        return {
            term: alternatives.get(term.lower(), f"consider rephrasing '{term}'")
            for term in risky_terms
            if term.lower() in alternatives
        }

    def _get_best_regions(self, category: str, target_regions: List[str]) -> List[str]:
        """Get best regions for the category."""
        # Region CPM multipliers
        region_multipliers = {
            "US": 1.5,
            "UK": 1.2,
            "AU": 1.1,
            "CA": 1.0,
            "DE": 0.9,
            "JP": 1.3,
            "CH": 1.4,
        }

        # Sort target regions by multiplier
        sorted_regions = sorted(target_regions, key=lambda r: region_multipliers.get(r, 0.5), reverse=True)

        return sorted_regions[:4]  # Return top 4

    def quick_score(self, title: str, tags: List[str]) -> Tuple[int, AdSuitabilityLevel]:
        """Quick score based on title and tags only.

        Args:
            title: Video title
            tags: List of tags

        Returns:
            Tuple of (score, level)
        """
        text = f"{title} {' '.join(tags)}"

        # Quick calculations
        ad_keywords = len(self._find_ad_friendly_keywords(text))
        quality_signals = len(self._find_quality_signals(text))
        risks, _ = self._find_demonetization_risks(text)

        score = min(ad_keywords * 10 + quality_signals * 5, 50)  # Max 50 from keywords
        score += 50  # Base score
        score -= len([r for r in risks if r[1] == "high"]) * 20
        score -= len([r for r in risks if r[1] == "medium"]) * 10

        score = max(0, min(100, score))

        return score, self._score_to_level(score)


# Global instance
ad_scorer = AdScorer()
