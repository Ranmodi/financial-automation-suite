# -*- coding: utf-8 -*-
"""Public-safe desk balance alert automation."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

from shared.excel_utils import normalize_account_column, read_table, parse_brl
from shared.logging_utils import configure_logging, log_start, log_finish


def build_desk_balance_alerts(accounts: pd.DataFrame, balances: pd.DataFrame, advisors: pd.DataFrame, min_balance: float) -> dict[str, pd.DataFrame]:
    accounts = accounts.copy()
    balances = balances.copy()
    advisors = advisors.copy()

    accounts["account_norm"] = normalize_account_column(accounts["Account"])
    balances["account_norm"] = normalize_account_column(balances["Account"])
    advisors["account_norm"] = normalize_account_column(advisors["Account"])

    balances["Balance"] = balances["Balance"].apply(parse_brl)

    base = (
        accounts[["account_norm", "Client Name"]]
        .merge(balances[["account_norm", "Balance"]], on="account_norm", how="left")
        .merge(advisors[["account_norm", "Advisor", "Advisor Email"]], on="account_norm", how="left")
    )

    positives = base[base["Balance"] > min_balance].copy().sort_values("Balance", ascending=False)
    negatives = base[base["Balance"] < 0].copy().sort_values("Balance")

    return {
        "Positive Balances": positives.rename(columns={"account_norm": "Account"}),
        "Negative Balances": negatives.rename(columns={"account_norm": "Account"}),
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Generate desk balance alerts.")
    parser.add_argument("--accounts", required=True)
    parser.add_argument("--balances", required=True)
    parser.add_argument("--advisors", required=True)
    parser.add_argument("--output", default="./output/desk_balance_alerts.xlsx")
    parser.add_argument("--log", default="./logs/desk_balance_alerts.log")
    parser.add_argument("--min-balance", type=float, default=5000.0)
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(Path(args.log))
    log_start("desk_balance_alerts")

    outputs = build_desk_balance_alerts(
        accounts=read_table(Path(args.accounts)),
        balances=read_table(Path(args.balances)),
        advisors=read_table(Path(args.advisors)),
        min_balance=args.min_balance,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        for sheet, df in outputs.items():
            df.to_excel(writer, index=False, sheet_name=sheet[:31])

    logging.info("Generated output: %s", output_path)
    log_finish("desk_balance_alerts")
    print(f"Output generated: {output_path}")


if __name__ == "__main__":
    main()
