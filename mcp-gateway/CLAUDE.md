# CLAUDE.md - YT-Factory MCP Gateway
## Production-Ready ULTIMATE Final Version (2026)
## (Complete Base + All Gemini Optimizations)

---

## 🎯 Role Definition

你是一名资深的 **Cloud Infrastructure & API Integration Expert**。
你正在构建 `yt-factory/mcp-gateway` —— 一个连接 AI 大脑与物理世界的"协议枢纽"。

这不仅仅是 API 转发，而是构建一个具备**实时感知能力**（Google Trends + Knowledge Graph）、**智能分发能力**（YouTube Publishing + Shorts 优化）、和**反馈学习能力**（Analytics + A/B Testing）的 MCP 服务端。

**核心原则：**
- **协议转换**：将复杂的 Google/YouTube API 包装成简洁的 MCP Tools
- **热词智能**：不仅获取热词，还要分类（established/fleeting/evergreen）
- **安全发布**：OAuth2 多账户管理 + 断点续传 + Shorts 专属处理
- **反馈循环**：Analytics 数据驱动内容优化
- **配额保护**：智能缓存 + 速率限制 + 指数退避

---

## 🏗️ Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────┐
│                    YT-Factory MCP Gateway (2026)                       │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│   [orchestrator] <───Stdio (MCP Protocol)───> [mcp-gateway]           │
│                                                      │                │
│   ┌──────────────────────────────────────────────────┼──────────────┐ │
│   │                    MCP TOOLS LAYER               │              │ │
│   ├──────────────────────────────────────────────────▼──────────────┤ │
│   │                                                                 │ │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│   │  │   TRENDS    │  │   SEARCH    │  │  KNOWLEDGE  │             │ │
│   │  │   SERVICE   │  │   SERVICE   │  │    GRAPH    │             │ │
│   │  │             │  │             │  │   SERVICE   │             │ │
│   │  │ • 热词获取   │  │ • 事实核查  │  │ • 实体抓取  │             │ │
│   │  │ • 趋势分级   │  │ • AIO 数据  │  │ • 关系映射  │             │ │
│   │  │ • 缓存管理   │  │ • 竞品分析  │  │ • 权威验证  │             │ │
│   │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│   │                                                                 │ │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│   │  │   YOUTUBE   │  │  ANALYTICS  │  │   COMMENT   │             │ │
│   │  │  PUBLISHER  │  │   SERVICE   │  │   SERVICE   │             │ │
│   │  │             │  │             │  │             │             │ │
│   │  │ • 视频上传   │  │ • 播放追踪  │  │ • 自动评论  │             │ │
│   │  │ • Shorts 发布│  │ • 收入报告  │  │ • 置顶管理  │             │ │
│   │  │ • 多语言 SEO │  │ • A/B 测试  │  │ • 回复模板  │             │ │
│   │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│   │                                                                 │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                              │                                        │
│   ┌──────────────────────────┼──────────────────────────────────────┐ │
│   │              INFRASTRUCTURE LAYER                               │ │
│   ├──────────────────────────▼──────────────────────────────────────┤ │
│   │                                                                 │ │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │ │
│   │  │    AUTH     │  │    CACHE    │  │    RATE     │             │ │
│   │  │   MANAGER   │  │   MANAGER   │  │   LIMITER   │             │ │
│   │  │             │  │             │  │             │             │ │
│   │  │ • OAuth2    │  │ • Redis     │  │ • 配额管理   │             │ │
│   │  │ • 多账户    │  │ • TTL 策略   │  │ • 指数退避   │             │ │
│   │  │ • Token轮换 │  │ • 热词缓存   │  │ • 优先队列   │             │ │
│   │  └─────────────┘  └─────────────┘  └─────────────┘             │ │
│   │                                                                 │ │
│   └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Python 3.11+ | AI 生态与 API 库支持最全 |
| Framework | FastMCP (Pydantic) | 快速构建 MCP 服务器 |
| Auth | google-auth-oauthlib | YouTube/Search OAuth2 |
| HTTP | httpx + asyncio | 高并发异步请求 |
| Cache | Redis / diskcache | 热词缓存 + 响应缓存 |
| Validation | Pydantic v2 | 强类型数据验证 |
| Secrets | python-dotenv + keyring | 安全凭据管理 |
| Logging | structlog | 结构化日志 |
| Retry | tenacity | 指数退避重试 |

---

## 📂 Project Structure

```
mcp-gateway/
├── src/
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── trends.py           # Google Trends + 热词分级
│   │   ├── search.py           # Google Search + AIO 事实核查
│   │   ├── knowledge.py        # Knowledge Graph API
│   │   ├── youtube.py          # 视频上传 + Shorts 发布
│   │   ├── analytics.py        # YouTube Analytics
│   │   └── comments.py         # 评论自动化
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_manager.py     # OAuth2 多账户管理
│   │   ├── cache_manager.py    # 缓存策略管理
│   │   ├── rate_limiter.py     # API 配额管理
│   │   └── webhook.py          # 完成通知
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── trends.py           # 热词相关 Schema
│   │   ├── youtube.py          # YouTube 相关 Schema
│   │   ├── analytics.py        # Analytics 相关 Schema
│   │   └── common.py           # 通用响应格式
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py           # 结构化日志
│   │   └── helpers.py          # 工具函数
│   ├── config.py               # 配置管理
│   └── server.py               # FastMCP 入口
├── tests/
│   ├── test_trends.py
│   ├── test_youtube.py
│   └── test_integration.py
├── credentials/
│   └── .gitkeep                # OAuth 凭据目录 (gitignore)
├── .env.example
├── pyproject.toml
├── Dockerfile
└── CLAUDE.md
```

---

## 📋 MCP Tools Specification

### Tool 1: `get_trending_topics` (热词获取与分级)

**Purpose:** 获取实时热词并进行智能分级

**Input Schema:**
```python
class TrendingTopicsInput(BaseModel):
    category: str = Field(
        description="内容类别: technology, finance, health, entertainment, etc."
    )
    geo: str = Field(
        default="US",
        description="地理位置代码: US, GB, CN, JP, etc."
    )
    timeframe: str = Field(
        default="now 7-d",
        description="时间范围: now 1-H, now 4-H, now 1-d, now 7-d, today 1-m"
    )
    max_results: int = Field(
        default=10,
        ge=1,
        le=25,
        description="返回结果数量"
    )
    include_related: bool = Field(
        default=True,
        description="是否包含相关查询"
    )
```

**Output Schema:**
```python
class TrendClassification(str, Enum):
    ESTABLISHED = "established"  # 稳定趋势，适合深度内容
    EMERGING = "emerging"        # 新兴趋势，适合快速跟进
    FLEETING = "fleeting"        # 短暂热点，风险较高
    EVERGREEN = "evergreen"      # 常青话题，长期价值

class TrendingTopic(BaseModel):
    keyword: str
    search_volume: int
    volume_change_percent: float  # 24h 变化
    classification: TrendClassification
    authority_score: int  # 0-100
    
    # 分级依据
    classification_factors: dict = Field(
        description="分级因子详情",
        example={
            "news_coverage_count": 15,
            "has_wikipedia": True,
            "days_trending": 12,
            "social_velocity": 0.7
        }
    )
    
    # 相关数据
    related_queries: List[str] = []
    related_entities: List[str] = []
    suggested_angles: List[str] = []  # AI 建议的切入角度

class TrendingTopicsOutput(BaseModel):
    topics: List[TrendingTopic]
    cache_hit: bool
    cache_expires_at: Optional[datetime]
    api_quota_remaining: int
```

**Implementation Logic (热词分级算法):**

```python
# src/tools/trends.py

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import httpx
from pytrends.request import TrendReq

from ..services.cache_manager import CacheManager
from ..services.rate_limiter import RateLimiter
from ..schemas.trends import (
    TrendingTopicsInput,
    TrendingTopicsOutput,
    TrendingTopic,
    TrendClassification
)
from ..utils.logger import logger


class TrendClassifier:
    """
    热词分级算法
    
    分级逻辑：
    1. ESTABLISHED: 搜索量稳定 > 7 天 + 权威来源覆盖 > 3 + authority_score > 70
    2. EMERGING: 24h 增长 > 200% + 新闻覆盖 > 5 + authority_score 40-70
    3. FLEETING: 仅社交媒体驱动 + 无权威来源 + authority_score < 40
    4. EVERGREEN: 周期性重现 + 历史数据 > 1 年 + 稳定搜索量
    """
    
    # 权威度评分因子权重
    AUTHORITY_WEIGHTS = {
        'news_coverage': 0.30,       # 主流媒体覆盖数 (0-20 mapped to 0-1)
        'wikipedia_exists': 0.20,    # 是否有维基百科条目 (0 or 1)
        'days_trending': 0.20,       # 持续趋势天数 (0-30 mapped to 0-1)
        'search_volume_stability': 0.15,  # 搜索量稳定性 (stddev inverse)
        'academic_mentions': 0.15    # 学术/官方来源 (0-10 mapped to 0-1)
    }
    
    # 分类阈值
    THRESHOLDS = {
        'established_authority': 70,
        'established_days': 7,
        'emerging_growth': 200,  # 百分比
        'emerging_news': 5,
        'fleeting_authority': 40,
        'evergreen_history_days': 365
    }
    
    async def classify(
        self,
        keyword: str,
        trend_data: dict,
        news_data: Optional[dict] = None,
        historical_data: Optional[dict] = None
    ) -> tuple[TrendClassification, int, dict]:
        """
        对单个热词进行分级
        
        Returns:
            (classification, authority_score, factors)
        """
        factors = {}
        
        # Factor 1: 新闻覆盖
        news_count = news_data.get('total_results', 0) if news_data else 0
        factors['news_coverage_count'] = news_count
        news_score = min(news_count / 20, 1.0)
        
        # Factor 2: Wikipedia 存在
        has_wikipedia = await self._check_wikipedia(keyword)
        factors['has_wikipedia'] = has_wikipedia
        wiki_score = 1.0 if has_wikipedia else 0.0
        
        # Factor 3: 趋势持续天数
        days_trending = self._calculate_days_trending(trend_data)
        factors['days_trending'] = days_trending
        days_score = min(days_trending / 30, 1.0)
        
        # Factor 4: 搜索量稳定性
        stability = self._calculate_stability(trend_data)
        factors['search_volume_stability'] = stability
        stability_score = stability  # Already 0-1
        
        # Factor 5: 学术/官方提及
        academic_count = await self._check_academic_sources(keyword)
        factors['academic_mentions'] = academic_count
        academic_score = min(academic_count / 10, 1.0)
        
        # 计算综合权威度分数
        authority_score = int(
            (news_score * self.AUTHORITY_WEIGHTS['news_coverage'] +
             wiki_score * self.AUTHORITY_WEIGHTS['wikipedia_exists'] +
             days_score * self.AUTHORITY_WEIGHTS['days_trending'] +
             stability_score * self.AUTHORITY_WEIGHTS['search_volume_stability'] +
             academic_score * self.AUTHORITY_WEIGHTS['academic_mentions']) * 100
        )
        
        # 额外因子
        volume_change = trend_data.get('volume_change_percent', 0)
        factors['volume_change_24h'] = volume_change
        
        social_velocity = trend_data.get('social_velocity', 0)
        factors['social_velocity'] = social_velocity
        
        # 分类决策
        classification = self._decide_classification(
            authority_score=authority_score,
            days_trending=days_trending,
            volume_change=volume_change,
            news_count=news_count,
            has_historical=historical_data is not None and len(historical_data.get('data', [])) > 0
        )
        
        return classification, authority_score, factors
    
    def _decide_classification(
        self,
        authority_score: int,
        days_trending: int,
        volume_change: float,
        news_count: int,
        has_historical: bool
    ) -> TrendClassification:
        """分类决策树"""
        
        # Evergreen: 有长期历史数据 + 权威度高
        if has_historical and authority_score > 60:
            return TrendClassification.EVERGREEN
        
        # Established: 稳定趋势
        if (authority_score >= self.THRESHOLDS['established_authority'] and
            days_trending >= self.THRESHOLDS['established_days']):
            return TrendClassification.ESTABLISHED
        
        # Emerging: 快速增长
        if (volume_change >= self.THRESHOLDS['emerging_growth'] and
            news_count >= self.THRESHOLDS['emerging_news']):
            return TrendClassification.EMERGING
        
        # Fleeting: 低权威度
        if authority_score < self.THRESHOLDS['fleeting_authority']:
            return TrendClassification.FLEETING
        
        # 默认为 Emerging
        return TrendClassification.EMERGING
    
    async def _check_wikipedia(self, keyword: str) -> bool:
        """检查是否有 Wikipedia 条目"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://en.wikipedia.org/w/api.php",
                    params={
                        "action": "query",
                        "titles": keyword,
                        "format": "json"
                    },
                    timeout=5.0
                )
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                # 如果返回 -1，表示页面不存在
                return "-1" not in pages
        except Exception:
            return False
    
    async def _check_academic_sources(self, keyword: str) -> int:
        """检查学术来源提及数（简化实现）"""
        # 实际可集成 Google Scholar API 或 Semantic Scholar
        return 0
    
    def _calculate_days_trending(self, trend_data: dict) -> int:
        """计算趋势持续天数"""
        # 基于 trend_data 中的时间序列数据
        timeline = trend_data.get('timeline', [])
        if not timeline:
            return 1
        
        # 计算连续有搜索量的天数
        consecutive_days = 0
        for point in reversed(timeline):
            if point.get('value', 0) > 0:
                consecutive_days += 1
            else:
                break
        
        return max(consecutive_days, 1)
    
    def _calculate_stability(self, trend_data: dict) -> float:
        """计算搜索量稳定性 (0-1，越高越稳定)"""
        timeline = trend_data.get('timeline', [])
        if not timeline or len(timeline) < 2:
            return 0.5
        
        values = [p.get('value', 0) for p in timeline]
        mean = sum(values) / len(values)
        
        if mean == 0:
            return 0.0
        
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        stddev = variance ** 0.5
        
        # 变异系数的反向指标
        cv = stddev / mean if mean > 0 else 1
        stability = max(0, 1 - cv)
        
        return round(stability, 2)


class TrendsService:
    """Google Trends 服务"""
    
    def __init__(
        self,
        cache_manager: CacheManager,
        rate_limiter: RateLimiter
    ):
        self.cache = cache_manager
        self.rate_limiter = rate_limiter
        self.classifier = TrendClassifier()
        self.pytrends = TrendReq(hl='en-US', tz=360)
    
    async def get_trending_topics(
        self,
        input_data: TrendingTopicsInput
    ) -> TrendingTopicsOutput:
        """获取热词并分级"""
        
        cache_key = f"trends:{input_data.category}:{input_data.geo}:{input_data.timeframe}"
        
        # 检查缓存
        cached = await self.cache.get(cache_key)
        if cached:
            logger.info("Trends cache hit", cache_key=cache_key)
            return TrendingTopicsOutput(
                topics=cached['topics'],
                cache_hit=True,
                cache_expires_at=cached['expires_at'],
                api_quota_remaining=self.rate_limiter.get_remaining('trends')
            )
        
        # 检查速率限制
        await self.rate_limiter.acquire('trends')
        
        # 获取趋势数据
        try:
            self.pytrends.build_payload(
                kw_list=[input_data.category],
                cat=0,
                timeframe=input_data.timeframe,
                geo=input_data.geo
            )
            
            # 获取相关查询
            related_queries = self.pytrends.related_queries()
            trending_searches = self.pytrends.trending_searches(pn=input_data.geo.lower())
            
            topics: List[TrendingTopic] = []
            
            # 处理每个热词
            for idx, row in trending_searches.head(input_data.max_results).iterrows():
                keyword = row[0] if isinstance(row, pd.Series) else str(row)
                
                # 获取该关键词的详细趋势数据
                trend_data = await self._get_keyword_trend_data(keyword, input_data)
                
                # 获取新闻覆盖
                news_data = await self._get_news_coverage(keyword)
                
                # 分级
                classification, authority_score, factors = await self.classifier.classify(
                    keyword=keyword,
                    trend_data=trend_data,
                    news_data=news_data
                )
                
                # 生成建议角度
                suggested_angles = self._generate_angles(keyword, classification)
                
                topics.append(TrendingTopic(
                    keyword=keyword,
                    search_volume=trend_data.get('search_volume', 0),
                    volume_change_percent=trend_data.get('volume_change_percent', 0),
                    classification=classification,
                    authority_score=authority_score,
                    classification_factors=factors,
                    related_queries=trend_data.get('related', [])[:5],
                    related_entities=[],  # 从 Knowledge Graph 获取
                    suggested_angles=suggested_angles
                ))
            
            # 缓存结果 (1 小时)
            cache_expires = datetime.utcnow() + timedelta(hours=1)
            await self.cache.set(
                cache_key,
                {'topics': topics, 'expires_at': cache_expires},
                ttl=3600
            )
            
            return TrendingTopicsOutput(
                topics=topics,
                cache_hit=False,
                cache_expires_at=cache_expires,
                api_quota_remaining=self.rate_limiter.get_remaining('trends')
            )
            
        except Exception as e:
            logger.error("Trends API error", error=str(e))
            raise
    
    async def _get_keyword_trend_data(
        self,
        keyword: str,
        input_data: TrendingTopicsInput
    ) -> dict:
        """获取单个关键词的详细趋势数据"""
        try:
            self.pytrends.build_payload(
                kw_list=[keyword],
                timeframe=input_data.timeframe,
                geo=input_data.geo
            )
            
            interest_over_time = self.pytrends.interest_over_time()
            
            if interest_over_time.empty:
                return {'search_volume': 0, 'volume_change_percent': 0, 'timeline': []}
            
            values = interest_over_time[keyword].tolist()
            
            # 计算 24h 变化
            if len(values) >= 2:
                recent = values[-1]
                previous = values[-2] if values[-2] > 0 else 1
                change = ((recent - previous) / previous) * 100
            else:
                change = 0
            
            return {
                'search_volume': int(values[-1]) if values else 0,
                'volume_change_percent': round(change, 1),
                'timeline': [{'value': v} for v in values],
                'related': self.pytrends.related_queries().get(keyword, {}).get('top', pd.DataFrame()).head(5).values.tolist() if hasattr(self.pytrends.related_queries().get(keyword, {}).get('top', pd.DataFrame()), 'values') else []
            }
        except Exception:
            return {'search_volume': 0, 'volume_change_percent': 0, 'timeline': []}
    
    async def _get_news_coverage(self, keyword: str) -> dict:
        """获取新闻覆盖数据"""
        # 实际实现需要 Google News API 或类似服务
        return {'total_results': 0}
    
    def _generate_angles(
        self,
        keyword: str,
        classification: TrendClassification
    ) -> List[str]:
        """基于分类生成内容角度建议"""
        base_angles = {
            TrendClassification.ESTABLISHED: [
                f"深度解析：{keyword} 的完整指南",
                f"{keyword} 专家都在用的 10 个技巧",
                f"2026 年 {keyword} 最新趋势预测"
            ],
            TrendClassification.EMERGING: [
                f"刚刚发生：{keyword} 最新动态",
                f"为什么 {keyword} 突然火了？",
                f"{keyword} 你必须知道的 5 件事"
            ],
            TrendClassification.FLEETING: [
                f"快讯：{keyword} 引发热议",
                f"网友热议：{keyword} 事件全记录"
            ],
            TrendClassification.EVERGREEN: [
                f"{keyword} 入门到精通完全教程",
                f"新手必看：{keyword} 终极指南",
                f"{keyword} 常见问题解答 FAQ"
            ]
        }
        
        return base_angles.get(classification, [])
```

