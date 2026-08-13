"""Safely unlock the final three quests in an existing Faith-Trails database."""
import sqlite3
from pathlib import Path

database_path = Path(__file__).resolve().parent / "faith_trails.db"
if not database_path.exists():
    raise SystemExit("faith_trails.db was not found. Put this file in the Faith-Trails project folder and run it again.")

with sqlite3.connect(database_path) as database:
    database.execute(
        """UPDATE quests SET is_available = 1
           WHERE slug IN ('david-goliath', 'jonah-big-fish', 'daniel-lions-den')"""
    )
    database.commit()

print("Faith-Trails unified update applied. Existing players and badges were preserved.")
