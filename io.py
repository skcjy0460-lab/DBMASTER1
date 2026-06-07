from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


def ensure_dirs() -> None:
    for p in ["data/raw", "data/processed", "db"]:
        Path(p).mkdir(parents=True, exist_ok=True)


def read_table(path: str | Path, sheet_name: str | int | None = 0) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
    suffix = path.suffix.lower()
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path, sheet_name=sheet_name, dtype=str)
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str, encoding="utf-8-sig")
    raise ValueError(f"지원하지 않는 파일 형식입니다: {suffix}")


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().replace("\n", " ").replace("  ", " ") for c in df.columns]
    return df


def save_csv(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")


def load_json(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
