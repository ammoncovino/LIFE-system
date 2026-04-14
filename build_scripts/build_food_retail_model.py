"""
Food & Retail Operator Model — Strategy Document PDF
Studio Giraffe / Zoo+Aquarium Campus, Houston
"""

import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.flowables import Flowable

# ── Colors ──────────────────────────────────────────────────────────────────
NAVY      = HexColor("#2C3481")
TEAL      = HexColor("#00AAAD")
TEAL_LITE = HexColor("#E6F7F7")
NAVY_LITE = HexColor("#EAEBF5")
GOLD      = HexColor("#D4A017")
TEXT      = HexColor("#1C1C1C")
MUTED     = HexColor("#555555")
BORDER    = HexColor("#C8C8C8")
BG_LIGHT  = HexColor("#F8F8F8")
WHITE     = white

# ── Fonts ────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

def download_font(url, filename):
    path = FONT_DIR / filename
    if not path.exists():
        urllib.request.urlretrieve(url, path)
    return str(path)

# DM Sans (clean, modern sans)
fonts = {
    "DMSans":       "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "DMSans-Bold":  "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
}

try:
    p_reg  = download_font(fonts["DMSans"],      "DMSans.ttf")
    p_bold = download_font(fonts["DMSans-Bold"], "DMSans-Bold.ttf")
    pdfmetrics.registerFont(TTFont("DMSans",      p_reg))
    pdfmetrics.registerFont(TTFont("DMSans-Bold", p_bold))
    BODY_FONT = "DMSans"
    HEAD_FONT = "DMSans-Bold"
except Exception:
    BODY_FONT = "Helvetica"
    HEAD_FONT = "Helvetica-Bold"

# ── Styles ────────────────────────────────────────────────────────────────────
ss = getSampleStyleSheet()

