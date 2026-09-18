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
from copy import deepcopy
from pathlib import Path

import app as faith_trails
from narration_utils import build_narration_index, narration_filename


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

    def test_09_read_complete_25_quest_roadmap(self):
        response = self.client.get("/api/quests")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 25)
        self.assertEqual(sum(quest["is_available"] for quest in response.json), 25)
        self.assertEqual({quest["series_number"] for quest in response.json}, {1, 2, 3, 4, 5})

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

    def test_20_all_current_playable_badges_are_saved(self):
        self.create_profile()

        for difficulty in faith_trails.DIFFICULTIES:
            self.client.put(
                "/api/profile",
                json={"difficulty": difficulty},
            )
            for slug in faith_trails.QUEST_CONTENT:
                self.client.post(f"/api/complete/{slug}")

        progress = self.client.get("/api/progress")
        self.assertEqual(len(progress.json["earned"]), 75)

    def test_21_series_one_contains_five_playable_quests(self):
        self.create_profile()
        progress = self.client.get("/api/progress")
        first_series = [
            quest for quest in progress.json["quests"]
            if quest["series_number"] == 1
        ]
        self.assertEqual(len(first_series), 5)
        self.assertTrue(all(quest["is_available"] for quest in first_series))
        self.assertEqual(
            {quest["slug"] for quest in first_series},
            {"creation", "noahs-ark", "jonah-big-fish", "daniel-lions-den", "red-sea"},
        )

    def test_22_interactive_activity_follows_complete_story(self):
        self.create_profile()

        for slug in faith_trails.QUEST_CONTENT:
            response = self.client.get(f"/api/quest/{slug}")
            scenes = response.json["scenes"]
            interactive_index = next(
                index for index, scene in enumerate(scenes)
                if scene["type"] == "interactive"
            )
            story_indexes = [
                index for index, scene in enumerate(scenes)
                if scene["type"] == "story"
            ]
            self.assertGreater(interactive_index, max(story_indexes), slug)

    def test_23_series_two_contains_five_playable_quests(self):
        self.create_profile()
        progress = self.client.get("/api/progress")
        second_series = [
            quest for quest in progress.json["quests"]
            if quest["series_number"] == 2
        ]
        self.assertEqual(len(second_series), 5)
        self.assertTrue(all(quest["is_available"] for quest in second_series))
        self.assertEqual(
            {quest["slug"] for quest in second_series},
            {"josephs-coat", "abraham", "jacob", "ruth", "samuel"},
        )

    def test_24_narration_index_assigns_each_quest_its_series_voice(self):
        for item in faith_trails.NARRATION_INDEX:
            self.assertIn("series_number", item)
            self.assertEqual(
                item["voice_id"],
                faith_trails.SERIES_VOICE_IDS[item["series_number"]],
            )

    def test_25_voice_change_creates_a_separate_audio_cache_name(self):
        sample = {
            "abraham": {
                "intro_scenes": [{"type": "story", "text": "God called Abraham."}],
            }
        }
        original = faith_trails.DEFAULT_ELEVENLABS_VOICE_ID
        default_index = build_narration_index(
            deepcopy(sample),
            {"abraham": 2},
            {2: original},
            original,
        )
        new_voice_index = build_narration_index(
            deepcopy(sample),
            {"abraham": 2},
            {2: "a-different-series-two-voice"},
            original,
        )
        self.assertEqual(
            default_index[0]["filename"],
            narration_filename("abraham__intro__0", "God called Abraham."),
        )
        self.assertNotEqual(
            default_index[0]["filename"], new_voice_index[0]["filename"]
        )
        self.assertIn("__voice-", new_voice_index[0]["filename"])

    def test_26_scene_image_metadata_reaches_the_browser_api(self):
        self.create_profile()
        response = self.client.get("/api/quest/abraham")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["scenes"][0]["image"], "abraham/01.webp")

    def test_27_frontend_preloads_and_falls_back_for_scene_art(self):
        javascript = (PROJECT_DIR / "static" / "js" / "game.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("preloadNextSceneImage", javascript)
        self.assertIn("loader.onerror=()=>apply(cover)", javascript)
        self.assertIn("/static/img/quests/scenes/", javascript)

    def test_28_every_playable_series_story_has_scene_art(self):
        self.create_profile()
        expected_total = 0
        delivered_total = 0
        for slug, series_number in faith_trails.QUEST_SERIES.items():
            if series_number not in {1, 2, 3, 4, 5}:
                continue
            expected_total += len(faith_trails.QUEST_CONTENT[slug]["intro_scenes"])
            expected_total += len(faith_trails.QUEST_CONTENT[slug]["outro_scenes"])
            response = self.client.get(f"/api/quest/{slug}")
            story_scenes = [
                scene for scene in response.json["scenes"]
                if scene["type"] == "story"
            ]
            for scene in story_scenes:
                self.assertIn("image", scene, slug)
                image_path = PROJECT_DIR / "static" / "img" / "quests" / "scenes" / scene["image"]
                self.assertTrue(image_path.exists(), image_path)
                delivered_total += 1
        self.assertEqual(expected_total, 142)
        self.assertEqual(delivered_total, 142)

    def test_29_series_three_contains_five_playable_quests(self):
        self.create_profile()
        progress = self.client.get("/api/progress")
        third_series = [
            quest for quest in progress.json["quests"]
            if quest["series_number"] == 3
        ]
        self.assertEqual(len(third_series), 5)
        self.assertTrue(all(quest["is_available"] for quest in third_series))
        self.assertEqual(
            {quest["slug"] for quest in third_series},
            {"david-goliath", "apostles-pentecost", "gideon", "esther", "jericho"},
        )

    def test_30_series_three_verses_are_child_sized(self):
        for slug in {"david-goliath", "apostles-pentecost", "gideon", "esther", "jericho"}:
            content = faith_trails.QUEST_CONTENT[slug]
            for difficulty in faith_trails.DIFFICULTIES:
                selected = content["verse_bank_by_difficulty"][difficulty][0]
                self.assertLessEqual(len(selected["verse"].split()), 18, f"{slug}:{difficulty}")

    def test_31_series_four_contains_five_playable_quests(self):
        self.create_profile()
        progress = self.client.get("/api/progress")
        fourth_series = [
            quest for quest in progress.json["quests"]
            if quest["series_number"] == 4
        ]
        self.assertEqual(len(fourth_series), 5)
        self.assertTrue(all(quest["is_available"] for quest in fourth_series))
        self.assertEqual(
            {quest["slug"] for quest in fourth_series},
            {"solomon", "ten-commandments", "elijah", "nehemiah", "job"},
        )

    def test_32_series_four_verses_follow_age_related_lengths(self):
        limits = {"easy": 8, "medium": 12, "hard": 20}
        series_four = {"solomon", "ten-commandments", "elijah", "nehemiah", "job"}
        for slug in series_four:
            content = faith_trails.QUEST_CONTENT[slug]
            for difficulty, maximum_words in limits.items():
                selected = content["verse_bank_by_difficulty"][difficulty][0]
                self.assertLessEqual(
                    len(selected["verse"].split()),
                    maximum_words,
                    f"{slug}:{difficulty}",
                )

    def test_33_series_four_uses_distinct_verses_by_difficulty(self):
        series_four = {"solomon", "ten-commandments", "elijah", "nehemiah", "job"}
        for slug in series_four:
            verses = {
                faith_trails.QUEST_CONTENT[slug]["verse_bank_by_difficulty"][difficulty][0]["verse"]
                for difficulty in faith_trails.DIFFICULTIES
            }
            self.assertEqual(len(verses), 3, slug)

    def test_34_series_five_contains_five_playable_quests(self):
        self.create_profile()
        progress = self.client.get("/api/progress")
        fifth_series = [
            quest for quest in progress.json["quests"]
            if quest["series_number"] == 5
        ]
        self.assertEqual(len(fifth_series), 5)
        self.assertTrue(all(quest["is_available"] for quest in fifth_series))
        self.assertEqual(
            {quest["slug"] for quest in fifth_series},
            {"nativity", "beatitudes", "good-samaritan", "feeding-5000", "easter"},
        )

    def test_35_series_five_uses_the_approved_memory_verses(self):
        approved = {
            ("nativity", "easy"): ("Glory to God in the Highest.", "Luke 2:14"),
            ("nativity", "medium"): ("Let's go to Bethlehem, now, and see this thing that has happened.", "Luke 2:15"),
            ("nativity", "hard"): ("For there is born to you today, in David's city, a Savior, who is Christ the Lord.", "Luke 2:11"),
            ("beatitudes", "easy"): ("You are the salt of the earth.", "Matthew 5:13"),
            ("beatitudes", "medium"): ("Blessed are the merciful, for they shall obtain mercy.", "Matthew 5:7"),
            ("beatitudes", "hard"): ("Even so, let your light shine before men, that they may see your good works.", "Matthew 5:16"),
            ("good-samaritan", "easy"): ("Go and do likewise.", "Luke 10:37"),
            ("good-samaritan", "medium"): ("Now which of these three do you think seemed to be a good neighbor?", "Luke 10:36"),
            ("good-samaritan", "hard"): ("You shall love the Lord your God with all your heart, with all your soul, with all your strength, and with all your mind.", "Luke 10:27"),
            ("feeding-5000", "easy"): ('Jesus said, "Have the people sit down."', "John 6:10"),
            ("feeding-5000", "medium"): ("He who comes to me I will in no way throw out.", "John 6:37"),
            ("feeding-5000", "hard"): ("I am the bread of life. Whoever comes to me will not be hungry.", "John 6:35"),
            ("easter", "easy"): ("He is not here, for he has risen.", "Matthew 28:6"),
            ("easter", "medium"): ("Go quickly and tell his disciples, 'He is risen from the dead.'", "Matthew 28:7"),
            ("easter", "hard"): ("Go and make disciples of all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Spirit.", "Matthew 28:19"),
        }
        for (slug, difficulty), expected in approved.items():
            selected = faith_trails.QUEST_CONTENT[slug]["verse_bank_by_difficulty"][difficulty][0]
            self.assertEqual((selected["verse"], selected["reference"]), expected)

    def test_36_series_five_uses_distinct_verses_by_difficulty(self):
        series_five = {"nativity", "beatitudes", "good-samaritan", "feeding-5000", "easter"}
        for slug in series_five:
            verses = {
                faith_trails.QUEST_CONTENT[slug]["verse_bank_by_difficulty"][difficulty][0]["verse"]
                for difficulty in faith_trails.DIFFICULTIES
            }
            self.assertEqual(len(verses), 3, slug)

    def test_37_series_five_uses_the_fifth_narrator(self):
        series_five_files = {
            item["filename"] for item in faith_trails.NARRATION_INDEX
            if item["series_number"] == 5
        }
        self.assertTrue(series_five_files)
        for item in faith_trails.NARRATION_INDEX:
            if item["series_number"] == 5:
                self.assertEqual(item["voice_id"], faith_trails.SERIES_VOICE_IDS[5])


if __name__ == "__main__":
    unittest.main(verbosity=2)
