"""
Faith Trails: A Closer Walk for Kids
Flask application entry point.

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""
import sqlite3
import json
import random
import secrets
import os
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError
from flask import (
    Flask, render_template, g, jsonify, abort, request,
    session, redirect, url_for, send_file,
)
from narration_utils import build_narration_index

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "faith_trails.db")
DIFFICULTIES = ("easy", "medium", "hard")

app = Flask(__name__)
# Needed for Flask's session cookie (tracks which player is logged in).
# In production, set this from an environment variable instead of
# regenerating it on every restart -- otherwise everyone gets logged out
# each time the server reloads. For the class demo this is fine as-is.
app.secret_key = os.environ.get("FAITH_TRAILS_SECRET_KEY", "faith-trails-local-development-key-change-in-production")

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
#
# DIFFICULTY LEVELS
# The child chooses easy / medium / hard once, when they set up their
# profile (or later, via "Change difficulty" on the trail map). That
# choice applies to every quest they play until they change it again.
# The Bible story itself never changes between difficulties -- only how
# it's tested does:
#   - "intro_scenes" / "outro_scenes": the fixed story beats that surround
#     the interactive checkpoint. These are identical at every difficulty
#     -- the story doesn't get harder, just the challenge around it does.
#   - "interactive_by_difficulty": the hands-on checkpoint, scaled per
#     level (more items to place, more events to sequence, etc).
#   - "quiz_bank_by_difficulty": a pool of quiz questions per level. A
#     random sample is drawn each play, so replaying serves different
#     questions. Harder tiers ask for more specific detail and use
#     closer-sounding wrong answers.
#   - "quiz_count_by_difficulty": how many quiz questions to draw per
#     level (hard asks for one more than easy/medium).
#   - "verse_bank_by_difficulty": a pool of memory verses per level. Easy
#     verses are short and familiar; hard verses are longer or use
#     trickier reference options.
#   - "lesson": the takeaway shown on the final badge screen (same at
#     every difficulty).
# Adding a new Bible story still just means adding a new entry here, not
# writing new page logic -- the quest() route below assembles whichever
# pieces match the player's current_difficulty into the final scene list.
# ---------------------------------------------------------------------------

QUEST_CONTENT = {
    "noahs-ark": {
        "title": "Noah's Ark",
        "intro_scenes": [
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
        ],
        "interactive_by_difficulty": {
            "easy": {
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
            "medium": {
                "type": "interactive",
                "subtype": "matching",
                "prompt": "Drag each animal into the ark to help Noah gather them, two by two!",
                "items": [
                    {"id": "lion", "emoji": "🦁", "label": "Lion"},
                    {"id": "elephant", "emoji": "🐘", "label": "Elephant"},
                    {"id": "dove", "emoji": "🕊️", "label": "Dove"},
                    {"id": "zebra", "emoji": "🦓", "label": "Zebra"},
                    {"id": "bear", "emoji": "🐻", "label": "Bear"},
                    {"id": "camel", "emoji": "🐫", "label": "Camel"},
                ],
            },
            "hard": {
                "type": "interactive",
                "subtype": "matching",
                "prompt": "Drag every animal into the ark to help Noah gather them, two by two!",
                "items": [
                    {"id": "lion", "emoji": "🦁", "label": "Lion"},
                    {"id": "elephant", "emoji": "🐘", "label": "Elephant"},
                    {"id": "dove", "emoji": "🕊️", "label": "Dove"},
                    {"id": "zebra", "emoji": "🦓", "label": "Zebra"},
                    {"id": "bear", "emoji": "🐻", "label": "Bear"},
                    {"id": "camel", "emoji": "🐫", "label": "Camel"},
                    {"id": "giraffe", "emoji": "🦒", "label": "Giraffe"},
                    {"id": "kangaroo", "emoji": "🦘", "label": "Kangaroo"},
                ],
            },
        },
        "outro_scenes": [
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
        "quiz_bank_by_difficulty": {
            "easy": [
                {
                    "type": "quiz",
                    "prompt": "Who did God ask to build the ark?",
                    "options": ["Noah", "Moses", "Abraham"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "How many of each animal came onto the ark?",
                    "options": ["Two", "Ten", "One"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What appeared in the sky after the rain stopped?",
                    "options": ["A rainbow", "A shooting star", "A cloud shaped like a dove"],
                    "correct_index": 0,
                },
            ],
            "medium": [
                {
                    "type": "quiz",
                    "prompt": "Why did God want Noah to build the ark?",
                    "options": [
                        "To keep Noah, his family, and the animals safe from the flood",
                        "To give Noah a new home in the mountains",
                        "To help Noah travel across the sea to Egypt",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What did God see about the world that made Him decide to send the flood?",
                    "options": [
                        "It had grown very unkind",
                        "It was too crowded with animals",
                        "It had run out of rain",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "How long did the rain fall?",
                    "options": [
                        "Forty days and forty nights",
                        "Seven days and seven nights",
                        "One whole year",
                    ],
                    "correct_index": 0,
                },
            ],
            "hard": [
                {
                    "type": "quiz",
                    "prompt": "Exactly what did God ask Noah to build?",
                    "options": [
                        "A giant boat called an ark",
                        "A giant boat called a ship",
                        "A giant tower called an ark",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "Besides Noah's family, who else stayed safe inside the ark?",
                    "options": [
                        "All of the animals",
                        "Only the birds",
                        "Noah's neighbors",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What exactly did the rainbow promise?",
                    "options": [
                        "God would never destroy the whole Earth by flood again",
                        "God would never let it rain again",
                        "God would build Noah a second ark someday",
                    ],
                    "correct_index": 0,
                },
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [
                {
                    "type": "memory_verse",
                    "verse": "Noah found favor in the eyes of the Lord.",
                    "reference": "Genesis 6:8",
                    "reference_options": ["Genesis 6:8", "Genesis 3:8", "Exodus 6:8"],
                },
            ],
            "medium": [
                {
                    "type": "memory_verse",
                    "verse": "Noah was a righteous man, blameless among the people of his time, and he walked faithfully with God.",
                    "reference": "Genesis 6:9",
                    "reference_options": ["Genesis 6:9", "Genesis 9:6", "Exodus 6:9"],
                },
            ],
            "hard": [
                {
                    "type": "memory_verse",
                    "verse": "I have set my rainbow in the clouds, and it will be the sign of the covenant between me and the earth.",
                    "reference": "Genesis 9:13",
                    "reference_options": ["Genesis 9:13", "Genesis 6:13", "Exodus 9:13"],
                },
            ],
        },
        "lesson": "God keeps His promises, even when things feel scary.",
    },
    "josephs-coat": {
        "title": "Joseph's Colorful Coat",
        "intro_scenes": [
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
        ],
        "interactive_by_difficulty": {
            "easy": {
                "type": "interactive",
                "subtype": "color_picker",
                "prompt": "Help design Joseph's colorful coat! Tap 4 colors to fill it in.",
                "target_count": 4,
                "palette": [
                    {"name": "Red", "hex": "#C1652F"},
                    {"name": "Gold", "hex": "#D9A73B"},
                    {"name": "Green", "hex": "#2F5233"},
                    {"name": "Blue", "hex": "#3B7A9C"},
                    {"name": "Purple", "hex": "#7B5CA8"},
                    {"name": "Teal", "hex": "#3B9C8A"},
                ],
            },
            "medium": {
                "type": "interactive",
                "subtype": "color_picker",
                "prompt": "Help design Joseph's colorful coat! Tap 6 colors to fill it in.",
                "target_count": 6,
                "palette": [
                    {"name": "Red", "hex": "#C1652F"},
                    {"name": "Gold", "hex": "#D9A73B"},
                    {"name": "Green", "hex": "#2F5233"},
                    {"name": "Blue", "hex": "#3B7A9C"},
                    {"name": "Purple", "hex": "#7B5CA8"},
                    {"name": "Teal", "hex": "#3B9C8A"},
                    {"name": "Coral", "hex": "#E07856"},
                ],
            },
            "hard": {
                "type": "interactive",
                "subtype": "color_picker",
                "prompt": "Help design Joseph's colorful coat! Tap 8 colors to fill it in — try not to "
                          "use any color twice in a row.",
                "target_count": 8,
                "palette": [
                    {"name": "Red", "hex": "#C1652F"},
                    {"name": "Gold", "hex": "#D9A73B"},
                    {"name": "Green", "hex": "#2F5233"},
                    {"name": "Blue", "hex": "#3B7A9C"},
                    {"name": "Purple", "hex": "#7B5CA8"},
                    {"name": "Teal", "hex": "#3B9C8A"},
                    {"name": "Coral", "hex": "#E07856"},
                    {"name": "Mustard", "hex": "#C9A227"},
                ],
            },
        },
        "outro_scenes": [
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
        "quiz_bank_by_difficulty": {
            "easy": [
                {
                    "type": "quiz",
                    "prompt": "What did Jacob give Joseph as a special gift?",
                    "options": ["A beautiful, colorful coat", "A golden crown", "A wooden sword"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "How did Joseph's brothers feel about his colorful coat?",
                    "options": ["Jealous", "Excited for him", "They didn't notice it"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "Where did Joseph's brothers send him?",
                    "options": ["Egypt", "Jerusalem", "Rome"],
                    "correct_index": 0,
                },
            ],
            "medium": [
                {
                    "type": "quiz",
                    "prompt": "Why did Joseph's brothers grow jealous of him?",
                    "options": [
                        "It seemed like their father loved Joseph the most of all",
                        "Joseph had more sheep than they did",
                        "Joseph was the oldest brother",
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
                    "prompt": "What happened to Joseph because of his brothers' jealousy?",
                    "options": [
                        "They treated him unkindly and sent him away",
                        "They gave him an even nicer coat",
                        "They asked their father to punish him",
                    ],
                    "correct_index": 0,
                },
            ],
            "hard": [
                {
                    "type": "quiz",
                    "prompt": "Whose love for Joseph is described as the reason for the gift of the coat?",
                    "options": ["Jacob's, his father", "His brothers'", "Pharaoh's"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What, specifically, seemed unfair to Joseph's brothers?",
                    "options": [
                        "That their father loved Joseph the most of all",
                        "That Joseph refused to share his coat",
                        "That Joseph was given their father's land",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "Even far from home in a brand new land, what did Joseph continue to trust?",
                    "options": [
                        "That God was with him",
                        "That his brothers would come rescue him",
                        "That he would find another coat",
                    ],
                    "correct_index": 0,
                },
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [
                {
                    "type": "memory_verse",
                    "verse": "The Lord was with Joseph, and he prospered.",
                    "reference": "Genesis 39:2",
                    "reference_options": ["Genesis 39:2", "Genesis 3:2", "Exodus 39:2"],
                },
            ],
            "medium": [
                {
                    "type": "memory_verse",
                    "verse": "Trust in the Lord with all your heart and lean not on your own understanding.",
                    "reference": "Proverbs 3:5",
                    "reference_options": ["Proverbs 3:5", "Psalm 3:5", "Proverbs 3:8"],
                },
            ],
            "hard": [
                {
                    "type": "memory_verse",
                    "verse": "You intended to harm me, but God intended it for good, to accomplish what is now being done, the saving of many lives.",
                    "reference": "Genesis 50:20",
                    "reference_options": ["Genesis 50:20", "Genesis 15:20", "Exodus 50:20"],
                },
            ],
        },
        "lesson": "God is with us, even when things feel hard or unfair.",
    },
    "red-sea": {
        "title": "Moses and the Red Sea",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "❤️",
                "text": "God loved His people very much. He wanted them to be happy "
                        "and free, not stuck as slaves in Egypt.",
            },
            {
                "type": "story",
                "emoji": "👴🏼",
                "text": "So God chose a leader to help set His people free — his name "
                        "was Moses!",
            },
            {
                "type": "story",
                "emoji": "😠",
                "text": "But Pharaoh, the ruler of Egypt, was mean and stubborn. "
                        "He refused to let God's people go.",
            },
            {
                "type": "story",
                "emoji": "⚡",
                "text": "God sent trouble after trouble to Egypt, until Pharaoh finally "
                        "gave in and let the people leave.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": {
                "type": "interactive",
                "subtype": "sequence",
                "prompt": "Tap these three events in the order they happened!",
                "items": [
                    {"id": "refuse", "emoji": "😠", "label": "Pharaoh says no"},
                    {"id": "staff", "emoji": "🪄", "label": "Moses raises his staff"},
                    {"id": "cross", "emoji": "🕊️", "label": "The people cross safely"},
                ],
            },
            "medium": {
                "type": "interactive",
                "subtype": "sequence",
                "prompt": "Tap these five events in the order they happened!",
                "items": [
                    {"id": "chosen", "emoji": "👴🏼", "label": "God chooses Moses"},
                    {"id": "refuse", "emoji": "😠", "label": "Pharaoh says no"},
                    {"id": "let-go", "emoji": "🚪", "label": "Pharaoh finally lets them go"},
                    {"id": "staff", "emoji": "🪄", "label": "Moses raises his staff"},
                    {"id": "cross", "emoji": "🕊️", "label": "The people cross safely"},
                ],
            },
            "hard": {
                "type": "interactive",
                "subtype": "sequence",
                "prompt": "Tap all seven events in the exact order they happened!",
                "items": [
                    {"id": "chosen", "emoji": "👴🏼", "label": "God chooses Moses to lead His people"},
                    {"id": "refuse", "emoji": "😠", "label": "Pharaoh refuses to let them go"},
                    {"id": "plagues", "emoji": "⚡", "label": "God sends trouble after trouble to Egypt"},
                    {"id": "let-go", "emoji": "🚪", "label": "Pharaoh finally lets the people go"},
                    {"id": "blocked", "emoji": "🌊", "label": "The Red Sea blocks their path"},
                    {"id": "staff", "emoji": "🪄", "label": "Moses raises his staff and the sea parts"},
                    {"id": "cross", "emoji": "🕊️", "label": "The people cross safely to their new home"},
                ],
            },
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🌊",
                "text": "God's people set out for the land God had promised them. But "
                        "a huge sea, the Red Sea, blocked their path!",
            },
            {
                "type": "story",
                "emoji": "🪄",
                "text": "God told Moses to raise his staff. When he did, God performed "
                        "an amazing miracle — the sea parted, and dry ground appeared! "
                        "God's people walked safely across to their new home.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                {
                    "type": "quiz",
                    "prompt": "Who did God choose to lead His people?",
                    "options": ["Moses", "Pharaoh", "Joseph"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What blocked the people's path?",
                    "options": ["The Red Sea", "A mountain", "A desert"],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What did Moses raise to make the sea part?",
                    "options": ["His staff", "His hand", "A trumpet"],
                    "correct_index": 0,
                },
            ],
            "medium": [
                {
                    "type": "quiz",
                    "prompt": "Why did God want His people to be free?",
                    "options": [
                        "Because He loved them",
                        "Because Pharaoh asked Him to",
                        "Because Egypt was too crowded",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "Why wouldn't Pharaoh let the people go, at first?",
                    "options": [
                        "He was mean and stubborn",
                        "He wanted to go with them",
                        "He didn't have enough food for them",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What finally made Pharaoh let the people go?",
                    "options": [
                        "God sent trouble after trouble to Egypt",
                        "Moses paid him gold",
                        "The people ran away in the night",
                    ],
                    "correct_index": 0,
                },
            ],
            "hard": [
                {
                    "type": "quiz",
                    "prompt": "What happened right after Moses raised his staff?",
                    "options": [
                        "The sea parted and dry ground appeared",
                        "It began to rain",
                        "Pharaoh's soldiers turned back",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What was true about the ground the people walked across?",
                    "options": [
                        "It was dry",
                        "It was covered in sand dunes",
                        "It was frozen solid",
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "quiz",
                    "prompt": "What were God's people trying to reach when the sea blocked their path?",
                    "options": [
                        "The land God had promised them",
                        "Pharaoh's palace",
                        "A mountain to build an altar",
                    ],
                    "correct_index": 0,
                },
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [
                {
                    "type": "memory_verse",
                    "verse": "Moses answered the people, \"Do not be afraid.\"",
                    "reference": "Exodus 14:13",
                    "reference_options": ["Exodus 14:13", "Exodus 4:13", "Genesis 14:13"],
                },
            ],
            "medium": [
                {
                    "type": "memory_verse",
                    "verse": "The Lord will fight for you; you only need to be still.",
                    "reference": "Exodus 14:14",
                    "reference_options": ["Exodus 14:14", "Exodus 4:14", "Genesis 14:14"],
                },
            ],
            "hard": [
                {
                    "type": "memory_verse",
                    "verse": "Then Moses stretched out his hand over the sea, and all that night the Lord drove the sea back with a strong east wind and turned it into dry land.",
                    "reference": "Exodus 14:21",
                    "reference_options": ["Exodus 14:21", "Exodus 4:21", "Genesis 14:21"],
                },
            ],
        },
        "lesson": "When we're afraid, we can be still and trust God to fight for us.",
    },
}

# Attaches a "narration_file" field to every scene/question/verse dict
# above (and a "lesson_narration_file" to each quest), and returns the
# flat list generate_narration.py uses to actually call ElevenLabs. Run
# once here, at import time, so every request already has the filenames
# baked in with zero extra per-request work.
NARRATION_INDEX = build_narration_index(QUEST_CONTENT)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_current_user(db):
    """Returns the users row for whoever is logged in this session, or
    None if nobody's picked a profile yet (session has no user_id, or
    that user_id no longer exists)."""
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


def build_scenes(content, difficulty):
    """Assemble one playthrough's scene list for a given difficulty:
    fixed intro scenes, the difficulty-scaled interactive checkpoint,
    fixed outro scenes, a fresh random sample of quiz questions from
    that difficulty's bank, and one random verse from that difficulty's
    bank."""
    quiz_bank = content["quiz_bank_by_difficulty"][difficulty]
    quiz_count = min(content["quiz_count_by_difficulty"][difficulty], len(quiz_bank))
    verse_bank = content["verse_bank_by_difficulty"][difficulty]

    return (
        content["intro_scenes"]
        + [content["interactive_by_difficulty"][difficulty]]
        + content["outro_scenes"]
        + random.sample(quiz_bank, k=quiz_count)
        + [random.choice(verse_bank)]
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/players")
def players():
    """Who's Playing? Lists every existing profile so a returning player
    can tap their name and pick up where they left off, plus a
    'New Player' tile that leads to create_profile.html."""
    db = get_db()
    all_players = db.execute(
        "SELECT * FROM users ORDER BY name COLLATE NOCASE"
    ).fetchall()
    return render_template("players.html", players=all_players)


@app.route("/players/<int:user_id>/select")
def select_player(user_id):
    """Logs the chosen player in by storing their id in the session,
    then sends them to the trail map."""
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        abort(404)
    session["user_id"] = user_id
    return redirect(url_for("home"))


@app.route("/players/new")
def new_player():
    """Onboarding screen for a brand-new player: choose a name and a
    starting difficulty. Submits to POST /api/profile, which creates
    the user row and logs them in."""
    return render_template("create_profile.html", difficulties=DIFFICULTIES)


@app.route("/logout")
def logout():
    """Clears who's logged in for this browser session. Doesn't touch
    any data -- the player's name, difficulty, and badges are all still
    in the database, waiting for them (or anyone) to log back in."""
    session.pop("user_id", None)
    return redirect(url_for("players"))


@app.route("/")
def home():
    """Trail map: shows every quest and which ones are already completed
    at the logged-in player's current difficulty. If nobody's logged in
    yet, send them to the player picker instead."""
    db = get_db()
    profile = get_current_user(db)

    if profile is None:
        return redirect(url_for("players"))

    quests = db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]
        for row in db.execute(
            "SELECT quest_id FROM badges_earned WHERE user_id = ? AND difficulty = ?",
            (profile["id"], profile["current_difficulty"]),
        ).fetchall()
    }
    return render_template(
        "game.html",
        quests=[dict(q) for q in quests],
        earned=list(earned),
        profile=profile,
        difficulties=DIFFICULTIES,
        initial_quest=None,
    )


@app.route("/badges")
def badges():
    """Badge case: shows every badge the player has earned so far at
    their current difficulty, plus the ones still waiting to be earned."""
    db = get_db()
    profile = get_current_user(db)

    if profile is None:
        return redirect(url_for("players"))

    quests = db.execute(
        "SELECT * FROM quests WHERE is_available = 1 ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]: row["earned_at"]
        for row in db.execute(
            "SELECT quest_id, earned_at FROM badges_earned WHERE user_id = ? AND difficulty = ?",
            (profile["id"], profile["current_difficulty"]),
        ).fetchall()
    }
    return render_template("badges.html", quests=quests, earned=earned, profile=profile)


@app.route("/hall-of-fame")
def hall_of_fame():
    """Hall of Fame: a table view of every badge earned across every
    difficulty at once (unlike the trail map and badge case, which only
    show badges for the profile's current_difficulty). Rows are quests,
    columns are easy/medium/hard -- exactly the view for a child (or
    parent) who wants to see everything they've ever earned in one
    place, not just their current level."""
    db = get_db()
    profile = get_current_user(db)

    if profile is None:
        return redirect(url_for("players"))

    quests = db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()
    earned_rows = db.execute(
        "SELECT quest_id, difficulty, earned_at FROM badges_earned WHERE user_id = ?",
        (profile["id"],),
    ).fetchall()
    # Map of (quest_id, difficulty) -> earned_at, for quick lookup per cell.
    earned = {(row["quest_id"], row["difficulty"]): row["earned_at"] for row in earned_rows}

    return render_template(
        "hall_of_fame.html",
        quests=quests,
        earned=earned,
        profile=profile,
        difficulties=DIFFICULTIES,
    )


@app.route("/quest/<slug>")
def quest(slug):
    db = get_db()
    profile = get_current_user(db)

    if profile is None:
        return redirect(url_for("players"))

    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        abort(404)

    if not quest_row["is_available"]:
        return render_template("coming_soon.html", quest=quest_row)

    if QUEST_CONTENT.get(slug) is None:
        abort(404)

    quests = db.execute("SELECT * FROM quests ORDER BY sort_order").fetchall()
    earned = {
        row["quest_id"]
        for row in db.execute(
            "SELECT quest_id FROM badges_earned WHERE user_id = ? AND difficulty = ?",
            (profile["id"], profile["current_difficulty"]),
        ).fetchall()
    }
    return render_template(
        "game.html",
        quests=[dict(q) for q in quests],
        earned=list(earned),
        profile=profile,
        difficulties=DIFFICULTIES,
        initial_quest=slug,
    )


@app.route("/api/quest/<slug>")
def api_quest(slug):
    """Return one randomized quest playthrough to the permanent game shell."""
    db = get_db()
    profile = get_current_user(db)
    if profile is None:
        return jsonify({"error": "No player logged in"}), 401
    quest_row = db.execute("SELECT * FROM quests WHERE slug = ?", (slug,)).fetchone()
    content = QUEST_CONTENT.get(slug)
    if quest_row is None or content is None:
        return jsonify({"error": "Quest not found"}), 404
    if not quest_row["is_available"]:
        return jsonify({"error": "Quest coming soon"}), 409
    difficulty = profile["current_difficulty"]
    return jsonify({
        "quest": dict(quest_row),
        "difficulty": difficulty,
        "scenes": build_scenes(content, difficulty),
        "lesson": content["lesson"],
        "lesson_narration_file": content.get("lesson_narration_file"),
    })


@app.route("/api/progress")
def api_progress():
    """Badge and all-difficulty progress for animated in-shell collections."""
    db = get_db()
    profile = get_current_user(db)
    if profile is None:
        return jsonify({"error": "No player logged in"}), 401
    quests = [dict(row) for row in db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()]
    earned = [dict(row) for row in db.execute(
        "SELECT quest_id, difficulty, earned_at FROM badges_earned WHERE user_id = ?",
        (profile["id"],),
    ).fetchall()]
    return jsonify({"quests": quests, "earned": earned})


@app.route("/api/narration/<path:filename>")
def api_narration(filename):
    """Serve cached narration, generating a missing file securely on demand."""
    narration_item = next(
        (item for item in NARRATION_INDEX if item["filename"] == filename),
        None,
    )
    if narration_item is None:
        abort(404)

    output_dir = BASE_DIR / "static" / "audio" / "quests"
    output_path = output_dir / filename
    if output_path.exists():
        return send_file(output_path, mimetype="audio/mpeg")

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return jsonify({"error": "ElevenLabs narration is not configured"}), 503

    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "Q4oILuo4P8VeXtE6FMLI")
    payload = json.dumps({
        "text": narration_item["text"],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.8,
            "style": 0.35,
            "use_speaker_boost": True,
        },
    }).encode("utf-8")
    eleven_request = urlrequest.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        data=payload,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(eleven_request, timeout=45) as response:
            audio_bytes = response.read()
    except (HTTPError, URLError, TimeoutError):
        return jsonify({"error": "Narration could not be generated"}), 502

    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".tmp")
    temporary_path.write_bytes(audio_bytes)
    temporary_path.replace(output_path)
    return send_file(output_path, mimetype="audio/mpeg")


@app.route("/api/complete/<slug>", methods=["POST"])
def complete_quest(slug):
    """CREATE: called by the front end once a child finishes every scene
    in a quest. Records a new badge for that quest, tied to the profile's
    current difficulty."""
    db = get_db()
    profile = get_current_user(db)
    if profile is None:
        return jsonify({"error": "No player logged in"}), 401

    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    if not profile["current_difficulty"]:
        return jsonify({"error": "No difficulty set for this profile"}), 400

    db.execute(
        "INSERT OR IGNORE INTO badges_earned (user_id, quest_id, difficulty) VALUES (?, ?, ?)",
        (profile["id"], quest_row["id"], profile["current_difficulty"]),
    )
    db.commit()

    return jsonify({"success": True, "badge_icon": quest_row["icon"]})


@app.route("/api/quests", methods=["GET"])
def api_quests():
    """READ: returns every quest as JSON, including whether the demo user
    has earned its badge yet at their current difficulty. Useful for
    testing the API layer directly (e.g. visiting /api/quests in the
    browser) and for any future screen that needs quest data without a
    full page reload."""
    db = get_db()
    profile = get_current_user(db)
    quests = db.execute("SELECT * FROM quests ORDER BY sort_order").fetchall()
    earned = set()
    if profile is not None and profile["current_difficulty"]:
        earned = {
            row["quest_id"]
            for row in db.execute(
                "SELECT quest_id FROM badges_earned WHERE user_id = ? AND difficulty = ?",
                (profile["id"], profile["current_difficulty"]),
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
    """CREATE: registers a brand-new player (name + starting difficulty)
    and logs them in for this session. Player names must be unique
    (case-insensitive) so the picker on /players can tell everyone
    apart. (Separate from the PUT endpoint below, which handles
    renames/difficulty changes for whoever's currently logged in.)"""
    data = request.get_json(silent=True) or {}
    new_name = (data.get("name") or "").strip()
    difficulty = (data.get("difficulty") or "").strip().lower()

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400
    if difficulty not in DIFFICULTIES:
        return jsonify({"error": "A 'difficulty' of easy, medium, or hard is required"}), 400

    db = get_db()
    existing = db.execute(
        "SELECT id FROM users WHERE name = ? COLLATE NOCASE", (new_name,)
    ).fetchone()
    if existing is not None:
        return jsonify({"error": "That name is already taken -- pick a different one"}), 409

    cursor = db.execute(
        "INSERT INTO users (name, current_difficulty) VALUES (?, ?)",
        (new_name, difficulty),
    )
    db.commit()
    new_id = cursor.lastrowid
    session["user_id"] = new_id

    return jsonify({"success": True, "id": new_id, "name": new_name, "difficulty": difficulty}), 201


@app.route("/api/profile", methods=["GET"])
def get_profile_route():
    """READ: returns the logged-in player's profile name and difficulty."""
    db = get_db()
    user = get_current_user(db)
    if user is None:
        return jsonify({"error": "No player logged in"}), 401
    return jsonify({"id": user["id"], "name": user["name"], "difficulty": user["current_difficulty"]})


@app.route("/api/profile", methods=["PUT"])
def update_profile():
    """UPDATE: lets a child (or parent) change the profile name and/or
    difficulty shown in the app. Expects a JSON body like
    {"name": "Aria"} and/or {"difficulty": "hard"}. Changing difficulty
    doesn't erase any badges -- they stay in the database under their
    original difficulty -- but the trail map will only show badges
    earned at the newly selected difficulty, so it will look like
    progress was reset."""
    data = request.get_json(silent=True) or {}
    db = get_db()
    profile = get_current_user(db)
    if profile is None:
        return jsonify({"error": "No player logged in"}), 401

    new_name = (data.get("name") or "").strip() if "name" in data else profile["name"]
    new_difficulty = profile["current_difficulty"]
    if "difficulty" in data:
        candidate = (data.get("difficulty") or "").strip().lower()
        if candidate not in DIFFICULTIES:
            return jsonify({"error": "A 'difficulty' of easy, medium, or hard is required"}), 400
        new_difficulty = candidate

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    if new_name.lower() != profile["name"].lower():
        clash = db.execute(
            "SELECT id FROM users WHERE name = ? COLLATE NOCASE AND id != ?",
            (new_name, profile["id"]),
        ).fetchone()
        if clash is not None:
            return jsonify({"error": "That name is already taken -- pick a different one"}), 409

    db.execute(
        "UPDATE users SET name = ?, current_difficulty = ? WHERE id = ?",
        (new_name, new_difficulty, profile["id"]),
    )
    db.commit()

    return jsonify({"success": True, "id": profile["id"], "name": new_name, "difficulty": new_difficulty})


@app.route("/api/reset/<slug>", methods=["DELETE"])
def reset_badge(slug):
    """DELETE: removes an earned badge for a quest at the profile's
    current difficulty, so the demo user can replay it. Also useful
    during development/testing."""
    db = get_db()
    profile = get_current_user(db)
    if profile is None:
        return jsonify({"error": "No player logged in"}), 401

    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    cursor = db.execute(
        "DELETE FROM badges_earned WHERE user_id = ? AND quest_id = ? AND difficulty = ?",
        (profile["id"], quest_row["id"], profile["current_difficulty"]),
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "message": "No badge was earned for this quest"}), 404

    return jsonify({"success": True, "message": f"Badge for '{quest_row['title']}' has been reset"})


if __name__ == "__main__":
    app.run(debug=True)
