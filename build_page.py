from datetime import datetime, timezone, timedelta
from config import SECTIONS

IST = timezone(timedelta(hours=5, minutes=30))

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gunjan's News Feed — {date}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #f5f5f0;
      color: #1a1a1a;
      margin: 0;
      padding: 1rem;
      max-width: 780px;
      margin-inline: auto;
    }}
    header {{
      text-align: center;
      padding: 2rem 0 1rem;
      border-bottom: 2px solid #d0c8b0;
      margin-bottom: 2rem;
    }}
    header h1 {{
      font-size: 1.8rem;
      margin: 0 0 0.3rem;
      color: #2c2c2c;
    }}
    header p.date {{
      font-size: 0.9rem;
      color: #666;
      margin: 0;
    }}
    .quote-block {{
      background: #fffbef;
      border-left: 4px solid #e8c84a;
      padding: 1rem 1.2rem;
      border-radius: 4px;
      margin-bottom: 2rem;
      font-style: italic;
    }}
    .quote-block span.author {{
      display: block;
      margin-top: 0.5rem;
      font-style: normal;
      font-size: 0.85rem;
      color: #555;
    }}
    section {{
      margin-bottom: 2.5rem;
    }}
    section h2 {{
      font-size: 1.15rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #444;
      border-bottom: 1px solid #ddd;
      padding-bottom: 0.4rem;
      margin-bottom: 1rem;
    }}
    .article {{
      margin-bottom: 1.2rem;
      padding-bottom: 1.2rem;
      border-bottom: 1px solid #e8e8e0;
    }}
    .article:last-child {{
      border-bottom: none;
      margin-bottom: 0;
      padding-bottom: 0;
    }}
    .article h3 {{
      margin: 0 0 0.3rem;
      font-size: 1rem;
    }}
    .article h3 a {{
      color: #1a5276;
      text-decoration: none;
    }}
    .article h3 a:hover {{
      text-decoration: underline;
    }}
    .article p {{
      margin: 0 0 0.3rem;
      font-size: 0.92rem;
      line-height: 1.55;
      color: #333;
    }}
    .article .source {{
      font-size: 0.78rem;
      color: #888;
    }}
    .thought-block {{
      background: #f0f4ff;
      border-left: 4px solid #5b7fd4;
      padding: 1rem 1.2rem;
      border-radius: 4px;
    }}
    .thought-block h3 {{
      margin: 0 0 0.4rem;
      font-size: 1rem;
    }}
    .thought-block h3 a {{
      color: #1a3a7a;
      text-decoration: none;
    }}
    .thought-block h3 a:hover {{
      text-decoration: underline;
    }}
    .thought-block p {{
      margin: 0 0 0.4rem;
      font-size: 0.92rem;
      line-height: 1.5;
      color: #333;
    }}
    .thought-block .source {{
      font-size: 0.78rem;
      color: #777;
    }}
    footer {{
      text-align: center;
      font-size: 0.78rem;
      color: #aaa;
      padding: 2rem 0 1rem;
      border-top: 1px solid #ddd;
      margin-top: 2rem;
    }}
    @media (max-width: 480px) {{
      body {{ padding: 0.75rem; }}
      header h1 {{ font-size: 1.4rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Gunjan's News Feed</h1>
    <p class="date">{date}</p>
  </header>

  <div class="quote-block">
    &ldquo;{quote_text}&rdquo;
    <span class="author">&mdash; {quote_author}</span>
  </div>

{sections_html}

  <footer>
    Generated automatically &middot; Powered by NewsAPI &amp; Claude AI
  </footer>
</body>
</html>
"""

ARTICLE_TEMPLATE = """\
    <div class="article">
      <h3><a href="{url}" target="_blank" rel="noopener">{title}</a></h3>
      <p>{summary}</p>
      <span class="source">{source}</span>
    </div>"""

THOUGHT_TEMPLATE = """\
  <section>
    <h2>{section_title}</h2>
    <div class="thought-block">
      <h3><a href="{url}" target="_blank" rel="noopener">{title}</a></h3>
      <p>{summary}</p>
      <span class="source">{source}</span>
    </div>
  </section>"""

SECTION_TEMPLATE = """\
  <section>
    <h2>{section_title}</h2>
{articles_html}
  </section>"""


def _escape(text: str) -> str:
    """Minimal HTML escaping."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def build_section_html(section: dict, articles: list) -> str:
    """Render a single feed section to HTML."""
    if not articles:
        return ""

    section_title = _escape(section["title"])

    if section.get("mode") == "thought":
        article = articles[0]
        return THOUGHT_TEMPLATE.format(
            section_title=section_title,
            url=_escape(article["url"]),
            title=_escape(article["title"]),
            summary=_escape(article["summary"]),
            source=_escape(article["source"]),
        )

    article_htmls = []
    for article in articles:
        article_htmls.append(ARTICLE_TEMPLATE.format(
            url=_escape(article["url"]),
            title=_escape(article["title"]),
            summary=_escape(article["summary"]),
            source=_escape(article["source"]),
        ))

    return SECTION_TEMPLATE.format(
        section_title=section_title,
        articles_html="\n".join(article_htmls),
    )


def build_page(quote: dict, enriched_data: dict, output_path: str = "index.html"):
    """Assemble the full HTML page and write to output_path."""
    now_ist = datetime.now(IST)
    date_str = now_ist.strftime("%A, %B %-d, %Y")  # e.g. "Sunday, March 8, 2026"

    # Build sections HTML in the order defined in SECTIONS
    section_map = {s["id"]: s for s in SECTIONS}
    sections_html_parts = []
    for section in SECTIONS:
        sid = section["id"]
        articles = enriched_data.get(sid, [])
        html = build_section_html(section, articles)
        if html:
            sections_html_parts.append(html)

    full_html = HTML_TEMPLATE.format(
        date=date_str,
        quote_text=_escape(quote.get("text", "")),
        quote_author=_escape(quote.get("author", "")),
        sections_html="\n".join(sections_html_parts),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"[build] Written to {output_path}")
