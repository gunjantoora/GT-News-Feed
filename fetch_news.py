import time
import requests
import random
from config import GNEWS_API_KEY, GNEWS_BASE, ZENQUOTES_URL, SECTIONS

INDIA_EXCLUDE_KEYWORDS = {
    "bollywood", "cricket", "ipl", "celebrity", "actor", "actress",
    "film", "movie", "box office", "wicket", "batting", "bowling",
    "odi", "t20", "test match", "entertainment", "gossip", "bigg boss",
    "reality show", "serial", "tv show",
}


def fetch_quote():
    """Fetch today's motivational quote from ZenQuotes."""
    try:
        resp = requests.get(ZENQUOTES_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return {"text": data[0]["q"], "author": data[0]["a"]}
    except Exception as e:
        print(f"[quote] Failed: {e}")
    return {"text": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu"}


def _fetch_articles(section: dict) -> list:
    """Fetch raw articles from GNews for a given section config."""
    fetch_type = section["fetch_type"]  # "search" or "top-headlines"
    params = dict(section["params"])
    params["apikey"] = GNEWS_API_KEY

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


def _filter_india(articles: list) -> list:
    """Remove entertainment/cricket/celebrity articles from India news."""
    filtered = []
    for a in articles:
        text = ((a.get("title") or "") + " " + (a.get("description") or "")).lower()
        if not any(kw in text for kw in INDIA_EXCLUDE_KEYWORDS):
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

        if section["id"] == "india":
            articles = _filter_india(articles)

        if section.get("mode") == "thought":
            results[section["id"]] = [random.choice(articles)] if articles else []
        else:
            results[section["id"]] = articles[:max_items]

        print(f"[fetch] {section['id']}: {len(results[section['id']])} articles")
        time.sleep(1)  # avoid hitting per-second rate limits

    return results
