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
    is_available INTEGER NOT NULL DEFAULT 0, -- 1 = playable now, 0 = "coming soon"
    series_number INTEGER NOT NULL,
    series_order INTEGER NOT NULL
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
-- The 25 adventures are grouped into five themed series. Existing playable
-- adventures retain their slugs so saved badge relationships remain stable.

INSERT INTO quests (slug, title, summary, icon, sort_order, is_available, series_number, series_order) VALUES
    ('creation', 'Creation', 'Discover how God created a beautiful world.', '🌍', 1, 1, 1, 1),
    ('noahs-ark', 'Noah''s Ark', 'Help gather the animals two by two!', '🐘', 2, 1, 1, 2),
    ('jonah-big-fish', 'Jonah and the Big Fish', 'Follow Jonah through a wild, watery rescue.', '🐋', 3, 1, 1, 3),
    ('daniel-lions-den', 'Daniel and the Lions'' Den', 'Stay brave through a scary night.', '🦁', 4, 1, 1, 4),
    ('red-sea', 'Moses and the Red Sea', 'Watch God rescue His people and part the sea.', '🌊', 5, 1, 1, 5),
    ('josephs-coat', 'Joseph''s Colorful Coat', 'Learn how God remained with Joseph.', '🧥', 1, 1, 2, 1),
    ('abraham', 'Abraham', 'Trust God''s promises, even while waiting.', '⭐', 2, 1, 2, 2),
    ('jacob', 'Jacob', 'See how God changed Jacob''s heart and future.', '🪜', 3, 1, 2, 3),
    ('ruth', 'Ruth', 'Walk with Ruth in loyalty, kindness, and trust.', '🌾', 4, 1, 2, 4),
    ('samuel', 'Samuel', 'Listen for God''s voice with young Samuel.', '🕯️', 5, 1, 2, 5),
    ('david-goliath', 'David & Goliath', 'A young shepherd trusts God and faces a giant.', '🪨', 1, 1, 3, 1),
    ('apostles-pentecost', 'The Apostles and Pentecost', 'Filled with the Holy Spirit, they boldly share the good news.', '🔥', 2, 0, 3, 2),
    ('gideon', 'Gideon', 'Discover how God works through a small, faithful army.', '🏺', 3, 0, 3, 3),
    ('esther', 'Esther', 'See how Esther courageously speaks for her people.', '👑', 4, 0, 3, 4),
    ('jericho', 'The Battle of Jericho', 'Follow God''s unusual plan with courage and faith.', '🎺', 5, 0, 3, 5),
    ('solomon', 'Solomon', 'Ask God for wisdom like King Solomon.', '⚖️', 1, 0, 4, 1),
    ('ten-commandments', 'The Ten Commandments', 'Learn the loving instructions God gave His people.', '📜', 2, 0, 4, 2),
    ('elijah', 'Elijah', 'Stand faithfully for God on Mount Carmel.', '🔥', 3, 0, 4, 3),
    ('nehemiah', 'Nehemiah', 'Help rebuild Jerusalem''s wall with prayer and perseverance.', '🧱', 4, 0, 4, 4),
    ('job', 'Job', 'Hold on to faith when life is difficult.', '🙏', 5, 0, 4, 5),
    ('nativity', 'The Nativity', 'Celebrate the birth of Jesus, God''s promised Son.', '⭐', 1, 0, 5, 1),
    ('beatitudes', 'Jesus'' Teachings: The Beatitudes', 'Learn Jesus'' surprising picture of a blessed life.', '⛰️', 2, 0, 5, 2),
    ('good-samaritan', 'The Good Samaritan', 'Discover what it means to love your neighbor.', '❤️', 3, 0, 5, 3),
    ('feeding-5000', 'Feeding the 5,000', 'See Jesus multiply five loaves and two fish.', '🐟', 4, 0, 5, 4),
    ('easter', 'Easter', 'Follow the story of Jesus'' death and resurrection.', '✝️', 5, 0, 5, 5);
