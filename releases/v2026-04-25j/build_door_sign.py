#!/usr/bin/env python3
"""LIFE Encounter Door Sign — Pay-Here framing  ·  v2026-04-25j

User decisions encoded:
  - Encounter fee at the DOOR (not a tip jar)
  - 15 / 20 / 25 % exit-gratuity prompt handled by the payment terminal
    (Stripe / Square / Toast — like restaurant checkout)
  - Brown palette stays for BOTH Houston and San Antonio
  - Encounter rules already exist — DO NOT rebuild; reference them
  - "Animals are TEACHERS, not attractions"
  - "Manager on duty" — never name personnel

Outputs two PDFs:
  Lemur_Encounter_Door_Sign_HOU_v2026-04-25j.pdf
  Lemur_Encounter_Door_Sign_SA_v2026-04-25j.pdf

Plus an exit gratuity card (small, 4×6 in) with three preset percentages.
"""
import sys
from pathlib import Path

# Use v23 fonts
V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))
import build_diet_cards_v23 as v23  # noqa: E402

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

OUT = Path("/tmp/LIFE-push/releases/v2026-04-25j/door_signs")
OUT.mkdir(parents=True, exist_ok=True)

# ============== PALETTE — Brown / cream / gold (BOTH sites) =====
CREAM = HexColor("#F4EBD9")       # background
COFFEE = HexColor("#3B2A1A")      # primary ink — deep brown
WALNUT = HexColor("#5C4124")      # secondary brown
GOLD = HexColor("#B8860B")        # accent gold (matches GS band)
GOLD_LIGHT = HexColor("#E5C56A")
RUST = HexColor("#7A3416")        # encounter sub-accent (used in GS posters)
PAPER = HexColor("#FFFFFF")
RULE = HexColor("#C9B58A")
MUTED = HexColor("#7A6A55")


def wrap(c, text, x, y_top, w, font, size, leading=12, color=None, align="LEFT"):
    style = ParagraphStyle("_w", fontName=font, fontSize=size, leading=leading,
                           textColor=color or COFFEE, alignment={"LEFT": 0, "CENTER": 1, "RIGHT": 2}[align])
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 999)
    p.drawOn(c, x, y_top - ph)
    return ph


def draw_door_sign(out_path, site_label):
    """Letter-portrait door sign — 8.5×11 in.

    Layout (top to bottom):
      [GOLD bar]     "ENCOUNTER ENTRY · PAY HERE"
      Headline       "RED-RUFFED LEMUR ENCOUNTER"
      Sub            "{site_label} · Animals are TEACHERS, not attractions."
      Two-col band:
         LEFT  → "What you're paying for" (real costs framing)
         RIGHT → "How it works" (encounter rules — pointer only, NOT rebuilt)
      Pay-here block (large, with QR placeholder + price line)
      Exit gratuity card preview note
      Footer: ground-truth principle + manager-on-duty escalation line
    """
    PAGE_W, PAGE_H = letter
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Encounter Door Sign — {site_label}")
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

    # ---- Site label band (walnut) ----
    site_h = 0.30 * 72
    y_site = PAGE_H - band_h - site_h
    c.setFillColor(WALNUT)
    c.rect(0, y_site, PAGE_W, site_h, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.BODY_SEMI, 10)
    c.drawCentredString(PAGE_W / 2, y_site + site_h / 2 - 3, site_label.upper())

    # ---- Headline block ----
    margin = 0.6 * 72
    content_w = PAGE_W - 2 * margin
    y = y_site - 0.38 * 72

    c.setFillColor(COFFEE)
    c.setFont(v23.DISPLAY, 30)
    c.drawCentredString(PAGE_W / 2, y, "RED-RUFFED LEMUR ENCOUNTER")
    y -= 22

    c.setFont(v23.DISPLAY, 11)
    c.setFillColor(WALNUT)
    c.drawCentredString(PAGE_W / 2, y,
                        "Animals are TEACHERS, not attractions.")
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

    # left column — "What you're paying for"
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
    body_text_left = (
        "<b>Real animal care costs real money.</b><br/>"
        "Your encounter fee directly funds:<br/>"
        "<br/>"
        "•  USDA-grade housing &amp; veterinary care<br/>"
        "•  Trained keeper time — every encounter is staffed<br/>"
        "•  Species-correct diets (not 'whatever's in the bowl')<br/>"
        "•  Enrichment &amp; daily welfare auditing<br/>"
        "<br/>"
        "<b>Not a tip — a posted fee, paid at the door.</b>"
    )
    wrap(c, body_text_left, lx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 8.5, leading=11.5)

    # right column — "How it works"
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
    body_text_right = (
        "•  <b>10 minutes</b>, up to <b>6 guests</b>, age <b>5+</b><br/>"
        "•  Wash hands &amp; sanitize before entry<br/>"
        "•  Keeper leads — <b>match the keeper, not the animal</b><br/>"
        "•  Quiet voices &amp; slow movement<br/>"
        "•  Food comes <b>from the daily allocation</b>, never extra<br/>"
        "•  No flash, no grabbing, no tail/limb contact<br/>"
        "<br/>"
        "Full encounter rules are posted inside.<br/>"
        "If you're unsure → <b>Pause · Ask · Escalate</b>."
    )
    wrap(c, body_text_right, rx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 8.5, leading=11.5)

    y = col_top - col_h - 18

    # ---- PAY-HERE block (large, centered) ----
    pay_h = 2.55 * 72
    c.setFillColor(COFFEE)
    c.roundRect(margin, y - pay_h, content_w, pay_h, 8, stroke=0, fill=1)

    # QR / Tap placeholder (right side, full height of pay block)
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

    # Left side — three steps stacked
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
    c.drawString(text_x, step_y - 44, "Per group of up to 6  ·  10 minutes  ·  keeper-led")

    # STEP 2
    step_y -= 70
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(text_x, step_y, "STEP 2 — ENJOY THE ENCOUNTER")
    c.setFillColor(PAPER)
    c.setFont(v23.BODY, 9)
    c.drawString(text_x, step_y - 14, "Keeper checks you in. Hand-sanitize. 10 minutes begins.")

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
    # Three percent chips, right-aligned
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
    c.drawString(margin, 0.08 * 72,
                 f"LIFE Encounter Door Sign  ·  v2026-04-25j  ·  Pay-Here framing")
    c.drawRightString(PAGE_W - margin, 0.08 * 72,
                      "Animals are TEACHERS, not attractions.")

    c.save()


