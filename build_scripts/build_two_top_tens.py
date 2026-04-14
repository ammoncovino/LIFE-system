#!/usr/bin/env python3
"""
TWO OWNER'S TOP TENS — Print-ready wall signs
1. OPERATIONAL (back of house)
2. GUEST-FACING (front of house)
"""

import urllib.request, math
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Fonts ──
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)
for name, url in {
    "DMSans": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
}.items():
    p = FONT_DIR / f"{name}.ttf"
    if not p.exists():
        urllib.request.urlretrieve(url, p)
    pdfmetrics.registerFont(TTFont(name, str(p)))

# ── Colors ──
NAVY = HexColor("#2C3481")
TEAL = HexColor("#00AAAD")
RED = HexColor("#CC0000")
DARK = HexColor("#1A1A1A")
MUTED = HexColor("#666666")
LIGHT_BG = HexColor("#EEF0F8")
WHITE = white
WARN_BG = HexColor("#FDE8E8")
GREEN = HexColor("#2E7D32")

W, H = letter
MX = 0.75 * inch
MW = W - 2 * MX

def draw_rounded_rect(c, x, y, w, h, radius=6, fill_color=None, stroke_color=None, stroke_width=1):
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, radius)
    if fill_color: c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(stroke_width)
    c.drawPath(p, fill=1 if fill_color else 0, stroke=1 if stroke_color else 0)
    c.restoreState()

