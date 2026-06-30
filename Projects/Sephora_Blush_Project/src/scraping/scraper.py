from __future__ import annotations

import random, time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import BASE_URL, HEADERS_HTML, MAX_CONCURRENT_REQUESTS, RAW_DATA_DIR

from io_utils import write_json_utf8
from scraping.http import build_session
from scraping.product_detail import fetch_product_detail
from scraping.listing import fetch_all_products, parse_listing_product
from scraping.shades import fetch_shades

def _warm_up(session) -> None:
    try:
        session.get(BASE_URL, headers=HEADERS_HTML, timeout=10)
    except Exception:
        pass

def _scrape_one(base_record: dict) -> dict:
    session = build_session()
    time.sleep(random.uniform(0.3, 0.9))
    _warm_up(session)

    detail = fetch_product_detail(session, base_record["target_url"], base_record["sku_id"])

    if detail.get("_error") == "403 blocked":
        time.sleep(random.uniform(3.0, 6.0))
        retry_session = build_session()
        _warm_up(retry_session)
        detail = fetch_product_detail(retry_session, base_record["target_url"], base_record["sku_id"])

    shades = fetch_shades(session, base_record["product_id"], base_record["sku_id"])
    return {**base_record, **detail, "shades": shades}


def scrape_category(
    category: str = "blush",
    limit: int | None = None,
    max_workers: int = MAX_CONCURRENT_REQUESTS,
    checkpoint_every: int = 25,
) -> list[dict]:
    """
    Full pipeline: listing -> (detail + shades, in parallel) -> records.

    Parameters
    ----------
    limit: cap the number of products processed (useful for test runs).
    max_workers: how many products to enrich concurrently.
    checkpoint_every: write a JSON checkpoint to data/raw every N completions,
        so a crash partway through doesn't lose all progress.
    """
    print(f"Fetching '{category}' listing...")
    listing = fetch_all_products(category=category)
    base_records = [parse_listing_product(p) for p in listing]
    if limit:
        base_records = base_records[:limit]
    print(f"  {len(base_records)} products to enrich (max_workers={max_workers})")

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_scrape_one, rec): rec for rec in base_records}
        for i, future in enumerate(as_completed(futures), 1):
            base_record = futures[future]
            try:
                results.append(future.result())
            except Exception as e:
                print(f"  [{i}/{len(base_records)}] FAILED {base_record.get('product_name')}: {e}")
                continue

            if i % 10 == 0 or i == len(base_records):
                print(f"  [{i}/{len(base_records)}] done")

            if checkpoint_every and i % checkpoint_every == 0:
                checkpoint_path = RAW_DATA_DIR / f"{category}_checkpoint_{i}.json"
                write_json_utf8(results, checkpoint_path)

    final_path = RAW_DATA_DIR / f"{category}_detailed.json"
    write_json_utf8(results, final_path)
    print(f"Saved {len(results)} products -> {final_path}")
    return results


if __name__ == "__main__":
    scrape_category(category="blush", limit=5)  # small test run; raise/remove limit for full scrape