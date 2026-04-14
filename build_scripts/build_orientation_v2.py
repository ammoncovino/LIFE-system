#!/usr/bin/env python3
"""
STAFF ORIENTATION WALKTHROUGH v2 — 10-page print-ready PDF
Visual-first, child-grade simple, one concept per page.
Face-to-face walk-through with sign-off.
"""

import urllib.request
from pathlib import Path
from datetime import datetime
import math

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas

# ── Fonts ──────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Download DM Sans
dm_url = "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf"
dm_path = FONT_DIR / "DMSans.ttf"
if not dm_path.exists():
    urllib.request.urlretrieve(dm_url, dm_path)
pdfmetrics.registerFont(TTFont("DMSans", str(dm_path)))

# Download Inter
inter_url = "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
inter_path = FONT_DIR / "Inter.ttf"
if not inter_path.exists():
    urllib.request.urlretrieve(inter_url, inter_path)
pdfmetrics.registerFont(TTFont("Inter", str(inter_path)))

# ── Colors ─────────────────────────────────────────────────
NAVY = HexColor("#2C3481")
TEAL = HexColor("#00AAAD")
BLUE = HexColor("#29AAE2")
YELLOW = HexColor("#F9ED32")
CORAL = HexColor("#EF5A67")
RED = HexColor("#CC0000")
DARK_RED = HexColor("#8B0000")
DARK = HexColor("#1A1A1A")
MUTED = HexColor("#666666")
LIGHT_BG = HexColor("#EEF0F8")
LIGHT_TEAL = HexColor("#E0F7FA")
WARN_BG = HexColor("#FDE8E8")
GREEN = HexColor("#2E7D32")
GREEN_BG = HexColor("#E8F5E9")
WHITE = white

W, H = letter
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STAFF_ORIENTATION_WALKTHROUGH.pdf"

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("Staff Orientation Walkthrough")
c.setAuthor("Perplexity Computer")

