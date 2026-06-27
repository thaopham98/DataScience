"""
Usage
-----
    python run.py scrape --category blush --limit 5      # small test scrape
    python run.py clean 
"""
from __future__ import annotations

import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from scraping.scraper import scrape_category
from cleaning.cleaning import run_cleaning_pipeline


def main():
    parser = argparse.ArgumentParser(description="Sephora blush data pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    ## 1. SCRAPE
    p_scrape = sub.add_parser("scrape", help="Scrape raw product/shade data")
    p_scrape.add_argument("--category", default="blush")
    p_scrape.add_argument("--limit", type=int, default=None, help="Cap number of products (for testing)")
    p_scrape.add_argument("--max-workers", type=int, default=8)

    ## 2. CLEAN (updated)
    p_clean = sub.add_parser("clean", help="Clean raw JSON into products.csv + shades.csv")
    p_clean.add_argument("--category", default="blush", help="Category JSON file to clean")

        ### old
    # sub.add_parser("clean", help="Clean raw JSON into products.csv + shades.csv") 
    # sub.add_parser("merge", help="Merge products.csv + shades.csv into merged.csv")

    ## 3. MERGE (new)
    p_merge = sub.add_parser("merge", help="Merge products.csv + shades.csv into merged.csv")
    p_merge.add_argument("--category", default="blush")

    ## 4. ALL
    p_all = sub.add_parser("all", help="Run scrape -> clean -> merge in sequence")
    p_all.add_argument("--category", default="blush")
    p_all.add_argument("--limit", type=int, default=None)
    p_all.add_argument("--max-workers", type=int, default=8)

    args = parser.parse_args()

    if args.command == "scrape":
        scrape_category(category=args.category, limit=args.limit, max_workers=args.max_workers)
    elif args.command == "clean":
        # run_cleaning_pipeline(raw_filename=f"{getattr(args, 'category', 'blush')}_detailed.json") # input will be blush_detailed.csv # old

        ## Updated Version 1
        filename = f"{args.category}_detailed.json"
        print(f"Starting cleaning pipeline for file: {filename}")
        run_cleaning_pipeline(raw_filename=filename)
    
    ## new
    elif args.command == "all":
        # For the 'all' command, it flows sequentially
        scrape_category(category=args.category, limit=args.limit, max_workers=args.max_workers)
        run_cleaning_pipeline(raw_filename=f"{args.category}_detailed.json")

if __name__ == "__main__":
    main()