-- Safe migration for an existing Faith-Trails database.
-- Preserves every player and earned badge.
UPDATE quests
SET is_available = 1
WHERE slug IN ('david-goliath', 'jonah-big-fish', 'daniel-lions-den');