# ── Helper functions ───────────────────────────────────────
def draw_header_bar(c, title):
    """Navy header bar with white title."""
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - 65, W, 65, fill=1, stroke=0)
    # Teal accent line
    c.setFillColor(TEAL)
    c.rect(0, H - 68, W, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("DMSans", 26)
    c.drawCentredString(W/2, H - 48, title)
    c.restoreState()

def draw_footer(c, page_num):
    """Page number footer."""
    c.saveState()
    c.setFont("Inter", 8)
    c.setFillColor(MUTED)
    c.drawCentredString(W/2, 22, f"Page {page_num}")
    c.restoreState()

def draw_rounded_rect(c, x, y, w, h, radius=8, fill_color=None, stroke_color=None, stroke_width=1):
    """Draw a rounded rectangle."""
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    if fill_color and stroke_color:
        c.drawPath(p, fill=1, stroke=1)
    elif fill_color:
        c.drawPath(p, fill=1, stroke=0)
    elif stroke_color:
        c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def draw_circle_number(c, x, y, num, radius=22, bg_color=NAVY):
    """Draw a numbered circle."""
    c.saveState()
    c.setFillColor(bg_color)
    c.circle(x, y, radius, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("DMSans", 16)
    c.drawCentredString(x, y - 6, str(num))
    c.restoreState()

def draw_rule_box(c, x, y, w, h, text, font_size=14):
    """Red-bordered critical rule box."""
    draw_rounded_rect(c, x, y, w, h, radius=6, fill_color=WARN_BG, stroke_color=RED, stroke_width=2)
    c.saveState()
    c.setFillColor(DARK_RED)
    c.setFont("DMSans", font_size)
    # Center text in box
    text_w = c.stringWidth(text, "DMSans", font_size)
    if text_w > w - 30:
        # Multi-line: split at reasonable point
        words = text.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        c.drawCentredString(x + w/2, y + h/2 + 6, line1)
        c.drawCentredString(x + w/2, y + h/2 - 14, line2)
    else:
        c.drawCentredString(x + w/2, y + h/2 - 5, text)
    c.restoreState()

def draw_green_box(c, x, y, w, h, text, font_size=13):
    """Green positive-action box."""
    draw_rounded_rect(c, x, y, w, h, radius=6, fill_color=GREEN_BG, stroke_color=GREEN, stroke_width=1.5)
    c.saveState()
    c.setFillColor(GREEN)
    c.setFont("DMSans", font_size)
    text_w = c.stringWidth(text, "DMSans", font_size)
    if text_w > w - 30:
        words = text.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        c.drawCentredString(x + w/2, y + h/2 + 6, line1)
        c.drawCentredString(x + w/2, y + h/2 - 14, line2)
    else:
        c.drawCentredString(x + w/2, y + h/2 - 5, text)
    c.restoreState()

def draw_navy_box(c, x, y, w, h, text, font_size=14):
    """Navy filled box with white text."""
    draw_rounded_rect(c, x, y, w, h, radius=6, fill_color=NAVY)
    c.saveState()
    c.setFillColor(WHITE)
    c.setFont("DMSans", font_size)
    c.drawCentredString(x + w/2, y + h/2 - 5, text)
    c.restoreState()

def draw_x_mark(c, x, y, size=14):
    """Draw a red X."""
    c.saveState()
    c.setStrokeColor(RED)
    c.setLineWidth(3)
    c.line(x - size/2, y - size/2, x + size/2, y + size/2)
    c.line(x - size/2, y + size/2, x + size/2, y - size/2)
    c.restoreState()

def draw_checkmark(c, x, y, size=14):
    """Draw a green checkmark."""
    c.saveState()
    c.setStrokeColor(GREEN)
    c.setLineWidth(3)
    c.line(x - size/2, y, x - size/6, y - size/2)
    c.line(x - size/6, y - size/2, x + size/2, y + size/3)
    c.restoreState()

def draw_arrow(c, x1, y1, x2, y2, color=NAVY):
    """Draw an arrow from (x1,y1) to (x2,y2)."""
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(2)
    c.line(x1, y1, x2, y2)
    # Arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 8
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - arrow_len * math.cos(angle - 0.4), y2 - arrow_len * math.sin(angle - 0.4))
    p.lineTo(x2 - arrow_len * math.cos(angle + 0.4), y2 - arrow_len * math.sin(angle + 0.4))
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def draw_flow_box(c, x, y, w, h, text, bg_color=LIGHT_TEAL, text_color=DARK, border_color=TEAL, sub_text=None):
    """Draw a flow diagram box with optional subtitle."""
    draw_rounded_rect(c, x, y, w, h, radius=6, fill_color=bg_color, stroke_color=border_color, stroke_width=1.5)
    c.saveState()
    c.setFillColor(text_color)
    c.setFont("DMSans", 12)
    if sub_text:
        c.drawCentredString(x + w/2, y + h/2 + 4, text)
        c.setFont("Inter", 9)
        c.setFillColor(MUTED)
        c.drawCentredString(x + w/2, y + h/2 - 12, sub_text)
    else:
        c.drawCentredString(x + w/2, y + h/2 - 4, text)
    c.restoreState()

MX = inch  # margin x
MW = W - 2*inch  # margin width

# ═══════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════
# Full navy background
c.setFillColor(NAVY)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Teal accent bar at top
c.setFillColor(TEAL)
c.rect(0, H - 8, W, 8, fill=1, stroke=0)

# Title
c.setFillColor(WHITE)
c.setFont("DMSans", 42)
c.drawCentredString(W/2, H - 220, "Staff")
c.drawCentredString(W/2, H - 275, "Orientation")

# Thin yellow divider
c.setFillColor(YELLOW)
c.rect(MX + 60, H - 310, MW - 120, 3, fill=1, stroke=0)

# Locations
c.setFillColor(HexColor("#B0B8D8"))
c.setFont("Inter", 13)
c.drawCentredString(W/2, H - 345, "San Antonio Aquarium")
c.drawCentredString(W/2, H - 365, "Houston Interactive Aquarium & Animal Preserve")

# Instructions
c.setFillColor(HexColor("#8890B0"))
c.setFont("Inter", 12)
c.drawCentredString(W/2, H - 430, "Read with your manager. Page by page.")
c.drawCentredString(W/2, H - 450, "Sign at the end.")

# Sign-in fields on cover
cy = 220
c.setStrokeColor(HexColor("#4A5090"))
c.setLineWidth(0.5)
c.setFillColor(HexColor("#9DA3C0"))
c.setFont("Inter", 12)

c.drawString(MX + 40, cy + 40, "Date:")
c.line(MX + 120, cy + 38, W - MX - 40, cy + 38)

c.drawString(MX + 40, cy, "Employee:")
c.line(MX + 150, cy - 2, W - MX - 40, cy - 2)

# Effective date
c.setFont("Inter", 9)
c.setFillColor(HexColor("#6A70A0"))
c.drawCentredString(W/2, 50, f"Effective: {datetime.now().strftime('%B %Y')}  |  Owner: Ammon Covino")

draw_footer(c, 1)
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 2 — HOW WE WORK HERE (THE ONE RULE)
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "How We Work Here")
draw_footer(c, 2)

