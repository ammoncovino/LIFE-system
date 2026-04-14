#!/usr/bin/env python3
"""
COMPLETE STAFF RESET PACKAGE — Single PDF
One hour, cover to cover, everything at once.

Contents:
  1. Cover — "Full Staff Reset"
  2. Owner's Top Ten — Operational
  3. Owner's Top Ten — Guest-Facing
  4-14. Orientation Walkthrough (11 pages: rules, tasks, diet, waste, cleaning, education, exhibits, workspace, do-not, sign-off)

Total: ~15 pages, one continuous document, print and read top to bottom.
"""

import urllib.request, math
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)
for name, url in {
    "DMSans": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
}.items():
    p = FONT_DIR / f"{name}.ttf"
    if not p.exists(): urllib.request.urlretrieve(url, p)
    pdfmetrics.registerFont(TTFont(name, str(p)))

# ── Colors ──
NAVY = HexColor("#2C3481")
TEAL = HexColor("#00AAAD")
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
YELLOW = HexColor("#F9ED32")

W, H = letter
MX = 0.75 * inch
MW = W - 2 * MX
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STAFF_RESET_PACKAGE.pdf"

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("Complete Staff Reset Package")
c.setAuthor("Perplexity Computer")

page_num = [0]  # mutable counter

def new_page():
    page_num[0] += 1

def draw_header_bar(title, font_size=26):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H-65, W, 65, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, H-68, W, 3, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("DMSans", font_size)
    c.drawCentredString(W/2, H-48, title)
    c.restoreState()

def draw_footer():
    c.saveState()
    c.setFont("Inter", 8); c.setFillColor(MUTED)
    c.drawCentredString(W/2, 22, f"Page {page_num[0]}")
    c.drawRightString(W-MX, 22, "STAFF RESET PACKAGE — CONFIDENTIAL")
    c.restoreState()

def rr(x, y, w, h, r=6, fill=None, stroke=None, sw=1):
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y, w, h, r)
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()

def cn(x, y, num, bg=NAVY, r=16):
    c.saveState()
    c.setFillColor(bg); c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("DMSans", 12); c.drawCentredString(x, y-4, str(num))
    c.restoreState()

def xm(x, y, s=14):
    c.saveState(); c.setStrokeColor(RED); c.setLineWidth(3)
    c.line(x-s/2, y-s/2, x+s/2, y+s/2); c.line(x-s/2, y+s/2, x+s/2, y-s/2)
    c.restoreState()

def chk(x, y, s=14):
    c.saveState(); c.setStrokeColor(GREEN); c.setLineWidth(3)
    c.line(x-s/2, y, x-s/6, y-s/2); c.line(x-s/6, y-s/2, x+s/2, y+s/3)
    c.restoreState()

def arr(x1, y1, x2, y2, color=NAVY):
    c.saveState(); c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(2)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2-y1, x2-x1); al = 8
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2-al*math.cos(a-0.4), y2-al*math.sin(a-0.4))
    p.lineTo(x2-al*math.cos(a+0.4), y2-al*math.sin(a+0.4))
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

def rb(x, y, w, h, text, fs=14):
    rr(x, y, w, h, r=6, fill=WARN_BG, stroke=RED, sw=2)
    c.saveState(); c.setFillColor(DARK_RED); c.setFont("DMSans", fs)
    tw = c.stringWidth(text, "DMSans", fs)
    if tw > w - 30:
        words = text.split(); mid = len(words) // 2
        c.drawCentredString(x+w/2, y+h/2+6, " ".join(words[:mid]))
        c.drawCentredString(x+w/2, y+h/2-14, " ".join(words[mid:]))
    else:
        c.drawCentredString(x+w/2, y+h/2-5, text)
    c.restoreState()

def nb(x, y, w, h, text, fs=14):
    rr(x, y, w, h, r=6, fill=NAVY)
    c.saveState(); c.setFillColor(WHITE); c.setFont("DMSans", fs)
    c.drawCentredString(x+w/2, y+h/2-5, text); c.restoreState()

