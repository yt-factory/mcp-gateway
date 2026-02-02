# MCP Gateway

Python-based Model Context Protocol (MCP) gateway providing 19 production-ready tools for YouTube automation, Google Trends analysis, content safety, and monetization optimization.

Part of the **yt-factory** ecosystem — serves as the bridge between the orchestrator and external APIs (YouTube, Google Trends, Knowledge Graph).

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        MCP Gateway                                │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   [orchestrator] ─── MCP Protocol ───> [mcp-gateway]             │
│                                              │                    │
│                          ┌───────────────────┼───────────────────┐
│                          │                   │                   │
│                          ▼                   ▼                   ▼
│                   ┌─────────────┐   ┌─────────────┐   ┌─────────┐
│                   │   Google    │   │   YouTube   │   │  Mock   │
│                   │   Trends    │   │  Data API   │   │Provider │
│                   └─────────────┘   └─────────────┘   └─────────┘
│                                                                   │
│   Features:                                                       │
│   • 19 MCP Tools (trends, safety, publishing, analytics)        │
│   • Mock Mode for development without API keys                   │
│   • OAuth2 authentication with token refresh                     │
│   • Circuit breaker pattern for resilience                       │
│   • Rate limiting with async-safe token bucket                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Navigate to the gateway directory
cd mcp-gateway/mcp-gateway

# Install dependencies
uv sync

# Run in mock mode (no API keys required)
MOCK_MODE=true uv run python -m src

# Run with real APIs (requires credentials)
uv run python -m src
```

## Available Tools (19 Total)

### Content Discovery & Trends

| Tool | Description | Example Use |
|------|-------------|-------------|
| `get_trending_topics` | Fetch trending topics with authority scoring | Find viral content ideas |
| `search_facts` | Fact-check content via Knowledge Graph | Verify claims before scripting |

### Publishing & Management

| Tool | Description | Example Use |
|------|-------------|-------------|
| `publish_video` | Upload videos with safe publish flow | Automated YouTube upload |
| `manage_comments` | Comment moderation automation | Filter spam, pin highlights |
| `get_optimal_publish_time` | Smart scheduling recommendations | Maximize initial engagement |

### Content Safety

| Tool | Description | Example Use |
|------|-------------|-------------|
| `check_content_safety` | 3-tier content filtering | Pre-flight safety check |
| `check_regional_safety` | Cultural sensitivity validation | Multi-market content |
| `check_compliance` | YouTube 2026 AI disclosure compliance | Avoid policy strikes |

### Monetization

| Tool | Description | Example Use |
|------|-------------|-------------|
| `get_ad_suitability_score` | Predict monetization eligibility | CPM optimization |
| `get_ad_friendly_suggestions` | Brand-safe keyword alternatives | Improve ad revenue |
| `extract_affiliate_links` | Detect affiliate opportunities | Revenue diversification |
| `get_monetization_dashboard` | Revenue intelligence overview | Track earnings |
| `get_metric_details` | Deep-dive into specific metrics | Analyze performance |

### SEO & AI Overview

| Tool | Description | Example Use |
|------|-------------|-------------|
| `check_aio_status` | Check Google AI Overview attribution | SEO visibility |
| `get_aio_optimization_feedback` | FAQ optimization suggestions | Improve AI citations |

### Analytics & System

| Tool | Description | Example Use |
|------|-------------|-------------|
| `get_analytics` | Fetch video performance data | Track view counts |
| `get_system_status` | Health check & circuit breaker status | Operational monitoring |

## Usage Examples

### Example 1: Get Trending Topics

```python
# Test trending topics in mock mode
cd mcp-gateway/mcp-gateway
MOCK_MODE=true uv run python -c "
import asyncio
from src.server import mcp

async def test():
    result = await mcp._tool_manager._tools['get_trending_topics'].fn(
        category='technology',
        geo='US',
        max_results=5
    )
    print('Trending Topics:')
    for topic in result.get('topics', []):
        print(f\"  • {topic['keyword']} (authority: {topic['authority_score']})\"
    )
    return result

asyncio.run(test())
"
```

**Expected Output:**
```
Trending Topics:
  • AI Code Assistants (authority: 85)
  • Quantum Computing Breakthrough (authority: 72)
  • GPT-5 Release (authority: 91)
  • Rust Programming (authority: 68)
  • WebAssembly Future (authority: 64)
```

### Example 2: Check Content Safety

```python
cd mcp-gateway/mcp-gateway
MOCK_MODE=true uv run python -c "
import asyncio
from src.server import mcp

