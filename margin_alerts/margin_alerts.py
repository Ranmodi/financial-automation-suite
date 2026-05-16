# -*- coding: utf-8 -*-
"""Public-safe margin alert automation."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from shared.excel_utils import normalize_account_column, read_table, write_excel, parse_brl
from shared.logging_utils import configure_logging, log_start, log_finish


def build_margin_alerts(movements: pd.DataFrame, advisors: pd.DataFrame) -> pd.DataFrame:
    movements = movements.copy()
    advisors = advisors.copy()

    movements["account_norm"] = normalize_account_column(movements["Account"])
    advisors["account_norm"] = normalize_account_column(advisors["Account"])

    movements["Net Amount"] = movements["Net Amount"].apply(parse_brl)

    margin_movements = movements[
        movements["Movement Type"].astype(str).str.contains("margin", case=False, na=False)
    ].copy()

    grouped = (
        margin_movements
        .groupby("account_norm", as_index=False)
        .agg({"Net Amount": "sum"})
    )

    result = grouped.merge(
        advisors[["account_norm", "Advisor", "Advisor Email"]],
        on="account_norm",
        how="left",
    )

    result = result.rename(columns={"account_norm": "Account"})
    result = result[result["Net Amount"] < 0].sort_values("Net Amount")

    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Generate margin alert output.")
    parser.add_argument("--movements", required=True)
    parser.add_argument("--advisors", required=True)
    parser.add_argument("--output", default="./output/margin_alerts.xlsx")
    parser.add_argument("--log", default="./logs/margin_alerts.log")
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(Path(args.log))
    log_start("margin_alerts")

    movements = read_table(Path(args.movements))
    advisors = read_table(Path(args.advisors))

    result = build_margin_alerts(movements, advisors)
    write_excel(result, Path(args.output), sheet_name="Margin Alerts")

    logging.info("Generated rows: %s", len(result))
    log_finish("margin_alerts")
    print(f"Output generated: {args.output}")


if __name__ == "__main__":
    main()