def draw_exit_gratuity_card(out_path, site_label):
    """4×6 in card to print and place at the exit terminal.

    Three-button gratuity prompt explanation.
    """
    PAGE_W, PAGE_H = (4 * 72, 6 * 72)
    c = canvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"LIFE Exit Gratuity Card — {site_label}")
    c.setAuthor("Perplexity Computer")

    # background
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # top band
    band_h = 0.45 * 72
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 13)
    c.drawCentredString(PAGE_W / 2, PAGE_H - band_h / 2 - 5, "TIP YOUR KEEPER")

    # subtitle
    y = PAGE_H - band_h - 0.30 * 72
    c.setFillColor(COFFEE)
    c.setFont(v23.DISPLAY, 11)
    c.drawCentredString(PAGE_W / 2, y, "Three taps. That's it.")
    y -= 16
    c.setFont(v23.BODY, 9)
    c.setFillColor(WALNUT)
    wrap(c, "The terminal will show three preset percentages. Pick one — or skip — and you're done.",
         0.4 * 72, y, PAGE_W - 0.8 * 72, v23.BODY, 9, leading=12, align="CENTER")
    y -= 38

    # Three big chips
    chips = [("15%", "Standard"), ("20%", "Generous"), ("25%", "Outstanding")]
    chip_w = (PAGE_W - 0.6 * 72 - 24) / 3
    chip_h = 1.1 * 72
    chip_y = y - chip_h
    for i, (pct, label) in enumerate(chips):
        cx = 0.30 * 72 + i * (chip_w + 12)
        # box
        c.setFillColor(COFFEE)
        c.roundRect(cx, chip_y, chip_w, chip_h, 6, stroke=0, fill=1)
        # pct
        c.setFillColor(GOLD_LIGHT)
        c.setFont(v23.DISPLAY, 22)
        c.drawCentredString(cx + chip_w / 2, chip_y + chip_h - 30, pct)
        # label
        c.setFillColor(CREAM)
        c.setFont(v23.BODY, 8)
        c.drawCentredString(cx + chip_w / 2, chip_y + 18, label)

    y = chip_y - 22

    # Why box
    c.setFillColor(PAPER)
    c.setStrokeColor(RULE)
    c.roundRect(0.3 * 72, y - 1.1 * 72, PAGE_W - 0.6 * 72, 1.1 * 72, 6, stroke=1, fill=1)
    c.setFillColor(WALNUT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(0.4 * 72, y - 16, "WHY TIP?")
    c.setFillColor(COFFEE)
    body = (
        "Your encounter <b>fee</b> covers animal care, food, and housing. "
        "Your <b>tip</b> goes 100% to the keeper who led your encounter. "
        "Like a restaurant — the fee is the meal, the tip is for the server."
    )
    wrap(c, body, 0.4 * 72, y - 30, PAGE_W - 0.8 * 72, v23.BODY, 8.5, leading=11.5)

    # Footer
    c.setFillColor(WALNUT)
    c.rect(0, 0, PAGE_W, 0.3 * 72, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.BODY, 6)
    c.drawCentredString(PAGE_W / 2, 0.10 * 72,
                        f"v2026-04-25j  ·  Animals are TEACHERS, not attractions.")

    c.save()


def main():
    sites = [
        ("HOU", "Houston Interactive Aquarium & Animal Preserve"),
        ("SA", "San Antonio Aquarium"),
    ]
    for code, full in sites:
        door = OUT / f"Lemur_Encounter_Door_Sign_{code}_v2026-04-25j.pdf"
        card = OUT / f"Exit_Gratuity_Card_{code}_v2026-04-25j.pdf"
        draw_door_sign(door, full)
        draw_exit_gratuity_card(card, full)
        print(f"  built {door.name}")
        print(f"  built {card.name}")


if __name__ == "__main__":
    main()
