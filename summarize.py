import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, SECTIONS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _build_prompt(section_title: str, articles: list) -> str:
    """Build a single prompt to summarize all articles in a section at once."""
    lines = [
        f"You are writing summaries for a personal daily digest called \"Gunjan's News Feed\".",
        f"Section: {section_title}",
        "",
        "For each article, write a 1-3 sentence summary in plain, smart English.",
        "Be direct and specific. No corporate language, no filler phrases like 'in a significant development'.",
        "Make every word count. Write like a sharp journalist, not a press release.",
        "Return ONLY a numbered list matching the article numbers. No extra commentary.",
        "Format each item exactly as:",
        "N. <summary text>",
        "",
        "Articles:",
    ]
    for i, article in enumerate(articles, 1):
        title = article.get("title", "").strip()
        description = article.get("description") or article.get("content") or ""
        description = description.strip()[:500]  # cap to avoid huge prompts
        lines.append(f"{i}. Title: {title}")
        if description:
            lines.append(f"   Description: {description}")
    return "\n".join(lines)


def _parse_summaries(response_text: str, count: int) -> list:
    """Parse the numbered list response into a list of summary strings."""
    summaries = [""] * count
    for line in response_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Match lines like "1. summary text"
        for i in range(count, 0, -1):
            prefix = f"{i}."
            if line.startswith(prefix):
                summaries[i - 1] = line[len(prefix):].strip()
                break
    return summaries


def summarize_section(section_id: str, section_title: str, articles: list) -> list:
    """
    Given a list of raw article dicts, returns enriched dicts with a 'summary' key added.
    Makes ONE Claude API call per section to minimize token usage.
    """
    if not articles:
        return []

    prompt = _build_prompt(section_title, articles)

    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}],
        )
        response_text = message.content[0].text
        summaries = _parse_summaries(response_text, len(articles))
    except Exception as e:
        print(f"[summarize] Section '{section_id}' Claude call failed: {e}")
        summaries = [article.get("description") or "" for article in articles]

    enriched = []
    for article, summary in zip(articles, summaries):
        enriched.append({
            "title": article.get("title", "").strip(),
            "url": article.get("url", ""),
            "source": article.get("source", {}).get("name", ""),
            "summary": summary or article.get("description") or "",
        })
    return enriched


def evaluate_quote(quote: dict) -> dict:
    """
    Check if the ZenQuotes quote is shallow/generic. If so, ask Claude for a better one.
    Returns the original or a replacement quote dict with 'text' and 'author' keys.
    """
    prompt = (
        f"Here is today's quote:\n\"{quote['text']}\" — {quote['author']}\n\n"
        "Is this quote intellectually interesting, thought-provoking, or slightly uncomfortable in a good way? "
        "Or is it generic, motivational-poster-level, or LinkedIn-style?\n\n"
        "If it's good, reply with just: KEEP\n"
        "If it's generic, reply with a better quote from a Stoic philosopher, Dostoevsky, Kafka, Feynman, "
        "or another sharp historical mind. Format exactly as:\n"
        "REPLACE: \"<quote text>\" — <Author Name>"
    )
    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        response = message.content[0].text.strip()
        if response.startswith("REPLACE:"):
            parts = response[len("REPLACE:"):].strip()
            # Parse: "quote text" — Author Name
            if "\" —" in parts:
                text_part, author_part = parts.rsplit("\" —", 1)
                text = text_part.strip().lstrip('"')
                author = author_part.strip()
                print(f"[quote] Replaced with: {author}")
                return {"text": text, "author": author}
    except Exception as e:
        print(f"[quote] Evaluation failed: {e}")
    return quote


def summarize_all(sections_data: dict) -> dict:
    """
    Takes the raw fetched data dict (section_id -> list of articles).
    Returns enriched dict (section_id -> list of article dicts with summaries).
    Skips 'thought' section — it needs no AI summary.
    """
    # Build a map of section mode by id
    section_modes = {s["id"]: s.get("mode") for s in SECTIONS}
    section_titles = {s["id"]: s["title"] for s in SECTIONS}

    enriched = {}
    for section_id, articles in sections_data.items():
        if section_modes.get(section_id) == "thought":
            # Pass through as-is for the thought section
            enriched[section_id] = [
                {
                    "title": a.get("title", "").strip(),
                    "url": a.get("url", ""),
                    "source": a.get("source", {}).get("name", ""),
                    "summary": (a.get("description") or "")[:300],
                }
                for a in articles
            ]
            print(f"[summarize] {section_id}: skipped (thought section)")
        else:
            title = section_titles.get(section_id, section_id)
            enriched[section_id] = summarize_section(section_id, title, articles)
            print(f"[summarize] {section_id}: {len(enriched[section_id])} articles summarized")

    return enriched
