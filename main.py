"""
main.py — Entry point for Gunjan's News Feed generator.
Run:  python main.py
"""

from fetch_news import fetch_quote, fetch_all_sections
from summarize import summarize_all
from build_page import build_page


def main():
    print("=== Gunjan's News Feed ===")

    print("\n[1/3] Fetching data...")
    quote = fetch_quote()
    sections_data = fetch_all_sections()

    print("\n[2/3] Summarizing with Claude...")
    enriched_data = summarize_all(sections_data)

    print("\n[3/3] Building HTML page...")
    build_page(quote, enriched_data, output_path="index.html")

    print("\nDone! Open index.html to preview.")


if __name__ == "__main__":
    main()
