# -*- coding: utf-8 -*-
"""Shared logging helpers."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        filemode="a",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def log_start(module_name: str) -> None:
    logging.info("=" * 80)
    logging.info("Starting module: %s", module_name)


def log_finish(module_name: str) -> None:
    logging.info("Finished module: %s", module_name)