def gb(x, y, w, h, text, fs=13):
    rr(x, y, w, h, r=6, fill=GREEN_BG, stroke=GREEN, sw=1.5)
    c.saveState(); c.setFillColor(GREEN); c.setFont("DMSans", fs)
    c.drawCentredString(x+w/2, y+h/2-5, text); c.restoreState()

def divider(y):
    c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)

# ═══════════════════════════════════════════════════════════
# PAGE 1 — MASTER COVER
# ═══════════════════════════════════════════════════════════
new_page()
c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(TEAL); c.rect(0, H-8, W, 8, fill=1, stroke=0)

c.setFillColor(WHITE); c.setFont("DMSans", 44)
c.drawCentredString(W/2, H-180, "FULL STAFF")
c.drawCentredString(W/2, H-235, "RESET")

c.setFillColor(YELLOW); c.rect(MX+80, H-270, MW-160, 3, fill=1, stroke=0)

c.setFillColor(HexColor("#B0B8D8")); c.setFont("Inter", 14)
c.drawCentredString(W/2, H-305, "San Antonio Aquarium")
c.drawCentredString(W/2, H-325, "Houston Interactive Aquarium & Animal Preserve")

c.setFillColor(HexColor("#8890B0")); c.setFont("Inter", 12)
c.drawCentredString(W/2, H-380, "This document replaces all previous systems.")
c.drawCentredString(W/2, H-400, "Read it cover to cover. Understand it. Sign it.")

# Table of contents
cy = 280
c.setFillColor(HexColor("#9DA3C0")); c.setFont("DMSans", 12)
c.drawString(MX+40, cy+10, "CONTENTS")
c.setFont("Inter", 11); c.setFillColor(HexColor("#8890B0"))
toc = [
    "Pages 2\u20133    Owner's Top Ten \u2014 Operational Standards",
    "Pages 4\u20135    Owner's Top Ten \u2014 Guest-Facing Standards",
    "Pages 6\u201315   Staff Orientation Walkthrough",
    "Page 15       Sign-Off Sheet",
]
for item in toc:
    c.drawString(MX+50, cy-10, item); cy -= 20

# Sign-in fields
cy = 130
c.setStrokeColor(HexColor("#4A5090")); c.setLineWidth(0.5)
c.setFillColor(HexColor("#9DA3C0")); c.setFont("Inter", 12)
c.drawString(MX+40, cy+40, "Date:"); c.line(MX+120, cy+38, W-MX-40, cy+38)
c.drawString(MX+40, cy, "Employee:"); c.line(MX+150, cy-2, W-MX-40, cy-2)

