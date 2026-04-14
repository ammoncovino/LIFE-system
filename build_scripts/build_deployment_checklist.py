"""
LIFE System Deployment Checklist PDF Generator
"""
from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Fonts ──────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
pdfmetrics.registerFont(TTFont("DMSans", str(FONT_DIR / "DMSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Bold", str(FONT_DIR / "DMSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-SemiBold", str(FONT_DIR / "DMSans-SemiBold.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Medium", str(FONT_DIR / "DMSans-Medium.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Italic", str(FONT_DIR / "DMSans-Italic.ttf")))

# ── Brand Colors ───────────────────────────────────────────────────
NAVY = HexColor("#2C3481")
LIGHT_BLUE = HexColor("#29AAE2")
YELLOW = HexColor("#F9ED32")
CORAL = HexColor("#EF5A67")
WHITE = white
BLACK = black
DARK_TEXT = HexColor("#1E1E2F")
LIGHT_BG = HexColor("#F4F6FB")
MID_GRAY = HexColor("#8B8FA3")
BORDER_GRAY = HexColor("#D0D3E0")
ROW_ALT = HexColor("#EFF1F8")

# ── Page setup ─────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
LEFT_MARGIN = 0.65 * inch
RIGHT_MARGIN = 0.65 * inch
TOP_MARGIN = 0.75 * inch
BOTTOM_MARGIN = 0.75 * inch
CONTENT_W = PAGE_W - LEFT_MARGIN - RIGHT_MARGIN

OUTPUT = "/home/user/workspace/LIFE_system/print_ready/DEPLOYMENT_CHECKLIST.pdf"

# ── Styles ─────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

sTitle = ParagraphStyle(
    "DocTitle", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=26, leading=31,
    textColor=NAVY, spaceAfter=4, alignment=TA_CENTER,
    tracking=1.5,
)
sSubtitle = ParagraphStyle(
    "DocSubtitle", parent=styles["Normal"],
    fontName="DMSans-Medium", fontSize=13, leading=17,
    textColor=LIGHT_BLUE, spaceAfter=6, alignment=TA_CENTER,
)
sSectionNum = ParagraphStyle(
    "SectionNum", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=9, leading=12,
    textColor=LIGHT_BLUE, spaceBefore=0, spaceAfter=0,
)
sSectionTitle = ParagraphStyle(
    "SectionTitle", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=16, leading=20,
    textColor=NAVY, spaceBefore=2, spaceAfter=4,
)
sSectionDesc = ParagraphStyle(
    "SectionDesc", parent=styles["Normal"],
    fontName="DMSans-Italic", fontSize=9.5, leading=13,
    textColor=MID_GRAY, spaceBefore=0, spaceAfter=10,
)
sBody = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="DMSans", fontSize=10, leading=14,
    textColor=DARK_TEXT, spaceAfter=6,
)
sBodyBold = ParagraphStyle(
    "BodyBold", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=10, leading=14,
    textColor=DARK_TEXT, spaceAfter=6,
)
sTableHeader = ParagraphStyle(
    "TH", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=8.5, leading=11,
    textColor=WHITE,
)
sTableCell = ParagraphStyle(
    "TC", parent=styles["Normal"],
    fontName="DMSans", fontSize=8.5, leading=12,
    textColor=DARK_TEXT,
)
sTableCellBold = ParagraphStyle(
    "TCB", parent=styles["Normal"],
    fontName="DMSans-SemiBold", fontSize=8.5, leading=12,
    textColor=DARK_TEXT,
)
sStepNum = ParagraphStyle(
    "StepNum", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=11, leading=14,
    textColor=LIGHT_BLUE, alignment=TA_CENTER,
)
sStepLabel = ParagraphStyle(
    "StepLabel", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=11, leading=15,
    textColor=NAVY,
)
sStepDesc = ParagraphStyle(
    "StepDesc", parent=styles["Normal"],
    fontName="DMSans", fontSize=9.5, leading=13,
    textColor=DARK_TEXT,
)
sAgendaNum = ParagraphStyle(
    "AgNum", parent=styles["Normal"],
    fontName="DMSans-Bold", fontSize=10, leading=14,
    textColor=CORAL, alignment=TA_CENTER,
)
sAgendaItem = ParagraphStyle(
    "AgItem", parent=styles["Normal"],
    fontName="DMSans", fontSize=10, leading=14,
    textColor=DARK_TEXT,
)
sDateField = ParagraphStyle(
    "DateField", parent=styles["Normal"],
    fontName="DMSans", fontSize=9, leading=12,
    textColor=MID_GRAY, alignment=TA_CENTER,
)
sQuote = ParagraphStyle(
    "Quote", parent=styles["Normal"],
    fontName="DMSans-SemiBold", fontSize=10, leading=14,
    textColor=NAVY, leftIndent=20, rightIndent=20,
    spaceBefore=4, spaceAfter=8,
)

# ── Helper: Section Header ─────────────────────────────────────────
def section_header(num, title, description=None):
    """Return flowables for a section header with accent bar."""
    elements = []
    elements.append(Spacer(1, 16))
    # Colored accent line
    elements.append(HRFlowable(
        width="100%", thickness=3, color=NAVY,
        spaceBefore=0, spaceAfter=6,
    ))
    elements.append(Paragraph(f"SECTION {num}", sSectionNum))
    elements.append(Paragraph(title, sSectionTitle))
    if description:
        elements.append(Paragraph(description, sSectionDesc))
    return elements


# ── Helper: Styled Table ───────────────────────────────────────────
def make_table(headers, rows, col_widths, first_col_bold=True):
    """Build a branded table with header row and alternating stripes."""
    header_row = [Paragraph(h, sTableHeader) for h in headers]
    data = [header_row]
    for row in rows:
        styled = []
        for i, cell in enumerate(row):
            st = sTableCellBold if (i == 0 and first_col_bold) else sTableCell
            styled.append(Paragraph(cell, st))
        data.append(styled)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "DMSans-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("GRID", (0, 0), (-1, 0), 0.5, NAVY),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 0.75, BORDER_GRAY),
        ("LINEBEFORE", (0, 1), (0, -1), 0.5, BORDER_GRAY),
        ("LINEAFTER", (-1, 1), (-1, -1), 0.5, BORDER_GRAY),
    ]
    # Alternating row colors
    for i in range(1, len(data)):
        bg = ROW_ALT if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    # Horizontal grid lines between body rows
    for i in range(1, len(data) - 1):
        style_cmds.append(("LINEBELOW", (0, i), (-1, i), 0.25, BORDER_GRAY))

    t.setStyle(TableStyle(style_cmds))
    return t


# ── Header / Footer ───────────────────────────────────────────────
def draw_header_footer(canvas_obj, doc):
    canvas_obj.saveState()

    # Top accent bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, PAGE_H - 18, PAGE_W, 18, fill=1, stroke=0)
    # Thin light-blue line beneath
    canvas_obj.setStrokeColor(LIGHT_BLUE)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(0, PAGE_H - 19.5, PAGE_W, PAGE_H - 19.5)

    # Footer line
    canvas_obj.setStrokeColor(BORDER_GRAY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(LEFT_MARGIN, 42, PAGE_W - RIGHT_MARGIN, 42)

    # Footer text
    canvas_obj.setFont("DMSans", 7.5)
    canvas_obj.setFillColor(MID_GRAY)
    canvas_obj.drawString(LEFT_MARGIN, 30,
                          "LIFE System — Canonical Deployment Guide")
    canvas_obj.drawRightString(PAGE_W - RIGHT_MARGIN, 30,
                               f"Page {doc.page}")

    # Date field at bottom center
    canvas_obj.drawCentredString(PAGE_W / 2, 30,
                                 f"Generated: {datetime.now().strftime('%B %d, %Y')}")

    canvas_obj.restoreState()


# ── Build Story ────────────────────────────────────────────────────
story = []

# ── TITLE BLOCK ────────────────────────────────────────────────────
story.append(Spacer(1, 0.65 * inch))

# Yellow accent line above title
story.append(HRFlowable(
    width="40%", thickness=4, color=YELLOW,
    spaceBefore=0, spaceAfter=12,
))
story.append(Paragraph("LIFE SYSTEM — DEPLOYMENT CHECKLIST", sTitle))
story.append(Spacer(1, 4))
story.append(Paragraph("Print, Post, and Distribute Guide", sSubtitle))
story.append(Spacer(1, 6))
story.append(HRFlowable(
    width="60%", thickness=1.5, color=LIGHT_BLUE,
    spaceBefore=0, spaceAfter=14,
))
# Brief intro
story.append(Paragraph(
    "This checklist tells you exactly what to print, how many copies, "
    "and where each document goes. Follow it top-to-bottom. "
    "Every item maps to a document that already exists in the LIFE System or "
    "is flagged for creation.",
    ParagraphStyle("Intro", parent=sBody, alignment=TA_CENTER, textColor=MID_GRAY,
                   fontSize=9.5, leading=13.5, leftIndent=30, rightIndent=30),
))
story.append(Spacer(1, 10))

# ═══════════════════════════════════════════════════════════════════
# SECTION 1
# ═══════════════════════════════════════════════════════════════════
story.extend(section_header(
    1,
    "DOCUMENTS ALREADY PRINT-READY",
    "These exist as finalized PDFs — print them exactly as-is. No edits, no improvisation."
))

sec1_headers = ["Document", "Copies Needed", "Distribution"]
sec1_rows = [
    ["Owner's Top Ten — Expanded (4 pp.)", "1 per manager",
     "Managers only — kept in manager binder"],
    ["Owner's Top Ten — Reduced (1 pp.)", "3–5",
     "Post in every back room, break room, office"],
    ["Manager Packet V1 (3 pp.)", "1 per manager",
     "Given directly to each manager, signed receipt"],
    ["Staff Packet V1 (2 pp.)", "1 per staff member",
     "Given at orientation or shift meeting"],
    ["Employee Packet V1 (2 pp.)", "1 per employee",
     "Given at hiring / onboarding"],
    ["Operational Spine V1 (~6 pp.)", "2 per location",
     "1 for office binder, 1 posted in manager area"],
    ["Exhibit Feeding Addendum — Batch 1", "1 per feeding station",
     "Posted at each relevant exhibit prep area"],
    ["Exhibit Feeding Addendum — Batch 2", "1 per feeding station",
     "Posted at each relevant exhibit prep area"],
    ["Exhibit Feeding Addendum — Batch 3", "1 per feeding station",
     "Posted at each relevant exhibit prep area"],
    ["Park-Wide Signage Replacement Map (8 pp.)", "2 per location",
     "1 for manager, 1 for signage execution team"],
    ["Branding Guidelines (2 pp.)", "1 per location",
     "Office reference — do not post publicly"],
]
sec1_widths = [CONTENT_W * 0.40, CONTENT_W * 0.18, CONTENT_W * 0.42]
story.append(make_table(sec1_headers, sec1_rows, sec1_widths))

# ═══════════════════════════════════════════════════════════════════
# SECTION 2
# ═══════════════════════════════════════════════════════════════════
sec2_header = section_header(
    2,
    "DOCUMENTS TO BE PRINTED & POSTED (SIGNS)",
    "These are physical signs for posting in the park. Laminate where indicated."
)

sec2_headers = ["Sign", "Size", "Copies", "Location"]
sec2_rows = [
    ['Back Room Authorization\n("STOP. If not assigned…")',
     "8.5×11 or 11×17", "Every back room door",
     "Back of every prep room, office, storage area"],
    ["Owner's Top Ten — Reduced",
     "8.5×11", "3–5 per location",
     "Break room, back hallway, manager office"],
    ["Diet Verification Reminder",
     "8.5×11", "1 per feeding station",
     "Posted at diet kitchen and each prep area"],
]
sec2_widths = [CONTENT_W * 0.30, CONTENT_W * 0.14, CONTENT_W * 0.20, CONTENT_W * 0.36]
sec2_table = make_table(sec2_headers, sec2_rows, sec2_widths)
story.append(KeepTogether(sec2_header + [sec2_table]))

# ═══════════════════════════════════════════════════════════════════
# SECTION 3
# ═══════════════════════════════════════════════════════════════════
story.extend(section_header(
    3,
    "DOCUMENTS NOT YET CREATED — NEEDS TO BE BUILT",
    "Referenced in the system but don't have final print versions yet. Track status here."
))

sec3_headers = ["Document", "Status", "What's Needed"]
sec3_rows = [
    ["Digital Totem signs (per species)",
     "Prototype exists (Red Ruffed Lemur)",
     "Complete for all species — image-only vertical graphic top, vinyl text box bottom"],
    ["Student Totem signs (K–5)",
     "Structure defined, content not finalized",
     "8-question format per species for public display"],
    ["Instructional signs (icon-based)",
     "Rules defined in Signage Map",
     "Graphic design execution — icons + short commands"],
    ["Commercial / Pricing signs",
     "Rules defined in Signage Map",
     "Standardized pricing vinyl designed"],
    ["Directional / Wayfinding signs",
     "Rules defined in Signage Map",
     "Icon-only vinyl or acrylic designed"],
    ["TV Content Loops",
     "Roles assigned per Operational Spine",
     "Content production (instruction, education, ambient)"],
    ["QR codes for narration suites",
     "Task defined, Kevin's payment page",
     "QR generation + physical sign installation"],
]
sec3_widths = [CONTENT_W * 0.28, CONTENT_W * 0.30, CONTENT_W * 0.42]
story.append(make_table(sec3_headers, sec3_rows, sec3_widths))

# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — Execution Order
# ═══════════════════════════════════════════════════════════════════
story.extend(section_header(
    4,
    "EXECUTION ORDER",
    "From Operational Spine §14. This is the correct sequence — do not skip steps."
))

steps = [
    ("1", "LANGUAGE FIRST",
     "All documents reviewed, approved, and finalized before any design work begins."),
    ("2", "GRAPHICS SECOND",
     "Signs, totems, and vinyl designed to brand spec — only after language is locked."),
    ("3", "PHYSICAL INSTALLATION THIRD",
     "Print, mount, and post all materials across every location."),
    ("4", "STAFF ORIENTATION LAST",
     "Hold a meeting to distribute packets and walk the entire system."),
]

step_data = []
for num, label, desc in steps:
    step_data.append([
        Paragraph(num, sStepNum),
        Paragraph(label, sStepLabel),
        Paragraph(desc, sStepDesc),
    ])

step_table = Table(step_data,
                   colWidths=[0.45 * inch, CONTENT_W * 0.30, CONTENT_W - 0.45 * inch - CONTENT_W * 0.30])
step_style = [
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("LEFTPADDING", (0, 0), (0, -1), 4),
    ("RIGHTPADDING", (-1, 0), (-1, -1), 4),
]
# Add a left accent bar to each row
for i in range(len(steps)):
    step_style.append(("LINEBELOW", (0, i), (-1, i), 0.5, BORDER_GRAY))
    step_style.append(("LINEBEFORE", (0, i), (0, i), 3, LIGHT_BLUE))
# Alternate background
for i in range(len(steps)):
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    step_style.append(("BACKGROUND", (0, i), (-1, i), bg))

step_table.setStyle(TableStyle(step_style))
story.append(step_table)

# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — Distribution Meeting Agenda
# ═══════════════════════════════════════════════════════════════════
story.extend(section_header(
    5,
    "DISTRIBUTION MEETING AGENDA",
    "When all materials are printed, hold one meeting per location. Follow this order exactly."
))

agenda_items = [
    "Hand out <b>Employee Packets</b> (all staff)",
    "Hand out <b>Staff Packets</b> (floor staff)",
    "Hand out <b>Manager Packets</b> (managers only — separate meeting or section)",
    "Walk the floor pointing to posted signs",
    "Review the <b>Owner's Top Ten — Reduced</b> (read aloud)",
    "Review escalation rule: <b>Pause \u2192 Ask \u2192 Escalate</b>",
    "Confirm every person has signed receipt of their packet",
    "State: <b>\u201cThese are locked. If you are unsure, ask. Do not improvise.\u201d</b>",
]

agenda_data = []
for i, item in enumerate(agenda_items, 1):
    agenda_data.append([
        Paragraph(str(i), sAgendaNum),
        Paragraph(item, sAgendaItem),
    ])

agenda_table = Table(agenda_data, colWidths=[0.4 * inch, CONTENT_W - 0.4 * inch])
a_style = [
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (0, -1), 6),
]
for i in range(len(agenda_items)):
    a_style.append(("LINEBELOW", (0, i), (-1, i), 0.25, BORDER_GRAY))
    bg = LIGHT_BG if i % 2 == 0 else WHITE
    a_style.append(("BACKGROUND", (0, i), (-1, i), bg))
# Left coral accent
for i in range(len(agenda_items)):
    a_style.append(("LINEBEFORE", (0, i), (0, i), 3, CORAL))

agenda_table.setStyle(TableStyle(a_style))
story.append(agenda_table)

story.append(Spacer(1, 16))

# Closing directive — boxed
closing_text = (
    '<b>"These are locked. If you are unsure, ask. Do not improvise."</b>'
)
closing_style = ParagraphStyle(
    "Closing", parent=sBody,
    fontName="DMSans-Bold", fontSize=11, leading=15,
    textColor=NAVY, alignment=TA_CENTER,
    spaceBefore=0, spaceAfter=0,
)
closing_para = Paragraph(closing_text, closing_style)

# Wrap in a small table with coral left border and yellow background
closing_table = Table([[closing_para]], colWidths=[CONTENT_W - 20])
closing_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FFF9E0")),
    ("LINEBEFORE", (0, 0), (0, 0), 4, CORAL),
    ("TOPPADDING", (0, 0), (-1, -1), 14),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ("LEFTPADDING", (0, 0), (-1, -1), 16),
    ("RIGHTPADDING", (0, 0), (-1, -1), 16),
    ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
]))
story.append(closing_table)

story.append(Spacer(1, 24))

# Date field
story.append(Paragraph(
    "Date: ____________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    "Location: ____________________&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    "Prepared by: ____________________",
    ParagraphStyle("Fields", parent=sBody, fontSize=9, leading=13,
                   textColor=MID_GRAY, alignment=TA_CENTER),
))

# ── Build PDF ──────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    title="LIFE System — Deployment Checklist",
    author="Perplexity Computer",
    leftMargin=LEFT_MARGIN,
    rightMargin=RIGHT_MARGIN,
    topMargin=TOP_MARGIN + 18,   # account for top bar
    bottomMargin=BOTTOM_MARGIN,
)
doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)

print(f"✓ PDF created: {OUTPUT}")
