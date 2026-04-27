"""Parameterized door totem builder for paid encounter species.

Adapts the locked v2026-04-25j lemur door sign template to all encounter species.
Renders 16 PDFs (8 species × HOU/SA) + a master combined PDF.

Locked elements (do not change):
  - Brown/cream/gold palette (both venues)
  - "Animals are TEACHERS, not attractions"
  - Pay-Here framing — fee at the door, optional tip on exit
  - "Manager on duty has final say"
  - Footer: "What a living thing can sense becomes its reality. Environment shapes design."
"""
import sys, os
from pathlib import Path

# Use v23 fonts via the locked template path
V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))
import build_diet_cards_v23 as v23

sys.path.insert(0, "/tmp")
from encounter_species import ENCOUNTERS

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfWriter, PdfReader

VERSION = "v2026-04-27a"
OUT = Path(f"/tmp/door_totems_{VERSION}")
OUT.mkdir(parents=True, exist_ok=True)

# ============== PALETTE — locked brown/cream/gold ==============
CREAM = HexColor("#F4EBD9")
COFFEE = HexColor("#3B2A1A")
WALNUT = HexColor("#5C4124")
GOLD = HexColor("#B8860B")
GOLD_LIGHT = HexColor("#E5C56A")
RUST = HexColor("#7A3416")
PAPER = HexColor("#FFFFFF")
RULE = HexColor("#C9B58A")
MUTED = HexColor("#7A6A55")


def wrap(c, text, x, y_top, w, font, size, leading=12, color=None, align="LEFT"):
    style = ParagraphStyle("_w", fontName=font, fontSize=size, leading=leading,
                           textColor=color or COFFEE,
                           alignment={"LEFT": 0, "CENTER": 1, "RIGHT": 2}[align])
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 999)
    p.drawOn(c, x, y_top - ph)
    return ph


def auto_fit_title(c, text, x_center, y, max_w, max_pt=30, min_pt=18, font=None):
    """Shrink title until it fits."""
    font = font or v23.DISPLAY
    pt = max_pt
    while pt > min_pt:
        c.setFont(font, pt)
        if c.stringWidth(text, font, pt) <= max_w:
            break
        pt -= 1
    c.setFont(font, pt)
    c.drawCentredString(x_center, y, text)


