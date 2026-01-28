import re
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple


class SafetyLevel(str, Enum):
    SAFE = "safe"
    CAUTION = "caution"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


@dataclass
class SafetyCheckResult:
    level: SafetyLevel
    issues: List[str]
    suggestions: List[str]
    flagged_terms: List[str]
    safe_alternatives: Dict[str, str]


class ContentSafetyFilter:
    """Content safety filter to prevent YouTube demonetization or removal."""

    CAUTION_TERMS = {
        "en": [
            "cure",
            "treatment",
            "miracle",
            "medical advice",
            "weight loss",
            "diet pill",
            "supplement",
            "guaranteed returns",
            "get rich quick",
            "financial advice",
            "investment opportunity",
            "crypto gains",
            "election fraud",
            "conspiracy",
            "cover-up",
            "shocking truth",
            "they don't want you to know",
            "banned",
            "censored",
        ],
        "zh": [
            "治愈",
            "神药",
            "特效药",
            "医疗建议",
            "减肥药",
            "保健品",
            "稳赚不赔",
            "财务自由",
            "投资建议",
            "暴富",
            "理财秘诀",
            "阴谋",
            "真相",
            "内幕",
            "震惊",
            "他们不想让你知道",
            "被禁",
        ],
    }

    RESTRICTED_TERMS = {
        "en": [
            "violence",
            "graphic",
            "brutal",
            "attack",
            "weapon",
            "gun",
            "shooting",
            "adult",
            "explicit",
            "nsfw",
            "xxx",
            "dangerous",
            "do not try",
            "challenge gone wrong",
            "hate",
            "racist",
            "discrimination",
        ],
        "zh": [
            "暴力",
            "血腥",
            "残忍",
            "攻击",
            "武器",
            "枪",
            "枪击",
            "危险",
            "请勿模仿",
            "挑战失败",
            "仇恨",
            "歧视",
        ],
    }

    BLOCKED_TERMS = {
        "en": [
            "full movie",
            "free download",
            "pirated",
            "watch free",
            "stream free",
            "free money",
            "cheat",
            "exploit",
        ],
        "zh": [
            "完整电影",
            "免费下载",
            "盗版",
            "免费观看",
            "在线播放",
            "免费领取",
            "破解",
            "作弊",
            "漏洞",
        ],
    }

    SAFE_ALTERNATIVES = {
        "en": {
            "cure": "may help with",
            "guaranteed": "potential",
            "shocking": "surprising",
            "secret": "lesser-known",
            "hack": "tip",
            "free": "no-cost",
            "miracle": "effective",
            "banned": "controversial",
        },
        "zh": {
            "治愈": "可能有帮助",
            "稳赚": "潜在收益",
            "震惊": "令人惊讶",
            "秘密": "鲜为人知",
            "破解": "技巧",
            "免费": "无需付费",
            "神药": "有效方法",
            "被禁": "有争议",
        },
    }

    def __init__(self):
        self._patterns: Dict[str, Dict[str, list]] = {"caution": {}, "restricted": {}, "blocked": {}}
        for lang in ["en", "zh"]:
            self._patterns["caution"][lang] = [
                re.compile(rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term), re.IGNORECASE)
                for term in self.CAUTION_TERMS.get(lang, [])
            ]
            self._patterns["restricted"][lang] = [
                re.compile(rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term), re.IGNORECASE)
                for term in self.RESTRICTED_TERMS.get(lang, [])
            ]
            self._patterns["blocked"][lang] = [
                re.compile(rf"\b{re.escape(term)}\b" if lang == "en" else re.escape(term), re.IGNORECASE)
                for term in self.BLOCKED_TERMS.get(lang, [])
            ]

    def check_content(self, title: str, description: str, tags: List[str], language: str = "en") -> SafetyCheckResult:
        full_text = f"{title} {description} {' '.join(tags)}"
        issues: List[str] = []
        flagged_terms: List[str] = []
        lang = language if language in ["en", "zh"] else "en"

        # Check BLOCKED
        for pattern in self._patterns["blocked"].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
                issues.append(f"BLOCKED term detected: {matches}")
        if flagged_terms:
            return SafetyCheckResult(
                level=SafetyLevel.BLOCKED,
                issues=issues,
                suggestions=["Remove or completely rephrase flagged content"],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives={},
            )

        # Check RESTRICTED
        for pattern in self._patterns["restricted"].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
                issues.append(f"RESTRICTED term detected: {matches}")
        if flagged_terms:
            return SafetyCheckResult(
                level=SafetyLevel.RESTRICTED,
                issues=issues,
                suggestions=["Content may be age-restricted or demonetized", "Consider rephrasing or adding context"],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives=self._get_alternatives(flagged_terms, lang),
            )

        # Check CAUTION
        for pattern in self._patterns["caution"].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
                issues.append(f"CAUTION term detected: {matches}")
        if flagged_terms:
            return SafetyCheckResult(
                level=SafetyLevel.CAUTION,
                issues=issues,
                suggestions=[
                    "Content may receive limited ads (yellow dollar sign)",
                    "Consider using safer alternatives",
                ],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives=self._get_alternatives(flagged_terms, lang),
            )

        return SafetyCheckResult(
            level=SafetyLevel.SAFE,
            issues=[],
            suggestions=["Content appears safe for monetization"],
            flagged_terms=[],
            safe_alternatives={},
        )

    def _get_alternatives(self, terms: List[str], lang: str) -> Dict[str, str]:
        alt_dict = self.SAFE_ALTERNATIVES.get(lang, {})
        return {term: alt_dict[term.lower()] for term in terms if term.lower() in alt_dict}

    def sanitize_content(self, text: str, language: str = "en") -> Tuple[str, List[str]]:
        changes: List[str] = []
        result = text
        alt_dict = self.SAFE_ALTERNATIVES.get(language, {})
        for original, replacement in alt_dict.items():
            pattern = re.compile(
                rf"\b{re.escape(original)}\b" if language == "en" else re.escape(original), re.IGNORECASE
            )
            if pattern.search(result):
                result = pattern.sub(replacement, result)
                changes.append(f"'{original}' -> '{replacement}'")
        return result, changes


content_safety = ContentSafetyFilter()
