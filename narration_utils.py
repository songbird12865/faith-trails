"""
narration_utils.py

Single source of truth for how narration audio filenames are built from
QUEST_CONTENT. Both app.py (to know which file to play) and
generate_narration.py (to know which file to generate) import
build_narration_index() from here, so they can never disagree about a
filename.

HOW IT WORKS
build_narration_index() walks QUEST_CONTENT once and, for every piece of
narratable text, does two things:
  1. Computes a filename like "red-sea__quiz__hard__2__a1b2c3d4e5.mp3"
  2. Attaches that filename directly onto the same dict that scenes are
     built from (scene["narration_file"] = filename), so once a scene is
     assembled by build_scenes() in app.py, it automatically already
     carries the correct narration_file -- no separate lookup needed.

Call this ONCE, right after QUEST_CONTENT is defined in app.py. After
that, every scene dict handed to a template (and therefore to the
browser via scenes_json) already has narration_file baked in.
"""

import hashlib

DIFFICULTIES = ("easy", "medium", "hard")


def text_hash(text):
    """Return a short stable content hash used for cache invalidation."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def narration_filename(key, text, voice_id=None, legacy_voice_id=None):
    """Build a content-addressed MP3 filename for both text and voice.

    Files made with the original Faith-Trails voice keep their historic names,
    so an existing narration library is still reusable. Choosing a different
    voice adds a short voice fingerprint and creates a separate safe cache.
    """
    voice_suffix = ""
    if voice_id and voice_id != legacy_voice_id:
        voice_suffix = f"__voice-{text_hash(voice_id)[:8]}"
    return f"{key}{voice_suffix}__{text_hash(text)}.mp3"


def build_narration_index(
    quest_content,
    quest_series=None,
    series_voice_ids=None,
    legacy_voice_id=None,
):
    """
    Mutates quest_content in place, attaching a "narration_file" key to
    every narratable item. Returns a flat list of
    {"key", "text", "filename"} entries -- this list is what
    generate_narration.py actually loops over to call the ElevenLabs API.
    """
    index = []

    quest_series = quest_series or {}
    series_voice_ids = series_voice_ids or {}

    def register(item, key, text_field, series_number):
        # Mutating the source dictionary deliberately keeps the generated
        # filename beside the exact content that the browser later receives.
        text = item[text_field]
        voice_id = series_voice_ids.get(series_number, legacy_voice_id)
        filename = narration_filename(key, text, voice_id, legacy_voice_id)
        item["narration_file"] = filename
        index.append({
            "key": key,
            "text": text,
            "filename": filename,
            "series_number": series_number,
            "voice_id": voice_id,
        })

    for slug, quest in quest_content.items():
        series_number = quest_series.get(slug, 1)

        for i, scene in enumerate(quest.get("intro_scenes", [])):
            register(scene, f"{slug}__intro__{i}", "text", series_number)

        for i, scene in enumerate(quest.get("outro_scenes", [])):
            register(scene, f"{slug}__outro__{i}", "text", series_number)

        interactive = quest.get("interactive_by_difficulty", {})
        for diff in DIFFICULTIES:
            if diff in interactive:
                register(interactive[diff], f"{slug}__interactive__{diff}", "prompt", series_number)

        quiz_bank = quest.get("quiz_bank_by_difficulty", {})
        for diff in DIFFICULTIES:
            for i, q in enumerate(quiz_bank.get(diff, [])):
                # Narrate the question plus its answer options together,
                # so a child hears the full question read aloud, not just
                # the prompt with no choices.
                option_list = ". Or ".join(q["options"])
                q["_narration_text"] = f"{q['prompt']} Is it: {option_list}?"
                register(q, f"{slug}__quiz__{diff}__{i}", "_narration_text", series_number)

        verse_bank = quest.get("verse_bank_by_difficulty", {})
        for diff in DIFFICULTIES:
            for i, v in enumerate(verse_bank.get(diff, [])):
                register(v, f"{slug}__verse__{diff}__{i}", "verse", series_number)

        if "lesson" in quest:
            voice_id = series_voice_ids.get(series_number, legacy_voice_id)
            filename = narration_filename(
                f"{slug}__lesson", quest["lesson"], voice_id, legacy_voice_id
            )
            quest["lesson_narration_file"] = filename
            index.append({
                "key": f"{slug}__lesson",
                "text": quest["lesson"],
                "filename": filename,
                "series_number": series_number,
                "voice_id": voice_id,
            })

    return index
