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
DIFFICULTIES = ("easy", "medium", "hard")

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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_profile(db):
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (DEMO_USER_ID,)
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

@app.route("/")
def home():
    """Trail map: shows every quest and which ones are already completed
    at the player's current difficulty. If the player hasn't created a
    profile (name + difficulty) yet, show the onboarding screen instead."""
    db = get_db()
    profile = get_profile(db)

    if not profile["name"] or not profile["current_difficulty"]:
        return render_template("create_profile.html", difficulties=DIFFICULTIES)

    quests = db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]
        for row in db.execute(
            "SELECT quest_id FROM badges_earned WHERE user_id = ? AND difficulty = ?",
            (DEMO_USER_ID, profile["current_difficulty"]),
        ).fetchall()
    }
    return render_template(
        "home.html",
        quests=quests,
        earned=earned,
        profile=profile,
        difficulties=DIFFICULTIES,
    )


@app.route("/badges")
def badges():
    """Badge case: shows every badge the player has earned so far at
    their current difficulty, plus the ones still waiting to be earned."""
    db = get_db()
    profile = get_profile(db)

    if not profile["name"] or not profile["current_difficulty"]:
        return render_template("create_profile.html", difficulties=DIFFICULTIES)

    quests = db.execute(
        "SELECT * FROM quests WHERE is_available = 1 ORDER BY sort_order"
    ).fetchall()
    earned = {
        row["quest_id"]: row["earned_at"]
        for row in db.execute(
            "SELECT quest_id, earned_at FROM badges_earned WHERE user_id = ? AND difficulty = ?",
            (DEMO_USER_ID, profile["current_difficulty"]),
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
    profile = get_profile(db)

    if not profile["name"] or not profile["current_difficulty"]:
        return render_template("create_profile.html", difficulties=DIFFICULTIES)

    quests = db.execute(
        "SELECT * FROM quests ORDER BY sort_order"
    ).fetchall()
    earned_rows = db.execute(
        "SELECT quest_id, difficulty, earned_at FROM badges_earned WHERE user_id = ?",
        (DEMO_USER_ID,),
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
    profile = get_profile(db)

    if not profile["name"] or not profile["current_difficulty"]:
        return render_template("create_profile.html", difficulties=DIFFICULTIES)

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

    difficulty = profile["current_difficulty"]
    scenes = build_scenes(content, difficulty)

    return render_template(
        "quest.html",
        quest=quest_row,
        scenes_json=json.dumps(scenes),
        lesson=content["lesson"],
        difficulty=difficulty,
    )


@app.route("/api/complete/<slug>", methods=["POST"])
def complete_quest(slug):
    """CREATE: called by the front end once a child finishes every scene
    in a quest. Records a new badge for that quest, tied to the profile's
    current difficulty."""
    db = get_db()
    profile = get_profile(db)
    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    if not profile["current_difficulty"]:
        return jsonify({"error": "No difficulty set for this profile"}), 400

    db.execute(
        "INSERT OR IGNORE INTO badges_earned (user_id, quest_id, difficulty) VALUES (?, ?, ?)",
        (DEMO_USER_ID, quest_row["id"], profile["current_difficulty"]),
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
    profile = get_profile(db)
    quests = db.execute("SELECT * FROM quests ORDER BY sort_order").fetchall()
    earned = set()
    if profile["current_difficulty"]:
        earned = {
            row["quest_id"]
            for row in db.execute(
                "SELECT quest_id FROM badges_earned WHERE user_id = ? AND difficulty = ?",
                (DEMO_USER_ID, profile["current_difficulty"]),
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
    """CREATE: sets the player's name and starting difficulty for the
    first time, during onboarding. (Separate from the PUT endpoint
    below, which handles later renames/difficulty changes.)"""
    data = request.get_json(silent=True) or {}
    new_name = (data.get("name") or "").strip()
    difficulty = (data.get("difficulty") or "").strip().lower()

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400
    if difficulty not in DIFFICULTIES:
        return jsonify({"error": "A 'difficulty' of easy, medium, or hard is required"}), 400

    db = get_db()
    db.execute(
        "UPDATE users SET name = ?, current_difficulty = ? WHERE id = ?",
        (new_name, difficulty, DEMO_USER_ID),
    )
    db.commit()

    return jsonify({"success": True, "id": DEMO_USER_ID, "name": new_name, "difficulty": difficulty}), 201


@app.route("/api/profile", methods=["GET"])
def get_profile_route():
    """READ: returns the demo user's current profile name and difficulty."""
    db = get_db()
    user = get_profile(db)
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
    profile = get_profile(db)

    new_name = (data.get("name") or "").strip() if "name" in data else profile["name"]
    new_difficulty = profile["current_difficulty"]
    if "difficulty" in data:
        candidate = (data.get("difficulty") or "").strip().lower()
        if candidate not in DIFFICULTIES:
            return jsonify({"error": "A 'difficulty' of easy, medium, or hard is required"}), 400
        new_difficulty = candidate

    if not new_name:
        return jsonify({"error": "A non-empty 'name' is required"}), 400

    db.execute(
        "UPDATE users SET name = ?, current_difficulty = ? WHERE id = ?",
        (new_name, new_difficulty, DEMO_USER_ID),
    )
    db.commit()

    return jsonify({"success": True, "id": DEMO_USER_ID, "name": new_name, "difficulty": new_difficulty})


@app.route("/api/reset/<slug>", methods=["DELETE"])
def reset_badge(slug):
    """DELETE: removes an earned badge for a quest at the profile's
    current difficulty, so the demo user can replay it. Also useful
    during development/testing."""
    db = get_db()
    profile = get_profile(db)
    quest_row = db.execute(
        "SELECT * FROM quests WHERE slug = ?", (slug,)
    ).fetchone()

    if quest_row is None:
        return jsonify({"error": "Quest not found"}), 404

    cursor = db.execute(
        "DELETE FROM badges_earned WHERE user_id = ? AND quest_id = ? AND difficulty = ?",
        (DEMO_USER_ID, quest_row["id"], profile["current_difficulty"]),
    )
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"success": False, "message": "No badge was earned for this quest"}), 404

    return jsonify({"success": True, "message": f"Badge for '{quest_row['title']}' has been reset"})


if __name__ == "__main__":
    app.run(debug=True)
