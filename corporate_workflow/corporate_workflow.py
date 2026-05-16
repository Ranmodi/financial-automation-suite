# -*- coding: utf-8 -*-
"""Public-safe corporate workflow communication helper."""

from __future__ import annotations

import argparse
from pathlib import Path

from shared.excel_utils import read_table
from shared.email_utils import dataframe_to_html_table, wrap_email_html


def parse_args():
    parser = argparse.ArgumentParser(description="Build corporate workflow HTML report.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-html", default="./output/corporate_workflow_email.html")
    parser.add_argument("--status-column", default="Status")
    parser.add_argument("--target-status", default="Pending")
    return parser.parse_args()


def main():
    args = parse_args()
    df = read_table(Path(args.input))

    if args.status_column in df.columns:
        df = df[df[args.status_column].astype(str).str.lower() == args.target_status.lower()]

    html = wrap_email_html("Corporate Workflow Update", dataframe_to_html_table(df))

    output_path = Path(args.output_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"HTML generated: {output_path}")


if __name__ == "__main__":
    main()