def S(name, parent="Normal", **kw):
    base = ss.get(parent, ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

style_h1 = S("H1",
    fontName=HEAD_FONT, fontSize=17, leading=22,
    textColor=NAVY, spaceAfter=4, spaceBefore=0)

style_h2 = S("H2",
    fontName=HEAD_FONT, fontSize=11, leading=15,
    textColor=NAVY, spaceAfter=3, spaceBefore=10)

style_h3 = S("H3",
    fontName=HEAD_FONT, fontSize=10, leading=13,
    textColor=TEAL, spaceAfter=2, spaceBefore=6)

style_body = S("Body",
    fontName=BODY_FONT, fontSize=9.5, leading=14,
    textColor=TEXT, spaceAfter=6)

style_body_sm = S("BodySm",
    fontName=BODY_FONT, fontSize=9, leading=13,
    textColor=TEXT, spaceAfter=4)

style_bullet = S("Bullet",
    fontName=BODY_FONT, fontSize=9.5, leading=14,
    textColor=TEXT, spaceAfter=3,
    leftIndent=14, bulletIndent=0,
    bulletText="•")

style_label = S("Label",
    fontName=HEAD_FONT, fontSize=8.5, leading=11,
    textColor=MUTED, spaceAfter=2)

style_callout = S("Callout",
    fontName=HEAD_FONT, fontSize=9.5, leading=14,
    textColor=NAVY, spaceAfter=4,
    leftIndent=10, rightIndent=10)

style_teal_box = S("TealBox",
    fontName=BODY_FONT, fontSize=9.5, leading=14,
    textColor=HexColor("#004E50"), spaceAfter=4,
    leftIndent=10, rightIndent=10)

style_footer = S("Footer",
    fontName=BODY_FONT, fontSize=7.5, leading=10,
    textColor=MUTED)

style_page_title = S("PageTitle",
    fontName=HEAD_FONT, fontSize=22, leading=28,
    textColor=WHITE, spaceAfter=0)

style_page_subtitle = S("PageSubtitle",
    fontName=BODY_FONT, fontSize=10, leading=14,
    textColor=HexColor("#D0E8F0"), spaceAfter=0)

style_option_title = S("OptionTitle",
    fontName=HEAD_FONT, fontSize=10.5, leading=14,
    textColor=WHITE, spaceAfter=0)

# ── Custom Flowables ──────────────────────────────────────────────────────────
class PageBanner(Flowable):
    """Full-width color banner for page headers."""
    def __init__(self, page_num, title, subtitle, w, accent=NAVY):
        super().__init__()
        self.page_num  = page_num
        self.title     = title
        self.subtitle  = subtitle
        self._w        = w
        self.accent    = accent
        self.height    = 64

    def wrap(self, availWidth, availHeight):
        return (self._w, self.height)

    def draw(self):
        c = self.canv
        w, h = self._w, self.height
        # Background
        c.setFillColor(self.accent)
        c.rect(0, 0, w, h, fill=1, stroke=0)
        # Page number tag
        tag_w = 36
        c.setFillColor(TEAL)
        c.rect(w - tag_w - 8, h//2 - 10, tag_w, 20, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(HEAD_FONT, 9)
        c.drawCentredString(w - tag_w//2 - 8, h//2 - 4, f"P{self.page_num}")
        # Title
        c.setFillColor(WHITE)
        c.setFont(HEAD_FONT, 16)
        c.drawString(16, h - 28, self.title)
        # Subtitle
        c.setFillColor(HexColor("#A0C8D0"))
        c.setFont(BODY_FONT, 8.5)
        c.drawString(16, h - 44, self.subtitle)
        # Bottom teal strip
        c.setFillColor(TEAL)
        c.rect(0, 0, w, 4, fill=1, stroke=0)


class ColorBox(Flowable):
    """Colored box with label + value for KPI-style cells."""
    def __init__(self, label, value, bg=NAVY_LITE, text_color=NAVY, w=120, h=48):
        super().__init__()
        self.label      = label
        self.value      = value
        self.bg         = bg
        self.text_color = text_color
        self._w = w
        self._h = h

    def wrap(self, availWidth, availHeight):
        return (self._w, self._h)

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.roundRect(0, 0, self._w, self._h, 4, fill=1, stroke=0)
        c.setFillColor(self.text_color)
        c.setFont(HEAD_FONT, 13)
        c.drawCentredString(self._w / 2, self._h - 22, self.value)
        c.setFillColor(MUTED)
        c.setFont(BODY_FONT, 7.5)
        c.drawCentredString(self._w / 2, 8, self.label)


class SectionDivider(Flowable):
    """Thin teal rule with label."""
    def __init__(self, label, w):
        super().__init__()
        self.label = label
        self._w    = w

    def wrap(self, availWidth, availHeight):
        return (self._w, 16)

    def draw(self):
        c = self.canv
        c.setFillColor(TEAL)
        c.rect(0, 7, self._w, 2, fill=1, stroke=0)
        c.setFillColor(WHITE)
        lw = len(self.label) * 5.5 + 12
        c.rect(6, 2, lw, 12, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.setFont(HEAD_FONT, 8)
        c.drawString(12, 4, self.label)


def callout_box(text, bg=TEAL_LITE, border=TEAL, style=None):
    """Returns a 1-cell table styled as a callout box."""
    if style is None:
        style = style_teal_box
    t = Table([[Paragraph(text, style)]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), bg),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LINEBEFORE",   (0,0), (0,-1),  3, border),
        ("ROWBACKGROUNDS",(0,0),(-1,-1), [bg]),
    ]))
    return t


def navy_callout(text):
    return callout_box(
        text, bg=NAVY_LITE, border=NAVY,
        style=S("NC", fontName=HEAD_FONT, fontSize=9.5, leading=14, textColor=NAVY,
                leftIndent=0, rightIndent=0)
    )


def option_header(letter_tag, title, tag_label, bg=NAVY):
    """Colored option header row for options table."""
    cell_letter = Paragraph(
        f'<font color="white"><b>{letter_tag}</b></font>',
        S("OL", fontName=HEAD_FONT, fontSize=14, leading=18, textColor=WHITE))
    cell_title = Paragraph(
        f'<font color="white"><b>{title}</b></font>',
        S("OT", fontName=HEAD_FONT, fontSize=11, leading=14, textColor=WHITE))
    cell_tag = Paragraph(
        f'<font color="white">{tag_label}</font>',
        S("OG", fontName=BODY_FONT, fontSize=8.5, leading=11, textColor=HexColor("#A0E0E2")))
    return Table(
        [[cell_letter, [cell_title, cell_tag]]],
        colWidths=[32, "*"]
    ), bg


# ─────────────────────────────────────────────────────────────────────────────
# Document build
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/FOOD_RETAIL_OPERATOR_MODEL.pdf"
PAGE_W, PAGE_H = letter
MARGIN = 0.65 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=0.5 * inch,
    bottomMargin=0.55 * inch,
    title="Food & Retail Operator Model — Strategy Document",
    author="Perplexity Computer",
)

story = []

# ═══════════════════════════════════════════════════════════════
# PAGE 1: Current Operations Assessment
# ═══════════════════════════════════════════════════════════════

story.append(PageBanner(1,
    "Current Operations Assessment",
    "Studio Giraffe · Zoo / Aquarium + Entertainment Campus · Houston, TX",
    CONTENT_W, NAVY))
story.append(Spacer(1, 10))

# KPI row
kpi_data = [
    [ColorBox("Annual Visitors",    "300,000",     NAVY_LITE,  NAVY,   w=118, h=52),
     ColorBox("Parking Capacity",   "600–700 cars", NAVY_LITE, NAVY,   w=118, h=52),
     ColorBox("Narration Suites",   "20 @ $300/nt", TEAL_LITE, HexColor("#004E50"), w=118, h=52),
     ColorBox("Annual Events",      "40–60",        TEAL_LITE, HexColor("#004E50"), w=118, h=52)],
]
kpi_table = Table(kpi_data, colWidths=[118, 118, 118, 118])
kpi_table.setStyle(TableStyle([
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 4),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4),
]))
story.append(kpi_table)
story.append(Spacer(1, 10))

