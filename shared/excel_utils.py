# -*- coding: utf-8 -*-
"""Shared Excel and dataframe utilities."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


def normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_account(value) -> str:
    if pd.isna(value):
        return ""

    if isinstance(value, float) and value.is_integer():
        value = int(value)

    text = re.sub(r"\D+", "", str(value))
    return text.lstrip("0") or text


def normalize_account_column(series: pd.Series) -> pd.Series:
    return series.apply(normalize_account)


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()

    if suffix in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path)

    raise ValueError(f"Unsupported file type: {path.suffix}")


def write_excel(df: pd.DataFrame, output_path: Path, sheet_name: str = "Result") -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)


def parse_brl(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).replace("R$", "").strip()
    text = text.replace(".", "").replace(",", ".")

    try:
        return float(text)
    except Exception:
        return None


def format_brl(value) -> str:
    if value is None or pd.isna(value):
        return ""
    text = f"R$ {float(value):,.2f}"
    return text.replace(",", "X").replace(".", ",").replace("X", ".")
