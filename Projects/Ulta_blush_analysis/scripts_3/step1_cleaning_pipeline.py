"""
cleaning_pipeline.py
====================
Single-file cleaning pipeline for the Ulta blush dataset.
"""

import re, os
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
# PATHS (Using relative-path protection)
# ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
INPUT_PATH  = os.path.abspath(os.path.join(SCRIPT_DIR, "../raw_data/ulta_clean_blush.csv"))
OUTPUT_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "../clean_data/ulta_clean_blush_v1_claude.csv"))


# ══════════════════════════════════════════════════════════════════
# STEP 1 — LOAD
# ══════════════════════════════════════════════════════════════════
def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"[load] {len(df)} rows, {len(df.columns)} columns")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 2 — FIX ENCODING
# ══════════════════════════════════════════════════════════════════
def power_clean(text):
    if not isinstance(text, str):
        return text
    
    # 1. Target specific "Futurist" messes
    text = re.sub(r'Ã[Â\x82\xa0\x82]+', ' ', text)
    text = re.sub(r'Â', '', text)
    
    # 2. Target standard Mojibake character corruptions
    text = text.replace('ÃƒÂ©', 'é').replace('ÃƒÂ', 'à').replace('NÃ‚°', 'N°')
    
    # ─────────────────────────────────────────────────────────
    # THE FIX: Target both the raw hidden bytes (\x80\x99) 
    # AND the editor-converted symbols (€™)
    # ─────────────────────────────────────────────────────────
    text = re.sub(r'Ã¢[\x80€][\x99™]', "'", text) 
    
    # 3. Clean up the literal low-comma glitch variations
    text = re.sub(r'Ã[‚\x82\x80-\x9f‚]+', ' ', text)
    text = re.sub(r'[‚‚]', '', text)
    text = text.replace('\xa0', ' ')
    
    # 4. Standardize and strip spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Amp’d Up Apple : AmpÃ¢d Up Apple

