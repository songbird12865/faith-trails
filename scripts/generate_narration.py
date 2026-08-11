"""
generate_narration.py

Generates narration .mp3 files for Faith Trails quest content using your
saved ElevenLabs voice, and saves them into static/audio/quests/.

CACHING: Before calling the API, this script hashes each piece of text.
If an audio file already exists for that exact text (same hash), it's
skipped. This means re-running the script after adding new quests only
spends credits on the NEW content, not everything you've already made.

SETUP
1. pip install requests
2. Set your API key as an environment variable (never hardcode it):
       Windows (PowerShell):  $env:ELEVENLABS_API_KEY="your_key_here"
       Mac/Linux:             export ELEVENLABS_API_KEY="your_key_here"
3. Find your saved narrator voice's Voice ID in ElevenLabs:
   Voice Library / My Voices -> click your voice -> copy the Voice ID.
   Paste it into VOICE_ID below.
4. Edit the QUEST_CONTENT list below (or point get_quest_content() at
   your actual database instead -- see note at the bottom).
5. Run: python generate_narration.py
"""

import os
import hashlib
import time
import requests

# ---- CONFIG -----------------------------------------------------------

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "PASTE_YOUR_SAVED_VOICE_ID_HERE"

# eleven_multilingual_v2 gives the most natural inflection/expressiveness.
# eleven_turbo_v2_5 is faster and cheaper on credits but slightly less rich.
MODEL_ID = "eleven_multilingual_v2"

OUTPUT_DIR = os.path.join("static", "audio", "quests")

# Voice settings: lower stability = more expressive/varied inflection,
# higher stability = more consistent/monotone. 0.4-0.5 is a good starting
# point for storytelling. Tune this after listening to a couple samples.
VOICE_SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.8,
    "style": 0.35,
    "use_speaker_boost": True
}

# ---- QUEST CONTENT ------------------------------------------------------
# Each entry needs a unique "key" (used as the output filename) and the
# "text" to narrate. Replace this list with a call into your own database
# -- see get_quest_content_from_db() stub near the bottom for the pattern.

QUEST_CONTENT = [
    {
        "key": "noahs_ark_story",
        "text": "God saw that the earth had become full of wickedness. But there was one man, Noah, who walked faithfully with God..."
    },
    {
        "key": "noahs_ark_quiz_q1",
        "text": "How many of each clean animal did God tell Noah to bring onto the ark?"
    },
    {
        "key": "noahs_ark_feedback_correct",
        "text": "That's right! God told Noah to bring seven pairs of every clean animal."
    },
    {
        "key": "noahs_ark_feedback_incorrect",
        "text": "Not quite! Let's look at that verse again together."
    },
]

# ---- SCRIPT LOGIC -------------------------------------------------------


def text_hash(text):
    """Short hash of the text, used to detect if content has changed."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def output_path(key, text):
    """
    Filename includes both the content key and a hash of the text, so if
    you edit a quest's wording later, it naturally generates a NEW file
    instead of silently reusing stale audio for changed text.
    """
    h = text_hash(text)
    return os.path.join(OUTPUT_DIR, f"{key}__{h}.mp3")


def generate_audio(text, out_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"  ERROR ({response.status_code}): {response.text[:200]}")
        return False

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(response.content)
    return True


def main():
    if not API_KEY:
        print("ELEVENLABS_API_KEY environment variable is not set. Stopping.")
        return
    if VOICE_ID == "PASTE_YOUR_SAVED_VOICE_ID_HERE":
        print("Set VOICE_ID to your saved narrator voice's ID before running.")
        return

    generated = 0
    skipped = 0

    for item in QUEST_CONTENT:
        key = item["key"]
        text = item["text"]
        out_path = output_path(key, text)

        if os.path.exists(out_path):
            print(f"[skip]  {key} (already generated, text unchanged)")
            skipped += 1
            continue

        print(f"[gen]   {key} ...")
        success = generate_audio(text, out_path)
        if success:
            generated += 1
            # Small delay to stay well within API rate limits
            time.sleep(0.5)

    print(f"\nDone. Generated: {generated}, skipped (cached): {skipped}")


# ---- OPTIONAL: pulling content from your real database ------------------
#
# Instead of hardcoding QUEST_CONTENT above, you can build the list from
# your existing Flask/SQLite models. Something like:
#
# def get_quest_content_from_db():
#     import sqlite3
#     conn = sqlite3.connect("faithtrails.db")
#     cur = conn.cursor()
#     cur.execute("SELECT id, story_text FROM quests")
#     content = []
#     for quest_id, story_text in cur.fetchall():
#         content.append({"key": f"quest_{quest_id}_story", "text": story_text})
#     conn.close()
#     return content
#
# Then replace: for item in QUEST_CONTENT:
# with:         for item in get_quest_content_from_db():


if __name__ == "__main__":
    main()