# ── Section A ──
story.append(SectionDivider("A.  FOOD & RETAIL OPERATIONS OVERVIEW", CONTENT_W))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Studio Giraffe currently operates all food and beverage services in-house across two "
    "channels: a permanent indoor food facility and an on-site food truck. Alcohol sales are "
    "managed entirely by venue staff and are integrated into event packages, general admission "
    "experiences, and lodging revenue. Retail merchandise is sold through the main guest services "
    "counter. There is no third-party food operator currently involved.",
    style_body))

ops_data = [
    [Paragraph("<b>Channel</b>",       style_label),
     Paragraph("<b>Type</b>",          style_label),
     Paragraph("<b>Managed By</b>",    style_label),
     Paragraph("<b>Alcohol?</b>",      style_label)],
    [Paragraph("Indoor Food Facility", style_body_sm),
     Paragraph("Permanent",           style_body_sm),
     Paragraph("Venue Staff",         style_body_sm),
     Paragraph("Yes — internal",      style_body_sm)],
    [Paragraph("On-Site Food Truck",   style_body_sm),
     Paragraph("Mobile / Seasonal",   style_body_sm),
     Paragraph("Venue Staff",         style_body_sm),
     Paragraph("Limited",             style_body_sm)],
    [Paragraph("Retail Merchandise",   style_body_sm),
     Paragraph("Counter Sales",       style_body_sm),
     Paragraph("Venue Staff",         style_body_sm),
     Paragraph("N/A",                 style_body_sm)],
]
ops_table = Table(ops_data, colWidths=[160, 110, 120, 90])
ops_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("FONTNAME",      (0,0), (-1,0), HEAD_FONT),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
]))
story.append(ops_table)
story.append(Spacer(1, 10))

# ── Section B ──
story.append(SectionDivider("B.  PAIN POINTS — OPERATIONAL DISTRACTION", CONTENT_W))
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Self-operating food services creates recurring strain across three dimensions that compete "
    "directly with the venue's core mission of guest experience, animal care, and event quality:",
    style_body))

pain_items = [
    ("<b>Staffing Burden</b>",
     "Food/beverage positions require specialized scheduling, training, and retention — effort "
     "diverted from venue operations, animal programs, and event coordination."),
    ("<b>Operational Complexity</b>",
     "Inventory management, supplier relationships, food safety compliance, equipment maintenance, "
     "and health inspections demand dedicated management bandwidth."),
    ("<b>Revenue Inconsistency</b>",
     "Without a professional operator, food sales underperform during peak periods. Untrained "
     "staff leaves revenue on the table — particularly in upsell, alcohol, and event catering."),
    ("<b>Capital Exposure</b>",
     "Venue absorbs all food COGS, waste, and equipment investment risk — with no guaranteed "
     "fixed revenue floor from a tenant or operator."),
]
for title, body in pain_items:
    row_data = [[
        Paragraph(title, S("PT", fontName=HEAD_FONT, fontSize=9.5, leading=13,
                            textColor=NAVY, leftIndent=0)),
        Paragraph(body,  style_body_sm),
    ]]
    row_t = Table(row_data, colWidths=[130, CONTENT_W - 130])
    row_t.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LINEABOVE",     (0,0), (-1,0),  0.4, BORDER),
    ]))
    story.append(row_t)
story.append(Spacer(1, 10))