async def test():
    result = await mcp._tool_manager._tools['check_content_safety'].fn(
        title='10 Python Tips for Beginners',
        description='Learn Python faster with these proven techniques',
        tags=['python', 'programming', 'tutorial'],
        language='en'
    )
    print(f\"Safety Level: {result['level']}\")
    print(f\"Ad-Friendly: {result['ad_friendly']}\")
    print(f\"Concerns: {result.get('concerns', 'None')}\")
    return result

asyncio.run(test())
"
```

**Expected Output:**
```
Safety Level: ad_friendly
Ad-Friendly: True
Concerns: None
```

### Example 3: Get Optimal Publish Time

```python
cd mcp-gateway/mcp-gateway
MOCK_MODE=true uv run python -c "
import asyncio
from src.server import mcp

async def test():
    result = await mcp._tool_manager._tools['get_optimal_publish_time'].fn(
        content_type='main_video',
        target_audience='US'
    )
    print(f\"Recommended Time: {result['recommended_time']}\")
    print(f\"Day: {result['day_of_week']}\")
    print(f\"Timezone: {result['timezone']}\")
    print(f\"Reasoning: {result['reasoning']}\")
    return result

asyncio.run(test())
"
```

**Expected Output:**
```
Recommended Time: 14:00
Day: Tuesday
Timezone: America/Los_Angeles
Reasoning: Peak engagement for tech content in US market
```

### Example 4: Check System Status

```python
cd mcp-gateway/mcp-gateway
MOCK_MODE=true uv run python -c "
import asyncio
import json
from src.server import mcp

async def test():
    result = await mcp._tool_manager._tools['get_system_status'].fn()
    print(json.dumps(result, indent=2, default=str))
    return result

asyncio.run(test())
"
```

**Expected Output:**
```json
{
  "status": "healthy",
  "mock_mode": true,
  "tools_registered": 19,
  "circuit_breakers": {
    "youtube": "closed",
    "trends": "closed"
  },
  "uptime_seconds": 12.5
}
```

### Example 5: Full Content Validation Pipeline

```python
cd mcp-gateway/mcp-gateway
MOCK_MODE=true uv run python -c "
import asyncio
from src.server import mcp

async def full_validation():
    title = 'Why Rust is Taking Over C++'
    description = 'A deep dive into memory safety and performance'
    tags = ['rust', 'programming', 'cpp', 'memory-safety']

    # Step 1: Content Safety
    safety = await mcp._tool_manager._tools['check_content_safety'].fn(
        title=title,
        description=description,
        tags=tags,
        language='en'
    )
    print(f'1. Safety Check: {safety[\"level\"]}')

    # Step 2: Regional Safety
    regional = await mcp._tool_manager._tools['check_regional_safety'].fn(
        title=title,
        description=description,
        target_regions=['US', 'DE', 'JP']
    )
    print(f'2. Regional Safety: {regional[\"status\"]}')

    # Step 3: Compliance Check
    compliance = await mcp._tool_manager._tools['check_compliance'].fn(
        content_type='educational',
        ai_generated=False,
        sponsored=False
    )
    print(f'3. Compliance: {compliance[\"compliant\"]}')

    # Step 4: Ad Suitability
    ad_score = await mcp._tool_manager._tools['get_ad_suitability_score'].fn(
        title=title,
        description=description,
        category='technology'
    )
    print(f'4. Ad Suitability: {ad_score[\"score\"]}/100')

    # Step 5: Optimal Publish Time
    publish_time = await mcp._tool_manager._tools['get_optimal_publish_time'].fn(
        content_type='main_video',
        target_audience='US'
    )
    print(f'5. Best Publish Time: {publish_time[\"recommended_time\"]} {publish_time[\"timezone\"]}')

    print('\\n✅ Content validated and ready for production!')

asyncio.run(full_validation())
"
```

**Expected Output:**
```
1. Safety Check: ad_friendly
2. Regional Safety: approved
3. Compliance: True
4. Ad Suitability: 87/100
5. Best Publish Time: 14:00 America/Los_Angeles

✅ Content validated and ready for production!
```

## Configuration

### Environment Variables

Create `.env` in `mcp-gateway/mcp-gateway/`:

```bash
# ===========================================
# MOCK MODE - Enable for development
# ===========================================
MOCK_MODE=true    # Set to 'false' for production

# ===========================================
# Google API Keys (required for production)
# ===========================================
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CSE_ID=your_custom_search_engine_id_here

# OAuth2 Client Secrets
GOOGLE_CLIENT_SECRETS_FILE=./credentials/client_secrets.json

# ===========================================
# Directories
# ===========================================
CREDENTIALS_DIR=./credentials
CACHE_DIR=./.cache

# ===========================================
# Logging
# ===========================================
LOG_LEVEL=INFO    # DEBUG | INFO | WARNING | ERROR

# ===========================================
# Rate Limiting (optional)
# ===========================================
RATE_LIMIT_RPM=60
```

### Setting Up Real API Credentials

1. **Create Google Cloud Project**
   ```bash
   # Go to https://console.cloud.google.com
   # Create new project: "yt-factory"
   ```

2. **Enable Required APIs**
   - YouTube Data API v3
   - YouTube Analytics API
   - Custom Search API
   - Knowledge Graph Search API

3. **Create OAuth 2.0 Credentials**
   ```bash
   # Download client_secrets.json
   mkdir -p mcp-gateway/mcp-gateway/credentials
   mv ~/Downloads/client_secrets.json mcp-gateway/mcp-gateway/credentials/
   ```

4. **First-time OAuth Flow**
   ```bash
   cd mcp-gateway/mcp-gateway
   MOCK_MODE=false uv run python -c "
   from src.services.auth_manager import PreemptiveAuthManager
   auth = PreemptiveAuthManager()
   creds = auth.get_credentials('youtube')
   print('✅ YouTube credentials obtained successfully')
   "
   # Browser will open for OAuth consent
   ```

## Project Structure

```
mcp-gateway/
└── mcp-gateway/
    ├── src/
    │   ├── __init__.py
    │   ├── __main__.py           # Entry point
    │   ├── server.py             # MCP server with 19 tools
    │   ├── config.py             # Configuration & validation
    │   └── services/
    │       ├── auth_manager.py   # OAuth2 with token refresh
    │       ├── rate_limiter.py   # Async-safe token bucket
    │       ├── mock_provider.py  # Mock responses for dev
    │       ├── youtube_client.py # YouTube API wrapper
    │       └── trends_client.py  # Google Trends wrapper
    ├── credentials/              # OAuth tokens (gitignored)
    ├── .cache/                   # API response cache
    ├── pyproject.toml
    └── .env
```

## Mock Mode

Mock mode provides realistic simulated responses for development without API credentials:

```bash
# Enable mock mode
export MOCK_MODE=true

# Or set in .env
echo "MOCK_MODE=true" >> .env

# Run with mock mode
uv run python -m src
```

**Mock Mode Features:**
- Realistic trending topics with authority scores
- Simulated content safety responses
- Mock video upload with fake video IDs
- Simulated analytics data
- Consistent, reproducible responses

## Integration with Orchestrator

The MCP gateway is designed to be invoked by the orchestrator via MCP protocol:

```typescript
// In orchestrator, the gateway is configured in .env:
MCP_GATEWAY_COMMAND=uv run python -m src
MCP_GATEWAY_CWD=../mcp-gateway/mcp-gateway

// The orchestrator calls tools like:
const trends = await mcpClient.call('get_trending_topics', {
  category: 'technology',
  geo: 'US',
  max_results: 10
});
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.11+ |
| Package Manager | UV |
| MCP Framework | mcp-python |
| HTTP Client | httpx (async) |
| OAuth | google-auth-oauthlib |
| Validation | Pydantic |
| Caching | diskcache |

## Troubleshooting

### Common Issues

**"MOCK_MODE not working"**
```bash
# Set directly in command
MOCK_MODE=true uv run python -m src
```

**"OAuth token expired"**
```bash
# Delete cached tokens
rm -f credentials/token_*.json
# Re-run to trigger OAuth flow
```

**"Rate limit exceeded"**
```bash
# Check circuit breaker status
MOCK_MODE=true uv run python -c "
import asyncio
from src.server import mcp
asyncio.run(mcp._tool_manager._tools['get_system_status'].fn())
"
```

**"Import errors"**
```bash
# Reinstall dependencies
cd mcp-gateway/mcp-gateway
rm -rf .venv uv.lock
uv sync
```

## Recent Updates (Feb 2026)

- **Critical Bug Fixes**: Fixed async blocking issues in auth_manager and rate_limiter
- **Config Validation**: Added `validate_config()` for required credentials
- **Rate Limiting**: Implemented jitter to prevent thundering herd
- **Error Handling**: Improved error messages and logging

---

*Part of the [YT-Factory](../docs/SETUP.md) YouTube automation ecosystem*
