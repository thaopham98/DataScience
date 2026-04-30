# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 19:55:20 2026

@author: thaop
"""

# %% SETUP
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import numpy as np

# %%


# %% LOAD DATASETS
# rdf = pd.read_csv(r'../raw_data/ulta_clean_blush.csv', encoding='utf-8-sig')
rdf = pd.read_csv(r"C:\Users\thaop\Desktop\Ulta_blush_analysis/raw_data/ulta_clean_blush.csv", encoding='utf-8-sig')
rdf.info()

df = pd.read_csv(r"C:\Users\thaop\Desktop\Ulta_blush_analysis/clean_data/ulta_clean_blush_v1.csv", encoding="utf-8-sig")
df.info()
# %%

# %% DISPLAY MISSING VALUES OF THE DATASET
def plot_missing_values(df):
    # 1. Prepare Data
    total_rows = len(df)
    null_counts = df.isnull().sum()
    present_counts = total_rows - null_counts
    
    plot_df = pd.DataFrame({
        'Column': df.columns,
        'Present': present_counts,
        'Missing': null_counts
    }).sort_values(by='Missing', ascending=False)

    # 2. Setup Plot
    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(14, 8))

    # 3. Create Stacked Bars
    bar_present = ax.bar(plot_df['Column'], plot_df['Present'], 
                         color='#2ecc71', label='Present (Non-Null)')
    
    bar_missing = ax.bar(plot_df['Column'], plot_df['Missing'], 
                         bottom=plot_df['Present'], color='#e74c3c', label='Missing (Null)')

    # 4. Generate Custom Labels (Count + Percentage)
    # Format: "Count (Percent%)"
    # We use \n for a line break to keep it tidy inside the bars
    present_labels = [
        f'{int(c)}\n({(c/total_rows*100):.1f}%)' if c > 0 else '' 
        for c in plot_df['Present']
    ]
    
    missing_labels = [
        f'{int(c)}\n({(c/total_rows*100):.1f}%)' if c > 0 else '' 
        for c in plot_df['Missing']
    ]

    # 5. Apply Labels to Bars
    ax.bar_label(bar_present, labels=present_labels, label_type='center', 
                 color='black', fontweight='bold', fontsize=9)
    
    ax.bar_label(bar_missing, labels=missing_labels, label_type='center', 
                 color='black', fontweight='bold', fontsize=9)

    # 6. Formatting & Final Touches
    ax.set_title('Data Completeness: Count and Percentage per Column', fontsize=16, pad=20)
    ax.set_ylabel('Number of Records', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Move legend outside the plot area
    ax.legend(title="Status", bbox_to_anchor=(1.02, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
# %%

# %%
plot_missing_values(rdf)

plot_missing_values(df)

# %%

# msno.matrix(rdf) # will need to run `pip install missingno`


# %% DISPLAY NUMBER OF MISSING SIZE PER BRAND
null_size = rdf[rdf['size'].isnull()] # rows of missing values of size

# 1. Assign the plot to 'ax'
ax = null_size['brand'].value_counts().plot(kind='barh', color='skyblue')

# 2. Use bar_label on the first container (the bars)
ax.bar_label(ax.containers[0], padding=3)

# 3. Clean up labels
plt.ylabel('Brand')
plt.xlabel('Count')
plt.title('Number of Missing Size Value per Brand')
plt.tight_layout() # Prevents labels from getting cut off
plt.show()
# %%

# %% 
def plot_missing_size(dataset):
    print("\n===Checking before plotting===")
    if 'size' not in dataset:
        raise ValueError("Missing required field: 'size'")
    
    missing = dataset[dataset['size'].isnull()]
    ax = missing['brand'].value_counts().plot(kind='barh', color='skyblue')
    ax.bar_label(ax.containers[0], padding=3)
    plt.ylabel('Brand')
    plt.xlabel('Number of Missing Value')
    plt.title('Number of Missing Size Value per Brand')
    plt.tight_layout()
    plt.show()
    print("Plotting Complete!")

# Wrap function calls in try-except to catch errors and continue
try:
    plot_missing_size(df)  # has no 'size'
except ValueError as e:
    print(f"ERROR: {e}")

try:
    plot_missing_size(rdf)  # has 'size'
except ValueError as e:
    print(f"ERROR: {e}")
# %%











































