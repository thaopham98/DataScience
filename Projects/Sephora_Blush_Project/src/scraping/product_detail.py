from __future__ import annotations

import json, re

from curl_cffi import requests
from curl_cffi.requests.exceptions import RequestException
from bs4 import BeautifulSoup

from config import BASE_URL, HEADERS_HTML

EMPTY_DETAIL = {
    "short_description": None,
    "long_description": None,
    "how_to_use": None,
    "loves_count": None,
    "ingredients": None,
    "size": None,
}


def strip_html(html_str: str | None) -> str | None:
    """Strip HTML tags, collapse whitespace, return clean plain text."""
    if not html_str:
        return None
    text = BeautifulSoup(html_str, "html.parser").get_text(separator=" ").strip()
    return re.sub(r"\s{2,}", " ", text) or None


def fetch_product_detail(session: requests.Session, target_url: str, sku_id: str) -> dict:
    """Fetch one product page and extract the linkStore detail fields."""
    url = f"{BASE_URL}{target_url}"
    if "skuId" not in url:
        url += f"?skuId={sku_id}"

    try:
        response = session.get(url, headers=HEADERS_HTML, timeout=15)
        response.encoding = "utf-8"
        if response.status_code == 403:
            return {**EMPTY_DETAIL, "_error": "403 blocked"}
        response.raise_for_status()
    except RequestException as e:
        return {**EMPTY_DETAIL, "_error": str(e)}

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", {"id": "linkStore", "type": "text/json"})
    if not (script_tag and script_tag.string):
        return {**EMPTY_DETAIL, "_error": "linkStore not found"}

    try:
        data = json.loads(script_tag.string)
        product = data.get("page", {}).get("product", {})
        details = product.get("productDetails", {})
        current_sku = product.get("currentSku", {})

        return {
            "short_description": strip_html(product.get("quickLookDescription")),
            "long_description": strip_html(details.get("longDescription")),
            "how_to_use": strip_html(details.get("suggestedUsage")),
            "loves_count": details.get("lovesCount"),
            "ingredients": strip_html(current_sku.get("ingredientDesc")),
            "size": current_sku.get("size"),
        }
    except (json.JSONDecodeError, AttributeError) as e:
        return {**EMPTY_DETAIL, "_error": f"linkStore parse error: {e}"}