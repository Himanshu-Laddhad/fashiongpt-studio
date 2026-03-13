"""
LLM Configuration using FREE Groq API
Super fast (100+ tokens/sec) and completely free
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    # Manual .env loading fallback
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

# Groq API Configuration (FREE)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Use the latest available Groq model (llama-3.3-70b-versatile is the newest, falls back to 70b-8192)
GROQ_MODEL = "llama-3.3-70b-versatile"

# Model settings
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# Check if API key is configured (empty or unset placeholder)
_PLACEHOLDER = "your-groq-api-key-here"
USE_FALLBACK = not GROQ_API_KEY or GROQ_API_KEY == _PLACEHOLDER

if USE_FALLBACK:
    print("\n" + "=" * 60)
    print("⚠️  WARNING: No Groq API key configured")
    print("=" * 60)
    print("To enable AI-powered analysis:")
    print("1. Visit: https://console.groq.com/keys")
    print("2. Sign up (FREE, no credit card)")
    print("3. Create API key")
    print("4. Add to .env file: GROQ_API_KEY=your-key-here")
    print("\nUsing fallback rule-based analysis for now...")
    print("=" * 60 + "\n")
else:
    print(f"[OK] Groq API key loaded (model: {GROQ_MODEL})")
