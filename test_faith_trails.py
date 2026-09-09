"""Automated integration tests for Faith-Trails.

Place this file in the main project folder beside app.py and schema.sql.
Run from that folder with:

    python -m unittest test_faith_trails.py -v

The tests create a temporary SQLite database. They do not modify the real
faith_trails.db file or any saved player progress.
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path

import app as faith_trails


PROJECT_DIR = Path(__file__).resolve().parent


class FaithTrailsIntegrationTests(unittest.TestCase):
    """Test the Flask routes, API operations, and database integration."""

    def setUp(self):
        """Create a fresh database and Flask client for each test."""
        self.temporary_folder = tempfile.TemporaryDirectory()
        self.test_database = Path(self.temporary_folder.name) / "test.db"

        database = sqlite3.connect(self.test_database)
        database.executescript(
            (PROJECT_DIR / "schema.sql").read_text(encoding="utf-8")
        )
        database.close()

        faith_trails.DB_PATH = str(self.test_database)
        faith_trails.app.config.update(
            TESTING=True,
            SECRET_KEY="faith-trails-automated-test-key",
        )
        self.client = faith_trails.app.test_client()

    def tearDown(self):
        """Delete the temporary test database after each test."""
        self.temporary_folder.cleanup()

    def create_profile(self, name="Mellie", difficulty="easy"):
        """Create and log in a player for tests that require a profile."""
        return self.client.post(
            "/api/profile",
            json={"name": name, "difficulty": difficulty},
        )

    def test_01_players_page_loads(self):
        response = self.client.get("/players")
        self.assertEqual(response.status_code, 200)

    def test_02_home_redirects_without_profile(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_03_create_profile(self):
        response = self.create_profile()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Mellie")
        self.assertEqual(response.json["difficulty"], "easy")

    def test_04_blank_name_is_rejected(self):
        response = self.create_profile(name=" ")
        self.assertEqual(response.status_code, 400)

    def test_05_invalid_difficulty_is_rejected(self):
        response = self.create_profile(difficulty="expert")
        self.assertEqual(response.status_code, 400)

    def test_06_duplicate_name_is_rejected_case_insensitively(self):
        self.create_profile(name="Mellie")
        self.client.get("/logout")
        response = self.create_profile(name="mellie")
        self.assertEqual(response.status_code, 409)

    def test_07_read_current_profile(self):
        self.create_profile()
        response = self.client.get("/api/profile")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Mellie")
        self.assertEqual(response.json["difficulty"], "easy")

    def test_08_update_profile_name_and_difficulty(self):
        self.create_profile()
        response = self.client.put(
            "/api/profile",
            json={"name": "Mia", "difficulty": "hard"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Mia")
        self.assertEqual(response.json["difficulty"], "hard")

    def test_09_read_all_six_quests(self):
        response = self.client.get("/api/quests")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 6)

    def test_10_every_quest_supports_every_difficulty(self):
        self.create_profile()

        for difficulty in faith_trails.DIFFICULTIES:
            self.client.put(
                "/api/profile",
                json={"difficulty": difficulty},
            )

            for slug in faith_trails.QUEST_CONTENT:
                response = self.client.get(f"/api/quest/{slug}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json["difficulty"], difficulty)

                scene_types = {
                    scene["type"] for scene in response.json["scenes"]
                }
                required_types = {
                    "story",
                    "interactive",
                    "quiz",
                    "memory_verse",
                }
                self.assertTrue(required_types.issubset(scene_types))

    def test_11_unknown_quest_returns_404(self):
        self.create_profile()
        response = self.client.get("/api/quest/not-a-real-quest")
        self.assertEqual(response.status_code, 404)

    def test_12_complete_quest_creates_badge(self):
        self.create_profile()
        response = self.client.post("/api/complete/noahs-ark")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])

    def test_13_duplicate_completion_does_not_duplicate_badge(self):
        self.create_profile()
        self.client.post("/api/complete/noahs-ark")
        self.client.post("/api/complete/noahs-ark")

        progress = self.client.get("/api/progress")
        self.assertEqual(len(progress.json["earned"]), 1)

    def test_14_read_saved_progress(self):
        self.create_profile()
        self.client.post("/api/complete/noahs-ark")

        response = self.client.get("/api/progress")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["earned"]), 1)

    def test_15_difficulty_change_preserves_prior_badges(self):
        self.create_profile()
        self.client.post("/api/complete/noahs-ark")
        self.client.put(
            "/api/profile",
            json={"difficulty": "medium"},
        )
        self.client.post("/api/complete/noahs-ark")

        progress = self.client.get("/api/progress")
        self.assertEqual(len(progress.json["earned"]), 2)

    def test_16_delete_earned_badge(self):
        self.create_profile()
        self.client.post("/api/complete/noahs-ark")

        response = self.client.delete("/api/reset/noahs-ark")
        self.assertEqual(response.status_code, 200)

        progress = self.client.get("/api/progress")
        self.assertEqual(len(progress.json["earned"]), 0)

    def test_17_delete_missing_badge_returns_404(self):
        self.create_profile()
        response = self.client.delete("/api/reset/noahs-ark")
        self.assertEqual(response.status_code, 404)

    def test_18_progress_api_requires_a_profile(self):
        response = self.client.get("/api/progress")
        self.assertEqual(response.status_code, 401)

    def test_19_badges_and_hall_of_fame_pages_load(self):
        self.create_profile()
        self.assertEqual(self.client.get("/badges").status_code, 200)
        self.assertEqual(self.client.get("/hall-of-fame").status_code, 200)

    def test_20_all_18_badges_are_saved(self):
        self.create_profile()

        for difficulty in faith_trails.DIFFICULTIES:
            self.client.put(
                "/api/profile",
                json={"difficulty": difficulty},
            )
            for slug in faith_trails.QUEST_CONTENT:
                self.client.post(f"/api/complete/{slug}")

        progress = self.client.get("/api/progress")
        self.assertEqual(len(progress.json["earned"]), 18)


if __name__ == "__main__":
    unittest.main(verbosity=2)
