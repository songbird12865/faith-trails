# Faith-Trails scene illustrations

Store story-specific artwork here, grouped by quest slug. WebP is recommended
for smaller mobile downloads; JPEG also works.

Example:

```text
static/img/quests/scenes/abraham/01-leaving-home.webp
static/img/quests/scenes/abraham/02-promised-land.webp
static/img/quests/scenes/abraham/03-stars.webp
```

Then add the relative path to the matching story scene in the quest content:

```python
{
    "type": "story",
    "emoji": "⭐",
    "image": "abraham/03-stars.webp",
    "text": "God brought Abraham outside and told him to look at the stars."
}
```

Keep recurring characters' faces, clothing, ages, proportions, and illustration
style consistent throughout one quest and series. Aim for one compressed image
per story beat, sized around 1280 by 720 pixels. The original quest cover stays
the map and badge artwork and is also the automatic fallback.
