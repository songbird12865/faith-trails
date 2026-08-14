# Faith-Trails Commenting Notes

This revision adds comments and docstrings where a future developer would need
context to maintain the application safely. Comments focus on intent,
architecture, browser constraints, data integrity, and non-obvious behavior.

## Commented areas

- Flask and SQLite maintenance safeguards
- Single-page game state and scene dispatch
- Safe insertion of player/content text into generated HTML
- Responsive SVG trail calculation
- Memory-verse duplicate-word handling and answer normalization
- Narration fallback and music ducking
- Mobile browser audio authorization and crossfade behavior
- Server-confirmed badge and Champion progress
- Narration filename caching and generation scripts
- Template bootstrap data and session-related flows
- CSS sections for rewards, narration, print, and reduced motion

Straightforward declarations and self-explanatory styling are intentionally not
commented line by line. Excess comments can make code harder to maintain when
they merely repeat what the next statement already says.
