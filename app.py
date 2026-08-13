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
from narration_utils import build_narration_index, narration_filename

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
    "david-goliath": {
        "title": "David & Goliath",
        "intro_scenes": [
            {
                "type": "story",
                "emoji": "😨",
                "text": "The Israelite army was afraid. Every day, a giant named Goliath stood before them and dared anyone to fight him.",
            },
            {
                "type": "story",
                "emoji": "🐑",
                "text": "David was only a young shepherd, but he trusted God completely. He told King Saul that he would face the giant.",
            },
        ],
        "interactive_by_difficulty": {
            "easy": {
                "type": "interactive", "subtype": "matching",
                "prompt": "Help David prepare! Put the five smooth stones into his shepherd's bag.",
                "items": [
                    {"id": "stone-1", "emoji": "🪨", "label": "Smooth stone 1"},
                    {"id": "stone-2", "emoji": "🪨", "label": "Smooth stone 2"},
                    {"id": "stone-3", "emoji": "🪨", "label": "Smooth stone 3"},
                    {"id": "stone-4", "emoji": "🪨", "label": "Smooth stone 4"},
                    {"id": "stone-5", "emoji": "🪨", "label": "Smooth stone 5"},
                ],
            },
            "medium": {
                "type": "interactive", "subtype": "sequence",
                "prompt": "Tap these events in the order they happened!",
                "items": [
                    {"id": "challenge", "emoji": "📣", "label": "Goliath challenges Israel"},
                    {"id": "volunteer", "emoji": "🙋", "label": "David offers to fight"},
                    {"id": "armor", "emoji": "🛡️", "label": "David refuses Saul's armor"},
                    {"id": "stones", "emoji": "🪨", "label": "David chooses five smooth stones"},
                    {"id": "victory", "emoji": "🎯", "label": "God gives David victory"},
                ],
            },
            "hard": {
                "type": "interactive", "subtype": "sequence",
                "prompt": "Tap all seven events in the exact order they happened!",
                "items": [
                    {"id": "fear", "emoji": "😨", "label": "Israel's army is afraid"},
                    {"id": "challenge", "emoji": "📣", "label": "Goliath challenges Israel"},
                    {"id": "volunteer", "emoji": "🙋", "label": "David tells Saul he will fight"},
                    {"id": "armor", "emoji": "🛡️", "label": "David refuses Saul's heavy armor"},
                    {"id": "stones", "emoji": "🪨", "label": "David chooses five smooth stones"},
                    {"id": "faith", "emoji": "🙏", "label": "David says the battle belongs to God"},
                    {"id": "victory", "emoji": "🎯", "label": "The stone strikes Goliath down"},
                ],
            },
        },
        "outro_scenes": [
            {
                "type": "story",
                "emoji": "🛡️",
                "text": "David refused Saul's heavy armor. He picked up five smooth stones and his sling, trusting God instead of weapons.",
            },
            {
                "type": "story",
                "emoji": "🎯",
                "text": "David said the battle belonged to God. He swung his sling, the stone struck Goliath down, and the whole army saw what faith could do.",
            },
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                {"type": "quiz", "prompt": "Who was the giant?", "options": ["Goliath", "Saul", "Jonah"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did David use to face Goliath?", "options": ["A sling and stones", "A spear", "A chariot"], "correct_index": 0},
                {"type": "quiz", "prompt": "Who gave David the victory?", "options": ["God", "King Saul", "The army"], "correct_index": 0},
            ],
            "medium": [
                {"type": "quiz", "prompt": "Why was David willing to face Goliath?", "options": ["He trusted God completely", "He was taller than Goliath", "He had magical armor"], "correct_index": 0},
                {"type": "quiz", "prompt": "Why did David refuse Saul's armor?", "options": ["He trusted God instead of heavy weapons", "It belonged to Goliath", "It was made of wood"], "correct_index": 0},
                {"type": "quiz", "prompt": "How many smooth stones did David choose?", "options": ["Five", "Three", "Twelve"], "correct_index": 0},
            ],
            "hard": [
                {"type": "quiz", "prompt": "What did Goliath do when he saw David?", "options": ["He laughed at and mocked him", "He surrendered immediately", "He asked David for help"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did David say about the battle?", "options": ["The battle belongs to the Lord", "The strongest soldier always wins", "Saul's armor would save him"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did the Israelite army learn from David's victory?", "options": ["What faith in God could do", "How to build better armor", "Why shepherds should be kings"], "correct_index": 0},
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [{"type": "memory_verse", "verse": "The battle is the Lord's.", "reference": "1 Samuel 17:47", "reference_options": ["1 Samuel 17:47", "1 Samuel 7:47", "2 Samuel 17:47"]}],
            "medium": [{"type": "memory_verse", "verse": "It is not by sword or spear that the Lord saves; for the battle is the Lord's.", "reference": "1 Samuel 17:47", "reference_options": ["1 Samuel 17:47", "1 Samuel 17:37", "2 Samuel 17:47"]}],
            "hard": [{"type": "memory_verse", "verse": "The Lord who rescued me from the paw of the lion and the paw of the bear will rescue me from the hand of this Philistine.", "reference": "1 Samuel 17:37", "reference_options": ["1 Samuel 17:37", "1 Samuel 17:47", "2 Samuel 17:37"]}],
        },
        "lesson": "Courage grows when we trust that God is bigger than every giant we face.",
    },
    "jonah-big-fish": {
        "title": "Jonah and the Big Fish",
        "intro_scenes": [
            {"type": "story", "emoji": "🏙️", "text": "God asked Jonah to go to Nineveh and warn the people to turn back to Him."},
            {"type": "story", "emoji": "⛵", "text": "Jonah was afraid and ran the other way. He boarded a ship headed far from Nineveh."},
        ],
        "interactive_by_difficulty": {
            "easy": {
                "type": "interactive", "subtype": "sequence", "prompt": "Tap these three events in the order they happened!",
                "items": [
                    {"id": "run", "emoji": "⛵", "label": "Jonah sails away"},
                    {"id": "storm", "emoji": "🌊", "label": "A huge storm hits"},
                    {"id": "fish", "emoji": "🐋", "label": "A big fish swallows Jonah"},
                ],
            },
            "medium": {
                "type": "interactive", "subtype": "sequence", "prompt": "Tap these five events in the order they happened!",
                "items": [
                    {"id": "call", "emoji": "🏙️", "label": "God sends Jonah to Nineveh"},
                    {"id": "run", "emoji": "⛵", "label": "Jonah sails the other way"},
                    {"id": "storm", "emoji": "🌊", "label": "A huge storm hits"},
                    {"id": "sea", "emoji": "🤿", "label": "Jonah is thrown into the sea"},
                    {"id": "fish", "emoji": "🐋", "label": "A big fish swallows Jonah"},
                ],
            },
            "hard": {
                "type": "interactive", "subtype": "sequence", "prompt": "Tap all seven events in the exact order they happened!",
                "items": [
                    {"id": "call", "emoji": "🏙️", "label": "God sends Jonah to Nineveh"},
                    {"id": "run", "emoji": "⛵", "label": "Jonah sails in the opposite direction"},
                    {"id": "storm", "emoji": "🌊", "label": "A huge storm terrifies the sailors"},
                    {"id": "sea", "emoji": "🤿", "label": "The sailors throw Jonah into the sea"},
                    {"id": "calm", "emoji": "☀️", "label": "The water becomes calm"},
                    {"id": "fish", "emoji": "🐋", "label": "Jonah prays inside the fish"},
                    {"id": "obey", "emoji": "🙏", "label": "Jonah obeys and goes to Nineveh"},
                ],
            },
        },
        "outro_scenes": [
            {"type": "story", "emoji": "🌊", "text": "Jonah told the sailors to throw him into the sea. The moment they did, the storm became calm, and God sent a huge fish to swallow Jonah."},
            {"type": "story", "emoji": "🙏", "text": "Jonah prayed inside the fish for three days and three nights. God had the fish spit him onto dry land, and Jonah obeyed God the second time."},
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                {"type": "quiz", "prompt": "Where did God ask Jonah to go?", "options": ["Nineveh", "Egypt", "Bethlehem"], "correct_index": 0},
                {"type": "quiz", "prompt": "What swallowed Jonah?", "options": ["A huge fish", "A lion", "A crocodile"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did Jonah do inside the fish?", "options": ["He prayed to God", "He built a boat", "He went to sleep"], "correct_index": 0},
            ],
            "medium": [
                {"type": "quiz", "prompt": "Why did Jonah board a ship?", "options": ["He was running away from what God asked him to do", "God told him to sail", "He wanted to catch fish"], "correct_index": 0},
                {"type": "quiz", "prompt": "What happened when Jonah was thrown into the sea?", "options": ["The water became calm", "The storm grew stronger", "The ship sank"], "correct_index": 0},
                {"type": "quiz", "prompt": "How long was Jonah inside the fish?", "options": ["Three days and three nights", "One day", "Forty days"], "correct_index": 0},
            ],
            "hard": [
                {"type": "quiz", "prompt": "What message was Jonah supposed to take to Nineveh?", "options": ["The people should turn back to God", "The people should build a ship", "The city should choose a new king"], "correct_index": 0},
                {"type": "quiz", "prompt": "Why did Jonah believe the storm had come?", "options": ["Because he had run from God", "Because the sailors were lost", "Because the ship was too heavy"], "correct_index": 0},
                {"type": "quiz", "prompt": "What happened when Jonah finally went to Nineveh?", "options": ["The people listened", "The people sent him away", "Another storm began"], "correct_index": 0},
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [{"type": "memory_verse", "verse": "In my distress I called to the Lord, and he answered me.", "reference": "Jonah 2:2", "reference_options": ["Jonah 2:2", "Jonah 1:2", "Joel 2:2"]}],
            "medium": [{"type": "memory_verse", "verse": "Then the word of the Lord came to Jonah a second time.", "reference": "Jonah 3:1", "reference_options": ["Jonah 3:1", "Jonah 1:3", "Joel 3:1"]}],
            "hard": [{"type": "memory_verse", "verse": "Those who cling to worthless idols turn away from God's love for them.", "reference": "Jonah 2:8", "reference_options": ["Jonah 2:8", "Jonah 3:8", "Joel 2:8"]}],
        },
        "lesson": "God gives second chances, and obeying Him is always the right direction.",
    },
    "daniel-lions-den": {
        "title": "Daniel and the Lions' Den",
        "intro_scenes": [
            {"type": "story", "emoji": "🙏", "text": "Daniel loved God and prayed to Him every day, even after moving to a new kingdom with different rules."},
            {"type": "story", "emoji": "📜", "text": "Jealous officials tricked the king into making a law: anyone who prayed to anyone but the king would be thrown to the lions."},
        ],
        "interactive_by_difficulty": {
            "easy": {
                "type": "interactive", "subtype": "matching", "prompt": "Help the angel! Gently guide each lion to a quiet resting place.",
                "items": [
                    {"id": "lion-1", "emoji": "🦁", "label": "Lion 1"},
                    {"id": "lion-2", "emoji": "🦁", "label": "Lion 2"},
                    {"id": "lion-3", "emoji": "🦁", "label": "Lion 3"},
                ],
            },
            "medium": {
                "type": "interactive", "subtype": "sequence", "prompt": "Tap these five events in the order they happened!",
                "items": [
                    {"id": "law", "emoji": "📜", "label": "The king signs the new law"},
                    {"id": "pray", "emoji": "🙏", "label": "Daniel keeps praying to God"},
                    {"id": "caught", "emoji": "👀", "label": "The officials catch Daniel"},
                    {"id": "den", "emoji": "🦁", "label": "Daniel is placed in the lions' den"},
                    {"id": "safe", "emoji": "😇", "label": "God keeps Daniel safe"},
                ],
            },
            "hard": {
                "type": "interactive", "subtype": "sequence", "prompt": "Tap all seven events in the exact order they happened!",
                "items": [
                    {"id": "jealous", "emoji": "😠", "label": "Jealous officials plan a trap"},
                    {"id": "law", "emoji": "📜", "label": "The king signs the prayer law"},
                    {"id": "pray", "emoji": "🙏", "label": "Daniel prays as he always has"},
                    {"id": "caught", "emoji": "👀", "label": "The officials report Daniel"},
                    {"id": "den", "emoji": "🦁", "label": "Daniel is thrown into the den"},
                    {"id": "angel", "emoji": "😇", "label": "God's angel shuts the lions' mouths"},
                    {"id": "morning", "emoji": "🌅", "label": "The king finds Daniel safe"},
                ],
            },
        },
        "outro_scenes": [
            {"type": "story", "emoji": "🦁", "text": "Daniel kept praying to God, just as he always had. The officials caught him, and the saddened king had Daniel thrown into the lions' den."},
            {"type": "story", "emoji": "😇", "text": "God sent an angel to shut the lions' mouths. In the morning, the king found Daniel completely safe because Daniel had trusted God."},
        ],
        "quiz_bank_by_difficulty": {
            "easy": [
                {"type": "quiz", "prompt": "Who did Daniel pray to?", "options": ["God", "The king", "The officials"], "correct_index": 0},
                {"type": "quiz", "prompt": "Where was Daniel thrown?", "options": ["Into the lions' den", "Into the sea", "Into a prison tower"], "correct_index": 0},
                {"type": "quiz", "prompt": "Who kept Daniel safe?", "options": ["God", "The officials", "A soldier"], "correct_index": 0},
            ],
            "medium": [
                {"type": "quiz", "prompt": "Why did the officials make a plan against Daniel?", "options": ["They were jealous of him", "Daniel had broken the palace", "The king ordered them to"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did Daniel do after he heard about the new law?", "options": ["He kept praying to God", "He prayed to the king", "He stopped praying"], "correct_index": 0},
                {"type": "quiz", "prompt": "What did God send to protect Daniel?", "options": ["An angel", "A shepherd", "A storm"], "correct_index": 0},
            ],
            "hard": [
                {"type": "quiz", "prompt": "What punishment did the new law require for praying to anyone but the king?", "options": ["Being thrown to the lions", "Leaving the kingdom", "Paying the king gold"], "correct_index": 0},
                {"type": "quiz", "prompt": "How often had Daniel been praying before the law was made?", "options": ["Every day", "Only on special days", "Once a year"], "correct_index": 0},
                {"type": "quiz", "prompt": "Why was Daniel unharmed in the morning?", "options": ["He trusted God, who protected him", "The lions were not in the den", "The king secretly rescued him"], "correct_index": 0},
            ],
        },
        "quiz_count_by_difficulty": {"easy": 2, "medium": 2, "hard": 3},
        "verse_bank_by_difficulty": {
            "easy": [{"type": "memory_verse", "verse": "My God sent his angel, and he shut the mouths of the lions.", "reference": "Daniel 6:22", "reference_options": ["Daniel 6:22", "Daniel 6:12", "David 6:22"]}],
            "medium": [{"type": "memory_verse", "verse": "He got down on his knees and prayed, giving thanks to his God, just as he had done before.", "reference": "Daniel 6:10", "reference_options": ["Daniel 6:10", "Daniel 6:20", "Daniel 3:10"]}],
            "hard": [{"type": "memory_verse", "verse": "He is the living God and he endures forever; his kingdom will not be destroyed, his dominion will never end.", "reference": "Daniel 6:26", "reference_options": ["Daniel 6:26", "Daniel 3:26", "Daniel 6:16"]}],
        },
        "lesson": "We can stay faithful and trust God, even when doing the right thing feels scary.",
    },
}

# Attaches a "narration_file" field to every scene/question/verse dict
# above (and a "lesson_narration_file" to each quest), and returns the
# flat list generate_narration.py uses to actually call ElevenLabs. Run
# once here, at import time, so every request already has the filenames
# baked in with zero extra per-request work.
NARRATION_INDEX = build_narration_index(QUEST_CONTENT)
CHAMPION_NARRATION_TEXT = (
    "You followed Noah, Joseph, Moses, David, Jonah, and Daniel through every adventure. "
    "Each one trusted God in a different way—and now you know that you can trust Him too."
)
CHAMPION_NARRATION_FILE = narration_filename("faith-trails-champion", CHAMPION_NARRATION_TEXT)
NARRATION_INDEX.append({
    "key": "faith-trails-champion",
    "text": CHAMPION_NARRATION_TEXT,
    "filename": CHAMPION_NARRATION_FILE,
})


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
