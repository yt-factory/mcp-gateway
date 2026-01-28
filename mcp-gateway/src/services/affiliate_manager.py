"""Affiliate Link Manager for automated affiliate content embedding.

This module provides:
- Affiliate link database management
- Entity-based affiliate matching
- Automated affiliate comment generation
- Disclosure compliance
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class AffiliateLink:
    """Affiliate link configuration."""

    id: str
    name: str
    url: str
    category: str
    keywords: List[str]
    discount_code: Optional[str] = None
    commission_rate: float = 0.0
    description: Optional[str] = None


@dataclass
class AffiliateConfig:
    """Affiliate automation configuration."""

    enabled: bool = True
    auto_comment: bool = True
    auto_pin: bool = True
    disclosure_required: bool = True
    max_links_per_video: int = 5


@dataclass
class AffiliateMatch:
    """Result of affiliate entity matching."""

    link: AffiliateLink
    matched_keyword: str
    confidence: float
    context: str


@dataclass
class AffiliateCommentResult:
    """Result of affiliate comment generation."""

    comment_text: str
    links_included: List[AffiliateLink]
    has_disclosure: bool
    language: str


class AffiliateManager:
    """Manager for affiliate link automation.

    Handles:
    - Detecting mentioned products/tools in content
    - Matching entities to affiliate database
    - Generating compliant affiliate comments
    - Multi-language support
    """

    # ============================================
    # AFFILIATE DATABASE
    # ============================================

    AFFILIATE_DATABASE: Dict[str, AffiliateLink] = {
        # AI Tools
        "claude": AffiliateLink(
            id="claude",
            name="Claude AI",
            url="https://claude.ai/?ref=ytfactory",
            category="ai_tools",
            keywords=["claude", "claude ai", "anthropic", "claude code"],
            commission_rate=0.20,
            description="Advanced AI assistant",
        ),
        "chatgpt": AffiliateLink(
            id="chatgpt",
            name="ChatGPT Plus",
            url="https://chat.openai.com/?ref=ytfactory",
            category="ai_tools",
            keywords=["chatgpt", "gpt-4", "openai", "gpt"],
            commission_rate=0.15,
            description="OpenAI's conversational AI",
        ),
        "midjourney": AffiliateLink(
            id="midjourney",
            name="Midjourney",
            url="https://midjourney.com/?ref=ytfactory",
            category="ai_tools",
            keywords=["midjourney", "mj", "ai art"],
            commission_rate=0.10,
            description="AI image generation",
        ),
        # Developer Tools
        "cursor": AffiliateLink(
            id="cursor",
            name="Cursor IDE",
            url="https://cursor.sh/?ref=ytfactory",
            category="dev_tools",
            keywords=["cursor", "cursor ide", "cursor ai", "ai coding"],
            commission_rate=0.15,
            description="AI-powered code editor",
        ),
        "github_copilot": AffiliateLink(
            id="github_copilot",
            name="GitHub Copilot",
            url="https://github.com/features/copilot?ref=ytfactory",
            category="dev_tools",
            keywords=["github copilot", "copilot", "ai pair programmer"],
            commission_rate=0.10,
            description="AI pair programmer",
        ),
        "vercel": AffiliateLink(
            id="vercel",
            name="Vercel",
            url="https://vercel.com/?ref=ytfactory",
            category="dev_tools",
            keywords=["vercel", "vercel deploy", "next.js hosting"],
            commission_rate=0.15,
            description="Frontend cloud platform",
        ),
        "railway": AffiliateLink(
            id="railway",
            name="Railway",
            url="https://railway.app/?ref=ytfactory",
            category="dev_tools",
            keywords=["railway", "railway app", "deploy backend"],
            commission_rate=0.20,
            description="Infrastructure platform",
        ),
        # Productivity Tools
        "notion": AffiliateLink(
            id="notion",
            name="Notion",
            url="https://notion.so/?ref=ytfactory",
            category="productivity",
            keywords=["notion", "notion app", "note taking"],
            discount_code="YTFACTORY",
            commission_rate=0.15,
            description="All-in-one workspace",
        ),
        "obsidian": AffiliateLink(
            id="obsidian",
            name="Obsidian",
            url="https://obsidian.md/?ref=ytfactory",
            category="productivity",
            keywords=["obsidian", "obsidian md", "knowledge base"],
            commission_rate=0.10,
            description="Personal knowledge base",
        ),
        "linear": AffiliateLink(
            id="linear",
            name="Linear",
            url="https://linear.app/?ref=ytfactory",
            category="productivity",
            keywords=["linear", "linear app", "issue tracking", "project management"],
            commission_rate=0.15,
            description="Issue tracking for teams",
        ),
        # Design Tools
        "figma": AffiliateLink(
            id="figma",
            name="Figma",
            url="https://figma.com/?ref=ytfactory",
            category="design",
            keywords=["figma", "figma design", "ui design"],
            commission_rate=0.10,
            description="Collaborative design tool",
        ),
        "canva": AffiliateLink(
            id="canva",
            name="Canva Pro",
            url="https://canva.com/?ref=ytfactory",
            category="design",
            keywords=["canva", "canva pro", "graphic design"],
            discount_code="YTFACTORY30",
            commission_rate=0.15,
            description="Easy graphic design",
        ),
        # Learning Platforms
        "skillshare": AffiliateLink(
            id="skillshare",
            name="Skillshare",
            url="https://skillshare.com/?ref=ytfactory",
            category="education",
            keywords=["skillshare", "online course", "learn"],
            discount_code="YTFACTORY",
            commission_rate=0.40,
            description="Creative learning platform",
        ),
        "udemy": AffiliateLink(
            id="udemy",
            name="Udemy",
            url="https://udemy.com/?ref=ytfactory",
            category="education",
            keywords=["udemy", "udemy course", "online learning"],
            commission_rate=0.15,
            description="Online course marketplace",
        ),
        # Cloud Services
        "aws": AffiliateLink(
            id="aws",
            name="AWS",
            url="https://aws.amazon.com/?ref=ytfactory",
            category="cloud",
            keywords=["aws", "amazon web services", "cloud computing"],
            commission_rate=0.05,
            description="Amazon cloud platform",
        ),
        "digitalocean": AffiliateLink(
            id="digitalocean",
            name="DigitalOcean",
            url="https://digitalocean.com/?ref=ytfactory",
            category="cloud",
            keywords=["digitalocean", "droplet", "vps"],
            discount_code="YTFACTORY100",
            commission_rate=0.25,
            description="Cloud infrastructure",
        ),
    }

    # ============================================
    # COMMENT TEMPLATES
    # ============================================

    COMMENT_TEMPLATES = {
        "en": {
            "header": "Tools & Resources mentioned in this video:",
            "link_format": "{emoji} {name}: {url}",
            "discount_format": "{emoji} {name}: {url} (Use code: {code})",
            "disclosure": (
                "Some links above are affiliate links. If you purchase through them, "
                "I may earn a commission at no extra cost to you. Thanks for supporting the channel!"
            ),
            "footer": "Thank you for watching!",
        },
        "zh": {
            "header": "本视频提到的工具和资源：",
            "link_format": "{emoji} {name}：{url}",
            "discount_format": "{emoji} {name}：{url}（优惠码：{code}）",
            "disclosure": (
                "以上部分链接为联盟链接。如果您通过这些链接购买，我可能会获得佣金，但不会增加您的费用。感谢支持！"
            ),
            "footer": "感谢观看！",
        },
        "ja": {
            "header": "この動画で紹介したツール＆リソース：",
            "link_format": "{emoji} {name}：{url}",
            "discount_format": "{emoji} {name}：{url}（クーポンコード：{code}）",
            "disclosure": (
                "上記のリンクの一部はアフィリエイトリンクです。"
                "これらのリンクを通じて購入された場合、追加費用なしでコミッションを得る場合があります。"
            ),
            "footer": "ご視聴ありがとうございます！",
        },
    }

    # ============================================
    # CATEGORY EMOJIS
    # ============================================

    CATEGORY_EMOJIS = {
        "ai_tools": "🤖",
        "dev_tools": "💻",
        "productivity": "📝",
        "design": "🎨",
        "education": "📚",
        "cloud": "☁️",
        "general": "🔗",
    }

    def __init__(self, config: Optional[AffiliateConfig] = None):
        """Initialize the affiliate manager.

        Args:
            config: Optional affiliate configuration
        """
        self.config = config or AffiliateConfig()
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for keyword matching."""
        self._keyword_patterns: Dict[str, List[tuple]] = {}

        for link_id, link in self.AFFILIATE_DATABASE.items():
            for keyword in link.keywords:
                pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
                if link_id not in self._keyword_patterns:
                    self._keyword_patterns[link_id] = []
                self._keyword_patterns[link_id].append((keyword, pattern))

    def extract_affiliate_entities(
        self,
        title: str,
        description: str,
        tags: List[str],
        script: Optional[str] = None,
    ) -> List[AffiliateMatch]:
        """Extract affiliate-matchable entities from content.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            script: Optional script content

        Returns:
            List of AffiliateMatch objects
        """
        full_text = f"{title} {description} {' '.join(tags)}"
        if script:
            full_text += f" {script}"

        matches: List[AffiliateMatch] = []
        seen_ids = set()

        for link_id, patterns in self._keyword_patterns.items():
            for keyword, pattern in patterns:
                if pattern.search(full_text):
                    if link_id not in seen_ids:
                        link = self.AFFILIATE_DATABASE[link_id]
                        # Find context
                        match = pattern.search(full_text)
                        context = ""
                        if match:
                            start = max(0, match.start() - 30)
                            end = min(len(full_text), match.end() + 30)
                            context = full_text[start:end]

                        matches.append(
                            AffiliateMatch(
                                link=link,
                                matched_keyword=keyword,
                                confidence=0.9 if keyword.lower() == link.name.lower() else 0.7,
                                context=context,
                            )
                        )
                        seen_ids.add(link_id)
                        break  # Only match once per link

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)

        # Limit to max links
        return matches[: self.config.max_links_per_video]

    def generate_affiliate_comment(
        self,
        matches: List[AffiliateMatch],
        language: str = "en",
        include_disclosure: bool = True,
    ) -> AffiliateCommentResult:
        """Generate affiliate comment text.

        Args:
            matches: List of affiliate matches
            language: Comment language
            include_disclosure: Whether to include affiliate disclosure

        Returns:
            AffiliateCommentResult with comment text and metadata
        """
        if not matches:
            return AffiliateCommentResult(
                comment_text="",
                links_included=[],
                has_disclosure=False,
                language=language,
            )

        template = self.COMMENT_TEMPLATES.get(language, self.COMMENT_TEMPLATES["en"])
        lines = [template["header"], ""]

        links_included = []
        for match in matches:
            link = match.link
            emoji = self.CATEGORY_EMOJIS.get(link.category, self.CATEGORY_EMOJIS["general"])

            if link.discount_code:
                line = template["discount_format"].format(
                    emoji=emoji, name=link.name, url=link.url, code=link.discount_code
                )
            else:
                line = template["link_format"].format(emoji=emoji, name=link.name, url=link.url)

            lines.append(line)
            links_included.append(link)

        # Add disclosure if required
        has_disclosure = False
        if include_disclosure and self.config.disclosure_required:
            lines.append("")
            lines.append("---")
            lines.append(template["disclosure"])
            has_disclosure = True

        lines.append("")
        lines.append(template["footer"])

        comment_text = "\n".join(lines)

        return AffiliateCommentResult(
            comment_text=comment_text,
            links_included=links_included,
            has_disclosure=has_disclosure,
            language=language,
        )

    def get_affiliate_links_for_category(self, category: str) -> List[AffiliateLink]:
        """Get all affiliate links for a category.

        Args:
            category: Category name

        Returns:
            List of AffiliateLink objects
        """
        return [link for link in self.AFFILIATE_DATABASE.values() if link.category == category]

    def get_affiliate_by_keyword(self, keyword: str) -> Optional[AffiliateLink]:
        """Find affiliate link by keyword.

        Args:
            keyword: Keyword to search

        Returns:
            AffiliateLink if found, None otherwise
        """
        keyword_lower = keyword.lower()

        for link in self.AFFILIATE_DATABASE.values():
            if any(kw.lower() == keyword_lower for kw in link.keywords):
                return link

        return None

    def calculate_potential_commission(self, matches: List[AffiliateMatch], estimated_conversions: int = 10) -> Dict:
        """Calculate potential commission from affiliate matches.

        Args:
            matches: List of affiliate matches
            estimated_conversions: Estimated conversions per 1000 views

        Returns:
            Dict with commission estimates
        """
        total_rate = sum(m.link.commission_rate for m in matches)
        avg_rate = total_rate / len(matches) if matches else 0

        # Assume $50 average order value
        avg_order_value = 50

        return {
            "total_links": len(matches),
            "average_commission_rate": round(avg_rate * 100, 1),
            "estimated_commission_per_1000_views": round(estimated_conversions * avg_order_value * avg_rate, 2),
            "links_with_discount_codes": sum(1 for m in matches if m.link.discount_code),
            "categories_covered": list(set(m.link.category for m in matches)),
        }

    def add_affiliate_link(self, link: AffiliateLink):
        """Add a new affiliate link to the database.

        Args:
            link: AffiliateLink to add
        """
        self.AFFILIATE_DATABASE[link.id] = link
        # Recompile patterns
        for keyword in link.keywords:
            pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
            if link.id not in self._keyword_patterns:
                self._keyword_patterns[link.id] = []
            self._keyword_patterns[link.id].append((keyword, pattern))


# Global instance
affiliate_manager = AffiliateManager()
