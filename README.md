# Faith Trails — Animated Single-Page Edition

This edition keeps the trail map, quests, activities, memory verses, badge
collection, Hall of Fame, music, narration ducking, and celebrations inside one
continuous game shell. The browser does not replace the page while a child is
playing, so gameplay music remains alive and screen changes can animate.

## Run locally

1. Open a terminal in this folder.
2. Install the dependencies: `python -m pip install -r requirements.txt`
3. Start the app: `python app.py`
4. Open `http://127.0.0.1:5000`

The included database preserves the uploaded player and progress data. To make
a completely new database, run `python init_db.py`.

## Production setting

Set `FAITH_TRAILS_SECRET_KEY` to a long private value in the hosting service.
Do not change it between restarts, because it protects player sessions.

For ElevenLabs narration, also set `ELEVENLABS_API_KEY` in the server
environment. `ELEVENLABS_VOICE_ID` is optional; the saved Faith Trails narrator
voice is used by default. Missing narration is generated once and cached in
`static/audio/quests`. If ElevenLabs is unavailable, the game uses the device's
built-in voice instead of remaining silent.

## Main architecture

- `templates/game.html` is the permanent game shell.
- `static/js/game.js` renders the map, story scenes, activities, quizzes,
  memory verses, badge collection, Hall of Fame, and celebration without full
  page navigation.
- `static/js/audio-engine.js` keeps gameplay music running, ducks it for
  narration, and crossfades to and from celebration music.
- `static/css/style.css` contains the responsive game UI and animations.
- `app.py` still owns quest content, profiles, difficulty, badge persistence,
  and JSON endpoints.

## Adding narration

Generated narration files belong in `static/audio/quests/`. If a narration file
is absent, the quest continues normally without it.

## Mobile-store direction

This code is now structured so the continuous game front end can later be
placed inside a mobile wrapper. Store packaging, offline asset bundling,
parental/privacy screens, icons, splash screens, and store metadata should be a
separate release phase after gameplay is approved on phones and tablets.
