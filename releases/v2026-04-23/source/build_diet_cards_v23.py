#!/usr/bin/env python3
"""LIFE v2026.04.23 Diet Card Builder.

Changes from v3:
- Adds MORNING FEED + ENCOUNTER PORTION framing band (between title and CORRECT)
- Adds approximate daily weight
- Shows scientific name under common name
- Historical species (no sites) render "[HISTORICAL — NO CURRENT SITE]" badge
"""
import json
import re
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
SPECIES_PHOTOS = WS / "LIFE_system" / "species_photos"
OUT_DIR = WS / "LIFE_v2026-04-23" / "diet_cards"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")
LIGHT = HexColor("#F5F5F2")
RULE = HexColor("#D4D1CA")
GREEN_BG = HexColor("#E9F2E3")
GREEN_INK = HexColor("#2C5020")
RED_BG = HexColor("#F8E3E3")
RED_INK = HexColor("#8A1C1C")
NAVY = HexColor("#2C3481")
AMBER_BG = HexColor("#FFF4D6")
AMBER_INK = HexColor("#6B4A00")
AMBER_BORDER = HexColor("#E0B94A")
# Framing band: morning-feed + encounter
BAND_BG = HexColor("#EEF2F7")        # cool slate
BAND_INK = HexColor("#233044")
BAND_BORDER = HexColor("#A9B6C6")
ENC_INK = HexColor("#7A3416")        # rust (encounter sub-accent)
HIST_BG = HexColor("#EDEDED")
HIST_INK = HexColor("#555555")

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

# Map slug -> photo filename (existing library uses shorter filenames)
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
    # new — no photos yet; renderer falls back to placeholder
}

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
    "pear": "Pear",
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

PAGE_W, PAGE_H = letter
MARGIN = 0.5 * 72


