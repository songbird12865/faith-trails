"""
Run this once (and any time you want to reset your data) to build
faith_trails.db from schema.sql.

    python init_db.py
"""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "faith_trails.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")

if __name__ == "__main__":
    init_db()
