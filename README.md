# Faith-Trails

**Faith-Trails: A Closer Walk for Kids** is an interactive Bible-adventure web application designed to help children learn Scripture through narrated stories, activities, quizzes, memory verses, badges, and rewards.

The completed application contains five themed series, 25 playable quests, and 75 collectible badges. Players complete every quest on Easy, Medium, and Hard to become a Faith-Trails Grand Champion.

Live application: [faithtrails.acloserwalk.org](https://faithtrails.acloserwalk.org)

## Features

- Five complete Bible-adventure series with five quests each
- Easy, Medium, and Hard play for every quest
- 75 total badges with bronze, silver, and gold difficulty levels
- Six narrated story scenes with changing illustrations in every quest
- Series-specific ElevenLabs narrators with secure environment-based configuration
- Narration preloading to reduce pauses between scenes
- Interactive matching, sequencing, color, quiz, and memory-verse activities
- Multiple player profiles with saved progress and difficulty selection
- Animated trail map, badge collection, and 25-row Hall of Fame
- Continuous gameplay music, narration ducking, and mobile audio permission handling
- Grand Champion celebration after all 75 badges are earned
- Golden Trail, printable completion certificate, and downloadable custom badge designer
- Reusable Grand Champion screen so players can return to their certificate and custom badge
- Responsive single-page gameplay with animated screen and illustration transitions

## Complete Quest Roadmap

### Series 1 — God's Rescue and New Beginnings

1. Creation
2. Noah's Ark
3. Jonah and the Big Fish
4. Daniel and the Lions' Den
5. Moses and the Red Sea

### Series 2 — Family and Trust

1. Joseph's Colorful Coat
2. Abraham
3. Jacob
4. Ruth
5. Samuel

### Series 3 — Courage and Leadership

1. David and Goliath
2. The Apostles and Pentecost
3. Gideon
4. Esther
5. The Battle of Jericho

### Series 4 — Wisdom and Faithfulness

1. Solomon
2. The Ten Commandments
3. Elijah
4. Nehemiah
5. Job

### Series 5 — Jesus and the Good News

1. The Nativity
2. Jesus' Teachings: The Beatitudes
3. The Good Samaritan
4. Feeding the 5,000
5. Easter

## Technology

- Python and Flask
- SQLite
- HTML and Jinja templates
- CSS, Tailwind CSS, and responsive design
- Vanilla JavaScript
- ElevenLabs text-to-speech narration
- Optimized WebP scene illustrations

## Project Structure

```text
faith-trails/
├── app.py                         Flask application and API routes
├── schema.sql                     Fresh-install SQLite schema
├── generate_narration.py          ElevenLabs narration generator
├── narration_utils.py             Narration indexing and cache filenames
├── quest_content_series2.py       Series 2 quest content
├── quest_content_series3.py       Series 3 quest content
├── quest_content_series4.py       Series 4 quest content
├── quest_content_series5.py       Series 5 quest content
├── prepare_grand_champion_test.py Optional 74-badge test-player setup
├── test_faith_trails.py           Automated integration tests
├── requirements.txt               Python dependencies
├── static/
│   ├── audio/quests/              Generated narration files
│   ├── css/                       Application styling
│   ├── img/quests/                Quest covers and scene illustrations
│   ├── js/                        Gameplay, audio, and player navigation
│   └── music/                     Gameplay and celebration music
└── templates/                     Flask and Jinja page templates
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/songbird12865/faith-trails.git
cd faith-trails
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the database

If you already have `faith_trails.db`, keep it and make a backup before updating the application. The app performs a non-destructive quest-catalog migration when the site is opened.

For a brand-new installation only, create the database from `schema.sql`:

```bash
sqlite3 faith_trails.db ".read schema.sql"
```

> **Warning:** Do not run `schema.sql` against an existing application database. It drops and recreates the tables, which would erase player profiles and badge progress.

### 5. Start the application

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

## Narration Setup

Keep the ElevenLabs API key outside the source code. Set it as an environment variable before generating narration or starting the hosted application.

Windows PowerShell example:

```powershell
$env:ELEVENLABS_API_KEY="your_api_key"
$env:ELEVENLABS_VOICE_ID_SERIES_1="your_series_1_voice_id"
$env:ELEVENLABS_VOICE_ID_SERIES_2="your_series_2_voice_id"
$env:ELEVENLABS_VOICE_ID_SERIES_3="your_series_3_voice_id"
$env:ELEVENLABS_VOICE_ID_SERIES_4="your_series_4_voice_id"
$env:ELEVENLABS_VOICE_ID_SERIES_5="your_series_5_voice_id"
```

Generate any missing narration files:

```bash
python generate_narration.py
```

Narration filenames are based on the text and selected voice. Existing matching recordings are reused, while revised narration automatically receives a new filename. If a recording is unavailable, the application can fall back to the device voice.

Never commit an ElevenLabs API key, `.env` file containing secrets, or PythonAnywhere configuration containing credentials.

## Automated Testing

Run the complete integration test suite from the project root:

```bash
python -m unittest -v test_faith_trails.py
```

The current suite contains 39 tests covering player profiles, all five series, quest content, difficulty levels, badges, narration indexing, scene artwork, saved progress, and the 75-badge Grand Champion trigger.

## Grand Champion Test Player

The optional setup script creates a disposable player with 74 of 75 badges. Easter on Hard remains unfinished so the final celebration can be tested without manually completing every earlier quest.

```bash
python prepare_grand_champion_test.py
```

Select **Grand Champion Test**, open Series 5, and complete Easter on Hard.

Remove the test player afterward:

```bash
python prepare_grand_champion_test.py --remove
```

The script changes only the disposable test profile and does not alter other players' progress.

## PythonAnywhere Deployment Notes

1. Back up the live project folder and `faith_trails.db`.
2. Upload the updated application files without replacing the live database.
3. Keep `ELEVENLABS_API_KEY` and narrator voice IDs in the PythonAnywhere environment or WSGI configuration.
4. Reload the web application from the PythonAnywhere Web tab.
5. Open the site once so the non-destructive quest-catalog migration runs.
6. Verify player selection, narration, difficulty changes, badges, Hall of Fame, and quest completion.

Do not place credentials directly in `app.py`, `generate_narration.py`, or any file committed to GitHub.

## Before Committing to GitHub

Review `git status` and confirm that secrets, local environments, cache files, and player data are not included. These items should remain untracked:

```text
.env
.venv/
__pycache__/
*.pyc
faith_trails.db
```

Keep the application code, templates, styles, JavaScript, quest artwork, music, and required narration assets in the repository. Then commit the completed build:

```bash
git status
git add .
git commit -m "Complete Faith-Trails five-series app"
git push
```

## Music Credit

Gameplay and celebration music are provided by [FiftySounds](https://www.fiftysounds.com/).

## Project Owner

Created by **Melissa Joyce** as part of the *A Closer Walk* children's ministry and software-development portfolio.

- Website: [acloserwalk.org](https://acloserwalk.org)
- GitHub: [songbird12865](https://github.com/songbird12865)
- LinkedIn: [Melissa Joyce](https://www.linkedin.com/in/melissa-joyce-21147386/)

## Copyright

Copyright © 2026 Melissa Joyce. All rights reserved. This project is shared publicly for portfolio and demonstration purposes. The code, artwork, narration, branding, and written content may not be copied, redistributed, or used commercially without permission.
