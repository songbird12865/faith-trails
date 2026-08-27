# Faith-Trails: A Closer Walk for Kids

**Faith-Trails** is an interactive Bible-learning adventure designed to help children learn about God through stories, quizzes, activities, memory verses, animated scenes, narration, music, and collectible rewards.

Rather than presenting Bible lessons as static pages, Faith-Trails turns learning into an interactive journey. Children travel along a visual trail, complete Bible-themed quests, earn badges, and unlock special rewards as they progress.

The application is built as a continuous single-page game experience so music, narration, animations, and player progress can continue smoothly as the child moves between activities.

## Project Highlights

* Interactive Bible-themed quests
* Multiple difficulty levels
* Animated story and activity screens
* Bible quizzes and memory verses
* Narrated game content
* Continuous background music
* Automatic music ducking during narration
* Player profiles and progress tracking
* Collectible achievement badges
* Hall of Fame badge collection
* Celebration sequences and rewards
* Responsive interface for desktop and mobile devices
* Persistent game experience without full-page reloads

## Technologies Used

* **Python**
* **Flask**
* **HTML5**
* **CSS3**
* **JavaScript**
* **JSON**
* **SQLite**
* **ElevenLabs API** for narration
* **Git & GitHub** for version control
* **PythonAnywhere** for web deployment

## Application Design

Faith-Trails uses a Flask backend with a JavaScript-driven single-page game interface.

The browser remains inside one continuous game shell while JavaScript renders the trail map, Bible stories, activities, quizzes, memory verses, badge collection, Hall of Fame, and celebration sequences. This design prevents unnecessary page reloads and allows background music and animations to continue smoothly throughout gameplay.

The backend manages game content, player profiles, difficulty levels, badge persistence, and JSON endpoints used by the front end.

## Main Architecture

* `templates/game.html` — Permanent game shell
* `static/js/game.js` — Controls the trail map, story scenes, activities, quizzes, memory verses, badge collection, Hall of Fame, and celebrations
* `static/js/audio-engine.js` — Manages continuous gameplay music, narration ducking, and music transitions
* `static/css/style.css` — Responsive game interface, visual styling, and animations
* `app.py` — Flask application containing quest content, profiles, difficulty handling, badge persistence, and JSON endpoints
* `static/audio/quests/` — Stores generated narration used throughout the game

## Audio and Narration

Faith-Trails incorporates narration and background music to create a more immersive experience for children.

Narration can be generated through the ElevenLabs API and stored with the game's audio assets. During narration, the audio engine automatically lowers the background music so spoken content remains clear. Music returns to its normal level after narration finishes.

If narration is unavailable, the game continues normally rather than preventing the child from completing the activity.

## Player Progress and Rewards

Faith-Trails was designed to encourage children to continue learning by rewarding progress.

Players earn badges by completing Bible-learning activities at different difficulty levels. Their achievements are displayed in the Hall of Fame, allowing them to see their progress as they continue along the Faith-Trails journey.

Additional celebration and reward features are incorporated into the game to make completing milestones feel meaningful and fun.

## Responsive and Mobile Design

The application is designed to work on both desktop and mobile devices.

The current web architecture also provides a foundation for future packaging as a mobile application. Mobile-store packaging, offline asset management, privacy and parental information, application icons, splash screens, and store metadata can be handled as a separate release phase.

## Run Locally

1. Clone or download the repository.

2. Open a terminal in the project folder.

3. Install the required dependencies:

   `python -m pip install -r requirements.txt`

4. Start the application:

   `python app.py`

5. Open the local application in your browser:

   `http://127.0.0.1:5000`

The included database preserves existing player and progress data. To create a new database, run:

`python init_db.py`

## Environment Configuration

For production deployment, set `FAITH_TRAILS_SECRET_KEY` to a secure private value in the hosting environment.

For ElevenLabs narration, set `ELEVENLABS_API_KEY` in the server environment. `ELEVENLABS_VOICE_ID` may also be configured when needed.

**API keys and secret values should never be committed to the GitHub repository.**

## Future Development

Faith-Trails is an evolving project. Planned development includes expanding the number of Bible quests and rewards, continuing mobile optimization, and preparing the application for eventual mobile distribution.

The existing single-page architecture was designed to provide a foundation for that continued expansion.

## What I Learned

Developing Faith-Trails has allowed me to combine front-end and back-end development within a larger application of my own design.

The project has strengthened my experience with Python and Flask development, JavaScript-driven interfaces, responsive design, application state, persistent player data, API integration, multimedia management, debugging, deployment, and Git-based version control.

It has also given me experience designing software around the needs of a specific audience rather than simply implementing individual programming requirements.

## Author

**Melissa Joyce**

B.S. Information Technology
Strayer University — Expected December 2026

---

*Faith-Trails is an independently developed educational application created to make Bible learning interactive, engaging, and rewarding for children.*

