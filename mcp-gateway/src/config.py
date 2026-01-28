import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")
GOOGLE_CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "./credentials/client_secrets.json")
CREDENTIALS_DIR = os.getenv("CREDENTIALS_DIR", "./credentials")
CACHE_DIR = os.getenv("CACHE_DIR", "./.cache")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
