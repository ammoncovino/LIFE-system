# LIFE v2026.04.23 — Additions to Master Binder

**Release date:** 23 April 2026
**Philosophy:** *Additions, not replacements.* The master binder grows; each site prints the subset they need.

---

## What's new in this release

### New species (3 totems + 8 diet cards)

| Species | Sites | USDA Banner |
|---|---|---|
| Keel-Billed Toucan *(Ramphastos sulfuratus)* | Houston · SAA · Other | ✓ |
| Southern Three-Banded Armadillo *(Tolypeutes matacus)* | Houston · SAA · Other | ✓ |
| Six-Banded Armadillo *(Euphractus sexcinctus)* | SAA | ✓ |
| Chinese Water Dragon *(Physignathus cocincinus)* | diet card only | — |
| Veiled Chameleon *(Chamaeleo calyptratus)* | diet card only | — |
| Leopard Tortoise *(Stigmochelys pardalis)* | diet card only | — |
| Russian Tortoise *(Testudo horsfieldii)* | diet card only | — |
| Yellow-Foot Tortoise *(Chelonoidis denticulatus)* | diet card only | — |

### Red Ruffed Lemur totem — corrected
- `q6_babies` now reads "up to six infants after about 102 days of gestation, though litters of two to three are most common." (Prior text incorrectly capped at 2–3.)
- Verified against Duke Lemur Center, San Diego Zoo Fact Sheet, and Animal Diversity Web.

### New framing band on all 26 diet cards
- **Morning Feed-Out** vs **Encounter/Enrichment Portion** now split on every card.
- Answers Mia Ketsa's question: encounters draw *bite-sized portions* from the daily diet allocation, not separate meals.

### Per-site print subset lists
- `site_prints/PRINT_LIST_Houston.md` — 23 species
- `site_prints/PRINT_LIST_SAA.md` — 21 species (includes six-banded armadillo)
- `site_prints/PRINT_LIST_Other.md` — 23 species
- `site_prints/PRINT_LIST_ALL_SITES.md` — combined reference

### Historical (retired from floor, kept in master binder)
- Toco Toucan → replaced by Keel-Billed Toucan (all sites)
- Nine-Banded Armadillo → replaced by Southern Three-Banded (all sites)

---

## Folder layout

```
releases/v2026-04-23/
├── README.md                                        ← this file
├── LIFE_Totems_v2026-04-23_additions.pdf           ← 3 new totems + fixed red ruffed lemur
├── LIFE_diet_cards_all_26_v2026-04-23.pdf          ← combined 26-card binder
├── content/
│   ├── LIFE_diet_content_v23.json                  ← 26 species, sites + framing fields
│   └── LIFE_totem_content_21.json                  ← 21 species (18 existing + 3 new)
├── diet_cards/                                      ← 26 individual PDFs
├── totems/                                          ← 4 styled base PDFs
├── totems_usda/                                     ← 4 USDA-stamped final PDFs
├── site_prints/                                     ← Houston / SAA / Other / all
├── source/                                          ← builders
└── preview/                                         ← QA preview images
```

## Printing guidance

- Print **only the species on your site** — see `site_prints/PRINT_LIST_<site>.md`.
- All mammal and bird totems carry the **USDA Federally Licensed** banner and should be the `totems_usda/` versions.
- Diet cards print 8.5×11 portrait. Totems print 8.5×14 legal portrait (same as prior releases).

## Design constants (locked)

- Framing: *"The animals teach. The keeper guides. You observe."*
- Footer: *"What a living thing can sense becomes its reality. / Environment shapes design."*
- FREE learning experience; tip is optional ($3–$10); never front-loaded.

---

*Part of the LIFE master binder, maintained by Ammon Covino.*