---

### Tool 2: `search_facts` (事实核查与 AIO 实体)

**Purpose:** 搜索验证事实 + 获取 AIO 相关实体数据

**Input Schema:**
```python
class SearchFactsInput(BaseModel):
    query: str = Field(description="搜索查询")
    purpose: Literal['fact_check', 'entity_research', 'competitor_analysis'] = Field(
        default='fact_check',
        description="搜索目的"
    )
    num_results: int = Field(default=10, ge=1, le=20)
    include_snippets: bool = Field(default=True)
    include_entities: bool = Field(default=True)
```

**Output Schema:**
```python
class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_authority: Literal['high', 'medium', 'low']
    publish_date: Optional[datetime]

class Entity(BaseModel):
    name: str
    type: str  # person, organization, place, concept
    description: str
    wiki_url: Optional[str]
    related_entities: List[str]

class SearchFactsOutput(BaseModel):
    results: List[SearchResult]
    entities: List[Entity]
    knowledge_panel: Optional[dict]  # Google 知识面板数据
    fact_check_summary: Optional[str]
```

**Implementation:**

```python
# src/tools/search.py

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from ..services.auth_manager import AuthManager
from ..utils.logger import logger


class SearchService:
    """Google Search + Knowledge Graph 服务"""
    
    def __init__(self, auth_manager: AuthManager):
        self.auth = auth_manager
        self._search_service = None
        self._kg_service = None
    
    @property
    def search_service(self):
        if not self._search_service:
            self._search_service = build(
                'customsearch', 'v1',
                credentials=self.auth.get_credentials('search')
            )
        return self._search_service
    
    @property
    def kg_service(self):
        if not self._kg_service:
            self._kg_service = build(
                'kgsearch', 'v1',
                credentials=self.auth.get_credentials('knowledge_graph')
            )
        return self._kg_service
    
    async def search_facts(
        self,
        input_data: SearchFactsInput
    ) -> SearchFactsOutput:
        """执行搜索并提取实体"""
        
        results = []
        entities = []
        knowledge_panel = None
        
        # 执行 Google 搜索
        try:
            search_response = self.search_service.cse().list(
                q=input_data.query,
                cx=os.getenv('GOOGLE_CSE_ID'),
                num=input_data.num_results
            ).execute()
            
            for item in search_response.get('items', []):
                authority = self._assess_source_authority(item.get('link', ''))
                
                results.append(SearchResult(
                    title=item.get('title', ''),
                    url=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    source_authority=authority,
                    publish_date=self._extract_date(item)
                ))
            
            # 获取知识面板
            if 'knowledge_graph' in search_response:
                knowledge_panel = search_response['knowledge_graph']
            
        except Exception as e:
            logger.error("Search API error", error=str(e))
        
        # 获取实体数据
    nput_data.include_entities:
            entities = await self._extract_entities(input_data.query)
        
        # 事实核查摘要
        fact_summary = None
        if input_data.purpose == 'fact_check':
            fact_summary = self._generate_fact_summary(results)
        
        return SearchFactsOutput(
            results=results,
            entities=entities,
            knowledge_panel=knowledge_panel,
            fact_check_summary=fact_summary
        )
    
    async def _extract_entitiey: str) -> List[Entity]:
        """从 Knowledge Graph 提取实体"""
        try:
            response = self.kg_service.entities().search(
                query=query,
                limit=10,
                languages=['en']
            ).execute()
            
            entities = []
            for item in response.get('itemListElement', []):
                result = item.get('result', {})
                entities.append(Entity(
                    name=result.get('name', ''),
                    t.get('@type', ['Unknown'])[0] if isinstance(result.get('@type'), list) else result.get('@type', 'Unknown'),
                    description=result.get('description', ''),
                    wiki_url=result.get('detailedDescription', {}).get('url'),
                    related_entities=[]  # 需要额外查询
                ))
            
            return entities
            
        except Exception as e:
            logger.error("Knowledge Graph error", error=str(e))
            return []
    
    source_authority(self, url: str) -> Literal['high', 'medium', 'low']:
        """评估来源权威性"""
        high_authority_domains = [
            'wikipedia.org', 'gov.', 'edu.', 'bbc.com', 'nytimes.com',
            'reuters.com', 'ap.org', 'nature.com', 'sciencedirect.com'
        ]
        medium_authority_domains = [
            'medium.com', 'forbes.com', 'techcrunch.com', 'wired.com'
        ]
        
        for domain in high_authority_domains:
            if domain in url:
                r       
        for domain in medium_authority_domains:
            if domain in url:
                return 'medium'
        
        return 'low'
    
    def _extract_date(self, item: dict) -> Optional[datetime]:
        """提取发布日期"""
        # 从 meta 或 snippet 中提取日期
        return None
    
    def _generate_fact_summary(self, results: List[SearchResult]) -> str:
        """生成事实核查摘要"""
        high_auth_count = sum(1 for r in results if r.source_authority == 'hig  
        if high_auth_count >= 3:
            return f"Found {high_auth_count} high-authority sources supporting this topic."
        elif high_auth_count >= 1:
            return f"Limited high-authority sources ({high_auth_count}). Recommend additional verification."
        else:
            return "No high-authority sources found. Treat claims with caution."
```

---

### Tool 3: `publish_video` (视频上传)

**Purpose:** 上传视频到 YouTube，支持主视频和 Shorts

**Input Schema:**
```python
class VideoPrivacy(str, Enum):
    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"

class ShortsConfig(BaseModel):
    is_short: bool = True
    disable_remix: bool = True  # 防止内容被盗
    
class PublishVideoInput(BaseModel):
    video_path: str = Field(description="本地视频文件路径")
    title: str = Field(max_length=100)
    description: str = Field(max_length=5000)
    tags: List[str] = Field(max_items=500)
    category_id: str = Field(default="22")  # People & Blocy: VideoPrivacy = VideoPrivacy.PRIVATE
    
    # 多语言支持
    localized_metadata: Optional[Dict[str, dict]] = Field(
        default=None,
        description="多语言标题和描述: {'zh': {'title': '...', 'description': '...'}}"
    )
    
    # Shorts 配置
    shorts_config: Optional[ShortsConfig] = None
    
    # 章节
    chapters: Optional[str] = Field(
        default=None,
        description="章节时间戳字符串，将添加到描述"
    )
    
    # 定时发布
    scheduled_time: Optional[datetime] = None
    
    # 缩略图
    thumbnail_path: Optional[str] = None
    
    # 评论设置
    auto_comment: Optional[str] = Field(
        default=None,
        description="发布后自动发表的置顶评论"
    )
    
    # 所属频道 (多账户支持)
    channel_id: Optional[str] = None
```

**Output Schema:**
```python
class PublishVideoOutput(BaseModel):
    success: bool
    video_id: Optional[str]
    video_url: Optional[str]
    shorts_url: Optional[str]  # 如果æumbnail_set: bool
    comment_posted: bool
    comment_id: Optional[str]
    error: Optional[str]
    
    # 上传统计
    upload_duration_seconds: float
    file_size_bytes: int
```

**Implementation (含 Shorts 专属处理):**

```python
# src/tools/youtube.py

import os
import time
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUploafrom googleapiclient.errors import HttpError

from ..services.auth_manager import AuthManager
from ..services.rate_limiter import RateLimiter
from ..utils.logger import logger


# ============================================
# Shorts 必须满足的条件
# ============================================

SHORTS_REQUIREMENTS = {
    'max_duration_seconds': 60,
    'aspect_ratio': '9:16',
    'min_resolution': (1080, 1920),
    'required_hashtag': '#Shorts',
    'hashtag_position': 'description_first_line'
}


ublisher:
    """YouTube 视频发布服务"""
    
    def __init__(
        self,
        auth_manager: AuthManager,
        rate_limiter: RateLimiter
    ):
        self.auth = auth_manager
        self.rate_limiter = rate_limiter
        self._youtube_service = None
    
    def _get_youtube_service(self, channel_id: Optional[str] = None):
        """获取 YouTube API 服务实例"""
        credentials = self.auth.get_credentials('youtube', channel_id)
        return build('youtube', 'v3', credentialsials)
    
    async def publish_video(
        self,
        input_data: PublishVideoInput
    ) -> PublishVideoOutput:
        """上传视频到 YouTube"""
        
        start_time = time.time()
        file_size = os.path.getsize(input_data.video_path)
        
        # 检查速率限制
        await self.rate_limiter.acquire('youtube_upload')
        
        youtube = self._get_youtube_service(input_data.channel_id)
        
        try:
            # 准备描述 (Shorts 需要特殊处理)
   escription = self._prepare_description(input_data)
            
            # 准备元数据
            body = {
                'snippet': {
                    'title': input_data.title,
                    'description': description,
                    'tags': input_data.tags,
                    'categoryId': input_data.category_id
                },
                'status': {
                    'privacyStatus': input_data.privacy.value,
                    'selfDeclaredMadeForKids': False
                    }
            
            # 定时发布
            if input_data.scheduled_publish_time:
                body['status']['publishAt'] = input_data.scheduled_publish_time.isoformat()
                body['status']['privacyStatus'] = 'private'
            
            # 多语言本地化
            if input_data.localized_metadata:
                body['localizations'] = {}
                for lang, meta in input_data.localized_metadata.items():
                    body['localizations'][lang]                         'title': meta.get('title', input_data.title),
                        'description': meta.get('description', description)
                    }
            
            # 创建上传请求
            media = MediaFileUpload(
                input_data.video_path,
                mimetype='video/*',
                resumable=True,
                chunksize=1024 * 1024 * 10  # 10MB chunks
            )
            
            request = youtube.videos().insert(
                part='us,localizations',
                body=body,
                media_body=media
            )
            
            # 执行断点续传
            video_id = await self._resumable_upload(request)
            
            if not video_id:
                return PublishVideoOutput(
                    success=False,
                    error="Upload failed after retries",
                    upload_duration_seconds=time.time() - start_time,
                    file_size_bytes=file_size,
                  set=False,
                    comment_posted=False
                )
            
            # 设置缩略图
            thumbnail_set = False
            if input_data.thumbnail_path:
                thumbnail_set = await self._set_thumbnail(
                    youtube, video_id, input_data.thumbnail_path
                )
            
            # 发布置顶评论
            comment_posted = False
            comment_id = None
            if input_data.auto_comment:
                comment_id = aelf._post_pinned_comment(
                    youtube, video_id, input_data.auto_comment
                )
                comment_posted = comment_id is not None
            
            # 构建 URL
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            shorts_url = None
            if input_data.shorts_config and input_data.shorts_config.is_short:
                shorts_url = f"https://www.youtube.com/shorts/{video_id}"
            
            logger.info("Video published succully", 
                       video_id=video_id,
                       is_short=bool(shorts_url))
            
            return PublishVideoOutput(
                success=True,
                video_id=video_id,
                video_url=video_url,
                shorts_url=shorts_url,
                thumbnail_set=thumbnail_set,
                comment_posted=comment_posted,
                comment_id=comment_id,
                upload_duration_seconds=time.time() - start_time,
                file_size_bytes=file_size
            )
            
        except HttpError as e:
            logger.error("YouTube API error", error=str(e))
            return PublishVideoOutput(
                success=False,
                error=str(e),
                upload_duration_seconds=time.time() - start_time,
                file_size_bytes=file_size,
                thumbnail_set=False,
                comment_posted=False
            )
    
    def _prepare_description(self, input_data: PublishVideoInput) -> str:
        """准备视频描述，Shorts 需要特殊处理"""
        
        parts = []
        
        # Shorts: #Shorts 必须在第一行
        if input_data.shorts_config and input_data.shorts_config.is_short:
            parts.append("#Shorts")
            parts.append("")  # 空行
        
        # 主描述
        parts.append(input_data.description)
        
        # 章节 (非 Shorts)
        if input_data.chapters and not (input_data.shorts_config and input_data.shorts_config.is_short):       parts.append("")
            parts.append("📚 Chapters:")
            parts.append(input_data.chapters)
        
        # 标签作为 hashtags
        if input_data.tags:
            parts.append("")
            hashtags = ' '.join(f"#{tag.replace(' ', '')}" for tag in input_data.tags[:5])
            parts.append(hashtags)
        
        return '\n'.join(parts)
    
    async def _resumable_upload(self, request) -> Optional[str]:
        """执行断点续传，带指数退避重试"""
           response = None
        error = None
        retry = 0
        max_retries = 10
        
        while response is None:
            try:
                status, response = request.next_chunk()
                
                if status:
                    logger.debug("Upload progress", 
                               progress=f"{int(status.progress() * 100)}%")
                
                if response:
                    return response.get('id')
                    
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    # 服务器错误，重试
                    error = e
                    if retry < max_retries:
                        sleep_seconds = 2 ** retry
                        logger.warning("Upload error, retrying",
                                      retry=retry,
                                      sleep=sleep_seconds)
                        time.sleep(sleep_seconds)
                        retry += 1
                    else:
                        raise
                else:
                    raise
            
            except Exception as e:
                # 网络错误
                error = e
                if retry < max_retries:
                    sleep_seconds = 2 ** retry
                    logger.warning("Network error, retrying",
                                  retry=retry,
                                  sleep=sleep_seconds)
                    time.sleep(sleep_seconds)
                    r1
                else:
                    raise
        
        return None
    
    async def _set_thumbnail(
        self,
        youtube,
        video_id: str,
        thumbnail_path: str
    ) -> bool:
        """设置视频缩略图"""
        try:
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
            return True
        except HttpError as e:
            logger.error("Thumbnail set err(e))
            return False
    
    async def _post_pinned_comment(
        self,
        youtube,
        video_id: str,
        comment_text: str
    ) -> Optional[str]:
        """发布并置顶评论"""
        try:
            # 发布评论
            comment_response = youtube.commentThreads().insert(
                part='snippet',
                body={
                    'snippet': {
                        'videoId': video_id,
                        'topLevelComment': {
                      'snippet': {
                                'textOriginal': comment_text
                            }
                        }
                    }
                }
            ).execute()
            
            comment_id = comment_response['id']
            
            # 注意：置顶评论需要额外的 API 调用
            # YouTube API v3 没有直接的置顶功能
            # 需要使用 YouTube Studio API (非公开)
            
            logger.info("Comment posted", comment_d)
            return comment_id
            
        except HttpError as e:
            logger.error("Comment post error", error=str(e))
            return None
```

---

### Tool 4: `get_analytics` (数据分析)

**Purpose:** 获取视频表现数据，支持 A/B 测试分析

**Input Schema:**
```python
class AnalyticsInput(BaseModel):
    video_ids: List[str] = Field(description="视频 ID 列表")
    metrics: List[str] = Field(
        default=["views", "likes", "comments", "shares", "watchTime", "avion"],
        description="要获取的指标"
    )
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    include_demographics: bool = False
    include_traffic_sources: bool = False
```

**Output Schema:**
```python
class VideoMetrics(BaseModel):
    video_id: str
    views: int
    likes: int
    comments: int
    shares: int
    watch_time_minutes: float
    average_view_duration_seconds: float
    average_view_percentage: float
    
    # 可选的详细数据
    demographics:dict] = None
    traffic_sources: Optional[dict] = None
    
    # 计算指标
    engagement_rate: float  # (likes + comments + shares) / views
    retention_score: float  # average_view_percentage normalized

class AnalyticsOutput(BaseModel):
    videos: List[VideoMetrics]
    total_views: int
    total_watch_time_minutes: float
    best_performing_video: str
    
    # A/B 测试分析
    ab_analysis: Optional[dict] = None
```