def draw_door_totem(out_path, species_key, site_label):
    spec = ENCOUNTERS[species_key]
    PAGE_W, PAGE_H = letter
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Encounter Door Totem — {spec['title']} — {site_label}")
    c.setAuthor("Perplexity Computer")

    # ---- Background cream ----
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # ---- Top GOLD bar ----
    band_h = 0.46 * 72
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 17)
    c.drawCentredString(PAGE_W / 2, PAGE_H - band_h / 2 - 6, "ENCOUNTER ENTRY  ·  PAY HERE")

    # ---- Site label band ----
    site_h = 0.30 * 72
    y_site = PAGE_H - band_h - site_h
    c.setFillColor(WALNUT)
    c.rect(0, y_site, PAGE_W, site_h, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.BODY_SEMI, 10)
    c.drawCentredString(PAGE_W / 2, y_site + site_h / 2 - 3, site_label.upper())

    # ---- Headline ----
    margin = 0.6 * 72
    content_w = PAGE_W - 2 * margin
    y = y_site - 0.42 * 72

    c.setFillColor(COFFEE)
    auto_fit_title(c, spec["title"], PAGE_W / 2, y, content_w - 8, max_pt=30, min_pt=18)
    y -= 22

    c.setFont(v23.DISPLAY, 11)
    c.setFillColor(WALNUT)
    c.drawCentredString(PAGE_W / 2, y, "Animals are TEACHERS, not attractions.")
    y -= 14
    c.setFillColor(MUTED)
    c.setFont(v23.BODY, 9)
    c.drawCentredString(PAGE_W / 2, y,
                        "USDA-regulated  ·  Encounter rules posted at exhibit  ·  Manager on duty has final say.")
    y -= 18

    # ---- Two-column band ----
    col_h = 1.95 * 72
    col_top = y
    col_w = (content_w - 14) / 2

    # LEFT — What you're paying for
    lx = margin
    c.setFillColor(PAPER)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(lx, col_top - col_h, col_w, col_h, 6, stroke=1, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx, col_top - 0.30 * 72, col_w, 0.30 * 72, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 11)
    c.drawString(lx + 10, col_top - 0.21 * 72, "WHAT YOU'RE PAYING FOR")
    c.setFillColor(COFFEE)
    body_left = (
        "<b>Real animal care costs real money.</b><br/>"
        "Your encounter fee directly funds:<br/><br/>"
        "•  USDA-grade housing &amp; veterinary care<br/>"
        "•  Trained keeper time — every encounter is staffed<br/>"
        "•  Species-correct diets (not 'whatever's in the bowl')<br/>"
        "•  Enrichment &amp; daily welfare auditing<br/><br/>"
        "<b>Not a tip — a posted fee, paid at the door.</b>"
    )
    wrap(c, body_left, lx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 8.5, leading=11.5)

    # RIGHT — How it works (species-specific)
    rx = lx + col_w + 14
    c.setFillColor(PAPER)
    c.setStrokeColor(RULE)
    c.roundRect(rx, col_top - col_h, col_w, col_h, 6, stroke=1, fill=1)
    c.setFillColor(WALNUT)
    c.rect(rx, col_top - 0.30 * 72, col_w, 0.30 * 72, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.DISPLAY, 11)
    c.drawString(rx + 10, col_top - 0.21 * 72, "HOW IT WORKS")
    c.setFillColor(COFFEE)
    body_right = (
        f"•  <b>{spec['duration']}</b>, up to <b>{spec['group_size']}</b>, age <b>{spec['age_min']}</b><br/>"
        f"•  Wash hands &amp; sanitize before entry<br/>"
        f"•  {spec['contact_rule']}<br/>"
        f"•  {spec['food_note']}<br/>"
        f"•  No flash, no grabbing<br/><br/>"
        f"Full encounter rules are posted inside.<br/>"
        f"If you're unsure → <b>Pause · Ask · Escalate</b>."
    )
    wrap(c, body_right, rx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 8.5, leading=11.5)

    y = col_top - col_h - 18

    # ---- PAY-HERE block ----
    pay_h = 2.55 * 72
    c.setFillColor(COFFEE)
    c.roundRect(margin, y - pay_h, content_w, pay_h, 8, stroke=0, fill=1)

    qr_size = 1.55 * 72
    qr_x = margin + content_w - qr_size - 18
    qr_y = y - (pay_h + qr_size) / 2
    c.setFillColor(PAPER)
    c.roundRect(qr_x, qr_y, qr_size, qr_size, 6, stroke=0, fill=1)
    c.setStrokeColor(COFFEE)
    c.setLineWidth(0.8)
    c.rect(qr_x + 8, qr_y + 8, qr_size - 16, qr_size - 16, stroke=1, fill=0)
    c.setFillColor(COFFEE)
    c.setFont(v23.DISPLAY, 11)
    c.drawCentredString(qr_x + qr_size / 2, qr_y + qr_size / 2 + 10, "TAP  /  SCAN")
    c.setFont(v23.BODY, 8)
    c.drawCentredString(qr_x + qr_size / 2, qr_y + qr_size / 2 - 4, "to pay your fee")
    c.setFont(v23.BODY, 7)
    c.setFillColor(WALNUT)
    c.drawCentredString(qr_x + qr_size / 2, qr_y + qr_size / 2 - 16, "Apple Pay · Google Pay")
    c.drawCentredString(qr_x + qr_size / 2, qr_y + qr_size / 2 - 26, "Card · Cash inside")

    text_x = margin + 18
    text_w = qr_x - text_x - 18

    # STEP 1
    step_y = y - 22
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(text_x, step_y, "STEP 1 — PAY AT THE DOOR")
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 22)
    c.drawString(text_x, step_y - 28, "Encounter Fee:  $______")
    c.setFont(v23.BODY, 9)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(text_x, step_y - 44,
                 f"Per group of up to {spec['group_size'].split()[0]}  ·  {spec['duration']}  ·  keeper-led")

    # STEP 2
    step_y -= 70
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(text_x, step_y, "STEP 2 — ENJOY THE ENCOUNTER")
    c.setFillColor(PAPER)
    c.setFont(v23.BODY, 9)
    c.drawString(text_x, step_y - 14,
                 f"Keeper checks you in. Hand-sanitize. {spec['duration']} begins.")

    # STEP 3
    step_y -= 36
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(text_x, step_y, "STEP 3 — TIP ON THE WAY OUT (OPTIONAL)")
    c.setFillColor(PAPER)
    c.setFont(v23.BODY, 9)
    c.drawString(text_x, step_y - 14, "Terminal offers 15% / 20% / 25%. Skip is fine.")

    y -= pay_h + 14

    # ---- Exit gratuity teaser ----
    grat_h = 0.65 * 72
    c.setFillColor(GOLD_LIGHT)
    c.setStrokeColor(GOLD)
    c.roundRect(margin, y - grat_h, content_w, grat_h, 6, stroke=1, fill=1)
    c.setFillColor(COFFEE)
    c.setFont(v23.DISPLAY, 11)
    c.drawString(margin + 14, y - 18, "ON YOUR WAY OUT — TIP YOUR KEEPER")
    c.setFont(v23.BODY, 9)
    c.drawString(margin + 14, y - 34,
                 "Terminal offers three preset taps  ·  100% to keepers.")
    chip_y = y - grat_h + 8
    chips = ["15%", "20%", "25%"]
    chip_w = 0.60 * 72
    for i, chip in enumerate(chips):
        cx = margin + content_w - (3 - i) * (chip_w + 6) - 8
        c.setFillColor(COFFEE)
        c.roundRect(cx, chip_y, chip_w, 22, 4, stroke=0, fill=1)
        c.setFillColor(GOLD_LIGHT)
        c.setFont(v23.DISPLAY, 11)
        c.drawCentredString(cx + chip_w / 2, chip_y + 6, chip)
    y -= grat_h + 14

    # ---- Footer principle band ----
    foot_h = 0.42 * 72
    c.setFillColor(WALNUT)
    c.rect(0, 0.45 * 72, PAGE_W, foot_h, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.DISPLAY, 9.5)
    c.drawCentredString(PAGE_W / 2, 0.45 * 72 + foot_h / 2 + 2,
                        "What a living thing can sense becomes its reality. Environment shapes design.")
    c.setFont(v23.BODY, 7.5)
    c.drawCentredString(PAGE_W / 2, 0.45 * 72 + 4,
                        "Manager on duty has final say  ·  Encounter rules posted inside  ·  USDA Animal Welfare Act compliance")

    # bottom strip
    c.setFillColor(GOLD)
    c.rect(0, 0, PAGE_W, 0.22 * 72, stroke=0, fill=1)
    c.setFillColor(WALNUT)
    c.setFont(v23.BODY, 6.5)
    c.drawString(margin, 0.08 * 72, f"LIFE Encounter Door Totem  ·  {VERSION}  ·  {species_key}")
    c.drawRightString(PAGE_W - margin, 0.08 * 72, "Animals are TEACHERS, not attractions.")

    c.save()
    return out_path


def main():
    sites = [
        ("HOU", "Houston Interactive Aquarium & Animal Preserve"),
        ("SA", "San Antonio Aquarium"),
    ]
    species_order = [
        "red_ruffed_lemur",
        "black_and_white_ruffed_lemur",
        "ring_tailed_lemur",
        "two_toed_sloth",
        "kinkajou",
        "capybara",
        "argentine_tegu",
        "prehensile_tailed_porcupine",
    ]

    built = []
    for sp in species_order:
        for code, full in sites:
            out = OUT / f"Door_Totem_{sp}_{code}_{VERSION}.pdf"
            draw_door_totem(out, sp, full)
            built.append(out)
            print(f"  built {out.name}")

    # Combined master
    master = OUT / f"LIFE_Door_Totems_All_{VERSION}.pdf"
    writer = PdfWriter()
    for p in built:
        for page in PdfReader(str(p)).pages:
            writer.add_page(page)
    with open(master, "wb") as f:
        writer.write(f)
    print(f"\n  built {master.name} ({len(built)} pages)")
    return built, master


if __name__ == "__main__":
    main()
