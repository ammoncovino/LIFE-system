#!/usr/bin/env python3
"""Gold Standard Verbatim Diet Poster builder — v2026-04-25.

Builds 10 print-ready Gold Standard posters for the 10 active totems missing them.
Uses the v23 diet card builder as the rendering engine and overlays:
  - "GOLD STANDARD VERBATIM DIET" header banner
  - Regulatory banner (USDA / USDA + HC / TPWD / no banner) drawn from totem manifest
  - "POST AT EXHIBIT — DO NOT REMOVE" footer line
"""
import json
import sys
from pathlib import Path

# Add v23 builder to path so we reuse its rendering primitives
V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

# Reuse the v23 builder
import build_diet_cards_v23 as v23

# Extend the species-slug photo map for new species without dedicated photos.
# We use closest-relative photos as placeholders (will be replaced when site photos arrive).
v23.SPECIES_SLUG.update({
    "keel_billed_toucan": "toco_toucan",        # close relative — Ramphastidae family
    "six_banded_armadillo": "armadillo",        # generic armadillo placeholder
    "southern_three_banded_armadillo": "armadillo",  # generic placeholder
})


def wrap_text(c, text, x, y_top, w, font, size, leading=11, color=None):
    """Render wrapped text into a box; returns height used."""
    if color is None:
        color = HexColor("#1A1A1A")
    style = ParagraphStyle("_w", fontName=font, fontSize=size, leading=leading, textColor=color)
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 999)
    p.drawOn(c, x, y_top - ph)
    return ph

WS = Path("/home/user/workspace")
GS_CONTENT = WS / "LIFE_diet_content_gs10_v2026-04-25.json"
TOTEM_MANIFEST = Path("/tmp/LIFE-push/releases/print_catalog_v2026-04-24/totem_catalog_manifest.json")
OUT_DIR = WS / "LIFE_GoldStandard_v2026-04-25"
OUT_DIR.mkdir(parents=True, exist_ok=True)
POSTER_DIR = OUT_DIR / "posters"
POSTER_DIR.mkdir(parents=True, exist_ok=True)

# Banner colors per regulatory authority
USDA_BG = HexColor("#0F3D2E")     # USDA forest green
USDA_INK = HexColor("#FFFFFF")
HC_BG = HexColor("#9C2A2A")       # Harris County crimson
HC_INK = HexColor("#FFFFFF")
TPWD_BG = HexColor("#7A5C28")     # Texas Parks earth
TPWD_INK = HexColor("#FFFFFF")
EXEMPT_BG = HexColor("#5A5A5A")
EXEMPT_INK = HexColor("#FFFFFF")

GOLD_BG = HexColor("#B8860B")     # gold standard band
GOLD_INK = HexColor("#FFFFFF")

NAVY = HexColor("#1B474D")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#555555")


def load_banner_map():
    """Return slug -> banner string."""
    manifest = json.loads(TOTEM_MANIFEST.read_text())
    target_names = {
        "Ring-Tailed Lemur": "ring_tailed_lemur",
        "Red Ruffed Lemur": "red_ruffed_lemur",
        "Black-and-White Ruffed Lemur": "black_and_white_ruffed_lemur",
        "Six-Banded Armadillo": "six_banded_armadillo",
        "Southern Three-Banded Armadillo": "southern_three_banded_armadillo",
        "Alpaca": "alpaca",
        "Keel-Billed Toucan": "keel_billed_toucan",
        "Sulcata Tortoise": "sulcata_tortoise",
        "Sailfin Dragon": "sailfin_dragon",
        "Monkey-Tailed Skink": "monkey_tailed_skink",
    }
    out = {}
    for t in manifest:
        slug = target_names.get(t["name"])
        if slug:
            out[slug] = t["banner"]
    return out


def banner_styling(banner: str):
    """Return (label, agency_text, bg, ink) for the regulatory strip."""
    if banner == "USDA + Harris County":
        return (
            "USDA · HARRIS COUNTY VETERINARY PUBLIC HEALTH",
            "USDA Animal Welfare Act + Harris County primate licensing",
            HC_BG, HC_INK,
        )
    if banner == "USDA":
        return (
            "USDA REGULATED FACILITY",
            "USDA Animal Welfare Act — APHIS jurisdiction",
            USDA_BG, USDA_INK,
        )
    if banner == "Texas Parks & Wildlife":
        return (
            "TEXAS PARKS & WILDLIFE DEPARTMENT",
            "TPWD exotic species permit",
            TPWD_BG, TPWD_INK,
        )
    # Exempt or no banner
    return (
        "NO REGULATORY BANNER — EXEMPT REPTILE",
        "Outside USDA / TPWD jurisdiction. Husbandry per LIFE protocol.",
        EXEMPT_BG, EXEMPT_INK,
    )


