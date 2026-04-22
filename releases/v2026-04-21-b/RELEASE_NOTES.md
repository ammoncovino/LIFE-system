# LIFE System Release v2026.04.21-b

**Scope:** 18-species canonical K-5 + Tier 1 + Tier 2 JSON set + 18 Student Totem PDFs + 18 Micro Totem PDFs + per-species Alpha/Omega failure cycles.

## What's in this release

| Folder            | Count | Description                                                                 |
|-------------------|-------|-----------------------------------------------------------------------------|
| `k5_json/`        | 18    | Canonical K-5 totems (10-19 words/answer, no forbidden words, locked spine) |
| `tier1_json/`     | 18    | Tier 1 — animal-voice, locked 8 questions, K-5 ceiling                      |
| `tier2_json/`     | 18    | Tier 2 — naturalist voice + per-species Alpha/Omega failure cycle           |
| `student_totems/` | 18    | Student Totem PDFs (LETTER portrait)                                        |
| `micro_totems/`   | 18    | Micro Totem PDFs (3.5×2 in card, front+back)                                |
| `build_scripts/`  | 9     | Python builders + QA scripts + master source JSON + per-species bullets     |

Also included: `LIFE_v2026-04-21-b_all_18.zip` (5.4 MB all-in-one archive).

## Species (18)

alpaca, argentine-tegu, bennetts-wallaby, black-and-white-ruffed-lemur, capybara, geoffroys-spider-monkey, kinkajou, linnes-two-toed-sloth, monkey-tailed-skink, nine-banded-armadillo, patagonian-mara, prehensile-tailed-porcupine, rabbit, red-ruffed-lemur, ring-tailed-lemur, sailfin-dragon, sulcata-tortoise, toco-toucan.

## Alpha/Omega failure cycle structure (Tier 2)

Each Tier 2 JSON carries a four-part `alpha_omega_failure_cycle` object:

- `broadly_accepted` — 4 items
- `still_debated` — 3 items
- `common_failure_modes` — 3 items
- `species_specific_guardrails` — 3 items

Total: 234 items across the 18 species, all unique (QA-verified).

## Locked rules (governing this release)

- "WE SIMPLIFY ANSWERS — NOT STRUCTURE"
- Locked 8-question spine, tagline format, K-5 closing + footer — see `README.txt`
- K-5 word count: 10-19 words/answer
- Forbidden words list enforced
- Owner: Family Fun Group. $350/card max.

## Rebuilding from source

```bash
cd build_scripts/
python build_all_k5_jsons.py
python build_tier_content.py
python build_alpha_omega_failure_cycles.py
python build_student_totem_generic.py
python build_micro_totem_generic.py
python qa_check.py
python qa_alpha_omega.py
```
