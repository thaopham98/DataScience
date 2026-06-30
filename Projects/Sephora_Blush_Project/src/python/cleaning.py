"""
Data Cleaning for scraped JSONs from sephora.com

Transforming nested product JSON into three normalized flat tables:
 1. products     — one row per product (brand, name, description, etc.)
 2. skus         — one row per shade variant (shade name, price, size, unit values)
 3. sku_details  — one row per SKU with extracted text fields
                    (ingredients, finish, coverage, formulation, callouts)
"""

import re, json, os, argparse
import pandas as pd

RE_FINISH = re.compile(
    r"(?i)finish\s*:\s*([\w\s/-]+?)(?=\s*\.|$|\s*<br|\s*\n)",
)
RE_COVERAGE = re.compile(
    r"(?i)coverage\s*:\s*([\w\s/-]+?)(?=\s*\.|$|\s*<br|\s*\n)",
)
RE_FORMULATION = re.compile(
    r"(?i)formulation\s*:\s*([\w\s/-]+?)(?=\s*\.|$|\s*<br|\s*\n)",
)
RE_INGREDIENT_CALLOUTS = re.compile(
    r"(?i)(?:free of|formulated without|without)[\s:]+(.+?)(?:\s*[•·-]|\s*<br|\s*\n|$)",
)
RE_CLEAN_AT_SEPHORA = re.compile(
    r"(?i)(clean at sephora)",
)
RE_HIGHLIGHTED = re.compile(
    r"(?i)(?:key ingredients|star ingredients|highlighted ingredients?)[\s:]+(.+?)(?:\s*[•·-]|\s*<br|\s*\n|$)",
)
RE_CLINICAL = re.compile(
    r"(?i)(?:clinical results?|proven results?)[\s:]+(.+?)(?:\s*[•·-]|\s*<br|\s*\n|$)",
)

def _extract_finish(text: str) -> tuple[str | None, str | None]:
    """Extract finish type from a description string. Returns (finish, source)."""
    if not isinstance(text, str):
        return None, None
    m = RE_FINISH.search(text)
    if m:
        return m.group(1).strip().rstrip("."), "long_description"
    return None, None

