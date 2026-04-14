#!/usr/bin/env python3
"""Staff Orientation Walkthrough PDF — ReportLab Canvas API"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
import os

# ── Output path ──────────────────────────────────────────────────────────────
OUT_PATH = "/home/user/workspace/LIFE_system/print_ready/STAFF_ORIENTATION_WALKTHROUGH.pdf"
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

# ── Page size ─────────────────────────────────────────────────────────────────
W, H = letter          # 612 x 792 pts
MARGIN = 54            # ~0.75 in

# ── Colour palette ────────────────────────────────────────────────────────────
NAVY   = HexColor("#2C3481")
BROWN  = HexColor("#271610")
TEAL   = HexColor("#00AAAD")
RED    = HexColor("#CC0000")
GREEN  = HexColor("#2E7D32")
YELLOW = HexColor("#F9A825")
ORANGE = HexColor("#E65100")
LIGHT_TEAL_BG = HexColor("#E0F7F7")
LIGHT_RED_BG  = HexColor("#FFF0F0")
LIGHT_GRAY    = HexColor("#F4F4F4")
MID_GRAY      = HexColor("#CCCCCC")
DARK_GRAY     = HexColor("#555555")

# ── Helpers ───────────────────────────────────────────────────────────────────

def page_number_footer(c, page_num):
    """Draw small page number at bottom center."""
    c.setFont("Helvetica", 9)
    c.setFillColor(MID_GRAY)
    c.drawCentredString(W / 2, 22, f"Page {page_num}")


def header_bar(c, title, color=NAVY):
    """Full-width header bar at top."""
    bar_h = 64
    c.setFillColor(color)
    c.rect(0, H - bar_h, W, bar_h, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W / 2, H - bar_h + 18, title)


def draw_rule(c, y, color=MID_GRAY, lw=1):
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    c.line(MARGIN, y, W - MARGIN, y)


def callout_box(c, x, y, w, h, bg_color, border_color, text_lines,
                font="Helvetica-Bold", font_size=16, text_color=None):
    """Draw a filled callout box with centred text lines."""
    if text_color is None:
        text_color = border_color
    radius = 6
    c.setFillColor(bg_color)
    c.setStrokeColor(border_color)
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

    # multi-line text, top-aligned with padding
    padding = 14
    line_h = font_size * 1.4
    total_text_h = len(text_lines) * line_h
    start_y = y + h - padding - font_size
    c.setFillColor(text_color)
    c.setFont(font, font_size)
    for i, line in enumerate(text_lines):
        c.drawCentredString(x + w / 2, start_y - i * line_h, line)


def circle_number(c, cx, cy, r, number, bg_color=NAVY):
    """Draw a filled circle with a number inside."""
    c.setFillColor(bg_color)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", r * 1.0)
    c.drawCentredString(cx, cy - r * 0.35, str(number))


def draw_x_mark(c, cx, cy, size=10, color=None):
    """Draw a red X mark."""
    c.setStrokeColor(color if color else RED)
    c.setLineWidth(3)
    half = size * 0.7
    c.line(cx - half, cy - half, cx + half, cy + half)
    c.line(cx + half, cy - half, cx - half, cy + half)


def draw_check_mark(c, cx, cy, size=10):
    """Draw a green checkmark."""
    c.setStrokeColor(GREEN)
    c.setLineWidth(3)
    c.setLineCap(1)
    p = c.beginPath()
    p.moveTo(cx - size * 0.5, cy)
    p.lineTo(cx - size * 0.1, cy - size * 0.5)
    p.lineTo(cx + size * 0.6, cy + size * 0.5)
    c.drawPath(p, stroke=1, fill=0)


def arrow_right(c, x1, y, x2, color=NAVY, lw=2.5):
    """Draw a horizontal right arrow."""
    from reportlab.graphics.shapes import Drawing
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.line(x1, y, x2 - 8, y)
    # arrowhead
    p = c.beginPath()
    p.moveTo(x2, y)
    p.lineTo(x2 - 12, y + 6)
    p.lineTo(x2 - 12, y - 6)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def arrow_down(c, x, y1, y2, color=NAVY, lw=2.5):
    """Draw a downward arrow."""
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.line(x, y1, x, y2 + 8)
    p = c.beginPath()
    p.moveTo(x, y2)
    p.lineTo(x - 6, y2 + 12)
    p.lineTo(x + 6, y2 + 12)
    p.close()
    c.drawPath(p, stroke=0, fill=1)


def step_box(c, x, y, w, h, label, sub="", bg=LIGHT_TEAL_BG, border=TEAL):
    """Draw a step box with a label (supports \\n in label)."""
    c.setFillColor(bg)
    c.setStrokeColor(border)
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    lines = label.split("\n")
    line_h = 16
    total = len(lines) * line_h
    start = y + h / 2 + total / 2 - line_h * 0.7
    for i, ln in enumerate(lines):
        c.drawCentredString(x + w / 2, start - i * line_h, ln)
    if sub:
        c.setFont("Helvetica", 10)
        c.setFillColor(BROWN)
        sub_lines = sub.split("\n")
        sub_start = y + 14
        for i, sl in enumerate(sub_lines):
            c.drawCentredString(x + w / 2, sub_start - i * 13, sl)


# ══════════════════════════════════════════════════════════════════════════════
# Build PDF
# ══════════════════════════════════════════════════════════════════════════════
c = canvas.Canvas(OUT_PATH, pagesize=letter)
c.setTitle("Staff Orientation Walkthrough")
c.setAuthor("Perplexity Computer")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — COVER
# ─────────────────────────────────────────────────────────────────────────────
# Navy background top half
c.setFillColor(NAVY)
c.rect(0, H / 2, W, H / 2, fill=1, stroke=0)

# Teal accent band
c.setFillColor(TEAL)
c.rect(0, H / 2 - 6, W, 12, fill=1, stroke=0)

# Title
c.setFillColor(white)
c.setFont("Helvetica-Bold", 52)
c.drawCentredString(W / 2, H - 200, "Staff")
c.setFont("Helvetica-Bold", 52)
c.drawCentredString(W / 2, H - 262, "Orientation")

# Subtitle — location placeholder
c.setFillColor(LIGHT_TEAL_BG)
c.setFont("Helvetica", 22)
c.drawCentredString(W / 2, H - 310, "[Location Name]")

# Bottom half — instructions
y = H / 2 - 60
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(W / 2, y, "Read with your manager.")
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(W / 2, y - 36, "Sign at the end.")

draw_rule(c, y - 64, color=MID_GRAY, lw=1)

# Date and Employee lines
c.setFont("Helvetica", 16)
c.setFillColor(BROWN)
line_y = y - 110
c.drawString(MARGIN + 20, line_y, "Date:")
c.setStrokeColor(MID_GRAY)
c.setLineWidth(1)
c.line(MARGIN + 80, line_y, W - MARGIN - 20, line_y)

line_y -= 54
c.drawString(MARGIN + 20, line_y, "Employee:")
c.line(MARGIN + 110, line_y, W - MARGIN - 20, line_y)

page_number_footer(c, 1)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — HOW WE WORK
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "How We Work Here")

rules = [
    ("1", "If it is not assigned, written,\nor approved — do not do it."),
    ("2", "If you are not sure —\nstop and ask."),
    ("3", "Every task has an owner.\nIf it is yours, own it."),
]

start_y = H - 110
for i, (num, text) in enumerate(rules):
    box_y = start_y - i * 168
    # background strip
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(NAVY)
    c.setLineWidth(2)
    c.roundRect(MARGIN, box_y - 120, W - 2 * MARGIN, 128, 8, fill=1, stroke=1)

    # number circle
    circle_number(c, MARGIN + 40, box_y - 56, 22, num, bg_color=NAVY)

    # rule text
    lines = text.split("\n")
    c.setFillColor(BROWN)
    c.setFont("Helvetica-Bold", 20)
    text_x = MARGIN + 80
    c.drawString(text_x, box_y - 42, lines[0])
    if len(lines) > 1:
        c.drawString(text_x, box_y - 70, lines[1])

# Bottom callout
callout_y = start_y - 3 * 168 + 10
callout_box(c, MARGIN, callout_y, W - 2 * MARGIN, 58,
            NAVY, NAVY,
            ["This is not optional. This is how we operate."],
            font="Helvetica-Bold", font_size=17, text_color=white)

page_number_footer(c, 2)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — CLAIMING WORK
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "How Tasks Work")

# 4-step horizontal flow
steps = [
    ("A task\nis posted", ""),
    ("You claim it", '"I will take\nthis"'),
    ("You do it", ""),
    ("It gets\nverified", ""),
]

box_w = 108
box_h = 80
gap = 28
total_w = 4 * box_w + 3 * gap
start_x = (W - total_w) / 2
flow_y = H - 220

for i, (label, sub) in enumerate(steps):
    bx = start_x + i * (box_w + gap)
    step_box(c, bx, flow_y, box_w, box_h, label, sub)
    if i < 3:
        arrow_right(c, bx + box_w, flow_y + box_h / 2,
                    bx + box_w + gap, color=TEAL, lw=3)

# "If you don't claim it..." lines
c.setFont("Helvetica-Bold", 18)
c.setFillColor(BROWN)
c.drawCentredString(W / 2, flow_y - 60, "If you don't claim it, it's not yours.")

c.setFont("Helvetica-Bold", 18)
c.setFillColor(RED)
c.drawCentredString(W / 2, flow_y - 100, "If nobody claims it, we have a problem.")

# small reminder
draw_rule(c, flow_y - 130, color=MID_GRAY)
c.setFont("Helvetica", 15)
c.setFillColor(DARK_GRAY)
c.drawCentredString(W / 2, flow_y - 160, "Every open task must have a person's name on it.")
c.drawCentredString(W / 2, flow_y - 186, "If you see something unclaimed, flag it.")

page_number_footer(c, 3)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — ANIMAL CARE RULE
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "Animal Care Is Not Optional")

# Big bold sub-header
c.setFillColor(TEAL)
c.setFont("Helvetica-Bold", 26)
c.drawCentredString(W / 2, H - 100, "Diet Verification Protocol")
draw_rule(c, H - 114, color=TEAL, lw=2)

steps4 = [
    ("1", "Prepare", "Use the written diet sheet. No substitutions."),
    ("2", "Verify",  "Confirm items and amounts."),
    ("3", "Photograph", "Take a clear photo. Post with animal name, date, your initials."),
    ("4", "Deliver",  "Place food according to protocol."),
]

step_h = 72
step_gap = 18
start_y4 = H - 148

for i, (num, title, detail) in enumerate(steps4):
    sy = start_y4 - i * (step_h + step_gap)
    # background
    bg_col = LIGHT_TEAL_BG if i % 2 == 0 else HexColor("#F0FAFA")
    c.setFillColor(bg_col)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.roundRect(MARGIN, sy - step_h + 8, W - 2 * MARGIN, step_h, 6, fill=1, stroke=1)
    # number circle
    circle_number(c, MARGIN + 36, sy - step_h / 2 + 8, 20, num, bg_color=TEAL)
    # title
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN + 68, sy - 22, title)
    # detail
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 14)
    c.drawString(MARGIN + 68, sy - 46, detail)

# Red callout — positioned below the last step box
last_sy = start_y4 - 3 * (step_h + step_gap)
last_box_bottom = last_sy - step_h + 8
red_y = last_box_bottom - 82
callout_box(c, MARGIN, red_y, W - 2 * MARGIN, 72,
            LIGHT_RED_BG, RED,
            ["No guessing.", "No 'close enough.'  No skipping photos."],
            font="Helvetica-Bold", font_size=17, text_color=RED)

page_number_footer(c, 4)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — FOOD WASTE RULE
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "Nothing Gets Thrown Away")

# Flow diagram: Food → Compost → Bugs → Chickens → Eggs → Animals
flow_items = ["Food", "Compost", "Bugs", "Chickens", "Eggs", "Animals"]
flow_colors = [
    HexColor("#A5D6A7"),  # green
    HexColor("#A5D6A7"),
    HexColor("#80CBC4"),
    HexColor("#80CBC4"),
    HexColor("#FFF176"),
    HexColor("#80DEEA"),
]

box_w5 = 72
box_h5 = 50
gap5 = 16
total_w5 = len(flow_items) * box_w5 + (len(flow_items) - 1) * gap5
start_x5 = (W - total_w5) / 2
flow_y5 = H - 178

for i, (label, col) in enumerate(zip(flow_items, flow_colors)):
    bx = start_x5 + i * (box_w5 + gap5)
    c.setFillColor(col)
    c.setStrokeColor(NAVY)
    c.setLineWidth(2)
    c.roundRect(bx, flow_y5, box_w5, box_h5, 6, fill=1, stroke=1)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(bx + box_w5 / 2, flow_y5 + 17, label)
    if i < len(flow_items) - 1:
        arrow_right(c, bx + box_w5, flow_y5 + box_h5 / 2,
                    bx + box_w5 + gap5, color=NAVY, lw=2.5)

# Main rule
c.setFillColor(BROWN)
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(W / 2, flow_y5 - 52, "ALL uneaten food goes in the collection bin.")

# Exception note
c.setFillColor(DARK_GRAY)
c.setFont("Helvetica", 15)
c.drawCentredString(W / 2, flow_y5 - 84,
                    "The outside aviary is the only exception.")

draw_rule(c, flow_y5 - 104, color=MID_GRAY)

# Red X — DO NOT throw away
xmark_y = flow_y5 - 140
draw_x_mark(c, MARGIN + 30, xmark_y + 14, size=16)
c.setFillColor(RED)
c.setFont("Helvetica-Bold", 20)
c.drawString(MARGIN + 60, xmark_y + 6, "DO NOT throw food in the trash.")

draw_rule(c, xmark_y - 28, color=MID_GRAY)

# Warning text
callout_box(c, MARGIN, xmark_y - 110, W - 2 * MARGIN, 70,
            LIGHT_RED_BG, RED,
            ["If you are about to throw something away — STOP.",
             "You are breaking the system."],
            font="Helvetica-Bold", font_size=16, text_color=RED)

page_number_footer(c, 5)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 — CLEANING STANDARDS
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "How to Clean")

cleaning_items = [
    ("Acrylic windows",   "Blue rags + distilled water ONLY. Nothing else."),
    ("Exhibits",          "Virkon for disinfection. Follow the label."),
    ("Food prep areas",   "Clean, sanitize, photo."),
    ("Water dishes",      "Carbon filtered water where specified."),
]

start_y6 = H - 112
item_h = 86
for i, (area, method) in enumerate(cleaning_items):
    iy = start_y6 - i * (item_h + 10)
    bg = LIGHT_TEAL_BG if i % 2 == 0 else HexColor("#F0FAFA")
    c.setFillColor(bg)
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.roundRect(MARGIN, iy - item_h + 8, W - 2 * MARGIN, item_h, 6, fill=1, stroke=1)
    # checkmark
    draw_check_mark(c, MARGIN + 36, iy - item_h / 2 + 8, size=14)
    # area label
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(MARGIN + 66, iy - 28, area)
    # method
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 15)
    c.drawString(MARGIN + 66, iy - 52, method)

# Red callout — placed below last item box
last_iy6 = start_y6 - (len(cleaning_items) - 1) * (item_h + 10)
last_box_bottom6 = last_iy6 - item_h + 8
red_y6 = last_box_bottom6 - 82
callout_box(c, MARGIN, red_y6, W - 2 * MARGIN, 72,
            LIGHT_RED_BG, RED,
            ["If you don't know the method for something, ASK.",
             "Do not guess."],
            font="Helvetica-Bold", font_size=16, text_color=RED)

page_number_footer(c, 6)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 7 — WHAT HAPPENS WHEN THINGS GO WRONG
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "If You Make a Mistake")

strikes = [
    (1, "Strike 1", "Correction — we fix it together", YELLOW,  BROWN),
    (2, "Strike 2", "Warning + retraining",             ORANGE,  white),
    (3, "Strike 3", "Disciplinary action",              RED,     white),
]

start_y7 = H - 120
strike_gap = 148

for i, (num, label, desc, bg, txt_col) in enumerate(strikes):
    sy = start_y7 - i * strike_gap

    # Large circle
    cx = MARGIN + 54
    cy = sy - 44
    c.setFillColor(bg)
    c.circle(cx, cy, 42, fill=1, stroke=0)
    # number
    c.setFillColor(txt_col)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(cx, cy - 13, str(num))

    # label + description
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(cx + 62, sy - 30, label)
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 18)
    c.drawString(cx + 62, sy - 58, desc)

    # divider (except last)
    if i < 2:
        draw_rule(c, sy - strike_gap + 12, color=LIGHT_GRAY, lw=1)

# Bottom statements
bottom_y7 = start_y7 - 3 * strike_gap + 20
draw_rule(c, bottom_y7, color=MID_GRAY, lw=1)
c.setFillColor(BROWN)
c.setFont("Helvetica", 16)
c.drawCentredString(W / 2, bottom_y7 - 30, "This applies to everyone. Managers too.")
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(W / 2, bottom_y7 - 62, "Animal welfare comes first. Always.")

page_number_footer(c, 7)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 8 — DOCUMENTATION
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "If It's Not Documented, It Didn't Happen")

doc_items = [
    "Diet prep (before feeding)",
    "Food waste collection",
    "Cleaning completion",
    "Any issue or damage",
]

start_y8 = H - 110

# "Photos are required for:" intro
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 22)
c.drawString(MARGIN, start_y8, "Photos are required for:")

item_y = start_y8 - 42
for item in doc_items:
    # camera icon placeholder — simple rectangle with circle
    c.setFillColor(TEAL)
    c.roundRect(MARGIN + 4, item_y - 6, 28, 22, 3, fill=1, stroke=0)
    c.setFillColor(white)
    c.circle(MARGIN + 18, item_y + 5, 7, fill=1, stroke=0)
    # text
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 18)
    c.drawString(MARGIN + 44, item_y + 2, item)
    item_y -= 44

# "Post photos with:" block
draw_rule(c, item_y - 6, color=MID_GRAY)
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 18)
c.drawString(MARGIN, item_y - 36, "Post photos with:")

c.setFillColor(TEAL)
c.setFont("Helvetica-Bold", 17)
c.drawCentredString(W / 2, item_y - 70,
                    "Animal/Area name  +  Date  +  Your initials")

draw_rule(c, item_y - 90, color=MID_GRAY)

# "No photo = task not complete"
callout_box(c, MARGIN, item_y - 168, W - 2 * MARGIN, 64,
            LIGHT_RED_BG, RED,
            ["No photo = task not complete"],
            font="Helvetica-Bold", font_size=22, text_color=RED)

page_number_footer(c, 8)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 9 — WHAT NOT TO DO
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "Do Not")

donots = [
    "Do not act without authorization",
    "Do not substitute diet items",
    "Do not throw away food",
    "Do not clean acrylic with anything except blue rags + distilled water",
    "Do not skip photos",
    "Do not improvise",
    "Do not edit checklists or procedures yourself",
]

start_y9 = H - 106
item_gap = 60

for i, text in enumerate(donots):
    iy = start_y9 - i * item_gap
    draw_x_mark(c, MARGIN + 24, iy + 5, size=14)
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 16)
    c.drawString(MARGIN + 54, iy - 1, text)

# Bottom STOP → ASK → WAIT
bottom_y9 = start_y9 - len(donots) * item_gap - 10
draw_rule(c, bottom_y9, color=MID_GRAY)

btn_w = 110
btn_h = 52
btn_gap = 36
labels = ["STOP", "ASK", "WAIT"]
colors9 = [RED, ORANGE, TEAL]
total_btn_w = 3 * btn_w + 2 * btn_gap
btn_start_x = (W - total_btn_w) / 2
btn_y = bottom_y9 - 80

for i, (lbl, col) in enumerate(zip(labels, colors9)):
    bx = btn_start_x + i * (btn_w + btn_gap)
    c.setFillColor(col)
    c.roundRect(bx, btn_y, btn_w, btn_h, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(bx + btn_w / 2, btn_y + 15, lbl)
    if i < 2:
        arrow_right(c, bx + btn_w + 4, btn_y + btn_h / 2,
                    bx + btn_w + btn_gap - 4, color=NAVY, lw=3)

c.setFont("Helvetica", 13)
c.setFillColor(DARK_GRAY)
c.drawCentredString(W / 2, btn_y - 24, "When in doubt")

page_number_footer(c, 9)
c.showPage()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 10 — SIGN-OFF PAGE
# ─────────────────────────────────────────────────────────────────────────────
header_bar(c, "I Have Read and Understand This Document", color=NAVY)

# Intro paragraphs
texts10 = [
    "My manager walked me through every page of this orientation.",
    "I understand the rules, the diet protocol, the food waste system,",
    "and the documentation requirements.",
    "I understand that if I am unsure about something, I will stop",
    "and ask before acting.",
]

ty = H - 110
for t in texts10:
    c.setFillColor(BROWN)
    c.setFont("Helvetica", 16)
    c.drawCentredString(W / 2, ty, t)
    ty -= 28

# Signature block
draw_rule(c, ty - 10, color=MID_GRAY, lw=1.5)

sig_items = [
    ("Employee Name (print):", 280),
    ("Employee Signature:", 280),
    ("Date:", 160),
    ("Manager Name (print):", 280),
    ("Manager Signature:", 280),
    ("Date:", 160),
]

sig_y = ty - 52
label_x = MARGIN + 10
line_x_start = MARGIN + 220
c.setFont("Helvetica", 15)
c.setFillColor(BROWN)

for i, (lbl, line_len) in enumerate(sig_items):
    if i == 3:
        # Separator before manager block
        draw_rule(c, sig_y + 24, color=LIGHT_GRAY)
    c.setFont("Helvetica", 15)
    c.setFillColor(BROWN)
    c.drawString(label_x, sig_y, lbl)
    c.setStrokeColor(MID_GRAY)
    c.setLineWidth(1)
    c.line(line_x_start, sig_y, line_x_start + line_len, sig_y)
    sig_y -= 48

# Footer notice
draw_rule(c, sig_y - 8, color=MID_GRAY)
c.setFont("Helvetica", 11)
c.setFillColor(DARK_GRAY)
c.drawCentredString(W / 2, sig_y - 28,
    "This document is retained by management.")
c.drawCentredString(W / 2, sig_y - 46,
    "A copy may be provided to the employee upon request.")

page_number_footer(c, 10)
c.showPage()

# ── Save ──────────────────────────────────────────────────────────────────────
c.save()
print(f"PDF saved to: {OUT_PATH}")
