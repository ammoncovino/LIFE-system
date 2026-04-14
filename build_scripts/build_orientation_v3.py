#!/usr/bin/env python3
"""
STAFF ORIENTATION WALKTHROUGH v3 — Revised per Ammon's feedback:
- Remove redundancy (acrylic rule only once)
- Add exhibit integrity rule (no toys, no moving animals)
- Add workspace/office rule (not a hangout)
- Add software prohibition rule
- Tighter — meant to be read in one sitting as part of full reset package
"""

import urllib.request, math
from pathlib import Path
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
MX = inch
MW = W - 2 * inch
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STAFF_ORIENTATION_WALKTHROUGH.pdf"

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("Staff Orientation Walkthrough")
c.setAuthor("Perplexity Computer")

def draw_header_bar(title, font_size=26):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - 65, W, 65, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 68, W, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("DMSans", font_size)
    c.drawCentredString(W/2, H - 48, title)
    c.restoreState()

def draw_footer(page_num):
    c.saveState()
    c.setFont("Inter", 8)
    c.setFillColor(MUTED)
    c.drawCentredString(W/2, 22, f"Page {page_num}")
    c.restoreState()

def rounded_rect(x, y, w, h, r=6, fill=None, stroke=None, sw=1):
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    if fill: c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()

def circle_num(x, y, num, bg=NAVY, r=20):
    c.saveState()
    c.setFillColor(bg); c.circle(x, y, r, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("DMSans", 14); c.drawCentredString(x, y - 5, str(num))
    c.restoreState()

def x_mark(x, y, s=14):
    c.saveState(); c.setStrokeColor(RED); c.setLineWidth(3)
    c.line(x-s/2, y-s/2, x+s/2, y+s/2); c.line(x-s/2, y+s/2, x+s/2, y-s/2)
    c.restoreState()

def check_mark(x, y, s=14):
    c.saveState(); c.setStrokeColor(GREEN); c.setLineWidth(3)
    c.line(x-s/2, y, x-s/6, y-s/2); c.line(x-s/6, y-s/2, x+s/2, y+s/3)
    c.restoreState()

def arrow(x1, y1, x2, y2, color=NAVY):
    c.saveState(); c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(2)
    c.line(x1, y1, x2, y2)
    a = math.atan2(y2-y1, x2-x1); al = 8
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2-al*math.cos(a-0.4), y2-al*math.sin(a-0.4))
    p.lineTo(x2-al*math.cos(a+0.4), y2-al*math.sin(a+0.4))
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

def rule_box(x, y, w, h, text, fs=14):
    rounded_rect(x, y, w, h, r=6, fill=WARN_BG, stroke=RED, sw=2)
    c.saveState(); c.setFillColor(DARK_RED); c.setFont("DMSans", fs)
    tw = c.stringWidth(text, "DMSans", fs)
    if tw > w - 30:
        words = text.split(); mid = len(words) // 2
        c.drawCentredString(x+w/2, y+h/2+6, " ".join(words[:mid]))
        c.drawCentredString(x+w/2, y+h/2-14, " ".join(words[mid:]))
    else:
        c.drawCentredString(x+w/2, y+h/2-5, text)
    c.restoreState()

def navy_box(x, y, w, h, text, fs=14):
    rounded_rect(x, y, w, h, r=6, fill=NAVY)
    c.saveState(); c.setFillColor(WHITE); c.setFont("DMSans", fs)
    c.drawCentredString(x+w/2, y+h/2-5, text); c.restoreState()

from datetime import datetime

