"""
Mock Provider for YT-Factory MCP Gateway

Provides mock responses for all external API calls when MOCK_MODE=true.
This allows testing the full integration flow without real API credentials.
"""

import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


def is_mock_mode() -> bool:
    """Check if mock mode is enabled."""
    return os.getenv("MOCK_MODE", "false").lower() in ("true", "1", "yes")


# ===========================================
# Mock Data Generators
# ===========================================

@dataclass
class MockTrendingTopic:
    """Mock trending topic data."""
    keyword: str
    search_volume: int
    volume_change_percent: float
    classification: str
    authority_score: int
    related_queries: List[str]
    suggested_angles: List[str]


MOCK_TREND_KEYWORDS = [
    ("AI coding assistants", "established", 85),
    ("Claude Code", "emerging", 62),
    ("GPT-5 release date", "fleeting", 35),
    ("machine learning basics", "evergreen", 90),
    ("Python 3.14 features", "emerging", 55),
    ("remote work productivity", "established", 78),
    ("sustainable tech", "emerging", 48),
    ("quantum computing explained", "evergreen", 72),
    ("cybersecurity trends 2026", "established", 81),
    ("no-code platforms", "established", 75),
]


def generate_mock_trending_topics(
    category: str,
    geo: str = "US",
    max_results: int = 10
) -> Dict[str, Any]:
    """Generate mock trending topics response."""
    topics = []

    for keyword, classification, base_authority in MOCK_TREND_KEYWORDS[:max_results]:
        # Add some randomness
        authority = base_authority + random.randint(-5, 5)
        volume = random.randint(10000, 100000)
        change = random.uniform(-20, 200)

        topics.append({
            "keyword": keyword,
            "search_volume": volume,
            "volume_change_percent": round(change, 1),
            "classification": classification,
            "authority_score": min(100, max(0, authority)),
            "classification_factors": {
                "news_coverage_count": random.randint(0, 20),
                "has_wikipedia": classification in ("established", "evergreen"),
                "days_trending": random.randint(1, 30),
                "social_velocity": round(random.uniform(0.2, 0.9), 2)
            },
            "related_queries": [
                f"{keyword} tutorial",
                f"{keyword} examples",
                f"best {keyword}",
            ],
            "related_entities": [],
            "suggested_angles": [
                f"Complete Guide to {keyword}",
                f"{keyword}: What You Need to Know in 2026",
                f"Top 10 {keyword} Tips for Beginners",
            ]
        })

    return {
        "topics": topics,
        "cache_hit": False,
        "cache_expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "api_quota_remaining": 950,
        "clusters": [
            {
                "primary_keyword": topics[0]["keyword"] if topics else "AI",
                "related_keywords": [t["keyword"] for t in topics[1:3]],
                "cluster_score": 0.72,
                "suggested_title": f"The Complete Guide to {category.title()}",
                "combined_authority": 82,
                "rationale": "These topics are strongly correlated in search patterns."
            }
        ] if len(topics) >= 3 else []
    }


