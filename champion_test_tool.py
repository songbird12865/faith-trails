"""Prepare or remove a safe 17-badge Faith-Trails Champion test player.

Windows PowerShell:
    python champion_test_tool.py setup
    python champion_test_tool.py status
    python champion_test_tool.py cleanup
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


DATABASE_NAME = "faith_trails.db"
TEST_PLAYER_NAME = "Champion Test Player"
FINAL_QUEST_SLUG = "daniel-lions-den"
FINAL_DIFFICULTY = "hard"
DIFFICULTIES = ("easy", "medium", "hard")
EXPECTED_QUEST_SLUGS = (
    "noahs-ark",
    "josephs-coat",
    "red-sea",
    "david-goliath",
    "jonah-big-fish",
    "daniel-lions-den",
)


def database_path() -> Path:
    return Path(__file__).resolve().parent / DATABASE_NAME


def connect_database() -> sqlite3.Connection:
    """Open the local database with row names and foreign keys enabled."""
    path = database_path()
    if not path.is_file():
        raise SystemExit(
            f"ERROR: {DATABASE_NAME} was not found next to this script.\n"
            "Copy champion_test_tool.py into your Faith-Trails project folder, then run it there."
        )
    database = sqlite3.connect(path)
    database.row_factory = sqlite3.Row
    database.execute("PRAGMA foreign_keys = ON")
    return database


def verify_schema(database: sqlite3.Connection) -> list[sqlite3.Row]:
    """Refuse to modify a database unless the expected six-quest schema exists."""
    table_names = {
        row["name"]
        for row in database.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    required_tables = {"users", "quests", "badges_earned"}
    if not required_tables.issubset(table_names):
        raise SystemExit(
            "ERROR: This does not appear to be the Faith-Trails database. No changes were made."
        )

    placeholders = ",".join("?" for _ in EXPECTED_QUEST_SLUGS)
    quests = database.execute(
        f"""SELECT id, slug, title, is_available
            FROM quests
            WHERE slug IN ({placeholders})
            ORDER BY sort_order""",
        EXPECTED_QUEST_SLUGS,
    ).fetchall()
    found_slugs = {row["slug"] for row in quests}
    missing = set(EXPECTED_QUEST_SLUGS) - found_slugs
    if missing:
        raise SystemExit(
            "ERROR: The unified six-quest update is not fully installed. Missing: "
            + ", ".join(sorted(missing))
            + ". No changes were made."
        )
    if any(not row["is_available"] for row in quests):
        raise SystemExit(
            "ERROR: One or more of the six quests is not available. Run "
            "apply_unified_update.py first. No changes were made."
        )
    return quests


def make_backup() -> Path:
    """Create a timestamped recovery copy before changing test data."""
    source = database_path()
    backup_dir = source.parent / "test_backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = backup_dir / f"faith_trails-before-champion-test-{timestamp}.db"
    shutil.copy2(source, destination)
    return destination


def get_test_player(database: sqlite3.Connection) -> sqlite3.Row | None:
    return database.execute(
        "SELECT id, name, current_difficulty FROM users WHERE name = ? COLLATE NOCASE",
        (TEST_PLAYER_NAME,),
    ).fetchone()


def setup_test() -> None:
    """Prepare one isolated player with exactly 17 of the 18 badges."""
    database = connect_database()
    try:
        quests = verify_schema(database)
        backup = make_backup()

        with database:
            player = get_test_player(database)
            if player is None:
                cursor = database.execute(
                    "INSERT INTO users (name, current_difficulty) VALUES (?, ?)",
                    (TEST_PLAYER_NAME, FINAL_DIFFICULTY),
                )
                player_id = cursor.lastrowid
            else:
                player_id = player["id"]
                database.execute(
                    "UPDATE users SET current_difficulty = ? WHERE id = ?",
                    (FINAL_DIFFICULTY, player_id),
                )

            # Modify badges belonging only to the specially named test player.
            database.execute(
                "DELETE FROM badges_earned WHERE user_id = ?", (player_id,)
            )
            final_quest_id = next(
                row["id"] for row in quests if row["slug"] == FINAL_QUEST_SLUG
            )
            for quest in quests:
                for difficulty in DIFFICULTIES:
                    if quest["id"] == final_quest_id and difficulty == FINAL_DIFFICULTY:
                        continue
                    database.execute(
                        """INSERT INTO badges_earned (user_id, quest_id, difficulty)
                           VALUES (?, ?, ?)""",
                        (player_id, quest["id"], difficulty),
                    )

        earned = database.execute(
            "SELECT COUNT(*) AS total FROM badges_earned WHERE user_id = ?",
            (player_id,),
        ).fetchone()["total"]
        if earned != 17:
            raise RuntimeError(f"Safety check failed: expected 17 badges, found {earned}.")

        print("\nCHAMPION TEST IS READY")
        print(f"Backup created: {backup}")
        print(f"Test player: {TEST_PLAYER_NAME}")
        print("Badges prepared: 17 of 18")
        print("Difficulty selected: Hard")
        print("Badge left to earn: Daniel and the Lions' Den — Hard")
        print("\nNext:")
        print("1. Start Faith-Trails with: python app.py")
        print(f"2. Choose the player named: {TEST_PLAYER_NAME}")
        print("3. Open Daniel and the Lions' Den and complete it.")
        print("4. The Grand Champion celebration should start after that badge.")
    finally:
        database.close()


def show_status() -> None:
    database = connect_database()
    try:
        verify_schema(database)
        player = get_test_player(database)
        if player is None:
            print(f"No player named '{TEST_PLAYER_NAME}' exists.")
            return
        total = database.execute(
            "SELECT COUNT(*) AS total FROM badges_earned WHERE user_id = ?",
            (player["id"],),
        ).fetchone()["total"]
        final_badge = database.execute(
            """SELECT COUNT(*) AS total
               FROM badges_earned b
               JOIN quests q ON q.id = b.quest_id
               WHERE b.user_id = ? AND q.slug = ? AND b.difficulty = ?""",
            (player["id"], FINAL_QUEST_SLUG, FINAL_DIFFICULTY),
        ).fetchone()["total"]
        print(f"Test player: {TEST_PLAYER_NAME}")
        print(f"Difficulty: {player['current_difficulty']}")
        print(f"Badges: {total} of 18")
        print(
            "Daniel Hard: "
            + ("earned — Champion should be unlocked" if final_badge else "not earned — ready for final test")
        )
    finally:
        database.close()


def cleanup_test() -> None:
    """Delete only the specially named test player and that player's badges."""
    database = connect_database()
    try:
        verify_schema(database)
        player = get_test_player(database)
        if player is None:
            print(f"Nothing to remove. '{TEST_PLAYER_NAME}' does not exist.")
            return
        player_id = player["id"]
        with database:
            deleted_badges = database.execute(
                "DELETE FROM badges_earned WHERE user_id = ?", (player_id,)
            ).rowcount
            deleted_players = database.execute(
                "DELETE FROM users WHERE id = ? AND name = ? COLLATE NOCASE",
                (player_id, TEST_PLAYER_NAME),
            ).rowcount
        if deleted_players != 1:
            raise RuntimeError("Safety check failed while removing the test player.")
        print("\nCHAMPION TEST PLAYER REMOVED")
        print(f"Removed player: {TEST_PLAYER_NAME}")
        print(f"Removed test badges: {deleted_badges}")
        print("Your other players and their progress were not changed.")
        print("The automatic backup in the test_backups folder was kept.")
    finally:
        database.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare, inspect, or remove a safe Faith-Trails Champion test player."
    )
    parser.add_argument("command", choices=("setup", "status", "cleanup"))
    arguments = parser.parse_args()
    try:
        {"setup": setup_test, "status": show_status, "cleanup": cleanup_test}[
            arguments.command
        ]()
    except (sqlite3.Error, OSError, RuntimeError) as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
