from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.utils.io import read_table, clean_columns, save_csv
from src.utils.db import save_table, create_indexes
from src.loaders.normalizers import (
    normalize_kcd,
    normalize_drug_benefit,
    normalize_fee,
    normalize_medical_act,
    normalize_material,
    normalize_special_case_rare,
    normalize_special_case_rule,
)

NORMALIZERS = {
    "kcd": (normalize_kcd, "kcd_master"),
    "drug_benefit": (normalize_drug_benefit, "drug_benefit_master"),
    "fee_reflection": (normalize_fee, "fee_master"),
    "medical_act": (normalize_medical_act, "medical_act_master"),
    "material_file": (normalize_material, "material_master"),
    "special_case_rare": (normalize_special_case_rare, "special_case_rare_master"),
    "special_case_rule": (normalize_special_case_rule, "special_case_rule_master"),
}


def load_file(master_name: str, file_path: str, sheet_name: str | int | None = 0) -> pd.DataFrame:
    if master_name not in NORMALIZERS:
        raise ValueError(f"지원하지 않는 master_name입니다: {master_name}. 가능값: {list(NORMALIZERS)}")
    raw = clean_columns(read_table(file_path, sheet_name=sheet_name))
    normalizer, table = NORMALIZERS[master_name]
    df = normalizer(raw)
    save_csv(df, Path("data/processed") / f"{master_name}.csv")
    save_table(df, table)
    create_indexes()
    return df
