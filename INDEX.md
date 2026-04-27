---
title: LIFE System — Master Index
maintainer: Ammon Covino
tags: [index, governance]
---

# LIFE System — Master Index

> Open this in Obsidian. Every list below auto-populates from frontmatter — never edit by hand.

## Locked Phrases & Governance
- [[LOCKED_PHRASES]] — canonical strings used everywhere
- [[06_governance/TERMINOLOGY|Terminology]]
- [[06_governance/AI_GOVERNANCE|AI Governance]]
- [[06_governance/DECISIONS_AND_OPEN_THREADS|Decisions & Open Threads]]
- [[06_governance/SYSTEM_EVALUATION|System Evaluation]]

## Species (auto-listed)

```dataview
TABLE
  scientific AS "Scientific",
  trophic AS "Trophic",
  status AS "Status",
  version AS "Version"
FROM "species"
SORT common_name ASC
```

## Drift Watch — Anything Stale or Drafted

```dataview
LIST
FROM "species" OR "templates" OR "locked_phrases"
WHERE status = "draft"
```

## SOPs

```dataview
TABLE owner, venue, version, status
FROM "03_operations" OR "sops"
WHERE contains(file.tags, "#sop")
```

## Releases (latest)
- [[releases/v2026-04-26b|v2026-04-26b — Diet Cards (18 species)]]
- [[releases/v2026-04-25k|v2026-04-25k — Path B (door sign + totem)]]
- [[releases/v2026-04-25j|v2026-04-25j — Path A (GS-10 lock + GS-16)]]
- [[releases/gold_standard_v2026-04-25|Gold Standard Posters]]

## Build Scripts
- `08_build/` — all PDF generators
- `/tmp/build_diet_card.py` (parameterized template)
- `/tmp/build_all_diet_cards.py` (master builder)

## How To Use This Vault
- See [[OBSIDIAN_README]]
