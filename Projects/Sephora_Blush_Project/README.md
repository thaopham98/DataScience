# Sephora Blush Product Analysis

A reusable pipeline for scraping [Sephora](sephora.com) product data and analyzing  pricing, product attributes, and brand comparisons. This is built for the 2026 Sephora **blush** catalog.

## Structure

```
sephora-blush-analysis/
├── data/
│   ├── raw/             # Scraped JSON output (gitignored)
├── src/python
│   ├── scraper.py          # Parameterized scraper (any category, CLI-ready). Will create checkpoint for every 25 rows
│   └── cleaning.py         # JSON → 3 flat tables + price-per-unit

```