c.setFont("Inter", 9); c.setFillColor(HexColor("#6A70A0"))
c.drawCentredString(W/2, 50, f"Effective: {datetime.now().strftime('%B %Y')}  |  Owner: Ammon Covino")
c.setFont("Inter", 8); c.setFillColor(MUTED); c.drawCentredString(W/2, 22, f"Page {page_num[0]}")
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGES 2-3 — OPERATIONAL TOP TEN (2 pages for larger text)
# ═══════════════════════════════════════════════════════════
op_rules = [
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

# Page 2 — Rules 1-5
new_page()
draw_header_bar("THE OWNER'S TOP TEN", 24)
c.setFont("Inter", 11); c.setFillColor(HexColor("#D0D4E8"))
c.saveState(); c.setFillColor(WHITE); c.setFont("Inter", 10)
c.drawCentredString(W/2, H-67, "OPERATIONAL STANDARDS"); c.restoreState()
draw_footer()

def draw_rule_text(rule, sub, num, by, bh, bg, accent=NAVY):
    """Draw a numbered rule box, auto-shrinking rule text if it overflows."""
    rr(MX, by, MW, bh, r=6, fill=bg, stroke=HexColor("#D0D4E8"), sw=0.5)
    cn(MX+28, by+bh/2, num, accent, 18)
    max_w = MW - 68  # text area width (MX+58 to MX+MW-10)
    fs = 13
    while fs >= 9:
        tw = c.stringWidth(rule, "DMSans", fs)
        if tw <= max_w: break
        fs -= 0.5
    c.setFont("DMSans", fs); c.setFillColor(DARK)
    c.drawString(MX+58, by+bh-22, rule)
    c.setFont("Inter", 10); c.setFillColor(MUTED)
    c.drawString(MX+58, by+12, sub)

y = H - 105
for i, (rule, sub) in enumerate(op_rules[:5]):
    bh = 70; by = y - bh
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rule_text(rule, sub, i+1, by, bh, bg, NAVY)
    y = by - 6
c.showPage()

# Page 3 — Rules 6-10
new_page()
draw_header_bar("THE OWNER'S TOP TEN", 24)
c.saveState(); c.setFillColor(WHITE); c.setFont("Inter", 10)
c.drawCentredString(W/2, H-67, "OPERATIONAL STANDARDS (CONTINUED)"); c.restoreState()
draw_footer()

y = H - 105
for i, (rule, sub) in enumerate(op_rules[5:], 6):
    bh = 70; by = y - bh
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rule_text(rule, sub, i, by, bh, bg, NAVY)
    y = by - 6

y -= 15
nb(MX, y-45, MW, 42, "Violation of these rules will result in corrective action. These are non-negotiable.", 12)

c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGES 4-5 — GUEST-FACING TOP TEN (2 pages)
# ═══════════════════════════════════════════════════════════
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
    ("Education is always on. Signs, screens, and QR codes must be correct.",
     "If a screen is wrong or a sign is missing, report it immediately. Do not ignore it."),
    ("Encounters are joyful. Most are free. Feeding costs money; joy does not.",
     "Do not make guests feel like every experience costs money. Free interaction is the product."),
    ("No personal items, clutter, food, or drinks visible in guest areas.",
     "Your phone, your water bottle, your bag \u2014 not on the floor, not on a ledge, not in sight."),
    ("Orderly and organized. Every area a guest can see must look intentional.",
     "No exposed cords, no random supplies, no half-finished setups. If it looks like backstage, fix it."),
]

# Page 4 — Rules 1-5
new_page()
draw_header_bar("THE OWNER'S TOP TEN", 24)
c.saveState(); c.setFillColor(WHITE); c.setFont("Inter", 10)
c.drawCentredString(W/2, H-67, "GUEST-FACING STANDARDS"); c.restoreState()
draw_footer()

y = H - 105
for i, (rule, sub) in enumerate(guest_rules[:5]):
    bh = 70; by = y - bh
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rule_text(rule, sub, i+1, by, bh, bg, TEAL)
    y = by - 6
c.showPage()

# Page 5 — Rules 6-10
new_page()
draw_header_bar("THE OWNER'S TOP TEN", 24)
c.saveState(); c.setFillColor(WHITE); c.setFont("Inter", 10)
c.drawCentredString(W/2, H-67, "GUEST-FACING STANDARDS (CONTINUED)"); c.restoreState()
draw_footer()

y = H - 105
for i, (rule, sub) in enumerate(guest_rules[5:], 6):
    bh = 70; by = y - bh
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    draw_rule_text(rule, sub, i, by, bh, bg, TEAL)
    y = by - 6

y -= 15
gb(MX, y-42, MW, 40, "Guests judge us in the first 30 seconds. Every second after confirms or corrects.", 11)

