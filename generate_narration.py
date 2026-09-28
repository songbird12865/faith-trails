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

CACHING: each filename includes a hash of its text and, when a series uses a
different narrator, a fingerprint of that voice. Re-running this after only
adding content or changing one series voice regenerates only those files.

SETUP
1. pip install requests
2. Set ELEVENLABS_API_KEY as an environment variable.
3. Set ELEVENLABS_VOICE_ID_SERIES_1, ELEVENLABS_VOICE_ID_SERIES_2, and so on
   to the saved voice IDs you want. ELEVENLABS_VOICE_ID remains the fallback.
4. Run from your project root (same folder as app.py):
       python generate_narration.py
"""

import argparse
import os
import sys
import time
import requests

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app import NARRATION_INDEX  # noqa: E402

# CONFIG

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
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

# Series 4's chosen narrator needed cleaner settings to avoid distortion.
# Keep the settings used for its existing narration when making new scenes.
VOICE_SETTINGS_BY_SERIES = {
    4: {
        "stability": 0.65,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": False,
    },
}

# ---- SCRIPT LOGIC -------------------------------------------------------


def generate_audio(text, out_path, voice_id, series_number):
    """Request one MP3 from ElevenLabs and write it to the cache path."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": VOICE_SETTINGS_BY_SERIES.get(series_number, VOICE_SETTINGS)
    }

    # A request is made only for content whose hash-based output file is absent.
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
    except requests.RequestException as exc:
        print(f"  Request failed: {type(exc).__name__}")
        return False

    if response.status_code != 200:
        print(f"  ERROR ({response.status_code}): {response.text[:200]}")
        return False

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(response.content)
    return True


def main():
    """Generate only missing narration files and report cache usage."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--instructions-only', action='store_true',
                        help='Generate only the new memory-verse instructions.')
    parser.add_argument('--dry-run', action='store_true',
                        help='List selected voices/files without contacting ElevenLabs.')
    args = parser.parse_args()
    items = [item for item in NARRATION_INDEX
             if not args.instructions_only or item['key'].startswith('instructions__')]
    if args.instructions_only and len(items) != 10:
        print('Expected ten instruction clips. Install the updated narration_utils.py first.')
        return 1
    if args.dry_run:
        for item in items:
            cached = os.path.exists(os.path.join(OUTPUT_DIR, item['filename']))
            print(f"Series {item['series_number']} | voice {item['voice_id']} | {'cached' if cached else 'new'} | {item['key']}")
        print(f'Selected: {len(items)} clips. No audio requested.')
        return 0
    if not API_KEY:
        print("ELEVENLABS_API_KEY environment variable is not set. Stopping.")
        return 1
    print(f"Found {len(items)} narratable pieces of content.\n")

    generated = 0
    skipped = 0
    failed = 0

    for item in items:
        out_path = os.path.join(OUTPUT_DIR, item["filename"])

        # Hashes in filenames make an existing file safe to reuse: if narration
        # text changes, its hash and therefore its output filename also change.
        if os.path.exists(out_path):
            skipped += 1
            continue

        voice_id = item.get("voice_id")
        if not voice_id or voice_id == "PASTE_YOUR_SAVED_VOICE_ID_HERE":
            print(f"[skip]  {item['key']} has no valid Series {item.get('series_number')} voice ID")
            failed += 1
            continue

        print(f"[gen]   Series {item['series_number']} · {item['key']} ...")
        success = generate_audio(item["text"], out_path, voice_id, item["series_number"])
        if success:
            generated += 1
            time.sleep(0.5)
        else:
            failed += 1

    print(f"\nDone. Generated: {generated}, skipped (cached): {skipped}, failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
