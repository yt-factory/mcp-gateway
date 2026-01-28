"""AIO (AI Overview) Attribution Tracker for Google search visibility.

This module provides tracking and optimization for Google AI Overview
citations, helping improve content visibility in AI-generated search results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class AIOAttribution:
    """Record of an AIO attribution for a video."""

    video_id: str
    query: str  # Search query that triggered the attribution
    faq_item_matched: str  # The FAQ content that was cited
    position: int  # Position in the AIO results (1-based)
    detected_at: datetime
    estimated_traffic: int  # Estimated traffic from this attribution
    source_url: Optional[str] = None


@dataclass
class AIOPerformanceReport:
    """Performance report for AIO attributions."""

    video_id: str
    total_attributions: int
    top_queries: List[str]
    best_performing_faqs: List[str]
    attribution_rate: float  # Percentage of checked queries with attribution
    estimated_aio_traffic: int
    optimization_suggestions: List[str]
    trend: str  # 'improving', 'stable', 'declining'
    report_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class AIOFeedbackForOrchestrator:
    """Feedback data for orchestrator to improve FAQ generation."""

    top_performing_patterns: List[str]
    recommended_question_formats: List[str]
    high_attribution_topics: List[str]
    underperforming_faqs: List[str]
    suggestions: List[str]
    optimal_faq_length: int  # Optimal character count
    optimal_faq_count: int  # Optimal number of FAQs per video


class AIOTracker:
    """Tracker for Google AI Overview attributions.

    Monitors and optimizes content for AIO visibility by:
    - Tracking which FAQs get cited in AI Overviews
    - Identifying high-performing question patterns
    - Providing feedback for FAQ optimization
    """

    # ============================================
    # SEARCH PATTERNS FOR AIO CHECKING
    # ============================================

    SEARCH_PATTERNS = [
        "how to {topic}",
        "what is {topic}",
        "why {topic}",
        "{topic} tutorial",
        "{topic} guide 2026",
        "best {topic}",
        "{topic} explained",
        "{topic} for beginners",
        "{topic} vs {alternative}",
        "how does {topic} work",
    ]

    # ============================================
    # HIGH-PERFORMING FAQ PATTERNS
    # ============================================

    HIGH_PERFORMING_PATTERNS = [
        "What is {topic} and how does it work?",
        "How do I get started with {topic}?",
        "What are the benefits of {topic}?",
        "Is {topic} worth it in 2026?",
        "What's the difference between {topic} and {alternative}?",
        "How much does {topic} cost?",
        "Can beginners use {topic}?",
        "What are the best practices for {topic}?",
    ]

    # ============================================
    # RECOMMENDED QUESTION FORMATS
    # ============================================

    RECOMMENDED_FORMATS = {
        "direct_answer": {
            "pattern": "What is {topic}?",
            "answer_style": "Start with a clear, concise definition (2-3 sentences)",
            "optimal_length": 150,
        },
        "how_to": {
            "pattern": "How do I {action}?",
            "answer_style": "Numbered steps, each step 1-2 sentences",
            "optimal_length": 200,
        },
        "comparison": {
            "pattern": "{topic} vs {alternative}: Which is better?",
            "answer_style": "Brief comparison with clear recommendation",
            "optimal_length": 180,
        },
        "best_practices": {
            "pattern": "What are the best practices for {topic}?",
            "answer_style": "Bullet points with actionable tips",
            "optimal_length": 220,
        },
        "cost_benefit": {
            "pattern": "Is {topic} worth the cost?",
            "answer_style": "Direct value proposition with specific benefits",
            "optimal_length": 160,
        },
    }

    def __init__(self):
        """Initialize the AIO tracker."""
        self._attribution_cache: Dict[str, List[AIOAttribution]] = {}
        self._performance_history: Dict[str, List[AIOPerformanceReport]] = {}

    async def check_aio_attribution(
        self,
        video_id: str,
        video_title: str,
        faq_items: List[str],
        topic_keywords: Optional[List[str]] = None,
    ) -> List[AIOAttribution]:
        """Check if video FAQs appear in AI Overviews.

        Args:
            video_id: YouTube video ID
            video_title: Video title for topic extraction
            faq_items: List of FAQ questions/answers
            topic_keywords: Optional topic keywords for search patterns

        Returns:
            List of AIOAttribution objects

        Note: This is a simulated implementation. Real implementation
        would need to integrate with Google Search API or use
        web scraping (with appropriate permissions).
        """
        attributions: List[AIOAttribution] = []

        # Extract topics from title if not provided
        if not topic_keywords:
            topic_keywords = self._extract_topics(video_title)

        # Generate search queries to check
        queries = self._generate_search_queries(topic_keywords)

        # In a real implementation, you would:
        # 1. Make Google Search API calls
        # 2. Parse AI Overview results
        # 3. Check if FAQ content is cited

        # For now, we simulate based on FAQ quality
        for i, faq in enumerate(faq_items[:5]):
            # Simulate attribution check
            if self._estimate_attribution_likelihood(faq):
                attributions.append(
                    AIOAttribution(
                        video_id=video_id,
                        query=queries[i % len(queries)]
                        if queries
                        else f"query about {topic_keywords[0] if topic_keywords else 'topic'}",
                        faq_item_matched=faq[:200],
                        position=i + 1,
                        detected_at=datetime.utcnow(),
                        estimated_traffic=self._estimate_traffic(i + 1),
                    )
                )

        # Cache results
        self._attribution_cache[video_id] = attributions

        return attributions

    async def generate_aio_report(
        self,
        video_ids: List[str],
        date_range_days: int = 30,
    ) -> List[AIOPerformanceReport]:
        """Generate AIO performance reports for videos.

        Args:
            video_ids: List of video IDs to analyze
            date_range_days: Number of days to analyze

        Returns:
            List of AIOPerformanceReport objects
        """
        reports: List[AIOPerformanceReport] = []

        for video_id in video_ids:
            # Get cached attributions or fetch new ones
            attributions = self._attribution_cache.get(video_id, [])

            if not attributions:
                # Simulate some data for demonstration
                total_attributions = 0
                top_queries = []
                best_faqs = []
                attribution_rate = 0.0
                estimated_traffic = 0
                trend = "stable"
            else:
                total_attributions = len(attributions)
                top_queries = [a.query for a in attributions[:5]]
                best_faqs = [a.faq_item_matched for a in attributions[:3]]
                attribution_rate = min(total_attributions / 10, 1.0)  # Max 100%
                estimated_traffic = sum(a.estimated_traffic for a in attributions)
                trend = self._calculate_trend(video_id)

            suggestions = self._generate_report_suggestions(attribution_rate, total_attributions)

            report = AIOPerformanceReport(
                video_id=video_id,
                total_attributions=total_attributions,
                top_queries=top_queries,
                best_performing_faqs=best_faqs,
                attribution_rate=attribution_rate,
                estimated_aio_traffic=estimated_traffic,
                optimization_suggestions=suggestions,
                trend=trend,
            )

            reports.append(report)

            # Store in history
            if video_id not in self._performance_history:
                self._performance_history[video_id] = []
            self._performance_history[video_id].append(report)

        return reports

    def get_optimization_feedback(
        self,
        historical_data: Optional[List[AIOAttribution]] = None,
    ) -> AIOFeedbackForOrchestrator:
        """Generate optimization feedback for the orchestrator.

        Args:
            historical_data: Optional historical attribution data

        Returns:
            AIOFeedbackForOrchestrator with recommendations
        """
        # Analyze all cached data if no specific data provided
        if historical_data is None:
            historical_data = []
            for attributions in self._attribution_cache.values():
                historical_data.extend(attributions)

        # Identify top performing patterns
        top_patterns = self._identify_top_patterns(historical_data)

        # Get recommended question formats
        recommended_formats = list(self.RECOMMENDED_FORMATS.keys())

        # Identify high-attribution topics
        high_attribution_topics = self._identify_high_topics(historical_data)

        # Identify underperforming FAQs
        underperforming = self._identify_underperforming(historical_data)

        # Generate suggestions
        suggestions = self._generate_optimization_suggestions(historical_data)

        return AIOFeedbackForOrchestrator(
            top_performing_patterns=top_patterns,
            recommended_question_formats=recommended_formats,
            high_attribution_topics=high_attribution_topics,
            underperforming_faqs=underperforming,
            suggestions=suggestions,
            optimal_faq_length=175,  # Characters
            optimal_faq_count=5,  # FAQs per video
        )

    def _extract_topics(self, title: str) -> List[str]:
        """Extract topic keywords from title."""
        # Simple extraction - in production, use NLP
        words = title.lower().split()
        # Filter common words
        stop_words = {"the", "a", "an", "is", "are", "how", "to", "what", "why", "for", "with", "and", "or", "in", "on"}
        topics = [w for w in words if w not in stop_words and len(w) > 3]
        return topics[:5]

    def _generate_search_queries(self, topics: List[str]) -> List[str]:
        """Generate search queries from topics."""
        queries = []
        for topic in topics[:3]:
            for pattern in self.SEARCH_PATTERNS[:5]:
                queries.append(pattern.format(topic=topic, alternative="alternative"))
        return queries

    def _estimate_attribution_likelihood(self, faq: str) -> bool:
        """Estimate likelihood of FAQ being cited in AIO."""
        # Simple heuristics
        faq_lower = faq.lower()

        positive_signals = [
            len(faq) > 100,  # Substantial content
            "?" in faq,  # Contains question
            any(word in faq_lower for word in ["how", "what", "why", "when", "best"]),
            faq_lower.startswith(("how", "what", "why", "when", "is", "can", "does")),
        ]

        return sum(positive_signals) >= 2

    def _estimate_traffic(self, position: int) -> int:
        """Estimate traffic based on AIO position."""
        # Position 1 gets most traffic, decreasing
        base_traffic = 100
        return max(base_traffic // position, 10)

    def _calculate_trend(self, video_id: str) -> str:
        """Calculate attribution trend for a video."""
        history = self._performance_history.get(video_id, [])
        if len(history) < 2:
            return "stable"

        recent = history[-1].total_attributions
        previous = history[-2].total_attributions

        if recent > previous * 1.1:
            return "improving"
        elif recent < previous * 0.9:
            return "declining"
        else:
            return "stable"

    def _generate_report_suggestions(self, attribution_rate: float, total_attributions: int) -> List[str]:
        """Generate suggestions based on report metrics."""
        suggestions = []

        if attribution_rate < 0.1:
            suggestions.append("Low attribution rate - consider restructuring FAQs with direct question-answer format")
            suggestions.append("Add more 'How to' and 'What is' style questions")

        if total_attributions < 3:
            suggestions.append("Add more FAQ items (aim for 5-7 per video)")
            suggestions.append("Use specific, searchable questions that users actually ask")

        if attribution_rate > 0.3:
            suggestions.append("Good attribution rate! Consider creating more content on similar topics")

        if not suggestions:
            suggestions.append("Performance looks good - maintain current FAQ strategy")

        return suggestions

    def _identify_top_patterns(self, data: List[AIOAttribution]) -> List[str]:
        """Identify top performing FAQ patterns."""
        if not data:
            return self.HIGH_PERFORMING_PATTERNS[:5]

        # In production, analyze actual FAQ content
        return self.HIGH_PERFORMING_PATTERNS[:5]

    def _identify_high_topics(self, data: List[AIOAttribution]) -> List[str]:
        """Identify topics with high attribution rates."""
        if not data:
            return []

        # Extract topics from queries
        topics = []
        for attr in data:
            words = attr.query.lower().split()
            topics.extend([w for w in words if len(w) > 4])

        # Count occurrences
        from collections import Counter

        topic_counts = Counter(topics)
        return [topic for topic, _ in topic_counts.most_common(5)]

    def _identify_underperforming(self, data: List[AIOAttribution]) -> List[str]:
        """Identify underperforming FAQ patterns."""
        # In production, compare expected vs actual attributions
        return [
            "Vague questions without specific keywords",
            "FAQs longer than 300 characters",
            "Questions not starting with interrogative words",
        ]

    def _generate_optimization_suggestions(self, data: List[AIOAttribution]) -> List[str]:
        """Generate optimization suggestions."""
        suggestions = [
            "Start FAQ questions with 'What', 'How', 'Why', or 'Is'",
            "Keep answers between 100-200 characters for optimal AIO citation",
            "Include the main topic keyword in both question and answer",
            "Use numbered steps for 'How to' questions",
            "Add year (2026) to time-sensitive topics",
            "Structure answers to directly answer the question in the first sentence",
            "Include specific numbers or statistics when relevant",
        ]

        if data and len(data) > 5:
            # Add data-driven suggestions
            avg_traffic = sum(a.estimated_traffic for a in data) / len(data)
            if avg_traffic > 50:
                suggestions.insert(0, "Current strategy is working well - scale similar content")

        return suggestions


# Global instance
aio_tracker = AIOTracker()