def fix_encoding(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['product_name', 'swatch_alt', 'shade', 'description']:
        if col in df.columns:
            df[col] = df[col].apply(power_clean)

    if 'brand' in df.columns:
        df.loc[df['brand'].str.contains('Ã', na=False), 'brand'] = 'PÜR Minerals'

    print("[fix_encoding] Encoding repaired on product_name, swatch_alt, shade, brand")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 3 — DROP COLUMNS (Cleaned up logic)
# ══════════════════════════════════════════════════════════════════
def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Only target currency here. 'size' is handled dynamically in Step 5.
    existing = [c for c in ['currency'] if c in df.columns]
    df = df.drop(columns=existing)
    print(f"[drop_columns] Dropped: {existing}")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 4 — FILL MISSING SIZE VALUES
# ══════════════════════════════════════════════════════════════════
SIZE_MAP_METRIC = {
    '22 g':   ['Marble Cream Blush Stick'],
    '21 g':   ['Ultimate Blush Palette'],
    '16.8 g': ['Blushed Duo'],
    '12 g':   ['Blursh Pod Domed Blusher '],
    '10 g':   ['MegaGlo Blushlighter'],
    '9 g':    ['DreamStick Cream Blush'],
    '8.5 g':  ['Cream Stick Blush with Brush Applicator', 'Blush Crush Liquid Blush'],
    '8.4 g':  ['Effervescence Extra Dimension Face Compact'],
    '8.2 g':  ['Juice Stick Dewy Gel-Cream Blush'],
    '7.7 g':  ['Blushed Liquid Blushlighter'],
    '7.5 g':  ['Glow Time Blush Stick'],
    '6 g':    ['Blushed Cream Blush', 'Matte Blush', 'Megaglo Makeup Stick',
               "I'm Blushing 2-in-1 Cheek and Lip Tint", 'Heart Pressed Powder Blush'],
    '5.5 g':  ['Blusher Reloaded', 'Jelly Blush Stick Lip & Cheek Stain',
               'Baby Got Blush', 'Bouncy Blur Blush'],
    '5 g':    ['2-in-1 Mosaic Blush & Bronzer Powder', 'Liquid Blush - 2-in-1 Lip & Cheek Tint',
               "Strawberry Rococo Series Embossed Blush"], 
    '4.5 g':  ['Blush-Mallow Soft Blusher', 'Skin Silk Marble Blush Stick'],
    '3.2 g':  ['PurePressed Blush'],
    '3 g':    ['Magic Touch Cream Blush & Lip Trio', 'Just Kissed Lip and Cheek Stain'],
    '2.5 g':  ['Baked Blush'],
    '15 ml':  ['Hot Shot Blush Drops', "Tinted Moisturizer Cream Blush"],
    '10 ml':  ['Futurist Blushmaker Dewy Cheek Tint Liquid Blush', 'Superdewy Liquid Blush Burst'],
    '9.5 ml': ['Glimmer Blush Drops'],
    '8.5 ml': ['Skin Idôle Juicy Liquid Blush'],
    '8 ml':   ['Maneater Satin Blush Cheek Plump'],
    '6 ml':   ['Play Daze Airy Liquid Blush', 'Play Daze Airy Soft Matte Liquid Blush'],
    '3.9 ml': ['Jelly Tint - 2-in-1 Lip & Cheek Tint Stain'],
    '3.5 ml': ['Blush Rush Liquid Blush'],
    
    # '4.25 g': ["Stila", "Convertible Color Lip & Cheek Cream Blush"],
    # '5 g':    ["Flower Knows", "Strawberry Rococo Series Embossed Blush"],
    # '15 ml':  ["Laura Mercier", "Tinted Moisturizer Cream Blush"],
    # '10.3 ml':["HOURGLASS", "Unreal Liquid Blush"],
    # '4 g':    ["LORAC", "Color Source Buildable Blush"],

    '4.25 g': ["Convertible Color Lip & Cheek Cream Blush"],
    '10.3 ml':["Unreal Liquid Blush"],
    '4 g':    ["Color Source Buildable Blush"],
    '7.8 g': ["Macaron Blush & Glow Duo"],    
}

## Inverted to support composite keys: {(brand, product_name): size}
_SIZE_LOOKUP = {
    product.strip(): size
    for size, products in SIZE_MAP_METRIC.items()
    for product in products

    # ## Update 
    # (brand.strip().lower(), product.strip().lower()): size 
    # for size, products in SIZE_MAP_METRIC.items()
    # for brand, product in products
}

def fill_missing_size(df: pd.DataFrame) -> pd.DataFrame:
    # before = df['size'].isnull().sum()
    # df['size'] = df['size'].fillna(df['product_name'].str.strip().map(_SIZE_LOOKUP))
    # after = df['size'].isnull().sum()
    # print(f"[fill_missing_size] Filled {before - after} rows  |  Still missing: {after}")
    # return df

    ## Fixing V1
    # Clean string spaces to match dictionary keys
    clean_prod_names = df['product_name'].str.strip()
    
    # Check which items are tracked in your dictionary
    is_tracked = clean_prod_names.isin(_SIZE_LOOKUP.keys())
    
    # OVERWRITE matching products to make them perfectly uniform
    df.loc[is_tracked, 'size'] = clean_prod_names.map(_SIZE_LOOKUP)
    
    # For any leftovers NOT in your map, keep original values or let them stay NaN
    print(f"[fill_missing_size] Unified sizes based on custom dictionary map.")
    return df

    # ## Fixing V2
    # # Create matching tuples of lowercased (brand, product_name) to avoid case mismatches
    # composite_keys = list(zip(
    #     df['brand'].str.strip().str.lower(),
    #     df['product_name'].str.strip().str.lower()
    # ))
    
    # # Map the composite keys using our updated dictionary lookup
    # mapped_sizes = pd.Series(composite_keys, index=df.index).map(_SIZE_LOOKUP)
    
    # # Identify which products exist in your hardcoded dictionary
    # is_tracked = mapped_sizes.notna()
    
    # # Option 1: Force overwrite anything tracked to ensure brand-wide consistency
    # df.loc[is_tracked, 'size'] = mapped_sizes[is_tracked]
    
    # print(f"[fill_missing_size] Unified sizes using unique Brand + Product name keys.")
    # return df


# ══════════════════════════════════════════════════════════════════
# STEP 5 — PARSE & STANDARDIZE `size`
# ══════════════════════════════════════════════════════════════════
def _parse_one(size_str):
    if pd.isna(size_str):
        return pd.Series([np.nan, np.nan], index=['standard_value', 'standard_unit'])

    s = str(size_str).lower().strip()
    if s == '0.5':
        s = '0.5 oz'

    s = re.sub(r'fl\.?\s*oz', 'fl_oz', s)
    matches = re.findall(r'(\d*\.?\d+)\s*([a-z_]+)\b', s)
    extracted = {unit: float(val) for val, unit in matches}

    if 'g' in extracted:
        return pd.Series([extracted['g'], 'g'], index=['standard_value', 'standard_unit'])
    if 'ml' in extracted:
        return pd.Series([extracted['ml'], 'ml'], index=['standard_value', 'standard_unit'])
    if 'oz' in extracted:
        return pd.Series([round(extracted['oz'] * 28.3495, 2), 'g'], index=['standard_value', 'standard_unit'])
    if 'fl_oz' in extracted:
        return pd.Series([round(extracted['fl_oz'] * 29.5735, 2), 'ml'], index=['standard_value', 'standard_unit'])
    
    if extracted:
        odd_unit = next(iter(extracted))
        return pd.Series([extracted[odd_unit], odd_unit], index=['standard_value', 'standard_unit'])

    return pd.Series([np.nan, np.nan], index=['standard_value', 'standard_unit'])


def parse_size(df: pd.DataFrame) -> pd.DataFrame:
    df[['standard_value', 'standard_unit']] = df['size'].apply(_parse_one)

    ct_mask = df['standard_unit'] == 'ct'
    if ct_mask.any():
        df.loc[ct_mask, 'standard_value'] = (df.loc[ct_mask, 'standard_value'] * 28.3495).round(2)
        df.loc[ct_mask, 'standard_unit'] = 'g'
        print(f"[parse_size] Fixed {ct_mask.sum()} 'ct' rows → converted to grams")

    df = df.drop(columns=['size'])
    print(f"[parse_size] standard_value range: {df['standard_value'].min()} – {df['standard_value'].max()}")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 6 — EXTRACT IDs AND BUILD PRODUCT IMAGE URL
# ══════════════════════════════════════════════════════════════════
_IMG_BASE   = "https://media.ulta.com/i/ulta/"
_IMG_SUFFIX = "?w=1080&h=1080&fmt=auto"


def extract_ids_and_image_url(df: pd.DataFrame) -> pd.DataFrame:
    df['product_id'] = df['shade_url'].str.extract(r'(?:rod|mkt|VP)(\d+)')
    df['shade_id']   = df['shade_url'].str.extract(r'sku=(\d+)')

    # Essential clean: Drop rows where both product_id and shade_id extraction completely fail
    # This keeps your output from carrying corrupted string remnants into SQL
    df = df.dropna(subset=['product_id', 'shade_id'])

    df['product_image_url'] = df['shade_id'].apply(
        lambda x: f"{_IMG_BASE}{x}{_IMG_SUFFIX}" if pd.notna(x) else None
    )

    # Cast to string safely to avoid losing leading zeroes while stripping trailing whitespaces
    df['product_id'] = df['product_id'].astype(str).str.strip()
    df['shade_id']   = df['shade_id'].astype(str).str.strip()

    print(f"[extract_ids] Cleaned unique IDs. Rows retained: {len(df)}")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 7 — FINAL COLUMN ORDER
# ══════════════════════════════════════════════════════════════════
FINAL_COLUMNS = [
    'shade_url',
    'brand',
    'product_name',
    'shade',
    'swatch_img_url',
    'swatch_alt',
    'description',
    'price',
    'standard_value',
    'standard_unit',
    'product_id',
    'shade_id',
    'product_image_url',
]


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    present = [c for c in FINAL_COLUMNS if c in df.columns]
    df = df[present]
    print(f"[reorder_columns] Schema locked to final layout. Shape: {df.shape}")
    return df


# ══════════════════════════════════════════════════════════════════
# STEP 8 — SAVE
# ══════════════════════════════════════════════════════════════════
def save(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, encoding='utf-8-sig', index=False)
    print(f"[save] Written to {path}")

# ══════════════════════════════════════════════════════════════════
# STEP 9 — VERIFY (NEW)
# ══════════════════════════════════════════════════════════════════
def verify_size_consistency(df: pd.DataFrame) -> bool:
    """
    Validates that every unique Brand + Product Name combination has exactly 
    ONE unique combination of standard_value and standard_unit across the dataset.
    """
    print("\n" + "="*55)
    print("  Pipeline Verification: Brand + Product Size Consistency Check")
    print("=" * 55)
    
    # Group by both brand and product name, counting unique values and units (including NaNs)
    consistency_check = df.groupby(['brand', 'product_name'])[['standard_value', 'standard_unit']].nunique(dropna=False)
    
    # Flag rows where a single brand's product has multiple distinct sizes across shades
    violators = consistency_check[(consistency_check['standard_value'] > 1) | (consistency_check['standard_unit'] > 1)]
    
    if violators.empty:
        print("✅ SUCCESS: All products are 100% size-consistent within their brands!")
        print(f"Total Brand-Product Combinations Validated: {len(consistency_check)}")
        print("="*55 + "\n")
        return True
    else:
        print(f"❌ FAILURE: Found {len(violators)} unique product(s) with size discrepancies!\n")
        print("Detailed Breakdown of Conflicts:")
        print("-" * 55)
        
        # Display the explicit rows where a brand's product has conflicting sizes
        for brand, prod_name in violators.index:
            print(f"\nBrand: '{brand}' | Product: '{prod_name}'")
            mismatched_rows = df[(df['brand'] == brand) & (df['product_name'] == prod_name)][
                ['shade', 'standard_value', 'standard_unit']
            ].drop_duplicates()
            print(mismatched_rows.to_string(index=False))
            
        print("\n" + "="*55 + "\n")
        return False

# ══════════════════════════════════════════════════════════════════
# MAIN PIPELINE RUNNER
# ══════════════════════════════════════════════════════════════════
def run_pipeline(input_path: str = INPUT_PATH, output_path: str = OUTPUT_PATH) -> pd.DataFrame:
    print("=" * 55)
    print("  Ulta Blush — Integrated Data Cleaning Pipeline")
    print("=" * 55)

    df = load(input_path)
    df = fix_encoding(df)
    df = drop_columns(df)


    df = fill_missing_size(df)

    df = parse_size(df)
    df = extract_ids_and_image_url(df)
    df = reorder_columns(df)

    pipeline_passed = verify_size_consistency(df) # Step 9 (new)
    if not pipeline_passed:
        print("⚠️ Warning: Data saved, but contains data-entry/mapping discrepancies. See log above.")

    save(df, output_path) # Step 8

    print("=" * 55)
    print("  Data pipeline executed successfully.")
    print("=" * 55)
    return df


if __name__ == "__main__":
    run_pipeline()

# # --- QUICK TEST VERIFICATION ---

# # Create a small sample dataframe matching your layout (All arrays must be length 3!)
# test_df = pd.DataFrame({
#     'product_name': ['Glow Time Blush Stick', 'Liquid Blush', 'Powder Blush'],
#     'description': [
#         'A beautiful shade of apricotÃ‚‚',     # The exact glitch you hit
#         'Soft pink finishÃ‚   ',               # Glitch with trailing spaces
#         'Fresh peach tone'                    # Clean string to ensure no text gets broken
#     ],
#     # Padded with two empty strings so the length is 3
#     'swatch_alt': ["AmpÃ¢€™d Up Apple", "", ""] 
# })

# print("Before cleaning:")
# print("Description:", test_df['description'].to_list())
# print("Swatch Alt:", test_df['swatch_alt'].to_list())

# # Apply the power_clean function
# test_df['description'] = test_df['description'].apply(power_clean)

# # Fixed the typo here: changed .apple() to .apply()
# test_df['swatch_alt'] = test_df['swatch_alt'].apply(power_clean)

# print("\nAfter cleaning with Option 2:")
# print("Description:", test_df['description'].to_list())
# print("Swatch Alt:", test_df['swatch_alt'].to_list())