import sys, os, re

import pandas as pd
import numpy as np

from datetime import datetime

from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from encoding import fix_mojibake_in_dataframe
from io_utils import read_json_utf8, write_csv_utf8
from cleaning.missing_values import print_missing_analysis, comprehensive_missing_analysis # cleaning. when running run.py

PRODUCT_COLUMNS = [
    "product_id", "brand", "product_name", "product_url",
    "short_description", "long_description", "how_to_use",
    "ingredients", "loves_count", "hero_image_url", "size", 
]

SHADE_COLUMNS = [
    "sku_id", "product_id", "shade_name", "list_price", "sale_price",
    "in_stock", "is_final_sale", "badge", "shade_img_url", "color_img_url",
]

LEGACY_SHADE_COLUMN_ALIASES = {
    "image_url": "shade_img_url",
}

UNIT_COLUMNS = ["oz_value", "g_value", "ml_value", "fl_oz_value"]


# loading json file called "blush_detailed.json" and returns it as a JSON list of dict
def load_raw(filename: str ="bronzer-makeup_detailed.json") -> list[dict]:
    return read_json_utf8(RAW_DATA_DIR / filename)

def build_products_table(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records) # turns the readed JSON list into DataFrame
    for col in PRODUCT_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df[PRODUCT_COLUMNS].drop_duplicates(subset="product_id")

## Flattening/Denormalizing `shades`
def build_shades_table(records: list[dict]) -> pd.DataFrame:
    rows = []
    for record in records:
        ## Looking for "shades" keys
        for shade in record.get("shades", []): # .get() if a product is missing the "shades" keys, it returns an empty list instead of crashing
            rows.append({**shade, "product_id": record.get("product_id")}) # ** takes all the key-value pairs inside "shades" dict and flatten them out
            ## then add "product_id" to the dict to track which shade belongs to which product_id
    df = pd.DataFrame(rows)
    df = df.rename(columns=LEGACY_SHADE_COLUMN_ALIASES)

    for col in SHADE_COLUMNS:
        if col not in df.columns:
            df[col] = None
            
    return df[SHADE_COLUMNS]

def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = fix_mojibake_in_dataframe(df)
    df = df.drop_duplicates(subset="product_id")
    print(f"Missing Percentage: {(df.isnull().sum().sum() / df.size) * 100:.2f}%")
    print(f"Columns with missing values: {df.columns[df.isnull().any()].tolist()}")
    return df

def clean_shades(df: pd.DataFrame) -> pd.DataFrame:
    df = fix_mojibake_in_dataframe(df) # fixing mofibake encoding exist in df

    ## Convert list_price and sale_price from string into numeric
    for column in ['list_price','sale_price']:
        df[column] = pd.to_numeric(
            df[column]
            .astype("string")
            .str.replace(r"[$,]", "", regex=True)
            .str.strip(),
            errors="coerce",
        )


    # df = df.drop_duplicates(subset="sku_id") # fix the problem with only clean the first shade of each product
    df = df.drop_duplicates(
            subset=["product_id", "sku_id"]
        ).reset_index(drop=True)
    return df

## Handling Size strings
def parse_size_units(size_str) -> pd.Series:
    if pd.isna(size_str): # check for missing values
        return pd.Series([np.nan]*4, index=UNIT_COLUMNS) # when the original spot is null, then all 4 cells are also null
    
    oz_val = g_val = ml_val = fl_oz_val = np.nan

    normalized = re.sub(r"fl\.?\s*oz", "fl_oz", str(size_str).lower().strip())

    for part in normalized.split("/"):
        for value_str, unit in re.findall(r"(\d*\.?\d+)\s*(oz|g|ml|fl_oz)\b", part):
            try:
                value = float(value_str)
            except ValueError:
                continue
            if unit == "oz" and pd.isna(oz_val):
                oz_val = value
            elif unit == "g" and pd.isna(g_val):
                g_val = value
            elif unit == "ml" and pd.isna(ml_val):
                ml_val = value
            elif unit == "fl_oz" and pd.isna(fl_oz_val):
                fl_oz_val = value
                
    return pd.Series([oz_val, g_val, ml_val, fl_oz_val], index=UNIT_COLUMNS)

def add_unit_columns(df: pd.DataFrame, size_column: str = "size") -> pd.DataFrame:
    """Add oz_value / g_value / ml_value / fl_oz_value columns derived from `size_column`."""
    df = df.copy()
    df[UNIT_COLUMNS] = df[size_column].apply(parse_size_units)
    # df.drop("size", axis=1, inplace=True) # size, axis = 1: column, inplace
    return df

def validate_tables(products, shades):
    problems = [] # tracking the problems of the products and shades datasets

    if products["product_id"].isna().any():
        problems.append("Products contain missing product_id values")

    if products["product_id"].duplicated().any():
        problems.append("Products contain duplicate product_id values")

    if shades["sku_id"].isna().any():
        problems.append("Shades contain missing sku_id values")

    if shades["sku_id"].duplicated().any():
        problems.append("Shades contain duplicate sku_id values")

    orphan_ids = set(shades["product_id"]) - set(products["product_id"])
    if orphan_ids:
        problems.append(
            f"Shades reference {len(orphan_ids)} unknown products"
        )

    if problems:
        raise ValueError("\n".join(problems))

    print("Validation passed")

def run_cleaning_pipeline(raw_filename: str = "bronzer-makeup_detailed.json") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load raw JSON, clean, and write products.csv + shades.csv. Returns both DataFrames."""
    records = load_raw(raw_filename) # load dataset
    # print(f"Loading file: {raw_filename}")
    
    products = clean_products(build_products_table(records)) # Create, flatten, and clean products table
    shades = clean_shades(build_shades_table(records)) # Create, flatten, and clean shades table
    
    products = add_unit_columns(products, size_column="size") # Handling the products size and add new columns
    

    print_missing_analysis(comprehensive_missing_analysis(products), title="PRODUCT MISSING-VALUE REPORT") # missing values report
    print_missing_analysis(comprehensive_missing_analysis(shades), title="SHADE MISSING-VALUE REPORT") # missing values report

    unparsed_size = products[
        products["size"].notna()
        & products[UNIT_COLUMNS].isna().all(axis=1)
    ]

    print(f"Unparsed size values: {len(unparsed_size)}")


    category = raw_filename.replace("_detailed.json", "")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # year/month/date_hour/minute/second

    validate_tables(products, shades) # Checking what kind of problems do each dataset have

    write_csv_utf8(products, PROCESSED_DATA_DIR / f"{category}_products_{timestamp}.csv")
    write_csv_utf8(shades, PROCESSED_DATA_DIR / f"{category}_shades_{timestamp}.csv")

    print(f"Saved: {f"{category}_products_{timestamp}.csv"} ({len(products)} rows)")
    print(f"Saved: {f"{category}_shades_{timestamp}.csv"} ({len(shades)} rows)")

    return products, shades

if __name__ == "__main__":
    # run_cleaning_pipeline() # compiled via run.py

    # ONLY runs when execute this file directly and COMPLETELY IGNORE when run.py imports it
    user_input = input("Enter Category (press Enter for default 'bronzer-makeup'): ").strip()
    if user_input:
        target_file = f"{user_input}_detailed.json"
    else:
        target_file = "blush_detailed.json"

    run_cleaning_pipeline(raw_filename=target_file)