def safe_slug(s: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


def draw_image_box(c, path, x, y, w, h, fill_bg=None):
    if fill_bg:
        c.setFillColor(fill_bg)
        c.rect(x, y, w, h, stroke=0, fill=1)
        c.setFillColor(INK)
    if not path or not path.exists():
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


def food_grid(c, x, y_top, w, food_slugs, tint_bg, compact=False):
    n = len(food_slugs)
    if n == 0:
        return y_top
    # If >4 items, switch to 5 cols to stay on 1 row when possible
    cols = 5 if n > 4 and n <= 5 else min(4, n)
    if n > 5:
        # 4 cols, possibly 2 rows
        cols = 4
    rows = (n + cols - 1) // cols
    cell_w = (w - (cols - 1) * 6) / cols
    # Squeeze photo height when we're in a dense card
    ratio = 0.48 if compact else 0.58
    photo_h = cell_w * ratio
    label_h = 14 if compact else 16
    cell_h = photo_h + label_h + 2
    for i, slug in enumerate(food_slugs):
        r = i // cols
        col = i % cols
        cx = x + col * (cell_w + 6)
        cy = y_top - r * (cell_h + 6) - photo_h
        path = FOOD / f"{slug}.jpg"
        draw_image_box(c, path, cx, cy, cell_w, photo_h, fill_bg=LIGHT)
        c.setFont(BODY_SEMI, 8)
        c.setFillColor(INK)
        label = FOOD_LABELS.get(slug, slug.replace("_", " ").title())
        max_chars = int(cell_w / 4)
        if len(label) > max_chars:
            words = label.split()
            line1, line2 = [], []
            cur = 0
            for wd in words:
                if cur + len(wd) + 1 <= max_chars:
                    line1.append(wd); cur += len(wd) + 1
                else:
                    line2.append(wd)
            c.drawCentredString(cx + cell_w / 2, cy - 8, " ".join(line1))
            c.drawCentredString(cx + cell_w / 2, cy - 16, " ".join(line2))
        else:
            c.drawCentredString(cx + cell_w / 2, cy - 10, label)
    return y_top - rows * (cell_h + 6) - 4


def draw_paragraph(c, text, x, y_top, w, font=BODY, size=9, leading=11, color=INK):
    style = ParagraphStyle("_p", fontName=font, fontSize=size, leading=leading, textColor=color)
    p = Paragraph(text, style)
    _, h = p.wrap(w, 200)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def build_card(sp, out_path):
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Diet Card — {sp['common_name'].title()}")
    c.setAuthor("Perplexity Computer")

    content_w = PAGE_W - 2 * MARGIN
    historical = not sp.get("sites")

    # ======= TOP BAND: photo left, title block right =======
    y = PAGE_H - MARGIN
    photo_slug = SPECIES_SLUG.get(sp["slug"], sp["slug"])
    photo_path = SPECIES_PHOTOS / f"{photo_slug}.jpg"
    hero_w = 2.1 * 72
    hero_h = 1.5 * 72
    draw_image_box(c, photo_path, MARGIN, y - hero_h, hero_w, hero_h, fill_bg=LIGHT)

    tx = MARGIN + hero_w + 12
    tw = content_w - hero_w - 12
    # Auto-fit title to column width
    title = sp["common_name"]
    title_font = DISPLAY
    title_size = 20
    while title_size > 11 and c.stringWidth(title, title_font, title_size) > tw - 4:
        title_size -= 0.5
    c.setFont(title_font, title_size)
    c.setFillColor(INK)
    c.drawString(tx, y - 20, title)

    # Scientific name
    sci = sp.get("scientific_name", "")
    if sci:
        c.setFont(BODY, 9)
        c.setFillColor(MUTED)
        c.drawString(tx, y - 33, sci)

    # Historical badge (right of scientific)
    if historical:
        c.setFillColor(HIST_BG)
        c.setStrokeColor(HIST_INK)
        c.setLineWidth(0.5)
        badge_w = 155; badge_h = 14
        c.rect(tx + tw - badge_w, y - 14 - 2, badge_w, badge_h, stroke=1, fill=1)
        c.setFillColor(HIST_INK)
        c.setFont(DISPLAY, 8)
        c.drawCentredString(tx + tw - badge_w/2, y - 14 + 1, "HISTORICAL — NO CURRENT SITE")

    # Category
    c.setFont(BODY_SEMI, 10)
    c.setFillColor(NAVY)
    c.drawString(tx, y - 48, sp["category"])

    # What this animal is
    c.setFont(BODY, 9)
    c.setFillColor(INK)
    c.drawString(tx, y - 62, f"WHAT THIS ANIMAL IS: {sp['what_this_animal_is']}")

    # Sites list
    sites = sp.get("sites", [])
    if sites:
        c.setFont(BODY_SEMI, 8)
        c.setFillColor(MUTED)
        c.drawString(tx, y - 74, f"SITES: {' · '.join(sites)}")

    # 3-second check — pushed down below sites line
    check_y = y - 103
    c.setFillColor(NAVY)
    c.rect(tx, check_y, tw, 22, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(DISPLAY, 9.5)
    c.drawString(tx + 8, check_y + 12, "3-SEC CHECK")
    c.setFont(BODY_SEMI, 9.5)
    # Truncate if too long for the band
    check_text = sp["three_second_check"]
    if len(check_text) > 54:
        check_text = check_text[:53] + "…"
    c.drawString(tx + 78, check_y + 8, check_text)
    c.setFillColor(INK)

    y = y - hero_h - 10

    # ======= SCOPE / EXCLUSION NOTE =======
    note_h = 42
    c.setFillColor(AMBER_BG)
    c.setStrokeColor(AMBER_BORDER)
    c.setLineWidth(0.8)
    c.rect(MARGIN, y - note_h, content_w, note_h, stroke=1, fill=1)
    c.setFillColor(AMBER_INK)
    c.setFont(DISPLAY, 10)
    c.drawString(MARGIN + 10, y - 13, "STANDARD DIET — HEALTHY ANIMALS ONLY")
    c.setFont(BODY_SEMI, 8)
    c.drawRightString(MARGIN + content_w - 10, y - 13,
                      "Excludes sick / vet-care / special-diet animals")
    note_body = (
        'Covers <b>~95%</b> of daily feedings. For the remaining 5%, '
        'use training and observation within sound science. '
        '<font color="#6B4A00"><b>Unsure — Pause. Ask. Escalate.</b></font>'
    )
    draw_paragraph(c, note_body, MARGIN + 10, y - 18, content_w - 20, font=BODY, size=8, leading=10, color=INK)
    y -= note_h + 8

    # ======= FRAMING BAND: MORNING + ENCOUNTER =======
    # v23 band answering Mia's question about encounters vs morning feed.
    band_h = 78
    c.setFillColor(BAND_BG)
    c.setStrokeColor(BAND_BORDER)
    c.setLineWidth(0.7)
    c.rect(MARGIN, y - band_h, content_w, band_h, stroke=1, fill=1)
    # Two columns
    col_w = (content_w - 16) / 2
    text_top = y - 14
    text_bottom_reserve = 14  # reserve for daily weight line
    avail_h = band_h - 18 - text_bottom_reserve
    # Morning feed (left)
    c.setFillColor(BAND_INK)
    c.setFont(DISPLAY, 9.5)
    c.drawString(MARGIN + 10, text_top, "MORNING FEED-OUT")
    c.setFont(BODY, 8.5)
    c.setFillColor(INK)
    mf = sp.get("morning_feed", "Per posted SOP.")
    mf_style = ParagraphStyle("_mf", fontName=BODY, fontSize=8.5, leading=10.5, textColor=INK)
    mp = Paragraph(mf, mf_style)
    mp_w, mp_h = mp.wrap(col_w - 8, avail_h)
    mp.drawOn(c, MARGIN + 10, text_top - 4 - mp_h)
    # Vertical divider
    c.setStrokeColor(BAND_BORDER)
    c.setLineWidth(0.5)
    c.line(MARGIN + col_w + 8, y - 4, MARGIN + col_w + 8, y - band_h + 4)
    # Encounter portion (right)
    c.setFillColor(ENC_INK)
    c.setFont(DISPLAY, 9.5)
    c.drawString(MARGIN + col_w + 16, text_top, "ENCOUNTER / ENRICHMENT PORTION")
    c.setFont(BODY, 8.5)
    c.setFillColor(INK)
    ep = sp.get("encounter_portion", "Drawn from daily allocation.")
    ep_style = ParagraphStyle("_ep", fontName=BODY, fontSize=8.5, leading=10.5, textColor=INK)
    epp = Paragraph(ep, ep_style)
    _, ep_h = epp.wrap(col_w - 10, avail_h)
    epp.drawOn(c, MARGIN + col_w + 16, text_top - 4 - ep_h)
    # Daily weight — bottom-right within band, on its own line
    dw = sp.get("daily_weight", "")
    if dw:
        c.setFont(BODY_SEMI, 7.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 10, y - band_h + 5, f"APPROX DAILY: {dw}")
    y -= band_h + 8

    # ======= CORRECT =======
    band_h_cw = 20
    c.setFillColor(GREEN_BG)
    c.rect(MARGIN, y - band_h_cw, content_w, band_h_cw, stroke=0, fill=1)
    c.setFillColor(GREEN_INK)
    c.setFont(DISPLAY, 12)
    c.drawString(MARGIN + 10, y - 14, "CORRECT")
    c.setFont(BODY_SEMI, 9.5)
    c.drawString(MARGIN + 90, y - 13, " · ".join(sp["correct"]))
    c.setFillColor(INK)
    y -= band_h_cw + 6
    # Detect dense card (many wrong_foods or many correct_foods -> compact mode)
    is_dense = len(sp["correct_foods"]) + len(sp["wrong_foods"]) > 9
    y = food_grid(c, MARGIN, y, content_w, sp["correct_foods"], GREEN_BG, compact=is_dense)
    y -= 4

    # ======= WRONG =======
    c.setFillColor(RED_BG)
    c.rect(MARGIN, y - band_h_cw, content_w, band_h_cw, stroke=0, fill=1)
    c.setFillColor(RED_INK)
    c.setFont(DISPLAY, 12)
    c.drawString(MARGIN + 10, y - 14, "WRONG — FIX IMMEDIATELY")
    c.setFont(BODY_SEMI, 9.5)
    c.drawString(MARGIN + 210, y - 13, " · ".join(sp["wrong"]))
    c.setFillColor(INK)
    y -= band_h_cw + 6
    y = food_grid(c, MARGIN, y, content_w, sp["wrong_foods"], RED_BG, compact=is_dense)
    y -= 4

    # ======= SIMPLE BUILD + PREP RULE row =======
    # Size based on content — prep rule tends to be the long one
    half = (content_w - 10) / 2
    # Compute needed heights
    sb_lines = len(sp["simple_build"])
    sb_needed = 20 + sb_lines * 10 + 6
    pr_style = ParagraphStyle("_pr", fontName=BODY, fontSize=8.5, leading=10.5, textColor=INK)
    prp = Paragraph(sp["prep_rule"], pr_style)
    _, pr_h = prp.wrap(half - 16, 200)
    pr_needed = 20 + pr_h + 8
    box_h = max(54, sb_needed, pr_needed)
    c.setStrokeColor(RULE); c.setLineWidth(0.6)
    c.rect(MARGIN, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(DISPLAY, 9.5)
    c.setFillColor(NAVY)
    c.drawString(MARGIN + 8, y - 13, "SIMPLE BUILD")
    c.setFillColor(INK)
    c.setFont(BODY, 8.5)
    for i, line in enumerate(sp["simple_build"]):
        c.drawString(MARGIN + 8, y - 26 - i * 10, "• " + line)

    rx = MARGIN + half + 10
    c.rect(rx, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(DISPLAY, 9.5)
    c.setFillColor(NAVY)
    c.drawString(rx + 8, y - 13, "PREP RULE")
    c.setFillColor(INK)
    prp.drawOn(c, rx + 8, y - 17 - pr_h)
    y -= box_h + 8

    # ======= Enforcement =======
    # Skip if we'd collide with footer (below ~0.55in)
    min_y_for_enforce = 0.85 * 72
    if y > min_y_for_enforce + 20:
        c.setFillColor(NAVY)
        c.setFont(DISPLAY, 10.5)
        c.drawCentredString(PAGE_W / 2, y - 10, "MATCH THE BOWL — DO NOT INTERPRET.")
        c.setFont(BODY, 8)
        c.setFillColor(MUTED)
        y -= 20
        if y > min_y_for_enforce:
            c.drawCentredString(PAGE_W / 2, y,
                "No photo = feeding not complete.  ·  No substitutions without approval.  ·  Unsure → Pause → Ask → Escalate.")

    # Footer (always at bottom)
    c.setFont(BODY, 6.5)
    c.setFillColor(MUTED)
    src_label = "Verbatim Gold Standard" if sp.get("verbatim") else "Body-text extraction"
    src_line = f"Source: {sp['source_line']}  ·  {src_label}"
    if len(src_line) > 140:
        src_line = src_line[:139] + "…"
    c.drawString(MARGIN, 0.42 * 72, src_line)
    c.drawString(MARGIN, 0.30 * 72,
        "LIFE Diet Governance System  ·  v2026.04.23  ·  Match the bowl. Don't interpret.")
    c.setFillColor(INK)

    c.save()


def main():
    content_path = Path("/home/user/workspace/LIFE_v2026-04-23/content/LIFE_diet_content_v23.json")
    data = json.loads(content_path.read_text())
    built = []
    for sp in data["species"]:
        out = OUT_DIR / f"DietCard_{sp['slug']}.pdf"
        build_card(sp, out)
        built.append(out)
        tag = "HIST" if not sp.get("sites") else "LIVE"
        print(f"✓ [{tag}] {sp['common_name']} → {out.name}")
    print(f"\nBuilt {len(built)} diet cards in {OUT_DIR}")


if __name__ == "__main__":
    main()
