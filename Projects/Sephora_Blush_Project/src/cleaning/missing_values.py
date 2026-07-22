import pandas as pd
# import numpy as np

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from config import PROCESSED_DATA_DIR
from io_utils import read_csv_utf8

# %% Comprehensive Missing Analysis
# def comprehensive_missing_analysis(df):
#     """
#     Comprehensive missing value analysis with visual indicators.
    
#     Parameters:
#     df (pd.DataFrame): Input DataFrame
    
#     Returns:
#     dict: Dictionary containing various missing value analyses
#     """
    
#     # Basic missing value statistics
#     missing_count = df.isnull().sum()
#     missing_percentage = (df.isnull().sum() / len(df)) * 100
    
#     # Create detailed summary
#     summary_df = pd.DataFrame({
#         'Column': df.columns,
#         'Missing_Count': missing_count,
#         'Missing_Percentage': missing_percentage.round(2),
#         'Non_Null_Count': len(df) - missing_count,
#         'Data_Type': df.dtypes.values,
#         'Total_Rows': len(df),
#         # 'Complete_Rows': len(df) - missing_count
#     })
    
#     # Add severity indicator
#     summary_df['Severity'] = pd.cut(
#         summary_df['Missing_Percentage'],
#         bins=[-0.1, 5, 20, 50, 100],
#         labels=['Low (<5%)', 'Medium (5-20%)', 'High (20-50%)', 'Critical (>50%)']
#     )
    
#     # Sort by missing percentage
#     summary_df = summary_df.sort_values('Missing_Percentage', ascending=False)
    
#     # Overall statistics
#     total_cells = df.size
#     total_missing = df.isnull().sum().sum()
#     overall_missing_percentage = (total_missing / total_cells) * 100
    
#     # Missing value patterns
#     complete_rows = df.dropna().shape[0]
#     rows_with_missing = len(df) - complete_rows
    
#     # Columns with no missing values
#     complete_columns = df.columns[df.isnull().sum() == 0].tolist()
    
#     # Columns with missing values
#     columns_with_missing = df.columns[df.isnull().sum() > 0].tolist()
    
#     return {
#         'detailed_summary': summary_df,
#         'overall_stats': {
#             'total_rows': len(df),
#             'total_columns': len(df.columns),
#             'total_cells': total_cells,
#             'total_missing_cells': total_missing,
#             'overall_missing_percentage': overall_missing_percentage.round(2),
#             'complete_rows': complete_rows,
#             'rows_with_missing': rows_with_missing,
#             'complete_columns_count': len(complete_columns),
#             'columns_with_missing_count': len(columns_with_missing)
#         },
#         'complete_columns': complete_columns,
#         'columns_with_missing': columns_with_missing
#     }


# def print_missing_analysis(results):
#     """Print formatted missing value analysis"""
    
#     print("=" * 80)
#     print("MISSING VALUE ANALYSIS REPORT")
#     print("=" * 80)
    
#     # Overall statistics
#     stats = results['overall_stats']
#     print(f"\n📊 OVERALL STATISTICS:")
#     print(f"  • Total Rows: {stats['total_rows']:,}")
#     print(f"  • Total Columns: {stats['total_columns']}")
#     print(f"  • Total Cells: {stats['total_cells']:,}")
#     print(f"  • Missing Cells: {stats['total_missing_cells']:,} ({stats['overall_missing_percentage']:.2f}%)")
#     print(f"  • Complete Rows: {stats['complete_rows']:,}")
#     print(f"  • Rows with Missing Values: {stats['rows_with_missing']:,}")
    
#     # Column summary
#     print(f"\n📋 COLUMN SUMMARY:")
#     print(f"  • Complete Columns: {stats['complete_columns_count']}")
#     print(f"  • Columns with Missing Values: {stats['columns_with_missing_count']}")
    
#     # Detailed summary
#     if not results['detailed_summary'].empty:
#         print(f"\n🔍 DETAILED MISSING VALUE SUMMARY:")
#         print(results['detailed_summary'].to_string(index=False))
#     else:
#         print(f"\n✅ No missing values found in the dataset!")
    
#     print("\n" + "=" * 80)

# ## ONLY for direct execution
# if __name__ == "__main__":
#     try:
#         file_name = input("Enter File Name (no file type): ").strip()
#         products = read_csv_utf8(f"{PROCESSED_DATA_DIR}/{file_name}.csv")
#         print_missing_analysis(comprehensive_missing_analysis(products))
#     except FileNotFoundError as e:
#         print(f"Error: File {e.filename} was not found.")

