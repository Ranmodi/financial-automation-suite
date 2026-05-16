# -*- coding: utf-8 -*-
"""Public-safe advisor profitability communication helper."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from shared.excel_utils import read_table
from shared.email_utils import dataframe_to_html_table, wrap_email_html


def build_profitability_summary(df: pd.DataFrame, advisor_col: str = "Advisor") -> pd.DataFrame:
    numeric_cols = [c for c in df.columns if c.lower() in {"revenue", "profit", "result", "aum"}]
    if not numeric_cols:
        return df.groupby(advisor_col, as_index=False).size().rename(columns={"size": "Records"})

    return df.groupby(advisor_col, as_index=False)[numeric_cols].sum()


def parse_args():
    parser = argparse.ArgumentParser(description="Build advisor profitability summary.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="./output/advisor_profitability_summary.xlsx")
    parser.add_argument("--html-output", default="./output/advisor_profitability_email.html")
    return parser.parse_args()


def main():
    args = parse_args()
    df = read_table(Path(args.input))
    summary = build_profitability_summary(df)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_excel(output_path, index=False)

    html = wrap_email_html("Advisor Profitability Summary", dataframe_to_html_table(summary))
    Path(args.html_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.html_output).write_text(html, encoding="utf-8")

    print(f"Output generated: {output_path}")
    print(f"HTML generated: {args.html_output}")


if __name__ == "__main__":
    main()
