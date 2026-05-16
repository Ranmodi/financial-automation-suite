# -*- coding: utf-8 -*-
"""Shared public-safe configuration helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


def load_environment() -> None:
    if load_dotenv:
        load_dotenv()


def env_path(name: str, default: str) -> Path:
    return Path(os.getenv(name, default)).expanduser()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "y", "sim"}


def env_list(name: str, default: str = "") -> List[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


def get_default_dirs():
    input_dir = env_path("INPUT_DIR", "./samples")
    output_dir = env_path("OUTPUT_DIR", "./output")
    log_dir = env_path("LOG_DIR", "./logs")

    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    return input_dir, output_dir, log_dir
