"""Content Safety Filter for YouTube monetization protection.

This module implements a comprehensive content safety system with:
- Three-tier violation levels (BLOCKED, RESTRICTED, CAUTION)
- AD_FRIENDLY keyword detection for CPM optimization
- Required disclaimer detection
- Regional safety checking
- Auto-fix capabilities
"""

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SafetyLevel(str, Enum):
    """Content safety levels aligned with YouTube monetization policies."""

    BLOCKED = "blocked"  # Content will be removed
    RESTRICTED = "restricted"  # Age-restricted or demonetized
    CAUTION = "caution"  # Yellow dollar sign (limited ads)
    SAFE = "safe"  # Normal monetization
    AD_FRIENDLY = "ad_friendly"  # High CPM potential


@dataclass
class SafetyViolation:
    """Individual safety violation details."""

    term: str
    category: str
    level: SafetyLevel
    context: str
    suggestion: Optional[str] = None


@dataclass
class SafetyCheckResult:
    """Comprehensive safety check result."""

    level: SafetyLevel
    is_safe_to_publish: bool
    violations: List[SafetyViolation]
    issues: List[str]
    warnings: List[str]
    suggestions: List[str]
    flagged_terms: List[str]
    safe_alternatives: Dict[str, str]
    required_disclaimers: List[str]
    ad_friendly_keywords_found: List[str]
    estimated_cpm_impact: str  # 'high', 'medium', 'low', 'blocked'
    fixed_title: Optional[str] = None
    fixed_description: Optional[str] = None
    fixed_tags: Optional[List[str]] = None
    changes_made: List[str] = field(default_factory=list)


