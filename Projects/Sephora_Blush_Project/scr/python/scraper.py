"""
Sephora Product Scraper
=======================
Parameterized scraper for any Sephora category (blush, foundation, bronzer, etc.).

Data sources:
  1. Listing API         → basic product info (pagination-aware)
  2. Product page HTML   → linkStore JSON blob (description, ingredients, how-to-use)
  3. Anonymous SKU API   → all shade variants + per-shade pricing

All detail data comes from server-rendered linkStore JSON — no browser automation needed.

Usage:
    from sephora.scraper import SephoraScraper

    scraper = SephoraScraper(category="blush")
    scraper.run(limit=None)              # scrape all products
    scraper.run(limit=5)                 # test with 5 products
    scraper.run(category="foundation")   # scrape a different category

CLI:
    python -m sephora.scraper --category blush
    python -m sephora.scraper --category foundation --limit 10 --output ./data
"""

import os
import json
import re
import time
import math
import random
import argparse
from datetime import datetime, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sephora.com"

# ── HTTP Headers ─────────────────────────────────────────────────────────────────
# These Chrome 122 headers + random delays are sufficient to avoid Akamai 403s
# on product page fetches.  The listing & SKU APIs don't need bot headers.

HEADERS_HTML = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "Sec-Ch-Ua": (
        '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"'
    ),
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Upgrade-Insecure-Requests": "1",
}

HEADERS_API = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sephora.com/shop/blush",
}


# ── Helpers ──────────────────────────────────────────────────────────────────────

def strip_html(html_str: Optional[str]) -> Optional[str]:
    """Remove HTML tags and collapse whitespace. Returns None for empty input."""
    if not html_str:
        return None
    text = BeautifulSoup(html_str, "html.parser").get_text(separator=" ").strip()
    text = re.sub(r"\s{2,}", " ", text)
    return text or None


def extract_shade_name(alt_text: str) -> Optional[str]:
    """
    Extract shade name from altText like:
        'brand Product in SHADE_NAME Image 2'
        'brand Product in SHADE_NAME - color description Image 2'
    """
    if " in " in alt_text:
        shade = alt_text.split(" in ", 1)[1]
        shade = re.sub(r"\s+Image\s+\d+$", "", shade).strip()
        return shade or None
    return None


# ── Scraper Class ────────────────────────────────────────────────────────────────

