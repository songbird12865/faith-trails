-- Faith Trails: A Closer Walk for Kids
-- Database schema (SQLite)

DROP TABLE IF EXISTS badges_earned;
DROP TABLE IF EXISTS quests;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- UNIQUE + COLLATE NOCASE: every player needs a distinct name (case-
    -- insensitive) so the "Who's Playing?" picker can tell them apart.
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    -- Chosen once by the child when they set up their profile ("log in").
    -- Applies to every quest until they deliberately change it. NULL means
    -- they haven't picked a difficulty yet (shown the picker on first visit).
    current_difficulty TEXT CHECK (current_difficulty IN ('easy', 'medium', 'hard'))
);

CREATE TABLE quests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    icon TEXT NOT NULL,          -- emoji fallback used in the badge corner
    sort_order INTEGER NOT NULL,
    is_available INTEGER NOT NULL DEFAULT 0  -- 1 = playable now, 0 = "coming soon"
);

CREATE TABLE badges_earned (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quest_id INTEGER NOT NULL,
    -- A badge is tied to the difficulty it was earned at. This is what
    -- makes switching difficulty feel like "starting over": a medium
    -- badge doesn't count as a hard badge, so the trail map shows a
    -- fresh, unearned set when the child switches levels. Nothing is
    -- ever deleted -- old badges are still in the table -- but only the
    -- badges matching the profile's current_difficulty are shown.
    difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    earned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (quest_id) REFERENCES quests(id),
    UNIQUE(user_id, quest_id, difficulty)
);

-- Seed data: just the trail's story quests. Player profiles are no
-- longer pre-seeded -- each player creates their own via the "New
-- Player" screen (/players/new), which is what makes the "Who's
-- Playing?" picker meaningful once more than one profile exists.
-- Order matches the zigzag map layout: 1-3 across the top row,
-- 4-6 across the bottom row, read left to right on each row.

INSERT INTO quests (slug, title, summary, icon, sort_order, is_available) VALUES
    ('noahs-ark', 'Noah''s Ark', 'Help gather the animals two by two!', '🐘', 1, 1),
    ('josephs-coat', 'Joseph''s Colorful Coat', 'A gift of many colors starts a big adventure.', '🧥', 2, 1),
    ('red-sea', 'Moses and the Red Sea', 'Watch the sea part in an amazing rescue.', '🌊', 3, 1),
    ('david-goliath', 'David & Goliath', 'A small shepherd faces a giant.', '🪨', 4, 0),
    ('jonah-big-fish', 'Jonah and the Big Fish', 'Swallowed up on a wild, watery journey.', '🐋', 5, 0),
    ('daniel-lions-den', 'Daniel and the Lions'' Den', 'Stay brave through a scary night.', '🦁', 6, 0);