c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 6 — ORIENTATION: HOW WE WORK HERE
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("How We Work Here"); draw_footer()
y = H - 120
rules_p = [
    ("If it is not assigned, written,", "or approved \u2014 do not do it."),
    ("If you are not sure \u2014", "stop and ask."),
    ("Every task has an owner.", "If it is yours, own it."),
]
for i, (l1, l2) in enumerate(rules_p):
    rr(MX, y-85, MW, 85, r=10, fill=LIGHT_BG, stroke=NAVY, sw=1.5)
    cn(MX+40, y-42, i+1, NAVY, 20)
    c.setFont("DMSans", 17); c.setFillColor(DARK)
    c.drawString(MX+75, y-32, l1); c.drawString(MX+75, y-54, l2)
    y -= 105
nb(MX, y-50, MW, 50, "This is not optional. This is how we operate.", 15)
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 7 — ORIENTATION: HOW TASKS WORK
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("How Tasks Work"); draw_footer()
y = H - 120
bw, bh2, gap = 115, 55, 20
tw = 4*bw+3*gap; sx = (W-tw)/2
flow = [("A task", "is posted"), ("You claim it", '"I will take this"'), ("You do it", ""), ("It gets", "verified")]
for i, (l1, l2) in enumerate(flow):
    bx = sx+i*(bw+gap); by = y-bh2
    rr(bx, by, bw, bh2, r=6, fill=LIGHT_TEAL, stroke=TEAL, sw=1.5)
    c.setFont("DMSans", 12); c.setFillColor(DARK)
    if l2:
        c.drawCentredString(bx+bw/2, by+bh2/2+4, l1)
        c.setFont("Inter", 9); c.setFillColor(MUTED); c.drawCentredString(bx+bw/2, by+bh2/2-12, l2)
    else:
        c.drawCentredString(bx+bw/2, by+bh2/2-4, l1)
    if i < 3: arr(bx+bw+2, by+bh2/2, bx+bw+gap-2, by+bh2/2, NAVY)
y -= bh2+60
c.setFont("DMSans", 18); c.setFillColor(DARK); c.drawCentredString(W/2, y, "If you don't claim it, it's not yours.")
y -= 35; c.setFillColor(RED); c.drawCentredString(W/2, y, "If nobody claims it, we have a problem.")
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 8 — ORIENTATION: ANIMAL CARE / DIET
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Animal Care Is Not Optional"); draw_footer()
y = H - 90
c.setFont("DMSans", 20); c.setFillColor(TEAL); c.drawCentredString(W/2, y, "Diet Verification Protocol")
c.setStrokeColor(TEAL); c.setLineWidth(1.5); c.line(MX+60, y-8, W-MX-60, y-8)
y -= 40
for i, (label, desc) in enumerate([
    ("Prepare", "Use the written diet sheet. No substitutions."),
    ("Verify", "Confirm items and amounts."),
    ("Photograph", "Take a clear photo. Post with animal name, date, your initials."),
    ("Deliver", "Place food according to protocol."),
]):
    by = y-70
    rr(MX, by, MW, 65, r=8, fill=LIGHT_TEAL, stroke=TEAL, sw=1)
    cn(MX+35, by+32, i+1, TEAL, 18)
    c.setFont("DMSans", 15); c.setFillColor(DARK); c.drawString(MX+65, by+40, label)
    c.setFont("Inter", 11); c.setFillColor(MUTED); c.drawString(MX+65, by+18, desc)
    y = by-8
y -= 5; rb(MX, y-55, MW, 50, "No guessing. No 'close enough.' No skipping photos.", 15)
y -= 70; c.setFont("Inter", 11); c.setFillColor(DARK)
c.drawString(MX+10, y, "\u2022  No animal fed to fullness before guest hours")
y -= 18; c.drawString(MX+10, y, "\u2022  Manager reviews all photos and responds \"Verified\"")
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 9 — ORIENTATION: ZERO WASTE FOOD LOOP
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Nothing Gets Thrown Away"); draw_footer()
y = H - 110
labels = ["Food", "Compost", "Bugs", "Chickens", "Eggs", "Animals"]
colors_list = [HexColor("#C8E6C9"), HexColor("#B2DFDB"), HexColor("#B2DFDB"),
               HexColor("#B2EBF2"), HexColor("#FFF9C4"), HexColor("#B3E5FC")]
