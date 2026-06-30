from __future__ import annotations
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Sephora endpoints ────────────────────────────────────────────────────────
BASE_URL = "https://www.sephora.com"
LISTING_API_PATH = "/api/v2/catalog/categories/{category}/seo"
SKU_API_PATH = "/api/v3/users/profiles/anonymous/product/{product_id}"

# ── Request settings ─────────────────────────────────────────────────────────
# Every text response from requests MUST be read as UTF-8 explicitly.
# This is the single most important constant in the project: see
# docs/ENCODING.md for why, and src/sephora_blush/scraping/http.py for
# where it's enforced.
RESPONSE_ENCODING = "utf-8"

DEFAULT_TIMEOUT = 15  # seconds
MAX_RETRIES = 3
MAX_CONCURRENT_REQUESTS = 8  # polite parallelism; see docs/PERFORMANCE.md

HEADERS_HTML = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}

HEADERS_API = {
    "User-Agent": HEADERS_HTML["User-Agent"],
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sephora.com/shop/blush",
}