**Implementation:**

```python
# src/tools/analytics.py

from typing import List, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel, Field
from googleapiclient.discovery import build

from ..services.auth_manager import AuthManager
from ..utils.logger import logger


class AnalyticsService:
    """YouTube Analytics 服务"""
    
    def __init__(self, auth_manager: AuthManager):
        self.auth = auth_manager
        self._analytics_service = None
    
    @property
    def analytics_service(self):
        if not self._analytics_service:
        self._analytics_service = build(
                'youtubeAnalytics', 'v2',
                credentials=self.auth.get_credentials('youtube_analytics')
            )
        return self._analytics_service
    
    async def get_analytics(
        self,
        input_data: AnalyticsInput
    ) -> AnalyticsOutput:
        """获取视频分析数据"""
        
        # 默认时间范围：过去 28 天
        end_date = input_data.end_date or date.today()
        start_date = input_data.start_date or (date - timedelta(days=28))
        
        videos_metrics = []
        
        for video_id in input_data.video_ids:
            try:
                # 基础指标
                response = self.analytics_service.reports().query(
                    ids='channel==MINE',
                    startDate=start_date.isoformat(),
                    endDate=end_date.isoformat(),
                    metrics=','.join(input_data.metrics),
                    filters=f'video=={video_id}'
                ).execute(          
                if response.get('rows'):
                    row = response['rows'][0]
                    metrics_data = dict(zip(
                        [h['name'] for h in response['columnHeaders']],
                        row
                    ))
                    
                    # 计算参与率
                    views = metrics_data.get('views', 0)
                    likes = metrics_data.get('likes', 0)
                    comments = metrics_data.get('comments', 0)
          shares = metrics_data.get('shares', 0)
                    
                    engagement_rate = 0
                    if views > 0:
                        engagement_rate = (likes + comments + shares) / views * 100
                    
                    # 计算留存分数
                    avg_view_duration = metrics_data.get('averageViewDuration', 0)
                    avg_view_percentage = metrics_data.get('averageViewPercentage', 0)
                    retention_score = min(avg_view_percentage                     
                    video_metrics = VideoMetrics(
                        video_id=video_id,
                        views=views,
                        likes=likes,
                        comments=comments,
                        shares=shares,
                        watch_time_minutes=metrics_data.get('estimatedMinutesWatched', 0),
                        average_view_duration_seconds=avg_view_duration,
                        average_view_percentage=avg_view_percentage,
                        engagement_rate=round(engagement_rate, 2),
                        retention_score=round(retention_score, 2)
                    )
                    
                    # 人口统计
                    if input_data.include_demographics:
                        video_metrics.demographics = await self._get_demographics(
                            video_id, start_date, end_date
                        )
                    
                    # 流量来源
                    if input_data.include_traffic_sources:
                        video_metrics.traffic_sources = await self._get_traffic_sources(
                            video_id, start_date, end_date
                        )
                    
                    videos_metrics.append(video_metrics)
                    
            except Exception as e:
                logger.error("Analytics error for video", 
                           video_id=video_id, error=str(e))
        
        # 汇总
        total_views = sum(v.vifor v in videos_metrics)
        total_watch_time = sum(v.watch_time_minutes for v in videos_metrics)
        
        best_video = max(videos_metrics, key=lambda v: v.views) if videos_metrics else None
        
        # A/B 测试分析
        ab_analysis = None
        if len(videos_metrics) == 2:
            ab_analysis = self._analyze_ab_test(videos_metrics[0], videos_metrics[1])
        
        return AnalyticsOutput(
            videos=videos_metrics,
            total_views=total_views,
          watch_time_minutes=total_watch_time,
            best_performing_video=best_video.video_id if best_video else None,
            ab_analysis=ab_analysis
        )
    
    async def _get_demographics(
        self,
        video_id: str,
        start_date: date,
        end_date: date
    ) -> dict:
        """获取人口统计数据"""
        try:
            response = self.analytics_service.reports().query(
                ids='channel==MINE',
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics='viewerPercentage',
                dimensions='ageGroup,gender',
                filters=f'video=={video_id}'
            ).execute()
            
            demographics = {'age': {}, 'gender': {}}
            
            for row in response.get('rows', []):
                age_group, gender, percentage = row
                demographics['age'][age_group] = demographics['age'].get(age_group, 0) + percentage
                demographics['gender'][gender] = demographics['gender'].get(gender, 0) + percentage
            
            return demographics
            
        except Exception as e:
            logger.error("Demographics error", video_id=video_id, error=str(e))
            return {}
    
    async def _get_traffic_sources(
        self,
        video_id: str,
        start_date: date,
        end_date: date
    ) -> dict:
        """获取流量来源数据"""
        try:
            response = self.analytics_service.reports().query(
                ids='channel==MINE',
                startDate=start_date.isoformat(),
                endDate=end_date.isoformat(),
                metrics='views',
                dimensions='insightTrafficSourceType',
                filters=f'video=={video_id}'
            ).execute()
            
            sources = {}
            for row in response.get('rows', []):
                source, views = row
                sources[source] = views
            
            return sources
            
        except Exception as e:
            logger.error("Traffic sources error", video_id=video_id, error=str(e))
            return {}
    
    def _analyze_ab_test(
        self,
        variant_a: VideoMetrics,
        variant_b: VideoMetrics
    ) -> dict:
        """A/B 测试分析"""
        
        # 计算各指标的胜出者
        winner_views = 'A' if variant_a.views > variant_b.views else 'B'
        winner_engagement = 'A' if variant_a.engagement_rate > variant_b.engagement_rate else 'B'
        ention = 'A' if variant_a.retention_score > variant_b.retention_score else 'B'
        
        # 计算改进百分比
        views_improvement = 0
        if min(variant_a.views, variant_b.views) > 0:
            better = max(variant_a.views, variant_b.views)
            worse = min(variant_a.views, variant_b.views)
            views_improvement = ((better - worse) / worse) * 100
        
        return {
            'winner_overall': winner_views,
            'winner_by_metric': {
                'viewss,
                'engagement': winner_engagement,
                'retention': winner_retention
            },
            'improvement_percent': {
                'views': round(views_improvement, 1)
            },
            'recommendation': f"Variant {winner_views} performed better overall. "
                            f"Consider using similar elements for future videos."
        }
```

---

### Tool 5: `manage_comments` (评论管理)

**Purpose:** 自动化评论管理

**Input Schema:**
```python CommentAction(str, Enum):
    POST = "post"
    PIN = "pin"
    REPLY = "reply"
    DELETE = "delete"
    HIDE = "hide"

class ManageCommentsInput(BaseModel):
    action: CommentAction
    video_id: str
    
    # POST/REPLY
    comment_text: Optional[str] = None
    reply_to_comment_id: Optional[str] = None
    
    # PIN/DELETE/HIDE
    comment_id: Optional[str] = None
    
    # 批量回复模板
    auto_reply_enabled: bool = False
    reply_templates: Optional[List[str]] = None
```

**Implementation:n
# src/tools/comments.py

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..services.auth_manager import AuthManager
from ..utils.logger import logger


class CommentsService:
    """评论管理服务"""
    
    def __init__(self, auth_manager: AuthManager):
        self.auth = auth_manager
    
    def _get_youtube_service(self, channel_id: Optional[str] = None):
        = self.auth.get_credentials('youtube', channel_id)
        return build('youtube', 'v3', credentials=credentials)
    
    async def manage_comments(
        self,
        input_data: ManageCommentsInput
    ) -> dict:
        """执行评论操作"""
        
        youtube = self._get_youtube_service()
        
        try:
            if input_data.action == CommentAction.POST:
                return await self._post_comment(
                    youtube,
                    input_data.video_id,
        input_data.comment_text
                )
            
            elif input_data.action == CommentAction.REPLY:
                return await self._reply_to_comment(
                    youtube,
                    input_data.reply_to_comment_id,
                    input_data.comment_text
                )
            
            elif input_data.action == CommentAction.DELETE:
                return await self._delete_comment(
                    youtube,
                    input_data.comment_id
                )
            
            elif input_data.action == CommentAction.HIDE:
                return await self._hide_comment(
                    youtube,
                    input_data.comment_id
                )
            
            else:
                return {'success': False, 'error': 'Unknown action'}
                
        except HttpError as e:
            logger.error("Comments API error", error=str(e))
            return {'success': False, 'error': str(e)}
    
    async def _post_comment(
        self,
        youtube,
        video_id: str,
        text: str
    ) -> dict:
        """发布评论"""
        response = youtube.commentThreads().insert(
            part='snippet',
            body={
                'snippet': {
                    'videoId': video_id,
                    'topLevelComment': {
                        'snippet': {
                            'textOriginal': text
                        }
                    }
                }
            }
        ).execut    
        return {
            'success': True,
            'comment_id': response['id'],
            'action': 'posted'
        }
    
    async def _reply_to_comment(
        self,
        youtube,
        parent_id: str,
        text: str
    ) -> dict:
        """回复评论"""
        response = youtube.comments().insert(
            part='snippet',
            body={
                'snippet': {
                    'parentId': parent_id,
                    'textOriginal': text
                }
    }
        ).execute()
        
        return {
            'success': True,
            'comment_id': response['id'],
            'action': 'replied'
        }
    
    async def _delete_comment(
        self,
        youtube,
        comment_id: str
    ) -> dict:
        """删除评论"""
        youtube.comments().delete(id=comment_id).execute()
        
        return {
            'success': True,
            'comment_id': comment_id,
            'action': 'deleted'
        }
    
    async def _hent(
        self,
        youtube,
        comment_id: str
    ) -> dict:
        """隐藏评论"""
        youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus='heldForReview'
        ).execute()
        
        return {
            'success': True,
            'comment_id': comment_id,
            'action': 'hidden'
        }
```

---

## 🔐 Services Layer

### OAuth2 Multi-Account Manager (src/services/auth_manager.py)

```python
# src/services/auth_managert os
import json
from typing import Optional, Dict
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from ..utils.logger import logger


# API 权限范围
SCOPES = {
    'youtube': [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtubepartner'
    ],
    'youtube_s': [
        'https://www.googleapis.com/auth/yt-analytics.readonly'
    ],
    'search': [
        'https://www.googleapis.com/auth/customsearch'
    ],
    'knowledge_graph': []  # 使用 API Key，不需要 OAuth
}


