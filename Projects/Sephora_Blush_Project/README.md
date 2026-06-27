# Sephora Blush Product Analysis

A reusable pipeline for scraping [Sephora](sephora.com) product data and analyzing  pricing, product attributes, and brand comparisons. This is built for the 2026 Sephora **blush** catalog.

## Structure

```
sephora-blush-analysis/
├── data/
│   ├── raw/             # Scraped JSON output (gitignored)
├── src
│   ├── scraping
│   │   ├── http.py               # requests.Session with curl_cffi
│   │   ├── listing.py            # Step 1: category listing API
│   │   ├── product_detail.py     # Step 2: product page -> linkStore JSON
│   │   ├── shades.py             # Step 3: shades API (incl. swatch images)
│   │   └── scraper.py            # orchestrator, runs steps 1-3 concurrently
│   ├── config.py                # paths, URLs, request settings (single source of truth)
│   ├── encoding_utils.py        # fix_mojibake() — see docs/ENCODING.md
│   ├── io_utils.py               # read/write CSV+JSON, always as UTF-8 
│   ├── run.py                      # CLI entry point
│   ├── cleaning
│   │   └── cleaning.py           # cleaning raw csv files 

```

## Scraping Performance

By using Python's `ThreadPoolExecutor`, the code is able to request multiple at the same time.