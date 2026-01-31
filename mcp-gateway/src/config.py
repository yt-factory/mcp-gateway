import os
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def _get_required_env(name: str, default: str | None = None) -> str:
    """Get required environment variable or raise error if not set."""
    value = os.getenv(name, default or "")
    if not value:
        logger.warning(f"Required environment variable {name} is not set")
    return value


def _get_optional_env(name: str, default: str) -> str:
    """Get optional environment variable with default."""
    return os.getenv(name, default)


# Required credentials - will log warning if not set
GOOGLE_API_KEY = _get_required_env("GOOGLE_API_KEY")
GOOGLE_CSE_ID = _get_required_env("GOOGLE_CSE_ID")

# Optional paths with sensible defaults
GOOGLE_CLIENT_SECRETS_FILE = _get_optional_env("GOOGLE_CLIENT_SECRETS_FILE", "./credentials/client_secrets.json")
CREDENTIALS_DIR = _get_optional_env("CREDENTIALS_DIR", "./credentials")
CACHE_DIR = _get_optional_env("CACHE_DIR", "./.cache")
LOG_LEVEL = _get_optional_env("LOG_LEVEL", "INFO")


def validate_config() -> list[str]:
    """Validate configuration and return list of missing required variables."""
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not GOOGLE_CSE_ID:
        missing.append("GOOGLE_CSE_ID")
    return missing
