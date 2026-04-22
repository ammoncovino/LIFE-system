# LIFE Totems — Release v2026.04.21-d

**Status:** LOCKED · one visual language across all 19 species
**Owner:** Family Fun Group
**Released:** April 22, 2026

This release is the deployable set of 19 park totems. Every sign speaks the same visual and verbal language. Do not modify wording, add or remove sections, or change formatting. If content needs to change, the source files in `source/` and `content/` get edited and the set is re-rendered — never edit a PDF directly.

---

## What's in this release

| Folder / file | What it is |
| --- | --- |
| `LIFE_Totems_Master_Binder_v2026-04-21-d.pdf` | All 19 totems combined into one print-ready PDF |
| `totems/` | Each species as its own PDF (19 files) |
| `source/` | The builder + content source files — edit these, re-render |
| `content/LIFE_k5_locked/` | The canonical 8-question K-5 answer JSON per species |

---

## The 19 totems

**18 animal species (with photos):**
alpaca · argentine tegu · bennett's wallaby · black and white ruffed lemur · capybara · geoffroy's spider monkey · kinkajou · linne's two-toed sloth · monkey-tailed skink · nine-banded armadillo · patagonian mara · prehensile-tailed porcupine · rabbit · red ruffed lemur · ring-tailed lemur · sailfin dragon · sulcata tortoise · toco toucan

**1 mirror totem:**
homo sapiens — the photo region is a cutout for a real acrylic mirror (see fabrication note below)

---

## Required elements on every sign (LOCKED)

1. Title + scientific name at the top
2. The 8-question spine, numbered 1.–8., rust-accented numbers, order unchanged, K-5 answers
3. "WHY IS THIS ANIMAL HERE?" panel (Reality Door) — opening line, 2 habitat lines, exactly 3 shrink bullets, bridge line
4. "THINK ABOUT THIS" reflection question in italic
5. Footer: *"What a living thing can sense becomes its reality. Environment shapes design."*
6. QR chip bottom-right with caption **"SCAN TO LEARN MORE"**

If any sign is missing one of these, it is not deployable. Reprint from the PDF.

---

## Homo sapiens mirror — fabrication note

The photo region is a cutout. Cut along the crop marks printed inside the panel and mount an acrylic mirror flush to the frame.

- Mirror size: **4.20 in wide × 6.52 in tall**
- Material: **1/8 in acrylic mirror**, rounded corners
- Mount flush behind the gold hairline rect

The printed placeholder says "YOU ARE LOOKING AT ONE" — that text gets removed when the mirror goes in. The 8 answers stay in third-person "it" on purpose so the mirror does the personalizing.

---

## How to re-render the totems (for the builder only)

```bash
cd source/
python build_totem_v3.py
```

Reads `content/LIFE_k5_locked/*.json` + `reality_doors.py` + `think_about_this.py` + species photos → writes 19 `TOTEM_{slug}.pdf` files.

Fonts required at `/tmp/fonts/`: Cinzel, Inter-Regular, Inter-Bold, CormorantGaramond-Italic.
Photos required in the working directory: `photo_{slug}.png` for every species except `homo-sapiens` (that one uses the mirror panel).

---

## Changelog vs v2026.04.21-c

- Reality Door standardized across all 19 species (opening + 2 habitat lines + exactly 3 shrink bullets + bridge line)
- RD header renamed to guest-facing **"WHY IS THIS ANIMAL HERE?"**
- 8-Q headings numbered 1.–8. in rust accent (consistent across every sign)
- QR caption standardized to **"SCAN TO LEARN MORE"** (no per-species variants)
- QR chip widened and caption repadded so "SCAN TO LEARN MORE" no longer clips or crowds the chip edge
- Homo sapiens photo replaced with mirror cutout + fabrication spec
- `homo-sapiens.json` K-5 content added with scientific name
- One reflection question per species in `think_about_this.py`