class ContentSafetyFilter:
    """Content safety filter to prevent YouTube demonetization or removal.

    Implements YouTube 2026 advertiser-friendly content guidelines with:
    - BLOCKED: Terrorism, child safety, extreme violence, illegal activities
    - RESTRICTED: Adult themes, violence, substances, self-harm references
    - CAUTION: Health/financial misinformation, clickbait, mild profanity
    """

    # ============================================
    # BLOCKED TERMS - Content will be removed
    # ============================================

    BLOCKED_TERMS = {
        "en": {
            "terrorism": [
                "terrorist attack",
                "how to make bomb",
                "terrorism tutorial",
                "join isis",
                "al qaeda recruitment",
            ],
            "child_safety": [
                "child exploitation",
                "minor abuse",
                "underage content",
                "predator guide",
            ],
            "extreme_violence": [
                "execution video",
                "beheading",
                "murder tutorial",
                "how to kill",
                "torture methods",
            ],
            "illegal_activities": [
                "drug manufacturing",
                "how to make meth",
                "counterfeit money",
                "identity theft guide",
                "hacking bank accounts",
            ],
            "copyright": [
                "full movie free",
                "free download movie",
                "pirated",
                "watch free stream",
                "torrent download",
            ],
            "fraud": [
                "free money hack",
                "unlimited money glitch",
                "credit card generator",
                "social security hack",
            ],
        },
        "zh": {
            "terrorism": ["恐怖袭击教程", "制作炸弹", "加入恐怖组织"],
            "child_safety": ["儿童剥削", "未成年人内容"],
            "extreme_violence": ["处决视频", "谋杀教程", "折磨方法"],
            "illegal_activities": ["制毒教程", "伪造货币", "盗取身份"],
            "copyright": ["完整电影", "免费下载", "盗版", "免费观看", "在线播放"],
            "fraud": ["免费领取", "无限金币", "破解账户"],
        },
    }

    # ============================================
    # RESTRICTED TERMS - Age-restricted/Demonetized
    # ============================================

    RESTRICTED_TERMS = {
        "en": {
            "adult_themes": [
                "explicit",
                "nsfw",
                "xxx",
                "pornographic",
                "sexual content",
                "adult only",
            ],
            "violence": [
                "graphic violence",
                "brutal attack",
                "violent assault",
                "gore",
                "blood splatter",
                "mass shooting",
            ],
            "weapons": [
                "gun tutorial",
                "weapon modification",
                "illegal firearm",
                "automatic weapon conversion",
            ],
            "substances": [
                "drug use",
                "getting high",
                "substance abuse",
                "drunk driving",
                "smoking promotion",
            ],
            "self_harm": [
                "suicide methods",
                "self harm tutorial",
                "eating disorder tips",
                "pro-ana",
                "cutting techniques",
            ],
            "dangerous_challenges": [
                "dangerous challenge",
                "do not try this",
                "challenge gone wrong",
                "nearly died",
                "almost killed me",
            ],
            "hate_speech": [
                "racist",
                "discrimination",
                "hate group",
                "white supremacy",
                "ethnic cleansing",
            ],
        },
        "zh": {
            "adult_themes": ["成人内容", "色情", "裸体"],
            "violence": ["暴力", "血腥", "残忍", "攻击", "大屠杀"],
            "weapons": ["武器", "枪", "枪击", "改装武器"],
            "substances": ["吸毒", "毒品使用", "酒驾"],
            "self_harm": ["自残", "自杀方法", "厌食教程"],
            "dangerous_challenges": ["危险", "请勿模仿", "挑战失败", "差点死了"],
            "hate_speech": ["仇恨", "歧视", "种族主义"],
        },
    }

    # ============================================
    # CAUTION TERMS - Yellow dollar sign (limited ads)
    # ============================================

    CAUTION_TERMS = {
        "en": {
            "health_misinformation": [
                "cure",
                "treatment",
                "miracle cure",
                "medical advice",
                "doctors hate this",
                "big pharma hiding",
                "vaccine injury",
                "cancer cure secret",
            ],
            "financial_misinformation": [
                "guaranteed returns",
                "get rich quick",
                "financial advice",
                "investment opportunity",
                "crypto gains guaranteed",
                "forex secret",
                "millionaire overnight",
                "passive income secret",
            ],
            "weight_health": [
                "weight loss",
                "diet pill",
                "supplement",
                "fat burner",
                "lose weight fast",
                "magic pill",
            ],
            "conspiracy": [
                "election fraud",
                "conspiracy",
                "cover-up",
                "deep state",
                "new world order",
                "illuminati",
                "flat earth proof",
            ],
            "clickbait": [
                "shocking truth",
                "they don't want you to know",
                "banned video",
                "censored content",
                "deleted everywhere",
                "you won't believe",
                "mind blowing secret",
            ],
            "profanity_mild": [
                "damn",
                "hell",
                "crap",
                "sucks",
                "pissed",
            ],
            "gambling": [
                "gambling tips",
                "casino strategy",
                "betting system",
                "poker cheat",
            ],
            "tobacco_alcohol": [
                "smoking review",
                "vape tricks",
                "alcohol challenge",
                "drinking game",
            ],
        },
        "zh": {
            "health_misinformation": [
                "治愈",
                "神药",
                "特效药",
                "医疗建议",
                "医生不想让你知道",
                "癌症秘方",
            ],
            "financial_misinformation": [
                "稳赚不赔",
                "财务自由",
                "投资建议",
                "暴富",
                "理财秘诀",
                "一夜暴富",
            ],
            "weight_health": ["减肥药", "保健品", "快速减肥", "神奇药丸"],
            "conspiracy": ["阴谋", "真相", "内幕", "深层政府", "新世界秩序"],
            "clickbait": ["震惊", "他们不想让你知道", "被禁", "到处被删", "你不会相信"],
            "profanity_mild": ["该死", "见鬼"],
            "gambling": ["赌博技巧", "赌场策略"],
            "tobacco_alcohol": ["吸烟评测", "电子烟技巧", "喝酒挑战"],
        },
    }

    # ============================================
    # AD-FRIENDLY KEYWORDS - High CPM potential
    # ============================================

    AD_FRIENDLY_KEYWORDS = {
        "en": [
            "tutorial",
            "how to",
            "guide",
            "review",
            "comparison",
            "best practices",
            "tips and tricks",
            "beginner friendly",
            "step by step",
            "complete guide",
            "professional",
            "enterprise",
            "business",
            "productivity",
            "investment strategy",
            "portfolio management",
            "career development",
            "skill building",
            "certification",
            "software review",
            "tool comparison",
            "workflow",
            "automation",
        ],
        "zh": [
            "教程",
            "如何",
            "指南",
            "评测",
            "对比",
            "最佳实践",
            "技巧",
            "入门",
            "完整指南",
            "专业",
            "企业",
            "商务",
            "生产力",
            "投资策略",
            "职业发展",
        ],
    }

    # ============================================
    # SAFE ALTERNATIVES - Replacement suggestions
    # ============================================

    SAFE_ALTERNATIVES = {
        "en": {
            # Health terms
            "cure": "may help with",
            "treatment": "approach",
            "miracle": "effective",
            "medical advice": "health information",
            "weight loss": "wellness journey",
            "diet pill": "dietary supplement",
            "fat burner": "metabolism support",
            # Financial terms
            "guaranteed": "potential",
            "get rich quick": "wealth building",
            "financial advice": "financial education",
            "passive income secret": "passive income ideas",
            # Clickbait terms
            "shocking": "surprising",
            "secret": "lesser-known",
            "banned": "controversial",
            "censored": "restricted",
            "they don't want you to know": "often overlooked",
            "you won't believe": "you might be surprised",
            # General
            "hack": "tip",
            "free": "no-cost",
            "kill": "defeat",
            "die": "fail",
            "dead": "eliminated",
            "gun": "tool",
            "weapon": "equipment",
            # Profanity
            "damn": "darn",
            "hell": "heck",
            "crap": "stuff",
            "sucks": "is disappointing",
        },
        "zh": {
            "治愈": "可能有帮助",
            "神药": "有效方法",
            "特效药": "有效产品",
            "稳赚": "潜在收益",
            "暴富": "财务增长",
            "震惊": "令人惊讶",
            "秘密": "鲜为人知",
            "被禁": "有争议",
            "破解": "技巧",
            "免费": "无需付费",
            "减肥": "健康之旅",
            "杀": "击败",
        },
    }

    # ============================================
    # DISCLAIMER TRIGGERS
    # ============================================

    DISCLAIMER_TRIGGERS = {
        "financial": {
            "keywords": [
                "investment",
                "stock",
                "crypto",
                "trading",
                "financial",
                "forex",
                "bitcoin",
                "ethereum",
                "portfolio",
                "dividend",
            ],
            "disclaimer": {
                "en": "This content is for educational purposes only and should not be considered financial advice. Always consult with a qualified financial advisor before making investment decisions.",
                "zh": "本内容仅供教育目的，不构成金融建议。在做出投资决策前，请咨询合格的金融顾问。",
            },
        },
        "health": {
            "keywords": [
                "health",
                "medical",
                "treatment",
                "diagnosis",
                "symptom",
                "medicine",
                "therapy",
                "cure",
                "disease",
                "condition",
            ],
            "disclaimer": {
                "en": "This content is for informational purposes only and is not a substitute for professional medical advice. Always seek the advice of your physician or qualified health provider.",
                "zh": "本内容仅供参考，不能替代专业医疗建议。请始终寻求医生或合格健康专家的建议。",
            },
        },
        "legal": {
            "keywords": [
                "legal",
                "law",
                "lawsuit",
                "attorney",
                "lawyer",
                "court",
                "rights",
                "sue",
            ],
            "disclaimer": {
                "en": "This content is for informational purposes only and does not constitute legal advice. Consult a licensed attorney for legal matters.",
                "zh": "本内容仅供参考，不构成法律建议。法律事务请咨询持牌律师。",
            },
        },
        "affiliate": {
            "keywords": [
                "affiliate",
                "sponsored",
                "paid promotion",
                "partner link",
                "commission",
                "referral",
            ],
            "disclaimer": {
                "en": "This video contains affiliate links. I may earn a commission at no extra cost to you if you make a purchase through these links.",
                "zh": "本视频包含联盟链接。如果您通过这些链接购买，我可能获得佣金，但不会增加您的费用。",
            },
        },
    }

    # ============================================
    # CPM IMPACT MAPPING
    # ============================================

    CPM_IMPACT = {
        SafetyLevel.BLOCKED: "none",
        SafetyLevel.RESTRICTED: "blocked",
        SafetyLevel.CAUTION: "low",
        SafetyLevel.SAFE: "medium",
        SafetyLevel.AD_FRIENDLY: "high",
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the content safety filter.

        Args:
            config_path: Optional path to external wordlist JSON file.
        """
        self._load_wordlists(config_path)
        self._compile_patterns()

    def _load_wordlists(self, config_path: Optional[str] = None):
        """Load wordlists from external file if provided."""
        if config_path:
            path = Path(config_path)
            if path.exists():
                with open(path) as f:
                    data = json.load(f)
                    # Merge external data with defaults
                    if "blocked_terms" in data:
                        self._merge_terms(self.BLOCKED_TERMS, data["blocked_terms"])
                    if "restricted_terms" in data:
                        self._merge_terms(self.RESTRICTED_TERMS, data["restricted_terms"])
                    if "caution_terms" in data:
                        self._merge_terms(self.CAUTION_TERMS, data["caution_terms"])
                    if "safe_alternatives" in data:
                        self._merge_dict(self.SAFE_ALTERNATIVES, data["safe_alternatives"])

    def _merge_terms(self, base: dict, new: dict):
        """Merge new terms into base dictionary."""
        for lang, categories in new.items():
            if lang not in base:
                base[lang] = {}
            if isinstance(categories, dict):
                for cat, terms in categories.items():
                    if cat not in base[lang]:
                        base[lang][cat] = []
                    base[lang][cat].extend(terms)
            elif isinstance(categories, list):
                # Handle flat list format
                if "general" not in base[lang]:
                    base[lang]["general"] = []
                base[lang]["general"].extend(categories)

    def _merge_dict(self, base: dict, new: dict):
        """Merge new dict into base dictionary."""
        for lang, items in new.items():
            if lang not in base:
                base[lang] = {}
            base[lang].update(items)

    def _compile_patterns(self):
        """Compile regex patterns for all term categories."""
        self._patterns: Dict[str, Dict[str, Dict[str, list]]] = {
            "blocked": {},
            "restricted": {},
            "caution": {},
        }

        for lang in ["en", "zh"]:
            self._patterns["blocked"][lang] = {}
            self._patterns["restricted"][lang] = {}
            self._patterns["caution"][lang] = {}

            # Compile blocked patterns
            for category, terms in self.BLOCKED_TERMS.get(lang, {}).items():
                self._patterns["blocked"][lang][category] = [
                    re.compile(
                        rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term),
                        re.IGNORECASE,
                    )
                    for term in terms
                ]

            # Compile restricted patterns
            for category, terms in self.RESTRICTED_TERMS.get(lang, {}).items():
                self._patterns["restricted"][lang][category] = [
                    re.compile(
                        rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term),
                        re.IGNORECASE,
                    )
                    for term in terms
                ]

            # Compile caution patterns
            for category, terms in self.CAUTION_TERMS.get(lang, {}).items():
                self._patterns["caution"][lang][category] = [
                    re.compile(
                        rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term),
                        re.IGNORECASE,
                    )
                    for term in terms
                ]

        # Compile ad-friendly patterns
        self._ad_friendly_patterns = {}
        for lang in ["en", "zh"]:
            self._ad_friendly_patterns[lang] = [
                re.compile(
                    rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term),
                    re.IGNORECASE,
                )
                for term in self.AD_FRIENDLY_KEYWORDS.get(lang, [])
            ]

    def check_content(
        self,
        title: str,
        description: str,
        tags: List[str],
        language: str = "en",
        target_regions: Optional[List[str]] = None,
        auto_fix: bool = False,
    ) -> SafetyCheckResult:
        """Perform comprehensive content safety check.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            language: Content language ('en' or 'zh')
            target_regions: Optional list of target regions for regional checks
            auto_fix: Whether to auto-fix violations

        Returns:
            SafetyCheckResult with detailed analysis
        """
        full_text = f"{title} {description} {' '.join(tags)}"
        violations: List[SafetyViolation] = []
        issues: List[str] = []
        warnings: List[str] = []
        flagged_terms: List[str] = []
        lang = language if language in ["en", "zh"] else "en"

        # ============================================
        # Level 1: Check BLOCKED terms
        # ============================================
        for category, patterns in self._patterns["blocked"].get(lang, {}).items():
            for pattern in patterns:
                matches = pattern.findall(full_text)
                if matches:
                    for match in matches:
                        flagged_terms.append(match)
                        violations.append(
                            SafetyViolation(
                                term=match,
                                category=category,
                                level=SafetyLevel.BLOCKED,
                                context=f"BLOCKED: {category}",
                                suggestion="Remove this content entirely",
                            )
                        )
                    issues.append(f"BLOCKED ({category}): {matches}")

        if violations:
            return SafetyCheckResult(
                level=SafetyLevel.BLOCKED,
                is_safe_to_publish=False,
                violations=violations,
                issues=issues,
                warnings=["Content contains terms that violate YouTube policies"],
                suggestions=[
                    "Remove or completely rephrase flagged content",
                    "This content cannot be published safely",
                ],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives={},
                required_disclaimers=[],
                ad_friendly_keywords_found=[],
                estimated_cpm_impact="none",
            )

        # ============================================
        # Level 2: Check RESTRICTED terms
        # ============================================
        for category, patterns in self._patterns["restricted"].get(lang, {}).items():
            for pattern in patterns:
                matches = pattern.findall(full_text)
                if matches:
                    for match in matches:
                        flagged_terms.append(match)
                        violations.append(
                            SafetyViolation(
                                term=match,
                                category=category,
                                level=SafetyLevel.RESTRICTED,
                                context=f"RESTRICTED: {category}",
                                suggestion=self.SAFE_ALTERNATIVES.get(lang, {}).get(match.lower()),
                            )
                        )
                    issues.append(f"RESTRICTED ({category}): {matches}")

        if violations:
            return SafetyCheckResult(
                level=SafetyLevel.RESTRICTED,
                is_safe_to_publish=False,
                violations=violations,
                issues=issues,
                warnings=["Content may be age-restricted or fully demonetized"],
                suggestions=[
                    "Content may be age-restricted or demonetized",
                    "Consider rephrasing or removing flagged terms",
                    "Add appropriate content warnings",
                ],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives=self._get_alternatives(flagged_terms, lang),
                required_disclaimers=[],
                ad_friendly_keywords_found=[],
                estimated_cpm_impact="blocked",
            )

        # ============================================
        # Level 3: Check CAUTION terms
        # ============================================
        for category, patterns in self._patterns["caution"].get(lang, {}).items():
            for pattern in patterns:
                matches = pattern.findall(full_text)
                if matches:
                    for match in matches:
                        flagged_terms.append(match)
                        violations.append(
                            SafetyViolation(
                                term=match,
                                category=category,
                                level=SafetyLevel.CAUTION,
                                context=f"CAUTION: {category}",
                                suggestion=self.SAFE_ALTERNATIVES.get(lang, {}).get(match.lower()),
                            )
                        )
                    warnings.append(f"CAUTION ({category}): {matches}")

        # ============================================
        # Check required disclaimers
        # ============================================
        required_disclaimers = self._check_required_disclaimers(full_text, lang)

        # ============================================
        # Check ad-friendly keywords
        # ============================================
        ad_friendly_found = self._find_ad_friendly_keywords(full_text, lang)

        # ============================================
        # Determine final level
        # ============================================
        if violations:
            level = SafetyLevel.CAUTION
            is_safe = True  # Can publish but with limitations
            cpm_impact = "low"
        elif ad_friendly_found and not flagged_terms:
            level = SafetyLevel.AD_FRIENDLY
            is_safe = True
            cpm_impact = "high"
        else:
            level = SafetyLevel.SAFE
            is_safe = True
            cpm_impact = "medium"

        # ============================================
        # Auto-fix if requested
        # ============================================
        fixed_title = None
        fixed_description = None
        fixed_tags = None
        changes_made = []

        if auto_fix and flagged_terms:
            fixed_title, title_changes = self.sanitize_content(title, lang)
            fixed_description, desc_changes = self.sanitize_content(description, lang)
            fixed_tags = []
            tag_changes = []
            for tag in tags:
                fixed_tag, tc = self.sanitize_content(tag, lang)
                fixed_tags.append(fixed_tag)
                tag_changes.extend(tc)
            changes_made = title_changes + desc_changes + tag_changes

        suggestions = []
        if flagged_terms:
            suggestions.append("Content may receive limited ads (yellow dollar sign)")
            suggestions.append("Consider using safer alternatives")
        if required_disclaimers:
            suggestions.append("Required disclaimers should be added to description")
        if not ad_friendly_found:
            suggestions.append("Consider adding ad-friendly keywords to improve CPM")

        return SafetyCheckResult(
            level=level,
            is_safe_to_publish=is_safe,
            violations=violations,
            issues=issues,
            warnings=warnings,
            suggestions=suggestions if suggestions else ["Content appears safe for monetization"],
            flagged_terms=list(set(flagged_terms)),
            safe_alternatives=self._get_alternatives(flagged_terms, lang),
            required_disclaimers=required_disclaimers,
            ad_friendly_keywords_found=ad_friendly_found,
            estimated_cpm_impact=cpm_impact,
            fixed_title=fixed_title,
            fixed_description=fixed_description,
            fixed_tags=fixed_tags,
            changes_made=changes_made,
        )

    def _get_alternatives(self, terms: List[str], lang: str) -> Dict[str, str]:
        """Get safe alternatives for flagged terms."""
        alt_dict = self.SAFE_ALTERNATIVES.get(lang, {})
        alternatives = {}
        for term in terms:
            term_lower = term.lower()
            if term_lower in alt_dict:
                alternatives[term] = alt_dict[term_lower]
        return alternatives

    def _check_required_disclaimers(self, text: str, lang: str) -> List[str]:
        """Check which disclaimers are required based on content."""
        required = []
        text_lower = text.lower()

        for disclaimer_type, config in self.DISCLAIMER_TRIGGERS.items():
            for keyword in config["keywords"]:
                if keyword.lower() in text_lower:
                    disclaimer_text = config["disclaimer"].get(lang, config["disclaimer"].get("en", ""))
                    if disclaimer_text and disclaimer_text not in required:
                        required.append(disclaimer_text)
                    break

        return required

    def _find_ad_friendly_keywords(self, text: str, lang: str) -> List[str]:
        """Find ad-friendly keywords in content."""
        found = []
        for pattern in self._ad_friendly_patterns.get(lang, []):
            matches = pattern.findall(text)
            found.extend(matches)
        return list(set(found))

    def sanitize_content(self, text: str, language: str = "en") -> Tuple[str, List[str]]:
        """Auto-fix text by replacing violations with safe alternatives.

        Args:
            text: Text to sanitize
            language: Content language

        Returns:
            Tuple of (sanitized_text, list_of_changes)
        """
        changes: List[str] = []
        result = text
        alt_dict = self.SAFE_ALTERNATIVES.get(language, {})

        for original, replacement in alt_dict.items():
            pattern = re.compile(
                rf"\b{re.escape(original)}\b" if language == "en" else re.escape(original),
                re.IGNORECASE,
            )
            if pattern.search(result):
                result = pattern.sub(replacement, result)
                changes.append(f"'{original}' -> '{replacement}'")

        return result, changes

    def validate_metadata(
        self,
        title: str,
        description: str,
        tags: List[str],
        language: str = "en",
    ) -> Tuple[bool, Optional[str], SafetyCheckResult]:
        """Validate metadata before publishing.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            language: Content language

        Returns:
            Tuple of (is_valid, error_message, safety_result)
        """
        result = self.check_content(title, description, tags, language)

        if result.level == SafetyLevel.BLOCKED:
            return False, "Content contains blocked terms and cannot be published", result
        elif result.level == SafetyLevel.RESTRICTED:
            return False, "Content contains restricted terms that will cause demonetization", result
        else:
            return True, None, result


# Global instance
content_safety = ContentSafetyFilter()
