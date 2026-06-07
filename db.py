from __future__ import annotations

import os
import sqlite3
from pathlib import Path
import pandas as pd


def get_db_path() -> str:
    return os.getenv("DB_PATH", "db/medical_master.db")


def save_table(df: pd.DataFrame, table_name: str, db_path: str | None = None, if_exists: str = "replace") -> None:
    db_path = db_path or get_db_path()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)


def create_indexes(db_path: str | None = None) -> None:
    db_path = db_path or get_db_path()
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        index_sql = [
            "CREATE INDEX IF NOT EXISTS idx_kcd_code ON kcd_master(kcd_code)",
            "CREATE INDEX IF NOT EXISTS idx_fee_code ON fee_master(fee_code)",
            "CREATE INDEX IF NOT EXISTS idx_act_code ON medical_act_master(act_code)",
            "CREATE INDEX IF NOT EXISTS idx_material_code ON material_master(material_code)",
            "CREATE INDEX IF NOT EXISTS idx_drug_code ON drug_benefit_master(drug_code)",
            "CREATE INDEX IF NOT EXISTS idx_special_kcd ON special_case_rare_master(kcd_code)",
            "CREATE INDEX IF NOT EXISTS idx_special_vcode ON special_case_rare_master(special_code)"
        ]
        for sql in index_sql:
            try:
                cur.execute(sql)
            except sqlite3.OperationalError:
                pass
        conn.commit()
