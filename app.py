"""
Faith Trails: A Closer Walk for Kids
Flask application entry point.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""
import sqlite3
import json
import random
from flask import Flask, render_template, g, jsonify, abort, request

DB_PATH = "faith_trails.db"
DEMO_USER_ID = 1  # single local profile for the MVP; multi-profile support is a future step

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# ---------------------------------------------------------------------------
# Quest content
# Each quest is a linear list of "scenes." A scene is either a story beat
# (illustrated text, tap Next to continue), an interactive checkpoint
# (a hands-on activity, like drag-and-drop), a "quiz" comprehension check
# (multiple choice, drawn from the story just told), or the closing
# "memory_verse" challenge (rebuild the verse in order, then identify its
# reference) that must be completed correctly before the badge is awarded.
# This structure is the reusable "quest engine" described in the Statement
# of Work: adding a new Bible story means adding a new entry here, not
# writing new page logic.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Quest content
# Each quest has:
#   - "story_scenes": the fixed story beats and interactive checkpoint, in
#     order. These never change between playthroughs — the Bible story
#     itself doesn't change.
#   - "quiz_bank": a pool of quiz questions. A random sample is drawn each
#     time the quest is played, so replaying serves different questions.
#   - "quiz_count": how many quiz questions to draw from the bank per play.
#   - "verse_bank": a pool of memory verses tied to the same lesson. One
#     is chosen at random each play, so a replay can serve a different
#     verse rather than repeating the same one.
#   - "lesson": the takeaway shown on the final badge screen.
# This structure is the reusable "quest engine" described in the Statement
# of Work: adding a new Bible story means adding a new entry here, not
# writing new page logic. See the quest() route below for how these pieces
# are assembled into the final scene list on each visit.
# ---------------------------------------------------------------------------

QUEST_CONTENT = {
    "noahs-ark": {
        "title": "Noah's Ark",
        "story_scenes": [
            {
                "type": "story",
                "emoji": "🌧️",
                "text": "Long ago, God saw that the world had grown very unkind. "
                        "But there was one man who still loved Him — Noah.",
            },
            {
                "type": "story",
                "emoji": "🛠️",
                "text": "God asked Noah to build a giant boat called an ark, "
                        "big enough for his family and two of every animal.",
            },
            {
                "type": "interactive",
                "subtype": "matching",
                "prompt": "Drag each animal into the ark to help Noah gather them, two by two!",
                "items": [
                    {"id": "lion", "emoji": "🦁", "label": "Lion"},
                    {"id": "elephant", "emoji": "🐘", "label": "Elephant"},
                    {"id": "dove", "emoji": "🕊️", "label": "Dove"},
                    {"id": "zebra", "emoji": "🦓", "label": "Zebra"},
                ],
            },
            {
                "type": "story",
                "emoji": "🌊",
                "text": "The rain fell for forty days and forty nights. "
                        "But Noah, his family, and all the animals stayed safe inside the ark.",
            },
            {
                "type": "story",
                "emoji": "🌈",
                "text": "When the rain finally stopped, God placed a rainbow in the sky "
                        "as a promise: He would never destroy the whole Earth by flood again.",
            },
        ],
        "quiz_bank": [
            {
                "type": "quiz",
                "prompt": "What did God see about the world?",
                "options": [
                    "It had grown very unkind",
                    "It was full of rainbows",
                    "It needed more animals",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "How did Noah gather the animals for the ark?",
                "options": [
                    "He brought two of every animal",
                    "He brought only lions",
                    "He left the animals behind",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "Who did God ask to build the ark?",
                "options": [
                    "Noah",
                    "Moses",
                    "Abraham",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "What did God place in the sky as a promise?",
                "options": [
                    "A rainbow",
                    "A shooting star",
                    "A cloud shaped like a dove",
                ],
                "correct_index": 0,
            },
        ],
        "quiz_count": 2,
        "verse_bank": [
            {
                "type": "memory_verse",
                "verse": "Noah found favor in the eyes of the Lord.",
                "reference": "Genesis 6:8",
                "reference_options": [
                    "Genesis 6:8",
                    "Genesis 3:8",
                    "Exodus 6:8",
                ],
            },
            {
                "type": "memory_verse",
                "verse": "Noah was a righteous man, blameless among the people of his time, and he walked faithfully with God.",
                "reference": "Genesis 6:9",
                "reference_options": [
                    "Genesis 6:9",
                    "Genesis 9:6",
                    "Exodus 6:9",
                ],
            },
        ],
        "lesson": "God keeps His promises, even when things feel scary.",
    },
    "josephs-coat": {
        "title": "Joseph's Colorful Coat",
        "story_scenes": [
            {
                "type": "story",
                "emoji": "🧡",
                "text": "Jacob loved his son Joseph very much, and gave him a beautiful, "
                        "colorful coat as a special gift.",
            },
            {
                "type": "story",
                "emoji": "😠",
                "text": "When Joseph's brothers saw the coat, they grew jealous. "
                        "It seemed like their father loved Joseph the most of all.",
            },
            {
                "type": "interactive",
                "subtype": "color_picker",
                "prompt": "Help design Joseph's colorful coat! Tap 5 colors to fill it in.",
                "target_count": 5,
                "palette": [
                    {"name": "Red", "hex": "#C1652F"},
                    {"name": "Gold", "hex": "#D9A73B"},
                    {"name": "Green", "hex": "#2F5233"},
                    {"name": "Blue", "hex": "#3B7A9C"},
                    {"name": "Purple", "hex": "#7B5CA8"},
                    {"name": "Teal", "hex": "#3B9C8A"},
                ],
            },
            {
                "type": "story",
                "emoji": "😢",
                "text": "The brothers' jealousy grew so strong that they treated Joseph "
                        "unkindly and sent him far away, all the way to Egypt.",
            },
            {
                "type": "story",
                "emoji": "🕊️",
                "text": "Everything felt scary and unfair. But even in a brand new land, "
                        "far from home, Joseph trusted that God was with him.",
            },
        ],
        "quiz_bank": [
            {
                "type": "quiz",
                "prompt": "How did Joseph's brothers feel about his colorful coat?",
                "options": [
                    "Jealous",
                    "Excited for him",
                    "They didn't notice it",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "Even when things felt scary and unfair, what did Joseph do?",
                "options": [
                    "He trusted that God was with him",
                    "He gave up hope",
                    "He ran away and hid forever",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "What did Jacob give Joseph as a special gift?",
                "options": [
                    "A beautiful, colorful coat",
                    "A golden crown",
                    "A wooden sword",
                ],
                "correct_index": 0,
            },
            {
                "type": "quiz",
                "prompt": "Where did Joseph's brothers send him?",
                "options": [
                    "Egypt",
                    "Jerusalem",
                    "Rome",
                ],
                "correct_index": 0,
            },
        ],
        "quiz_count": 2,
        "verse_bank": [
            {
                "type": "memory_verse",
                "verse": "The Lord was with Joseph, and he prospered.",
                "reference": "Genesis 39:2",
                "reference_options": [
                    "Genesis 39:2",
                    "Genesis 3:2",
                    "Exodus 39:2",
                ],
            },
            {
                "type": "memory_verse",
                "verse": "Trust in the Lord with all your heart and lean not on your own understanding.",
                "reference": "Proverbs 3:5",
                "reference_options": [
                    "Proverbs 3:5",
                    "Psalm 3:5",
                    "Proverbs 3:8",
                ],
            },
        ],
        "lesson": "God is with us, even when things feel hard or unfair.",
    },
}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Trail map: shows every quest and which ones are already completed.
    If the player hasn't created a name yet, show the onboarding screen
    instead."""
    db = get_db()
    profile = db.execute(
        "SELECT * FROM users WHERE id = ?", (DEMO_USER_ID,)
    ).fetchone()

    if not profile["name"]:
        return render_template("create_profile.html")

    quests = db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]
        for row in db.execute(
            "SELECT quest_id FROM badges_earned WHERE user_id = ?", (DEMO_USER_ID,)
        ).fetchall()
    }
    return render_template("home.html", quests=quests, earned=earned, profile=profile)


