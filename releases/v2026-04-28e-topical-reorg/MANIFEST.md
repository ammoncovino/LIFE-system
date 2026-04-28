# Release v2026-04-28e — Topical Reorganization

**Date:** April 28, 2026
**Driver:** "feeding complete should be with the rest of the feeding" — every document now flows to where it belongs by topic, not by old numbered prefix.

## What changed

**Before:** Numbered folders (`00_pre_system`, `01_master`, `02_education`, `03_operations`, `04_deployment`, `05_business`, `06_governance`, `07_source_documents`, `08_build`) — `SM_01_Feeding_Complete.pdf` lived in `04_deployment/complete_manuals/` while diet verification, feeding addendums, food retail model, and zero waste docs were scattered across four other folders.

**After:** Topical folders. Feeding documents — every single one of them — live under `feeding/`. Same pattern for operations, guest experience, education, business, governance, and master.

## New top-level structure

```
LIFE-system/
├── STAFF_FIRST/         day-one staff reading
├── master/              LIFE_SYSTEM_MASTER (canonical) + alpha-omega audit
├── feeding/             ★ all feeding/diet/zero-waste in one place
│   ├── GOLD_STANDARD_DIET_RULE.md
│   ├── manuals/           SM_01_Feeding_Complete.pdf
│   ├── quick_reference/   QR_02_Feeding_Protocol.pdf
│   ├── signs/             SIGN_Diet_Verification.pdf
│   ├── staff_extract/     part07_feeding_addendums.md, part08_diet_verification.md
│   ├── zero_waste/        ZERO_WASTE_FOOD_LOOP.md, QR_04_Zero_Waste.pdf, part06
│   ├── business/          FOOD_RETAIL_OPERATOR_MODEL.pdf
│   └── source_addendums/  Exhibit_Feeding_Addendum_Batch{1,2,3}.pdf
├── operations/          SOPs, checklists, top-ten, do-not, cleaning, packets
├── guest_experience/    guest-facing manuals, signs, mirror mirror
├── education/           LIFE education spine, narration arc, digital totems, QR codes
├── business/            legal, calendar, branding, venue, promoter packet
├── governance/          locked phrases, terminology, AI governance, decisions
├── by_species/          per-animal folders (22 species)
├── by_asset_type/       all assets grouped by type
├── narration_suites/    20 suite totems + rental info
├── templates/           sign, SOP, species
├── source_documents/    original exports
├── build/               build scripts
└── releases/            versioned snapshots (incl. this one)
```

## Move map — feeding consolidation

| From | To |
|---|---|
| `04_deployment/complete_manuals/SM_01_Feeding_Complete.pdf` | `feeding/manuals/` |
| `04_deployment/quick_reference/QR_02_Feeding_Protocol.pdf` | `feeding/quick_reference/` |
| `04_deployment/quick_reference/QR_04_Zero_Waste.pdf` | `feeding/zero_waste/` |
| `04_deployment/signs/SIGN_Diet_Verification.pdf` | `feeding/signs/` |
| `03_operations/staff_extract/part07_feeding_addendums.md` | `feeding/staff_extract/` |
| `03_operations/staff_extract/part08_diet_verification.md` | `feeding/staff_extract/` |
| `03_operations/staff_extract/part06_zero_waste.md` | `feeding/zero_waste/` |
| `03_operations/ZERO_WASTE_FOOD_LOOP.md` | `feeding/zero_waste/` |
| `05_business/FOOD_RETAIL_OPERATOR_MODEL.pdf` | `feeding/business/` |
| `07_source_documents/operations/Exhibit_Feeding_Addendum_Batch{1,2,3}*.pdf` | `feeding/source_addendums/` |
| `GOLD_STANDARD_DIET_RULE.md` (root) | `feeding/` |

## Move map — operations consolidation

