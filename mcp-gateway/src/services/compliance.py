"""AI Compliance Service for YouTube 2026 regulations.

This module provides:
- AI disclosure templates for multiple languages
- Special content disclaimers (financial, health, legal, affiliate)
- YouTube synthetic content flags
- Automated compliance checking and injection
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ComplianceCheckResult:
    """Result of compliance check."""

    is_compliant: bool
    missing_disclosures: List[str]
    required_disclaimers: List[str]
    synthetic_content_flags: Dict[str, bool]
    updated_description: Optional[str] = None
    warnings: List[str] = None


class ComplianceChecker:
    """Service for checking and ensuring YouTube AI content compliance.

    Handles:
    - AI-generated content disclosure (2026 YouTube requirements)
    - Financial, health, legal disclaimers
    - Affiliate/sponsored content disclosure
    - Synthetic content API flags
    """

    # ============================================
    # AI DISCLOSURE TEMPLATES
    # ============================================

    AI_DISCLOSURE_TEMPLATES = {
        "en": """
---
AI Disclosure: This video was created with AI assistance, including:
- Script generation (AI-assisted writing)
- Voice synthesis (Text-to-Speech)
- Video editing automation

All content has been fact-checked and reviewed for accuracy.
---
""",
        "zh": """
---
AI 声明：本视频使用 AI 辅助制作，包括：
- 脚本生成（AI 辅助写作）
- 语音合成（TTS 配音）
- 视频自动化编辑

所有内容已经过事实核查和准确性审核。
---
""",
        "ja": """
---
AI開示：この動画はAIの支援を受けて作成されました：
- スクリプト生成（AI支援ライティング）
- 音声合成（テキスト読み上げ）
- ビデオ編集の自動化

すべてのコンテンツは事実確認と正確性のレビューが行われています。
---
""",
        "de": """
---
KI-Offenlegung: Dieses Video wurde mit KI-Unterstützung erstellt:
- Skriptgenerierung (KI-unterstütztes Schreiben)
- Sprachsynthese (Text-to-Speech)
- Automatisierte Videobearbeitung

Alle Inhalte wurden auf Fakten und Genauigkeit überprüft.
---
""",
        "es": """
---
Divulgación de IA: Este video fue creado con asistencia de IA, incluyendo:
- Generación de guión (escritura asistida por IA)
- Síntesis de voz (texto a voz)
- Automatización de edición de video

Todo el contenido ha sido verificado y revisado para garantizar su precisión.
---
""",
        "fr": """
---
Déclaration IA : Cette vidéo a été créée avec l'assistance de l'IA, notamment :
- Génération de script (écriture assistée par IA)
- Synthèse vocale (text-to-speech)
- Automatisation du montage vidéo

Tout le contenu a été vérifié et revu pour son exactitude.
---
""",
        "ko": """
---
AI 공개: 이 동영상은 AI 지원을 통해 제작되었습니다:
- 스크립트 생성 (AI 지원 글쓰기)
- 음성 합성 (텍스트 음성 변환)
- 동영상 편집 자동화

모든 콘텐츠는 정확성을 위해 검증되었습니다.
---
""",
        "pt": """
---
Divulgação de IA: Este vídeo foi criado com assistência de IA, incluindo:
- Geração de roteiro (escrita assistida por IA)
- Síntese de voz (texto para fala)
- Automação de edição de vídeo

Todo o conteúdo foi verificado e revisado quanto à precisão.
---
""",
    }

    # ============================================
    # SHORT AI DISCLOSURE (for description start)
    # ============================================

    AI_DISCLOSURE_SHORT = {
        "en": "AI-Generated Content | Script, Voice & Editing",
        "zh": "AI 生成内容 | 脚本、配音和编辑",
        "ja": "AI生成コンテンツ | スクリプト・音声・編集",
        "de": "KI-generierter Inhalt | Skript, Stimme & Bearbeitung",
        "es": "Contenido generado por IA | Guión, Voz y Edición",
        "fr": "Contenu généré par IA | Script, Voix et Montage",
        "ko": "AI 생성 콘텐츠 | 스크립트, 음성 및 편집",
        "pt": "Conteúdo gerado por IA | Roteiro, Voz e Edição",
    }

    # ============================================
    # SPECIAL DISCLAIMERS
    # ============================================

    SPECIAL_DISCLAIMERS = {
        "financial": {
            "required_when": [
                "investment",
                "stock",
                "crypto",
                "trading",
                "financial advice",
                "forex",
                "bitcoin",
                "ethereum",
                "portfolio",
                "dividend",
                "retirement",
                "401k",
                "ira",
                "wealth",
                "money management",
            ],
            "template": {
                "en": """
