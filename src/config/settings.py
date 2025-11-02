"""Configuration settings for the startup research agent."""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Email Configuration (Optional)
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",") if os.getenv("EMAIL_RECIPIENTS") else []
ENABLE_EMAIL_NOTIFICATIONS = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"

# LLM Configuration (OpenAI Models)
# Using gpt-4o for both - supports JSON schema structured outputs
# gpt-4o is cheaper than gpt-4 and faster than gpt-3.5-turbo
LLM_MODEL_FAST = "gpt-4o"  # Fast, supports JSON schema
LLM_MODEL_SMART = "gpt-4o"  # Supports JSON schema for structured outputs

# City Tiers
TIER_1_CITIES = ["Delhi", "Mumbai", "Bangalore"]
TIER_2_CITIES = ["Pune", "Hyderabad", "Chennai"]
TIER_3_CITIES = ["Jaipur", "Lucknow", "Chandigarh", "Ahmedabad", "Kolkata"]

# Search Configuration
SEARCH_RESULTS_PER_QUERY = 10
MAX_STARTUPS_PER_RUN = 100
MIN_INDIA_FIT_SCORE = 40

# API Rate Limits
GOOGLE_SEARCH_RATE_LIMIT = 100  # per day
REQUESTS_TIMEOUT = 30  # seconds

# Database
DB_PATH = Path(__file__).parent.parent.parent / "startup_research.db"

# Output
OUTPUT_DIR = Path(__file__).parent.parent.parent / "reports"
REPORT_FORMAT = "json"  # json or pdf

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = Path(__file__).parent.parent.parent / "logs" / "startup_research.log"

# Agent Configuration
AGENT_TIMEOUT = 300  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
API_RATE_LIMIT_DELAY = 2  # seconds between OpenAI API calls to avoid 429 errors

# Deduplication
DEDUPLICATION_THRESHOLD = 0.85  # Fuzzy match threshold


def validate_config() -> None:
    """Validate required configuration."""
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY is required in .env file. Get it from: https://platform.openai.com/api-keys")
    logger.info("✅ Configuration validated successfully")
    logger.info(f"✅ Using OpenAI models: {LLM_MODEL_FAST} (fast) and {LLM_MODEL_SMART} (smart)")


if __name__ == "__main__":
    validate_config()
    logger.info("✅ Configuration loaded successfully")