# ── Section C ──
story.append(SectionDivider("C.  REVENUE BASELINE FRAMEWORK", CONTENT_W))
story.append(Spacer(1, 6))
rev_data = [
    [Paragraph("<b>Revenue Stream</b>", style_label),
     Paragraph("<b>Current Model</b>",   style_label),
     Paragraph("<b>Annual Baseline</b>", style_label),
     Paragraph("<b>Operator Impact</b>", style_label)],
    [Paragraph("Tickets",               style_body_sm),
     Paragraph("Venue-direct",          style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("None — unaffected",     style_body_sm)],
    [Paragraph("Food & Beverage",        style_body_sm),
     Paragraph("In-house",              style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("Shift to operator model",style_body_sm)],
    [Paragraph("Alcohol",               style_body_sm),
     Paragraph("Venue-controlled",      style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("Retained 100% by venue",style_body_sm)],
    [Paragraph("Parking",               style_body_sm),
     Paragraph("Venue-direct",          style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("None — unaffected",     style_body_sm)],
    [Paragraph("Lodging (20 suites)",   style_body_sm),
     Paragraph("Venue-direct",          style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("None — unaffected",     style_body_sm)],
    [Paragraph("Events (40–60/yr)",     style_body_sm),
     Paragraph("Venue-direct",          style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("Operator may cater",    style_body_sm)],
    [Paragraph("Vendors / Sponsorships",style_body_sm),
     Paragraph("Venue-direct",          style_body_sm),
     Paragraph("$____________",         style_body_sm),
     Paragraph("None — unaffected",     style_body_sm)],
]
rev_table = Table(rev_data, colWidths=[130, 100, 110, 140])
rev_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    # Highlight alcohol row
    ("BACKGROUND",    (0,3), (-1,3), HexColor("#FFFBE6")),
    ("TEXTCOLOR",     (3,3), (3,3),  HexColor("#004E50")),
    ("FONTNAME",      (0,3), (-1,3), HEAD_FONT),
]))
story.append(rev_table)
story.append(Spacer(1, 10))

# ── Goal box ──
story.append(callout_box(
    "<b>Strategic Goal:</b>  Professionalize food & beverage operations through a structured "
    "third-party operator model — reducing venue staffing burden and operational distraction "
    "while retaining brand identity, alcohol control, pricing authority, and all core "
    "revenue streams. The venue remains the operator of record; a partner handles execution.",
    TEAL_LITE, TEAL))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# PAGE 2: Operator Model Options
# ═══════════════════════════════════════════════════════════════

story.append(PageBanner(2,
    "Operator Model Options",
    "Evaluating three structural approaches for third-party concession engagement",
    CONTENT_W, NAVY))
story.append(Spacer(1, 10))

story.append(Paragraph(
    "Three operator models are presented below. Each reflects a different balance of revenue "
    "sharing, operational complexity, and venue control. The recommended model (Option A) "
    "provides the strongest combination of professional execution and owner control.",
    style_body))
story.append(Spacer(1, 6))

# ── Option A ──────────────────────────────────────────────────
opt_a_header = Table(
    [[Paragraph('<font color="white"><b>A</b></font>',
                S("OL2", fontName=HEAD_FONT, fontSize=16, leading=20, textColor=WHITE)),
      Paragraph('<font color="white"><b>Managed Concession</b></font><br/>'
                '<font color="#A0E0E2">Recommended — Strongest control + professional execution</font>',
                S("OT2", fontName=HEAD_FONT, fontSize=11, leading=14, textColor=WHITE))]],
    colWidths=[36, CONTENT_W - 36]
)
opt_a_header.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(opt_a_header)

opt_a_rows = [
    [Paragraph("<b>Venue provides:</b>",   style_label),
     Paragraph("Space, utilities, brand guidelines, menu framework, alcohol service",
               style_body_sm)],
    [Paragraph("<b>Operator provides:</b>", style_label),
     Paragraph("Staffing, food production, inventory management, supplier relationships, "
               "equipment maintenance, health compliance", style_body_sm)],
    [Paragraph("<b>Revenue model:</b>",    style_label),
     Paragraph("Base rent (fixed monthly) + <b>10–20% of gross food/beverage sales</b> "
               "to venue", style_body_sm)],
    [Paragraph("<b>Venue retains:</b>",    style_label),
     Paragraph("<b>100% alcohol control · Brand approval · Menu approval · Pricing authority · "
               "Event catering rights</b>", style_body_sm)],
    [Paragraph("<b>Best for:</b>",         style_label),
     Paragraph("Operators with existing F&B track record; venues with defined brand standards "
               "and strong repeat visitor base", style_body_sm)],
]
opt_a_body = Table(opt_a_rows, colWidths=[120, CONTENT_W - 120])
opt_a_body.setStyle(TableStyle([
    ("ROWBACKGROUNDS",  (0,0), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",            (0,0), (-1,-1), 0.4, BORDER),
    ("TOPPADDING",      (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",   (0,0), (-1,-1), 5),
    ("LEFTPADDING",     (0,0), (-1,-1), 8),
    ("VALIGN",          (0,0), (-1,-1), "TOP"),
    # Highlight the "venue retains" row
    ("BACKGROUND",      (0,3), (-1,3), HexColor("#FFFBE6")),
]))
story.append(opt_a_body)
story.append(Spacer(1, 10))

# ── Option B ──────────────────────────────────────────────────
opt_b_header = Table(
    [[Paragraph('<font color="white"><b>B</b></font>',
                S("OL3", fontName=HEAD_FONT, fontSize=16, leading=20, textColor=WHITE)),
      Paragraph('<font color="white"><b>Revenue Share Only</b></font><br/>'
                '<font color="#A0CBCF">Lower base rent / higher revenue share — ideal for operator testing</font>',
                S("OT3", fontName=HEAD_FONT, fontSize=11, leading=14, textColor=WHITE))]],
    colWidths=[36, CONTENT_W - 36]
)
opt_b_header.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), HexColor("#3B4A9A")),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(opt_b_header)

opt_b_rows = [
    [Paragraph("<b>Structure:</b>",         style_label),
     Paragraph("Minimal or no base rent; venue takes higher percentage of gross sales "
               "(typically 20–30%)", style_body_sm)],
    [Paragraph("<b>Benefit:</b>",           style_label),
     Paragraph("Lower commitment barrier attracts quality operators. Venue revenue scales "
               "directly with operator performance — aligns incentives", style_body_sm)],
    [Paragraph("<b>Risk:</b>",              style_label),
     Paragraph("No guaranteed floor revenue. If operator underperforms or foot traffic is "
               "seasonal, venue earns less than a fixed-rent structure", style_body_sm)],
    [Paragraph("<b>Best use case:</b>",     style_label),
     Paragraph("6-month trial period to test a new operator before committing to base rent. "
               "Transition to Option A once performance is verified", style_body_sm)],
    [Paragraph("<b>Venue still retains:</b>", style_label),
     Paragraph("Alcohol, brand, menu approval, pricing — same protections as Option A",
               style_body_sm)],
]
opt_b_body = Table(opt_b_rows, colWidths=[120, CONTENT_W - 120])
opt_b_body.setStyle(TableStyle([
    ("ROWBACKGROUNDS",  (0,0), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",            (0,0), (-1,-1), 0.4, BORDER),
    ("TOPPADDING",      (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",   (0,0), (-1,-1), 5),
    ("LEFTPADDING",     (0,0), (-1,-1), 8),
    ("VALIGN",          (0,0), (-1,-1), "TOP"),
]))
story.append(opt_b_body)
story.append(Spacer(1, 10))

# ── Option C ──────────────────────────────────────────────────
opt_c_header = Table(
    [[Paragraph('<font color="white"><b>C</b></font>',
                S("OL4", fontName=HEAD_FONT, fontSize=16, leading=20, textColor=WHITE)),
      Paragraph('<font color="white"><b>Multi-Vendor Food Court</b></font><br/>'
                '<font color="#A0CBCF">Multiple specialty operators in distinct venue zones</font>',
                S("OT4", fontName=HEAD_FONT, fontSize=11, leading=14, textColor=WHITE))]],
    colWidths=[36, CONTENT_W - 36]
)
opt_c_header.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), HexColor("#1E2A6E")),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("TOPPADDING",    (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
]))
story.append(opt_c_header)

opt_c_rows = [
    [Paragraph("<b>Structure:</b>",    style_label),
     Paragraph("2–4 specialty food vendors assigned to specific venue zones (e.g., main plaza, "
               "event terrace, truck pad). Each signs separate agreements", style_body_sm)],
    [Paragraph("<b>Benefit:</b>",      style_label),
     Paragraph("Greater menu variety; vendors compete for best performance; redundancy if "
               "one vendor exits. Allows food to match each zone's experience theme",
               style_body_sm)],
    [Paragraph("<b>Risk:</b>",         style_label),
     Paragraph("Significantly higher management complexity — multiple contracts, multiple "
               "insurance relationships, coordination burden, consistency challenges across zones",
               style_body_sm)],
    [Paragraph("<b>Recommendation:</b>", style_label),
     Paragraph("<b>Not recommended for initial implementation.</b> Consider only after Option A "
               "or B is proven and venue has management capacity to oversee multiple operators",
               style_body_sm)],
]
opt_c_body = Table(opt_c_rows, colWidths=[120, CONTENT_W - 120])
opt_c_body.setStyle(TableStyle([
    ("ROWBACKGROUNDS",  (0,0), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",            (0,0), (-1,-1), 0.4, BORDER),
    ("TOPPADDING",      (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",   (0,0), (-1,-1), 5),
    ("LEFTPADDING",     (0,0), (-1,-1), 8),
    ("VALIGN",          (0,0), (-1,-1), "TOP"),
]))
story.append(opt_c_body)
story.append(Spacer(1, 10))

# Summary comparison
story.append(Paragraph("Quick Comparison", style_h2))
comp_data = [
    [Paragraph("<b>Factor</b>",            style_label),
     Paragraph("<b>Option A</b>",          style_label),
     Paragraph("<b>Option B</b>",          style_label),
     Paragraph("<b>Option C</b>",          style_label)],
    [Paragraph("Revenue Predictability",   style_body_sm),
     Paragraph("High (base + %)",          style_body_sm),
     Paragraph("Variable (% only)",        style_body_sm),
     Paragraph("Medium (multiple %s)",     style_body_sm)],
    [Paragraph("Management Burden",        style_body_sm),
     Paragraph("Low",                      style_body_sm),
     Paragraph("Low",                      style_body_sm),
     Paragraph("High",                     style_body_sm)],
    [Paragraph("Alcohol Control",          style_body_sm),
     Paragraph("100% Venue",               style_body_sm),
     Paragraph("100% Venue",               style_body_sm),
     Paragraph("100% Venue",               style_body_sm)],
    [Paragraph("Brand Control",            style_body_sm),
     Paragraph("Full",                     style_body_sm),
     Paragraph("Full",                     style_body_sm),
     Paragraph("Harder to enforce",        style_body_sm)],
    [Paragraph("Recommended Phase",        style_body_sm),
     Paragraph("Post-trial / Long-term",   style_body_sm),
     Paragraph("Trial phase",              style_body_sm),
     Paragraph("Phase 3 only",             style_body_sm)],
]
comp_table = Table(comp_data, colWidths=[130, 115, 115, 120])
comp_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("BACKGROUND",    (1,1), (1,-1), HexColor("#F0FFF0")),
]))
story.append(comp_table)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# PAGE 3: Deal Structure Framework
# ═══════════════════════════════════════════════════════════════

story.append(PageBanner(3,
    "Deal Structure Framework",
    "Non-negotiable terms, financial structure, and contractual protections",
    CONTENT_W, NAVY))
story.append(Spacer(1, 10))

story.append(navy_callout(
    "Owner's Rules:  Never give away alcohol control.  Never bundle multiple revenue streams "
    "in a single deal.  Operational control remains with the venue at all times."))
story.append(Spacer(1, 8))

# Financial terms
story.append(SectionDivider("1.  FINANCIAL TERMS", CONTENT_W))
story.append(Spacer(1, 6))
fin_data = [
    [Paragraph("<b>Term</b>",          style_label),
     Paragraph("<b>Structure</b>",     style_label),
     Paragraph("<b>Notes</b>",         style_label)],
    [Paragraph("Base Rent",            style_body_sm),
     Paragraph("$_______ / month",     style_body_sm),
     Paragraph("Fixed floor — provides guaranteed revenue regardless of operator sales volume",
               style_body_sm)],
    [Paragraph("Revenue Share",        style_body_sm),
     Paragraph("10–20% of gross food & non-alcohol beverage sales", style_body_sm),
     Paragraph("Gross = before operator's COGS deduction. Venue defines calculation method in contract",
               style_body_sm)],
    [Paragraph("Alcohol Revenue",      style_body_sm),
     Paragraph("100% retained by venue", style_body_sm),
     Paragraph("<b>Non-negotiable. Operator has zero alcohol revenue participation.</b> "
               "Venue employs or designates alcohol service staff",
               style_body_sm)],
    [Paragraph("Event Catering",       style_body_sm),
     Paragraph("Optional add-on at venue discretion", style_body_sm),
     Paragraph("Venue may assign operator to cater events at a negotiated per-event rate. "
               "Venue retains right to use alternative caterers", style_body_sm)],
    [Paragraph("Reporting",            style_body_sm),
     Paragraph("Monthly POS reports due by 10th of following month", style_body_sm),
     Paragraph("Venue has right to audit sales records at any time with 5-business-day notice",
               style_body_sm)],
]
fin_table = Table(fin_data, colWidths=[100, 155, CONTENT_W - 255])
fin_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ("BACKGROUND",    (0,3), (-1,3), HexColor("#FFFBE6")),
    ("FONTNAME",      (1,3), (1,3),  HEAD_FONT),
]))
story.append(fin_table)
story.append(Spacer(1, 10))

# Contract terms
story.append(SectionDivider("2.  CONTRACT TERMS & CONTROL PROVISIONS", CONTENT_W))
story.append(Spacer(1, 6))

contract_data = [
    [Paragraph("<b>Provision</b>",     style_label),
     Paragraph("<b>Term</b>",          style_label),
     Paragraph("<b>Rationale</b>",     style_label)],
    [Paragraph("Contract Duration",    style_body_sm),
     Paragraph("6-month trial → 1-year renewable → 3-year only after verified performance",
               style_body_sm),
     Paragraph("Protect venue from locking into underperforming operators",
               style_body_sm)],
    [Paragraph("Termination (Trial)",  style_body_sm),
     Paragraph("30-day written notice by either party", style_body_sm),
     Paragraph("Low commitment to test new operators", style_body_sm)],
    [Paragraph("Termination (Year 1+)",style_body_sm),
     Paragraph("90-day written notice",style_body_sm),
     Paragraph("Gives operator transition time; protects venue's continuity",
               style_body_sm)],
    [Paragraph("Menu Approval",        style_body_sm),
     Paragraph("Venue has final approval on all menu items, pricing, and presentation",
               style_body_sm),
     Paragraph("Preserves brand coherence and guest experience standards",
               style_body_sm)],
    [Paragraph("Branding",             style_body_sm),
     Paragraph("Operator works under Studio Giraffe brand umbrella — no competing brand signage",
               style_body_sm),
     Paragraph("Rejected model: Full brand takeover (Buc-ee's model). Identity stays with venue",
               style_body_sm)],
    [Paragraph("Quality Standards",    style_body_sm),
     Paragraph("Minimum standards defined in Exhibit A of contract — temp logs, presentation, "
               "service response time, complaint resolution", style_body_sm),
     Paragraph("Failure to meet standards = cure notice within 14 days or breach",
               style_body_sm)],
    [Paragraph("Insurance",            style_body_sm),
     Paragraph("Operator carries own commercial general liability ($1M+ per occurrence), "
               "workers' comp, and product liability", style_body_sm),
     Paragraph("Venue named as additional insured on all policies",
               style_body_sm)],
    [Paragraph("Non-Compete",          style_body_sm),
     Paragraph("Operator may not operate competing food service within 3-mile radius during "
               "contract + 6 months post-termination", style_body_sm),
     Paragraph("Protects venue's market position in the Houston zoo/entertainment corridor",
               style_body_sm)],
]
contract_table = Table(contract_data, colWidths=[105, 165, CONTENT_W - 270])
contract_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    # Highlight branding row
    ("BACKGROUND",    (0,5), (-1,5), HexColor("#FFFBE6")),
]))
story.append(contract_table)
story.append(Spacer(1, 10))

