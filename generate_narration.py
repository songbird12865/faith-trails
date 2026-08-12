"""
generate_narration.py

Generates narration .mp3 files for every piece of narratable Faith Trails
quest content, using your saved ElevenLabs voice.

This imports NARRATION_INDEX directly from app.py (which is built once,
at import time, by narration_utils.build_narration_index()). That's the
exact same list app.py uses to attach narration_file onto each scene, so
the filenames this script generates are GUARANTEED to match what
quest.html expects to find in static/audio/quests/. There's no separate
copy of this logic to keep in sync.

CACHING: each filename includes a hash of its text. Re-running this after
only adding one new quest regenerates just the new content -- everything
else is skipped.

SETUP
1. pip install requests
2. Set ELEVENLABS_API_KEY as an environment variable.
3. VOICE_ID below should be your saved narrator voice's ID.
4. Run from your project root (same folder as app.py):
       python scripts/generate_narration.py
"""

import os
import sys
import time
import requests

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app import NARRATION_INDEX  # noqa: E402

# ---- CONFIG -----------------------------------------------------------

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "Q4oILuo4P8VeXtE6FMLI"

MODEL_ID = "eleven_multilingual_v2"

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT, "static", "audio", "quests"
)

VOICE_SETTINGS = {
    "stability": 0.45,
    "similarity_boost": 0.8,
    "style": 0.35,
    "use_speaker_boost": True
}

# ---- SCRIPT LOGIC -------------------------------------------------------


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
    if not VOICE_ID or VOICE_ID == "PASTE_YOUR_SAVED_VOICE_ID_HERE":
        print("Set VOICE_ID to your saved narrator voice's ID before running.")
        return

    print(f"Found {len(NARRATION_INDEX)} narratable pieces of content.\n")

    generated = 0
    skipped = 0

    for item in NARRATION_INDEX:
        out_path = os.path.join(OUTPUT_DIR, item["filename"])

        if os.path.exists(out_path):
            skipped += 1
            continue

        print(f"[gen]   {item['key']} ...")
        success = generate_audio(item["text"], out_path)
        if success:
            generated += 1
            time.sleep(0.5)

    print(f"\nDone. Generated: {generated}, skipped (cached): {skipped}")


if __name__ == "__main__":
    main()