def build_poster(sp, banner, out_path):
    """Render one Gold Standard poster: banner strips + card body."""
    PAGE_W, PAGE_H = letter
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Gold Standard Diet — {sp['common_name'].title()}")
    c.setAuthor("Perplexity Computer")

    margin = 0.5 * 72

    # ===== Top: Gold Standard band (full-width, 0.42in) =====
    band_h = 0.42 * 72
    y = PAGE_H - band_h
    c.setFillColor(GOLD_BG)
    c.rect(0, y, PAGE_W, band_h, stroke=0, fill=1)
    c.setFillColor(GOLD_INK)
    c.setFont(v23.DISPLAY, 14)
    c.drawCentredString(PAGE_W / 2, y + band_h / 2 - 5, "GOLD STANDARD · VERBATIM DIET POSTER")

    # ===== Below it: Regulatory band (full-width, 0.34in) =====
    reg_label, reg_sub, reg_bg, reg_ink = banner_styling(banner)
    reg_h = 0.34 * 72
    y2 = y - reg_h
    c.setFillColor(reg_bg)
    c.rect(0, y2, PAGE_W, reg_h, stroke=0, fill=1)
    c.setFillColor(reg_ink)
    c.setFont(v23.DISPLAY, 10)
    c.drawCentredString(PAGE_W / 2, y2 + reg_h / 2 + 1, reg_label)
    c.setFont(v23.BODY, 7.5)
    c.drawCentredString(PAGE_W / 2, y2 + 4, reg_sub)

    # ===== Card body (offset down by total band height) =====
    card_top = y2  # this is where the card content begins
    band_total = (PAGE_H - card_top)

    # Render card content shifted down. v23 builds top-down from PAGE_H - MARGIN.
    # We need to redirect; simplest: override v23 PAGE_H temporarily? No — its functions
    # use module-level constants. Easier: render the card into the lower portion by
    # treating PAGE_H - band_total as the new "top".

    # Render header section manually mirroring v23's first part
    content_top = card_top - 0.10 * 72
    content_w = PAGE_W - 2 * margin

    # Photo + title
    photo_slug = v23.SPECIES_SLUG.get(sp["slug"], sp["slug"])
    photo_path = v23.SPECIES_PHOTOS / f"{photo_slug}.jpg"
    hero_w = 2.1 * 72
    hero_h = 1.5 * 72
    v23.draw_image_box(c, photo_path, margin, content_top - hero_h, hero_w, hero_h, fill_bg=v23.LIGHT)

    tx = margin + hero_w + 12
    tw = content_w - hero_w - 12

    title = sp["common_name"]
    title_size = 20
    while title_size > 11 and c.stringWidth(title, v23.DISPLAY, title_size) > tw - 4:
        title_size -= 0.5
    c.setFont(v23.DISPLAY, title_size)
    c.setFillColor(INK)
    c.drawString(tx, content_top - 20, title)

    sci = sp.get("scientific_name", "")
    if sci:
        c.setFont(v23.BODY, 9)
        c.setFillColor(MUTED)
        c.drawString(tx, content_top - 33, sci)

    c.setFont(v23.BODY_SEMI, 10)
    c.setFillColor(NAVY)
    c.drawString(tx, content_top - 50, sp["category"])

    c.setFont(v23.BODY, 9)
    c.setFillColor(INK)
    c.drawString(tx, content_top - 64, f"WHAT THIS ANIMAL IS: {sp['what_this_animal_is']}")

    sites_str = " · ".join(sp.get("sites", [])) or "—"
    c.drawString(tx, content_top - 76, f"SITES: {sites_str}")

    # 3-second check chip
    chip_text = f"3-SEC CHECK: {sp['three_second_check']}"
    chip_w = c.stringWidth(chip_text, v23.BODY_SEMI, 9) + 16
    chip_x = tx
    chip_y = content_top - 100
    c.setFillColor(HexColor("#FFF4D6"))
    c.setStrokeColor(HexColor("#E0B94A"))
    c.roundRect(chip_x, chip_y, chip_w, 18, 3, stroke=1, fill=1)
    c.setFillColor(HexColor("#6B4A00"))
    c.setFont(v23.BODY_SEMI, 9)
    c.drawString(chip_x + 8, chip_y + 5, chip_text)

    y = content_top - hero_h - 12

    # ===== Standard Diet rule strip =====
    c.setFillColor(NAVY)
    c.rect(margin, y - 16, content_w, 16, stroke=0, fill=1)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont(v23.DISPLAY, 9)
    c.drawString(margin + 8, y - 12, "STANDARD DIET — HEALTHY ANIMALS ONLY")
    c.setFont(v23.BODY, 7.5)
    c.drawRightString(PAGE_W - margin - 8, y - 12, "Excludes sick / vet-care / special-diet animals")
    y -= 20

    y -= 4  # gap between strip and explanatory line
    c.setFillColor(MUTED)
    c.setFont(v23.BODY, 7.5)
    c.drawString(margin, y,
        "Covers ~95% of daily feedings. For the remaining 5%, use training and observation within sound science. Unsure — Pause. Ask. Escalate.")
    y -= 14

    # ===== Morning Feed-Out + Encounter Portion band =====
    BAND_BG = HexColor("#EEF2F7")
    BAND_INK = HexColor("#233044")
    BAND_BORDER = HexColor("#A9B6C6")
    ENC_INK = HexColor("#7A3416")
    band_box_h = 0.62 * 72
    c.setFillColor(BAND_BG)
    c.setStrokeColor(BAND_BORDER)
    c.rect(margin, y - band_box_h, content_w, band_box_h, stroke=1, fill=1)
    c.setFillColor(BAND_INK)
    c.setFont(v23.DISPLAY, 9.5)
    c.drawString(margin + 8, y - 14, "MORNING FEED-OUT")
    c.setFillColor(ENC_INK)
    c.drawString(margin + content_w / 2 + 8, y - 14, "ENCOUNTER / ENRICHMENT PORTION")
    c.setFillColor(INK)
    c.setFont(v23.BODY, 8.5)
    # left text
    wrap_text(c, sp["morning_feed"], margin + 8, y - 22, content_w / 2 - 16, v23.BODY, 8.5, leading=11)
    # right text
    wrap_text(c, sp["encounter_portion"], margin + content_w / 2 + 8, y - 22, content_w / 2 - 16, v23.BODY, 8.5, leading=11, color=ENC_INK)
    y -= band_box_h + 6

    c.setFont(v23.BODY_SEMI, 8.5)
    c.setFillColor(NAVY)
    c.drawString(margin + 8, y, f"APPROX DAILY: {sp.get('daily_weight','—')}")
    y -= 14

    # ===== CORRECT row =====
    GREEN_BG = HexColor("#E9F2E3")
    GREEN_INK = HexColor("#2C5020")
    c.setFillColor(GREEN_BG)
    c.rect(margin, y - 18, content_w, 18, stroke=0, fill=1)
    c.setFillColor(GREEN_INK)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(margin + 8, y - 13, "CORRECT")
    c.setFont(v23.BODY, 9)
    correct_str = " · ".join(sp.get("correct", []))
    c.drawString(margin + 90, y - 13, correct_str)
    y -= 26

    # food image strip
    foods = sp.get("correct_foods", [])[:6]
    if foods:
        cell_w = content_w / max(len(foods), 1)
        for i, f in enumerate(foods):
            fx = margin + i * cell_w
            food_path = v23.FOOD / f"{f}.jpg"
            v23.draw_image_box(c, food_path, fx + 4, y - 56, cell_w - 8, 50, fill_bg=v23.LIGHT)
            c.setFont(v23.BODY, 7.5)
            c.setFillColor(INK)
            label = v23.FOOD_LABELS.get(f, f.replace("_", " ").title())
            c.drawCentredString(fx + cell_w / 2, y - 68, label)
        y -= 72

    # ===== WRONG row =====
    RED_BG = HexColor("#F8E3E3")
    RED_INK = HexColor("#8A1C1C")
    c.setFillColor(RED_BG)
    c.rect(margin, y - 18, content_w, 18, stroke=0, fill=1)
    c.setFillColor(RED_INK)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(margin + 8, y - 13, "WRONG — FIX IMMEDIATELY")
    c.setFont(v23.BODY, 9)
    wrong_str = " · ".join(sp.get("wrong", []))
    c.drawString(margin + 200, y - 13, wrong_str)
    y -= 26

    foods_w = sp.get("wrong_foods", [])[:6]
    if foods_w:
        cell_w = content_w / max(len(foods_w), 1)
        for i, f in enumerate(foods_w):
            fx = margin + i * cell_w
            food_path = v23.FOOD / f"{f}.jpg"
            v23.draw_image_box(c, food_path, fx + 4, y - 56, cell_w - 8, 50, fill_bg=v23.LIGHT)
            c.setFont(v23.BODY, 7.5)
            c.setFillColor(INK)
            label = v23.FOOD_LABELS.get(f, f.replace("_", " ").title())
            c.drawCentredString(fx + cell_w / 2, y - 68, label)
        y -= 72

    # ===== Simple build + Prep rule =====
    half = (content_w - 10) / 2
    box_h = 0.55 * 72
    c.setStrokeColor(v23.RULE)
    c.rect(margin, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(v23.DISPLAY, 9.5)
    c.setFillColor(NAVY)
    c.drawString(margin + 8, y - 13, "SIMPLE BUILD")
    c.setFillColor(INK)
    c.setFont(v23.BODY, 8.5)
    for i, line in enumerate(sp["simple_build"]):
        c.drawString(margin + 8, y - 26 - i * 10, "• " + line)

    rx = margin + half + 10
    c.rect(rx, y - box_h, half, box_h, stroke=1, fill=0)
    c.setFont(v23.DISPLAY, 9.5)
    c.setFillColor(NAVY)
    c.drawString(rx + 8, y - 13, "PREP RULE")
    c.setFillColor(INK)
    c.setFont(v23.BODY, 8.5)
    wrap_text(c, sp["prep_rule"], rx + 8, y - 22, half - 16, v23.BODY, 8.5, leading=11)
    y -= box_h + 8

    # ===== Enforcement =====
    if y > 0.85 * 72 + 20:
        c.setFillColor(NAVY)
        c.setFont(v23.DISPLAY, 10.5)
        c.drawCentredString(PAGE_W / 2, y - 10, "MATCH THE BOWL — DO NOT INTERPRET.")
        c.setFont(v23.BODY, 8)
        c.setFillColor(MUTED)
        y -= 20
        if y > 0.85 * 72:
            c.drawCentredString(PAGE_W / 2, y,
                "No photo = feeding not complete.  ·  No substitutions without approval.  ·  Unsure → Pause → Ask → Escalate.")

    # ===== Footer (post-at-exhibit + source) =====
    c.setFont(v23.DISPLAY, 8)
    c.setFillColor(NAVY)
    c.drawCentredString(PAGE_W / 2, 0.62 * 72, "POST AT EXHIBIT  ·  DO NOT REMOVE  ·  SUPERSEDES PRIOR DIET CARDS")

    c.setFont(v23.BODY, 6.5)
    c.setFillColor(MUTED)
    src_line = f"Source: {sp['source_line']}  ·  Verbatim Gold Standard"
    c.drawString(margin, 0.42 * 72, src_line)
    c.drawString(margin, 0.30 * 72,
        "LIFE Diet Governance System  ·  Gold Standard v2026.04.25  ·  Match the bowl. Don't interpret.")
    c.setFillColor(INK)

    c.save()


def main():
    data = json.loads(GS_CONTENT.read_text())
    banners = load_banner_map()
    built = []
    for sp in data["species"]:
        banner = banners.get(sp["slug"], "(no banner)")
        out = POSTER_DIR / f"GoldStandard_{sp['slug']}.pdf"
        build_poster(sp, banner, out)
        built.append({"slug": sp["slug"], "name": sp["common_name"], "banner": banner, "file": out.name})
        print(f"  built {sp['common_name']:35s} | {banner:25s} -> {out.name}")

    # Write manifest
    manifest_path = OUT_DIR / "gold_standard_manifest.json"
    manifest_path.write_text(json.dumps({
        "version": "v2026-04-25",
        "count": len(built),
        "scope": "10 active totems missing Gold Standard verbatim posters",
        "items": built,
    }, indent=2))
    print(f"\nWrote {len(built)} posters + manifest -> {OUT_DIR}")


if __name__ == "__main__":
    main()