# What is never negotiable
story.append(callout_box(
    "<b>Non-Negotiable — Owner Protections (applies to every deal structure):</b><br/>"
    "① Alcohol revenue and service control remain 100% with the venue — always.<br/>"
    "② No single operator receives rights to multiple revenue streams in one agreement.<br/>"
    "③ Menu, pricing, and brand identity are always subject to venue approval and override.<br/>"
    "④ Short-term contracts are required before any multi-year commitment.<br/>"
    "⑤ Venue retains the right to terminate for cause with immediate effect if quality, "
    "legal, or brand standards are violated.",
    TEAL_LITE, TEAL))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
# PAGE 4: Operator Sourcing & Next Steps
# ═══════════════════════════════════════════════════════════════

story.append(PageBanner(4,
    "Operator Sourcing & Next Steps",
    "Identifying, evaluating, and onboarding the right concession partner",
    CONTENT_W, NAVY))
story.append(Spacer(1, 10))

# Types of operators
story.append(SectionDivider("A.  OPERATOR TYPES TO TARGET — HOUSTON MARKET", CONTENT_W))
story.append(Spacer(1, 6))

op_types = [
    ("Local Restaurant Groups",
     "Houston-based multi-unit operators with proven F&B execution. Look for operators already "
     "managing 2–5 branded concepts who understand scaled food production and event environments."),
    ("Specialty Food Truck Operators (Upgrade Path)",
     "Established Houston food trucks with 3+ years of operation, strong event catering history, "
     "and existing food safety infrastructure. Lower capital requirement; familiar with mobile/campus contexts."),
    ("Zoo / Attraction Concession Specialists",
     "Firms with specific experience in zoo, aquarium, museum, or theme park food service. "
     "Industry groups: IAAPA, AZA member operators. These operators understand the unique guest "
     "mix and throughput demands of attraction venues."),
    ("Regional Catering Companies",
     "Companies that already handle corporate and event catering in the Houston market and are "
     "seeking a permanent venue anchor. Often have infrastructure, licensing, and staff in place."),
    ("Franchise-Affiliated Independent Operators",
     "Operators who hold a franchise brand license (e.g., a local Subway or similar) but operate "
     "independently — bring franchise-level systems without corporate control risk. "
     "<b>Evaluate brand fit carefully.</b>"),
]
for title, body in op_types:
    row = Table(
        [[Paragraph(f"<b>{title}</b>", S("OTL", fontName=HEAD_FONT, fontSize=9.5, leading=13,
                                          textColor=NAVY, leftIndent=0)),
          Paragraph(body, style_body_sm)]],
        colWidths=[145, CONTENT_W - 145])
    row.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LINEABOVE",     (0,0), (-1,0),  0.4, BORDER),
    ]))
    story.append(row)
