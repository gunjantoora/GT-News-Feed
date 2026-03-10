import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "env_vars.env")  # always resolves relative to config.py

# --- API Keys ---
GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# --- GNews base URL ---
GNEWS_BASE = "https://gnews.io/api/v4"

# --- Quote API (quotable.io — free, no key, quotes from famous people across history/culture/science) ---
QUOTE_URL = "https://api.quotable.io/quotes/random?minLength=60&maxLength=200"

# --- Claude model ---
CLAUDE_MODEL = "claude-haiku-4-5-20251001"  # cheapest model to minimize token cost

# --- Feed sections ---
# Each section: name, fetch_type, and type-specific params
SECTIONS = [
    {
        "id": "positive",
        "title": "Positive News",
        "fetch_type": "search",
        "params": {
            "q": "breakthrough OR conservation OR achievement OR innovation OR restored",
            "lang": "en",
            "max": 5,
        },
        "max_items": 1,
    },
    {
        "id": "world",
        "title": "World News",
        "fetch_type": "search",
        "params": {
            "q": "geopolitics OR war OR diplomacy OR sanctions OR election OR health crisis OR disaster OR famine OR treaty",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "india",
        "title": "India News",
        "fetch_type": "top-headlines",
        "params": {
            "country": "in",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "environment",
        "title": "Environment & Climate",
        "fetch_type": "search",
        "params": {
            "q": "climate change OR environment OR renewable energy",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "tech",
        "title": "Tech & AI",
        "fetch_type": "top-headlines",
        "params": {
            "category": "technology",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "science",
        "title": "Science & Engineering",
        "fetch_type": "top-headlines",
        "params": {
            "category": "science",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "energy",
        "title": "Energy",
        "fetch_type": "search",
        "params": {
            "q": "solar energy OR wind power OR nuclear energy",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
]