y = H - 120

# Rule box 1 — THE rule
draw_rounded_rect(c, MX, y - 85, MW, 85, radius=10, fill_color=LIGHT_BG, stroke_color=NAVY, stroke_width=1.5)
draw_circle_number(c, MX + 40, y - 42, 1)
c.setFont("DMSans", 17)
c.setFillColor(DARK)
c.drawString(MX + 75, y - 32, "If it is not assigned, written,")
c.drawString(MX + 75, y - 54, "or approved \u2014 do not do it.")
y -= 105

# Rule box 2
draw_rounded_rect(c, MX, y - 85, MW, 85, radius=10, fill_color=LIGHT_BG, stroke_color=NAVY, stroke_width=1.5)
draw_circle_number(c, MX + 40, y - 42, 2)
c.setFont("DMSans", 17)
c.setFillColor(DARK)
c.drawString(MX + 75, y - 32, "If you are not sure \u2014")
c.drawString(MX + 75, y - 54, "stop and ask.")
y -= 105

# Rule box 3
draw_rounded_rect(c, MX, y - 85, MW, 85, radius=10, fill_color=LIGHT_BG, stroke_color=NAVY, stroke_width=1.5)
draw_circle_number(c, MX + 40, y - 42, 3)
c.setFont("DMSans", 17)
c.setFillColor(DARK)
c.drawString(MX + 75, y - 32, "Every task has an owner.")
c.drawString(MX + 75, y - 54, "If it is yours, own it.")

# Navy bottom bar with emphasis
y -= 105
draw_navy_box(c, MX, y - 50, MW, 50, "This is not optional. This is how we operate.", 15)

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 3 — HOW TASKS WORK (CLAIM SYSTEM)
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "How Tasks Work")
draw_footer(c, 3)

y = H - 120

# 4-step flow diagram
box_w = 115
box_h = 55
gap = 20
total_w = 4 * box_w + 3 * gap
start_x = (W - total_w) / 2

flow_items = [
    ("A task", "is posted"),
    ("You claim it", '"I will take this"'),
    ("You do it", ""),
    ("It gets", "verified"),
]

for i, (line1, line2) in enumerate(flow_items):
    bx = start_x + i * (box_w + gap)
    by = y - box_h
    draw_rounded_rect(c, bx, by, box_w, box_h, radius=6, fill_color=LIGHT_TEAL, stroke_color=TEAL, stroke_width=1.5)
    c.setFont("DMSans", 12)
    c.setFillColor(DARK)
    if line2:
        c.drawCentredString(bx + box_w/2, by + box_h/2 + 4, line1)
        c.setFont("Inter", 9)
        c.setFillColor(MUTED)
        c.drawCentredString(bx + box_w/2, by + box_h/2 - 12, line2)
    else:
        c.drawCentredString(bx + box_w/2, by + box_h/2 - 4, line1)
    # Arrow between boxes
    if i < 3:
        ax = bx + box_w + 2
        ay = by + box_h/2
        draw_arrow(c, ax, ay, ax + gap - 4, ay, NAVY)