story.append(Spacer(1, 10))

# Evaluation criteria
story.append(SectionDivider("B.  EVALUATION CRITERIA", CONTENT_W))
story.append(Spacer(1, 6))
criteria_data = [
    [Paragraph("<b>Criterion</b>",       style_label),
     Paragraph("<b>What to Assess</b>",  style_label),
     Paragraph("<b>Weight</b>",          style_label)],
    [Paragraph("Operational Experience", style_body_sm),
     Paragraph("Minimum 3 years managing comparable volume (150K+ guests/yr or equivalent event load)",
               style_body_sm),
     Paragraph("High",                   style_body_sm)],
    [Paragraph("References",             style_body_sm),
     Paragraph("3 verifiable venue references; speak directly to venue owners/operators, not just provided contacts",
               style_body_sm),
     Paragraph("High",                   style_body_sm)],
    [Paragraph("Financial Stability",    style_body_sm),
     Paragraph("2 years P&L + bank statements. Can they fund inventory and payroll without venue advances?",
               style_body_sm),
     Paragraph("High",                   style_body_sm)],
    [Paragraph("Menu Quality",           style_body_sm),
     Paragraph("Tasting review required. Does the food align with Studio Giraffe guest experience?",
               style_body_sm),
     Paragraph("Medium",                 style_body_sm)],
    [Paragraph("Brand Compatibility",    style_body_sm),
     Paragraph("Will operator comply with branding subordination? No competing visual identity on site.",
               style_body_sm),
     Paragraph("Medium",                 style_body_sm)],
    [Paragraph("Insurance Coverage",     style_body_sm),
     Paragraph("Proof of $1M+ per occurrence GL and active workers' comp before trial begins",
               style_body_sm),
     Paragraph("Required",               style_body_sm)],
    [Paragraph("Staffing Plan",          style_body_sm),
     Paragraph("How will they staff peak days (event days, weekends, holidays)? What is their backup plan?",
               style_body_sm),
     Paragraph("Medium",                 style_body_sm)],
]
criteria_table = Table(criteria_data, colWidths=[115, CONTENT_W - 200, 80])
criteria_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(criteria_table)
story.append(Spacer(1, 10))

