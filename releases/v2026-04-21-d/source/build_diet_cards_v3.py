#!/usr/bin/env python3
"""LIFE Gold Standard Diet Card Builder.

Source template: DIETS-steward-export.txt PART 4 — Gold Standard Diet Posters.
Content: LIFE_diet_content_18.json.
Food photos: LIFE_system/food_photos/
Species photos: LIFE_system/species_photos/
"""
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

WS = Path("/home/user/workspace")
FOOD = WS / "LIFE_system" / "food_photos"
SPECIES = WS / "LIFE_system" / "species_photos"
OUT_DIR = WS / "LIFE_system" / "diet_cards"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Colors
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
LIGHT = HexColor("#F5F5F2")
RULE = HexColor("#D4D1CA")
GREEN_BG = HexColor("#E9F2E3")
GREEN_INK = HexColor("#2C5020")
RED_BG = HexColor("#F8E3E3")
RED_INK = HexColor("#8A1C1C")
NAVY = HexColor("#2C3481")
AMBER_BG = HexColor("#FFF4D6")     # scope/exclusion note band
AMBER_INK = HexColor("#6B4A00")
AMBER_BORDER = HexColor("#E0B94A")

# Fonts
FONT_DIR = Path("/tmp/fonts")
for name, path in {
    "DMSans-Bold": FONT_DIR / "DMSans-Bold.ttf",
    "DMSans-SemiBold": FONT_DIR / "DMSans-SemiBold.ttf",
    "Inter-Regular": FONT_DIR / "Inter-Regular.ttf",
    "Inter-Bold": FONT_DIR / "Inter-Bold.ttf",
    "Inter-SemiBold": FONT_DIR / "Inter-SemiBold.ttf",
}.items():
    if path.exists():
        pdfmetrics.registerFont(TTFont(name, str(path)))

BODY = "Inter-Regular"
BODY_SEMI = "Inter-SemiBold"
BODY_BOLD = "Inter-Bold"
DISPLAY = "DMSans-Bold"

SPECIES_SLUG = {
    "capybara": "capybara",
    "rabbit": "rabbit",
    "patagonian_mara": "patagonian_mara",
    "wallaby": "wallaby",
    "alpaca": "alpaca",
    "two_toed_sloth": "two_toed_sloth",
    "monkey_tailed_skink": "monkey_tailed_skink",
    "spider_monkey": "spider_monkey",
    "red_ruffed_lemur": "red_ruffed_lemur",
    "black_and_white_ruffed_lemur": "black_and_white_ruffed_lemur",
    "toco_toucan": "toco_toucan",
    "kinkajou": "kinkajou",
    "argentine_tegu": "tegu",
    "nine_banded_armadillo": "armadillo",
    "prehensile_tailed_porcupine": "porcupine",
    "ring_tailed_lemur": "ring_tailed_lemur",
    "sulcata_tortoise": "sulcata_tortoise",
    "sailfin_dragon": "sailfin_dragon",
}

PAGE_W, PAGE_H = letter
MARGIN = 0.5 * 72

FOOD_LABELS = {
    "timothy_hay": "Timothy hay",
    "grass_hay": "Grass hay",
    "kale": "Kale",
    "collard_greens": "Collard greens",
    "romaine": "Romaine",
    "dandelion_greens": "Dandelion greens",
    "mulberry_leaves": "Mulberry leaves",
    "browse_branches": "Browse branches",
    "mango": "Mango",
    "papaya": "Papaya",
    "berries": "Berries",
    "melon": "Melon",
    "banana": "Banana",
    "apple": "Apple",
    "sweet_potato_yam": "Sweet potato / yam",
    "carrot": "Carrot",
    "zucchini": "Zucchini",
    "squash": "Squash",
    "herbivore_pellets": "Herbivore pellets",
    "primate_chow": "Primate chow",
    "insect_diet": "Insectivore diet",
    "crickets": "Crickets",
    "mealworms": "Mealworms",
    "cooked_egg": "Cooked egg",
    "raw_meat_ground": "Ground meat",
    "softbill_chow": "Low-iron softbill chow",
    "leafy_greens_mix": "Leafy greens",
    "orange": "Orange",
    "corn": "Corn",
    "peas": "Peas",
}


def draw_image_box(c, path, x, y, w, h, fill_bg=None):
    if fill_bg:
        c.setFillColor(fill_bg)
        c.rect(x, y, w, h, stroke=0, fill=1)
        c.setFillColor(INK)
    if not path.exists():
        c.setStrokeColor(RULE)
        c.rect(x, y, w, h, stroke=1, fill=0)
        c.setFont(BODY, 7)
        c.setFillColor(MUTED)
        c.drawCentredString(x + w / 2, y + h / 2, "[photo]")
        c.setFillColor(INK)
        return
    try:
        img = ImageReader(str(path))
        iw, ih = img.getSize()
        ar = iw / ih
        box_ar = w / h
        if ar > box_ar:
            draw_w = w
            draw_h = w / ar
            dx = 0
            dy = (h - draw_h) / 2
        else:
            draw_h = h
            draw_w = h * ar
            dx = (w - draw_w) / 2
            dy = 0
        c.drawImage(img, x + dx, y + dy, width=draw_w, height=draw_h,
                    preserveAspectRatio=True, mask="auto")
        c.setStrokeColor(RULE)
        c.setLineWidth(0.4)
        c.rect(x, y, w, h, stroke=1, fill=0)
    except Exception as e:
        print(f"  img err {path}: {e}")


