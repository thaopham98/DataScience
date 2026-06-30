from __future__ import annotations

import re
from curl_cffi import requests
from curl_cffi.requests.exceptions import RequestException
from config import BASE_URL, HEADERS_API, SKU_API_PATH


def extract_shade_name(sku: dict) -> str | None:
    """
    Get the shade name for a SKU. Prefers `displayName` (format
    "{skuId} {shade name}"); falls back to parsing alternateImages[0]
    .altText (format "Brand Product in SHADE Image N") if displayName
    is missing. Note: skuImages.altText follows a different format
    ("Brand - Product SHADE SIZE Product Badge") that does NOT contain
    " in " and cannot be used as a shade-name fallback source.
    """
    display_name = sku.get("displayName")
    sku_id = str(sku.get("skuId", ""))
    if display_name and sku_id and display_name.startswith(sku_id):
        shade = display_name[len(sku_id):].strip()
        if shade:
            return shade

    alternate_images = sku.get("alternateImages", [])
    alt_text = alternate_images[0].get("altText", "") if alternate_images else ""
    if alt_text and " in " in alt_text:
        shade = alt_text.split(" in ", 1)[1]
        return re.sub(r"\s+Image\s+\d+$", "", shade).strip() or None

    return None


def _parse_sku(sku: dict) -> dict:
    swatch = sku.get("skuImages", {})
    sku_id = sku.get("skuId")

    return {
        "sku_id": sku_id,
        "shade_name": extract_shade_name(sku),
        "list_price": sku.get("listPrice"),
        "sale_price": sku.get("salePrice"),
        "in_stock": sku.get("isEligible", False),
        "is_final_sale": sku.get("isFinalSale", False),
        "badge": sku.get("badgeAltText"),
        "shade_img_url": swatch.get("imageUrl"),
        "swatch_alt": swatch.get("altText") or None,
        "color_img_url": f"https://www.sephora.com/productimages/sku/s{sku_id}+sw.jpg" if sku_id else None, # color of the shades
    }


def fetch_shades(session: requests.Session, product_id: str, default_sku_id: str) -> list[dict]:
    """Return every shade (name, size, price, stock, swatch image) for a product."""
    url = f"{BASE_URL}{SKU_API_PATH.format(product_id=product_id)}"
    params = {"preferedSku": default_sku_id, "countryCode": "US", "loc": "EN-US"}

    try:
        response = session.get(url, params=params, headers=HEADERS_API, timeout=10)
        response.encoding = "utf-8"
        response.raise_for_status()
        data = response.json()
    except RequestException:
        return []

    seen_sku_ids = set()
    shades = []

    if current := data.get("currentSku"):
        shades.append(_parse_sku(current))
        seen_sku_ids.add(current.get("skuId"))

    for child in data.get("regularChildSkus", []):
        # currentSku duplicates one entry in regularChildSkus (it's just
        # whichever shade the page loaded with selected) — skip it here.
        if child.get("skuId") in seen_sku_ids:
            continue
        shades.append(_parse_sku(child))
        seen_sku_ids.add(child.get("skuId"))

    return shades