def draw_number_circle(c, x, y, num, bg=NAVY, radius=16):
    c.saveState()
    c.setFillColor(bg)
    c.circle(x, y, radius, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("DMSans", 13)
    c.drawCentredString(x, y - 5, str(num))
    c.restoreState()


# ═══════════════════════════════════════════════════════════
# SIGN 1 — OPERATIONAL TOP TEN
# ═══════════════════════════════════════════════════════════
OUT1 = "/home/user/workspace/LIFE_system/print_ready/SIGN_Top_Ten_Operational.pdf"
c = canvas.Canvas(OUT1, pagesize=letter)
c.setTitle("Owner's Top Ten — Operational")
c.setAuthor("Perplexity Computer")

# Header bar
c.setFillColor(NAVY)
c.rect(0, H - 75, W, 75, fill=1, stroke=0)
c.setFillColor(TEAL)
c.rect(0, H - 78, W, 3, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("DMSans", 28)
c.drawCentredString(W/2, H - 52, "THE OWNER'S TOP TEN")
c.setFont("Inter", 12)
c.drawCentredString(W/2, H - 72, "OPERATIONAL STANDARDS")

y = H - 110

rules = [
    ("If it is not assigned, written, or approved \u2014 do not do it.",
     "No action without authorization. No exceptions."),
    ("Animal welfare overrides everything.",
     "Biology first. Convenience never."),
    ("Follow the written diet exactly. Photo every feeding.",
     "No substitutions. No guessing. No skipping photos."),
    ("Nothing gets thrown away. All food follows the Zero Waste loop.",
     "Uneaten food goes to collection. Not the trash."),
    ("If you are not sure \u2014 STOP. ASK. WAIT.",
     "Uncertainty is not a reason to act. It is a reason to pause."),
    ("No photo = not done. No record = did not happen.",
     "Documentation is proof. Everything is verified."),
    ("Do not move, modify, or add anything to any exhibit.",
     "No toys, no decorations, no relocating animals. Nothing changes without written approval."),
    ("Do not introduce, adopt, or use any software or system without owner approval.",
     "No apps. No tracking tools. No outside systems. If it wasn't approved, it doesn't exist."),
    ("Only authorized individuals approve purchases, sign contracts, or modify operations.",
     "If you did not get written approval to spend money or change a system, stop."),
    ("Workspaces are for work. Not storage. Not socializing. Not sitting.",
     "Offices, back rooms, desks \u2014 clean, organized, active. If you are clocked in, you are working."),
]

for i, (rule, sub) in enumerate(rules):
    box_h = 52
    by = y - box_h
    # Alternating background
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rounded_rect(c, MX, by, MW, box_h, radius=5, fill_color=bg, stroke_color=HexColor("#D0D4E8"), stroke_width=0.5)
    draw_number_circle(c, MX + 22, by + box_h/2, i + 1)
    # Rule text
    c.setFont("DMSans", 11)
    c.setFillColor(DARK)
    c.drawString(MX + 48, by + box_h - 17, rule)
    c.setFont("Inter", 9)
    c.setFillColor(MUTED)
    c.drawString(MX + 48, by + 9, sub)
    y = by - 4

# Footer
y -= 8
c.setStrokeColor(TEAL)
c.setLineWidth(1)
c.line(MX, y, W - MX, y)
y -= 18
c.setFont("Inter", 9)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "LIFE System \u2014 Owner's Operational Standards \u2014 Ammon Covino")
y -= 12
c.setFont("Inter", 8)
c.drawCentredString(W/2, y, "Violation of these rules will result in corrective action. These are non-negotiable.")

c.save()
print(f"Built: {OUT1}")


# ═══════════════════════════════════════════════════════════
# SIGN 2 — GUEST-FACING TOP TEN
# ═══════════════════════════════════════════════════════════
OUT2 = "/home/user/workspace/LIFE_system/print_ready/SIGN_Top_Ten_Guest_Facing.pdf"
c = canvas.Canvas(OUT2, pagesize=letter)
c.setTitle("Owner's Top Ten — Guest-Facing Standards")
c.setAuthor("Perplexity Computer")

# Header bar — slightly different tone
c.setFillColor(NAVY)
c.rect(0, H - 75, W, 75, fill=1, stroke=0)
c.setFillColor(TEAL)
c.rect(0, H - 78, W, 3, fill=1, stroke=0)
c.setFillColor(WHITE)
c.setFont("DMSans", 28)
c.drawCentredString(W/2, H - 52, "THE OWNER'S TOP TEN")
c.setFont("Inter", 12)
c.drawCentredString(W/2, H - 72, "GUEST-FACING STANDARDS")

y = H - 110

guest_rules = [
    ("You are on stage. Smile. Greet every guest.",
     "Guests see you before they see the animals. Your energy sets their experience."),
    ("The facility must be visibly clean at all times.",
     "Floors, glass, exhibits, restrooms, walkways. If it looks dirty, it is dirty. Fix it now."),
    ("The facility must smell clean.",
     "No odor from waste, food prep, or neglect should reach guest areas. Ever."),
    ("Animals must appear healthy, active, and in a quality environment.",
     "Guests observe. If an exhibit looks neglected, they see it. Standards are not negotiable."),
    ("Guest interaction is personal. Make eye contact. Be present.",
     "You are not a body in a uniform. You are the reason someone remembers this place."),
    ("If a guest asks a question you cannot answer, say so honestly.",
     '"That\'s a great question. Let me find someone who can help, or scan the QR code for more."'),
    ("Education is always on. Signs, screens, and QR codes must be correct and functioning.",
     "If a screen is wrong or a sign is missing, report it immediately. Do not ignore it."),
    ("Encounters are joyful. Most are free. Feeding costs money; joy does not.",
     "Do not make guests feel like every experience costs money. Free interaction is the product."),
    ("No personal items, clutter, food, or drinks visible in guest areas.",
     "Your phone, your water bottle, your bag \u2014 not on the floor, not on a ledge, not in sight."),
    ("Orderly and organized. Every area a guest can see must look intentional.",
     "No exposed cords, no random supplies, no half-finished setups. If it looks like backstage, fix it."),
]

for i, (rule, sub) in enumerate(guest_rules):
    box_h = 52
    by = y - box_h
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rounded_rect(c, MX, by, MW, box_h, radius=5, fill_color=bg, stroke_color=HexColor("#D0D4E8"), stroke_width=0.5)
    draw_number_circle(c, MX + 22, by + box_h/2, i + 1, TEAL)
    c.setFont("DMSans", 11)
    c.setFillColor(DARK)
    c.drawString(MX + 48, by + box_h - 17, rule)
    c.setFont("Inter", 9)
    c.setFillColor(MUTED)
    c.drawString(MX + 48, by + 9, sub)
    y = by - 4

# Footer
y -= 8
c.setStrokeColor(TEAL)
c.setLineWidth(1)
c.line(MX, y, W - MX, y)
y -= 18
c.setFont("Inter", 9)
c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "LIFE System \u2014 Owner's Guest-Facing Standards \u2014 Ammon Covino")
y -= 12
c.setFont("Inter", 8)
c.drawCentredString(W/2, y, "Guests judge us in the first 30 seconds. Every second after that confirms or corrects that judgment.")

c.save()
print(f"Built: {OUT2}")