# Timeline
story.append(SectionDivider("C.  OUTREACH PLAN & TIMELINE", CONTENT_W))
story.append(Spacer(1, 6))

timeline_steps = [
    ("Phase 1",  "Source",            "Weeks 1–3",
     "Identify 8–12 candidate operators through IAAPA directory, Houston Restaurant Association, "
     "personal referrals, and direct approach of top food trucks. Prepare one-page venue overview + "
     "deal structure summary for initial outreach."),
    ("Phase 2",  "Interview",         "Weeks 4–6",
     "Conduct in-person or video interviews with top 4–6 candidates. Provide campus tour. "
     "Collect references and initial financial documentation. Narrow to 2 finalists."),
    ("Phase 3",  "Trial Agreement",   "Weeks 7–8",
     "Execute 6-month trial agreement (Option B structure — revenue share only, no base rent). "
     "Agree on quality standards, reporting cadence, and termination terms."),
    ("Phase 4",  "Trial Operations",  "Months 3–8",
     "Monitor monthly sales reports, guest feedback, and operational compliance. Conduct "
     "mid-trial review at month 3. Evaluate readiness for long-term agreement."),
    ("Phase 5",  "Evaluate",          "Month 8–9",
     "Full performance review against agreed metrics. Decision: extend trial, convert to "
     "1-year Option A, or terminate and source replacement."),
    ("Phase 6",  "Long-Term",         "Month 10+",
     "If performance is proven, execute 1-year renewable agreement (Option A: base rent + %). "
     "3-year term only considered after at least one successful renewal cycle."),
]
tl_data = [[
    Paragraph(f"<b>{tag}</b>", S("TLT", fontName=HEAD_FONT, fontSize=8, leading=11,
                                  textColor=WHITE)),
    Paragraph(f"<b>{name}</b>", S("TLN", fontName=HEAD_FONT, fontSize=9.5, leading=13,
                                   textColor=NAVY)),
    Paragraph(timing, S("TLM", fontName=BODY_FONT, fontSize=8.5, leading=11,
                          textColor=MUTED)),
    Paragraph(desc, style_body_sm),
] for tag, name, timing, desc in timeline_steps]

