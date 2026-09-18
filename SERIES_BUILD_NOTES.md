# Faith-Trails Series Build

This development version reorganizes Faith-Trails into five themed series of
five adventures. Each adventure supports Easy, Medium, and Hard badges, for a
planned total of 75 badges.

## Series roadmap

1. **God's Rescue & New Beginnings** — Creation, Noah's Ark, Jonah and the Big
   Fish, Daniel and the Lions' Den, and Moses and the Red Sea.
2. **Family & Trust** — Joseph's Colorful Coat, Abraham, Jacob, Ruth, and
   Samuel.
3. **Courage & Leadership** — David & Goliath, The Apostles and Pentecost,
   Gideon, Esther, and The Battle of Jericho.
4. **Wisdom & Faithfulness** — Solomon, The Ten Commandments, Elijah,
   Nehemiah, and Job.
5. **Jesus & the Good News** — The Nativity, Jesus' Teachings: The Beatitudes,
   The Good Samaritan, Feeding the 5,000, and Easter.

## Completed in this build

- All 25 adventures are registered and placed in their themed series.
- The original six quest slugs and database IDs are preserved.
- Series 1 through Series 5 are playable at Easy, Medium, and Hard levels.
- Original saved profiles and badge records are preserved during migration.
- The first reward now unlocks after all 15 Series 1 badges are earned.
- Hall of Fame progress is measured against 75 badges; all 75 badges can now
  be earned across the five completed series.
- 37 automated integration tests cover profiles, quests, badges, the roadmap,
  activity sequencing, series narration voices, scene artwork, age-related
  memory-verse selections, and all five completed series.
- Series 5 uses the memory verses approved by the project owner. Familiar,
  intuitive passages in the Good Samaritan and Easter quests intentionally
  exceed the usual word-count guidelines.

## Narration

Creation narration is generated securely on demand through the existing
ElevenLabs integration. `ELEVENLABS_API_KEY` must remain an environment
variable on PythonAnywhere; it must never be added to this project.

### Different narrator for each series

Set any or all of these before starting Flask or running
`python generate_narration.py`:

```text
ELEVENLABS_VOICE_ID_SERIES_1=your_first_voice_id
ELEVENLABS_VOICE_ID_SERIES_2=your_second_voice_id
ELEVENLABS_VOICE_ID_SERIES_3=your_third_voice_id
ELEVENLABS_VOICE_ID_SERIES_4=your_fourth_voice_id
ELEVENLABS_VOICE_ID_SERIES_5=your_fifth_voice_id
```

`ELEVENLABS_VOICE_ID` remains the shared fallback. Narration filenames include
a voice fingerprint when a different voice is selected, so changing one series
does not overwrite another series' recordings. The original voice keeps its
existing filenames and cache.

## Scene illustrations

Every story scene may include an `image` value, for example:

```python
{"type": "story", "image": "abraham/01-leaving-home.webp", ...}
```

Put that optimized image at
`static/img/quests/scenes/abraham/01-leaving-home.webp`. The app preloads the
next story image, crossfades between scenes, and automatically uses the quest's
original cover if scene art is absent or fails to load. Activities, quizzes,
and memory verses return to the cover artwork.

This build includes compressed 1280 by 720 WebP story illustrations for
every narration scene in Series 1 through Series 5. The cover images remain
unchanged for the trail map, badge collection, activities, quizzes, and memory
verses.

## Safe deployment sequence

1. Back up the live PythonAnywhere project and `faith_trails.db`.
2. Upload this development build without overwriting the live database first.
3. Copy the current live database into the development build.
4. Reload the test web app. The catalog migration adds the series fields and
   future quest records without deleting profiles or badges.
5. Verify player selection, each existing quest, Creation, audio, difficulty
   changes, Badges, and Hall of Fame.
6. Promote the build only after the development URL passes those checks.

Do not run `schema.sql` against the live database. It intentionally drops and
recreates tables for fresh installations and automated tests.
