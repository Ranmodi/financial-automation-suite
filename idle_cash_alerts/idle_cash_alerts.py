# -*- coding: utf-8 -*-
"""Public-safe idle cash alert automation."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from shared.excel_utils import normalize_account_column, read_table, write_excel, parse_brl
from shared.logging_utils import configure_logging, log_start, log_finish


def build_idle_cash_alerts(balances, advisors, threshold: float):
    balances = balances.copy()
    advisors = advisors.copy()

    balances["account_norm"] = normalize_account_column(balances["Account"])
    advisors["account_norm"] = normalize_account_column(advisors["Account"])

    balances["Balance"] = balances["Balance"].apply(parse_brl)

    result = balances.merge(
        advisors[["account_norm", "Advisor", "Advisor Email"]],
        on="account_norm",
        how="left",
    )

    result = result[result["Balance"] >= threshold].sort_values("Balance", ascending=False)
    return result.rename(columns={"account_norm": "Account"})


def parse_args():
    parser = argparse.ArgumentParser(description="Generate idle cash alerts.")
    parser.add_argument("--balances", required=True)
    parser.add_argument("--advisors", required=True)
    parser.add_argument("--output", default="./output/idle_cash_alerts.xlsx")
    parser.add_argument("--log", default="./logs/idle_cash_alerts.log")
    parser.add_argument("--threshold", type=float, default=5000.0)
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging(Path(args.log))
    log_start("idle_cash_alerts")

    result = build_idle_cash_alerts(
        balances=read_table(Path(args.balances)),
        advisors=read_table(Path(args.advisors)),
        threshold=args.threshold,
    )

    write_excel(result, Path(args.output), sheet_name="Idle Cash")
    logging.info("Generated rows: %s", len(result))
    log_finish("idle_cash_alerts")
    print(f"Output generated: {args.output}")


if __name__ == "__main__":
    main()