# Insert header
tl_data.insert(0, [
    Paragraph("<b>Phase</b>", style_label),
    Paragraph("<b>Stage</b>", style_label),
    Paragraph("<b>Timing</b>", style_label),
    Paragraph("<b>Actions</b>", style_label),
])

tl_table = Table(tl_data, colWidths=[45, 100, 68, CONTENT_W - 213])
tl_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0), NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0), WHITE),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0), (-1,-1), 0.4, BORDER),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
    # Color phase tags
    ("BACKGROUND",    (0,1), (0,1),  TEAL),
    ("BACKGROUND",    (0,2), (0,2),  NAVY),
    ("BACKGROUND",    (0,3), (0,3),  TEAL),
    ("BACKGROUND",    (0,4), (0,4),  NAVY),
    ("BACKGROUND",    (0,5), (0,5),  TEAL),
    ("BACKGROUND",    (0,6), (0,6),  NAVY),
    ("TEXTCOLOR",     (0,1), (0,6),  WHITE),
    ("ALIGN",         (0,1), (0,6),  "CENTER"),
    ("VALIGN",        (0,1), (0,6),  "MIDDLE"),
]))
story.append(tl_table)
story.append(Spacer(1, 10))

# Contact / Next Steps
story.append(callout_box(
    "<b>Primary Contact / Decision Maker:</b><br/>"
    "Name: _________________________________    Title: _________________________<br/>"
    "Phone: ________________________________    Email: _________________________<br/><br/>"
    "<b>Immediate Next Steps:</b>  (1) Finalize base rent placeholder in deal framework.  "
    "(2) Assign sourcing lead and begin Phase 1 operator list.  "
    "(3) Draft one-page outreach brief for candidate operators.  "
    "(4) Set 30-day check-in date to review sourcing progress.",
    TEAL_LITE, TEAL,
    style=S("CBB", fontName=BODY_FONT, fontSize=9, leading=14,
             textColor=HexColor("#004E50"), leftIndent=0, rightIndent=0)))

# ─────────────────────────────────────────────────────────────────────────────
# Header / Footer callback
# ─────────────────────────────────────────────────────────────────────────────
def on_page(canvas_obj, doc):
    canvas_obj.saveState()
    w, h = letter
    # Top rule
    canvas_obj.setStrokeColor(TEAL)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(MARGIN, h - 0.35*inch, w - MARGIN, h - 0.35*inch)
    # Footer
    canvas_obj.setFillColor(MUTED)
    canvas_obj.setFont(BODY_FONT, 7.5)
    canvas_obj.drawString(MARGIN, 0.35*inch,
        "Studio Giraffe — Food & Retail Operator Model  |  Internal Strategy Document  |  Confidential")
    canvas_obj.drawRightString(w - MARGIN, 0.35*inch, f"Page {doc.page}")
    canvas_obj.restoreState()

# ─────────────────────────────────────────────────────────────────────────────
# Build
# ─────────────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF saved to: {OUTPUT}")
