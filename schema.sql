-- Faith Trails: A Closer Walk for Kids
-- Database schema (SQLite)

DROP TABLE IF EXISTS badges_earned;
DROP TABLE IF EXISTS quests;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
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
    earned_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (quest_id) REFERENCES quests(id),
    UNIQUE(user_id, quest_id)
);

-- Seed data: one demo child profile (name left blank until the player
-- creates it on first visit), and the trail's story quests.
-- Order matches the zigzag map layout: 1-3 across the top row,
-- 4-6 across the bottom row, read left to right on each row.
INSERT INTO users (id, name) VALUES (1, '');

INSERT INTO quests (slug, title, summary, icon, sort_order, is_available) VALUES
    ('noahs-ark', 'Noah''s Ark', 'Help gather the animals two by two!', '🐘', 1, 1),
    ('josephs-coat', 'Joseph''s Colorful Coat', 'A gift of many colors starts a big adventure.', '🧥', 2, 1),
    ('red-sea', 'Moses and the Red Sea', 'Watch the sea part in an amazing rescue.', '🌊', 3, 0),
    ('david-goliath', 'David & Goliath', 'A small shepherd faces a giant.', '🪨', 4, 0),
    ('jonah-big-fish', 'Jonah and the Big Fish', 'Swallowed up on a wild, watery journey.', '🐋', 5, 0),
    ('daniel-lions-den', 'Daniel and the Lions'' Den', 'Stay brave through a scary night.', '🦁', 6, 0);