y -= box_h + 60

# Bold statements
c.setFont("DMSans", 18)
c.setFillColor(DARK)
c.drawCentredString(W/2, y, "If you don't claim it, it's not yours.")
y -= 35
c.setFillColor(RED)
c.setFont("DMSans", 18)
c.drawCentredString(W/2, y, "If nobody claims it, we have a problem.")

y -= 30
c.setStrokeColor(HexColor("#D0D0D0"))
c.setLineWidth(0.5)
c.line(MX, y, W - MX, y)
y -= 30

c.setFont("Inter", 14)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "Every open task must have a person\u2019s name on it.")
y -= 24
c.drawCentredString(W/2, y, "If you see something unclaimed, flag it.")

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 4 — ANIMAL CARE / DIET PROTOCOL
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "Animal Care Is Not Optional")
draw_footer(c, 4)

y = H - 90

# Subtitle
c.setFont("DMSans", 20)
c.setFillColor(TEAL)
c.drawCentredString(W/2, y, "Diet Verification Protocol")
c.setStrokeColor(TEAL)
c.setLineWidth(1.5)
c.line(MX + 60, y - 8, W - MX - 60, y - 8)

y -= 40

# 4 step boxes
steps = [
    ("Prepare", "Use the written diet sheet. No substitutions."),
    ("Verify", "Confirm items and amounts."),
    ("Photograph", "Take a clear photo. Post with animal name, date, your initials."),
    ("Deliver", "Place food according to protocol."),
]

for i, (label, desc) in enumerate(steps):
    by = y - 75
    draw_rounded_rect(c, MX, by, MW, 70, radius=8, fill_color=LIGHT_TEAL, stroke_color=TEAL, stroke_width=1)
    draw_circle_number(c, MX + 35, by + 35, i+1, 20, TEAL)
    c.setFont("DMSans", 16)
    c.setFillColor(DARK)
    c.drawString(MX + 65, by + 42, label)
    c.setFont("Inter", 12)
    c.setFillColor(MUTED)
    c.drawString(MX + 65, by + 18, desc)
    y = by - 10

y -= 10
# Red warning box
draw_rule_box(c, MX, y - 60, MW, 55,
    "No guessing. No 'close enough.' No skipping photos.", 16)

y -= 80
# Extra rules
c.setFont("Inter", 12)
c.setFillColor(DARK)
c.drawString(MX + 10, y, "\u2022  No animal fed to fullness before guest hours")
y -= 20
c.drawString(MX + 10, y, "\u2022  Manager reviews all photos and responds \"Verified\"")

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 5 — ZERO WASTE FOOD LOOP
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "Nothing Gets Thrown Away")
draw_footer(c, 5)

y = H - 110

# Flow diagram — horizontal
labels = ["Food", "Compost", "Bugs", "Chickens", "Eggs", "Animals"]
colors_list = [
    HexColor("#C8E6C9"), HexColor("#B2DFDB"), HexColor("#B2DFDB"),
    HexColor("#B2EBF2"), HexColor("#FFF9C4"), HexColor("#B3E5FC"),
]
box_w = 78
box_h = 42
gap = 10
total_w = 6 * box_w + 5 * gap
sx = (W - total_w) / 2

for i, (label, clr) in enumerate(zip(labels, colors_list)):
    bx = sx + i * (box_w + gap)
    draw_rounded_rect(c, bx, y - box_h, box_w, box_h, radius=6, fill_color=clr, stroke_color=TEAL, stroke_width=1)
    c.setFont("DMSans", 12)
    c.setFillColor(DARK)
    c.drawCentredString(bx + box_w/2, y - box_h/2 - 4, label)
    if i < 5:
        draw_arrow(c, bx + box_w + 2, y - box_h/2, bx + box_w + gap - 2, y - box_h/2, NAVY)

