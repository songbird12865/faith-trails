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
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]


def narration_filename(key, text):
    return f"{key}__{text_hash(text)}.mp3"


def build_narration_index(quest_content):
    """
    Mutates quest_content in place, attaching a "narration_file" key to
    every narratable item. Returns a flat list of
    {"key", "text", "filename"} entries -- this list is what
    generate_narration.py actually loops over to call the ElevenLabs API.
    """
    index = []

    def register(item, key, text_field):
        text = item[text_field]
        filename = narration_filename(key, text)
        item["narration_file"] = filename
        index.append({"key": key, "text": text, "filename": filename})

    for slug, quest in quest_content.items():

        for i, scene in enumerate(quest.get("intro_scenes", [])):
            register(scene, f"{slug}__intro__{i}", "text")

        for i, scene in enumerate(quest.get("outro_scenes", [])):
            register(scene, f"{slug}__outro__{i}", "text")

        interactive = quest.get("interactive_by_difficulty", {})
        for diff in DIFFICULTIES:
            if diff in interactive:
                register(interactive[diff], f"{slug}__interactive__{diff}", "prompt")

        quiz_bank = quest.get("quiz_bank_by_difficulty", {})
        for diff in DIFFICULTIES:
            for i, q in enumerate(quiz_bank.get(diff, [])):
                # Narrate the question plus its answer options together,
                # so a child hears the full question read aloud, not just
                # the prompt with no choices.
                option_list = ". Or ".join(q["options"])
                q["_narration_text"] = f"{q['prompt']} Is it: {option_list}?"
                register(q, f"{slug}__quiz__{diff}__{i}", "_narration_text")

        verse_bank = quest.get("verse_bank_by_difficulty", {})
        for diff in DIFFICULTIES:
            for i, v in enumerate(verse_bank.get(diff, [])):
                register(v, f"{slug}__verse__{diff}__{i}", "verse")

        if "lesson" in quest:
            filename = narration_filename(f"{slug}__lesson", quest["lesson"])
            quest["lesson_narration_file"] = filename
            index.append({
                "key": f"{slug}__lesson",
                "text": quest["lesson"],
                "filename": filename,
            })

    return index
