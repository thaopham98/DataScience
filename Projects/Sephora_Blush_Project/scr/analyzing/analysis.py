## Setup

# %% 
###
import pandas as pd
# import numpy as np

# %% Path
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from config import PROCESSED_DATA_DIR
from io_utils import read_csv_utf8

## Load Data
# %% Read CSV files
try:
    products = read_csv_utf8(f"{PROCESSED_DATA_DIR}/bronzer-makeup_products_20260626_203349.csv")
except FileNotFoundError as e:
    print(f"Error: File {e.filename} was not found.")

# %% Exploratory Data Analysis

print(products.info())
print(f"Total Missing Value per Column:\n{products.isna().sum()}")

# %% 1. Basic Function
def check_null(df):
        # Total missing values per column
    missing_count = df.isnull().sum()
    
    # Percentage of missing values per column
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    
    # Create summary DataFrame
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_count,
        'Missing_Percentage': missing_percentage.round(2),
        'Data_Type': df.dtypes.values
    })
    
    # Filter only columns with missing values and sort
    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
    missing_summary = missing_summary.sort_values('Missing_Percentage', ascending=False)
    
    return missing_summary # Returns a DataFrame

# %% 2. Comprehensive Missing Analysis
def comprehensive_missing_analysis(df):
    """
    Comprehensive missing value analysis with visual indicators.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    
    Returns:
    dict: Dictionary containing various missing value analyses
    """
    
    # Basic missing value statistics
    missing_count = df.isnull().sum()
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    
    # Create detailed summary
    summary_df = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': missing_count,
        'Missing_Percentage': missing_percentage.round(2),
        'Data_Type': df.dtypes.values,
        'Total_Rows': len(df),
        'Complete_Rows': len(df) - missing_count
    })
    
    # Add severity indicator
    summary_df['Severity'] = pd.cut(
        summary_df['Missing_Percentage'],
        bins=[-0.1, 5, 20, 50, 100],
        labels=['Low (<5%)', 'Medium (5-20%)', 'High (20-50%)', 'Critical (>50%)']
    )
    
    # Sort by missing percentage
    summary_df = summary_df.sort_values('Missing_Percentage', ascending=False)
    
    # Overall statistics
    total_cells = df.size
    total_missing = df.isnull().sum().sum()
    overall_missing_percentage = (total_missing / total_cells) * 100
    
    # Missing value patterns
    complete_rows = df.dropna().shape[0]
    rows_with_missing = len(df) - complete_rows
    
    # Columns with no missing values
    complete_columns = df.columns[df.isnull().sum() == 0].tolist()
    
    # Columns with missing values
    columns_with_missing = df.columns[df.isnull().sum() > 0].tolist()
    
    return {
        'detailed_summary': summary_df,
        'overall_stats': {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_cells': total_cells,
            'total_missing_cells': total_missing,
            'overall_missing_percentage': overall_missing_percentage.round(2),
            'complete_rows': complete_rows,
            'rows_with_missing': rows_with_missing,
            'complete_columns_count': len(complete_columns),
            'columns_with_missing_count': len(columns_with_missing)
        },
        'complete_columns': complete_columns,
        'columns_with_missing': columns_with_missing
    }

# Example usage with visualization
def print_missing_analysis(results):
    """Print formatted missing value analysis"""
    
    print("=" * 80)
    print("MISSING VALUE ANALYSIS REPORT")
    print("=" * 80)
    
    # Overall statistics
    stats = results['overall_stats']
    print(f"\n📊 OVERALL STATISTICS:")
    print(f"  • Total Rows: {stats['total_rows']:,}")
    print(f"  • Total Columns: {stats['total_columns']}")
    print(f"  • Total Cells: {stats['total_cells']:,}")
    print(f"  • Missing Cells: {stats['total_missing_cells']:,} ({stats['overall_missing_percentage']:.2f}%)")
    print(f"  • Complete Rows: {stats['complete_rows']:,}")
    print(f"  • Rows with Missing Values: {stats['rows_with_missing']:,}")
    
    # Column summary
    print(f"\n📋 COLUMN SUMMARY:")
    print(f"  • Complete Columns: {stats['complete_columns_count']}")
    print(f"  • Columns with Missing Values: {stats['columns_with_missing_count']}")
    
    # Detailed summary
    if not results['detailed_summary'].empty:
        print(f"\n🔍 DETAILED MISSING VALUE SUMMARY:")
        print(results['detailed_summary'].to_string(index=False))
    else:
        print(f"\n✅ No missing values found in the dataset!")
    
    print("\n" + "=" * 80)

# %% Calling 2
# Run analysis
results = comprehensive_missing_analysis(products)
print_missing_analysis(results)