y -= box_h + 40

# Key statements
c.setFont("DMSans", 17)
c.setFillColor(DARK)
c.drawCentredString(W/2, y, "ALL uneaten food goes in the collection bin.")
y -= 25
c.setFont("Inter", 13)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "The outside aviary is the only exception.")

y -= 35
c.setStrokeColor(HexColor("#D0D0D0"))
c.setLineWidth(0.5)
c.line(MX, y, W - MX, y)
y -= 30

# Red X
draw_x_mark(c, MX + 25, y, 18)
c.setFont("DMSans", 17)
c.setFillColor(RED)
c.drawString(MX + 50, y - 7, "DO NOT throw food in the trash.")

y -= 45
c.setStrokeColor(HexColor("#D0D0D0"))
c.line(MX, y, W - MX, y)
y -= 15

# Warning box
draw_rule_box(c, MX, y - 60, MW, 55,
    "If you are about to throw something away \u2014 STOP. You are breaking the system.", 14)

y -= 80

# Sorting guide
c.setFont("DMSans", 14)
c.setFillColor(NAVY)
c.drawString(MX, y, "How to Sort:")
y -= 25
c.setFont("Inter", 12)
c.setFillColor(DARK)
items = [
    ("\u2022  Compost bin: fruits, vegetables, grains, plant material",),
    ("\u2022  Controlled bin: meat, eggs, protein",),
    ("\u2022  Reject: plastic, trash, anything unknown \u2014 ASK if unsure",),
]
for (txt,) in items:
    c.drawString(MX + 10, y, txt)
    y -= 20

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 6 — HOW TO CLEAN
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "How to Clean")
draw_footer(c, 6)

y = H - 100

# Cleaning items with checkmarks
clean_items = [
    ("Acrylic windows", "Blue rags + distilled water ONLY. Nothing else."),
    ("Exhibits", "Virkon for disinfection. Follow the label."),
    ("Food prep areas", "Clean, sanitize, photo."),
    ("Water dishes", "Carbon filtered water where specified."),
]

for label, desc in clean_items:
    by = y - 70
    draw_rounded_rect(c, MX, by, MW, 65, radius=8, fill_color=LIGHT_TEAL, stroke_color=TEAL, stroke_width=1)
    draw_checkmark(c, MX + 28, by + 38, 16)
    c.setFont("DMSans", 16)
    c.setFillColor(DARK)
    c.drawString(MX + 50, by + 40, label)
    c.setFont("Inter", 12)
    c.setFillColor(MUTED)
    c.drawString(MX + 50, by + 16, desc)
    y = by - 12

y -= 5
draw_rule_box(c, MX, y - 60, MW, 55,
    "If you don't know the method for something, ASK. Do not guess.", 15)

y -= 75
draw_green_box(c, MX, y - 50, MW, 45,
    "Clean as you go. No temporary fixes. No messes for later.", 13)

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 7 — EDUCATION SYSTEM (LIFE)
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "Education Is Always On")
draw_footer(c, 7)

y = H - 100

# LIFE banner
draw_navy_box(c, MX + 40, y - 45, MW - 80, 40,
    "LIFE = Language, Intelligence, Form, Ecology", 15)
y -= 70

c.setFont("Inter", 13)
c.setFillColor(DARK)
c.drawString(MX, y, "This facility runs an education system. It is not a gimmick.")
y -= 22
c.drawString(MX, y, "Every sign, QR code, and exhibit teaches visitors something.")
y -= 35

# What you need to know
c.setFont("DMSans", 16)
c.setFillColor(NAVY)
c.drawString(MX, y, "Your role:")
y -= 28

