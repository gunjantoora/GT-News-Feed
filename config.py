import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / "env_vars.env")  # always resolves relative to config.py

# --- API Keys ---
GNEWS_API_KEY = os.environ["GNEWS_API_KEY"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# --- GNews base URL ---
GNEWS_BASE = "https://gnews.io/api/v4"

# --- ZenQuotes URL ---
ZENQUOTES_URL = "https://zenquotes.io/api/today"

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
            "q": "conservation win OR scientific breakthrough OR clean energy milestone OR women leading OR community solution",
            "lang": "en",
            "max": 5,
        },
        "max_items": 3,
    },
    {
        "id": "world",
        "title": "World News",
        "fetch_type": "top-headlines",
        "params": {
            "category": "world",
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
    {
        "id": "thought",
        "title": "Thought of the Day",
        "fetch_type": "search",
        "params": {
            "q": "ancient civilization OR philosophical paradox OR counterintuitive science OR forgotten history OR rare phenomenon",
            "lang": "en",
            "max": 10,
        },
        "max_items": 1,
        "mode": "thought",  # special rendering mode — title + 2-line desc + link, no AI summary
    },
]