# ═══════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════
c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(TEAL); c.rect(0, H-8, W, 8, fill=1, stroke=0)
c.setFillColor(WHITE); c.setFont("DMSans", 42)
c.drawCentredString(W/2, H-220, "Staff"); c.drawCentredString(W/2, H-275, "Orientation")
c.setFillColor(YELLOW); c.rect(MX+60, H-310, MW-120, 3, fill=1, stroke=0)
c.setFillColor(HexColor("#B0B8D8")); c.setFont("Inter", 13)
c.drawCentredString(W/2, H-345, "San Antonio Aquarium")
c.drawCentredString(W/2, H-365, "Houston Interactive Aquarium & Animal Preserve")
c.setFillColor(HexColor("#8890B0")); c.setFont("Inter", 12)
c.drawCentredString(W/2, H-430, "Read together. Cover to cover. Sign at the end.")
cy = 220
c.setStrokeColor(HexColor("#4A5090")); c.setLineWidth(0.5)
c.setFillColor(HexColor("#9DA3C0")); c.setFont("Inter", 12)
c.drawString(MX+40, cy+40, "Date:"); c.line(MX+120, cy+38, W-MX-40, cy+38)
c.drawString(MX+40, cy, "Employee:"); c.line(MX+150, cy-2, W-MX-40, cy-2)
c.setFont("Inter", 9); c.setFillColor(HexColor("#6A70A0"))
c.drawCentredString(W/2, 50, f"Effective: {datetime.now().strftime('%B %Y')}  |  Owner: Ammon Covino")
draw_footer(1); c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 2 — HOW WE WORK HERE
# ═══════════════════════════════════════════════════════════
draw_header_bar("How We Work Here"); draw_footer(2)
y = H - 120
rules_p2 = [
    "If it is not assigned, written,\nor approved \u2014 do not do it.",
    "If you are not sure \u2014\nstop and ask.",
    "Every task has an owner.\nIf it is yours, own it.",
]
for i, text in enumerate(rules_p2):
    lines = text.split("\n")
    rounded_rect(MX, y-85, MW, 85, r=10, fill=LIGHT_BG, stroke=NAVY, sw=1.5)
    circle_num(MX+40, y-42, i+1)
    c.setFont("DMSans", 17); c.setFillColor(DARK)
    c.drawString(MX+75, y-32, lines[0])
    c.drawString(MX+75, y-54, lines[1])
    y -= 105
navy_box(MX, y-50, MW, 50, "This is not optional. This is how we operate.", 15)
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 3 — HOW TASKS WORK
# ═══════════════════════════════════════════════════════════
draw_header_bar("How Tasks Work"); draw_footer(3)
y = H - 120
bw, bh, gap = 115, 55, 20
tw = 4*bw + 3*gap; sx = (W-tw)/2
flow = [("A task", "is posted"), ("You claim it", '"I will take this"'), ("You do it", ""), ("It gets", "verified")]
for i, (l1, l2) in enumerate(flow):
    bx = sx + i*(bw+gap); by = y - bh
    rounded_rect(bx, by, bw, bh, r=6, fill=LIGHT_TEAL, stroke=TEAL, sw=1.5)
    c.setFont("DMSans", 12); c.setFillColor(DARK)
    if l2:
        c.drawCentredString(bx+bw/2, by+bh/2+4, l1)
        c.setFont("Inter", 9); c.setFillColor(MUTED)
        c.drawCentredString(bx+bw/2, by+bh/2-12, l2)
    else:
        c.drawCentredString(bx+bw/2, by+bh/2-4, l1)
    if i < 3: arrow(bx+bw+2, by+bh/2, bx+bw+gap-2, by+bh/2, NAVY)
y -= bh + 60
c.setFont("DMSans", 18); c.setFillColor(DARK)
c.drawCentredString(W/2, y, "If you don't claim it, it's not yours.")
y -= 35; c.setFillColor(RED); c.drawCentredString(W/2, y, "If nobody claims it, we have a problem.")
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 4 — ANIMAL CARE / DIET
# ═══════════════════════════════════════════════════════════
draw_header_bar("Animal Care Is Not Optional"); draw_footer(4)
y = H - 90
c.setFont("DMSans", 20); c.setFillColor(TEAL)
c.drawCentredString(W/2, y, "Diet Verification Protocol")
c.setStrokeColor(TEAL); c.setLineWidth(1.5); c.line(MX+60, y-8, W-MX-60, y-8)
y -= 40
steps = [("Prepare", "Use the written diet sheet. No substitutions."),
         ("Verify", "Confirm items and amounts."),
         ("Photograph", "Take a clear photo. Post with animal name, date, your initials."),
         ("Deliver", "Place food according to protocol.")]
for i, (label, desc) in enumerate(steps):
    by = y - 70
    rounded_rect(MX, by, MW, 65, r=8, fill=LIGHT_TEAL, stroke=TEAL, sw=1)
    circle_num(MX+35, by+32, i+1, TEAL, 18)
    c.setFont("DMSans", 15); c.setFillColor(DARK); c.drawString(MX+65, by+40, label)
    c.setFont("Inter", 11); c.setFillColor(MUTED); c.drawString(MX+65, by+18, desc)
    y = by - 8
