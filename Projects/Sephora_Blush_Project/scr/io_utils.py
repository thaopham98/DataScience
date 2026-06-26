from __future__ import annotations

import json, logging
from pathlib import Path

import pandas as pd


def read_csv_utf8(path: str | Path, **kwargs) -> pd.DataFrame:
    """Read a CSV, always as UTF-8. Use this instead of pd.read_csv directly."""
    return pd.read_csv(path, encoding="utf-8", **kwargs)


def write_csv_utf8(df: pd.DataFrame, path: str | Path, index: bool = False, **kwargs) -> None:
    """Write a CSV, always as UTF-8. Use this instead of df.to_csv directly."""
    df.to_csv(path, index=index, encoding="utf-8", **kwargs)


def read_json_utf8(path: str | Path):
    """Read a JSON file, always as UTF-8."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from {path}: {e}")
        raise


def write_json_utf8(obj, path: str | Path, indent: int = 2) -> None:
    """Write a JSON file, always as UTF-8, preserving non-ASCII characters as-is."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)