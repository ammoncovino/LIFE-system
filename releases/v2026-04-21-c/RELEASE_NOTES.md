# LIFE System — Release v2026.04.21-c

**Date:** April 21, 2026
**Tag:** `v2026.04.21-c`
**Previous:** v2026.04.21-b

## Summary

Styled edition of the 18 Student Totems. Replaces the flat-layout totems from v2026.04.21-b with a parchment + dark-wood layout and painterly AI-generated illustrations for every species. All text content (the locked 8-question spine and K-5 answers) is unchanged from v2026.04.21-b.

## What's new

### Visual design
- Full-page cream parchment background (AI-generated texture)
- Dark wood title band with Cinzel Bold common name + Cormorant Italic scientific name, both in cream
- 8 Q blocks rendered on parchment, left column, auto-shrink to fit
- Right column: painterly AI illustration of the species in natural habitat, framed with gold hairline
- Dark wood "Think About This" band: per-species reflection question (12-20 words), cream italic, centered
- Dark wood footer band: both locked lines, cream italic, centered

### AI illustrations
- 18 painterly / field-guide-style plates, **generated in-house — no internet images**
- Three-quarter views, rich textured brushwork, species-accurate anatomy, natural habitats
- Downsized to ~220 dpi at panel size, JPEG quality 82 — keeps each PDF under 1 MB

### New per-species content
- `think_about_this.py` — 18 reflection questions grounded in the master bullets
- Each question validated to 12-20 words, sense/adaptation/environment themed

### Build engineering
- `build_styled_totem.py` — ReportLab canvas-level builder
- Background and image embedding write optimized JPEGs to temp files, so ReportLab embeds them verbatim (avoids the BytesIO raw-pixel bloat that would have produced 20 MB PDFs)
- Auto-scaling title font (22-34pt) handles long names (e.g. "Black and White Ruffed Lemur")
- Auto-shrinking Q-block body text so all 8 answers fit regardless of length

## Locked rules preserved

- 8 locked questions, exact wording and order
- Footer: "What a living thing can sense becomes its reality." / "Environment shapes design."
- K-5: 10-19 words per answer
- "WE SIMPLIFY ANSWERS — NOT STRUCTURE"
- Owner: Family Fun Group, $350/card max

## Files

```
releases/v2026-04-21-c/
├── styled_totems/                 18 × ~900 KB PDFs
├── images/                        18 × ~500 KB JPEG illustrations
├── textures/                      2 × background textures
├── build_scripts/
│   ├── build_styled_totem.py
│   └── think_about_this.py
├── README.txt
└── RELEASE_NOTES.md
```

Total size: ~25 MB.

## Reproducing

The build pulls:
- K-5 JSON content from `LIFE_k5_locked/*.json` (already in-repo from v2026.04.21-b)
- Species metadata from `LIFE_totem_content_18.json` (in-repo)
- Fonts: Cinzel (Google Fonts), Cormorant Garamond (Google Fonts), Inter (Google Fonts)
- Textures + illustrations from this release directory

Run: `python build_scripts/build_styled_totem.py`
