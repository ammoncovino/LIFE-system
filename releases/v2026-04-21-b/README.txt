LIFE System — v2026.04.21-b — 18-Species Scale-Up
==================================================

Owner: Family Fun Group
Governed by the locked 8-question spine. Structure never changes; only ANSWERS simplify across tiers.

Folder contents:

  k5_json/            18 canonical K-5 JSONs (10-19 words/answer, K-2 floor, K-5 ceiling).
                      These drive the Student Totem + Micro Totem renders. Single source of truth.

  tier1_json/         18 Tier 1 (under 13) LLM sources — animal-voice, locked 8 ONLY,
                      forbidden-word list active. 'ground_truth_k5' field mirrors the K-5 JSON.

  tier2_json/         18 Tier 2 (13 and up) LLM sources — naturalist voice,
                      full master bullets + scientific name, conservation, Alpha/Omega lens note.

  student_totems/     18 Student Totem PDFs (LETTER portrait, navy #2C3481, public signage).
                      Filename pattern: STUDENT_{slug}.pdf

  micro_totems/       18 Micro Totem PDFs (3.5 x 2 in business-card size, front+back on letter page).
                      Pocket 5-of-8 Q/A with identical wording. Filename pattern: MICRO_{slug}.pdf

Locked constants (every file):
  - 8-question spine (exact wording, exact order)
  - Closing:  "LOOK AT THE ANIMAL: What do you see it doing right now?"
  - Footer:   "What a living thing can sense becomes its reality."
              "Environment shapes design."
  - Tagline:  "A [X] [Y] that lives in [Z]."

Forbidden words (never appear in Tier 1 or K-5):
  binocular, canopy, anogenital, territory, diurnal, nocturnal, brumation,
  metabolic rate, chemical particles, perception, vocalization, psychological,
  talk / talks / talking

To rebuild any PDF after editing a K-5 JSON:
  python /home/user/workspace/build_student_totem_generic.py
  python /home/user/workspace/build_micro_totem_generic.py

QA:
  python /home/user/workspace/qa_check.py     # expects: 0 errors, ALL CHECKS PASSED