y -= 5
rule_box(MX, y-55, MW, 50, "No guessing. No 'close enough.' No skipping photos.", 15)
y -= 70
c.setFont("Inter", 11); c.setFillColor(DARK)
c.drawString(MX+10, y, "\u2022  No animal fed to fullness before guest hours")
y -= 18; c.drawString(MX+10, y, "\u2022  Manager reviews all photos and responds \"Verified\"")
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 5 — ZERO WASTE FOOD LOOP
# ═══════════════════════════════════════════════════════════
draw_header_bar("Nothing Gets Thrown Away"); draw_footer(5)
y = H - 110
labels = ["Food", "Compost", "Bugs", "Chickens", "Eggs", "Animals"]
colors_list = [HexColor("#C8E6C9"), HexColor("#B2DFDB"), HexColor("#B2DFDB"),
               HexColor("#B2EBF2"), HexColor("#FFF9C4"), HexColor("#B3E5FC")]
bw2, gap2 = 78, 10; tw2 = 6*bw2+5*gap2; sx2 = (W-tw2)/2
for i, (lb, cl) in enumerate(zip(labels, colors_list)):
    bx = sx2 + i*(bw2+gap2)
    rounded_rect(bx, y-42, bw2, 42, r=6, fill=cl, stroke=TEAL, sw=1)
    c.setFont("DMSans", 12); c.setFillColor(DARK); c.drawCentredString(bx+bw2/2, y-25, lb)
    if i < 5: arrow(bx+bw2+2, y-21, bx+bw2+gap2-2, y-21, NAVY)
y -= 80
c.setFont("DMSans", 17); c.setFillColor(DARK)
c.drawCentredString(W/2, y, "ALL uneaten food goes in the collection bin.")
y -= 25; c.setFont("Inter", 13); c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "The outside aviary is the only exception.")
y -= 35; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
y -= 30; x_mark(MX+25, y, 18)
c.setFont("DMSans", 17); c.setFillColor(RED); c.drawString(MX+50, y-7, "DO NOT throw food in the trash.")
y -= 45; rule_box(MX, y-55, MW, 50, "If you are about to throw something away \u2014 STOP. You are breaking the system.", 13)
y -= 70
c.setFont("DMSans", 14); c.setFillColor(NAVY); c.drawString(MX, y, "How to Sort:")
y -= 25; c.setFont("Inter", 12); c.setFillColor(DARK)
for txt in ["\u2022  Compost bin: fruits, vegetables, grains, plant material",
            "\u2022  Controlled bin: meat, eggs, protein",
            "\u2022  Reject: plastic, trash, anything unknown \u2014 ASK if unsure"]:
    c.drawString(MX+10, y, txt); y -= 20
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 6 — HOW TO CLEAN (redundancy removed)
# ═══════════════════════════════════════════════════════════
draw_header_bar("How to Clean"); draw_footer(6)
y = H - 100
clean_items = [
    ("Acrylic windows", "Blue rags + distilled water ONLY. Nothing else."),
    ("Exhibits", "Virkon for disinfection. Follow the label."),
    ("Food prep areas", "Clean, sanitize, photo."),
    ("Water dishes", "Carbon filtered water where specified."),
]
for label, desc in clean_items:
    by = y - 70
    rounded_rect(MX, by, MW, 65, r=8, fill=LIGHT_TEAL, stroke=TEAL, sw=1)
    check_mark(MX+28, by+38, 16)
    c.setFont("DMSans", 16); c.setFillColor(DARK); c.drawString(MX+50, by+40, label)
    c.setFont("Inter", 12); c.setFillColor(MUTED); c.drawString(MX+50, by+16, desc)
    y = by - 12
y -= 5
rule_box(MX, y-55, MW, 50, "If you don't know the method, ASK. Do not guess.", 15)
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 7 — EDUCATION SYSTEM
# ═══════════════════════════════════════════════════════════
draw_header_bar("Education Is Always On"); draw_footer(7)
y = H - 100
navy_box(MX+40, y-45, MW-80, 40, "LIFE = Language, Intelligence, Form, Ecology", 15)
y -= 70
c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX, y, "This facility runs an education system. It is not a gimmick.")
y -= 22; c.drawString(MX, y, "Every sign, QR code, and exhibit teaches visitors something.")
y -= 35; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Your role:")
y -= 28
for item in ["Do not get in the way of the system.", "Do not make up facts about animals.",
             "Do not move, edit, or remove signs.", "Do not create your own materials.",
             "Do not tell visitors what to think."]:
    x_mark(MX+15, y+2, 12); c.setFont("Inter", 13); c.setFillColor(DARK)
    c.drawString(MX+40, y-3, item); y -= 28