bw3, gap3 = 78, 10; tw3 = 6*bw3+5*gap3; sx3 = (W-tw3)/2
for i, (lb, cl) in enumerate(zip(labels, colors_list)):
    bx = sx3+i*(bw3+gap3)
    rr(bx, y-42, bw3, 42, r=6, fill=cl, stroke=TEAL, sw=1)
    c.setFont("DMSans", 12); c.setFillColor(DARK); c.drawCentredString(bx+bw3/2, y-25, lb)
    if i < 5: arr(bx+bw3+2, y-21, bx+bw3+gap3-2, y-21, NAVY)
y -= 80
c.setFont("DMSans", 17); c.setFillColor(DARK); c.drawCentredString(W/2, y, "ALL uneaten food goes in the collection bin.")
y -= 25; c.setFont("Inter", 13); c.setFillColor(MUTED); c.drawCentredString(W/2, y, "The outside aviary is the only exception.")
y -= 35; divider(y); y -= 30
xm(MX+25, y, 18); c.setFont("DMSans", 17); c.setFillColor(RED); c.drawString(MX+50, y-7, "DO NOT throw food in the trash.")
y -= 45; rb(MX, y-55, MW, 50, "If you are about to throw something away \u2014 STOP. You are breaking the system.", 13)
y -= 70; c.setFont("DMSans", 14); c.setFillColor(NAVY); c.drawString(MX, y, "How to Sort:")
y -= 25; c.setFont("Inter", 12); c.setFillColor(DARK)
for txt in ["\u2022  Compost bin: fruits, vegetables, grains, plant material",
            "\u2022  Controlled bin: meat, eggs, protein",
            "\u2022  Reject: plastic, trash, anything unknown \u2014 ASK if unsure"]:
    c.drawString(MX+10, y, txt); y -= 20
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 10 — ORIENTATION: HOW TO CLEAN
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("How to Clean"); draw_footer()
y = H - 100
for label, desc in [
    ("Acrylic windows", "Blue rags + distilled water ONLY. Nothing else."),
    ("Exhibits", "Virkon for disinfection. Follow the label."),
    ("Food prep areas", "Clean, sanitize, photo."),
    ("Water dishes", "Carbon filtered water where specified."),
]:
    by = y-70
    rr(MX, by, MW, 65, r=8, fill=LIGHT_TEAL, stroke=TEAL, sw=1)
    chk(MX+28, by+38, 16)
    c.setFont("DMSans", 16); c.setFillColor(DARK); c.drawString(MX+50, by+40, label)
    c.setFont("Inter", 12); c.setFillColor(MUTED); c.drawString(MX+50, by+16, desc)
    y = by-12
y -= 5; rb(MX, y-55, MW, 50, "If you don't know the method, ASK. Do not guess.", 15)
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 11 — ORIENTATION: EDUCATION SYSTEM
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Education Is Always On"); draw_footer()
y = H - 100
nb(MX+40, y-45, MW-80, 40, "LIFE = Language, Intelligence, Form, Ecology", 15)
y -= 70; c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX, y, "This facility runs an education system. It is not a gimmick.")
y -= 22; c.drawString(MX, y, "Every sign, QR code, and exhibit teaches visitors something.")
y -= 35; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Your role:")
y -= 28
for item in ["Do not get in the way of the system.", "Do not make up facts about animals.",
             "Do not move, edit, or remove signs.", "Do not create your own materials.",
             "Do not tell visitors what to think."]:
    xm(MX+15, y+2, 12); c.setFont("Inter", 13); c.setFillColor(DARK); c.drawString(MX+40, y-3, item); y -= 28
