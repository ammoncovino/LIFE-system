# v2026-04-28d Release Manifest

**Release date:** 2026-04-28
**Owner:** Ammon Covino
**Tag:** v2026-04-28d-full-audit-and-reorg

## Summary

A three-part delivery:
1. **Diet fix** — 4 missing tortoise diet cards (red-foot, yellow-foot, russian, leopard) + full audit of all 22 canonical species against wild-diet science
2. **Totems** — 5 totem types built for each new tortoise (door, walk-by, micro, styled, student); 20 narration suite totems with $300/night rental info
3. **Repo reorg** — top-level `STAFF_FIRST/`, `by_species/`, `by_asset_type/`, `narration_suites/` folders so staff reading is up front and assets are grouped by both species and type

## File inventory

### Diet cards (4 new)
- `diet_cards/diet_card_red_foot_tortoise.pdf` — 55% fruit / 35% greens / 10% protein (weekly)
- `diet_cards/diet_card_yellow_foot_tortoise.pdf` — 75% greens / 20% fruit / 5% protein (weekly)
- `diet_cards/diet_card_russian_tortoise.pdf` — 90% leafy greens & weeds, NO protein, fruit only a few times/year
- `diet_cards/diet_card_leopard_tortoise.pdf` — 70% grasses + 30% greens, NO protein, NO fruit

### Diet audit
- `diet_drift_audit_v2026-04-28d.pdf` — all 22 species cross-referenced against wild-diet science; 15 OK / 4 NEW / 3 VERIFY-on-floor

### Tortoise totems (20 PDFs — 5 types × 4 species)
- `totems/door_totem_<species>_HOUSTON.pdf` — encounter entry door sign (×4)
- `totems/walkby_totem_<species>.pdf` — corridor pull-tab totem (×4)
- `totems/micro_totem_<species>.pdf` — small handheld card (×4)
- `totems/styled_totem_<species>.pdf` — full glamour totem (×4)
- `totems/student_totem_<species>.pdf` — STEM/classroom version (×4)

### Narration suite totems (20 PDFs)
- `narration_suites/narration_suite_01_reflection_suite.pdf` through `narration_suite_20_life_synthesis_suite.pdf`
- Each totem includes: suite number, anchor (fairy tale), governing statement, visitor prompt, LIFE principle, QR entry URL, and full $300/night rental info (hours, capacity, includes, guest brings, rules, booking)

### Canonical species files (4 new)
- `species/red_foot_tortoise.md`
- `species/yellow_foot_tortoise.md`
- `species/russian_tortoise.md`
- `species/leopard_tortoise.md`

### Repo reorg (new top-level folders)
- `STAFF_FIRST/README.md` — day-one reading order, quick-reference cards, complete training manuals, locked rules
- `by_species/<species>/` — 22 folders, one per animal, with all assets for that species in one place
- `by_asset_type/<asset>/` — 7 folders (diet_cards, door_totems, walkby_totems, micro_totems, styled_totems, student_totems, narration_suite_totems)
- `narration_suites/` — all 20 narration suite totems
- Updated `README.md` and `INDEX.md` at repo root pointing to the new structure first

## Audit findings — diet drift

| Status | Count | Species |
|---|---|---|
| **OK — aligned** | 15 | alpaca, argentine_tegu, black_and_white_ruffed_lemur, capybara, kinkajou, monkey_tailed_skink, nine_banded_armadillo, patagonian_mara, prehensile_tailed_porcupine, rabbit, red_ruffed_lemur, spider_monkey, sulcata, toco_toucan, wallaby |
| **NEW — built v2026-04-28d** | 4 | red_foot_tortoise, yellow_foot_tortoise, russian_tortoise, leopard_tortoise |
| **VERIFY ON FLOOR** | 3 | ring_tailed_lemur, sailfin_dragon, two_toed_sloth |

The 3 VERIFY species aren't wrong, but their current 90/10 cards may benefit from a more nuanced split (life-stage, leaf/protein supplement). Schedule a 30-minute floor walk with the lead keeper before the next print cycle.

## Locked elements honored

- Brown palette `#3E2C1C` `#6E522B` `#A47A4A`
- Footer: *What a living thing can sense becomes its reality. Environment shapes design.*
- Tagline: *Match the bowl. Don't interpret.*
- *Animals are TEACHERS, not attractions.*
- Sulcata = ONLY hay-only species
- Escalation phrase: *"This looked like we should take it out. What would you like to do here?"*
- Manager on duty (never named)
- PDF Author: Perplexity Computer; descriptive Title on each PDF

## Source citations (wild-diet science)

- **Tortoise Trust** — https://www.tortoisetrust.org/articles/feeding_redfoots.html
- **Arizona Exotic Animal Hospital** — https://azeah.com/tortoises-turtles/basic-care-red-foot-tortoise
- **Tropical Edu International** — https://tropicaledu.com/yellow-footed-tortoise-a-beauty-from-south-america/
- **Reptiles Magazine** — https://reptilesmagazine.com/yellow-footed-tortoise-versus-red-footed-tortoise-care/
- **Wikipedia** (leopard, yellow-foot) — https://en.wikipedia.org/wiki/Leopard_tortoise
- **PetMD** — https://www.petmd.com/russian-tortoise-agrionemys-horsfieldii
- **Garden State Tortoise** — https://www.gardenstatetortoise.com/post/tortoise-diet-testudo-species
- **Utica Zoo** — https://www.uticazoo.org/leopardtortoise/

## Next steps

1. Print the 4 new tortoise diet cards and post at exhibit
2. Schedule a 30-min floor walk to review the 3 VERIFY species
3. Print the 20 narration suite totems and post at suite entries
4. Optional: build the missing student/walkby/door totems for the existing 18 species (next sprint)
