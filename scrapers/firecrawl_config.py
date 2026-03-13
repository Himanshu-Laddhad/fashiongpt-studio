"""
Firecrawl Configuration
"""

import os
from pathlib import Path

# Load .env if not already loaded
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

# Scraping options for different sources
SCRAPE_OPTIONS = {
    "pinterest": {
        "formats": ["html"],
        "onlyMainContent": False,
        "waitFor": 2000,
        "timeout": 15000
    },
    "zara": {
        "formats": ["html", "markdown"],
        "onlyMainContent": True,
        "waitFor": 3000,
        "timeout": 20000
    },
    "uniqlo": {
        "formats": ["html"],
        "onlyMainContent": True,
        "waitFor": 2000,
        "timeout": 15000
    },
    "vogue": {
        "formats": ["markdown"],
        "onlyMainContent": True,
        "timeout": 10000
    }
}