@app.route("/badges")
def badges():
    """Badge case: shows every badge the player has earned so far, plus
    the ones still waiting to be earned, all in one place."""
    db = get_db()
    profile = db.execute(
        "SELECT * FROM users WHERE id = ?", (DEMO_USER_ID,)
    ).fetchone()

    if not profile["name"]:
        return render_template("create_profile.html")

    quests = db.execute(
        "SELECT * FROM quests WHERE is_available = 1 ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]: row["earned_at"]
        for row in db.execute(
            "SELECT quest_id, earned_at FROM badges_earned WHERE user_id = ?", (DEMO_USER_ID,)
        ).fetchall()
    }
    return render_template("badges.html", quests=quests, earned=earned, profile=profile)


@app.route("/quest/<slug>")
def quest(slug):
    db = get_db()
    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        abort(404)

    if not quest_row["is_available"]:
        return render_template("coming_soon.html", quest=quest_row)

    content = QUEST_CONTENT.get(slug)
    if content is None:
        abort(404)

    # Build this playthrough's scene list: the story beats and interactive
    # checkpoint are always the same, but the quiz questions and memory
    # verse are drawn fresh from their pools each visit, so replaying a
    # quest doesn't just repeat the exact same questions.
    quiz_count = min(content.get("quiz_count", 2), len(content["quiz_bank"]))
    scenes = (
        content["story_scenes"]
        + random.sample(content["quiz_bank"], k=quiz_count)
        + [random.choice(content["verse_bank"])]
    )

    return render_template(
        "quest.html",
        quest=quest_row,
        scenes_json=json.dumps(scenes),
        lesson=content["lesson"],
    )