y -= 10; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
y -= 25; c.setFont("DMSans", 14); c.setFillColor(GREEN)
c.drawString(MX, y, "If a guest asks something you don't know:")
y -= 28; c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX+20, y, '"That is a great question. Let me find someone')
y -= 20; c.drawString(MX+20, y, 'who can help, or scan the QR code for more."')
y -= 30; rule_box(MX, y-45, MW, 42, "All education content comes from central control. Not staff.", 13)
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 8 — EXHIBITS ARE LOCKED (NEW PAGE)
# ═══════════════════════════════════════════════════════════
draw_header_bar("Do Not Touch the Exhibits"); draw_footer(8)
y = H - 110
rule_box(MX, y-55, MW, 50, "Do not move, modify, or add anything to any exhibit.", 16)
y -= 80
c.setFont("DMSans", 15); c.setFillColor(NAVY); c.drawString(MX, y, "This means:")
y -= 30
exhibit_rules = [
    "Do not place toy animals inside exhibits.",
    "Do not relocate any animal from its assigned exhibit.",
    "Do not add decorations, objects, or personal items.",
    "Do not drill, paint, move barriers, or change lighting.",
    "Do not redesign layouts or exhibit flow.",
]
for item in exhibit_rules:
    x_mark(MX+15, y+2, 12); c.setFont("Inter", 13); c.setFillColor(DARK)
    c.drawString(MX+40, y-3, item); y -= 32
y -= 15; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
y -= 25; c.setFont("Inter", 13); c.setFillColor(DARK)
c.drawString(MX, y, "Exhibits are designed for biological and behavioral reasons")
y -= 20; c.drawString(MX, y, "you may not understand. That is fine. It is not your job to")
y -= 20; c.drawString(MX, y, "understand the design. It is your job to leave it alone.")
y -= 30
rounded_rect(MX, y-45, MW, 42, r=6, fill=GREEN_BG, stroke=GREEN, sw=1.5)
c.saveState(); c.setFillColor(GREEN); c.setFont("DMSans", 13)
c.drawCentredString(MX+MW/2, y-30, 'If something looks wrong, report it. Do not fix it yourself.'); c.restoreState()
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 9 — WORKSPACE + SOFTWARE + ESCALATION
# ═══════════════════════════════════════════════════════════
draw_header_bar("Workspaces and Systems", 24); draw_footer(9)
y = H - 100
# Office/workspace rule
c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Offices and Back Rooms")
y -= 25; c.setFont("Inter", 13); c.setFillColor(DARK)
for txt in ["Workspaces are for work. Not storage. Not socializing. Not sitting.",
            "If you are clocked in, you are working. There is no gray zone.",
            "Every desk, drawer, and cabinet must be clean and organized.",
            "If something is broken, report it. If something doesn't belong, remove it."]:
    c.drawString(MX+10, y, txt); y -= 20
y -= 15; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
# Software rule
y -= 20; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "Software and Systems")
y -= 25; c.setFont("Inter", 13); c.setFillColor(DARK)
for txt in ["Do not introduce, adopt, or use any software without owner approval.",
            "No tracking apps. No task management tools. No outside systems.",
            "If a vendor offers a tool, the answer is NO until the owner approves it.",
            "The only systems we use are the ones posted on these walls."]:
    c.drawString(MX+10, y, txt); y -= 20
y -= 15; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
# Escalation
y -= 20; c.setFont("DMSans", 16); c.setFillColor(NAVY); c.drawString(MX, y, "If You Make a Mistake")
y -= 30
strikes = [(HexColor("#FFC107"), "Strike 1", "Correction"), (HexColor("#FF9800"), "Strike 2", "Warning + retraining"),
           (HexColor("#D32F2F"), "Strike 3", "Disciplinary action")]
