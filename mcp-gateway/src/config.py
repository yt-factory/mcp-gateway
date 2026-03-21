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


MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() in ("true", "1", "yes")


def validate_config() -> list[str]:
    """Validate configuration and return list of missing required variables.

    In mock mode, missing API credentials are acceptable.
    In production mode, raises RuntimeError if required vars are missing.
    """
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not GOOGLE_CSE_ID:
        missing.append("GOOGLE_CSE_ID")

    if missing and not MOCK_MODE:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Set them in .env or enable MOCK_MODE=true for development."
        )

    if missing and MOCK_MODE:
        logger.warning(
            f"Missing env vars {missing} - running in MOCK_MODE, API calls will return mock data"
        )

    return missing
