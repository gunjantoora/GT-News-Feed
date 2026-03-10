import time
import requests
import random
from datetime import datetime, timezone, timedelta
from config import GNEWS_API_KEY, GNEWS_BASE, QUOTE_URL, SECTIONS

EXCLUDE_KEYWORDS = {
    # Sports
    "cricket", "ipl", "football", "soccer", "tennis", "basketball", "nba", "nfl", "nhl",
    "formula 1", "f1", "grand prix", "olympics", "fifa", "uefa", "premier league",
    "wicket", "batting", "bowling", "odi", "t20", "test match", "scorecard",
    "match result", "tournament", "championship", "league table",
    # Entertainment / celebrity
    "bollywood", "celebrity", "actor", "actress", "film", "movie", "box office",
    "entertainment", "gossip", "bigg boss", "reality show", "serial", "tv show",
    # Clickbait / sensationalist
    "you won't believe", "shocking", "mind-blowing", "goes viral", "twitter reacts",
    "breaks the internet", "slams", "destroys", "obliterates",
}


def fetch_quote():
    """Fetch a random quote from quotable.io (famous people across history, science, culture)."""
    try:
        resp = requests.get(QUOTE_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return {"text": data[0]["content"], "author": data[0]["author"]}
    except Exception as e:
        print(f"[quote] Failed: {e}")
    return {"text": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu"}


def _48h_from() -> str:
    """Return ISO timestamp for 48 hours ago, for GNews 'from' param."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    return cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")


def _fetch_articles(section: dict) -> list:
    """Fetch raw articles from GNews for a given section config."""
    fetch_type = section["fetch_type"]  # "search" or "top-headlines"
    params = dict(section["params"])
    params["apikey"] = GNEWS_API_KEY
    if fetch_type == "search" and section.get("mode") != "thought":
        params["from"] = _48h_from()  # only articles from last 48 hours (thought section is timeless)

    url = f"{GNEWS_BASE}/{fetch_type}"

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        articles = [
            a for a in articles
            if a.get("title") and a.get("url")
        ]
        return articles
    except Exception as e:
        print(f"[fetch] Section '{section['id']}' failed: {e}")
        return []


def _filter_articles(articles: list) -> list:
    """Remove sports, entertainment, and celebrity articles from any section."""
    filtered = []
    for a in articles:
        text = ((a.get("title") or "") + " " + (a.get("description") or "")).lower()
        if not any(kw in text for kw in EXCLUDE_KEYWORDS):
            filtered.append(a)
    return filtered


def fetch_all_sections() -> dict:
    """
    Returns a dict keyed by section id.
    Each value is a list of article dicts (raw from GNews), trimmed to max_items.
    The 'thought' section picks one random article.
    """
    results = {}
    for section in SECTIONS:
        articles = _fetch_articles(section)
        max_items = section.get("max_items", 3)

        articles = _filter_articles(articles)

        if section.get("mode") == "thought":
            results[section["id"]] = [random.choice(articles)] if articles else []
        else:
            results[section["id"]] = articles[:max_items]

        print(f"[fetch] {section['id']}: {len(results[section['id']])} articles")
        time.sleep(1)  # avoid hitting per-second rate limits

    return results
