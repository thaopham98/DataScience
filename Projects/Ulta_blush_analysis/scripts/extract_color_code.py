# !pip install pandas requests pillow scikit-image numpy


## Setup
import pandas as pd
import requests
import numpy as np
from PIL import Image
from io import BytesIO
from skimage.color import rgb2lab
import time

def extract_color_from_url(url):
    """
    Downloads an image from a URL and extracts its dominant RGB 
    and converts it to CIE L*a*b* color space.
    """
    if pd.isna(url) or not isinstance(url, str):
        return None, None, None, None, None, None

    try:
        # 1. Download the image
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 2. Open image and ensure it's in RGB mode
        img = Image.open(BytesIO(response.content)).convert('RGB')
        
        # 3. Focus on the center to avoid edge artifacts or background transparency
        width, height = img.size
        left = int(width * 0.4)
        top = int(height * 0.4)
        right = int(width * 0.6)
        bottom = int(height * 0.6)
        
        center_crop = img.crop((left, top, right, bottom))
        img_np = np.array(center_crop)
        
        # 4. Calculate the median RGB value of the center area
        # Median is safer than mean to exclude any stray pixel anomalies
        median_r = int(np.median(img_np[:, :, 0]))
        median_g = int(np.median(img_np[:, :, 1]))
        median_b = int(np.median(img_np[:, :, 2]))
        
        # 5. Convert RGB to L*a*b* # skimage expects RGB values normalized between 0 and 1
        rgb_normalized = np.array([[[median_r / 255.0, median_g / 255.0, median_b / 255.0]]])
        lab_normalized = rgb2lab(rgb_normalized)
        
        lab_l = round(float(lab_normalized[0][0][0]), 2)
        lab_a = round(float(lab_normalized[0][0][1]), 2)
        lab_b = round(float(lab_normalized[0][0][2]), 2)
        
        return median_r, median_g, median_b, lab_l, lab_a, lab_b

    except Exception as e:
        # Logs errors (e.g., 404, connection timeout, corrupted images) gracefully
        print(f"Error processing URL {url}: {e}")
        return None, None, None, None, None, None

def process_blush_dataset(input_csv_path, output_csv_path):
    # Load your dataset
    df = pd.read_csv(input_csv_path)
    
    print(f"Loaded {len(df)} rows. Starting color extraction pipeline...")
    
    # Initialize lists to hold our new data
    r_list, g_list, b_list = [], [], []
    lab_l_list, lab_a_list, lab_b_list = [], [], []
    
    for idx, url in enumerate(df['swatch_img_url']):
        # Optional tracking printout every 100 images
        if idx % 100 == 0 and idx > 0:
            print(f"Processed {idx}/{len(df)} images...")
            
        r, g, b, l, a, lab_b_val = extract_color_from_url(url)
        
        r_list.append(r)
        g_list.append(g)
        b_list.append(b)
        lab_l_list.append(l)
        lab_a_list.append(a)
        lab_b_list.append(lab_b_val)
        
        # Polite scraping delay to be kind to Ulta's servers
        time.sleep(0.05) 
        
    # Append the extracted color arrays back to the dataframe
    df['rgb_r'] = r_list
    df['rgb_g'] = g_list
    df['rgb_b'] = b_list
    df['lab_L'] = lab_l_list
    df['lab_a'] = lab_a_list
    df['lab_b'] = lab_b_list
    
    # Save to a new csv
    df.to_csv(output_csv_path, index=False)
    print(f"Pipeline complete! Saved results to {output_csv_path}")

# --- Execution ---
# Replace with your actual file names
process_blush_dataset(r'../clean_data/ulta_clean_blush_v1.csv', r'../clean_data/ulta_clean_blush_with_colors.csv')