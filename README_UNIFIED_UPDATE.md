# Faith‑Trails Unified Single‑Page Application

This is the one cumulative package to use. It replaces these three earlier downloads:

- `Faith-Trails-Final-Three-Quests.zip`
- `Faith-Trails-Grand-Champion-Update.zip`
- `Faith-Trails-Wooded-Animated-Trail-Update.zip`

Do not install those older ZIP files after installing this one.

## Included in this unified version

- Six complete Bible quests: Noah, Joseph, Moses, David, Jonah, and Daniel
- Easy, Medium, and Hard versions of every quest
- Eighteen earnable badges
- Wooded Start Adventure landing screen
- Compact adventure icons positioned along a real winding trail
- Trail animation that draws through the actual marker positions
- Responsive trail redraw on phone, tablet, desktop, and orientation changes
- Earned-marker pulse and sparkle effects
- Golden Champion trail after all 18 badges
- Grand Champion animation and final screen
- Exact inscription: **You have learned that God is Faithful through every journey!**
- Personalized printable certificate
- Secret Design Your Own Faith‑Trails Badge activity with PNG download
- Champion narration through the existing ElevenLabs narration system
- Final single-player mobile music fix
- Very low background-music level during narration

## Existing installation

1. Back up the current Faith‑Trails project folder, especially `faith_trails.db`.
2. Keep your existing `faith_trails.db`; do not replace or delete it.
3. Copy the files and folders from this package into the current project, allowing the program files to be replaced.
4. From the project folder, run:

   ```bash
   python apply_unified_update.py
   ```

5. Generate any missing quest and Champion narration files:

   ```bash
   python generate_narration.py
   ```

6. Restart the Flask application.
7. Refresh the browser without using cached files.

The update script changes only the availability of David, Jonah, and Daniel. It does not delete or reset any player, badge, or progress record.

## New installation

Run `python init_db.py`, generate narration, and then run `python app.py`.
