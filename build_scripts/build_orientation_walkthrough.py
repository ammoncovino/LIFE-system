#!/usr/bin/env python3
"""
STAFF ORIENTATION WALKTHROUGH — 10-page print-ready PDF
For face-to-face walk-through with each staff member, child-grade simple.
Owner: Ammon Covino — San Antonio Aquarium / Houston Interactive Aquarium
"""

import urllib.request
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Fonts ──────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

fonts = {
    "DMSans": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "DMSans-Bold": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
}

# Download and register
for name, url in fonts.items():
    fpath = FONT_DIR / f"{name}.ttf"
    if not fpath.exists():
        urllib.request.urlretrieve(url, fpath)

# DM Sans variable font - register at different weights
pdfmetrics.registerFont(TTFont("DMSans", str(FONT_DIR / "DMSans.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Bold", str(FONT_DIR / "DMSans-Bold.ttf")))

# Use Inter for body
inter_url = "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
inter_path = FONT_DIR / "Inter.ttf"
if not inter_path.exists():
    urllib.request.urlretrieve(inter_url, inter_path)
pdfmetrics.registerFont(TTFont("Inter", str(inter_path)))

# ── Colors ─────────────────────────────────────────────────
# Using SA brand palette
NAVY = HexColor("#2C3481")
BLUE = HexColor("#29AAE2")
YELLOW = HexColor("#F9ED32")
CORAL = HexColor("#EF5A67")
DARK_TEXT = HexColor("#1A1A1A")
MUTED_TEXT = HexColor("#555555")
LIGHT_BG = HexColor("#F5F6FA")
WHITE = white
WARN_BG = HexColor("#FFF3CD")
WARN_BORDER = HexColor("#E8A817")
GREEN_BG = HexColor("#E8F5E9")
GREEN_ACCENT = HexColor("#2E7D32")

# ── Output ─────────────────────────────────────────────────
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STAFF_ORIENTATION_WALKTHROUGH.pdf"
W, H = letter

# ── Styles ─────────────────────────────────────────────────
cover_title = ParagraphStyle(
    "CoverTitle", fontName="DMSans-Bold", fontSize=32, leading=38,
    textColor=WHITE, alignment=TA_CENTER,
)
cover_sub = ParagraphStyle(
    "CoverSub", fontName="Inter", fontSize=14, leading=20,
    textColor=HexColor("#D0D4F0"), alignment=TA_CENTER,
)
page_title = ParagraphStyle(
    "PageTitle", fontName="DMSans-Bold", fontSize=22, leading=28,
    textColor=NAVY, spaceAfter=6,
)
section_head = ParagraphStyle(
    "SectionHead", fontName="DMSans-Bold", fontSize=14, leading=18,
    textColor=NAVY, spaceBefore=12, spaceAfter=4,
)
body = ParagraphStyle(
    "Body", fontName="Inter", fontSize=11, leading=16,
    textColor=DARK_TEXT, spaceAfter=6,
)
body_bold = ParagraphStyle(
    "BodyBold", fontName="DMSans-Bold", fontSize=11, leading=16,
    textColor=DARK_TEXT, spaceAfter=6,
)
bullet = ParagraphStyle(
    "Bullet", fontName="Inter", fontSize=11, leading=16,
    textColor=DARK_TEXT, leftIndent=20, bulletIndent=8,
    spaceAfter=4, bulletFontName="Inter",
)
big_rule = ParagraphStyle(
    "BigRule", fontName="DMSans-Bold", fontSize=13, leading=18,
    textColor=HexColor("#B71C1C"), spaceBefore=8, spaceAfter=4,
    borderColor=HexColor("#B71C1C"), borderWidth=0,
)
warn_box = ParagraphStyle(
    "WarnBox", fontName="DMSans-Bold", fontSize=12, leading=17,
    textColor=HexColor("#6D4C00"), spaceAfter=6,
    backColor=WARN_BG, borderPadding=8,
)
step_style = ParagraphStyle(
    "Step", fontName="Inter", fontSize=11, leading=16,
    textColor=DARK_TEXT, leftIndent=24, spaceAfter=4,
)
footer_style = ParagraphStyle(
    "Footer", fontName="Inter", fontSize=8, leading=10,
    textColor=MUTED_TEXT, alignment=TA_CENTER,
)
signoff_label = ParagraphStyle(
    "SignLabel", fontName="Inter", fontSize=11, leading=15,
    textColor=DARK_TEXT, spaceAfter=2,
)
signoff_line = ParagraphStyle(
    "SignLine", fontName="Inter", fontSize=11, leading=15,
    textColor=MUTED_TEXT, spaceAfter=14,
)
page_number_str = ParagraphStyle(
    "PageNum", fontName="Inter", fontSize=9, leading=12,
    textColor=MUTED_TEXT, alignment=TA_CENTER,
)
toc_style = ParagraphStyle(
    "TOC", fontName="Inter", fontSize=12, leading=18,
    textColor=DARK_TEXT, leftIndent=10, spaceAfter=4,
)

# ── Helper functions ───────────────────────────────────────
def colored_box(text, bg_color, text_color, font="DMSans-Bold", size=12):
    """Returns a table acting as a colored box with text."""
    s = ParagraphStyle("box", fontName=font, fontSize=size, leading=size+5,
                       textColor=text_color, alignment=TA_LEFT)
    p = Paragraph(text, s)
    t = Table([[p]], colWidths=[W - 2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    return t

def rule_box(text):
    """Red-bordered rule box for critical rules."""
    s = ParagraphStyle("rulebox", fontName="DMSans-Bold", fontSize=12, leading=17,
                       textColor=HexColor("#7B1A1A"), alignment=TA_LEFT)
    p = Paragraph(text, s)
    t = Table([[p]], colWidths=[W - 2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FDEDEF")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("BOX", (0, 0), (-1, -1), 1.5, HexColor("#C62828")),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    return t

def green_box(text):
    """Green box for positive/do-this items."""
    s = ParagraphStyle("greenbox", fontName="DMSans-Bold", fontSize=11, leading=16,
                       textColor=GREEN_ACCENT, alignment=TA_LEFT)
    p = Paragraph(text, s)
    t = Table([[p]], colWidths=[W - 2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREEN_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("BOX", (0, 0), (-1, -1), 1, GREEN_ACCENT),
        ("ROUNDEDCORNERS", [6, 6, 6, 6]),
    ]))
    return t

def numbered_step(number, text):
    """Numbered step with circle number."""
    s = ParagraphStyle("ns", fontName="Inter", fontSize=11, leading=16,
                       textColor=DARK_TEXT)
    return Paragraph(f'<font name="DMSans-Bold" color="#2C3481" size="13">{number}.</font>  {text}', s)

def make_divider():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor("#D0D4E8"),
                      spaceBefore=8, spaceAfter=8)

# ── Page templates ─────────────────────────────────────────
def cover_page(canvas_obj, doc):
    """Full navy cover page."""
    canvas_obj.saveState()
    # Full navy background
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, W, H, fill=1, stroke=0)
    # Accent bar at top
    canvas_obj.setFillColor(BLUE)
    canvas_obj.rect(0, H - 8, W, 8, fill=1, stroke=0)
    # Yellow accent line
    canvas_obj.setFillColor(YELLOW)
    canvas_obj.rect(inch, H/2 - 10, W - 2*inch, 3, fill=1, stroke=0)
    canvas_obj.restoreState()

def later_pages(canvas_obj, doc):
    """Header and footer for content pages."""
    canvas_obj.saveState()
    # Top bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, H - 28, W, 28, fill=1, stroke=0)
    canvas_obj.setFont("Inter", 8)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.drawString(inch, H - 20, "STAFF ORIENTATION WALKTHROUGH")
    canvas_obj.drawRightString(W - inch, H - 20, "San Antonio Aquarium / Houston Interactive Aquarium")
    # Bottom
    canvas_obj.setFont("Inter", 8)
    canvas_obj.setFillColor(MUTED_TEXT)
    canvas_obj.drawCentredString(W/2, 24, f"Page {doc.page}")
    canvas_obj.drawRightString(W - inch, 24, "CONFIDENTIAL — INTERNAL USE ONLY")
    canvas_obj.restoreState()

# ── Build document ─────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    title="Staff Orientation Walkthrough",
    author="Perplexity Computer",
    topMargin=0.6*inch + 28,  # account for header bar
    bottomMargin=0.6*inch,
    leftMargin=inch,
    rightMargin=inch,
)

story = []

# ═══════════════════════════════════════════════════════════
# PAGE 1 — COVER
# ═══════════════════════════════════════════════════════════
story.append(Spacer(1, 2.2*inch))
story.append(Paragraph("STAFF ORIENTATION<br/>WALKTHROUGH", cover_title))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(
    "San Antonio Aquarium&nbsp;&nbsp;|&nbsp;&nbsp;Houston Interactive Aquarium &amp; Animal Preserve",
    cover_sub
))
story.append(Spacer(1, 0.6*inch))
cover_body = ParagraphStyle("cb", fontName="Inter", fontSize=12, leading=18,
                            textColor=HexColor("#B0B8D8"), alignment=TA_CENTER)