FINANCIAL DISCLAIMER: This content is for educational and informational purposes only and should not be considered financial advice. The information provided does not constitute investment recommendations. Always consult with a qualified financial advisor before making any investment decisions. Past performance is not indicative of future results.
""",
                "zh": """
金融免责声明：本内容仅供教育和信息目的，不应被视为金融建议。所提供的信息不构成投资建议。在做出任何投资决策之前，请务必咨询合格的金融顾问。过去的表现并不代表未来的结果。
""",
                "ja": """
金融免責事項：このコンテンツは教育および情報提供のみを目的としており、金融アドバイスとして解釈されるべきではありません。投資を決定する前に、必ず資格のあるファイナンシャルアドバイザーにご相談ください。
""",
                "de": """
FINANZHINWEIS: Dieser Inhalt dient nur zu Bildungs- und Informationszwecken und sollte nicht als Finanzberatung betrachtet werden. Konsultieren Sie immer einen qualifizierten Finanzberater, bevor Sie Anlageentscheidungen treffen.
""",
            },
        },
        "health": {
            "required_when": [
                "health",
                "medical",
                "treatment",
                "cure",
                "diagnosis",
                "symptom",
                "medicine",
                "therapy",
                "disease",
                "condition",
                "diet",
                "supplement",
                "fitness",
                "workout",
                "nutrition",
            ],
            "template": {
                "en": """
HEALTH DISCLAIMER: This content is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have seen in this video.
""",
                "zh": """
健康免责声明：本内容仅供参考，不能替代专业医疗建议、诊断或治疗。如有任何关于医疗状况的问题，请务必咨询您的医生或其他合格的医疗服务提供者。切勿因本视频中的内容而忽视专业医疗建议或延迟就医。
""",
                "ja": """
健康に関する免責事項：このコンテンツは情報提供のみを目的としており、専門的な医療アドバイス、診断、または治療の代わりにはなりません。医療状態に関するご質問がある場合は、必ず医師または資格のある医療提供者にご相談ください。
""",
                "de": """
GESUNDHEITSHINWEIS: Dieser Inhalt dient nur zu Informationszwecken und ersetzt nicht die professionelle medizinische Beratung, Diagnose oder Behandlung. Konsultieren Sie immer einen Arzt bei gesundheitlichen Fragen.
""",
            },
        },
        "legal": {
            "required_when": [
                "legal",
                "law",
                "lawsuit",
                "attorney",
                "lawyer",
                "court",
                "rights",
                "sue",
                "contract",
                "copyright",
                "trademark",
                "patent",
            ],
            "template": {
                "en": """
LEGAL DISCLAIMER: This content is for informational purposes only and does not constitute legal advice. For specific legal questions, consult a licensed attorney in your jurisdiction. Laws vary by location and are subject to change.
""",
                "zh": """
法律免责声明：本内容仅供参考，不构成法律建议。如有具体法律问题，请咨询您所在司法管辖区的持牌律师。法律因地区而异，且可能会发生变化。
""",
                "ja": """
法的免責事項：このコンテンツは情報提供のみを目的としており、法的アドバイスを構成するものではありません。具体的な法的質問については、管轄区域の弁護士にご相談ください。
""",
                "de": """
RECHTSHINWEIS: Dieser Inhalt dient nur zu Informationszwecken und stellt keine Rechtsberatung dar. Konsultieren Sie für rechtliche Fragen einen zugelassenen Anwalt.
""",
            },
        },
        "affiliate": {
            "required_when": [
                "affiliate",
                "sponsored",
                "paid promotion",
                "partner link",
                "commission",
                "referral link",
                "discount code",
                "promo code",
            ],
            "template": {
                "en": """
AFFILIATE DISCLOSURE: This video contains affiliate links. If you make a purchase through these links, I may earn a commission at no additional cost to you. I only recommend products/services I genuinely believe in. Thank you for your support!
""",
                "zh": """
联盟披露：本视频包含联盟链接。如果您通过这些链接购买，我可能会获得佣金，但不会增加您的费用。我只推荐我真正信任的产品/服务。感谢您的支持！
""",
                "ja": """
アフィリエイト開示：この動画にはアフィリエイトリンクが含まれています。これらのリンクを通じて購入された場合、追加費用なしでコミッションを得る場合があります。
""",
                "de": """
