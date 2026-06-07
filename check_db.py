from __future__ import annotations

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
db_path = os.getenv("DB_PATH", "db/medical_master.db")
with sqlite3.connect(db_path) as conn:
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    for (name,) in rows:
        cnt = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        print(f"{name}: {cnt:,}건")