story.append(Paragraph(
    "This document is walked through face-to-face with each staff member.<br/>"
    "Read each page together. Ask questions. Sign at the end.",
    cover_body
))
story.append(Spacer(1, 1.5*inch))
date_style = ParagraphStyle("ds", fontName="Inter", fontSize=10, leading=14,
                            textColor=HexColor("#8890B0"), alignment=TA_CENTER)
story.append(Paragraph(f"Effective: {datetime.now().strftime('%B %Y')}", date_style))
story.append(Paragraph("Owner: Ammon Covino", date_style))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 2 — TABLE OF CONTENTS
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("What We Will Cover", page_title))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph(
    "We are going to go through this together, page by page. "
    "Each section covers one part of how this place works. "
    "If you have a question, ask it right then.",
    body
))
story.append(Spacer(1, 0.15*inch))

toc_items = [
    ("1", "The One Rule", "The most important rule in this building"),
    ("2", "How Work Gets Done", "Claim system — how tasks are assigned and completed"),
    ("3", "Animal Care", "Diet verification, photos, and feeding rules"),
    ("4", "Cleaning Standards", "How we clean exhibits and public areas"),
    ("5", "Zero Waste Food Loop", "How uneaten food becomes animal feed"),
    ("6", "Education System", "What LIFE means and how it works here"),
    ("7", "Escalation", "What to do when something goes wrong"),
    ("8", "Your Sign-Off", "Read it, understood it, signed it"),
]