for color, label, desc in strikes:
    c.saveState(); c.setFillColor(color); c.circle(MX+30, y, 18, fill=1, stroke=0)
    num = label.split()[1]; c.setFillColor(WHITE); c.setFont("DMSans", 14); c.drawCentredString(MX+30, y-5, num)
    c.restoreState()
    c.setFont("DMSans", 14); c.setFillColor(DARK); c.drawString(MX+60, y+2, label)
    c.setFont("Inter", 11); c.setFillColor(MUTED); c.drawString(MX+60, y-14, desc)
    y -= 48
c.setFont("Inter", 12); c.setFillColor(DARK); c.drawCentredString(W/2, y, "This applies to everyone. Managers too.")
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 10 — DO NOT LIST (COMPREHENSIVE — NO REDUNDANCY)
# ═══════════════════════════════════════════════════════════
draw_header_bar("Do Not"); draw_footer(10)
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
    x_mark(MX+18, y, 14); c.setFont("Inter", 13); c.setFillColor(DARK)
    c.drawString(MX+48, y-5, item); y -= 36
y -= 5; c.setStrokeColor(HexColor("#D0D0D0")); c.setLineWidth(0.5); c.line(MX, y, W-MX, y)
y -= 30
# STOP → ASK → WAIT
bw3, bh3, gap3 = 120, 45, 30; tw3 = 3*bw3+2*gap3; sx3 = (W-tw3)/2
btns = [(RED, "STOP"), (HexColor("#FF9800"), "ASK"), (TEAL, "WAIT")]
for i, (col, txt) in enumerate(btns):
    bx = sx3 + i*(bw3+gap3)
    rounded_rect(bx, y-bh3, bw3, bh3, r=8, fill=col)
    c.setFont("DMSans", 20); c.setFillColor(WHITE); c.drawCentredString(bx+bw3/2, y-bh3/2-7, txt)
    if i < 2: arrow(bx+bw3+5, y-bh3/2, bx+bw3+gap3-5, y-bh3/2, NAVY)
c.setFont("Inter", 12); c.setFillColor(MUTED); c.drawCentredString(W/2, y-bh3-18, "When in doubt")
c.showPage()

# ═══════════════════════════════════════════════════════════
# PAGE 11 — SIGN-OFF
# ═══════════════════════════════════════════════════════════
c.setFillColor(NAVY); c.rect(0, H-55, W, 55, fill=1, stroke=0)
c.setFillColor(WHITE); c.setFont("DMSans", 24)
c.drawCentredString(W/2, H-40, "I Have Read and Understand This Document")
draw_footer(11)
y = H - 100
c.setFont("Inter", 13); c.setFillColor(DARK)
for line in [
    "My manager walked me through every page of this document.",
    "I understand the rules, the diet protocol, the food waste system,",
    "the cleaning standards, the education system, the exhibit rules,",
    "the workspace rules, and the documentation requirements.",
    "I understand that if I am unsure about something, I will stop",
    "and ask before acting.",
]: c.drawCentredString(W/2, y, line); y -= 22

y -= 15; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y)
y -= 35; c.setFont("Inter", 12); c.setFillColor(DARK)
c.setStrokeColor(MUTED); c.setLineWidth(0.5)
fields = [("Employee Name (print):", 185), ("Employee Signature:", 170), ("Date:", 70)]
for label, offset in fields:
    c.drawString(MX+10, y, label); c.line(MX+offset, y-2, W-MX-10, y-2); y -= 40
y -= 5; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y); y -= 35
c.setStrokeColor(MUTED); c.setLineWidth(0.5)
fields2 = [("Conducted By (print):", 180), ("Conductor Signature:", 175), ("Date:", 70)]
for label, offset in fields2:
    c.drawString(MX+10, y, label); c.line(MX+offset, y-2, W-MX-10, y-2); y -= 40
y -= 5; c.setStrokeColor(TEAL); c.setLineWidth(1); c.line(MX, y, W-MX, y); y -= 20
c.setFont("Inter", 10); c.setFillColor(MUTED)
c.drawCentredString(W/2, y, "This document is retained by management.")
y -= 14; c.drawCentredString(W/2, y, "A copy may be provided to the employee upon request.")

c.save()
print(f"Built: {OUTPUT}")
print(f"Size: {Path(OUTPUT).stat().st_size:,} bytes")
print(f"Pages: 11")
