# -*- coding: utf-8 -*-
"""Public-safe advisor maturities consolidation."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from shared.excel_utils import normalize_account_column, read_table


def consolidate_maturities(fixed_income, structured, advisors):
    fixed_income = fixed_income.copy()
    structured = structured.copy()
    advisors = advisors.copy()

    fixed_income["Product Class"] = "Fixed Income"
    structured["Product Class"] = "Structured Product"

    fixed_income = fixed_income.rename(columns={
        "Maturity Date": "Maturity Date",
        "Net Value": "Amount",
    })

    structured = structured.rename(columns={
        "Fixing Date": "Maturity Date",
        "Notional": "Amount",
    })

    common_cols = ["Account", "Client Name", "Product", "Product Class", "Maturity Date", "Amount"]
    combined = pd.concat([fixed_income[common_cols], structured[common_cols]], ignore_index=True)

    combined["account_norm"] = normalize_account_column(combined["Account"])
    advisors["account_norm"] = normalize_account_column(advisors["Account"])

    combined = combined.merge(
        advisors[["account_norm", "Advisor", "Advisor Email"]],
        on="account_norm",
        how="left",
    )

    return combined.drop(columns=["account_norm"])


def parse_args():
    parser = argparse.ArgumentParser(description="Consolidate maturities by advisor.")
    parser.add_argument("--fixed-income", required=True)
    parser.add_argument("--structured", required=True)
    parser.add_argument("--advisors", required=True)
    parser.add_argument("--output", default="./output/advisor_maturities.xlsx")
    return parser.parse_args()


def main():
    args = parse_args()
    result = consolidate_maturities(
        fixed_income=read_table(Path(args.fixed_income)),
        structured=read_table(Path(args.structured)),
        advisors=read_table(Path(args.advisors)),
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_excel(output_path, index=False)
    print(f"Output generated: {output_path}")


if __name__ == "__main__":
    main()