def food_grid(c, x, y_top, w, food_slugs, tint_bg, label_prefix=""):
    """Draw a grid of food photos with labels. Returns the bottom y."""
    n = len(food_slugs)
    if n == 0:
        return y_top
    cols = min(4, n)
    rows = (n + cols - 1) // cols
    cell_w = (w - (cols - 1) * 6) / cols
    # Tighter photo aspect to fit scope note without overflow
    photo_h = cell_w * 0.60
    label_h = 16
    cell_h = photo_h + label_h + 2
    for i, slug in enumerate(food_slugs):
        r = i // cols
        col = i % cols
        cx = x + col * (cell_w + 6)
        cy = y_top - r * (cell_h + 6) - photo_h
        path = FOOD / f"{slug}.jpg"
        draw_image_box(c, path, cx, cy, cell_w, photo_h, fill_bg=LIGHT)
        # Label below
        c.setFont(BODY_SEMI, 8)
        c.setFillColor(INK)
        label = FOOD_LABELS.get(slug, slug.replace("_", " ").title())
        # wrap if too long
        max_chars = int(cell_w / 4)
        if len(label) > max_chars:
            words = label.split()
            line1, line2 = [], []
            cur = 0
            for wd in words:
                if cur + len(wd) + 1 <= max_chars:
                    line1.append(wd)
                    cur += len(wd) + 1
                else:
                    line2.append(wd)
            c.drawCentredString(cx + cell_w / 2, cy - 8, " ".join(line1))
            c.drawCentredString(cx + cell_w / 2, cy - 16, " ".join(line2))
        else:
            c.drawCentredString(cx + cell_w / 2, cy - 10, label)
    return y_top - rows * (cell_h + 6) - 4


