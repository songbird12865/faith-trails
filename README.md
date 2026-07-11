# Faith Trails: A Closer Walk for Kids

An interactive Bible story app for children ages 7–10. Kids follow a trail
map of story "quests" (starting with Noah's Ark), each combining short
illustrated story scenes with a hands-on interactive checkpoint, and earn a
badge for every quest they complete.

## Tech stack
- **Backend:** Python + Flask
- **Database:** SQLite
- **Frontend:** HTML5 + Tailwind CSS (via CDN — no build step needed)

## Getting started

1. **Create a virtual environment (recommended)**
   ```
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Create the database**
   ```
   python init_db.py
   ```
   This creates `faith_trails.db` from `schema.sql`, seeded with the trail's
   story quests. Re-run this any time you want to wipe progress and start fresh.

4. **Run the app**
   ```
   python app.py
   ```
   Then open **http://127.0.0.1:5000** in your browser.

## Project structure

```
faith_trails/
├── app.py                 Flask routes and app logic
├── schema.sql              Database schema + seed data
├── init_db.py               Builds the .db file from schema.sql
├── requirements.txt
├── templates/
│   ├── base.html           Shared layout, fonts, Tailwind config
│   ├── home.html            Trail map (navigation hub)
│   ├── quest.html            Story quest player + interactive checkpoint
│   └── coming_soon.html       Placeholder for not-yet-built quests
└── static/
    └── css/style.css        Custom "trail map" path styling
```

## How the quest engine works

Every Bible story is defined as a list of "scenes" inside `QUEST_CONTENT` in
`app.py`. A scene is either:
- **`"type": "story"`** — an illustrated beat of narration with a Next button
- **`"type": "interactive", "subtype": "matching"`** — a drag-and-drop (or
  tap-to-place, for touch devices) checkpoint the child must complete before
  continuing

This means adding your next story (David & Goliath, Daniel in the Lions'
Den) is mostly a matter of writing new scene content, not new page logic —
exactly the reusable "quest engine" milestone described in the Statement of
Work.

## Current status

- ✅ Noah's Ark — fully playable, with a drag-and-drop animal-matching checkpoint
- 🔒 David & Goliath — placeholder ("coming soon") on the trail map
- 🔒 Daniel and the Lions' Den — placeholder ("coming soon") on the trail map

## Next steps to build out

1. Write the scene content for David & Goliath and Daniel in the Lions' Den
   inside `QUEST_CONTENT` in `app.py`, following the Noah's Ark pattern.
2. Flip `is_available` to `1` for each quest in `schema.sql` once its
   content is written, then re-run `python init_db.py`.
3. (Stretch goal from the SOW) Build a simple parent/leader view that reads
   from the `badges_earned` table.
4. Replace emoji artwork with real illustrations once you're ready — the
   `icon` field in the `quests` table and the `emoji` fields in
   `QUEST_CONTENT` are the only places art references live.
