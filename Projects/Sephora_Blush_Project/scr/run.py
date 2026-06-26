"""
Usage
-----
    python run.py scrape --category blush --limit 5      # small test scrape
"""
from __future__ import annotations

import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from scraping.scraper import scrape_category


def main():
    parser = argparse.ArgumentParser(description="Sephora blush data pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scrape = sub.add_parser("scrape", help="Scrape raw product/shade data")
    p_scrape.add_argument("--category", default="blush")
    p_scrape.add_argument("--limit", type=int, default=None, help="Cap number of products (for testing)")
    p_scrape.add_argument("--max-workers", type=int, default=8)

    sub.add_parser("clean", help="Clean raw JSON into products.csv + shades.csv")
    sub.add_parser("merge", help="Merge products.csv + shades.csv into merged.csv")

    p_all = sub.add_parser("all", help="Run scrape -> clean -> merge in sequence")
    p_all.add_argument("--category", default="blush")
    p_all.add_argument("--limit", type=int, default=None)
    p_all.add_argument("--max-workers", type=int, default=8)

    args = parser.parse_args()

    if args.command == "scrape":
        scrape_category(category=args.category, limit=args.limit, max_workers=args.max_workers)


if __name__ == "__main__":
    main()