class AuthManager:
    """
    多账户 OAuth2 管理器
    
    支持：
    - 多 YouTube 频道
    - 自动 Token 刷新
    - 凭据加密存储
    """
    
    def __init__(
        self,
        credentials_dir: str = './credentials',
        client_secrets_file: str = './credentent_secrets.json'
    ):
        self.credentials_dir = Path(credentials_dir)
        self.client_secrets_file = Path(client_secrets_file)
        self._credentials_cache: Dict[str, Credentials] = {}
    
    def get_credentials(
        self,
        service: str,
        channel_id: Optional[str] = None
    ) -> Credentials:
        """
        获取指定服务的凭据
        
        Args:
            service: youtube, youtube_analytics, search, knowledge_graph
            channel_id: 可选的频道       """
        
        cache_key = f"{service}:{channel_id or 'default'}"
        
        # 检查缓存
        if cache_key in self._credentials_cache:
            creds = self._credentials_cache[cache_key]
            if creds.valid:
                return creds
            elif creds.expired and creds.refresh_token:
                creds.refresh(Request())
                self._save_credentials(service, channel_id, creds)
                return creds
        
        # 尝试加载已保存的凭æds = self._load_credentials(service, channel_id)
        
        if creds and creds.valid:
            self._credentials_cache[cache_key] = creds
            return creds
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            self._save_credentials(service, channel_id, creds)
            self._credentials_cache[cache_key] = creds
            return creds
        
        # 需要新的授权
        creds = self._authorize(service, channel_idlf._credentials_cache[cache_key] = creds
        return creds
    
    def _load_credentials(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Optional[Credentials]:
        """从文件加载凭据"""
        token_file = self._get_token_file_path(service, channel_id)
        
        if not token_file.exists():
            return None
        
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            return Cr             token=token_data['token'],
                refresh_token=token_data.get('refresh_token'),
                token_uri=token_data.get('token_uri'),
                client_id=token_data.get('client_id'),
                client_secret=token_data.get('client_secret'),
                scopes=token_data.get('scopes')
            )
        except Exception as e:
            logger.error("Failed to load credentials", error=str(e))
            return None
    
    def _save_credentials(
        self,
        service: str,
        channel_id: Optional[str],
        credentials: Credentials
    ):
        """保存凭据到文件"""
        token_file = self._get_token_file_path(service, channel_id)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': cent_secret,
            'scopes': list(credentials.scopes) if credentials.scopes else []
        }
        
        with open(token_file, 'w') as f:
            json.dump(token_data, f)
        
        logger.info("Credentials saved", service=service, channel_id=channel_id)
    
    def _authorize(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Credentials:
        """执行 OAuth2 授权流程"""
        scopes = SCOPES.get(service, [])
        
        if not scopes:
      ValueError(f"Unknown service: {service}")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.client_secrets_file),
            scopes=scopes
        )
        
        credentials = flow.run_local_server(port=0)
        self._save_credentials(service, channel_id, credentials)
        
        logger.info("New authorization completed", service=service)
        return credentials
    
    def _get_token_file_path(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Path:
        """获取 token 文件路径"""
        filename = f"token_{service}"
        if channel_id:
            filename += f"_{channel_id}"
        filename += ".json"
        
        return self.credentials_dir / filename
    
    def list_authorized_accounts(self) -> Dict[str, list]:
        """列出所有已授权的账户"""
        accounts = {'youtube': [], 'youtube_analytics': [], 'search': []}
        
        for token_file in self.credentials_dir.glob('token_*.json'):
            parts = token_file.stem.split('_')
            if len(parts) >= 2:
                service = parts[1]
                channel_id = parts[2] if len(parts) > 2 else 'default'
                
                if service in accounts:
                    accounts[service].append(channel_id)
        
        return accounts
```

---

### Cache Manager (src/services/cache_manager.py)

```python
# src/services/cache_manager.py

import json
import hashlib
from typing import Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import aiofiles
import asyncio

from ..utils.logger import logger


class CacheManager:
    """
    本地文件缓存管理器
    
    用于：
    - 热词数据缓存 (1 小时 TTL)
    - 搜索结果缓存 (30 分钟 TTL)
    - API 响应缓存
    """
    
    def __init__(self, cache_dir: str = './.cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            async with aiofiles.open(cache_file, 'r') as f:
                content = await f.read()
                data = json.loads(content)
            
            # 检查过期
            expires_at = datetime.fromisoformat(data['expires_at'])
            if datetime.utcnow() > expires_:
                # 过期，删除
                cache_file.unlink()
                return None
            
            return data['value']
            
        except Exception as e:
            logger.error("Cache read error", key=key, error=str(e))
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600  # 默认 1 小时
    ) -> bool:
        """设置缓存值"""
        cache_file = self._get_cache_file(key)
        
        tr   expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            data = {
                'value': value,
                'expires_at': expires_at.isoformat(),
                'created_at': datetime.utcnow().isoformat()
            }
            
            async with self._lock:
                async with aiofiles.open(cache_file, 'w') as f:
                    await f.write(json.dumps(data, default=str))
            
            return True
            
        except Exception as e:
            logger.error("Cache write error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        cache_file = self._get_cache_file(key)
        
        if cache_file.exists():
            cache_file.unlink()
            return True
        
        return False
    
    async def clear_expired(self):
        """清理所有过期缓存"""
        count = 0
        
        for cache_file in self.cache_dir.glob('*.json'):
            try:
        async with aiofiles.open(cache_file, 'r') as f:
                    content = await f.read()
                    data = json.loads(content)
                
                expires_at = datetime.fromisoformat(data['expires_at'])
                if datetime.utcnow() > expires_at:
                    cache_file.unlink()
                    count += 1
                    
            except Exception:
                pass
        
        logger.info("Cache cleanup completed", cleared=count)
    
    def _get_cache_file(self, key: str) -> Path:
        """获取缓存文件路径"""
        # 使用 MD5 哈希作为文件名
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"
```

---

### Rate Limiter (src/services/rate_limiter.py)

```python
# src/services/rate_limiter.py

import asyncio
from typing import Dict
from datetime import datetime, timedelta
from dataclasses import dataclass
from ..utils.logger import logger


@dataclass
class RateLimit:   requests_per_day: int
    requests_per_minute: int
    current_day_count: int = 0
    current_minute_count: int = 0
    last_day_reset: datetime = None
    last_minute_reset: datetime = None


# API 配额限制
API_LIMITS = {
    'trends': RateLimit(requests_per_day=1000, requests_per_minute=60),
    'search': RateLimit(requests_per_day=10000, requests_per_minute=100),
    'youtube_upload': RateLimit(requests_per_day=50, requests_per_minute=5),
    'youtube_analytics': RateLimit(requests_per_day=10000, _per_minute=100),
    'knowledge_graph': RateLimit(requests_per_day=10000, requests_per_minute=100),
}


class RateLimiter:
    """
    API 速率限制器
    
    支持：
    - 每日配额
    - 每分钟配额
    - 指数退避
    """
    
    def __init__(self):
        self.limits: Dict[str, RateLimit] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        
        # 初始化限制
        for api, limit in API_LIMITS.items():
            self.limits[api] = RateLimit(
                requ_per_day=limit.requests_per_day,
                requests_per_minute=limit.requests_per_minute,
                last_day_reset=datetime.utcnow(),
                last_minute_reset=datetime.utcnow()
            )
            self._locks[api] = asyncio.Lock()
    
    async def acquire(self, api: str) -> bool:
        """
        获取 API 调用许可
        
        Returns:
            True if allowed, raises exception if rate limited
        """
        if api not in self.limits:
            return True      async with self._locks[api]:
            limit = self.limits[api]
            now = datetime.utcnow()
            
            # 重置每日计数
            if now - limit.last_day_reset > timedelta(days=1):
                limit.current_day_count = 0
                limit.last_day_reset = now
            
            # 重置每分钟计数
            if now - limit.last_minute_reset > timedelta(minutes=1):
                limit.current_minute_count = 0
                limit.last_minute_reset = n     
            # 检查每日限制
            if limit.current_day_count >= limit.requests_per_day:
                wait_seconds = (limit.last_day_reset + timedelta(days=1) - now).total_seconds()
                logger.warning("Daily rate limit reached", 
                             api=api, 
                             wait_seconds=wait_seconds)
                raise RateLimitExceeded(f"Daily limit for {api}", wait_seconds)
            
            # 检查每分钟限制
            if limit.currenount >= limit.requests_per_minute:
                wait_seconds = (limit.last_minute_reset + timedelta(minutes=1) - now).total_seconds()
                logger.warning("Minute rate limit reached", 
                             api=api, 
                             wait_seconds=wait_seconds)
                await asyncio.sleep(wait_seconds)
                limit.current_minute_count = 0
                limit.last_minute_reset = datetime.utcnow()
            
            # 更新计数
            limit.currcount += 1
            limit.current_minute_count += 1
            
            return True
    
    def get_remaining(self, api: str) -> int:
        """获取剩余配额"""
        if api not in self.limits:
            return -1
        
        limit = self.limits[api]
        return limit.requests_per_day - limit.current_day_count


class RateLimitExceeded(Exception):
    """速率限制异常"""
    
    def __init__(self, message: str, wait_seconds: float):
        super().__init__(message)
        t_seconds = wait_seconds
```

---

## 🚀 FastMCP Server Entry Point

```python
# src/server.py

import os
from dotenv import load_dotenv
from fastmcp import FastMCP

from .tools.trends import TrendsService, TrendingTopicsInput, TrendingTopicsOutput
from .tools.search import SearchService, SearchFactsInput, SearchFactsOutput
from .tools.youtube import YouTubePublisher, PublishVideoInput, PublishVideoOutput
from .tools.analytics import AnalyticsService, AnalyticsInput, AnalyticsOutput
from .tools.comments iort CommentsService, ManageCommentsInput

from .services.auth_manager import AuthManager
from .services.cache_manager import CacheManager
from .services.rate_limiter import RateLimiter

from .utils.logger import setup_logger

# 加载环境变量
load_dotenv()

# 初始化日志
logger = setup_logger()

# 创建 MCP 服务器
mcp = FastMCP("yt-factory-gateway")

# 初始化服务
auth_manager = AuthManager()
cache_manager = CacheManager()
rate_limiter = RateLimiter()

trends_service = TrendsService(cache_mae_limiter)
search_service = SearchService(auth_manager)
youtube_publisher = YouTubePublisher(auth_manager, rate_limiter)
analytics_service = AnalyticsService(auth_manager)
comments_service = CommentsService(auth_manager)


# ============================================
# MCP Tool 注册
# ============================================

@mcp.tool()
async def get_trending_topics(
    category: str,
    geo: str = "US",
    timeframe: str = "now 7-d",
    max_results: int = 10,
    include_related: bool = True
)TrendingTopicsOutput:
    """
    获取实时热词并进行智能分级
    
    分级类型：
    - established: 稳定趋势，适合深度内容
    - emerging: 新兴趋势，适合快速跟进
    - fleeting: 短暂热点，风险较高
    - evergreen: 常青话题，长期价值
    """
    input_data = TrendingTopicsInput(
        category=category,
        geo=geo,
        timeframe=timeframe,
        max_results=max_results,
        include_related=include_related
    )
    return await trendsvice.get_trending_topics(input_data)


@mcp.tool()
async def search_facts(
    query: str,
    purpose: str = "fact_check",
    num_results: int = 10,
    include_snippets: bool = True,
    include_entities: bool = True
) -> SearchFactsOutput:
    """
    搜索验证事实并获取相关实体数据
    
    用途：
    - fact_check: 事实核查
    - entity_research: 实体研究
    - competitor_analysis: 竞品分析
    """
    input_data = SearchFactsInput(
        query=query,
        purpose=purp num_results=num_results,
        include_snippets=include_snippets,
        include_entities=include_entities
    )
    return await search_service.search_facts(input_data)


@mcp.tool()
async def publish_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    privacy: str = "private",
    is_short: bool = False,
    thumbnail_path: str = None,
    auto_comment: str = None,
    channel_id: str = None
) -> PublishVideoOutput:
    """
    上传视频到 YouTube
    
    支持ïts
    - 自动添加 #Shorts 标签
    - 缩略图设置
    - 自动发布评论
    """
    shorts_config = None
    if is_short:
        from .tools.youtube import ShortsConfig
        shorts_config = ShortsConfig(is_short=True)
    
    input_data = PublishVideoInput(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags,
        privacy=privacy,
        shorts_config=shorts_config,
        thumbnail_path=thumbnail_path,
        auto_comment=auto_commt,
        channel_id=channel_id
    )
    return await youtube_publisher.publish_video(input_data)


@mcp.tool()
async def get_analytics(
    video_ids: list,
    metrics: list = None,
    include_demographics: bool = False,
    include_traffic_sources: bool = False
) -> AnalyticsOutput:
    """
    获取视频表现数据
    
    支持：
    - 多视频批量查询
    - A/B 测试分析
    - 人口统计数据
    - 流量来源分析
    """
    input_data = AnalyticsInput(
        video_ids=video_
        metrics=metrics or ["views", "likes", "comments", "watchTime"],
        include_demographics=include_demographics,
        include_traffic_sources=include_traffic_sources
    )
    return await analytics_service.get_analytics(input_data)


@mcp.tool()
async def manage_comments(
    action: str,
    video_id: str,
    comment_text: str = None,
    comment_id: str = None,
    reply_to_comment_id: str = None
) -> dict:
    """
    管理视频评论
    
    操作类型：
    - post: 发布评论
  论
    - delete: 删除评论
    - hide: 隐藏评论
    """
    input_data = ManageCommentsInput(
        action=action,
        video_id=video_id,
        comment_text=comment_text,
        comment_id=comment_id,
        reply_to_comment_id=reply_to_comment_id
    )
    return await comments_service.manage_comments(input_data)


# ============================================
# 启动服务器
# ============================================

if __name__ == "__main__":
    mcp.run()
```

---

## 🐳 Dockon

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml poetry.lock ./

# 安装 Python 依赖
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# 复制源代码
COPY src/ ./src/

# 创建必要目录
RUN mkdir -p /app/credentials /app/.cache

# 环境变量
ENV PYTHONPATH=/app

# 入口
CMD"python", "-m", "src.server"]
```

---

## 📋 pyproject.toml

```toml
[tool.poetry]
name = "yt-factory-mcp-gateway"
version = "1.0.0"
description = "MCP Gateway for YT-Factory - Google Trends, YouTube Publishing, Analytics"
authors = ["YT-Factory Team"]

[tool.poetry.dependencies]
python = "^3.11"
fastmcp = "^0.1.0"
pydantic = "^2.0"
httpx = "^0.25"
google-api-python-client = "^2.100"
google-auth-oauthlib = "^1.1"
google-auth-httplib2 = "^0.1"
pytrends = "^4.9"
python-dotenv = "^1.0"
structlog = "^23.2"
tacity = "^8.2"
aiofiles = "^23.2"

[tool.poetry.dev-dependencies]
pytest = "^7.4"
pytest-asyncio = "^0.21"
black = "^23.9"
mypy = "^1.5"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## ✅ Definition of Done

### MCP Protocol
- [ ] `mcp-gateway` 能够通过 `stdio` 正常响应 `orchestrator` 初始化请求
- [ ] 所有 5 个 Tool 都能被正确调用和响应
- [ ] 返回数据符合 Pydantic Schema 定义

### Trends Service
- [ ] `get_trending_topics` classification` 字段的数据
- [ ] 热词分级算法正确区分 established/emerging/fleeting/evergreen
- [ ] 缓存命中率 > 80% (相同参数 1 小时内)
- [ ] API 配额消耗记录在日志中

### YouTube Publishing
- [ ] 成功在开发环境上传测试视频到 YouTube 私有
- [ ] Shorts 视频自动添加 `#Shorts` 标签在描述第一行
- [ ] 断点续传在网络中断后能够恢复
- [ ] 缩略图设置成功率 > 95%

### OAuth2
- [ ] 授权流程支持多账户
- [ ] Refresh Token 正常工作
- [ ] Token 安全存储，不在日志中出现

### Analytics
- [ ] 能够获取视频基础指标 (views, likes, comments)
- [ ] A/B 测试分析功能正常
- [ ] 人口统计和流量来源数据可选获取

### Infrastructure
- [ ] 日志包含每次 Tool 调用的耗时和 API 消耗
- [ ] 速率限制正确防止 API 超限
- [ ] Docker 镜像构建成功并可运行

---

## 🔗 Integration with Orchestrator

**通信协议：**
```
orchestrator                              mcp-gatew
     │                                         │
     │  1. get_trending_topics(technology, US) │
     │ ──────────────────────────────────────> │
     │                                         │ → Google Trends API
     │  2. TrendingTopicsOutput                │ ← 缓存检查
     │ <────────────────────────────────────── │
                                   │
     │  3. search_facts(query, fact_check)     │
     │ ──────────────────────────────────────> │
     │                                         │ → Google Search API
     │  4. SearchFactsOutput                   │ → Knowledge Graph API
     │ <────────────────────────────────────── │
     │                                     │
     │  [生成 manifest.json]                   │
     │  [video-renderer 渲染]                  │
     │                                         │
     │  5. publish_video(path, manifest)       │
     │ ──────────────────────────────────────> │
     │                                         │ → YouTube Data API
     │  6. PublishVideoOutput(video_id)        │ →     │ <────────────────────────────────────── │
     │                                         │
     │  7. get_analytics([video_id])           │
     │ ──────────────────────────────────────> │
     │                                         │ → YouTube Analytics API
     │  8. AnalyticsOutput                     │
     │ <────────────────────────────── │
```

---

## 🎯 最终检查清单

### 热词服务
- [ ] 分级算法权重配置正确？
- [ ] 缓存 TTL 为 1 小时？
- [ ] 权威度评分因子都已实现？

### YouTube 发布
- [ ] #Shorts 在描述第一行？
- [ ] 断点续传最大重试 10 次？
- [ ] 自动评论功能正常？

### 安全性
- [ ] API Key 和 Token 不在日志中？
- [ ] OAuth 凭据加密存储？
- [ ] 速率限制防止超é## 性能
- [ ] 缓存命中时响应 < 100ms？
- [ ] API 调用有超时设置？
- [ ] 并发请求正确处理？

---

# 🆕 Gemini Optimizations (Additional Services)

## 🆕 Task 1: Circuit Breaker (熔断机制)

**Purpose:** 当 API 连续失败时，保护系统免受级联故障，并向 orchestrator 返回降级状态

```python
# src/services/circuit_breaker.py

import asyncio
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Callable, Any
from datac import dataclass, field
from ..utils.logger import logger


class CircuitState(str, Enum):
    """熔断器状态"""
    CLOSED = "closed"       # 正常运行，允许所有请求
    OPEN = "open"           # 熔断，拒绝所有请求
    HALF_OPEN = "half_open" # 试探性恢复，允许有限请求


@dataclass
class CircuitBreakerConfig:
    """熔断器配置"""
    failure_threshold: int = 5          # 连续失败次数触发熔断
    recovery_timeout: int = 300         # 熔断后恢复等待æ half_open_max_requests: int = 3     # 半开状态最大试探请求数
    success_threshold: int = 2          # 半开状态成功次数后完全恢复


@dataclass
class CircuitBreakerState:
    """熔断器状态数据"""
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    half_open_request_count: int = 0


class CircuitBreaker:
    """
    熔断器实现
    
    状态转换：
    CLOSED ---(failurthreshold达到)---> OPEN
    OPEN ---(recovery_timeout后)---> HALF_OPEN
    HALF_OPEN ---(success_threshold达到)---> CLOSED
    HALF_OPEN ---(任意失败)---> OPEN
    """
    
    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitBreakerState()
        self._lock = asyncio.Lock()
    
    @property
    def state(self) -> CircuitState:
        return self._state.state   
    @property
    def is_available(self) -> bool:
        """检查服务是否可用"""
        return self._state.state != CircuitState.OPEN or self._should_attempt_recovery()
    
    def _should_attempt_recovery(self) -> bool:
        """检查是否应该尝试恢复"""
        if self._state.state != CircuitState.OPEN:
            return False
        
        if self._state.last_failure_time is None:
            return True
        
        elapsed = datetime.utcnow() - self._state.last_failure_t        return elapsed.total_seconds() >= self.config.recovery_timeout
    
    async def call(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> tuple[Any, Optional[str]]:
        """
        通过熔断器执行函数调用
        
        Returns:
            (result, status) - status 为 None 表示正常，'downgraded' 表示降级
        """
        async with self._lock:
            # 检查是否应该转换到半开状态
            if self._state.state == CircuitStOPEN:
                if self._should_attempt_recovery():
                    self._transition_to_half_open()
                else:
                    logger.warning("Circuit breaker OPEN, rejecting request",
                                 breaker=self.name)
                    return None, "downgraded"
            
            # 半开状态检查请求限制
            if self._state.state == CircuitState.HALF_OPEN:
                if self._state.half_open_request_count >= self.config.half_open_max_rets:
                    logger.warning("Circuit breaker HALF_OPEN limit reached",
                                 breaker=self.name)
                    return None, "downgraded"
                self._state.half_open_request_count += 1
        
        # 执行实际调用
        try:
            result = await func(*args, **kwargs)
            await self._record_success()
            return result, None
            
        except Exception as e:
            await self._record_failure(e)
            raissync def _record_success(self):
        """记录成功"""
        async with self._lock:
            self._state.failure_count = 0
            
            if self._state.state == CircuitState.HALF_OPEN:
                self._state.success_count += 1
                
                if self._state.success_count >= self.config.success_threshold:
                    self._transition_to_closed()
    
    async def _record_failure(self, error: Exception):
        """记录失败"""
        async with self._lock:
            self._state.failure_count += 1
            self._state.last_failure_time = datetime.utcnow()
            self._state.success_count = 0
            
            logger.warning("Circuit breaker recorded failure",
                         breaker=self.name,
                         failure_count=self._state.failure_count,
                         error=str(error))
            
            if self._state.state == CircuitState.HALF_OPEN:
                # 半开状态下任何失败都触发熔断     self._transition_to_open()
            
            elif self._state.failure_count >= self.config.failure_threshold:
                self._transition_to_open()
    
    def _transition_to_open(self):
        """转换到熔断状态"""
        self._state.state = CircuitState.OPEN
        self._state.half_open_request_count = 0
        logger.error("Circuit breaker OPENED",
                    breaker=self.name,
                    recovery_in_seconds=self.config.recovery_timeout)
    
    def _transiten(self):
        """转换到半开状态"""
        self._state.state = CircuitState.HALF_OPEN
        self._state.half_open_request_count = 0
        self._state.success_count = 0
        logger.info("Circuit breaker HALF_OPEN, attempting recovery",
                   breaker=self.name)
    
    def _transition_to_closed(self):
        """转换到关闭状态（正常）"""
        self._state.state = CircuitState.CLOSED
        self._state.failure_count = 0
        self._state.success_count = 0
       f._state.half_open_request_count = 0
        logger.info("Circuit breaker CLOSED, fully recovered",
                   breaker=self.name)
    
    def get_status(self) -> dict:
        """获取熔断器状态摘要"""
        return {
            'name': self.name,
            'state': self._state.state.value,
            'failure_count': self._state.failure_count,
            'last_failure': self._state.last_failure_time.isoformat() if self._state.last_failure_time else None,
            'is_available': sf.is_available
        }


class CircuitBreakerRegistry:
    """熔断器注册中心"""
    
    def __init__(self):
        self._breakers: dict[str, CircuitBreaker] = {}
    
    def get_or_create(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None
    ) -> CircuitBreaker:
        """获取或创建熔断器"""
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(name, config)
        return self._breakers[name]
    
    def get_all_> dict:
        """获取所有熔断器状态"""
        return {
            name: breaker.get_status()
            for name, breaker in self._breakers.items()
        }


# 全局熔断器注册中心
circuit_registry = CircuitBreakerRegistry()

# 预配置的熔断器
BREAKER_CONFIGS = {
    'youtube_upload': CircuitBreakerConfig(
        failure_threshold=3,      # YouTube 更敏感
        recovery_timeout=600,     # 10 分钟恢复
        half_open_max_requests=1
    ),
    'youtube_analytics': CircuitBreakerConfig(
        failure_threshold=5,
        recovery_timeout=300
    ),
    'google_trends': CircuitBreakerConfig(
        failure_threshold=5,
        recovery_timeout=300
    ),
    'google_search': CircuitBreakerConfig(
        failure_threshold=10,     # Search API 更宽容
        recovery_timeout=180
    )
}
```

---

## 🆕 Task 2: Pre-emptive Auth Refresh (预刷新)

**Purpose:** 在 token 过期前主动刷新，防止长时间上传中断

```python
# src/services/auth_manager.py

imort os
import json
import asyncio
from typing import Optional, Dict
from pathlib import Path
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from ..utils.logger import logger


# API 权限范围
SCOPES = {
    'youtube': [
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://wwapis.com/auth/youtubepartner'
    ],
    'youtube_analytics': [
        'https://www.googleapis.com/auth/yt-analytics.readonly'
    ],
    'search': [
        'https://www.googleapis.com/auth/customsearch'
    ],
    'knowledge_graph': []
}


class PreemptiveAuthManager:
    """
    多账户 OAuth2 管理器 + 预刷新机制
    
    关键特性：
    - 多 YouTube 频道支持
    - Pre-emptive Refresh: 在 token 过期前 N 分钟主动刷新
    - 长上传保护: 确保 token 在整个上传过程ä   
    # 预刷新时间配置
    PREEMPTIVE_REFRESH_MINUTES = 10  # 提前 10 分钟刷新
    MIN_TOKEN_VALIDITY_MINUTES = 30  # 开始上传前至少保证 30 分钟有效
    
    def __init__(
        self,
        credentials_dir: str = './credentials',
        client_secrets_file: str = './credentials/client_secrets.json'
    ):
        self.credentials_dir = Path(credentials_dir)
        self.client_secrets_file = Path(client_secrets_file)
        self._credentials_cache: Dict[str, Credentials] =        self._token_expiry_cache: Dict[str, datetime] = {}
        self._refresh_lock = asyncio.Lock()
    
    async def get_credentials(
        self,
        service: str,
        channel_id: Optional[str] = None,
        min_validity_minutes: Optional[int] = None
    ) -> Credentials:
        """
        获取指定服务的凭据
        
        Args:
            service: youtube, youtube_analytics, search, knowledge_graph
            channel_id: 可选的频道 ID（用于多账户）
            mi_minutes: 最小有效期（分钟），用于长时间操作
        """
        cache_key = f"{service}:{channel_id or 'default'}"
        min_validity = min_validity_minutes or self.PREEMPTIVE_REFRESH_MINUTES
        
        async with self._refresh_lock:
            # 检查缓存
            if cache_key in self._credentials_cache:
                creds = self._credentials_cache[cache_key]
                
                # 检查是否需要预刷新
                if self._needs_preemptive_refresh(in_validity):
                    logger.info("Pre-emptive token refresh triggered",
                              service=service,
                              channel_id=channel_id,
                              min_validity_minutes=min_validity)
                    creds = await self._refresh_credentials(creds, service, channel_id)
                    self._credentials_cache[cache_key] = creds
                    self._update_expiry_cache(cache_key, creds)
                
                elif creds.valid:
                    return creds
                
                elif creds.expired and creds.refresh_token:
                    creds = await self._refresh_credentials(creds, service, channel_id)
                    self._credentials_cache[cache_key] = creds
                    self._update_expiry_cache(cache_key, creds)
                    return creds
            
            # 尝试加载已保存的凭据
            creds = self._load_credentials(service, channel_id)
            
            if s:
                if self._needs_preemptive_refresh_for_creds(creds, min_validity):
                    creds = await self._refresh_credentials(creds, service, channel_id)
                
                self._credentials_cache[cache_key] = creds
                self._update_expiry_cache(cache_key, creds)
                return creds
            
            # 需要新的授权
            creds = await self._authorize(service, channel_id)
            self._credentials_cache[cache_key] = creds
          te_expiry_cache(cache_key, creds)
            return creds
    
    def _needs_preemptive_refresh(self, cache_key: str, min_validity_minutes: int) -> bool:
        """检查是否需要预刷新"""
        if cache_key not in self._token_expiry_cache:
            return False
        
        expiry = self._token_expiry_cache[cache_key]
        time_until_expiry = expiry - datetime.utcnow()
        
        return time_until_expiry.total_seconds() < min_validity_minutes * 60
    
    def _needs_preemptive_rresh_for_creds(self, creds: Credentials, min_validity_minutes: int) -> bool:
        """检查凭据是否需要预刷新"""
        if not creds.expiry:
            return False
        
        time_until_expiry = creds.expiry - datetime.utcnow()
        return time_until_expiry.total_seconds() < min_validity_minutes * 60
    
    def _update_expiry_cache(self, cache_key: str, creds: Credentials):
        """更新过期时间缓存"""
        if creds.expiry:
            self._token_expiry_cache[cache_kereds.expiry
    
    async def _refresh_credentials(
        self,
        creds: Credentials,
        service: str,
        channel_id: Optional[str]
    ) -> Credentials:
        """刷新凭据"""
        try:
            creds.refresh(Request())
            self._save_credentials(service, channel_id, creds)
            logger.info("Token refreshed successfully",
                       service=service,
                       channel_id=channel_id,
                       new_expiry=creds.expiry.isoformat(ds.expiry else None)
            return creds
        except Exception as e:
            logger.error("Token refresh failed", error=str(e))
            raise
    
    async def ensure_valid_for_upload(
        self,
        service: str,
        channel_id: Optional[str] = None,
        estimated_upload_minutes: int = 30
    ) -> Credentials:
        """
        确保 token 在整个上传过程中有效
        
        Args:
            estimated_upload_minutes: 预计上传时间（分钟）
        """要的最小有效期 = 预计上传时间 + 缓冲时间
        min_validity = estimated_upload_minutes + self.PREEMPTIVE_REFRESH_MINUTES
        
        return await self.get_credentials(
            service=service,
            channel_id=channel_id,
            min_validity_minutes=min_validity
        )
    
    def _load_credentials(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Optional[Credentials]:
        """从文件加载凭据"""
        token_file = self._get_token_file_path(service, channel_id)
        
        if not token_file.exists():
            return None
        
        try:
            with open(token_file, 'r') as f:
                token_data = json.load(f)
            
            creds = Credentials(
                token=token_data['token'],
                refresh_token=token_data.get('refresh_token'),
                token_uri=token_data.get('token_uri'),
                client_id=token_data.get('client_id'),
                client_secret=token_data.get('client_secret'),
                scopes=token_data.get('scopes')
            )
            
            # 设置过期时间
            if 'expiry' in token_data:
                creds.expiry = datetime.fromisoformat(token_data['expiry'])
            
            return creds
            
        except Exception as e:
            logger.error("Failed to load credentials", error=str(e))
            return None
    
    def _save_credentials(
        self,
        service: str,
        channel_istr],
        credentials: Credentials
    ):
        """保存凭据到文件"""
        token_file = self._get_token_file_path(service, channel_id)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        
        token_data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes':als.scopes) if credentials.scopes else [],
            'expiry': credentials.expiry.isoformat() if credentials.expiry else None
        }
        
        with open(token_file, 'w') as f:
            json.dump(token_data, f)
        
        logger.info("Credentials saved", service=service, channel_id=channel_id)
    
    async def _authorize(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Credentials:
        """执行 OAuth2 授权流程"""
        scopes = SCOPES.get(servi    
        if not scopes:
            raise ValueError(f"Unknown service: {service}")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.client_secrets_file),
            scopes=scopes
        )
        
        credentials = flow.run_local_server(port=0)
        self._save_credentials(service, channel_id, credentials)
        
        logger.info("New authorization completed", service=service)
        return credentials
    
    def _get_token_file_path(
        self,
        service: str,
        channel_id: Optional[str]
    ) -> Path:
        """获取 token 文件路径"""
        filename = f"token_{service}"
        if channel_id:
            filename += f"_{channel_id}"
        filename += ".json"
        
        return self.credentials_dir / filename
    
    def get_token_status(self, service: str, channel_id: Optional[str] = None) -> dict:
        """获取 token 状态"""
        cache_key = f"{service}:{channel_id or 'default'}"
        
        if cache_ket in self._credentials_cache:
            return {'status': 'not_loaded', 'service': service}
        
        creds = self._credentials_cache[cache_key]
        expiry = self._token_expiry_cache.get(cache_key)
        
        if expiry:
            time_until_expiry = expiry - datetime.utcnow()
            minutes_remaining = int(time_until_expiry.total_seconds() / 60)
        else:
            minutes_remaining = None
        
        return {
            'status': 'valid' if creds.valid else 'expired',
            'service': service,
            'channel_id': channel_id,
            'expiry': expiry.isoformat() if expiry else None,
            'minutes_remaining': minutes_remaining,
            'needs_refresh': self._needs_preemptive_refresh(cache_key, self.PREEMPTIVE_REFRESH_MINUTES)
        }
```

---

## 🆕 Task 3: Entity Clusterer (实体聚类)

**Purpose:** 识别相关热词，建议合并主题以提升内容权威度

```python
# src/services/entity_clusterer.py

from typing import List, Dict, onal, Set
from dataclasses import dataclass
from collections import defaultdict
import asyncio
import httpx

from ..utils.logger import logger


@dataclass
class TrendCluster:
    """趋势聚类结果"""
    primary_keyword: str            # 主关键词
    related_keywords: List[str]     # 相关关键词
    cluster_score: float            # 聚类强度 (0-1)
    suggested_title: str            # 建议的合并标题
    combined_authority: float       # 合并后的权威度
    rationale: str                # 合并理由


class EntityClusterer:
    """
    实体聚类服务
    
    功能：
    1. 从 Knowledge Graph 获取实体关系
    2. 计算 co-occurrence score
    3. 建议合并高相关性主题
    """
    
    # 聚类阈值
    MIN_CLUSTER_SCORE = 0.6
    MAX_CLUSTER_SIZE = 4
    
    # 共现关系类型权重
    RELATION_WEIGHTS = {
        'same_category': 0.8,
        'common_entity': 0.7,
        'semantic_similarity': 0.6,
        'temporal_correlation': 0.5
    }
    
    de__(self, knowledge_graph_service=None):
        self.kg_service = knowledge_graph_service
        self._entity_cache: Dict[str, dict] = {}
    
    async def cluster_trends(
        self,
        trends: List[dict],
        max_clusters: int = 5
    ) -> List[TrendCluster]:
        """
        对热词进行聚类
        
        Args:
            trends: 热词列表，每个包含 keyword, authority_score 等
            max_clusters: 最大聚类数量
        
        Returns:
            聚类结果     """
        if len(trends) < 2:
            return []
        
        # 获取所有热词的实体信息
        entity_map = await self._fetch_entities_batch([t['keyword'] for t in trends])
        
        # 计算两两相关性
        similarity_matrix = await self._build_similarity_matrix(trends, entity_map)
        
        # 执行聚类
        clusters = self._hierarchical_clustering(trends, similarity_matrix)
        
        # 生成聚类建议
        result_clusters = []
        for clywords in clusters[:max_clusters]:
            if len(cluster_keywords) < 2:
                continue
            
            cluster = self._create_cluster_suggestion(
                cluster_keywords,
                trends,
                entity_map,
                similarity_matrix
            )
            
            if cluster and cluster.cluster_score >= self.MIN_CLUSTER_SCORE:
                result_clusters.append(cluster)
        
        logger.info("Trend clustering completed",
                   input_trends=len(trends),
                   clusters_found=len(result_clusters))
        
        return result_clusters
    
    async def _fetch_entities_batch(
        self,
        keywords: List[str]
    ) -> Dict[str, dict]:
        """批量获取实体信息"""
        entity_map = {}
        
        for keyword in keywords:
            if keyword in self._entity_cache:
                entity_map[keyword] = self._entity_cache[keyword]
                continue
            
            try:
                entity_info = await self._fetch_entity_info(keyword)
                self._entity_cache[keyword] = entity_info
                entity_map[keyword] = entity_info
            except Exception as e:
                logger.warning("Failed to fetch entity", keyword=keyword, error=str(e))
                entity_map[keyword] = {'types': [], 'related': []}
        
        return entity_map
    
    async def _fetch_entity_info(self, keyword: str) -> dict:
        """获取单个关键词的实体信       # 实际实现需要调用 Knowledge Graph API
        # 这里是简化版本
        return {
            'types': [],      # 实体类型
            'related': [],    # 相关实体
            'categories': [], # 分类
            'description': ''
        }
    
    async def _build_similarity_matrix(
        self,
        trends: List[dict],
        entity_map: Dict[str, dict]
    ) -> Dict[tuple, float]:
        """构建相似度矩阵"""
        matrix = {}
        keywords = [t['keyword'] for t in trends]
        
        for i, kw1 in enumerate(keywords):
            for j, kw2 in enumerate(keywords):
                if i >= j:
                    continue
                
                similarity = await self._calculate_similarity(
                    kw1, kw2,
                    entity_map.get(kw1, {}),
                    entity_map.get(kw2, {})
                )
                
                matrix[(kw1, kw2)] = similarity
                matrix[(kw2, kw1)] = similarity
        
        return matrix
    
    async def _calculate_similarity(
        self,
        kw1: str,
        kw2: str,
        entity1: dict,
        entity2: dict
    ) -> float:
        """计算两个关键词的相似度"""
        scores = []
        
        # 1. 共同实体类型
        types1 = set(entity1.get('types', []))
        types2 = set(entity2.get('types', []))
        if types1 and types2:
            common_types = types1 & types2
            type_score = len(common_types) / max(len(types1),en(types2))
            scores.append(('same_category', type_score))
        
        # 2. 共同相关实体
        related1 = set(entity1.get('related', []))
        related2 = set(entity2.get('related', []))
        if related1 and related2:
            common_related = related1 & related2
            related_score = len(common_related) / max(len(related1), len(related2))
            scores.append(('common_entity', related_score))
        
        # 3. 词汇相似度（简化版）
        words1 = set(kw1.lower().split())
        words2 = set(kw2.lower().split())
        if words1 and words2:
            word_overlap = len(words1 & words2) / max(len(words1), len(words2))
            scores.append(('semantic_similarity', word_overlap))
        
        if not scores:
            return 0.0
        
        # 加权平均
        total_weight = sum(self.RELATION_WEIGHTS.get(rel, 0.5) for rel, _ in scores)
        weighted_sum = sum(
            self.RELATION_WEIGHTS.get(rel, 0.5) * score
            for re in scores
        )
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _hierarchical_clustering(
        self,
        trends: List[dict],
        similarity_matrix: Dict[tuple, float]
    ) -> List[List[str]]:
        """层次聚类"""
        keywords = [t['keyword'] for t in trends]
        clusters = [[kw] for kw in keywords]  # 初始每个关键词一个簇
        
        while len(clusters) > 1:
            # 找最相似的两个簇
            best_sc        best_pair = None
            
            for i, c1 in enumerate(clusters):
                for j, c2 in enumerate(clusters):
                    if i >= j:
                        continue
                    
                    # 计算簇间平均相似度
                    scores = []
                    for kw1 in c1:
                        for kw2 in c2:
                            if (kw1, kw2) in similarity_matrix:
                                scores.append(similarity_matrix[(kw1, kw2)
                    
                    if scores:
                        avg_score = sum(scores) / len(scores)
                        if avg_score > best_score:
                            best_score = avg_score
                            best_pair = (i, j)
            
            # 如果最佳相似度低于阈值，停止合并
            if best_score < self.MIN_CLUSTER_SCORE or best_pair is None:
                break
            
            # 合并最相似的两个簇
            i, j = be_pair
            new_cluster = clusters[i] + clusters[j]
            
            # 限制簇大小
            if len(new_cluster) <= self.MAX_CLUSTER_SIZE:
                clusters = [c for k, c in enumerate(clusters) if k not in (i, j)]
                clusters.append(new_cluster)
            else:
                break
        
        # 过滤单元素簇
        return [c for c in clusters if len(c) >= 2]
    
    def _create_cluster_suggestion(
        self,
        cluster_keywords: List[str],
    ends: List[dict],
        entity_map: Dict[str, dict],
        similarity_matrix: Dict[tuple, float]
    ) -> Optional[TrendCluster]:
        """创建聚类建议"""
        # 找出权威度最高的作为主关键词
        keyword_authority = {
            t['keyword']: t.get('authority_score', 0)
            for t in trends
            if t['keyword'] in cluster_keywords
        }
        
        primary = max(cluster_keywords, key=lambda k: keyword_authority.get(k, 0))
        related = [k for k in keywords if k != primary]
        
        # 计算聚类分数
        scores = []
        for i, kw1 in enumerate(cluster_keywords):
            for kw2 in cluster_keywords[i+1:]:
                if (kw1, kw2) in similarity_matrix:
                    scores.append(similarity_matrix[(kw1, kw2)])
        
        cluster_score = sum(scores) / len(scores) if scores else 0
        
        # 计算合并权威度
        individual_authorities = [keyword_authority.get(k, 0) for k in cluster_keywords]
       authority = min(
            100,
            max(individual_authorities) + sum(individual_authorities) * 0.1
        )
        
        # 生成建议标题
        suggested_title = self._generate_combined_title(primary, related)
        
        # 生成理由
        rationale = self._generate_rationale(primary, related, cluster_score)
        
        return TrendCluster(
            primary_keyword=primary,
            related_keywords=related,
            cluster_score=cluster_score,
            suggd_title=suggested_title,
            combined_authority=combined_authority,
            rationale=rationale
        )
    
    def _generate_combined_title(self, primary: str, related: List[str]) -> str:
        """生成合并标题建议"""
        if len(related) == 1:
            return f"{primary}: How {related[0]} Changes Everything"
        else:
            related_str = ", ".join(related[:2])
            return f"{primary}: The Complete Guide ({related_str})"
    
    def _generate_rationale(
        self,
        primary: str,
        related: List[str],
        score: float
    ) -> str:
        """生成合并理由"""
        if score > 0.8:
            strength = "strongly"
        elif score > 0.6:
            strength = "moderately"
        else:
            strength = "weakly"
        
        return (
            f"'{primary}' and {related} are {strength} correlated "
            f"(score: {score:.2f}). Combining these topics can increase "
            f"content authority and capture broadernt."
        )
```

---

## 🆕 Task 4: Publish Scheduler (智能发布窗口)

**Purpose:** 根据历史数据和受众分析，计算最佳发布时间

```python
# src/services/publish_scheduler.py

from typing import Optional, List, Dict
from datetime import datetime, timedelta, time
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import logger


class ContentType(str, Enum):
    MAIN_VIDEO = "main_video"
    SHORTS = "shorts"


class AudienceRegion(str, Enum):
    US = "USUK = "UK"
    EU = "EU"
    ASIA = "ASIA"
    GLOBAL = "GLOBAL"


@dataclass
class PublishWindow:
    """发布窗口"""
    optimal_time: datetime
    window_start: datetime
    window_end: datetime
    confidence: float  # 置信度 (0-1)
    rationale: str
    
    # 备选时间
    alternative_times: List[datetime] = None


@dataclass
class AudienceInsight:
    """受众洞察"""
    peak_hours: List[int]           # 活跃高峰小时 (0-23)
    peak_days: List[int]            # 活跃高峰星期几    timezone: str                   # 主要时区
    avg_session_length_minutes: float


class PublishScheduler:
    """
    智能发布时间调度器
    
    功能：
    1. 分析历史视频表现
    2. 考虑时区和受众分布
    3. 避开竞争高峰期
    4. 针对 Shorts 和长视频分别优化
    """
    
    # 默认最佳时间（基于行业研究）
    DEFAULT_PEAK_HOURS = {
        ContentType.MAIN_VIDEO: [14, 15, 16, 17, 18],  # 下午 2-6 点
        ContentType.SHORTS: [11, 12,9, 20, 21]   # 午餐和晚餐时段
    }
    
    DEFAULT_PEAK_DAYS = [1, 2, 3, 4]  # 周二到周五
    
    # 时区配置
    TIMEZONE_OFFSETS = {
        AudienceRegion.US: -5,      # EST
        AudienceRegion.UK: 0,       # GMT
        AudienceRegion.EU: 1,       # CET
        AudienceRegion.ASIA: 8,     # CST (China)
        AudienceRegion.GLOBAL: -5   # 默认 EST
    }
    
    def __init__(self, analytics_service=None):
        self.analytics = analytics_service
        self._audience_cache: Ditr, AudienceInsight] = {}
    
    async def get_optimal_publish_time(
        self,
        channel_id: Optional[str] = None,
        content_type: ContentType = ContentType.MAIN_VIDEO,
        target_audience: AudienceRegion = AudienceRegion.GLOBAL,
        earliest_publish: Optional[datetime] = None
    ) -> PublishWindow:
        """
        计算最佳发布时间
        
        Args:
            channel_id: 频道 ID（用于获取历史数据）
            content_type: 内容类型
            target_audience: 目标受众区域
            earliest_publish: 最早可发布时间
        """
        now = datetime.utcnow()
        earliest = earliest_publish or now
        
        # 获取受众洞察
        audience = await self._get_audience_insight(channel_id, target_audience)
        
        # 计算最佳时间
        optimal = self._calculate_optimal_time(
            content_type=content_type,
            audience=audience,
            earliest=earliest
        )
        
        # 计ç     window_start = optimal - timedelta(hours=1)
        window_end = optimal + timedelta(hours=2)
        
        # 生成备选时间
        alternatives = self._generate_alternatives(
            optimal=optimal,
            content_type=content_type,
            audience=audience,
            count=3
        )
        
        # 计算置信度
        confidence = self._calculate_confidence(channel_id, audience)
        
        # 生成理由
        rationale = self._generate_rationale(
         imal,
            content_type=content_type,
            audience=audience
        )
        
        return PublishWindow(
            optimal_time=optimal,
            window_start=window_start,
            window_end=window_end,
            confidence=confidence,
            rationale=rationale,
            alternative_times=alternatives
        )
    
    async def _get_audience_insight(
        self,
        channel_id: Optional[str],
        region: AudienceRegion
    ) -> AudienceInsight:
        """获取受众洞察"""
        cache_key = f"{channel_id or 'default'}:{region.value}"
        
        if cache_key in self._audience_cache:
            return self._audience_cache[cache_key]
        
        # 如果有 Analytics 服务，从历史数据分析
        if self.analytics and channel_id:
            try:
                insight = await self._analyze_historical_data(channel_id, region)
                self._audience_cache[cache_key] = insight
                return insight
            except Eon as e:
                logger.warning("Failed to get historical insight", error=str(e))
        
        # 使用默认值
        default_insight = AudienceInsight(
            peak_hours=self.DEFAULT_PEAK_HOURS[ContentType.MAIN_VIDEO],
            peak_days=self.DEFAULT_PEAK_DAYS,
            timezone=f"UTC{self.TIMEZONE_OFFSETS[region]:+d}",
            avg_session_length_minutes=8.0
        )
        
        self._audience_cache[cache_key] = default_insight
        return default_insight
    
    asyalyze_historical_data(
        self,
        channel_id: str,
        region: AudienceRegion
    ) -> AudienceInsight:
        """分析历史数据获取受众洞察"""
        # 实际实现需要调用 Analytics API
        # 分析过去 30 天的数据
        return AudienceInsight(
            peak_hours=[14, 15, 16, 17],
            peak_days=[1, 2, 3, 4],
            timezone="UTC-5",
            avg_session_length_minutes=8.0
        )
    
    def _calculate_optimal_time(
        self,
        cope: ContentType,
        audience: AudienceInsight,
        earliest: datetime
    ) -> datetime:
        """计算最佳发布时间"""
        # 获取目标时区的当前时间
        tz_offset = self._parse_timezone_offset(audience.timezone)
        local_now = earliest + timedelta(hours=tz_offset)
        
        # 找到下一个最佳时间点
        peak_hours = audience.peak_hours or self.DEFAULT_PEAK_HOURS[content_type]
        peak_days = audience.peak_days or self.DEFAULT_PEAK_DAYS
        
从当前时间开始，找下一个 peak hour
        candidate = local_now
        
        for days_ahead in range(7):  # 最多查找 7 天
            check_date = local_now + timedelta(days=days_ahead)
            
            # 检查是否是 peak day
            if check_date.weekday() not in peak_days:
                continue
            
            for hour in sorted(peak_hours):
                candidate_time = check_date.replace(
                    hour=hour,
                    minute=0,
        second=0,
                    microsecond=0
                )
                
                # 转回 UTC
                optimal_utc = candidate_time - timedelta(hours=tz_offset)
                
                if optimal_utc >= earliest:
                    return optimal_utc
        
        # 如果找不到，返回明天的第一个 peak hour
        tomorrow = local_now + timedelta(days=1)
        first_peak = sorted(peak_hours)[0]
        fallback = tomorrow.replace(hour=first_peak, minute=0, second=0)
        return fallback - timedelta(hours=tz_offset)
    
    def _generate_alternatives(
        self,
        optimal: datetime,
        content_type: ContentType,
        audience: AudienceInsight,
        count: int
    ) -> List[datetime]:
        """生成备选发布时间"""
        alternatives = []
        peak_hours = audience.peak_hours or self.DEFAULT_PEAK_HOURS[content_type]
        
        for delta_days in [0, 1, 2]:
            for hour in peak_hours:
                alt = optimal.replace(hour=hour) + timedelta(days=delta_days)
                if alt != optimal and alt > datetime.utcnow():
                    alternatives.append(alt)
                
                if len(alternatives) >= count:
                    return alternatives
        
        return alternatives
    
    def _calculate_confidence(
        self,
        channel_id: Optional[str],
        audience: AudienceInsight
    ) -> float:
        """计算置信度"""
        # 基础置信度
        base = 0.5
    
        # 如果有频道数据，提高置信度
        if channel_id:
            base += 0.2
        
        # 如果有详细的受众数据，进一步提高
        if audience.avg_session_length_minutes > 0:
            base += 0.1
        
        if len(audience.peak_hours) > 2:
            base += 0.1
        
        return min(base, 0.95)
    
    def _generate_rationale(
        self,
        optimal: datetime,
        content_type: ContentType,
        audience: AudienceInsight
    ) ->    """生成发布时间理由"""
        day_name = optimal.strftime("%A")
        hour = optimal.strftime("%I %p")
        
        content_desc = "video" if content_type == ContentType.MAIN_VIDEO else "Short"
        
        return (
            f"Recommended to publish this {content_desc} on {day_name} at {hour} "
            f"({audience.timezone}). This aligns with audience peak activity hours "
            f"({', '.join(f'{h}:00' for h in audience.peak_hours[:3])}...). "
            f"Expected higher initial engagement and algorithm boost."
        )
    
    def _parse_timezone_offset(self, timezone: str) -> int:
        """解析时区偏移"""
        if timezone.startswith("UTC"):
            try:
                return int(timezone[3:])
            except ValueError:
                return 0
        return 0
```

---

## 📋 Updated MCP Tools with All Optimizations

```python
# src/server.py

import os
from dotenv import load_dotenv
from fastmcp import FastMCP

from .tools.trends import TrendsSngTopicsInput, TrendingTopicsOutput
from .tools.search import SearchService, SearchFactsInput, SearchFactsOutput
from .tools.youtube import YouTubePublisher, PublishVideoInput, PublishVideoOutput
from .tools.analytics import AnalyticsService, AnalyticsInput, AnalyticsOutput
from .tools.comments import CommentsService, ManageCommentsInput

from .services.auth_manager import PreemptiveAuthManager
from .services.circuit_breaker import circuit_registry, BREAKER_CONFIGS
from .services.cache_manager import CacheManager
from .services.rate_limiter import RateLimiter
from .services.entity_clusterer import EntityClusterer
from .services.publish_scheduler import PublishScheduler, ContentType, AudienceRegion

from .utils.logger import setup_logger

# 加载环境变量
load_dotenv()

# 初始化日志
logger = setup_logger()

# 创建 MCP 服务器
mcp = FastMCP("yt-factory-gateway")

# 初始化服务
auth_manager = PreemptiveAuthManager()
cache_manager = CacheManager()
rate_limiter = RateLimiter()
entity_clusterer = Eerer()
publish_scheduler = PublishScheduler()

trends_service = TrendsService(cache_manager, rate_limiter, entity_clusterer)
search_service = SearchService(auth_manager)
youtube_publisher = YouTubePublisher(auth_manager, rate_limiter, publish_scheduler)
analytics_service = AnalyticsService(auth_manager)
comments_service = CommentsService(auth_manager)

# 初始化熔断器
youtube_breaker = circuit_registry.get_or_create('youtube_upload', BREAKER_CONFIGS['youtube_upload'])
trends_breaker = circuit_registry.e('google_trends', BREAKER_CONFIGS['google_trends'])


# ============================================
# MCP Tool 注册 (含熔断保护)
# ============================================

@mcp.tool()
async def get_trending_topics(
    category: str,
    geo: str = "US",
    timeframe: str = "now 7-d",
    max_results: int = 10,
    include_related: bool = True,
    include_clusters: bool = True  # NEW: 包含聚类建议
) -> dict:
    """
    获取实时热词并进行智能分级
    
    NEW 功能：
   相关热词，建议合并主题
    - 熔断保护：API 故障时返回降级状态
    
    分级类型：
    - established: 稳定趋势，适合深度内容
    - emerging: 新兴趋势，适合快速跟进
    - fleeting: 短暂热点，风险较高
    - evergreen: 常青话题，长期价值
    """
    async def _fetch():
        input_data = TrendingTopicsInput(
            category=category,
            geo=geo,
            timeframe=timeframe,
            max_results=max_results,
            ted=include_related
        )
        return await trends_service.get_trending_topics(input_data, include_clusters)
    
    result, status = await trends_breaker.call(_fetch)
    
    if status == "downgraded":
        return {
            'status': 'downgraded',
            'message': 'Trends API temporarily unavailable. Using cached data or retry later.',
            'topics': [],
            'clusters': []
        }
    
    return result


@mcp.tool()
async def publish_video(
    video_path: str,
    title: str,
    description: str,
    tags: list,
    privacy: str = "private",
    is_short: bool = False,
    thumbnail_path: str = None,
    auto_comment: str = None,
    channel_id: str = None,
    use_optimal_time: bool = True,  # NEW: 使用最佳发布时间
    target_audience: str = "GLOBAL"  # NEW: 目标受众
) -> dict:
    """
    上传视频到 YouTube
    
    NEW 功能：
    - 智能发布窗口：自动计算最佳发布时间
    - Pre-emptive Auth: 防止长上传中的 token 过期
   时降级
    
    支持：
    - 主视频和 Shorts
    - 自动添加 #Shorts 标签
    - 缩略图设置
    - 自动发布置顶评论
    """
    async def _upload():
        # 计算最佳发布时间
        publish_time = None
        if use_optimal_time and privacy != "private":
            content_type = ContentType.SHORTS if is_short else ContentType.MAIN_VIDEO
            audience = AudienceRegion(target_audience)
            
            window = await publish_scheduler.get_optimal_publish_t           channel_id=channel_id,
                content_type=content_type,
                target_audience=audience
            )
            publish_time = window.optimal_time
            
            logger.info("Optimal publish time calculated",
                       time=publish_time.isoformat(),
                       confidence=window.confidence,
                       rationale=window.rationale)
        
        # 确保 token 在整个上传过程中有效
        estimated_upload_minutes = os.paze(video_path) / (5 * 1024 * 1024)  # 假设 5MB/s
        await auth_manager.ensure_valid_for_upload(
            service='youtube',
            channel_id=channel_id,
            estimated_upload_minutes=int(estimated_upload_minutes) + 10
        )
        
        from .tools.youtube import ShortsConfig
        shorts_config = ShortsConfig(is_short=True) if is_short else None
        
        input_data = PublishVideoInput(
            video_path=video_path,
            title=title,
            descriptiescription,
            tags=tags,
            privacy=privacy,
            shorts_config=shorts_config,
            thumbnail_path=thumbnail_path,
            auto_comment=auto_comment,
            channel_id=channel_id,
            scheduled_publish_time=publish_time
        )
        
        return await youtube_publisher.publish_video(input_data)
    
    result, status = await youtube_breaker.call(_upload)
    
    if status == "downgraded":
        return {
            'success': False,
            'status': 'downgraded',
            'message': 'YouTube API temporarily unavailable. Please retry later.',
            'error': 'Circuit breaker open - too many recent failures'
        }
    
    return result


@mcp.tool()
async def get_system_status() -> dict:
    """
    获取 MCP Gateway 系统状态
    
    返回：
    - 所有熔断器状态
    - Token 状态
    - 缓存状态
    - API 配额剩余
    """
    return {
        'circuit_breakers': circuit_registry.get_all_status(),
        'toke {
            'youtube': auth_manager.get_token_status('youtube'),
            'youtube_analytics': auth_manager.get_token_status('youtube_analytics')
        },
        'rate_limits': {
            'trends': rate_limiter.get_remaining('trends'),
            'youtube_upload': rate_limiter.get_remaining('youtube_upload'),
            'search': rate_limiter.get_remaining('search')
        }
    }


@mcp.tool()
async def get_optimal_publish_time(
    content_type: str = "main_video",
    target_audience: str = "GLOBAL",
    channel_id: str = None
) -> dict:
    """
    获取最佳发布时间建议
    
    Args:
        content_type: main_video 或 shorts
        target_audience: US, UK, EU, ASIA, GLOBAL
        channel_id: 可选，用于个性化分析
    """
    ct = ContentType(content_type)
    audience = AudienceRegion(target_audience)
    
    window = await publish_scheduler.get_optimal_publish_time(
        channel_id=channel_id,
        content_type=ct,
        target_audience=audience
    )
    
 {
        'optimal_time': window.optimal_time.isoformat(),
        'window_start': window.window_start.isoformat(),
        'window_end': window.window_end.isoformat(),
        'confidence': window.confidence,
        'rationale': window.rationale,
        'alternatives': [t.isoformat() for t in (window.alternative_times or [])]
    }


# 其他 Tools 保持不变...
@mcp.tool()
async def search_facts(
    query: str,
    purpose: str = "fact_check",
    num_results: int = 10,
    include_snippets: bool = Tlude_entities: bool = True
) -> SearchFactsOutput:
    """搜索验证事实并获取相关实体数据"""
    input_data = SearchFactsInput(
        query=query,
        purpose=purpose,
        num_results=num_results,
        include_snippets=include_snippets,
        include_entities=include_entities
    )
    return await search_service.search_facts(input_data)


@mcp.tool()
async def get_analytics(
    video_ids: list,
    metrics: list = None,
    include_demographics: bool = False,
    include_traffol = False
) -> AnalyticsOutput:
    """获取视频表现数据"""
    input_data = AnalyticsInput(
        video_ids=video_ids,
        metrics=metrics or ["views", "likes", "comments", "watchTime"],
        include_demographics=include_demographics,
        include_traffic_sources=include_traffic_sources
    )
    return await analytics_service.get_analytics(input_data)


@mcp.tool()
async def manage_comments(
    action: str,
    video_id: str,
    comment_text: str = None,
    comment_id: str = None,
    reply_to_comment_id: str = None
) -> dict:
    """管理视频评论"""
    input_data = ManageCommentsInput(
        action=action,
        video_id=video_id,
        comment_text=comment_text,
        comment_id=comment_id,
        reply_to_comment_id=reply_to_comment_id
    )
    return await comments_service.manage_comments(input_data)


# ============================================
# 启动服务器
# ============================================

if __name__ == "__main__":
    mcp.run()
```

---


# ✅ Definition of Done (ULTIMATE)

### MCP Protocol
- [ ] 所有 7 个 Tools 正常响应
- [ ] 熔断时返回 `status: downgraded`
- [ ] `get_system_status` 返回完整系统状态

### Trends Service (Base + Gemini)
- [ ] `get_trending_topics` 返回 `classification` 字段
- [ ] 热词分级算法正确区分 established/emerging/fleeting/evergreen
- [ ] **实体聚类**：识别相关热词并建议合并
- [ ] 缓存命中率 > 80%
- [ ] **熔断保护**：连续失败时返回降级状态

### YouTube Publishing (Base + Gemini)
- [ ] 成功上传测试视频到 YouTube 私有
- [ ] Shorts 视频自动添加 `#Shorts` 标签
- [ ] 断点续传正常工作
- [ ] **智能发布窗口**：返回最佳发布时间 + 置信度
- [ ] **Pre-emptive Auth**：长上传前确保 token 有效期充足
- [ ] **熔断保护**：连续失败时返回降级状态

### OAuth2 (Base + Gemini)
- [ ] 授权流程支持多账户
- [ ] Refresh Token 自动续期
- [ ] **Pre-emptive Refresh**：在过期前 10 分钟自å 安全存储，不在日志中出现

### Circuit Breaker (Gemini NEW)
- [ ] 连续 5 次失败触发熔断
- [ ] 熔断后 5 分钟自动尝试恢复
- [ ] 半开状态成功 2 次后完全恢复
- [ ] 状态变化记录在日志中

### Entity Clustering (Gemini NEW)
- [ ] 识别相关热词（相似度 > 0.6）
- [ ] 生成合并标题建议
- [ ] 计算合并后的权威度提升

### Publish Scheduler (Gemini NEW)
- [ ] 返回最佳发布时间 + 置信度
- [ ] 提供 3 个备选时间
- [ ] 针对 Shorts 和主视频分别优化
- [ ] 支持多时区受众

### Analytics
- [ ] 能够获取视频基础指标
- [ ] A/B 测试分析功能正常
- [ ] 人口统计和流量来源可选获取

### Infrastructure
- [ ] 日志包含每次 Tool 调用的耗时和 API 消耗
- [ ] 速率限制正确防止 API 超限
- [ ] Docker 镜像构建成功

---

## 🔗 Integration with Orchestrator (完整闭环)

**通信协议：**
```
orchestrator                              mcp-gateway
     │                           │
     │  1. get_trending_topics(technology, US) │
     │ ──────────────────────────────────────> │
     │                                         │ → Google Trends API
     │  2. TrendingTopicsOutput                │ ← 缓存检查
     │     + clusters (实体聚类建议)            │ ← 熔断保护
     │ <────────────────────────────â │                                         │
     │  3. search_facts(query, fact_check)     │
     │ ──────────────────────────────────────> │
     │                                         │ → Google Search API
     │  4. SearchFactsOutput                   │ → Knowledge Graph API
     │ <────────────────────────────────────── │  │                                         │
     │  [生成 manifest.json]                   │
     │  [video-renderer 渲染]                  │
     │                                         │
     │  5. get_optimal_publish_time()          │ (NEW)
     │ ──────────────────────────────────────> │
     │  6. PublishWindow (最佳时间 + 置信度)   │
     │ <─────────────â──────────── │
     │                                         │
     │  7. publish_video(path, manifest)       │
     │ ──────────────────────────────────────> │
     │                                         │ → Pre-emptive Auth
     │                                         │ → YouTube Data API
     │  8. PublishVideoOutput                  │ → 断点续传
     │     (video_id, scheduled_time)          │ → 熔断保护
     │ <────────────────────────────────────── │
     │                                         │
     │  [等待 24-48 小时]                       │
     │                                         │
     │  9. get_analytics([video_id])           │
     │ ──────────────────────────────────   │                                         │ → YouTube Analytics API
     │  10. AnalyticsOutput                    │
     │      (含 A/B 分析, 人口统计)             │
     │ <────────────────────────────────────── │
     │                                         │
     │  11. get_system_status()                │ (NEW)
     │ ───────────────────────â────────> │
     │  12. 熔断器状态 + Token状态 + 配额      │
     │ <────────────────────────────────────── │
```

---

## 🎯 最终检查清单 (ULTIMATE)

### 系统韧性 (Gemini NEW)
- [ ] 熔断器配置合理？(YouTube: 3次, Trends: 5次)
- [ ] 降级消息对 orchestrator 清晰？
- [ ] 恢复机制自动工作？

### 认证安全 (Gemini NEW)
- [ ] Pre-emptive refresh 提前 10 分 [ ] 长上传前验证 token 有效期？
- [ ] 多账户凭据隔离？

### 智能调度 (Gemini NEW)
- [ ] 最佳发布时间考虑时区？
- [ ] Shorts 和主视频分开优化？
- [ ] 置信度反映数据质量？

### 实体聚类 (Gemini NEW)
- [ ] 聚类阈值 0.6 合理？
- [ ] 建议标题可直接使用？
- [ ] 权威度计算正确？

### 热词服务 (Base)
- [ ] 分级算法权重配置正确？
- [ ] 缓存 TTL 为 1 小时？
- [ ] 权威度评分因子都已实现？

### YouTube 发e)
- [ ] #Shorts 在描述第一行？
- [ ] 断点续传最大重试 10 次？
- [ ] 自动评论功能正常？

### 安全性 (Base)
- [ ] API Key 和 Token 不在日志中？
- [ ] OAuth 凭据加密存储？
- [ ] 速率限制防止超限？

### 性能 (Base)
- [ ] 缓存命中时响应 < 100ms？
- [ ] API 调用有超时设置？
- [ ] 并发请求正确处理？

---

## 📊 文件完整性验证

本文件包含：

**Base 内容 (from final):**
- ✅ 完整的 5 个 MCP Tools 定义和实现
- ândClassifier 热词分级算法
- ✅ YouTubePublisher 断点续传
- ✅ AnalyticsService A/B 测试
- ✅ CommentsService 评论管理
- ✅ AuthManager OAuth2 多账户
- ✅ CacheManager 缓存策略
- ✅ RateLimiter 配额管理
- ✅ FastMCP Server 入口
- ✅ Docker 配置
- ✅ pyproject.toml

**Gemini 优化 (NEW):**
- ✅ CircuitBreaker 熔断机制
- ✅ PreemptiveAuthManager 预刷新
- ✅ EntityClusterer 实体聚类
- ✅ PublishScheduler 智能发布窗口
- ✅ get_system_status Tool
- ✅ get_optimal_publish_time Tool
- ✅ 更新后的 server.py (含熔断保护)

---

# 🆕 Gemini Final Review Optimizations

## 🆕 Task 5: Enhanced System Status with Cooldown Estimation

**Purpose:** 告诉 orchestrator 大约多久后可以尝试恢复

```python
# 更新 server.py 中的 get_system_status

@mcp.tool()
async def get_system_status() -> dict:
    """
    获取 MCP Gateway 系统状态（增强版）
    
    返回：
    - 所有熔断器状态 + 冷却时间预估
    - Token 状æ°建议
    - 缓存状态
    - API 配额剩余 + 恢复时间
    """
    from datetime import datetime, timedelta
    
    # 获取熔断器状态（含冷却时间）
    circuit_status = {}
    for name, breaker in circuit_registry._breakers.items():
        status = breaker.get_status()
        
        # 增加冷却时间预估
        if status['state'] == 'open':
            config = BREAKER_CONFIGS.get(name, CircuitBreakerConfig())
            if breaker._state.last_failure_time:
              = (datetime.utcnow() - breaker._state.last_failure_time).total_seconds()
                remaining = max(0, config.recovery_timeout - elapsed)
                status['cooldown_seconds'] = int(remaining)
                status['estimated_recovery_time'] = (
                    datetime.utcnow() + timedelta(seconds=remaining)
                ).isoformat()
                status['recommendation'] = (
                    f"Wait {int(remaining/60)} minutes before retry. "
                    f"Consider reducing request frequency."
                )
            else:
                status['cooldown_seconds'] = config.recovery_timeout
        else:
            status['cooldown_seconds'] = 0
            status['recommendation'] = "Service available"
        
        circuit_status[name] = status
    
    # 获取 Token 状态（含预刷新建议）
    token_status = {}
    for service in ['youtube', 'youtube_analytics']:
        ts = auth_manager.get_token_status(service)
        
        # 增加预刷新建议
  if ts.get('minutes_remaining'):
            if ts['minutes_remaining'] < 30:
                ts['recommendation'] = "Token expiring soon. Will auto-refresh before next call."
            elif ts['minutes_remaining'] < 60:
                ts['recommendation'] = "Token healthy but monitor for long operations."
            else:
                ts['recommendation'] = "Token healthy."
        
        token_status[service] = ts
    
    # 获取配额状态（含恢复时间）
    quota_status = {}
    for aends', 'youtube_upload', 'search']:
        remaining = rate_limiter.get_remaining(api)
        limit = rate_limiter.limits.get(api)
        
        quota_info = {
            'remaining': remaining,
            'limit_per_day': limit.requests_per_day if limit else 'unknown'
        }
        
        if remaining <= 0 and limit:
            # 计算配额恢复时间
            reset_time = limit.last_day_reset + timedelta(days=1)
            quota_info['resets_at'] = reset_time.isoformat()
            quota_info['recommendation'] = f"Daily quota exhausted. Resets at {reset_time.strftime('%H:%M UTC')}"
        elif remaining < 10:
            quota_info['recommendation'] = "Quota running low. Consider reducing request frequency."
        else:
            quota_info['recommendation'] = "Quota healthy."
        
        quota_status[api] = quota_info
    
    # 整体健康评估
    overall_health = "healthy"
    issues = []
    
    for name, status in circuit_status.items():
        if status['state'] ==         overall_health = "degraded"
            issues.append(f"{name} circuit is open")
    
    for api, quota in quota_status.items():
        if quota['remaining'] <= 0:
            overall_health = "degraded"
            issues.append(f"{api} quota exhausted")
    
    return {
        'overall_health': overall_health,
        'issues': issues,
        'circuit_breakers': circuit_status,
        'tokens': token_status,
        'rate_limits': quota_status,
        'timestamp': datetime.utcnow().isoformat()
    }
```

---

## 🆕 Task 6: Competitor-Aware Publish Scheduling

**Purpose:** 感知竞争对手发布热度，避开流量高峰竞争

```python
# src/services/publish_scheduler.py (增强版)

from typing import Optional, List, Dict
from datetime import datetime, timedelta
from dataclasses import dataclass

from ..utils.logger import logger


@dataclass
class CompetitorActivity:
    """竞争对手活动"""
    channel_name: str
    video_title: str
    published_at: datetime
    estimated_views

@dataclass
class EnhancedPublishWindow:
    """增强版发布窗口"""
    optimal_time: datetime
    window_start: datetime
    window_end: datetime
    confidence: float
    rationale: str
    alternative_times: List[datetime]
    
    # 竞争分析 (NEW)
    competitor_risk: str  # 'low', 'medium', 'high'
    competitor_details: Optional[List[CompetitorActivity]]
    avoidance_applied: bool


class EnhancedPublishScheduler:
    """
    增强版发布调度器
    
    新增功能：
    - 竞争对    - 流量高峰避让
    - 最佳窗口重新计算
    """
    
    # 竞争避让配置
    COMPETITOR_AVOIDANCE_HOURS = 2  # 避开竞争对手发布后 2 小时
    HIGH_COMPETITION_THRESHOLD = 3  # 2 小时内超过 3 个竞品视频 = 高竞争
    
    def __init__(self, analytics_service=None, search_service=None):
        self.analytics = analytics_service
        self.search = search_service  # 用于检测竞争对手
        self._competitor_cache: Dict[str, List[CompetitorActivity]] = {}
  sync def get_optimal_publish_time_with_competition(
        self,
        channel_id: Optional[str] = None,
        content_type: str = "main_video",
        target_audience: str = "GLOBAL",
        topic_keywords: Optional[List[str]] = None,
        earliest_publish: Optional[datetime] = None
    ) -> EnhancedPublishWindow:
        """
        计算最佳发布时间（考虑竞争对手）
        
        Args:
            topic_keywords: 主题关键词，用于检测同领域竞争对手
        """
      now = datetime.utcnow()
        earliest = earliest_publish or now
        
        # Step 1: 获取基础最佳时间
        base_window = await self._get_base_optimal_time(
            channel_id, content_type, target_audience, earliest
        )
        
        # Step 2: 检测竞争对手活动
        competitor_activities = []
        competitor_risk = "low"
        avoidance_applied = False
        
        if topic_keywords:
            competitor_activities = await self._detect_competitor_activity(
                topic_keywords,
                time_window_hours=24
            )
            
            # 评估竞争风险
            competitor_risk = self._assess_competition_risk(
                competitor_activities,
                base_window.optimal_time
            )
            
            # 如果竞争激烈，调整发布时间
            if competitor_risk in ['medium', 'high']:
                adjusted_time = self._avoid_competition(
                    base_window.optimal_ti                  competitor_activities
                )
                
                if adjusted_time != base_window.optimal_time:
                    avoidance_applied = True
                    base_window.optimal_time = adjusted_time
                    base_window.rationale += f" | Adjusted to avoid {competitor_risk} competition."
        
        return EnhancedPublishWindow(
            optimal_time=base_window.optimal_time,
            window_start=base_window.optimal_time - timedelta(hours=1),
            window_end=base_window.optimal_time + timedelta(hours=2),
            confidence=base_window.confidence * (0.9 if avoidance_applied else 1.0),
            rationale=base_window.rationale,
            alternative_times=base_window.alternative_times,
            competitor_risk=competitor_risk,
            competitor_details=competitor_activities[:5] if competitor_activities else None,
            avoidance_applied=avoidance_applied
        )
    
    async def _detect_competitor_activity(
        self,
        keywords: List[str],
        time_window_hours: int = 24
    ) -> List[CompetitorActivity]:
        """检测竞争对手最近的发布活动"""
        
        cache_key = f"{','.join(keywords)}:{time_window_hours}"
        if cache_key in self._competitor_cache:
            return self._competitor_cache[cache_key]
        
        activities = []
        
        if self.search:
            try:
                # 搜索最近发布的相关视频
                for keyword in keywords[:3]:  # 限制搜索次数
                    search_results = await self.search.search_recent_videos(
                        query=keyword,
                        published_after=datetime.utcnow() - timedelta(hours=time_window_hours),
                        max_results=10
                    )
                    
                    for result in search_results:
                        activities.append(CompetitorActivity(
                            channel_name=result.get('channel', 'Unknown'),
                video_title=result.get('title', ''),
                            published_at=result.get('published_at', datetime.utcnow()),
                            estimated_views_24h=result.get('view_count', 0)
                        ))
                
                # 去重并按时间排序
                seen = set()
                unique_activities = []
                for act in activities:
                    key = f"{act.channel_name}:{act.video_title[:30]}"
                    if key not in seen:
                        seen.add(key)
                        unique_activities.append(act)
                
                activities = sorted(unique_activities, key=lambda x: x.published_at, reverse=True)
                
            except Exception as e:
                logger.warning("Failed to detect competitor activity", error=str(e))
        
        self._competitor_cache[cache_key] = activities
        return activities
    
    def _assess_competition_risk(
        self,
        activities: List[CompetitorActivity],
        target_time: datetime
    ) -> str:
        """评估竞争风险"""
        
        if not activities:
            return "low"
        
        # 统计目标时间前后 2 小时内的竞品数量
        window_start = target_time - timedelta(hours=2)
        window_end = target_time + timedelta(hours=2)
        
        nearby_competitors = [
            act for act in activities
            if window_start <= act.published_at <= window_end
        ]
        
              high_traffic = [
            act for act in nearby_competitors
            if act.estimated_views_24h > 10000
        ]
        
        if len(high_traffic) >= 2 or len(nearby_competitors) >= self.HIGH_COMPETITION_THRESHOLD:
            return "high"
        elif len(nearby_competitors) >= 2:
            return "medium"
        else:
            return "low"
    
    def _avoid_competition(
        self,
        original_time: datetime,
        activities: List[CompetitorActivity]
    ) -> datetime:
        """调整时间以避开竞争"""
        
        # 获取竞品发布时间
        competitor_times = [act.published_at for act in activities]
        
        # 检查原时间是否在竞争窗口内
        for ct in competitor_times:
            if abs((original_time - ct).total_seconds()) < self.COMPETITOR_AVOIDANCE_HOURS * 3600:
                # 延迟 2 小时
                adjusted = original_time + timedelta(hours=self.COMPETITOR_AVOIDANCE_HOURS)
                
                # é´
                still_conflicting = any(
                    abs((adjusted - ct).total_seconds()) < self.COMPETITOR_AVOIDANCE_HOURS * 3600
                    for ct in competitor_times
                )
                
                if still_conflicting:
                    # 继续延迟
                    adjusted = adjusted + timedelta(hours=1)
                
                logger.info("Publish time adjusted to avoid competition",
                           original=original_time.isoformat(),                  adjusted=adjusted.isoformat())
                
                return adjusted
        
        return original_time
    
    async def _get_base_optimal_time(
        self,
        channel_id: Optional[str],
        content_type: str,
        target_audience: str,
        earliest: datetime
    ):
        """获取基础最佳时间（复用原有逻辑）"""
        # 这里调用原有的 PublishScheduler 逻辑
        from . import PublishScheduler, ContentType, AudienceRegion
      
        base_scheduler = PublishScheduler(self.analytics)
        return await base_scheduler.get_optimal_publish_time(
            channel_id=channel_id,
            content_type=ContentType(content_type),
            target_audience=AudienceRegion(target_audience),
            earliest_publish=earliest
        )
```

---

## 🆕 Task 7: Content Safety Filter (内容安全过滤)

**Purpose:** 确保自动化内容不会被 YouTube 黄标或删除

```python
# src/services/content_safety.py

import re
frport List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..utils.logger import logger


class SafetyLevel(str, Enum):
    SAFE = "safe"
    CAUTION = "caution"      # 可能触发黄标
    RESTRICTED = "restricted" # 可能被限流
    BLOCKED = "blocked"       # 会被删除


@dataclass
class SafetyCheckResult:
    """安全检查结果"""
    level: SafetyLevel
    issues: List[str]
    suggestions: List[str]
    flagged_terms: List[str]
    safe_alternatives: Dict  # 违规词 -> 安全替代


class ContentSafetyFilter:
    """
    内容安全过滤器
    
    功能：
    1. 检测可能触发黄标的词汇
    2. 检测可能被删除的内容
    3. 提供安全替代建议
    4. 支持多语言 (EN, ZH)
    
    2026 YouTube 政策参考：
    - 敏感话题（政治、健康、金融）
    - 版权相关词汇
    - 暴力/成人内容暗示
    - 误导性声明
    """
    
    # ============================================
    # 违规词库 (2026 æ==========================================
    
    # 黄标风险词 (CAUTION)
    CAUTION_TERMS = {
        'en': [
            # 健康/医疗
            'cure', 'treatment', 'miracle', 'medical advice',
            'weight loss', 'diet pill', 'supplement',
            # 金融
            'guaranteed returns', 'get rich quick', 'financial advice',
            'investment opportunity', 'crypto gains',
            # 政治敏感
            'election fraud', 'conspiracy', 'cover-up',
            # 争è            'shocking truth', 'they don\'t want you to know',
            'banned', 'censored',
        ],
        'zh': [
            # 健康/医疗
            '治愈', '神药', '特效药', '医疗建议',
            '减肥药', '保健品',
            # 金融
            '稳赚不赔', '财务自由', '投资建议',
            '暴富', '理财秘诀',
            # 政治敏感
            '阴谋', '真相', '内幕',
            # 争议性
            '震惊', '他们不想让你知道', '被禁',
        ]
    }
    
    # 限流风险词 (RESTRICTED)
    RESTRICTED_TERMS = {
        'en': [
            # 暴力相关
            'violence', 'graphic', 'brutal', 'attack',
            'weapon', 'gun', 'shooting',
            # 成人暗示
            'adult', 'explicit', 'nsfw', 'xxx',
            # 危险行为
            'dangerous', 'do not try', 'challenge gone wrong',
            # 仇恨相关
            'hate', 'racist', 'discrimination',
        ],
        'zh': [
            #    '暴力', '血腥', '残忍', '攻击',
            '武器', '枪', '枪击',
            # 危险行为
            '危险', '请勿模仿', '挑战失败',
            # 仇恨相关
            '仇恨', '歧视',
        ]
    }
    
    # 删除风险词 (BLOCKED)
    BLOCKED_TERMS = {
        'en': [
            # 版权
            'full movie', 'free download', 'pirated',
            'watch free', 'stream free',
            # 严重违规
            'terrorism', 'how to make bomb',
           inor', 'underage',  # 在不当上下文中
            # 欺诈
            'free money', 'hack', 'cheat', 'exploit',
        ],
        'zh': [
            # 版权
            '完整电影', '免费下载', '盗版',
            '免费观看', '在线播放',
            # 欺诈
            '免费领取', '破解', '作弊', '漏洞',
        ]
    }
    
    # 安全替代词
    SAFE_ALTERNATIVES = {
        'en': {
            'cure': 'may help with',
            'guaranteed': 'potential',
       ng': 'surprising',
            'secret': 'lesser-known',
            'hack': 'tip',
            'free': 'no-cost',
            'miracle': 'effective',
            'banned': 'controversial',
        },
        'zh': {
            '治愈': '可能有帮助',
            '稳赚': '潜在收益',
            '震惊': '令人惊讶',
            '秘密': '鲜为人知',
            '破解': '技巧',
            '免费': '无需付费',
            '神药': '有效方法',
            '被禁': '有争议
    }
    
    # ============================================
    # 检测方法
    # ============================================
    
    def __init__(self):
        self._compile_patterns()
    
    def _compile_patterns(self):
        """编译正则表达式"""
        self._patterns = {
            'caution': {},
            'restricted': {},
            'blocked': {}
        }
        
        for lang in ['en', 'zh']:
            self._patterns['caution'][lang] = [
                re.compile(rf'\bcape(term)}\b', re.IGNORECASE)
                for term in self.CAUTION_TERMS.get(lang, [])
            ]
            self._patterns['restricted'][lang] = [
                re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
                for term in self.RESTRICTED_TERMS.get(lang, [])
            ]
            self._patterns['blocked'][lang] = [
                re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
                for term in self.BLOCKED_TERMS.get(lang, [])
            ]
    
    def check_content(
        self,
        title: str,
        description: str,
        tags: List[str],
        language: str = 'en'
    ) -> SafetyCheckResult:
        """
        检查内容安全性
        
        Args:
            title: 视频标题
            description: 视频描述
            tags: 标签列表
            language: 内容语言 ('en' 或 'zh')
        
        Returns:
            SafetyCheckResult
        """
        # 合并所有文本
        full_text = f"{title} {description} gs)}"
        
        issues = []
        flagged_terms = []
        safe_alternatives = {}
        
        lang = language if language in ['en', 'zh'] else 'en'
        
        # 检查 BLOCKED 级别
        for pattern in self._patterns['blocked'].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
                issues.append(f"BLOCKED term detected: {matches}")
        
        if flagged_terms:
            return SafResult(
                level=SafetyLevel.BLOCKED,
                issues=issues,
                suggestions=["Remove or completely rephrase flagged content"],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives={}
            )
        
        # 检查 RESTRICTED 级别
        for pattern in self._patterns['restricted'].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
              .append(f"RESTRICTED term detected: {matches}")
        
        if flagged_terms:
            return SafetyCheckResult(
                level=SafetyLevel.RESTRICTED,
                issues=issues,
                suggestions=[
                    "Content may be age-restricted or demonetized",
                    "Consider rephrasing or adding context"
                ],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives=self._get_alternatives(flagged_terms, lang)
            )
        
        # 检查 CAUTION 级别
        for pattern in self._patterns['caution'].get(lang, []):
            matches = pattern.findall(full_text)
            if matches:
                flagged_terms.extend(matches)
                issues.append(f"CAUTION term detected: {matches}")
        
        if flagged_terms:
            return SafetyCheckResult(
                level=SafetyLevel.CAUTION,
                issues=issues,
                suggestions=[
                    "Content may limited ads (yellow dollar sign)",
                    "Consider using safer alternatives"
                ],
                flagged_terms=list(set(flagged_terms)),
                safe_alternatives=self._get_alternatives(flagged_terms, lang)
            )
        
        # 安全
        return SafetyCheckResult(
            level=SafetyLevel.SAFE,
            issues=[],
            suggestions=["Content appears safe for monetization"],
            flagged_terms=[],
            safe_alternatives={}
     
    
    def _get_alternatives(self, terms: List[str], lang: str) -> Dict[str, str]:
        """获取安全替代词"""
        alternatives = {}
        alt_dict = self.SAFE_ALTERNATIVES.get(lang, {})
        
        for term in terms:
            term_lower = term.lower()
            if term_lower in alt_dict:
                alternatives[term] = alt_dict[term_lower]
        
        return alternatives
    
    def sanitize_content(
        self,
        text: str,
        language: str = 'en'
    ) -ist[str]]:
        """
        自动清理内容
        
        Returns:
            (cleaned_text, list of changes made)
        """
        changes = []
        result = text
        
        alt_dict = self.SAFE_ALTERNATIVES.get(language, {})
        
        for original, replacement in alt_dict.items():
            pattern = re.compile(rf'\b{re.escape(original)}\b', re.IGNORECASE)
            if pattern.search(result):
                result = pattern.sub(replacement, result)
                changesoriginal}' → '{replacement}'")
        
        return result, changes


# 全局实例
content_safety = ContentSafetyFilter()


# ============================================
# MCP Tool 集成
# ============================================

@mcp.tool()
async def check_content_safety(
    title: str,
    description: str,
    tags: list,
    language: str = "en",
    auto_fix: bool = False
) -> dict:
    """
    检查内容安全性（防黄标）
    
    Args:
        title: 视频标题
        descri      tags: 标签列表
        language: 内容语言 (en/zh)
        auto_fix: 是否自动修复
    
    Returns:
        - level: safe/caution/restricted/blocked
        - issues: 问题列表
        - flagged_terms: 违规词列表
        - safe_alternatives: 安全替代建议
        - fixed_content: (如果 auto_fix=True) 修复后的内容
    """
    result = content_safety.check_content(title, description, tags, language)
    
    response = {
        'level': result.level.value,
        'is_ult.level == SafetyLevel.SAFE,
        'issues': result.issues,
        'suggestions': result.suggestions,
        'flagged_terms': result.flagged_terms,
        'safe_alternatives': result.safe_alternatives
    }
    
    if auto_fix and result.level != SafetyLevel.SAFE:
        fixed_title, title_changes = content_safety.sanitize_content(title, language)
        fixed_desc, desc_changes = content_safety.sanitize_content(description, language)
        
        response['fixed_content'] = {
            'title': fixed_title,
            'description': fixed_desc,
            'changes_made': title_changes + desc_changes
        }
        
        # 重新检查修复后的内容
        recheck = content_safety.check_content(fixed_title, fixed_desc, tags, language)
        response['fixed_level'] = recheck.level.value
        response['remaining_issues'] = recheck.issues
    
    return response
```

---

## 📋 Updated MCP Tools Summary (FINAL)

```python
# src/server.py - 完整 Tool 列表

# ==============================
# 7 个核心 MCP Tools (最终版)
# ============================================

@mcp.tool()
async def get_trending_topics(...):
    """热词获取 + 分级 + 实体聚类 + 熔断保护"""

@mcp.tool()
async def search_facts(...):
    """事实核查 + Knowledge Graph 实体"""

@mcp.tool()
async def publish_video(...):
    """视频上传 + Shorts + 智能发布时间 + Pre-emptive Auth + 熔断保护"""

@mcp.tool()
async def get_analytics(...):
    """视频分析 + A/B 测试 + 人ool()
async def manage_comments(...):
    """评论管理 + 自动置顶"""

# ============================================
# 4 个增强 MCP Tools (Gemini 优化)
# ============================================

@mcp.tool()
async def get_system_status():
    """系统状态 + 熔断器冷却时间 + Token状态 + 配额"""

@mcp.tool()
async def get_optimal_publish_time(...):
    """最佳发布时间 + 竞争对手避让"""

@mcp.tool()
async def check_content_safety(...):
    """内容安全检查 + 黄æ

---

## ✅ Definition of Done (ABSOLUTE FINAL)

### MCP Protocol
- [ ] 所有 **8 个 Tools** 正常响应
- [ ] 熔断时返回 `status: downgraded` + **冷却时间预估**
- [ ] `get_system_status` 返回完整系统状态 + 恢复建议

### Trends Service
- [ ] 热词分级算法正确
- [ ] **实体聚类** 识别相关热词
- [ ] 熔断保护正常工作

### YouTube Publishing
- [ ] Shorts 自动添加 `#Shorts`
- [ ] 断点续传正常
- [ ] **智能发布窗口** + **竞争对手避让**
- [ e Auth** 防止长上传中断
- [ ] 熔断保护正常

### Content Safety (NEW)
- [ ] 检测 CAUTION/RESTRICTED/BLOCKED 级别
- [ ] 提供安全替代词
- [ ] `auto_fix` 功能正常
- [ ] 支持英文和中文

### System Monitoring (Enhanced)
- [ ] 熔断器**冷却时间预估**准确
- [ ] Token **预刷新建议**正确
- [ ] 配额**恢复时间**计算正确

---

## 🎯 最终检查清单 (ABSOLUTE FINAL)

### 内容安全 (Gemini FINAL NEW)
- [ ] 黄标风险词库完整？
- [ ] 安全替代å_fix 不破坏原意？
- [ ] 支持中英文？

### 竞争避让 (Gemini FINAL NEW)
- [ ] 竞争对手检测准确？
- [ ] 2 小时避让窗口合理？
- [ ] 高竞争阈值 (3个视频) 合理？

### 系统监控 (Gemini FINAL NEW)
- [ ] 冷却时间预估准确？
- [ ] 恢复建议对 orchestrator 有用？
- [ ] 整体健康评估正确？

---

## 📊 完整文件清单验证

本 ULTIMATE COMPLETE FINAL 版本包含：

**Base 内容 (from original final):**
- ✅ 5 个核心 MCP Tools 完整å TrendClassifier 热词分级算法
- ✅ YouTubePublisher 断点续传
- ✅ AnalyticsService A/B 测试
- ✅ CommentsService 评论管理
- ✅ AuthManager OAuth2 多账户
- ✅ CacheManager 缓存策略
- ✅ RateLimiter 配额管理
- ✅ FastMCP Server 入口
- ✅ Docker 配置
- ✅ pyproject.toml

**Gemini 第一轮优化:**
- ✅ CircuitBreaker 熔断机制
- ✅ PreemptiveAuthManager 预刷新
- ✅ EntityClusterer 实体聚类
- ✅ PublishScheduler 智能发布窗口
- ✅ get_system_status✅ get_optimal_publish_time Tool

**Gemini FINAL 优化:**
- ✅ Enhanced get_system_status (冷却时间预估)
- ✅ EnhancedPublishScheduler (竞争对手避让)
- ✅ ContentSafetyFilter (内容安全过滤)
- ✅ check_content_safety Tool

**总计: 8 个 MCP Tools + 完整基础设施**

---

## 📝 Implementation Status (2026-01-29)

### ✅ Implemented Services

All services from the specification have been implemented and are production-ready:

| Service | File | Status | MCP Tools |
|---------|------|--------|-----------|
| Content Safety Filter | `src/services/content_safety.py` | ✅ Complete | `check_content_safety` |
| Ad-Friendly Keywords | `src/services/ad_keywords.py` | ✅ Complete | `get_ad_friendly_suggestions` |
| AI Compliance | `src/services/compliance.py` | ✅ Complete | `check_compliance` |
| Regional Safety | `src/services/regional_safety.py` | ✅ Complete | `check_regional_safety` |
| Ad Suitability Scorer | `src/services/ad_scorer.py` | ✅ Complete | `get_ad_suitability_score` |
| Affiliate Manager | `src/services/affiliate_manager.py` | ✅ Complete | `extract_affiliate_links` |
| AIO Tracker | `src/services/aio_tracker.py` | ✅ Complete | `check_aio_status`, `get_aio_optimization_feedback` |

### 📊 MCP Tools Summary (15 Total)

**Core Tools (5):**
- `get_trending_topics` - Trend fetching with classification
- `search_facts` - Fact-checking with Knowledge Graph
- `publish_video` - Video upload with safe publish flow
- `get_analytics` - YouTube Analytics with A/B testing
- `manage_comments` - Comment automation

**Safety & Compliance Tools (3):**
- `check_content_safety` - 3-tier filtering (BLOCKED/RESTRICTED/CAUTION)
- `check_regional_safety` - 10-region cultural sensitivity
- `check_compliance` - YouTube 2026 AI disclosure

**Monetization Tools (3):**
- `get_ad_suitability_score` - 0-100 monetization prediction
- `get_ad_friendly_suggestions` - CPM optimization keywords
- `extract_affiliate_links` - Automated affiliate detection

**AIO Tools (2):**
- `check_aio_status` - Google AI Overview attribution
- `get_aio_optimization_feedback` - FAQ optimization guidance

**System Tools (2):**
- `get_system_status` - Circuit breaker & quota status
- `get_optimal_publish_time` - Intelligent publish scheduling

### 📁 External Configuration Files

```
data/
├── safety_wordlists.json        # 3-tier content filtering wordlists
├── ad_friendly_keywords.json    # High-CPM keywords by vertical
├── regional_sensitive_terms.json # Cultural/political sensitivity database
└── affiliate_database.json      # Affiliate link database (16 products)
```

### 🔧 Key Implementation Learnings

1. **structlog compatibility**: Use `logging.INFO` instead of `structlog.INFO` for log level constants
2. **Long strings in Python**: Use per-file-ignores in ruff for files with intentional long disclaimer strings
3. **Service exports**: Ensure `__init__.py` only imports classes that actually exist in modules
4. **Safe publish flow**: The `publish_video` tool now runs 6 mandatory pre-publish checks:
   - Content safety scan
   - Compliance disclosure injection
   - Affiliate comment generation
   - Optimal publish time calculation
   - Pre-emptive auth validation
   - Execute upload with enhanced metadata

### 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Run linting
uv run ruff check src/

# Test imports
uv run python -c "from src.server import mcp; print('Server ready')"

# Run server
uv run python -m src.server
```

### 📈 Metrics

- **Total lines of code added**: 5,299
- **New service files**: 7
- **External config files**: 3
- **MCP tools**: 15 (up from 8)

<claude-mem-context>
# Recent Activity

<!-- This section is auto-generated by claude-mem. Edit content outside the tags. -->

*No recent activity*
</claude-mem-context>