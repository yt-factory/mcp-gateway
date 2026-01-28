"""Regional Safety Filter for cultural and political sensitivities.

This module provides region-specific content safety checking to avoid
cultural taboos, political sensitivities, and legal issues in different
markets.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class RegionalViolation:
    """Details of a regional safety violation."""

    term: str
    region: str
    category: str
    severity: str  # 'blocked', 'warning', 'caution'
    reason: str
    suggestion: Optional[str] = None


@dataclass
class RegionalSafetyResult:
    """Result of regional safety check."""

    safe_regions: List[str]
    blocked_regions: List[str]
    warning_regions: List[str]
    violations: List[RegionalViolation]
    regional_warnings: Dict[str, List[str]]
    recommendations: List[str]
    overall_safe: bool


class RegionalSafetyFilter:
    """Filter for checking content safety across different regions.

    Handles cultural sensitivities, political taboos, and legal restrictions
    in different markets including:
    - Japan (JP): Historical sensitivities
    - Germany (DE): Nazi/Holocaust-related restrictions
    - China (CN): Political sensitivities
    - Middle East (SA/AE): Religious restrictions
    - India (IN): Religious and caste sensitivities
    - South Korea (KR): Japan-related historical issues
    - Russia (RU): Political restrictions
    """

    # ============================================
    # REGIONAL SENSITIVE TERMS
    # ============================================

    REGIONAL_SENSITIVE_TERMS = {
        "JP": {
            "name": "Japan",
            "historical": {
                "terms": [
                    "atomic bomb joke",
                    "hiroshima joke",
                    "nagasaki joke",
                    "comfort women denial",
                    "war crimes denial japan",
                    "nanking denial",
                    "rising sun flag glorification",
                ],
                "severity": "blocked",
                "reason": "Historical sensitivity - atomic bombings and WWII",
                "suggestion": "Avoid jokes or denialism about WWII events in Japan",
            },
            "territorial": {
                "terms": [
                    "takeshima korean",
                    "senkaku chinese",
                    "northern territories russian",
                ],
                "severity": "warning",
                "reason": "Territorial dispute sensitivity",
                "suggestion": "Use neutral terms when discussing disputed territories",
            },
        },
        "DE": {
            "name": "Germany",
            "hate_symbols": {
                "terms": [
                    "nazi symbol",
                    "swastika promotion",
                    "hitler praise",
                    "third reich glorification",
                    "heil hitler",
                    "ss glorification",
                    "holocaust denial",
                    "holocaust joke",
                    "auschwitz joke",
                ],
                "severity": "blocked",
                "reason": "Strict hate speech laws in Germany - Criminal offense",
                "suggestion": "Nazi symbols and Holocaust denial are illegal in Germany",
            },
            "extremism": {
                "terms": [
                    "neo-nazi recruitment",
                    "white power germany",
                    "afd extremism praise",
                ],
                "severity": "blocked",
                "reason": "Anti-extremism laws",
                "suggestion": "Avoid content promoting extremist ideologies",
            },
        },
        "CN": {
            "name": "China",
            "political": {
                "terms": [
                    "tiananmen square massacre",
                    "june 4th incident",
                    "tank man",
                    "free tibet",
                    "tibet independence",
                    "taiwan independence",
                    "xinjiang camps",
                    "uyghur persecution",
                    "falun gong",
                    "dalai lama political",
                ],
                "severity": "blocked",
                "reason": "Political sensitivity - Content blocked in China",
                "suggestion": "Content will be blocked in mainland China",
            },
            "leadership": {
                "terms": [
                    "xi jinping criticism",
                    "ccp criticism",
                    "winnie the pooh xi",
                ],
                "severity": "blocked",
                "reason": "Leadership criticism - Content blocked in China",
                "suggestion": "Avoid political criticism of Chinese leadership",
            },
        },
        "SA": {
            "name": "Saudi Arabia / Middle East",
            "religious": {
                "terms": [
                    "prophet muhammad cartoon",
                    "prophet criticism",
                    "quran criticism",
                    "islam criticism harsh",
                    "apostasy promotion",
                    "atheism promotion",
                ],
                "severity": "blocked",
                "reason": "Religious restrictions - Potentially illegal",
                "suggestion": "Avoid content critical of Islam in Middle Eastern markets",
            },
            "lifestyle": {
                "terms": [
                    "lgbt pride promotion",
                    "gay marriage promotion",
                    "alcohol promotion",
                    "pork promotion halal",
                    "dating content explicit",
                ],
                "severity": "warning",
                "reason": "Lifestyle restrictions in conservative regions",
                "suggestion": "Content may be restricted in Middle Eastern countries",
            },
        },
        "IN": {
            "name": "India",
            "religious": {
                "terms": [
                    "beef eating promotion",
                    "cow slaughter",
                    "hindu-muslim conflict incitement",
                    "caste discrimination praise",
                    "dalit discrimination",
                ],
                "severity": "blocked",
                "reason": "Religious and caste sensitivity",
                "suggestion": "Avoid content that could incite religious tensions",
            },
            "political": {
                "terms": [
                    "kashmir independence",
                    "khalistan movement",
                    "modi criticism extreme",
                ],
                "severity": "warning",
                "reason": "Political sensitivity in India",
                "suggestion": "Use caution with political content about India",
            },
        },
        "KR": {
            "name": "South Korea",
            "japan_relations": {
                "terms": [
                    "dokdo japan",
                    "takeshima dispute korea wrong",
                    "comfort women denial",
                    "japanese occupation praise",
                    "rising sun flag",
                ],
                "severity": "blocked",
                "reason": "Historical Japan-Korea tensions",
                "suggestion": "Avoid content denying Japanese wartime actions in Korea",
            },
            "north_korea": {
                "terms": [
                    "kim jong un praise",
                    "north korea propaganda",
                    "juche ideology promotion",
                ],
                "severity": "blocked",
                "reason": "National Security Law violations",
                "suggestion": "Avoid content that could be seen as pro-North Korea",
            },
        },
        "RU": {
            "name": "Russia",
            "political": {
                "terms": [
                    "ukraine invasion criticism",
                    "russian war crimes",
                    "putin criticism direct",
                    "navalny support",
                    "anti-war protest russia",
                ],
                "severity": "blocked",
                "reason": "Political restrictions - May be blocked in Russia",
                "suggestion": "Content critical of Russian government may be blocked",
            },
            "historical": {
                "terms": [
                    "soviet crimes",
                    "holodomor ukraine",
                    "stalin criticism strong",
                ],
                "severity": "warning",
                "reason": "Historical sensitivity",
                "suggestion": "Use caution with Soviet-era historical criticism",
            },
        },
        "TR": {
            "name": "Turkey",
            "political": {
                "terms": [
                    "armenian genocide",
                    "kurdistan independence",
                    "pkk support",
                    "erdogan criticism strong",
                    "gulen support",
                ],
                "severity": "blocked",
                "reason": "Political and historical sensitivities in Turkey",
                "suggestion": "Content may be blocked or restricted in Turkey",
            },
        },
        "TH": {
            "name": "Thailand",
            "monarchy": {
                "terms": [
                    "thai king criticism",
                    "thai monarchy criticism",
                    "lese majeste",
                ],
                "severity": "blocked",
                "reason": "Lese majeste laws - Criminal offense in Thailand",
                "suggestion": "Criticism of Thai monarchy is illegal in Thailand",
            },
        },
        "PL": {
            "name": "Poland",
            "historical": {
                "terms": [
                    "polish death camps",
                    "polish collaboration nazis",
                ],
                "severity": "warning",
                "reason": "Historical sensitivity - May be illegal",
                "suggestion": "Use 'Nazi German camps in occupied Poland'",
            },
        },
    }

    # ============================================
    # ALL REGIONS FOR CHECKING
    # ============================================

    ALL_REGIONS = ["US", "UK", "CA", "AU", "DE", "FR", "JP", "KR", "CN", "IN", "SA", "RU", "TR", "TH", "PL", "BR", "MX"]

    def __init__(self):
        """Initialize the regional safety filter."""
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for all regional terms."""
        self._patterns: Dict[str, Dict[str, list]] = {}

        for region, categories in self.REGIONAL_SENSITIVE_TERMS.items():
            self._patterns[region] = {}
            for category, config in categories.items():
                if category == "name":
                    continue
                self._patterns[region][category] = {
                    "patterns": [re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE) for term in config["terms"]],
                    "severity": config["severity"],
                    "reason": config["reason"],
                    "suggestion": config.get("suggestion", ""),
                }

    def check_regional_safety(
        self,
        title: str,
        description: str,
        tags: List[str],
        target_regions: Optional[List[str]] = None,
    ) -> RegionalSafetyResult:
        """Check content safety for specific regions.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            target_regions: Specific regions to check (None = check all)

        Returns:
            RegionalSafetyResult with detailed regional analysis
        """
        full_text = f"{title} {description} {' '.join(tags)}"
        regions_to_check = target_regions or self.ALL_REGIONS

        violations: List[RegionalViolation] = []
        regional_warnings: Dict[str, List[str]] = {}
        blocked_regions: List[str] = []
        warning_regions: List[str] = []
        safe_regions: List[str] = []

        # Check each region
        for region in regions_to_check:
            region_violations = []
            region_warnings = []

            if region in self._patterns:
                for category, config in self._patterns[region].items():
                    for pattern in config["patterns"]:
                        matches = pattern.findall(full_text)
                        if matches:
                            for match in matches:
                                violation = RegionalViolation(
                                    term=match,
                                    region=region,
                                    category=category,
                                    severity=config["severity"],
                                    reason=config["reason"],
                                    suggestion=config["suggestion"],
                                )
                                violations.append(violation)
                                region_violations.append(violation)

                                if config["severity"] == "blocked":
                                    region_warnings.append(f"BLOCKED: {match} - {config['reason']}")
                                else:
                                    region_warnings.append(f"WARNING: {match} - {config['reason']}")

            # Classify region
            if any(v.severity == "blocked" for v in region_violations):
                blocked_regions.append(region)
            elif any(v.severity == "warning" for v in region_violations):
                warning_regions.append(region)
            else:
                safe_regions.append(region)

            if region_warnings:
                regional_warnings[region] = region_warnings

        # Generate recommendations
        recommendations = self._generate_recommendations(violations, blocked_regions, warning_regions)

        return RegionalSafetyResult(
            safe_regions=safe_regions,
            blocked_regions=blocked_regions,
            warning_regions=warning_regions,
            violations=violations,
            regional_warnings=regional_warnings,
            recommendations=recommendations,
            overall_safe=len(blocked_regions) == 0,
        )

    def _generate_recommendations(
        self,
        violations: List[RegionalViolation],
        blocked_regions: List[str],
        warning_regions: List[str],
    ) -> List[str]:
        """Generate recommendations based on violations."""
        recommendations = []

        if blocked_regions:
            region_names = [self.REGIONAL_SENSITIVE_TERMS.get(r, {}).get("name", r) for r in blocked_regions]
            recommendations.append(f"Content may be blocked or cause issues in: {', '.join(region_names)}")
            recommendations.append("Consider creating region-specific versions without flagged content")

        if warning_regions:
            region_names = [self.REGIONAL_SENSITIVE_TERMS.get(r, {}).get("name", r) for r in warning_regions]
            recommendations.append(f"Use caution when targeting: {', '.join(region_names)}")

        # Add specific suggestions from violations
        seen_suggestions = set()
        for violation in violations:
            if violation.suggestion and violation.suggestion not in seen_suggestions:
                recommendations.append(violation.suggestion)
                seen_suggestions.add(violation.suggestion)

        if not violations:
            recommendations.append("Content appears safe for all checked regions")

        return recommendations

    def get_safe_regions(
        self,
        title: str,
        description: str,
        tags: List[str],
    ) -> List[str]:
        """Get list of regions where content is safe to publish.

        Args:
            title: Video title
            description: Video description
            tags: List of tags

        Returns:
            List of safe region codes
        """
        result = self.check_regional_safety(title, description, tags)
        return result.safe_regions

    def check_specific_region(
        self,
        title: str,
        description: str,
        tags: List[str],
        region: str,
    ) -> Dict:
        """Check content safety for a specific region.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            region: Region code to check

        Returns:
            Dict with region-specific safety information
        """
        result = self.check_regional_safety(title, description, tags, [region])

        return {
            "region": region,
            "region_name": self.REGIONAL_SENSITIVE_TERMS.get(region, {}).get("name", region),
            "is_safe": region in result.safe_regions,
            "is_blocked": region in result.blocked_regions,
            "has_warnings": region in result.warning_regions,
            "warnings": result.regional_warnings.get(region, []),
            "recommendations": result.recommendations,
        }


# Global instance
regional_safety = RegionalSafetyFilter()