info_items = [
    "Do not get in the way of the system.",
    "Do not make up facts about animals.",
    "Do not move, edit, or remove signs.",
    "Do not create your own materials.",
    "Do not tell visitors what to think.",
]
for item in info_items:
    draw_x_mark(c, MX + 15, y + 2, 12)
    c.setFont("Inter", 13)
    c.setFillColor(DARK)
    c.drawString(MX + 40, y - 3, item)
    y -= 28

y -= 10
c.setStrokeColor(HexColor("#D0D0D0"))
c.setLineWidth(0.5)
c.line(MX, y, W - MX, y)
y -= 25

c.setFont("DMSans", 14)
c.setFillColor(GREEN)
c.drawString(MX, y, "If a guest asks you something you don't know:")
y -= 28
c.setFont("Inter", 13)
c.setFillColor(DARK)
c.drawString(MX + 20, y, '"That is a great question. Let me find someone')
y -= 20
c.drawString(MX + 20, y, 'who can help, or you can scan the QR code')
y -= 20
c.drawString(MX + 20, y, 'at the exhibit for more information."')

y -= 30
draw_rule_box(c, MX, y - 50, MW, 45,
    "All education content comes from central control. Not staff.", 14)

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 8 — IF YOU MAKE A MISTAKE (ESCALATION)
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "If You Make a Mistake")
draw_footer(c, 8)

y = H - 115

# Strike circles
strikes = [
    (HexColor("#FFC107"), "Strike 1", "Correction \u2014 we fix it together"),
    (HexColor("#FF9800"), "Strike 2", "Warning + retraining"),
    (HexColor("#D32F2F"), "Strike 3", "Disciplinary action"),
]

for color, label, desc in strikes:
    # Circle
    c.saveState()
    c.setFillColor(color)
    c.circle(MX + 45, y - 5, 32, fill=1, stroke=0)
    # Number in circle
    num = label.split()[1]
    c.setFillColor(WHITE)
    c.setFont("DMSans", 22)
    c.drawCentredString(MX + 45, y - 13, num)
    c.restoreState()

    # Text
    c.setFont("DMSans", 18)
    c.setFillColor(DARK)
    c.drawString(MX + 95, y, label)
    c.setFont("Inter", 13)
    c.setFillColor(MUTED)
    c.drawString(MX + 95, y - 22, desc)

    y -= 80

    # Divider
    c.setStrokeColor(HexColor("#E0E0E0"))
    c.setLineWidth(0.5)
    c.line(MX, y + 20, W - MX, y + 20)

y += 5

c.setFont("Inter", 14)
c.setFillColor(DARK)
c.drawCentredString(W/2, y, "This applies to everyone. Managers too.")
y -= 30
c.setFont("DMSans", 17)
c.setFillColor(NAVY)
c.drawCentredString(W/2, y, "Animal welfare comes first. Always.")

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 9 — DO NOT (COMPREHENSIVE LIST)
# ═══════════════════════════════════════════════════════════
draw_header_bar(c, "Do Not")
draw_footer(c, 9)

y = H - 110

donts = [
    "Do not act without authorization",
    "Do not substitute diet items",
    "Do not throw away food",
    "Do not clean acrylic with anything except blue rags + distilled water",
    "Do not skip photos",
    "Do not improvise",
    "Do not edit checklists or procedures yourself",
    "Do not make up facts about animals",
    "Do not move or remove signs",
]

for item in donts:
    draw_x_mark(c, MX + 18, y, 16)
    c.setFont("Inter", 14)
    c.setFillColor(DARK)
    c.drawString(MX + 50, y - 5, item)
    y -= 42

y -= 5
c.setStrokeColor(HexColor("#D0D0D0"))
c.setLineWidth(0.5)
c.line(MX, y, W - MX, y)
y -= 30

# STOP → ASK → WAIT buttons
btn_w = 120
btn_h = 45
gap = 30
total_w = 3 * btn_w + 2 * gap
sx = (W - total_w) / 2

# STOP button (red)
draw_rounded_rect(c, sx, y - btn_h, btn_w, btn_h, radius=8, fill_color=RED)
c.setFont("DMSans", 20)
c.setFillColor(WHITE)
c.drawCentredString(sx + btn_w/2, y - btn_h/2 - 7, "STOP")