y -= 10; divider(y); y -= 25
c.setFont("DMSans", 14); c.setFillColor(GREEN); c.drawString(MX, y, "If a guest asks something you don't know:")
y -= 28; c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX+20, y, '"That is a great question. Let me find someone')
y -= 20; c.drawString(MX+20, y, 'who can help, or scan the QR code for more."')
y -= 30; rb(MX, y-45, MW, 42, "All education content comes from central control. Not staff.", 13)
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 12 — ORIENTATION: EXHIBIT RULES
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Do Not Touch the Exhibits"); draw_footer()
y = H - 110
rb(MX, y-55, MW, 50, "Do not move, modify, or add anything to any exhibit.", 16)
y -= 80; c.setFont("DMSans", 15); c.setFillColor(NAVY); c.drawString(MX, y, "This means:")
y -= 30
for item in [
    "Do not place toy animals inside exhibits.",
    "Do not relocate any animal from its assigned exhibit.",
    "Do not add decorations, objects, or personal items.",
    "Do not drill, paint, move barriers, or change lighting.",
    "Do not redesign layouts or exhibit flow.",
]:
    xm(MX+15, y+2, 12); c.setFont("Inter", 13); c.setFillColor(DARK); c.drawString(MX+40, y-3, item); y -= 32
y -= 15; divider(y); y -= 25
c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX, y, "Exhibits are designed for biological and behavioral reasons")
y -= 20; c.drawString(MX, y, "you may not understand. That is fine. It is not your job to")
y -= 20; c.drawString(MX, y, "understand the design. It is your job to leave it alone.")
y -= 30; gb(MX, y-45, MW, 42, "If something looks wrong, report it. Do not fix it yourself.", 13)
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 13 — ORIENTATION: WORKSPACE + SOFTWARE + ESCALATION
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Workspaces and Systems", 24); draw_footer()
y = H - 100
c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Offices and Back Rooms")
y -= 25; c.setFont("Inter", 13); c.setFillColor(DARK)
for txt in ["Workspaces are for work. Not storage. Not socializing. Not sitting.",
            "If you are clocked in, you are working. There is no gray zone.",
            "Every desk, drawer, and cabinet must be clean and organized.",
            "If something is broken, report it. If something doesn't belong, remove it."]:
    c.drawString(MX+10, y, txt); y -= 20
y -= 15; divider(y)
y -= 20; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Software and Systems")
y -= 25; c.setFont("Inter", 13); c.setFillColor(DARK)
for txt in ["Do not introduce, adopt, or use any software without owner approval.",
            "No tracking apps. No task management tools. No outside systems.",
            "If a vendor offers a tool, the answer is NO until the owner approves it.",
            "The only systems we use are the ones posted on these walls."]:
    c.drawString(MX+10, y, txt); y -= 20
y -= 15; divider(y)
y -= 20; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "If You Make a Mistake")
y -= 30
for color, label, desc in [(HexColor("#FFC107"), "Strike 1", "Correction"),
                            (HexColor("#FF9800"), "Strike 2", "Warning + retraining"),
                            (HexColor("#D32F2F"), "Strike 3", "Disciplinary action")]:
    c.saveState(); c.setFillColor(color); c.circle(MX+30, y, 18, fill=1, stroke=0)
    num = label.split()[1]; c.setFillColor(WHITE); c.setFont("DMSans", 14); c.drawCentredString(MX+30, y-5, num)
    c.restoreState()
    c.setFont("DMSans", 14); c.setFillColor(DARK); c.drawString(MX+60, y+2, label)
    c.setFont("Inter", 11); c.setFillColor(MUTED); c.drawString(MX+60, y-14, desc)
    y -= 48
