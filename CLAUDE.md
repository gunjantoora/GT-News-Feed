# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Generates a daily personal newsfeed (`index.html`) hosted on GitHub Pages. Runs via GitHub Actions cron daily at 00:30 UTC (6am IST). Fetches news from GNews API, a motivational quote from ZenQuotes, summarizes articles with Claude AI, and renders a static HTML page.

## Running the project

```bash
# Install dependencies
pip install -r requirements.txt

# Generate index.html
python main.py
```

API keys must be in `env_vars.env` in the project root (gitignored):
```
GNEWS_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## Architecture

The pipeline runs in 3 sequential steps (`main.py`):

1. **`fetch_news.py`** — fetches quote from ZenQuotes and articles from GNews API for all sections defined in `config.py`
2. **`summarize.py`** — makes one Claude API call per section to summarize all articles in that section at once (not one call per article)
3. **`build_page.py`** — renders `index.html` using Python string templates (no Jinja2)

## Configuration

All feed sections are defined in `config.py` as the `SECTIONS` list. Each section has:
- `fetch_type`: `"top-headlines"` (category/country based) or `"search"` (keyword based)
- `params`: passed directly to GNews API (`lang`, `max`, `category`, `country`, or `q`)
- `max_items`: how many articles to show
- `mode: "thought"`: special flag for the Thought of the Day section — picks one random article, no AI summary, different HTML rendering

GNews free tier (100 req/day) supports both `top-headlines` and `search` endpoints. `search` uses `q` with keyword queries.

## Key constraints

- **Python 3.8** (Anaconda) — no `list[dict]` or `dict[str, X]` type hint syntax; use bare `list` and `dict`
- Claude model: `claude-haiku-4-5-20251001` to minimize cost
- `env_vars.env` is loaded via `python-dotenv` using an absolute path relative to `config.py` so it works regardless of working directory
- `index.html` is gitignored locally but committed by the GitHub Actions workflow


## News Filtering Rules

### India News
- Exclude Bollywood, cricket, celebrity gossip, entertainment news
- Focus on: policy, science, startups, economy, social issues, environment, space

### Positive News
- Don't just search generic "good news"
- Better search angles:
  - Scientific breakthroughs that help humanity
  - Conservation wins (species saved, forests restored, oceans cleaned)
  - Women leading change in politics, science, business
  - Community-led solutions to poverty, hunger, education
  - Clean energy milestones
- Tone filter: only include if the story is genuinely uplifting, not just "less bad than expected"

### Thought-Provoking Article (end of feed)
- Avoid generic lifestyle/wellness content
- Look for: unsolved historical mysteries, counterintuitive science,
  ancient civilizations, rare natural phenomena, philosophical paradoxes,
  interesting biographies of forgotten figures, deep nature stories
- Think: "would a curious 30-year-old find this fascinating at 7am?"

## Quote of the Day
- ZenQuotes API is the source, but if the quote returned is generic or
  motivational-poster-level shallow, Claude should regenerate a better one
- Preferred tone: intellectual, thought-provoking, slightly uncomfortable
- Good sources to draw from: Stoic philosophers, Marcus Aurelius, Seneca,
  Dostoevsky, Kafka, Feynman, historical figures, classic literature
- Avoid: generic hustle quotes, anything that sounds like a LinkedIn post

## General Principles
- Summarize in plain, smart English — not corporate or robotic
- 1-3 lines per summary max, make every word count
- URLs must always link to the original source article