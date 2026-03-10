import os
from datetime import datetime
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

# --- Thought of the Day: daily theme rotation (history, nature, philosophy, science, culture) ---
_THOUGHT_THEMES = [
    {
        "label": "history",
        "q": "ancient civilization OR archaeological discovery OR forgotten history OR historical mystery OR lost empire",
    },
    {
        "label": "nature",
        "q": "wildlife behavior OR ocean discovery OR rare species OR natural phenomenon OR animal intelligence",
    },
    {
        "label": "philosophy",
        "q": "philosophy consciousness OR thought experiment OR philosophical paradox OR ethics humanity OR meaning existence",
    },
    {
        "label": "science",
        "q": "scientific discovery OR quantum physics OR space exploration OR neuroscience OR cosmology OR mathematics",
    },
    {
        "label": "culture",
        "q": "cultural history OR anthropology OR human tradition OR ancient ritual OR art history OR civilization",
    },
]

_today_theme = _THOUGHT_THEMES[datetime.now().timetuple().tm_yday % len(_THOUGHT_THEMES)]

# --- Feed sections ---
# Each section: name, fetch_type, and type-specific params
SECTIONS = [
    {
        "id": "positive",
        "title": "Positive News",
        "fetch_type": "search",
        "params": {
            "q": "conservation OR breakthrough OR restoration OR milestone OR achievement",
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
        "fetch_type": "search",
        "params": {
            "q": (
                "India policy OR India economy OR India startup OR India science OR"
                " India environment OR India space OR India social OR India government"
            ),
            "lang": "en",
            "max": 8,
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
        "fetch_type": "search",
        "params": {
            "q": "artificial intelligence OR machine learning OR LLM OR OpenAI OR Anthropic",
            "lang": "en",
            "max": 8,
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
        "mode": "thought",
        "params": {
            "q": _today_theme["q"],
            "lang": "en",
            "max": 10,
        },
        "max_items": 1,
    },
]
