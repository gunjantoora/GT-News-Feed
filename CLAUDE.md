# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Generates a daily personal newsfeed (`index.html`) hosted on GitHub Pages. Runs via GitHub Actions cron daily at 11:00 UTC (6am CDT / 7am CST). Fetches news from GNews API, a quote from quotable.io, summarizes articles with Claude AI, and renders a static HTML page.

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

1. **`fetch_news.py`** — fetches quote from quotable.io and articles from GNews API for all sections defined in `config.py`
2. **`summarize.py`** — makes one Claude API call per section to summarize all articles in that section at once (not one call per article)
3. **`build_page.py`** — renders `index.html` using Python string templates (no Jinja2)

## Configuration

All feed sections are defined in `config.py` as the `SECTIONS` list. Each section has:
- `fetch_type`: `"top-headlines"` (category/country based) or `"search"` (keyword based)
- `params`: passed directly to GNews API (`lang`, `max`, `category`, `country`, or `q`)
- `max_items`: how many articles to show
- `mode: "thought"`: special flag for the Thought of the Day section — picks one random article, no AI summary, different HTML rendering

GNews free tier (100 req/day) supports both `top-headlines` and `search` endpoints. `search` uses `q` with keyword queries.

Never fetch a sports related article

## Key constraints

- **Python 3.8** (Anaconda) — no `list[dict]` or `dict[str, X]` type hint syntax; use bare `list` and `dict`
- Claude model: `claude-haiku-4-5-20251001` to minimize cost
- `env_vars.env` is loaded via `python-dotenv` using an absolute path relative to `config.py` so it works regardless of working directory
- `index.html` is gitignored locally but committed by the GitHub Actions workflow


## News Filtering Rules

### India News
- Exclude Bollywood, cricket, celebrity gossip, entertainment news
- Focus on: policy, science, startups, economy, social issues, environment, space

### World News
- When looking for World news, it should be relevant to the current world affairs and significant in these sectors- politics / geopolitics/ policy / health/ disasters etc.

### Positive News
- Don't just search generic "good news"
- Better search angles:
  - Scientific breakthroughs that help humanity
  - Conservation wins (species saved, forests restored, oceans cleaned)
  - Women leading change in politics, science, business
  - Community-led solutions to poverty, hunger, education
  - Clean energy milestones
- Tone filter: only include if the story is genuinely uplifting, not just "less bad than expected"

## Thought-Provoking Article (end of feed)
- Rotate theme daily across: history, nature, philosophy, science, culture
- Preferred sources by theme:
  - History: smithsonianmag.com, bbc.co.uk, historytoday.com
  - Nature: nationalgeographic.com, newscientist.com, bbc.com
  - Philosophy: aeon.co, psyche.co, philosophynow.org
  - Science: quantamagazine.org, scientificamerican.com, nautil.us
  - Culture: theatlantic.com, newyorker.com
- Rejection criteria: no "top 10 lists", no self-help, no wellness trends,
  no anything that could appear in a lifestyle magazine
- The bar: would a curious, well-read person genuinely want to read this
  over their morning coffee?

## Quote of the Day
- Preferred tone: intellectual, thought-provoking, slightly uncomfortable
- Good sources to draw from: Stoic philosophers, Marcus Aurelius, Seneca,
  Dostoevsky, Kafka, Feynman, historical figures, classic literature
- Avoid: generic hustle quotes, anything that sounds like a LinkedIn post

## General Principles
- Summarize in plain, smart English — not corporate or robotic
- 1-3 lines per summary max, make every word count
- URLs must always link to the original source article

## What NOT to include (global filter)
- Political propaganda or heavily opinionated op-eds
- Clickbait or sensationalist headlines
- Duplicate stories covering the same event across sections
- Anything older than 48 hours

## Tech & AI Section
- Pull ONLY from these sources: TechCrunch, The Verge, Wired, Ars Technica,
  MIT Technology Review, VentureBeat
- Keywords: "artificial intelligence OR LLM OR large language model OR
  machine learning OR computer science OR deep learning OR OpenAI OR Anthropic"
- Exclude: gadget reviews, phone launches, gaming news, social media drama,
  stock prices of tech companies
- Focus: research breakthroughs, new models, AI policy, CS fundamentals,
  interesting engineering problems