def _extract_coverage(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = RE_COVERAGE.search(text)
    return m.group(1).strip().rstrip(".") if m else None

def _extract_formulation(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = RE_FORMULATION.search(text)
    return m.group(1).strip().rstrip(".") if m else None

def _extract_ingredient_callouts(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = RE_INGREDIENT_CALLOUTS.search(text)
    return m.group(1).strip().rstrip(".") if m else None

def _extract_clean_at_sephora(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    return "Clean at Sephora" if RE_CLEAN_AT_SEPHORA.search(text) else None

def _extract_highlighted_ingredients(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = RE_HIGHLIGHTED.search(text)
    return m.group(1).strip().rstrip(".") if m else None

def _extract_clinical_results(text: str) -> str | None:
    if not isinstance(text, str):
        return None
    m = RE_CLINICAL.search(text)
    return m.group(1).strip().rstrip(".") if m else None

def _parse_size(size_str: str | None) -> dict[str, float | None]:
    result = {"oz_value": None, "g_value": None, "ml_value": None, "fl_oz_value": None}
    if not isinstance(size_str, str):
        return result

    size_str = size_str.lower().replace("/", " ").replace(",", "")

    oz_match = re.search(r"(\d+\.?\d*)\s*oz", size_str)
    g_match = re.search(r"(\d+\.?\d*)\s*g(?:\s|$)", size_str)
    ml_match = re.search(r"(\d+\.?\d*)\s*ml", size_str)
    fl_oz_match = re.search(r"(\d+\.?\d*)\s*fl\s*oz", size_str)

    if oz_match:
        result["oz_value"] = float(oz_match.group(1))
    if g_match:
        result["g_value"] = float(g_match.group(1))
    if ml_match:
        result["ml_value"] = float(ml_match.group(1))
    if fl_oz_match:
        result["fl_oz_value"] = float(fl_oz_match.group(1))

    return result

def extract_products_table(data: list[dict]) -> pd.DataFrame:
    """One row per product with top-level fields."""
    rows = []
    for p in data:
        rows.append({
            "product_id":               p.get("product_id"),
            "brand":                    p.get("brand"),
            "display_name":             p.get("name"),
            "brand_id":                 None,
            "target_url":               p.get("product_url"),
            "short_description":        p.get("short_description"),
            "long_description":         p.get("long_description"),
            "how_to_use":               p.get("how_to_use"),
            "what_it_is":               p.get("short_description"),
            "what_else_you_need_to_know": None,
            "loves_count":              p.get("loves_count"),
            "hero_image_url":           p.get("hero_image_url"),
            "rating":                   p.get("rating"),
            "reviews":                  p.get("reviews"),
            "is_bestseller":            p.get("is_bestseller"),
            "is_new":                   p.get("is_new"),
            "is_sephora_exclusive":     p.get("is_sephora_exclusive"),
            "is_limited_edition":       p.get("is_limited_edition"),
            "is_online_only":           p.get("is_online_only"),
            "is_discontinued":          p.get("is_discontinued"),
            "sponsored":                p.get("sponsored"),
            "sku_type":                 p.get("sku_type"),
            "scraped_at":               p.get("scraped_at"),
        })
    return pd.DataFrame(rows)

def extract_skus_table(data: list[dict]) -> pd.DataFrame:
    """One row per shade/SKU variant."""
    rows = []
    for p in data:
        product_id = p.get("product_id")
        shades = p.get("shades", [])
        for s in shades:
            size_str = s.get("size") or p.get("size")
            parsed = _parse_size(size_str)
            list_price_str = s.get("list_price", "0")
            try:
                list_price = float(re.sub(r"[^\d.]", "", str(list_price_str)))
            except (ValueError, TypeError):
                list_price = 0.0

            sale_price_str = s.get("sale_price")
            sale_price = None
            if sale_price_str:
                try:
                    sale_price = float(re.sub(r"[^\d.]", "", str(sale_price_str)))
                except (ValueError, TypeError):
                    pass

            rows.append({
                "sku_id":      s.get("sku_id"),
                "product_id":  product_id,
                "shade_name":  s.get("shade_name"),
                "list_price":  list_price,
                "sale_price":  sale_price,
                "size":        size_str,
                "oz_value":    parsed["oz_value"],
                "g_value":     parsed["g_value"],
                "ml_value":    parsed["ml_value"],
                "fl_oz_value": parsed["fl_oz_value"],
                "badge":       s.get("badge"),
                "in_stock":    s.get("in_stock"),
                "image_url":   s.get("image_url"),
            })
    return pd.DataFrame(rows)

def extract_sku_details_table(data: list[dict]) -> pd.DataFrame:
    """One row per SKU with parsed text fields (finish, coverage, etc.)."""
    rows = []
    for p in data:
        product_id = p.get("product_id")
        long_desc = p.get("long_description", "")
        shades = p.get("shades", [])

        finish_val, finish_src = _extract_finish(long_desc)
        coverage_val = _extract_coverage(long_desc)
        formulation_val = _extract_formulation(long_desc)
        callouts = _extract_ingredient_callouts(long_desc)
        clean = _extract_clean_at_sephora(long_desc)
        highlighted = _extract_highlighted_ingredients(long_desc)
        clinical = _extract_clinical_results(long_desc)

        for s in shades:
            rows.append({
                "sku_id":                   s.get("sku_id"),
                "product_id":               product_id,
                "ingredients":              p.get("ingredients"),
                "highlighted_ingredients":  highlighted,
                "ingredient_callouts":      callouts,
                "clinical_results":         clinical,
                "clean_at_sephora":         clean,
                "coverage":                 coverage_val,
                "finish":                   finish_val,
                "formulation":              formulation_val,
                "finish_source":            finish_src,
                "needs_review":             finish_val is None,
            })
    return pd.DataFrame(rows)

def compute_price_per_unit(skus_df: pd.DataFrame) -> pd.DataFrame:
    """Compute price-per-oz and price-per-g for each SKU."""
    df = skus_df.copy()

    mask_oz = df["oz_value"].notna() & (df["oz_value"] > 0)
    df["price_per_oz"] = None
    df.loc[mask_oz, "price_per_oz"] = (
        df.loc[mask_oz, "list_price"] / df.loc[mask_oz, "oz_value"]
    )

    mask_g = df["g_value"].notna() & (df["g_value"] > 0)
    df["price_per_g"] = None
    df.loc[mask_g, "price_per_g"] = (
        df.loc[mask_g, "list_price"] / df.loc[mask_g, "g_value"]
    )

    return df

def main():
    parser = argparse.ArgumentParser(
        description="Sephora product pipeline: clean + export"
    )
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--processed-dir", default="data/processed")

    args = parser.parse_args()

    # Load the data
    file_path = r"..\..\data\raw\sephora_blush_20260625_005925.json"
    processed_dir = r"..\..\data\processed"

    print(f"Loading: {file_path}")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(processed_dir, exist_ok=True)

    # Extract tables
    products_df = extract_products_table(data)
    skus_df = extract_skus_table(data)
    sku_details_df = extract_sku_details_table(data)

    # Save to CSV
    products_df.to_csv(os.path.join(processed_dir, "products.csv"), index=False)
    skus_df.to_csv(os.path.join(processed_dir, "skus.csv"), index=False)
    sku_details_df.to_csv(os.path.join(processed_dir, "sku_details.csv"), index=False)

    # Compute prices
    price_df = compute_price_per_unit(skus_df)
    price_df.to_csv(os.path.join(processed_dir, "price_per_unit.csv"), index=False)

    print(f"✅ Done! Files saved to {processed_dir}")

if __name__ == "__main__":
    main()