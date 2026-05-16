# -*- coding: utf-8 -*-
"""Public-safe NPS response processing template.

The original private workflow used provider credentials and production e-mail settings.
This public version intentionally uses environment variables only.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
import requests


def fetch_nps_responses(api_url: str, token: str) -> pd.DataFrame:
    if not api_url or not token:
        raise EnvironmentError("NPS_API_URL and NPS_API_TOKEN must be configured.")

    response = requests.get(
        api_url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict) and "data" in data:
        data = data["data"]

    return pd.DataFrame(data)


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and export NPS-like responses.")
    parser.add_argument("--api-url", default=os.getenv("NPS_API_URL", ""))
    parser.add_argument("--token", default=os.getenv("NPS_API_TOKEN", ""))
    parser.add_argument("--output", default="./output/nps_responses.xlsx")
    return parser.parse_args()


def main():
    args = parse_args()
    df = fetch_nps_responses(args.api_url, args.token)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False)

    print(f"Output generated: {output_path}")


if __name__ == "__main__":
    main()