class SephoraScraper:
    """
    Scrape Sephora product listings with full detail enrichment.

    Parameters
    ----------
    category : str
        Category slug (e.g. 'blush', 'foundation', 'bronzer', 'highlighter').
    output_dir : str
        Directory for output JSON files.  Created if needed.
    page_size : int
        Results per listing API page (max 60).
    checkpoint_every : int
        Save a checkpoint JSON every N products.
    """

    def __init__(
        self,
        category: str = "blush",
        output_dir: str = "data/raw",
        page_size: int = 60,
        checkpoint_every: int = 25,
    ):
        self.category = category
        self.output_dir = output_dir
        self.page_size = page_size
        self.checkpoint_every = checkpoint_every

        # Delay ranges (seconds) — increase for larger categories
        self.html_delay = (1.5, 3.0)
        self.sku_delay = (0.5, 1.2)

    # ── Step 1: Listing API ────────────────────────────────────────────────

    def _fetch_listing(self) -> list[dict]:
        """Paginate the category listing API and return all product dicts."""
        url = f"{BASE_URL}/api/v2/catalog/categories/{self.category}/seo"
        params = {
            "pageSize": self.page_size,
            "content": "true",
            "loc": "en-US",
            "ch": "rwd",
            "currentPage": 1,
        }

        print(f"Fetching listing page 1 for '{self.category}'...")
        r = requests.get(url, params=params, headers=HEADERS_API)
        r.raise_for_status()
        data = r.json()

        total = data.get("totalProducts", 0)
        total_pages = math.ceil(total / self.page_size)
        print(f"  {total} products across {total_pages} pages")

        products = list(data.get("products", []))

        for page in range(2, total_pages + 1):
            time.sleep(1)
            params["currentPage"] = page
            r = requests.get(url, params=params, headers=HEADERS_API)
            r.raise_for_status()
            batch = r.json().get("products", [])
            products.extend(batch)
            print(f"  Page {page}/{total_pages}: +{len(batch)} products")

        return products

    @staticmethod
    def _parse_listing_product(p: dict) -> dict:
        """Flatten a listing API product dict into a clean base record."""
        sku = p.get("currentSku", {})
        return {
            "product_id":           p.get("productId"),
            "brand":                p.get("brandName"),
            "name":                 p.get("displayName"),
            "sku_id":               sku.get("skuId"),
            "list_price":           sku.get("listPrice"),
            "sale_price":           sku.get("salePrice"),
            "on_sale":              p.get("onSaleData", "NONE") != "NONE",
            "rating":               float(p["rating"]) if p.get("rating") else None,
            "reviews":              int(p["reviews"]) if p.get("reviews") else None,
            "more_colors":          p.get("moreColors", 0),
            "sku_type":             sku.get("skuType"),          # 'wf', 'c', etc.
            "is_bestseller":        sku.get("isBestseller", False),
            "is_new":               sku.get("isNew", False),
            "is_sephora_exclusive": sku.get("isSephoraExclusive", False),
            "is_limited_edition":   sku.get("isLimitedEdition", False),
            "is_online_only":       sku.get("isOnlineOnly", False),
            "is_discontinued":      False,                # filled by detail step
            "sponsored":            p.get("sponsored", False),
            "product_url":          BASE_URL + (p.get("targetUrl") or ""),
            "hero_image_url":       p.get("heroImage", ""),
        }

    # ── Step 2: Product page → linkStore JSON ───────────────────────────────

    def _fetch_product_detail(
        self, target_url: str, sku_id: str
    ) -> dict:
        """
        Fetch product page HTML, extract linkStore JSON.

        Confirmed paths:
            page.product.quickLookDescription           → short_description
            page.product.productDetails.longDescription  → long_description
            page.product.productDetails.suggestedUsage   → how_to_use
            page.product.productDetails.lovesCount       → loves_count
            page.product.currentSku.ingredientDesc       → ingredients
            page.product.currentSku.sizeLabel            → size
        """
        result = {
            "short_description": None,
            "long_description":  None,
            "how_to_use":        None,
            "loves_count":       None,
            "ingredients":       None,
            "size":              None,
            "is_discontinued":   False,
        }

        url = f"{BASE_URL}{target_url}"
        if "skuId" not in url:
            url += f"?skuId={sku_id}"

        session = requests.Session()
        try:
            time.sleep(random.uniform(*self.html_delay))
            r = session.get(url, headers=HEADERS_HTML, timeout=15)

            if r.status_code == 404:
                result["is_discontinued"] = True
                return result
            if r.status_code == 403:
                print("    ⚠ 403 blocked")
                return result
            r.raise_for_status()
        except Exception as e:
            print(f"    ⚠ HTML fetch error: {e}")
            return result

        soup = BeautifulSoup(r.text, "html.parser")
        script_tag = soup.find("script", {"id": "linkStore", "type": "text/json"})

        if not (script_tag and script_tag.string):
            # Missing linkStore → likely discontinued
            result["is_discontinued"] = True
            return result

        try:
            data = json.loads(script_tag.string)
            product = data.get("page", {}).get("product", {})

            if not product:
                result["is_discontinued"] = True
                return result

            details = product.get("productDetails", {})
            cur_sku = product.get("currentSku", {})

            result["short_description"] = strip_html(
                product.get("quickLookDescription")
            )
            result["long_description"] = strip_html(
                details.get("longDescription")
            )
            result["how_to_use"] = strip_html(details.get("suggestedUsage"))
            result["loves_count"] = details.get("lovesCount")
            result["ingredients"] = strip_html(cur_sku.get("ingredientDesc"))
            result["size"] = cur_sku.get("sizeLabel")

        except Exception as e:
            print(f"    ⚠ linkStore parse error: {e}")

        return result

    # ── Step 3: Anonymous SKU API → shades ──────────────────────────────────

    def _fetch_shades(self, product_id: str, default_sku_id: str) -> list[dict]:
        """Return all shade variants with name, price, and stock info."""
        url = f"{BASE_URL}/api/v3/users/profiles/anonymous/product/{product_id}"
        params = {
            "preferedSku": default_sku_id,
            "countryCode": "US",
            "loc": "EN-US",
        }

        try:
            time.sleep(random.uniform(*self.sku_delay))
            r = requests.get(url, params=params, headers=HEADERS_API, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"    ⚠ SKU API error: {e}")
            return []

        def _parse(sku: dict) -> dict:
            imgs = sku.get("alternateImages", [])
            alt = imgs[0].get("altText", "") if imgs else ""
            return {
                "sku_id":        sku.get("skuId"),
                "shade_name":    extract_shade_name(alt),
                "list_price":    sku.get("listPrice"),
                "sale_price":    sku.get("salePrice"),
                "in_stock":      sku.get("isEligible", False),
                "is_final_sale": sku.get("isFinalSale", False),
                "badge":         sku.get("badgeAltText"),
                "image_url":     sku.get("skuImages", {}).get("imageUrl"),
            }

        shades = []
        if current := data.get("currentSku"):
            shades.append(_parse(current))
        for child in data.get("regularChildSkus", []):
            shades.append(_parse(child))

        return shades

    # ── Orchestration ───────────────────────────────────────────────────────

    def run(self, limit: Optional[int] = None) -> list[dict]:
        """
        Run the full scrape pipeline.

        Parameters
        ----------
        limit : int, optional
            Only process this many products (for testing).  None = all.

        Returns
        -------
        list[dict]
            Enriched product records with nested shade data.
        """
        print("=" * 55)
        print(f"  Sephora '{self.category}' Scraper")
        print("=" * 55)

        listing = self._fetch_listing()
        process_queue = listing[:limit] if limit else listing

        label = f"{len(process_queue)} of {len(listing)}" if limit else f"all {len(listing)}"
        print(f"\nEnriching {label} products...\n")

        os.makedirs(self.output_dir, exist_ok=True)

        all_data: list[dict] = []
        start_time = datetime.now(timezone.utc)

        for i, p in enumerate(process_queue, 1):
            pid = p.get("productId")
            tgt = p.get("targetUrl", "")
            sid = p.get("currentSku", {}).get("skuId", "")
            label = f"{p.get('brandName')} — {(p.get('displayName') or '')[:38]}"

            print(f"[{i:3}/{len(process_queue)}] {label}")

            base = self._parse_listing_product(p)
            timestamp = datetime.now(timezone.utc).isoformat()

            page_data = self._fetch_product_detail(tgt, sid)
            shades = self._fetch_shades(pid, sid)

            record = {
                **base,
                **page_data,
                "shades": shades,
                "scraped_at": timestamp,
            }

            # Propagate discontinued flag to base fields
            if page_data.get("is_discontinued"):
                record["is_discontinued"] = True

            all_data.append(record)

            d = "✓" if record.get("short_description") else "✗"
            g = "✓" if record.get("ingredients") else "✗"
            h = "✓" if record.get("how_to_use") else "✗"
            print(f"       desc:{d} ing:{g} how:{h} | {len(shades)} shades")

            if i % self.checkpoint_every == 0:
                ckpt = os.path.join(
                    self.output_dir,
                    f"checkpoint_{self.category}_{i:04d}.json",
                )
                with open(ckpt, "w", encoding="utf-8") as f:
                    json.dump(all_data, f, indent=2, ensure_ascii=False)
                print(f"       💾 Checkpoint saved ({i}/{len(process_queue)})\n")

        # Final output
        ts = start_time.strftime("%Y%m%d_%H%M%S")
        final_output = os.path.join(
            self.output_dir,
            f"sephora_{self.category}_{ts}.json",
        )
        with open(final_output, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        # Summary
        print(f"\n{'=' * 55}")
        print(f"  ✅ Saved {len(all_data)} products → {final_output}")
        print(f"\n  Field coverage:")
        for field in [
            "short_description", "long_description",
            "how_to_use", "ingredients",
        ]:
            count = sum(1 for r in all_data if r.get(field))
            print(f"    {field:<22} {count}/{len(all_data)}")

        total_shades = sum(len(r.get("shades", [])) for r in all_data)
        discontinued = sum(1 for r in all_data if r.get("is_discontinued"))
        print(f"    {'shades':<22} {total_shades} total shade records")
        if discontinued:
            print(f"    {'discontinued':<22} {discontinued} products")
        print("=" * 55)

        return all_data


# ── CLI ──────────────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sephora product scraper — fetch any category"
    )
    parser.add_argument(
        "--category", default="blush",
        help="Category slug (default: blush)",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Only scrape N products (default: all)",
    )
    parser.add_argument(
        "--output", default="data/raw",
        help="Output directory (default: data/raw)",
    )
    parser.add_argument(
        "--page-size", type=int, default=60,
        help="Products per listing page (default: 60)",
    )
    parser.add_argument(
        "--checkpoint", type=int, default=25,
        help="Save checkpoint every N products (default: 25)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    scraper = SephoraScraper(
        category=args.category,
        output_dir=args.output,
        page_size=args.page_size,
        checkpoint_every=args.checkpoint,
    )
    scraper.run(limit=args.limit)