# Arrow
draw_arrow(c, sx + btn_w + 5, y - btn_h/2, sx + btn_w + gap - 5, y - btn_h/2, NAVY)

# ASK button (orange)
ax = sx + btn_w + gap
draw_rounded_rect(c, ax, y - btn_h, btn_w, btn_h, radius=8, fill_color=HexColor("#FF9800"))
c.setFont("DMSans", 20)
c.setFillColor(WHITE)
c.drawCentredString(ax + btn_w/2, y - btn_h/2 - 7, "ASK")

# Arrow
draw_arrow(c, ax + btn_w + 5, y - btn_h/2, ax + btn_w + gap - 5, y - btn_h/2, NAVY)

# WAIT button (teal)
wx = ax + btn_w + gap
draw_rounded_rect(c, wx, y - btn_h, btn_w, btn_h, radius=8, fill_color=TEAL)
c.setFont("DMSans", 20)
c.setFillColor(WHITE)
c.drawCentredString(wx + btn_w/2, y - btn_h/2 - 7, "WAIT")

# Subtitle
c.setFont("Inter", 12)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y - btn_h - 18, "When in doubt")

c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 10 — SIGN-OFF
# ═══════════════════════════════════════════════════════════
# Header bar - slightly different for sign-off
c.setFillColor(NAVY)
c.rect(0, H - 55, W, 55, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("DMSans", 24)
c.drawCentredString(W/2, H - 40, "I Have Read and Understand This Document")

draw_footer(c, 10)

y = H - 100

# Confirmation text
c.setFont("Inter", 13)
c.setFillColor(DARK)
lines = [
    "My manager walked me through every page of this orientation.",
    "I understand the rules, the diet protocol, the food waste system,",
    "the cleaning standards, the education system, and the documentation requirements.",
    "I understand that if I am unsure about something, I will stop",
    "and ask before acting.",
]
for line in lines:
    c.drawCentredString(W/2, y, line)
    y -= 22

y -= 15
c.setStrokeColor(TEAL)
c.setLineWidth(1)
c.line(MX, y, W - MX, y)
y -= 35

# Employee section
c.setFont("Inter", 12)
c.setFillColor(DARK)

c.drawString(MX + 10, y, "Employee Name (print):")
c.setStrokeColor(MUTED)
c.setLineWidth(0.5)
c.line(MX + 185, y - 2, W - MX - 10, y - 2)
y -= 40

c.drawString(MX + 10, y, "Employee Signature:")
c.line(MX + 170, y - 2, W - MX - 10, y - 2)
y -= 40

c.drawString(MX + 10, y, "Date:")
c.line(MX + 70, y - 2, MX + 250, y - 2)
y -= 45

# Divider
c.setStrokeColor(TEAL)
c.setLineWidth(1)
c.line(MX, y, W - MX, y)
y -= 35

# Conducted-by section
c.setFont("Inter", 12)
c.setFillColor(DARK)
c.setStrokeColor(MUTED)
c.setLineWidth(0.5)

c.drawString(MX + 10, y, "Conducted By (print):")
c.line(MX + 180, y - 2, W - MX - 10, y - 2)
y -= 40

c.drawString(MX + 10, y, "Conductor Signature:")
c.line(MX + 175, y - 2, W - MX - 10, y - 2)
y -= 40

c.drawString(MX + 10, y, "Date:")
c.line(MX + 70, y - 2, MX + 250, y - 2)
y -= 40

# Divider
c.setStrokeColor(TEAL)
c.setLineWidth(1)
c.line(MX, y, W - MX, y)
y -= 25

# Fine print
c.setFont("Inter", 10)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "This document is retained by management.")
y -= 16
c.drawCentredString(W/2, y, "A copy may be provided to the employee upon request.")

c.save()
print(f"Built: {OUTPUT}")
print(f"Size: {Path(OUTPUT).stat().st_size:,} bytes")
