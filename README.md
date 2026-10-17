# Faith-Trails — A Closer Walk for Kids

Faith-Trails is a Bible-based interactive adventure game for children, created as part of the A Closer Walk collection.

**Website:** https://faithtrails.acloserwalk.org  
**Project repository:** https://github.com/songbird12865/faith-trails

## About the game

Players explore Bible stories along a visual trail, answer questions, complete interactive activities, practice memory verses, and earn achievement badges.

### Features

- Five themed series containing 25 quests in total
- Easy, Medium, and Hard difficulty options
- Up to 75 quest badges and a Hall of Fame progress display
- Story illustrations, narration, and background music controls
- Interactive quizzes, sequencing, matching, and memory-verse activities
- Series 1 Champion celebration, printable certificate, and custom badge designer
- Responsive interface for mobile and desktop

## Technology

The web application uses Python and Flask for its server-side functionality, with HTML, CSS, and JavaScript for the interactive game interface. The project also includes iOS and Android packaging/build work.

## Project organization

The repository contains the Flask application and its templates and static assets. Important front-end files include:

- `game.js` — quest screens, activities, progress displays, and celebrations
- `audio-engine.js` — music playback and toggle handling
- `player-navigation.js` — player/profile navigation
- `style.css` — main game styling

File locations may differ between releases; consult the repository's actual directory structure.

## Running locally

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the Python dependencies listed in the repository's requirements file, if present.
4. Configure any environment settings required by the Flask application.
5. Start the application using its documented Flask entry point.

The exact startup command depends on the version of the repository. Do not assume that a specific module name or configuration is available without checking the source.

## Audio and attribution

The project uses recorded narration and licensed music. FiftySounds music requires attribution wherever its tracks are used:

**FiftySounds:** https://www.fiftysounds.com

Audio and other third-party assets remain subject to their respective licenses. Do not redistribute licensed assets separately or assume that this README grants permission to reuse them.

## Privacy

Review the application's published privacy policy for current information about player data and storage. Do not include private keys, signing certificates, passwords, or provisioning profiles in a public repository.

## Ownership

Faith-Trails is an A Closer Walk project. Original application content, artwork, and branding are reserved by their respective owners; third-party materials remain under their original licenses.

## Support

Visit https://acloserwalk.org for information about A Closer Walk and its projects.