@app.route("/api/complete/<slug>", methods=["POST"])
def complete_quest(slug):
    """CREATE: called by the front end once a child finishes every scene
    in a quest. Records a new badge for that quest."""
    db = get_db()
    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    db.execute(
        "INSERT OR IGNORE INTO badges_earned (user_id, quest_id) VALUES (?, ?)",
        (DEMO_USER_ID, quest_row["id"]),
    )
    db.commit()

    return jsonify({"success": True, "badge_icon": quest_row["icon"]})


@app.route("/api/quests", methods=["GET"])
def api_quests():
    """READ: returns every quest as JSON, including whether the demo user
    has earned its badge yet. Useful for testing the API layer directly
    (e.g. visiting /api/quests in the browser) and for any future screen
    that needs quest data without a full page reload."""
    db = get_db()
    quests = db.execute("SELECT * FROM quests ORDER BY sort_order").fetchall()
    earned = {
        row["quest_id"]
        for row in db.execute(
            "SELECT quest_id FROM badges_earned WHERE user_id = ?", (DEMO_USER_ID,)
        ).fetchall()
    }

    return jsonify([
        {
            "slug": q["slug"],
            "title": q["title"],
            "summary": q["summary"],
            "icon": q["icon"],
            "is_available": bool(q["is_available"]),
            "earned": q["id"] in earned,
        }
        for q in quests
    ])


@app.route("/api/profile", methods=["POST"])
def create_profile():
    """CREATE: sets the player's name for the first time, during onboarding.
    (Separate from the PUT endpoint below, which handles later renames.)"""
    data = request.get_json(silent=True) or {}
    new_name = (data.get("name") or "").strip()

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET name = ? WHERE id = ?", (new_name, DEMO_USER_ID)
    )
    db.commit()

    return jsonify({"success": True, "id": DEMO_USER_ID, "name": new_name}), 201


@app.route("/api/profile", methods=["GET"])
def get_profile():
    """READ: returns the demo user's current profile name."""
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (DEMO_USER_ID,)
    ).fetchone()
    return jsonify({"id": user["id"], "name": user["name"]})


@app.route("/api/profile", methods=["PUT"])
def update_profile():
    """UPDATE: lets a child (or parent) change the profile name shown in
    the app, e.g. from the default "Explorer" to the child's own name.
    Expects a JSON body like {"name": "Aria"}."""
    data = request.get_json(silent=True) or {}
    new_name = (data.get("name") or "").strip()

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET name = ? WHERE id = ?", (new_name, DEMO_USER_ID)
    )
    db.commit()

    return jsonify({"success": True, "id": DEMO_USER_ID, "name": new_name})


@app.route("/api/reset/<slug>", methods=["DELETE"])
def reset_badge(slug):
    """DELETE: removes an earned badge for a quest, so the demo user can
    replay it. Also useful during development/testing."""
    db = get_db()
    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    cursor = db.execute(
        "DELETE FROM badges_earned WHERE user_id = ? AND quest_id = ?",
        (DEMO_USER_ID, quest_row["id"]),
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "message": "No badge was earned for this quest"}), 404

    return jsonify({"success": True, "message": f"Badge for '{quest_row['title']}' has been reset"})


if __name__ == "__main__":
    app.run(debug=True)