def generate_mock_search_results(query: str, num_results: int = 10) -> Dict[str, Any]:
    """Generate mock search results response."""
    results = []

    sources = [
        ("Wikipedia", "wikipedia.org", "high"),
        ("TechCrunch", "techcrunch.com", "medium"),
        ("Medium", "medium.com", "medium"),
        ("Stack Overflow", "stackoverflow.com", "high"),
        ("GitHub", "github.com", "high"),
        ("Reddit", "reddit.com", "low"),
        ("Dev.to", "dev.to", "medium"),
        ("Hacker News", "news.ycombinator.com", "medium"),
    ]

    for i, (source, domain, authority) in enumerate(sources[:num_results]):
        results.append({
            "title": f"{query} - {source} Article {i+1}",
            "url": f"https://{domain}/article/{query.replace(' ', '-').lower()}-{i+1}",
            "snippet": f"This article covers {query} in detail, providing comprehensive information about the topic. Learn more about {query} and its applications.",
            "source_authority": authority,
            "publish_date": (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat()
        })

    return {
        "results": results,
        "entities": [
            {
                "name": query.split()[0] if query else "Topic",
                "type": "concept",
                "description": f"A concept related to {query}",
                "wiki_url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "related_entities": []
            }
        ],
        "knowledge_panel": {
            "title": query,
            "description": f"Information about {query}",
            "source": "Mock Knowledge Graph"
        },
        "fact_check_summary": f"Found {len(results)} sources. {sum(1 for r in results if r['source_authority'] == 'high')} high-authority sources support this topic."
    }


def generate_mock_publish_response(
    title: str,
    is_short: bool = False
) -> Dict[str, Any]:
    """Generate mock video publish response."""
    video_id = f"mock_{random.randint(10000, 99999)}"

    return {
        "success": True,
        "video_id": video_id,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "shorts_url": f"https://www.youtube.com/shorts/{video_id}" if is_short else None,
        "thumbnail_set": True,
        "comment_posted": True,
        "comment_id": f"comment_{random.randint(1000, 9999)}",
        "upload_duration_seconds": round(random.uniform(10, 60), 2),
        "file_size_bytes": random.randint(10000000, 500000000),
        "scheduled_time": None,
        "mock_mode": True
    }


def generate_mock_analytics(video_ids: List[str]) -> Dict[str, Any]:
    """Generate mock analytics response."""
    videos = []

    for video_id in video_ids:
        views = random.randint(100, 100000)
        likes = int(views * random.uniform(0.02, 0.1))
        comments = int(views * random.uniform(0.005, 0.02))
        shares = int(views * random.uniform(0.001, 0.01))

        videos.append({
            "video_id": video_id,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "watch_time_minutes": round(views * random.uniform(2, 8), 2),
            "average_view_duration_seconds": round(random.uniform(30, 300), 2),
            "average_view_percentage": round(random.uniform(20, 70), 2),
            "engagement_rate": round((likes + comments + shares) / views * 100, 2),
            "retention_score": round(random.uniform(30, 80), 2),
            "demographics": {
                "age": {
                    "18-24": round(random.uniform(10, 30), 1),
                    "25-34": round(random.uniform(25, 40), 1),
                    "35-44": round(random.uniform(15, 25), 1),
                    "45-54": round(random.uniform(10, 20), 1),
                    "55+": round(random.uniform(5, 15), 1)
                },
                "gender": {
                    "male": round(random.uniform(40, 70), 1),
                    "female": round(random.uniform(30, 60), 1)
                }
            },
            "traffic_sources": {
                "YouTube search": round(random.uniform(20, 40), 1),
                "Suggested videos": round(random.uniform(25, 45), 1),
                "Browse features": round(random.uniform(10, 25), 1),
                "External": round(random.uniform(5, 15), 1),
                "Direct": round(random.uniform(5, 10), 1)
            }
        })

    total_views = sum(v["views"] for v in videos)
    total_watch_time = sum(v["watch_time_minutes"] for v in videos)
    best_video = max(videos, key=lambda v: v["views"]) if videos else None

    return {
        "videos": videos,
        "total_views": total_views,
        "total_watch_time_minutes": round(total_watch_time, 2),
        "best_performing_video": best_video["video_id"] if best_video else None,
        "ab_analysis": {
            "winner_overall": "A" if len(videos) >= 2 else None,
            "winner_by_metric": {
                "views": "A",
                "engagement": "B",
                "retention": "A"
            },
            "improvement_percent": {"views": 15.3},
            "recommendation": "Variant A performed better overall."
        } if len(videos) == 2 else None,
        "mock_mode": True
    }


def generate_mock_comment_response(
    action: str,
    video_id: str,
    comment_text: Optional[str] = None
) -> Dict[str, Any]:
    """Generate mock comment management response."""
    return {
        "success": True,
        "comment_id": f"comment_{random.randint(1000, 9999)}",
        "action": action,
        "video_id": video_id,
        "mock_mode": True
    }


# ===========================================
# Mock TTS Provider
# ===========================================

def generate_mock_tts_audio(
    text: str,
    voice_id: str,
    output_path: str
) -> Dict[str, Any]:
    """Generate mock TTS response (creates a silent audio file placeholder)."""
    import wave
    import struct

    # Calculate approximate duration based on text length
    # Average speaking rate: ~150 words per minute
    word_count = len(text.split())
    duration_seconds = (word_count / 150) * 60

    # Create a silent WAV file
    sample_rate = 44100
    num_samples = int(sample_rate * duration_seconds)

    try:
        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)

            # Write silence (zeros)
            for _ in range(num_samples):
                wav_file.writeframes(struct.pack('h', 0))

        return {
            "success": True,
            "audio_path": output_path,
            "duration_seconds": duration_seconds,
            "mock_mode": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "mock_mode": True
        }


# ===========================================
# Integration with Server
# ===========================================

class MockProvider:
    """Central mock provider for all external services."""

    def __init__(self):
        self.enabled = is_mock_mode()

    def get_trending_topics(self, category: str, geo: str = "US", max_results: int = 10) -> Dict[str, Any]:
        """Get mock trending topics."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_trending_topics(category, geo, max_results)

    def search_facts(self, query: str, num_results: int = 10) -> Dict[str, Any]:
        """Get mock search results."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_search_results(query, num_results)

    def publish_video(self, title: str, is_short: bool = False) -> Dict[str, Any]:
        """Get mock publish response."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_publish_response(title, is_short)

    def get_analytics(self, video_ids: List[str]) -> Dict[str, Any]:
        """Get mock analytics."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_analytics(video_ids)

    def manage_comments(self, action: str, video_id: str, comment_text: Optional[str] = None) -> Dict[str, Any]:
        """Get mock comment response."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_comment_response(action, video_id, comment_text)

    def synthesize_speech(self, text: str, voice_id: str, output_path: str) -> Dict[str, Any]:
        """Generate mock TTS audio."""
        if not self.enabled:
            raise RuntimeError("Mock mode is not enabled")
        return generate_mock_tts_audio(text, voice_id, output_path)


# Global mock provider instance
mock_provider = MockProvider()