for num, title, desc in toc_items:
    toc_entry = ParagraphStyle("te", fontName="Inter", fontSize=11, leading=16,
                               textColor=DARK_TEXT, leftIndent=6, spaceAfter=2)
    toc_desc = ParagraphStyle("td", fontName="Inter", fontSize=10, leading=14,
                              textColor=MUTED_TEXT, leftIndent=30, spaceAfter=10)
    story.append(Paragraph(
        f'<font name="DMSans-Bold" color="#2C3481" size="14">{num}</font>'
        f'&nbsp;&nbsp;&nbsp;<font name="DMSans-Bold" size="12">{title}</font>',
        toc_entry
    ))
    story.append(Paragraph(desc, toc_desc))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 3 — THE ONE RULE
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("1. The One Rule", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(rule_box(
    "If it is not assigned, written, or approved — do not do it."
))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph(
    "This is the most important rule in the building. It applies to everyone, every day, "
    "every task. Before you do anything, ask yourself three questions:",
    body
))
story.append(Spacer(1, 0.1*inch))

story.append(colored_box(
    "1.&nbsp;&nbsp;Was it assigned to me?<br/>"
    "2.&nbsp;&nbsp;Is it written down?<br/>"
    "3.&nbsp;&nbsp;Was it approved?",
    LIGHT_BG, DARK_TEXT, "DMSans-Bold", 13
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "If the answer to all three is NO — stop. Do not act. Ask first.",
    body_bold
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("What this means in practice:", section_head))

examples = [
    ("You see something broken", "Do not fix it on your own. Report it. Wait for assignment."),
    ("You think a task should be done differently", "Do not change it. Raise it. Wait for approval."),
    ("A coworker asks you to do something", "If it is not on your assigned list, check with your manager first."),
    ("You are not sure", "Stop. Ask. Wait."),
]
for situation, action in examples:
    story.append(Paragraph(
        f'<font name="DMSans-Bold">{situation}:</font>  {action}', bullet
    ))

story.append(Spacer(1, 0.15*inch))
story.append(green_box(
    "Good habit: \"I was not sure, so I asked first.\""
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 4 — HOW WORK GETS DONE (CLAIM SYSTEM)
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("2. How Work Gets Done", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "We use a claim-based work system. Tasks are not just floating around hoping someone "
    "does them. Every task has a clear path:",
    body
))
story.append(Spacer(1, 0.1*inch))

# 4-step flow
steps_data = [
    ["POSTED", "CLAIMED", "DONE", "VERIFIED"],
    ["Task is posted\nby management", "You say:\n\"I will take this.\"", "You complete\nthe work", "Manager\nconfirms it"],
]
step_table = Table(steps_data, colWidths=[(W - 2*inch)/4]*4, rowHeights=[28, 50])
step_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("FONTNAME", (0, 0), (-1, 0), "DMSans-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 11),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("FONTNAME", (0, 1), (-1, 1), "Inter"),
    ("FONTSIZE", (0, 1), (-1, 1), 10),
    ("TEXTCOLOR", (0, 1), (-1, 1), DARK_TEXT),
    ("BACKGROUND", (0, 1), (-1, 1), LIGHT_BG),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D0D4E8")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(step_table)
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("How to claim a task:", section_head))
story.append(Paragraph(
    "When a task is available, you say out loud or in writing: "
    '<font name="DMSans-Bold" color="#2C3481">"I will take this assignment."</font>',
    body
))
story.append(Paragraph(
    "That means you own it. You are responsible for completing it and proving it was done.",
    body
))
story.append(Spacer(1, 0.1*inch))

story.append(rule_box(
    "If no one claims a task, it does not get done by accident. "
    "Unclaimed tasks are a system signal — they go back to management."
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("What counts as proof:", section_head))
story.append(Paragraph(
    "\u2022  Photos of completed work<br/>"
    "\u2022  Manager visual confirmation<br/>"
    "\u2022  Written verification",
    bullet
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 5 — ANIMAL CARE
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("3. Animal Care", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(rule_box(
    "Animal welfare overrides convenience. Always."
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Diet Verification — 4 Steps", section_head))
story.append(Spacer(1, 0.05*inch))

diet_steps = [
    ("PREPARE", "Use the written diet sheet. No substitutions. No guessing. No \"close enough.\""),
    ("VERIFY", "Check every item and quantity before feeding."),
    ("PHOTOGRAPH", "Take a clear photo — top-down, full plate visible, good lighting. "
                   "Post with: animal name, date, your initials."),
    ("DELIVER", "Place food according to protocol for that animal."),
]

for i, (label, desc) in enumerate(diet_steps):
    story.append(Paragraph(
        f'<font name="DMSans-Bold" color="#2C3481" size="13">{i+1}. {label}</font><br/>'
        f'{desc}',
        step_style
    ))
    story.append(Spacer(1, 0.04*inch))

story.append(Spacer(1, 0.1*inch))

story.append(rule_box(
    "No photo = not verified. If you skip the photo, the feeding is not complete."
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Critical Feeding Rules:", section_head))
story.append(Paragraph(
    "\u2022  No animal fed to fullness before guest hours<br/>"
    "\u2022  No substitutions — use the written diet sheet only<br/>"
    "\u2022  If something looks wrong: STOP. Do not feed. Ask immediately.<br/>"
    "\u2022  Manager reviews all diet photos daily and responds \"Verified\"",
    bullet
))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Manager Sign-Off:", section_head))
story.append(Paragraph(
    "Managers review all diet photos every day. They respond with "
    "\"Verified\" and their initials. No silent approvals — if a manager "
    "sees it, they confirm it in writing.",
    body
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 6 — CLEANING STANDARDS
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("4. Cleaning Standards", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Cleaning is not optional and it is not improvised. Every cleaning task has a specific method. "
    "Using the wrong materials damages the facility.",
    body
))
story.append(Spacer(1, 0.1*inch))

story.append(rule_box(
    "Acrylic windows — blue rags + distilled water ONLY. Nothing else. Ever."
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Core Standards:", section_head))

cleaning_rules = [
    ("Clean as you go", "Do not leave messes for later. Do not create \"temporary\" fixes."),
    ("Right materials, right surface", "Every surface has a specific cleaning method. If you do not know the method, ask before you clean."),
    ("No improvisation", "Do not use whatever product is nearby. If the correct supply is missing, report it — do not substitute."),
    ("Photo proof when assigned", "If a cleaning task is formally assigned, document completion with a photo."),
]

for title_text, desc in cleaning_rules:
    story.append(Paragraph(
        f'<font name="DMSans-Bold">{title_text}:</font>  {desc}', bullet
    ))
    story.append(Spacer(1, 0.03*inch))

story.append(Spacer(1, 0.15*inch))

# Quick reference box
clean_data = [
    [Paragraph('<font name="DMSans-Bold" color="white">Surface</font>', body),
     Paragraph('<font name="DMSans-Bold" color="white">Method</font>', body)],
    [Paragraph("Acrylic windows", body),
     Paragraph("Blue rags + distilled water ONLY", body)],
    [Paragraph("Glass surfaces", body),
     Paragraph("Glass cleaner + lint-free cloth", body)],
    [Paragraph("Floors (public areas)", body),
     Paragraph("Mop with approved solution", body)],
    [Paragraph("Exhibit surfaces", body),
     Paragraph("Check species-specific protocol — ASK if unsure", body)],
]
clean_table = Table(clean_data, colWidths=[2.2*inch, (W - 2*inch) - 2.2*inch])
clean_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
    ("BACKGROUND", (0, 1), (-1, -1), LIGHT_BG),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [LIGHT_BG, WHITE]),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D0D4E8")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(clean_table)
story.append(Spacer(1, 0.15*inch))

story.append(green_box(
    "When in doubt: ASK. Using the wrong cleaner can cause hundreds of dollars in damage."
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 7 — ZERO WASTE FOOD LOOP
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("5. Zero Waste Food Loop", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(colored_box(
    "Nothing is discarded. All organic material is converted into life through structured stages.",
    LIGHT_BG, NAVY, "DMSans-Bold", 12
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Uneaten food does not go in the trash. It follows a 7-stage loop that turns waste "
    "into animal feed. Here is how it works:",
    body
))
story.append(Spacer(1, 0.1*inch))

loop_data = [
    [Paragraph('<font name="DMSans-Bold" color="white">Stage</font>', body),
     Paragraph('<font name="DMSans-Bold" color="white">What Happens</font>', body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">1. Collect</font>', body),
     Paragraph("ALL uneaten food goes into ONE central bin", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">2. Sort</font>', body),
     Paragraph("Separate: compost (plants) / controlled (meat, protein) / reject (plastic, trash)", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">3. Compost</font>', body),
     Paragraph("Organic material breaks down with moisture + airflow", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">4. Insects</font>', body),
     Paragraph("Black soldier fly larvae convert compost into protein", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">5. Chickens</font>', body),
     Paragraph("Insects + barley sprouts feed the chickens", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">6. Eggs</font>', body),
     Paragraph("Chickens produce eggs (nutrient-dense)", body)],
    [Paragraph('<font name="DMSans-Bold" color="#2C3481">7. Animal Feed</font>', body),
     Paragraph("Eggs go back into the broader animal food system", body)],
]
loop_table = Table(loop_data, colWidths=[1.5*inch, (W - 2*inch) - 1.5*inch])
loop_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D0D4E8")),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(loop_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Your role in the loop:", section_head))
story.append(Paragraph(
    "\u2022  Collect uneaten food properly — no mixing with trash<br/>"
    "\u2022  Sort correctly — if you are not sure what category, ASK<br/>"
    "\u2022  Document with photos at every stage<br/>"
    "\u2022  Outside aviary is excluded from collection",
    bullet
))
story.append(Spacer(1, 0.1*inch))
story.append(rule_box(
    "Every action in this loop must have a named owner. "
    "You must verbally claim your assignment: \"I will take this.\""
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 8 — EDUCATION SYSTEM (LIFE)
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("6. Education System — LIFE", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(colored_box(
    "LIFE = Language, Intelligence, Form, Ecology",
    NAVY, WHITE, "DMSans-Bold", 14
))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "This facility runs an education system called LIFE. It is not a marketing gimmick. "
    "It is how we teach visitors about the animals. Here is what you need to know:",
    body
))
story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("Education is always on.", section_head))
story.append(Paragraph(
    "Every interaction a guest has — with you, with a sign, with an exhibit — is part of the "
    "education system. You do not need to be a teacher. You need to not get in the way of the system.",
    body
))

story.append(Paragraph("What the system does:", section_head))
story.append(Paragraph(
    "\u2022  Signs and QR codes give visitors information about animals<br/>"
    "\u2022  AI-powered tools let visitors ask questions and learn more<br/>"
    "\u2022  Everything is observation-based — we show how things work, not what to believe",
    bullet
))

story.append(Paragraph("What you should NOT do:", section_head))
story.append(Paragraph(
    "\u2022  Do not make up facts about animals — if you do not know, say \"I do not know\"<br/>"
    "\u2022  Do not remove, reposition, or edit signs without approval<br/>"
    "\u2022  Do not create your own educational materials<br/>"
    "\u2022  Do not tell visitors what to think or feel about animals",
    bullet
))
story.append(Spacer(1, 0.1*inch))

story.append(green_box(
    "Good response to a guest question you cannot answer:<br/>"
    "\"That is a great question. Let me find someone who can help, or you can "
    "scan the QR code at the exhibit for more information.\""
))
story.append(Spacer(1, 0.15*inch))

story.append(rule_box(
    "Staff do not create, edit, or rewrite any part of the education system. "
    "All content comes from central control."
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 9 — ESCALATION
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("7. Escalation — When Things Go Wrong", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "Things will go wrong. Animals get sick. Equipment breaks. Guests cause problems. "
    "The question is not whether something will happen — it is what you do when it does.",
    body
))
story.append(Spacer(1, 0.15*inch))

story.append(colored_box(
    "STOP&nbsp;&nbsp;&rarr;&nbsp;&nbsp;ASK&nbsp;&nbsp;&rarr;&nbsp;&nbsp;WAIT FOR INSTRUCTION",
    NAVY, WHITE, "DMSans-Bold", 16
))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("What this looks like:", section_head))

esc_items = [
    ("STOP", "Do not try to fix the problem yourself. Pause whatever you are doing."),
    ("ASK", "Tell your manager or the owner immediately. Describe exactly what you see."),
    ("WAIT", "Do not act until you receive instruction. Waiting is the correct action."),
]
for label, desc in esc_items:
    story.append(Paragraph(
        f'<font name="DMSans-Bold" color="#2C3481" size="13">{label}:</font>  {desc}',
        step_style
    ))
    story.append(Spacer(1, 0.04*inch))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Escalation Ladder:", section_head))

esc_data = [
    [Paragraph('<font name="DMSans-Bold" color="white">Level</font>', body),
     Paragraph('<font name="DMSans-Bold" color="white">What Happens</font>', body)],
    [Paragraph('<font name="DMSans-Bold">Strike 1</font>', body),
     Paragraph("Correction. You are told what was wrong and how to fix it.", body)],
    [Paragraph('<font name="DMSans-Bold">Strike 2</font>', body),
     Paragraph("Formal warning + retraining.", body)],
    [Paragraph('<font name="DMSans-Bold">Strike 3</font>', body),
     Paragraph("Disciplinary action.", body)],
]
esc_table = Table(esc_data, colWidths=[1.3*inch, (W - 2*inch) - 1.3*inch])
esc_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("BACKGROUND", (0, 1), (-1, 1), HexColor("#FFF9C4")),
    ("BACKGROUND", (0, 2), (-1, 2), HexColor("#FFE0B2")),
    ("BACKGROUND", (0, 3), (-1, 3), HexColor("#FFCDD2")),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#D0D4E8")),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(esc_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "This applies to everyone — staff and managers. The goal is to correct behavior, "
    "not to punish. But the rules exist because animal welfare depends on them.",
    body
))
story.append(Spacer(1, 0.1*inch))
story.append(green_box(
    "If you are uncertain about ANYTHING: Stop. Ask. Wait. "
    "That is always the right answer."
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════
# PAGE 10 — SIGN-OFF
# ═══════════════════════════════════════════════════════════
story.append(Paragraph("8. Your Sign-Off", page_title))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph(
    "You have now been walked through the core systems that run this facility. "
    "By signing below, you confirm:",
    body
))
story.append(Spacer(1, 0.15*inch))

confirms = [
    "I have been walked through this document page by page.",
    "I understand the authorization rule: if it is not assigned, written, or approved — do not do it.",
    "I understand the claim-based work system: tasks are posted, claimed, completed, and verified.",
    "I understand the diet verification protocol: prepare, verify, photograph, deliver.",
    "I understand the cleaning standards, including acrylic = blue rags + distilled water ONLY.",
    "I understand the Zero Waste Food Loop and my role in it.",
    "I understand the education system: I do not create, edit, or improvise educational content.",
    "I understand the escalation process: STOP, ASK, WAIT.",
    "I had the opportunity to ask questions during this walkthrough.",
]
for item in confirms:
    chk = ParagraphStyle("chk", fontName="Inter", fontSize=10.5, leading=15,
                         textColor=DARK_TEXT, leftIndent=24, bulletIndent=8,
                         spaceAfter=3)
    story.append(Paragraph(f"\u2610  {item}", chk))

story.append(Spacer(1, 0.35*inch))
story.append(make_divider())
story.append(Spacer(1, 0.1*inch))

# Signature fields
sig_fields = [
    ("Employee Name (Print):", "________________________________________"),
    ("Employee Signature:", "________________________________________"),
    ("Date:", "________________________________________"),
    ("", ""),
    ("Conducted By:", "________________________________________"),
    ("Conductor Signature:", "________________________________________"),
    ("Date:", "________________________________________"),
]

for label, line in sig_fields:
    if label == "" and line == "":
        story.append(Spacer(1, 0.2*inch))
        continue
    story.append(Paragraph(label, signoff_label))
    story.append(Paragraph(line, signoff_line))

# ── Build ──────────────────────────────────────────────────
doc.build(story, onFirstPage=cover_page, onLaterPages=later_pages)
print(f"Built: {OUTPUT}")