| From | To |
|---|---|
| `04_deployment/complete_manuals/SM_02_Operations_Complete.pdf` | `operations/manuals/` |
| `04_deployment/complete_manuals/SM_04_New_Hire_Packet.pdf` | `operations/manuals/` |
| `04_deployment/STAFF_RESET_PACKAGE.pdf` | `operations/manuals/` |
| `04_deployment/STAFF_ORIENTATION_WALKTHROUGH.pdf` | `operations/manuals/` |
| `04_deployment/quick_reference/QR_01,03,05,07.pdf` | `operations/quick_reference/` |
| `04_deployment/STAFF_QUICK_REFERENCE.pdf` | `operations/quick_reference/` |
| `04_deployment/signs/SIGN_Top_Ten_Operational.pdf, SIGN_Owners_Top_Ten_Reduced.pdf, SIGN_Back_Room_Authorization.pdf, SIGNS_INSTRUCTIONAL.pdf` | `operations/signs/` |
| `03_operations/CHECKLISTS_OPENING/CLOSING.pdf` | `operations/checklists/` |
| `04_deployment/LIFE_Deployment_Checklist.pdf, DEPLOYMENT_CHECKLIST.pdf` | `operations/checklists/` |
| `03_operations/OPERATIONS_SOPs.md, SOCIAL_MEDIA_SOP.md` | `operations/` |
| `03_operations/staff_extract/part01,03,04,05,09,10,18,19_*.md` | `operations/staff_extract/` |
| `07_source_documents/operations/Employee_Packet, Manager_Packet, Staff_Packet, sop-startup` | `operations/source_documents/` |

## Move map — other domains

- **Guest Experience:** SM_03, QR_06, top-ten guest-facing, wayfinding, pricing, Mirror Mirror, part02 → `guest_experience/`
- **Education:** LIFE_EDUCATION_SPINE, Narration_Suites_Complete_Arc, QR_NARRATION_SUITES, STUDENT_TOTEMS_ALL_SPECIES, digital_totems/, qr_codes/, part11, education source documents → `education/`
- **Business:** BUSINESS_SYSTEMS, STUDIO_GIRAFFE_*, COURT_UTILIZATION, JOE_HAND, PICKLEBALL, branding, land lease → `business/`
- **Governance:** AI_GOVERNANCE, DECISIONS, DOCUMENT_CATALOG, SYSTEM_EVALUATION, TERMINOLOGY, LOCKED_PHRASES, ALPHA_OMEGA_AUDIT_FIXES → `governance/`
- **Master:** LIFE_SYSTEM_MASTER.md/.pdf, alpha_omega_audit.md, Unified_System_Compression.pdf → `master/`
- **Build:** build_master_pdf.py, build_staff_pdfs.py → `build/`
- **Source documents:** LIFE-TEAM-MESSAGE-CANONICAL, LIFE-steward-export, ChatGPT thread → `source_documents/`

## Cleanup

- Removed empty old numbered folders: `00_pre_system/`, `01_master/`, `02_education/`, `03_operations/`, `04_deployment/`, `05_business/`, `06_governance/`, `07_source_documents/`, `08_build/`, `locked_phrases/`
- Merged `species/<sp>.md` into `by_species/<sp>/species_notes.md`
- Removed duplicate `LIFE_system/digital_totems/` (identical to `education/digital_totems/`)
- Reconciled the two `LIFE_SYSTEM_MASTER.md` files — kept the newer one (root, 3283 lines, Apr 26 21:31), dropped the older (master/, 7044 lines, Apr 26 02:45)

## What did NOT change

- `by_species/`, `by_asset_type/`, `narration_suites/`, `STAFF_FIRST/`, `releases/` — unchanged from v2026-04-28d
- All 40 totems built in v2026-04-28d are still in their by_species and by_asset_type homes
- All locked rules, locked phrases, and the brown palette are unchanged
- All 22 diet cards remain in both `by_species/<sp>/` and `by_asset_type/diet_cards/`

## Verification

After this commit:
- `feeding/` contains 12 files across 7 subfolders — every feeding document in the repo
- `operations/` contains all SOPs, checklists, top-ten, do-not, cleaning, packets
- `master/` contains the single canonical LIFE_SYSTEM_MASTER (md + pdf)
- Zero feeding documents remain outside `feeding/` (confirmed by grep)
