# Release v2026-04-28f — Three-Branch Split

**Date:** April 28, 2026
**Driver (verbatim):** "put employee files for them to read if they need it in one area, then a whole new branch as business remove joe hand legal and pickleball contract that's business and doesn't belong here, what else doesn't belong social media is business. one small section should be employee and the rest operations"

## What changed

The repo is now split into three clear branches:

| Branch | Audience | Count |
|---|---|---|
| `employee/` | Every staff member | 86 files |
| `operations/` | Owner / manager (running the system) | ~25 files |
| `business/` | Owner only (legal, marketing, Studio Giraffe) | 14 files |

## Employee branch — `employee/`

One area for everything an employee might read.

### `employee/feeding/`
- `GOLD_STANDARD_DIET_RULE.md`
- `SM_01_Feeding_Complete.pdf`
- `QR_02_Feeding_Protocol.pdf`, `QR_04_Zero_Waste.pdf`
- `SIGN_Diet_Verification.pdf`
- `ZERO_WASTE_FOOD_LOOP.md`, `part06_zero_waste.md`, `part07_feeding_addendums.md`, `part08_diet_verification.md`

### `employee/operations/`
- Manuals: `SM_02_Operations_Complete.pdf`, `SM_04_New_Hire_Packet.pdf`, `STAFF_RESET_PACKAGE.pdf`, `STAFF_ORIENTATION_WALKTHROUGH.pdf`, `Employee_Packet_V1-1.pdf`, `Staff_Packet_V1-1.pdf`
- QR/Signs: `STAFF_QUICK_REFERENCE.pdf`, `QR_01/03/05/07`, `SIGN_Top_Ten_Operational/Owners/Back_Room`, `SIGNS_INSTRUCTIONAL`
- Checklists: `CHECKLISTS_OPENING.pdf`, `CHECKLISTS_CLOSING.pdf`
- Markdown: `part01, 03, 04, 05, 09, 10, 18, 19_*.md`

### `employee/guest_experience/`
- `SM_03_Guest_Experience_Complete.pdf`, `QR_06_Guest_Interaction.pdf`
- `SIGN_Top_Ten_Guest_Facing.pdf`, `SIGNS_WAYFINDING.pdf`, `SIGNS_PRICING.pdf`
- `Mirror_Mirror_Wall_Content.md`, `part02_guest_facing_top_ten.md`

### `employee/education/`
- `LIFE_EDUCATION_SPINE.md`, `Narration_Suites_Complete_Arc.pdf`, `QR_NARRATION_SUITES.pdf`, `STUDENT_TOTEMS_ALL_SPECIES.pdf`
- `part11_education_life.md`
- `digital_totems/*.md` (19 species)
- `qr_codes/suite_01.png … suite_20.png`

## Operations branch — `operations/`

Running the system. Owner/manager-level.

- `OPERATIONS_SOPs.md`
- `master/` — `LIFE_SYSTEM_MASTER.md/.pdf`, `Unified_System_Compression.pdf`, `alpha_omega_audit.md`
- `governance/` — locked phrases, terminology, AI governance, decisions, document catalog, system evaluation, alpha-omega audit fixes
- `checklists/` — `DEPLOYMENT_CHECKLIST.pdf`, `LIFE_Deployment_Checklist.pdf` (manager-only deployment, not daily)
- `build/` — `build_master_pdf.py`, `build_staff_pdfs.py`
- `templates/` — sign, SOP, species
- `source_documents/` — Manager_Packet, sop-startup, education source PDFs, exports

## Business branch — `business/`

Owner only. Removed from anywhere employees would read.

- `BUSINESS_SYSTEMS.md`, `FOOD_RETAIL_OPERATOR_MODEL.pdf`
- `legal/` — `JOE_HAND_LEGAL_RESOLUTION.pdf`, `PICKLEBALL_CONTRACT_REVISION.pdf`
- `marketing/` — `SOCIAL_MEDIA_SOP.md`
- `outreach/` — `COURT_UTILIZATION_OUTREACH.pdf`
- `studio_giraffe/` — `STUDIO_GIRAFFE_VENUE.md`, `STUDIO_GIRAFFE_12MO_CALENDAR.pdf`, `STUDIO_GIRAFFE_PROMOTER_PACKET.pdf`
- `source_documents/` — `Branding-Guidelines-1.pdf`, `Land-LEASE-AGREEMENT_San-Antonio-Aquarium.pdf`, `feeding_addendums/Exhibit_Feeding_Addendum_Batch{1,2,3}.pdf`

## Key moves out of employee-facing areas

| File | From (was visible to staff) | To (now owner-only) |
|---|---|---|
| `JOE_HAND_LEGAL_RESOLUTION.pdf` | `business/` (mixed) | `business/legal/` |
| `PICKLEBALL_CONTRACT_REVISION.pdf` | `business/` (mixed) | `business/legal/` |
| `SOCIAL_MEDIA_SOP.md` | `operations/` | `business/marketing/` |
| `COURT_UTILIZATION_OUTREACH.pdf` | `business/` (mixed) | `business/outreach/` |
| `STUDIO_GIRAFFE_*` (3 files) | `business/` (mixed) | `business/studio_giraffe/` |
| `FOOD_RETAIL_OPERATOR_MODEL.pdf` | `feeding/business/` | `business/` |
| `Manager_Packet_V1-1.pdf` | `operations/source_documents/` | stays (manager-only) |

## Top-level structure

```
LIFE-system/
├── README.md, INDEX.md, OBSIDIAN_README.md, STAFF_FIRST/
├── employee/        ★ everything staff reads
│   ├── feeding/
│   ├── operations/
│   ├── guest_experience/
│   └── education/
├── operations/      ★ running the system (owner/manager)
│   ├── master/
│   ├── governance/
│   ├── checklists/
│   ├── build/
│   ├── templates/
│   └── source_documents/
├── business/        ★ owner-only
│   ├── legal/
│   ├── marketing/
│   ├── outreach/
│   ├── studio_giraffe/
│   └── source_documents/
├── by_species/      asset library: per-animal
├── by_asset_type/   asset library: by type
├── narration_suites/
└── releases/        versioned snapshots
```

## What did NOT change

- `by_species/`, `by_asset_type/`, `narration_suites/`, `STAFF_FIRST/`, `releases/` — unchanged from v2026-04-28e
- All locked rules, palette, footer text — unchanged
- All 22 diet cards still in `by_species/<sp>/` and `by_asset_type/diet_cards/`
- All 40 totems built in v2026-04-28d still in their by_species and by_asset_type homes

## Verification

- 0 marketing/legal/Studio Giraffe files in `employee/` (confirmed by find)
- All onboarding packets (Employee, Staff) in `employee/operations/`
- Manager_Packet remains in `operations/` (manager-only)
- 86 files in `employee/`, 14 in `business/`
