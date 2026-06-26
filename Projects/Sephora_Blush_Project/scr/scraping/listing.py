from __future__ import annotations

import math
import time

from scraping.http import build_session
from config import BASE_URL, HEADERS_API, LISTING_API_PATH


def fetch_all_products(category: str = "blush", page_size: int = 60, sleep_between_pages: float = 1.0) -> list[dict]:
    """
    Paginate the category listing API and return every raw product
    record (one per default SKU; shades are fetched separately).
    """
    session = build_session()
    url = f"{BASE_URL}{LISTING_API_PATH.format(category=category)}"
    params = {"pageSize": page_size, "content": "true", "loc": "en-US", "ch": "rwd", "currentPage": 1}

    response = session.get(url, params=params, headers=HEADERS_API, timeout=15)
    response.encoding = "utf-8"
    response.raise_for_status()
    data = response.json()

    total = data.get("totalProducts", 0)
    total_pages = math.ceil(total / data.get("pageSize", page_size))
    products = list(data.get("products", []))

    for page in range(2, total_pages + 1):
        time.sleep(sleep_between_pages)
        params["currentPage"] = page
        response = session.get(url, params=params, headers=HEADERS_API, timeout=15)
        response.encoding = "utf-8"
        response.raise_for_status()
        products.extend(response.json().get("products", []))

    return products


def parse_listing_product(p: dict) -> dict:
    """Flatten one raw listing-API product record into our base fields."""
    sku = p.get("currentSku", {})
    return {
        "product_id": p.get("productId"),
        "brand": p.get("brandName"),
        "product_name": p.get("displayName"),
        "sku_id": sku.get("skuId"),
        "list_price": sku.get("listPrice"),
        "sale_price": sku.get("salePrice"),
        "on_sale": p.get("onSaleData", "NONE") != "NONE",
        "rating": float(p["rating"]) if p.get("rating") else None,
        "reviews": int(p["reviews"]) if p.get("reviews") else None,
        "more_colors": p.get("moreColors", 0),
        "is_bestseller": sku.get("isBestseller", False),
        "is_new": sku.get("isNew", False),
        "is_sephora_exclusive": sku.get("isSephoraExclusive", False),
        "is_limited_edition": sku.get("isLimitedEdition", False),
        "is_online_only": sku.get("isOnlineOnly", False),
        "sponsored": p.get("sponsored", False),
        "product_url": BASE_URL + p.get("targetUrl", ""),
        "hero_image_url": p.get("heroImage", ""),
        "target_url": p.get("targetUrl", ""),  # kept for downstream requests
    }