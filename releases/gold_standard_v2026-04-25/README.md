# LIFE Gold Standard Verbatim Diet Posters — v2026-04-25

Print-ready Gold Standard verbatim diet posters for the **10 active totems** that the comprehensive audit (v2026-04-25) flagged as missing them.

## What this release adds

10 new Gold Standard posters — single page each, US Letter portrait, full bleed, ready to print:

| # | Species | Banner | Source §  |
|---|---|---|---|
| 1 | Ring-Tailed Lemur | USDA + Harris County | §17 |
| 2 | Red Ruffed Lemur | USDA + Harris County | §18 |
| 3 | Black-and-White Ruffed Lemur | USDA + Harris County | §19 |
| 4 | Six-Banded Armadillo | USDA | §20 |
| 5 | Southern Three-Banded Armadillo | USDA | §21 |
| 6 | Alpaca | USDA | §22 |
| 7 | Keel-Billed Toucan | USDA (post-2023 PACT) | §23 |
| 8 | Sulcata Tortoise | (no banner — exempt reptile) | §24 |
| 9 | Sailfin Dragon | Texas Parks & Wildlife | §25 |
| 10 | Monkey-Tailed Skink | (no banner — exempt reptile) | §26 |

Numbering §17–§26 continues from the 11 verbatim entries (§7–§16) already in the v2026-04-23 release.

## Files

- `LIFE_Gold_Standard_Posters_All_10_v2026-04-25.pdf` — master combined PDF (10 pages)
- `posters/GoldStandard_<slug>.pdf` — per-species single-page posters
- `gold_standard_manifest.json` — machine-readable manifest

## What "Gold Standard verbatim" means

A Gold Standard poster is the **canonical match-the-bowl reference** for a species. It is verbatim — staff do not interpret, paraphrase, or substitute. If a feeder cannot match what the poster shows, they pause and escalate.

Every Gold Standard poster includes:

1. **Gold band** (top) — identifies the document class
2. **Regulatory banner** (USDA / USDA + Harris County / TPWD / no banner)
3. **Species block** — name, scientific name, category, what-this-animal-is, sites
4. **3-second check** — single yes/no question for at-the-bowl verification
5. **Morning Feed-Out** — exact morning preparation language
6. **Encounter / Enrichment Portion** — drawn from daily allocation, never extra
7. **CORRECT foods** — visual food strip + text descriptors
8. **WRONG foods — fix immediately** — visual food strip + text descriptors
9. **Simple Build** — 1-3 line rule
10. **Prep Rule** — single-sentence action directive
11. **Match the bowl — do not interpret** enforcement banner
12. **Source attribution** — back to LIFE Master Doc §X
13. **Post-at-exhibit** footer

## Banner policy reference (verified by the comprehensive audit)

| Authority | Covers |
|---|---|
| USDA APHIS | All mammals + all birds (post-2023 PACT amendment) |
| Harris County Veterinary Public Health | Primates housed in Houston (stacks on USDA) |
| Texas Parks & Wildlife | Texas-listed exotic reptiles (tegu, sailfin, large constrictor pythons) |
| None / Exempt | Reptiles outside TPWD list (sulcata, monkey-tailed skink) |

## Photo placeholders

Three species do not yet have dedicated species photos in the LIFE photo library and currently render with closest-relative placeholders:

- **Keel-Billed Toucan** → uses Toco Toucan photo (same family — Ramphastidae)
- **Six-Banded Armadillo** → uses generic armadillo photo
- **Southern Three-Banded Armadillo** → uses generic armadillo photo

Replace these with site-shot photos before final print run if available.

## Source

- Content: `LIFE_diet_content_gs10_v2026-04-25.json`
- Builder: `build_gold_standard_posters.py`
- Engine: reuses `build_diet_cards_v23.py` rendering primitives

## Version

v2026-04-25 · Match the bowl. Don't interpret.