# %% 3. Missing Value Heatmap Visualization
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_missing_values(df, figsize=(12, 8)):
    """
    Create a heatmap visualization of missing values.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    figsize (tuple): Figure size for the plot
    """
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # 1. Missing value heatmap
    sns.heatmap(df.isnull(), cbar=True, yticklabels=False, 
                cmap='viridis', ax=axes[0, 0])
    axes[0, 0].set_title('Missing Value Heatmap', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Columns')
    axes[0, 0].set_ylabel('Rows')
    
    # 2. Missing value percentage bar plot
    missing_percentages = (df.isnull().sum() / len(df)) * 100
    missing_percentages = missing_percentages[missing_percentages > 0].sort_values(ascending=False)
    
    if not missing_percentages.empty:
        bars = axes[0, 1].barh(range(len(missing_percentages)), missing_percentages.values)
        axes[0, 1].set_yticks(range(len(missing_percentages)))
        axes[0, 1].set_yticklabels(missing_percentages.index)
        axes[0, 1].set_xlabel('Missing Percentage (%)')
        axes[0, 1].set_title('Columns with Missing Values', fontsize=12, fontweight='bold')
        
        # Add percentage labels on bars
        for i, (bar, percentage) in enumerate(zip(bars, missing_percentages.values)):
            axes[0, 1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                          f'{percentage:.1f}%', va='center')
    else:
        axes[0, 1].text(0.5, 0.5, 'No Missing Values', 
                       ha='center', va='center', transform=axes[0, 1].transAxes)
    
    # 3. Missing value pattern correlation
    if df.isnull().sum().sum() > 0:
        missing_corr = df.isnull().corr()
        sns.heatmap(missing_corr, annot=True, cmap='coolwarm', center=0,
                   ax=axes[1, 0])
        axes[1, 0].set_title('Missing Value Correlation', fontsize=12, fontweight='bold')
    else:
        axes[1, 0].text(0.5, 0.5, 'No Missing Values', 
                       ha='center', va='center', transform=axes[1, 0].transAxes)
    
    # 4. Missing value counts
    missing_counts = df.isnull().sum()
    missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)
    
    if not missing_counts.empty:
        bars = axes[1, 1].bar(range(len(missing_counts)), missing_counts.values)
        axes[1, 1].set_xticks(range(len(missing_counts)))
        axes[1, 1].set_xticklabels(missing_counts.index, rotation=45, ha='right')
        axes[1, 1].set_ylabel('Number of Missing Values')
        axes[1, 1].set_title('Missing Value Counts by Column', fontsize=12, fontweight='bold')
        
        # Add count labels on bars
        for bar, count in zip(bars, missing_counts.values):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                          str(count), ha='center', va='bottom')
    else:
        axes[1, 1].text(0.5, 0.5, 'No Missing Values', 
                       ha='center', va='center', transform=axes[1, 1].transAxes)
    
    plt.tight_layout()
    plt.show()

# Run visualization
visualize_missing_values(products)

# %% 4. Advanced Missing Value Patterns Analysis
def analyze_missing_patterns(df):
    """
    Analyze patterns and relationships in missing values.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    
    Returns:
    dict: Analysis of missing value patterns
    """
    
    # Create missing indicator matrix
    missing_matrix = df.isnull().astype(int)
    
    # Find unique missing patterns
    pattern_counts = missing_matrix.value_counts()
    
    # Analyze missing combinations
    patterns_analysis = []
    
    for pattern, count in pattern_counts.items():
        missing_columns = [col for col, val in zip(missing_matrix.columns, pattern) if val == 1]
        
        if missing_columns:
            patterns_analysis.append({
                'pattern': ' & '.join(missing_columns) if missing_columns else 'Complete',
                'missing_columns': missing_columns,
                'count': count,
                'percentage': (count / len(df)) * 100
            })
    
    # Sort by count
    patterns_analysis.sort(key=lambda x: x['count'], reverse=True)
    
    # Analyze correlations between missing patterns
    missing_correlation = df.isnull().corr()
    
    # Strong missing correlations
    strong_correlations = []
    for i in range(len(missing_correlation.columns)):
        for j in range(i+1, len(missing_correlation.columns)):
            if abs(missing_correlation.iloc[i, j]) > 0.5:
                strong_correlations.append({
                    'column1': missing_correlation.columns[i],
                    'column2': missing_correlation.columns[j],
                    'correlation': missing_correlation.iloc[i, j]
                })
    
    return {
        'patterns': patterns_analysis,
        'missing_correlation_matrix': missing_correlation,
        'strong_correlations': strong_correlations,
        'total_patterns': len(patterns_analysis)
    }

# Run pattern analysis
pattern_results = analyze_missing_patterns(products)
print("\nMissing Value Patterns:")
for pattern in pattern_results['patterns'][:5]:  # Show top 5 patterns
    print(f"  • Pattern: {pattern['pattern']}")
    print(f"    Count: {pattern['count']} rows ({pattern['percentage']:.2f}%)")

# %% 5. One-Liner Quick Checks
# Quick missing value checks
def quick_missing_check(df):
    """Quick summary of missing values"""
    print(f"Total missing values: {df.isnull().sum().sum()}")
    print(f"Missing percentage: {(df.isnull().sum().sum() / df.size) * 100:.2f}%")
    print(f"Columns with missing values: {df.columns[df.isnull().any()].tolist()}")
    print(f"Rows with missing values: {df.isnull().any(axis=1).sum()}")

# %% Calling One-Liner Quick Checks
missing_cols = products.columns[products.isnull().any()].tolist()  # Columns with any missing
print(f"Columns with Missing Values: {missing_cols}")
missing_percentage = (products.isnull().sum() / len(products)) * 100  # Missing percentage per column
print(f"Missing Percentage per Column: \n{missing_percentage}")
complete_rows = products.dropna().shape[0]  # Number of complete rows
print(f"Number of Complete Rows: {complete_rows}")