# %% NEW Updated Logic
def comprehensive_missing_analysis(
    df: pd.DataFrame,
    columns: list[str] | None = None,
) -> dict:
    """
    Analyze missing values for all columns or a selected subset.

    Parameters
    ----------
    df:
        Source DataFrame.
    columns:
        Columns to analyze. If None, analyze every column.
    """
    if columns is None:
        columns = df.columns.tolist()

    missing_columns = [
        column for column in columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Columns not found in DataFrame: {missing_columns}"
        )

    analyzed_df = df[columns]

    missing_count = analyzed_df.isna().sum()

    if len(analyzed_df) > 0:
        missing_percentage = missing_count / len(analyzed_df) * 100
    else:
        missing_percentage = missing_count.astype(float)

    summary_df = pd.DataFrame({
        "Column": columns,
        "Missing_Count": missing_count.to_numpy(),
        "Missing_Percentage": missing_percentage.round(2).to_numpy(),
        "Non_Null_Count": (
            len(analyzed_df) - missing_count
        ).to_numpy(),
        "Data_Type": analyzed_df.dtypes.astype(str).to_numpy(),
        "Total_Rows": len(analyzed_df),
    })

    summary_df["Severity"] = pd.cut(
        summary_df["Missing_Percentage"],
        bins=[-0.1, 5, 20, 50, 100],
        labels=[
            "Low (<5%)",
            "Medium (5-20%)",
            "High (20-50%)",
            "Critical (>50%)",
        ],
    )

    # Only show columns that actually contain missing values.
    detailed_summary = summary_df[
        summary_df["Missing_Count"] > 0
    ].sort_values(
        "Missing_Percentage",
        ascending=False,
    )

    total_cells = analyzed_df.size
    total_missing = int(missing_count.sum())

    overall_missing_percentage = (
        total_missing / total_cells * 100
        if total_cells > 0
        else 0.0
    )

    complete_rows = int(
        analyzed_df.notna().all(axis=1).sum()
    )

    rows_with_missing = len(analyzed_df) - complete_rows

    complete_columns = missing_count[
        missing_count == 0
    ].index.tolist()

    columns_with_missing = missing_count[
        missing_count > 0
    ].index.tolist()

    return {
        "detailed_summary": detailed_summary,
        "overall_stats": {
            "total_rows": len(analyzed_df),
            "total_columns": len(columns),
            "total_cells": total_cells,
            "total_missing_cells": total_missing,
            "overall_missing_percentage": round(
                overall_missing_percentage,
                2,
            ),
            "complete_rows": complete_rows,
            "rows_with_missing": rows_with_missing,
            "complete_columns_count": len(complete_columns),
            "columns_with_missing_count": len(
                columns_with_missing
            ),
        },
        "complete_columns": complete_columns,
        "columns_with_missing": columns_with_missing,
        "analyzed_columns": columns,
    }


def print_missing_analysis(
    results: dict,
    title: str = "MISSING VALUE ANALYSIS REPORT",
) -> None:
    """Print a formatted missing-value report."""
    print("=" * 80)
    print(title)
    print("=" * 80)

    stats = results["overall_stats"]

    print("\n📊 OVERALL STATISTICS:")
    print(f"  • Total Rows: {stats['total_rows']:,}")
    print(f"  • Analyzed Columns: {stats['total_columns']}")
    print(f"  • Total Cells: {stats['total_cells']:,}")
    print(
        "  • Missing Cells: "
        f"{stats['total_missing_cells']:,} "
        f"({stats['overall_missing_percentage']:.2f}%)"
    )
    print(f"  • Complete Rows: {stats['complete_rows']:,}")
    print(
        "  • Rows with Missing Values: "
        f"{stats['rows_with_missing']:,}"
    )

    print("\n📋 COLUMN SUMMARY:")
    print(
        "  • Complete Columns: "
        f"{stats['complete_columns_count']}"
    )
    print(
        "  • Columns with Missing Values: "
        f"{stats['columns_with_missing_count']}"
    )

    detailed_summary = results["detailed_summary"]

    if detailed_summary.empty:
        print("\n✅ No missing values found in the analyzed columns!")
    else:
        print("\n🔍 DETAILED MISSING VALUE SUMMARY:")
        print(detailed_summary.to_string(index=False))

    print("\n" + "=" * 80)