c.setFont("Inter", 12); c.setFillColor(DARK); c.drawCentredString(W/2, y, "This applies to everyone. Managers too.")
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 14 — ORIENTATION: DO NOT LIST
# ═══════════════════════════════════════════════════════════
new_page()
draw_header_bar("Do Not"); draw_footer()
y = H - 105
donts = [
    "Do not act without authorization",
    "Do not substitute diet items",
    "Do not throw away food",
    "Do not skip photos",
    "Do not improvise or guess",
    "Do not move, modify, or add to exhibits",
    "Do not relocate animals",
    "Do not use unapproved software or systems",
    "Do not edit checklists or procedures",
    "Do not make up facts about animals",
    "Do not sit in offices doing nothing",
]
for item in donts:
    xm(MX+18, y, 14); c.setFont("Inter", 13); c.setFillColor(DARK); c.drawString(MX+48, y-5, item); y -= 36
y -= 5; divider(y); y -= 30
bw4, bh4, gap4 = 120, 45, 30; tw4 = 3*bw4+2*gap4; sx4 = (W-tw4)/2
for i, (col, txt) in enumerate([(RED, "STOP"), (HexColor("#FF9800"), "ASK"), (TEAL, "WAIT")]):
    bx = sx4+i*(bw4+gap4)
    rr(bx, y-bh4, bw4, bh4, r=8, fill=col)
    c.setFont("DMSans", 20); c.setFillColor(WHITE); c.drawCentredString(bx+bw4/2, y-bh4/2-7, txt)
    if i < 2: arr(bx+bw4+5, y-bh4/2, bx+bw4+gap4-5, y-bh4/2, NAVY)
c.setFont("Inter", 12); c.setFillColor(MUTED); c.drawCentredString(W/2, y-bh4-18, "When in doubt")
c.showPage()


# ═══════════════════════════════════════════════════════════
# PAGE 15 — SIGN-OFF
# ═══════════════════════════════════════════════════════════
new_page()
c.setFillColor(NAVY); c.rect(0, H-55, W, 55, fill=1, stroke=0)
c.setFillColor(WHITE); c.setFont("DMSans", 22)
c.drawCentredString(W/2, H-40, "I Have Read and Understand This Document")
draw_footer()

y = H - 100
c.setFont("Inter", 12); c.setFillColor(DARK)
for line in [
    "I have read this entire document from cover to cover.",
    "I understand the Owner's Top Ten \u2014 Operational Standards.",
    "I understand the Owner's Top Ten \u2014 Guest-Facing Standards.",
    "I understand the diet verification protocol.",
    "I understand the Zero Waste Food Loop.",
    "I understand the cleaning standards.",
    "I understand the education system.",
    "I understand I am not to modify exhibits, relocate animals, or use unapproved systems.",
    "I understand that workspaces are for work only.",
    "I understand the escalation process: correction, warning, disciplinary action.",
    "I had the opportunity to ask questions.",
    "I understand that if I am unsure about something, I will stop and ask before acting.",
]:
    c.drawString(MX+10, y, line); y -= 20

y -= 15; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y)
y -= 35; c.setFont("Inter", 12); c.setFillColor(DARK); c.setStrokeColor(MUTED); c.setLineWidth(0.5)
for label, offset in [("Employee Name (print):", 185), ("Employee Signature:", 170), ("Date:", 70)]:
    c.drawString(MX+10, y, label); c.line(MX+offset, y-2, W-MX-10, y-2); y -= 35
y -= 5; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y)
y -= 30; c.setStrokeColor(MUTED); c.setLineWidth(0.5)
for label, offset in [("Conducted By (print):", 180), ("Conductor Signature:", 175), ("Date:", 70)]:
    c.drawString(MX+10, y, label); c.line(MX+offset, y-2, W-MX-10, y-2); y -= 35
y -= 5; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y)
y -= 18; c.setFont("Inter", 9); c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "This document is retained by management. A copy may be provided to the employee upon request.")

c.save()
print(f"Built: {OUTPUT}")
print(f"Size: {Path(OUTPUT).stat().st_size:,} bytes")
print(f"Pages: {page_num[0]}")