def build_card(sp, out_path):
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Diet Card — {sp['common_name'].title()}")
    c.setAuthor("Perplexity Computer")

    content_w = PAGE_W - 2 * MARGIN

    # Top band — species photo left, title block right
    y = PAGE_H - MARGIN
    photo_slug = SPECIES_SLUG.get(sp["slug"], sp["slug"])
    photo_path = SPECIES / f"{photo_slug}.jpg"
    hero_w = 2.2 * 72
    hero_h = 1.6 * 72
    draw_image_box(c, photo_path, MARGIN, y - hero_h, hero_w, hero_h, fill_bg=LIGHT)

    # Title block to the right
    tx = MARGIN + hero_w + 14
    tw = content_w - hero_w - 14
    # Title
    c.setFont(DISPLAY, 22)
    c.setFillColor(INK)
    c.drawString(tx, y - 22, sp["common_name"])
    # subtitle — GOLD STANDARD DIET
    c.setFont(BODY_SEMI, 10)
    c.setFillColor(NAVY)
    c.drawString(tx, y - 38, f"{sp['category']}")
    # What this animal is
    c.setFont(BODY, 10)
    c.setFillColor(INK)
    c.drawString(tx, y - 54, f"WHAT THIS ANIMAL IS: {sp['what_this_animal_is']}")

    # 3-second check — prominent
    check_y = y - 82
    c.setFillColor(NAVY)
    c.rect(tx, check_y, tw, 26, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(DISPLAY, 11)
    c.drawString(tx + 10, check_y + 14, "3-SECOND CHECK")
    c.setFont(BODY_SEMI, 12)
    c.drawString(tx + 135, check_y + 10, sp["three_second_check"])
    c.setFillColor(INK)

    # Move below hero
    y = y - hero_h - 14

    # === SCOPE / EXCLUSION NOTE ===
    # Highest-visibility callout: this diet applies to healthy animals only.
    # Covers ~95% of feedings; sick / vet-care / special-diet animals are
    # excluded and fall to trained staff judgment within sound science.
    note_h = 50
    c.setFillColor(AMBER_BG)
    c.setStrokeColor(AMBER_BORDER)
    c.setLineWidth(0.8)
    c.rect(MARGIN, y - note_h, content_w, note_h, stroke=1, fill=1)
    # Header row
    c.setFillColor(AMBER_INK)
    c.setFont(DISPLAY, 10.5)
    c.drawString(MARGIN + 10, y - 14, "STANDARD DIET \u2014 HEALTHY ANIMALS ONLY")
    # Scope line (right-justified)
    c.setFont(BODY_SEMI, 8.5)
    c.drawRightString(MARGIN + content_w - 10, y - 14,
                      "Excludes sick, vet-care, or special-diet animals")
    # Body paragraph (wrapped) + Pause/Ask/Escalate line
    note_body = (
        'This card covers about <b>95%</b> of daily feedings. For the remaining 5%, '
        'use your training and observation to adjust within sound science. '
        '<font color="#6B4A00"><b>When unsure \u2014 Pause. Ask. Escalate.</b></font>'
    )
    note_style = ParagraphStyle(
        "note_body", fontName=BODY, fontSize=8.5, leading=11,
        textColor=INK,
    )
    p = Paragraph(note_body, note_style)
    p.wrap(content_w - 20, note_h - 22)
    p.drawOn(c, MARGIN + 10, y - note_h + 6)
    c.setFillColor(INK)
    y -= note_h + 10

    # === CORRECT section ===
    # green band
    band_h = 22
    c.setFillColor(GREEN_BG)
    c.rect(MARGIN, y - band_h, content_w, band_h, stroke=0, fill=1)
    c.setFillColor(GREEN_INK)
    c.setFont(DISPLAY, 13)
    c.drawString(MARGIN + 10, y - 15, "CORRECT")
    c.setFont(BODY_SEMI, 10)
    correct_text = " · ".join(sp["correct"])
    c.drawString(MARGIN + 95, y - 14, correct_text)
    c.setFillColor(INK)
    y -= band_h + 8

    # food grid — correct
    y = food_grid(c, MARGIN, y, content_w, sp["correct_foods"], GREEN_BG)
    y -= 6

    # === WRONG section ===
    c.setFillColor(RED_BG)
    c.rect(MARGIN, y - band_h, content_w, band_h, stroke=0, fill=1)
    c.setFillColor(RED_INK)
    c.setFont(DISPLAY, 13)
    c.drawString(MARGIN + 10, y - 15, "WRONG — FIX IMMEDIATELY")
    c.setFont(BODY_SEMI, 10)
    wrong_text = " · ".join(sp["wrong"])
    c.drawString(MARGIN + 210, y - 14, wrong_text)
    c.setFillColor(INK)
    y -= band_h + 8

    y = food_grid(c, MARGIN, y, content_w, sp["wrong_foods"], RED_BG)
    y -= 6

    # === SIMPLE BUILD + PREP RULE row ===
    half = (content_w - 10) / 2
    box_h = 56
    # Simple build (left)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.rect(MARGIN, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(DISPLAY, 10)
    c.setFillColor(NAVY)
    c.drawString(MARGIN + 8, y - 14, "SIMPLE BUILD")
    c.setFillColor(INK)
    c.setFont(BODY, 9)
    for i, line in enumerate(sp["simple_build"]):
        c.drawString(MARGIN + 8, y - 28 - i * 11, "• " + line)

    # Prep rule (right)
    rx = MARGIN + half + 10
    c.rect(rx, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(DISPLAY, 10)
    c.setFillColor(NAVY)
    c.drawString(rx + 8, y - 14, "PREP RULE")
    c.setFillColor(INK)
    c.setFont(BODY, 10)
    # Wrap prep rule
    pr = sp["prep_rule"]
    style = ParagraphStyle("pr", fontName=BODY, fontSize=10, leading=12, textColor=INK)
    p = Paragraph(pr, style)
    ph = p.wrap(half - 16, box_h - 22)[1]
    p.drawOn(c, rx + 8, y - 22 - ph)

    y -= box_h + 10

    # Enforcement line
    c.setFillColor(NAVY)
    c.setFont(DISPLAY, 11)
    c.drawCentredString(PAGE_W / 2, y - 10, "MATCH THE BOWL — DO NOT INTERPRET.")
    c.setFont(BODY, 9)
    c.setFillColor(MUTED)
    y -= 22
    c.drawCentredString(PAGE_W / 2, y, "No photo = feeding not complete.  ·  No substitutions without approval.  ·  Unsure → Pause → Ask → Escalate.")

    # Source footer (two lines to avoid overlap)
    c.setFont(BODY, 7)
    c.setFillColor(MUTED)
    src_label = "Verbatim Gold Standard" if sp.get("verbatim") else "Body-text extraction"
    src_line = f"Source: {sp['source_line']}  ·  {src_label}"
    # Truncate if too long
    max_chars = 110
    if len(src_line) > max_chars:
        src_line = src_line[:max_chars - 1] + "…"
    c.drawString(MARGIN, 0.45 * 72, src_line)
    c.drawString(MARGIN, 0.32 * 72, "LIFE Diet Governance System  ·  Match the bowl. Don't interpret.")
    c.setFillColor(INK)

    c.save()


def main():
    data = json.loads((WS / "LIFE_diet_content_18.json").read_text())
    built = []
    for sp in data["species"]:
        out = OUT_DIR / f"DietCard_{sp['slug']}.pdf"
        build_card(sp, out)
        built.append(out)
        print(f"✓ {sp['common_name']}  → {out.name}")
    print(f"\nBuilt {len(built)} diet cards in {OUT_DIR}")


if __name__ == "__main__":
    main()
