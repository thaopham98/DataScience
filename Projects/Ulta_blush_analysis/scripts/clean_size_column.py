import pandas as pd
# import matplotli.sns
# import missingno as msno
import re


rdf = pd.read_csv(r"semi_cleaned_data/cleaned_data.csv", encoding='utf-8-sig')
# rdf.info()

## Display the missing data
# print(rdf.loc[rdf['size'].isnull(), ['brand', 'product_name', 'size']].nunique()) # rows of missing values of size

# print(rdf.loc[rdf["brand"] == "PÜR Minerals", "brand"].head(1))
# print(rdf.loc[rdf['product_name'].str.contains("Futurist", na=False), 'product_name'])

"""
Fixing Encoding
"""
######################################################
def power_clean(text):
    if not isinstance(text, str):
        return text
    
    # 1. Target the specific "Futurist" mess: Ã combined with Â or invisible spaces
    # This regex looks for Ã followed by any number of Â, \xa0, or other glitches
    text = re.sub(r'Ã[Â\x82\xa0\x82]+', ' ', text)
    
    # 2. Target the leftover Â that you saw in your output
    text = re.sub(r'Â', '', text)
    
    # 3. Target other known Mojibake patterns
    text = text.replace('ÃƒÂ©', 'é').replace('ÃƒÂ', 'à').replace('NÃ‚Â°', 'N°')
    
    # 4. Collapse multiple spaces into one and strip
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Apply to the column
rdf['product_name'] = rdf['product_name'].apply(power_clean)
rdf['swatch_alt'] = rdf['swatch_alt'].apply(power_clean)
rdf['shade'] = rdf['shade'].apply(power_clean)

# print(rdf.loc[rdf['product_name'].str.contains("Futurist", na=False), 'product_name'])


size_map_metric = {
    # --- GRAMS (Powders, Creams, Sticks) ---
    '22 g': ['Marble Cream Blush Stick'],                     # Converted from 0.78 oz
    '21 g': ['Ultimate Blush Palette'],                       # Total palette weight
    '16.8 g': ['Blushed Duo'],
    '12 g': ['Blursh Pod Domed Blusher '], 
    '10 g': ['MegaGlo Blushlighter'],
    '9 g': ['DreamStick Cream Blush'],
    '8.5 g': ['Cream Stick Blush with Brush Applicator', 'Blush Crush Liquid Blush'],
    '8.4 g': ['Effervescence Extra Dimension Face Compact'], 
    '8.2 g': ['Juice Stick Dewy Gel-Cream Blush'],
    '7.7 g': ['Blushed Liquid Blushlighter'],                 # Converted from 0.27 oz
    '7.5 g': ['Glow Time Blush Stick'],
    '6 g': ['Blushed Cream Blush', 'Matte Blush', 'Megaglo Makeup Stick', "I'm Blushing 2-in-1 Cheek and Lip Tint", 'Heart Pressed Powder Blush'],
    '5.5 g': ['Blusher Reloaded', 'Jelly Blush Stick Lip & Cheek Stain', 'Baby Got Blush', 'Bouncy Blur Blush'],
    '5 g': ['2-in-1 Mosaic Blush & Bronzer Powder', 'Macaron Blush & Glow Duo', 'Liquid Blush - 2-in-1 Lip & Cheek Tint'],
    '4.5 g': ['Blush-Mallow Soft Blusher', 'Skin Silk Marble Blush Stick'],
    '3.2 g': ['PurePressed Blush'],
    '3 g': ['Magic Touch Cream Blush & Lip Trio', 'Just Kissed Lip and Cheek Stain'],
    '2.5 g': ['Baked Blush'],

    # --- MILLILITERS (Liquids, Drops, Tints) ---
    '15 ml': ['Hot Shot Blush Drops'],                        # Converted from 0.5 oz
    '10 ml': ['Futurist Blushmaker Dewy Cheek Tint Liquid Blush', 'Superdewy Liquid Blush Burst'],
    '9.5 ml': ['Glimmer Blush Drops'],                        # Converted from 0.32 fl oz
    '8.5 ml': ['Skin Idôle Juicy Liquid Blush'],
    '8 ml': ['Maneater Satin Blush Cheek Plump'],
    '6 ml': ['Play Daze Airy Liquid Blush', 'Play Daze Airy Soft Matte Liquid Blush'],
    '3.9 ml': ['Jelly Tint - 2-in-1 Lip & Cheek Tint Stain'],
    '3.5 ml': ['Blush Rush Liquid Blush']
}

# 2. Invert the dictionary so it's {Product: Size} for fast mapping
size_lookup = {
    product.strip(): size 
    for size, products in size_map_metric.items() 
    for product in products
}

# 3. Fill the missing values in your DataFrame
# We use .str.strip() just in case your dataframe has hidden trailing spaces
rdf['size'] = rdf['size'].fillna(rdf['product_name'].str.strip().map(size_lookup))

# Check how many are still missing
print(f"Missing sizes remaining: {rdf['size'].isnull().sum()}")
print(rdf.loc[rdf['size'].isnull(), ['brand','product_name']].value_counts())
print(rdf.info())

#Export to CSV 
# index=False prevents pandas from adding a new column for the row numbers
# rdf.to_csv("semi_cleaned_data/cleaned_data_v2.csv", encoding='utf-8-sig', index=False)
# print("File exported successfully to semi_cleaned_data/cleaned_data_v2.csv")