AFFILIATE-OFFENLEGUNG: Dieses Video enthält Affiliate-Links. Wenn Sie über diese Links kaufen, erhalte ich möglicherweise eine Provision ohne zusätzliche Kosten für Sie.
""",
            },
        },
        "educational": {
            "required_when": [
                "tutorial",
                "course",
                "learn",
                "education",
                "training",
                "certification",
                "exam",
                "study",
            ],
            "template": {
                "en": """
EDUCATIONAL DISCLAIMER: This content is for educational purposes. Results may vary based on individual effort and circumstances. This is not a guarantee of specific outcomes.
""",
                "zh": """
教育免责声明：本内容仅供教育目的。结果可能因个人努力和情况而异。这不是对特定结果的保证。
""",
            },
        },
    }

    # ============================================
    # YOUTUBE SYNTHETIC CONTENT FLAGS
    # ============================================

    SYNTHETIC_CONTENT_TYPES = {
        "VOICE": "AI-synthesized or modified voice",
        "FACE": "AI-generated or modified face/likeness",
        "SCENE": "AI-generated scene or environment",
        "OBJECT": "AI-generated or modified objects",
        "OTHER": "Other AI-generated content",
    }

    def __init__(self):
        """Initialize the compliance checker."""
        pass

    def check_compliance(
        self,
        title: str,
        description: str,
        tags: List[str],
        language: str = "en",
        has_ai_voice: bool = True,
        has_ai_visuals: bool = False,
        has_affiliate_links: bool = False,
    ) -> ComplianceCheckResult:
        """Check content for compliance requirements.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            language: Content language
            has_ai_voice: Whether video uses AI voice
            has_ai_visuals: Whether video uses AI-generated visuals
            has_affiliate_links: Whether video has affiliate links

        Returns:
            ComplianceCheckResult with compliance status and required changes
        """
        full_text = f"{title} {description} {' '.join(tags)}".lower()
        missing_disclosures = []
        required_disclaimers = []
        warnings = []

        # Check for AI disclosure
        ai_disclosure_present = self._has_ai_disclosure(description, language)
        if (has_ai_voice or has_ai_visuals) and not ai_disclosure_present:
            missing_disclosures.append("AI content disclosure")

        # Check for required disclaimers
        for disclaimer_type, config in self.SPECIAL_DISCLAIMERS.items():
            if self._needs_disclaimer(full_text, config["required_when"]):
                template = config["template"].get(language, config["template"].get("en", ""))
                if template and template.strip() not in description:
                    required_disclaimers.append(template.strip())
                    warnings.append(f"Content may require {disclaimer_type} disclaimer")

        # Check for affiliate disclosure
        if has_affiliate_links and "affiliate" not in [d.lower() for d in required_disclaimers]:
            affiliate_template = self.SPECIAL_DISCLAIMERS["affiliate"]["template"].get(
                language, self.SPECIAL_DISCLAIMERS["affiliate"]["template"]["en"]
            )
            if affiliate_template.strip() not in description:
                required_disclaimers.append(affiliate_template.strip())
                warnings.append("Affiliate disclosure required")

        # Get synthetic content flags
        synthetic_flags = self.get_synthetic_content_flags(has_ai_voice, has_ai_visuals)

        # Determine compliance status
        is_compliant = len(missing_disclosures) == 0 and len(required_disclaimers) == 0

        return ComplianceCheckResult(
            is_compliant=is_compliant,
            missing_disclosures=missing_disclosures,
            required_disclaimers=required_disclaimers,
            synthetic_content_flags=synthetic_flags,
            warnings=warnings or None,
        )

    def inject_ai_disclosure(
        self,
        description: str,
        language: str = "en",
        position: str = "end",
    ) -> str:
        """Inject AI disclosure into description.

        Args:
            description: Original description
            language: Content language
            position: Where to inject ('start', 'end', or 'both')

        Returns:
            Updated description with AI disclosure
        """
        disclosure = self.AI_DISCLOSURE_TEMPLATES.get(language, self.AI_DISCLOSURE_TEMPLATES["en"])
        short_disclosure = self.AI_DISCLOSURE_SHORT.get(language, self.AI_DISCLOSURE_SHORT["en"])

        # Check if disclosure already exists
        if self._has_ai_disclosure(description, language):
            return description

        if position == "start":
            return f"{short_disclosure}\n\n{description}"
        elif position == "both":
            return f"{short_disclosure}\n\n{description}\n{disclosure}"
        else:  # end
            return f"{description}\n{disclosure}"

    def inject_disclaimers(
        self,
        description: str,
        disclaimer_types: List[str],
        language: str = "en",
    ) -> str:
        """Inject specific disclaimers into description.

        Args:
            description: Original description
            disclaimer_types: List of disclaimer types to inject
            language: Content language

        Returns:
            Updated description with disclaimers
        """
        disclaimers_section = "\n\n---\nDISCLAIMERS:\n"
        added = False

        for d_type in disclaimer_types:
            if d_type in self.SPECIAL_DISCLAIMERS:
                template = self.SPECIAL_DISCLAIMERS[d_type]["template"].get(
                    language, self.SPECIAL_DISCLAIMERS[d_type]["template"].get("en", "")
                )
                if template and template.strip() not in description:
                    disclaimers_section += template + "\n"
                    added = True

        if added:
            return description + disclaimers_section
        return description

    def get_synthetic_content_flags(
        self,
        has_ai_voice: bool = True,
        has_ai_visuals: bool = False,
        has_ai_face: bool = False,
        has_ai_scene: bool = False,
    ) -> Dict[str, bool]:
        """Get YouTube API synthetic content flags.

        Args:
            has_ai_voice: Whether AI voice is used
            has_ai_visuals: Whether AI visuals are used
            has_ai_face: Whether AI face/likeness is used
            has_ai_scene: Whether AI scene is used

        Returns:
            Dict of synthetic content flags for YouTube API
        """
        return {
            "hasSyntheticContent": has_ai_voice or has_ai_visuals or has_ai_face or has_ai_scene,
            "syntheticContentTypes": {
                "VOICE": has_ai_voice,
                "FACE": has_ai_face,
                "SCENE": has_ai_scene,
                "OBJECT": has_ai_visuals and not has_ai_scene,
                "OTHER": False,
            },
        }

    def check_required_disclaimers(
        self,
        title: str,
        description: str,
        tags: List[str],
        language: str = "en",
    ) -> List[str]:
        """Check which disclaimers are required based on content.

        Args:
            title: Video title
            description: Video description
            tags: List of tags
            language: Content language

        Returns:
            List of required disclaimer texts
        """
        full_text = f"{title} {description} {' '.join(tags)}".lower()
        required = []

        for disclaimer_type, config in self.SPECIAL_DISCLAIMERS.items():
            if self._needs_disclaimer(full_text, config["required_when"]):
                template = config["template"].get(language, config["template"].get("en", ""))
                if template:
                    required.append(template.strip())

        return required

    def get_full_compliant_description(
        self,
        description: str,
        title: str,
        tags: List[str],
        language: str = "en",
        has_ai_voice: bool = True,
        has_ai_visuals: bool = False,
        has_affiliate_links: bool = False,
    ) -> str:
        """Generate a fully compliant description with all required disclosures.

        Args:
            description: Original description
            title: Video title
            tags: List of tags
            language: Content language
            has_ai_voice: Whether AI voice is used
            has_ai_visuals: Whether AI visuals are used
            has_affiliate_links: Whether affiliate links are present

        Returns:
            Fully compliant description
        """
        result = description

        # Add AI disclosure if needed
        if has_ai_voice or has_ai_visuals:
            result = self.inject_ai_disclosure(result, language, position="end")

        # Check and add required disclaimers
        full_text = f"{title} {description} {' '.join(tags)}".lower()
        disclaimer_types = []

        for d_type, config in self.SPECIAL_DISCLAIMERS.items():
            if self._needs_disclaimer(full_text, config["required_when"]):
                disclaimer_types.append(d_type)

        if has_affiliate_links and "affiliate" not in disclaimer_types:
            disclaimer_types.append("affiliate")

        if disclaimer_types:
            result = self.inject_disclaimers(result, disclaimer_types, language)

        return result

    def _has_ai_disclosure(self, description: str, language: str) -> bool:
        """Check if description already has AI disclosure."""
        desc_lower = description.lower()

        # Check for common AI disclosure phrases
        ai_indicators = [
            "ai disclosure",
            "ai-generated",
            "ai generated",
            "created with ai",
            "ai assistance",
            "ai 声明",
            "ai生成",
            "ai開示",
            "ki-offenlegung",
        ]

        return any(indicator in desc_lower for indicator in ai_indicators)

    def _needs_disclaimer(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any keywords requiring a disclaimer."""
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords)


# Global instance
compliance_checker = ComplianceChecker()
