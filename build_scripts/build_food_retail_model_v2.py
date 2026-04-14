"""
Food & Retail Operator Model — Strategy Document PDF
Studio Giraffe / Zoo+Aquarium Campus, Houston
Compact 4-page layout
"""

import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.flowables import Flowable

# ── Colors ───────────────────────────────────────────────────────────────────
NAVY      = HexColor("#2C3481")
TEAL      = HexColor("#00AAAD")
TEAL_LITE = HexColor("#E8F7F7")
NAVY_LITE = HexColor("#EAEBF5")
TEXT      = HexColor("#1C1C1C")
MUTED     = HexColor("#6B6B6B")
BORDER    = HexColor("#CCCCCC")
BG_LIGHT  = HexColor("#F7F7F7")
WHITE     = white

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

try:
    p_reg  = str(FONT_DIR / "DMSans.ttf")
    p_bold = str(FONT_DIR / "DMSans-Bold.ttf")
    pdfmetrics.registerFont(TTFont("DMSans",      p_reg))
    pdfmetrics.registerFont(TTFont("DMSans-Bold", p_bold))
    BODY_FONT = "DMSans"
    HEAD_FONT = "DMSans-Bold"
except Exception:
    BODY_FONT = "Helvetica"
    HEAD_FONT = "Helvetica-Bold"

# ── Page geometry ─────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN    = 0.5 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

# ── Styles (compact) ─────────────────────────────────────────────────────────
ss = getSampleStyleSheet()

def S(name, parent="Normal", **kw):
    base = ss.get(parent, ss["Normal"])
    return ParagraphStyle(name, parent=base, **kw)

H2     = S("H2",   fontName=HEAD_FONT, fontSize=9.5,  leading=12, textColor=NAVY,  spaceAfter=2, spaceBefore=5)
H3     = S("H3",   fontName=HEAD_FONT, fontSize=8.5,  leading=11, textColor=TEAL,  spaceAfter=1, spaceBefore=3)
BODY   = S("Body", fontName=BODY_FONT, fontSize=8.5,  leading=11.5, textColor=TEXT, spaceAfter=3)
BODY_S = S("BodyS",fontName=BODY_FONT, fontSize=8,    leading=10.5, textColor=TEXT, spaceAfter=2)
LBL    = S("Lbl",  fontName=HEAD_FONT, fontSize=7.5,  leading=9.5,  textColor=MUTED, spaceAfter=1)
CAP    = S("Cap",  fontName=BODY_FONT, fontSize=7.5,  leading=10,   textColor=MUTED, spaceAfter=1)
TBOX   = S("Tbox", fontName=BODY_FONT, fontSize=8.5,  leading=11.5, textColor=HexColor("#004A4B"))
NBOX   = S("Nbox", fontName=HEAD_FONT, fontSize=8.5,  leading=11.5, textColor=NAVY)

# ── Custom Flowables ──────────────────────────────────────────────────────────
class PageBanner(Flowable):
    """Full-width navy banner for each page."""
    def __init__(self, num, title, sub, w):
        super().__init__()
        self.num   = num
        self.title = title
        self.sub   = sub
        self._w    = w
        self.height= 48

    def wrap(self, availWidth, availHeight):
        return (self._w, self.height)

    def draw(self):
        c = self.canv
        w, h = self._w, self.height
        c.setFillColor(NAVY);  c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(TEAL);  c.rect(0, 0, w, 3, fill=1, stroke=0)
        # Page pill
        c.setFillColor(TEAL);  c.roundRect(w-42, h-24, 38, 18, 3, fill=1, stroke=0)
        c.setFillColor(WHITE);  c.setFont(HEAD_FONT, 8)
        c.drawCentredString(w-23, h-14, f"PAGE {self.num}")
        # Title
        c.setFillColor(WHITE);  c.setFont(HEAD_FONT, 14)
        c.drawString(10, h-22, self.title)
        # Subtitle
        c.setFillColor(HexColor("#8BBFC4")); c.setFont(BODY_FONT, 7.5)
        c.drawString(10, h-34, self.sub)


class SectionBar(Flowable):
    """Thin navy left-bar section label."""
    def __init__(self, label, w):
        super().__init__()
        self.label = label
        self._w    = w
        self.height= 14

    def wrap(self, a, b): return (self._w, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY); c.rect(0, 2, 3, 10, fill=1, stroke=0)
        c.setFillColor(NAVY); c.setFont(HEAD_FONT, 8)
        c.drawString(8, 4, self.label)


def tbox(text, bg=TEAL_LITE, bar=TEAL, st=None):
    st = st or TBOX
    t = Table([[Paragraph(text, st)]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("LINEBEFORE",   (0,0),(0,-1),  3, bar),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    return t


def nbox(text):
    return tbox(text, bg=NAVY_LITE, bar=NAVY,
                st=S("NB2", fontName=HEAD_FONT, fontSize=8, leading=11, textColor=NAVY))


def grid(data, cols, hdr_bg=NAVY):
    t = Table(data, colWidths=cols)
    nrow = len(data)
    rows_bg = [WHITE if i % 2 == 0 else BG_LIGHT for i in range(nrow - 1)]
    ts = TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),   hdr_bg),
        ("TEXTCOLOR",     (0,0), (-1,0),   WHITE),
        ("FONTNAME",      (0,0), (-1,0),   HEAD_FONT),
        ("FONTSIZE",      (0,0), (-1,-1),  8),
        ("ROWBACKGROUNDS",(0,1), (-1,-1),  rows_bg),
        ("GRID",          (0,0), (-1,-1),  0.3, BORDER),
        ("TOPPADDING",    (0,0), (-1,-1),  4),
        ("BOTTOMPADDING", (0,0), (-1,-1),  4),
        ("LEFTPADDING",   (0,0), (-1,-1),  6),
        ("RIGHTPADDING",  (0,0), (-1,-1),  4),
        ("VALIGN",        (0,0), (-1,-1),  "TOP"),
    ])
    t.setStyle(ts)
    return t


# Header/footer
def on_page(cv, doc):
    cv.saveState()
    w, h = letter
    cv.setStrokeColor(TEAL); cv.setLineWidth(1)
    cv.line(MARGIN, h - 0.32*inch, w-MARGIN, h - 0.32*inch)
    cv.setFillColor(MUTED); cv.setFont(BODY_FONT, 6.5)
    cv.drawString(MARGIN, 0.28*inch,
        "Studio Giraffe — Food & Retail Operator Model  |  Internal Strategy Document  |  Confidential")
    cv.drawRightString(w-MARGIN, 0.28*inch, f"Page {doc.page}")
    cv.restoreState()

# ─────────────────────────────────────────────────────────────────────────────
# STORY
# ─────────────────────────────────────────────────────────────────────────────
story = []
sp  = lambda n=4: Spacer(1, n)

# ═══════════════════════════════════════════════════════
# PAGE 1 — Current Operations Assessment
# ═══════════════════════════════════════════════════════
story.append(PageBanner(1, "Current Operations Assessment",
    "Studio Giraffe · Zoo / Aquarium + Entertainment Campus · Houston, TX", CONTENT_W))
story.append(sp(6))

# KPI bar
kpi_cols = [CONTENT_W/4]*4
kpi = [
    [Paragraph("<b>300,000</b>", S("K1",fontName=HEAD_FONT,fontSize=14,leading=18,
                                    textColor=NAVY,spaceAfter=0)),
     Paragraph("<b>600–700</b>", S("K2",fontName=HEAD_FONT,fontSize=14,leading=18,
                                    textColor=NAVY,spaceAfter=0)),
     Paragraph("<b>20 Suites</b>", S("K3",fontName=HEAD_FONT,fontSize=14,leading=18,
                                      textColor=HexColor("#004E50"),spaceAfter=0)),
     Paragraph("<b>40–60 Events</b>", S("K4",fontName=HEAD_FONT,fontSize=14,leading=18,
                                         textColor=HexColor("#004E50"),spaceAfter=0))],
    [Paragraph("Annual Visitors", CAP),
     Paragraph("Parking Capacity", CAP),
     Paragraph("@ $300/night", CAP),
     Paragraph("Per Year", CAP)],
]
kpi_t = Table(kpi, colWidths=kpi_cols)
kpi_t.setStyle(TableStyle([
    ("ALIGN",         (0,0),(-1,-1),"CENTER"),
    ("VALIGN",        (0,0),(-1,-1),"MIDDLE"),
    ("BACKGROUND",    (0,0),(1,-1), NAVY_LITE),
    ("BACKGROUND",    (2,0),(3,-1), TEAL_LITE),
    ("TOPPADDING",    (0,0),(-1,-1), 5),
    ("BOTTOMPADDING", (0,0),(-1,-1), 5),
    ("GRID",          (0,0),(-1,-1), 0.3, BORDER),
]))
story.append(kpi_t)
story.append(sp(6))

# Section A
story.append(SectionBar("A.  FOOD & RETAIL OPERATIONS OVERVIEW", CONTENT_W))
story.append(sp(4))
story.append(Paragraph(
    "Studio Giraffe currently operates all food and beverage services in-house across two channels: "
    "a permanent indoor food facility and an on-site food truck. Alcohol is managed entirely by venue "
    "staff and is integrated into event packages, general admission, and lodging revenue. "
    "Retail merchandise is sold through the main guest services counter. No third-party food operator is currently engaged.",
    BODY))

ops_data = [
    [Paragraph("<b>Channel</b>",LBL),Paragraph("<b>Type</b>",LBL),
     Paragraph("<b>Managed By</b>",LBL),Paragraph("<b>Alcohol</b>",LBL)],
    [Paragraph("Indoor Food Facility",BODY_S),Paragraph("Permanent",BODY_S),
     Paragraph("Venue Staff",BODY_S),Paragraph("Yes — internal",BODY_S)],
    [Paragraph("On-Site Food Truck",BODY_S),Paragraph("Mobile / Seasonal",BODY_S),
     Paragraph("Venue Staff",BODY_S),Paragraph("Limited",BODY_S)],
    [Paragraph("Retail Merchandise",BODY_S),Paragraph("Counter Sales",BODY_S),
     Paragraph("Venue Staff",BODY_S),Paragraph("N/A",BODY_S)],
]
story.append(grid(ops_data, [155, 105, 120, 100]))
story.append(sp(5))

# Section B
story.append(SectionBar("B.  PAIN POINTS — OPERATIONAL DISTRACTION", CONTENT_W))
story.append(sp(3))

pain = [
    ("Staffing Burden",
     "F&B positions require specialized scheduling, training, and retention — diverting effort from animal programs, event coordination, and core venue ops."),
    ("Operational Complexity",
     "Inventory, supplier relations, food safety compliance, equipment maintenance, and health inspections demand dedicated management bandwidth."),
    ("Revenue Underperformance",
     "Without a professional operator, food sales lag during peak periods. Upsell, alcohol, and event catering revenue are regularly left on the table."),
    ("Capital Exposure",
     "Venue absorbs all food COGS, waste, and equipment risk with no guaranteed revenue floor from a tenant or partner."),
]
pain_data = [[Paragraph("<b>Pain Point</b>",LBL),Paragraph("<b>Impact</b>",LBL)]]
for t, b in pain:
    pain_data.append([Paragraph(f"<b>{t}</b>",S("PL",fontName=HEAD_FONT,fontSize=8,leading=11,textColor=NAVY)),
                      Paragraph(b,BODY_S)])
story.append(grid(pain_data,[130,CONTENT_W-130]))
story.append(sp(5))

# Section C
story.append(SectionBar("C.  REVENUE BASELINE FRAMEWORK", CONTENT_W))
story.append(sp(3))

rev_data = [
    [Paragraph("<b>Revenue Stream</b>",LBL),Paragraph("<b>Current Model</b>",LBL),
     Paragraph("<b>Baseline (fill in)</b>",LBL),Paragraph("<b>Operator Impact</b>",LBL)],
    [Paragraph("Tickets",BODY_S),Paragraph("Venue-direct",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("None — unaffected",BODY_S)],
    [Paragraph("Food & Beverage",BODY_S),Paragraph("In-house",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("Shift to operator model",BODY_S)],
    [Paragraph("Alcohol",S("ALC",fontName=HEAD_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500"))),
     Paragraph("Venue-controlled",S("ALC2",fontName=HEAD_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500"))),
     Paragraph("$____________",S("ALC3",fontName=BODY_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500"))),
     Paragraph("Retained 100% by venue",S("ALC4",fontName=HEAD_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500")))],
    [Paragraph("Parking",BODY_S),Paragraph("Venue-direct",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("None — unaffected",BODY_S)],
    [Paragraph("Lodging (20 suites)",BODY_S),Paragraph("Venue-direct",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("None — unaffected",BODY_S)],
    [Paragraph("Events (40–60/yr)",BODY_S),Paragraph("Venue-direct",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("Operator may cater",BODY_S)],
    [Paragraph("Vendors / Sponsorships",BODY_S),Paragraph("Venue-direct",BODY_S),
     Paragraph("$____________",BODY_S),Paragraph("None — unaffected",BODY_S)],
]
rev_t = grid(rev_data,[125,100,105,CONTENT_W-330])
rev_t.setStyle(TableStyle([
    ("BACKGROUND",    (0,0),(-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0),(-1,0),  WHITE),
    ("FONTNAME",      (0,0),(-1,0),  HEAD_FONT),
    ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, BG_LIGHT]),
    ("GRID",          (0,0),(-1,-1), 0.3, BORDER),
    ("TOPPADDING",    (0,0),(-1,-1), 4),
    ("BOTTOMPADDING", (0,0),(-1,-1), 4),
    ("LEFTPADDING",   (0,0),(-1,-1), 6),
    ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ("FONTSIZE",      (0,0),(-1,-1), 8),
    ("BACKGROUND",    (0,3),(-1,3),  HexColor("#FFF8E0")),
]))
story.append(rev_t)
story.append(sp(5))
story.append(tbox(
    "<b>Strategic Goal:</b>  Professionalize food & beverage through a structured third-party operator model — "
    "reducing staffing burden while retaining brand identity, alcohol control, pricing authority, and all revenue streams. "
    "Venue remains operator of record; partner handles execution."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════
# PAGE 2 — Operator Model Options
# ═══════════════════════════════════════════════════════
story.append(PageBanner(2, "Operator Model Options",
    "Three structural approaches — evaluate by control, revenue, and complexity", CONTENT_W))
story.append(sp(5))
story.append(Paragraph(
    "Each model reflects a different balance of revenue sharing, operational complexity, and venue control. "
    "Option A is recommended. Option B is ideal for an initial trial phase. Option C is reserved for Phase 3+.", BODY))
story.append(sp(4))

def option_block(letter_tag, title, tag, bg, rows, col_widths, highlight_row=None):
    # Header
    hdr = Table([[
        Paragraph(f'<font color="white"><b>{letter_tag}</b></font>',
                  S("OH",fontName=HEAD_FONT,fontSize=16,leading=20,textColor=WHITE)),
        Paragraph(f'<font color="white"><b>{title}</b></font><br/>'
                  f'<font color="#A0DFE2">{tag}</font>',
                  S("OT",fontName=HEAD_FONT,fontSize=10,leading=13,textColor=WHITE)),
    ]], colWidths=[30, CONTENT_W-30])
    hdr.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    # Body
    body_t = Table(rows, colWidths=col_widths)
    style_cmds = [
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[WHITE, BG_LIGHT]),
        ("GRID",(0,0),(-1,-1),0.3,BORDER),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),6),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("FONTSIZE",(0,0),(-1,-1),8),
    ]
    if highlight_row is not None:
        style_cmds.append(("BACKGROUND",(0,highlight_row),(-1,highlight_row),HexColor("#FFF8E0")))
        style_cmds.append(("FONTNAME",(0,highlight_row),(-1,highlight_row),HEAD_FONT))
    body_t.setStyle(TableStyle(style_cmds))
    return [hdr, body_t, sp(5)]

# Option A
opt_a_rows = [
    [Paragraph("<b>Venue provides:</b>",LBL), Paragraph("Space, utilities, brand guidelines, menu framework, alcohol service",BODY_S)],
    [Paragraph("<b>Operator provides:</b>",LBL), Paragraph("Staffing, food production, inventory, supplier relations, equipment maintenance, health compliance",BODY_S)],
    [Paragraph("<b>Revenue model:</b>",LBL), Paragraph("Base rent (fixed monthly) + <b>10–20% of gross food & non-alcohol beverage sales</b> to venue",BODY_S)],
    [Paragraph("<b>Venue retains:</b>",LBL), Paragraph("<b>100% alcohol · Brand approval · Menu approval · Pricing authority · Event catering rights</b>",BODY_S)],
    [Paragraph("<b>Best for:</b>",LBL), Paragraph("Operators with F&B track record; venues with defined brand standards and strong repeat visitor base",BODY_S)],
]
for item in option_block("A","Managed Concession","RECOMMENDED — Strongest control + professional execution",
                          NAVY, opt_a_rows,[110,CONTENT_W-110], highlight_row=3):
    story.append(item)

# Option B
opt_b_rows = [
    [Paragraph("<b>Structure:</b>",LBL), Paragraph("Minimal or no base rent; venue takes higher % of gross sales (typically 20–30%)",BODY_S)],
    [Paragraph("<b>Benefit:</b>",LBL), Paragraph("Lower commitment barrier attracts quality operators. Revenue scales with performance — aligns incentives",BODY_S)],
    [Paragraph("<b>Risk:</b>",LBL), Paragraph("No guaranteed floor revenue. Seasonal foot traffic = variable venue income",BODY_S)],
    [Paragraph("<b>Best use case:</b>",LBL), Paragraph("6-month trial period to test operator before committing to base rent. Transition to Option A once proven",BODY_S)],
    [Paragraph("<b>Venue retains:</b>",LBL), Paragraph("Alcohol, brand, menu approval, pricing — same protections as Option A",BODY_S)],
]
for item in option_block("B","Revenue Share Only","Lower base rent / higher revenue share — ideal for operator testing",
                          HexColor("#3B4A9A"), opt_b_rows,[110,CONTENT_W-110]):
    story.append(item)

# Option C
opt_c_rows = [
    [Paragraph("<b>Structure:</b>",LBL), Paragraph("2–4 specialty vendors assigned to specific zones. Each signs a separate agreement.",BODY_S)],
    [Paragraph("<b>Benefit:</b>",LBL), Paragraph("Menu variety, operator redundancy, zone-specific food themes",BODY_S)],
    [Paragraph("<b>Risk:</b>",LBL), Paragraph("High management complexity — multiple contracts, insurance relationships, consistency challenges",BODY_S)],
    [Paragraph("<b>Recommendation:</b>",LBL), Paragraph("<b>Not for initial phase.</b> Consider only after Option A is proven and venue has management capacity.",BODY_S)],
]
for item in option_block("C","Multi-Vendor Food Court","Multiple specialty operators in distinct venue zones",
                          HexColor("#1E2A6E"), opt_c_rows,[110,CONTENT_W-110], highlight_row=3):
    story.append(item)

# Quick comparison
story.append(SectionBar("QUICK COMPARISON", CONTENT_W))
story.append(sp(3))
comp_data = [
    [Paragraph("<b>Factor</b>",LBL),Paragraph("<b>Option A</b>",LBL),
     Paragraph("<b>Option B</b>",LBL),Paragraph("<b>Option C</b>",LBL)],
    [Paragraph("Revenue Predictability",BODY_S),Paragraph("High (base + %)",BODY_S),
     Paragraph("Variable (% only)",BODY_S),Paragraph("Medium",BODY_S)],
    [Paragraph("Management Burden",BODY_S),Paragraph("Low",BODY_S),
     Paragraph("Low",BODY_S),Paragraph("High",BODY_S)],
    [Paragraph("Alcohol / Brand Control",BODY_S),Paragraph("Full",BODY_S),
     Paragraph("Full",BODY_S),Paragraph("Harder to enforce",BODY_S)],
    [Paragraph("Recommended Phase",BODY_S),Paragraph("Post-trial / Long-term",BODY_S),
     Paragraph("Trial phase",BODY_S),Paragraph("Phase 3 only",BODY_S)],
]
comp_t = grid(comp_data,[130,108,108,CONTENT_W-346])
comp_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("FONTNAME",(0,0),(-1,0),HEAD_FONT),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,BORDER),
    ("FONTSIZE",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("BACKGROUND",(1,1),(1,-1),HexColor("#EDFFF0")),
]))
story.append(comp_t)

story.append(PageBreak())

# ═══════════════════════════════════════════════════════
# PAGE 3 — Deal Structure Framework
# ═══════════════════════════════════════════════════════
story.append(PageBanner(3, "Deal Structure Framework",
    "Non-negotiable terms, financial structure, and contractual protections", CONTENT_W))
story.append(sp(5))
story.append(nbox(
    "Owner Rules:  (1) Never give away alcohol control.  "
    "(2) Never bundle multiple revenue streams in one deal.  "
    "(3) Operational control remains with the venue.  "
    "(4) Short-term contracts before long-term commitments."))
story.append(sp(5))

# Financial terms
story.append(SectionBar("1.  FINANCIAL TERMS", CONTENT_W))
story.append(sp(3))
fin_data = [
    [Paragraph("<b>Term</b>",LBL),Paragraph("<b>Structure</b>",LBL),Paragraph("<b>Notes</b>",LBL)],
    [Paragraph("Base Rent",BODY_S),Paragraph("$_______ / month",BODY_S),
     Paragraph("Fixed floor — guaranteed revenue regardless of operator sales volume",BODY_S)],
    [Paragraph("Revenue Share",BODY_S),Paragraph("10–20% of gross food & non-alcohol beverage sales",BODY_S),
     Paragraph("Gross = before operator's COGS. Venue defines calculation method in contract",BODY_S)],
    [Paragraph("Alcohol Revenue",S("AR",fontName=HEAD_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500"))),
     Paragraph("100% retained by venue",S("ARV",fontName=HEAD_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500"))),
     Paragraph("<b>Non-negotiable.</b> Operator has zero alcohol revenue participation. Venue employs/designates alcohol service staff.",
               S("ARN",fontName=BODY_FONT,fontSize=8,leading=10.5,textColor=HexColor("#7A5500")))],

    [Paragraph("Event Catering",BODY_S),Paragraph("Optional — at venue discretion",BODY_S),
     Paragraph("Venue may assign operator at a negotiated per-event rate; retains right to use alternative caterers",BODY_S)],
    [Paragraph("Reporting",BODY_S),Paragraph("Monthly POS reports due by 10th of following month",BODY_S),
     Paragraph("Venue has right to audit sales records at any time with 5-business-day notice",BODY_S)],
]
fin_t = Table(fin_data, colWidths=[90, 145, CONTENT_W-235])
fin_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("FONTNAME",(0,0),(-1,0),HEAD_FONT),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,BORDER),
    ("FONTSIZE",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("BACKGROUND",(0,3),(-1,3),HexColor("#FFF8E0")),
]))
story.append(fin_t)
story.append(sp(5))

# Contract terms
story.append(SectionBar("2.  CONTRACT TERMS & CONTROL PROVISIONS", CONTENT_W))
story.append(sp(3))
contract_data = [
    [Paragraph("<b>Provision</b>",LBL),Paragraph("<b>Term</b>",LBL),Paragraph("<b>Rationale</b>",LBL)],
    [Paragraph("Duration",BODY_S),
     Paragraph("6-month trial -> 1-year renewable -> 3-year only after verified performance",BODY_S),
     Paragraph("Protects venue from locking into underperforming operators",BODY_S)],
    [Paragraph("Termination (Trial)",BODY_S),Paragraph("30-day written notice",BODY_S),
     Paragraph("Low commitment to test new operators with minimal lock-in",BODY_S)],
    [Paragraph("Termination (Year 1+)",BODY_S),Paragraph("90-day written notice",BODY_S),
     Paragraph("Gives operator transition time; protects venue's operational continuity",BODY_S)],
    [Paragraph("Menu Approval",BODY_S),
     Paragraph("Venue has final approval on all menu items, pricing, and presentation",BODY_S),
     Paragraph("Preserves brand coherence and guest experience standards",BODY_S)],
    [Paragraph("Branding",BODY_S),
     Paragraph("Operator works under Studio Giraffe brand umbrella — no competing brand signage on site",BODY_S),
     Paragraph("Rejected: full brand takeover (Buc-ee's model). Identity stays with venue.",BODY_S)],
    [Paragraph("Quality Standards",BODY_S),
     Paragraph("Minimum standards in Exhibit A: temp logs, presentation, service response, complaint resolution",BODY_S),
     Paragraph("Failure = 14-day cure notice or contract breach",BODY_S)],
    [Paragraph("Insurance",BODY_S),
     Paragraph("Operator carries own GL ($1M+ per occurrence), workers' comp, product liability",BODY_S),
     Paragraph("Venue named as additional insured on all policies",BODY_S)],
    [Paragraph("Non-Compete",BODY_S),
     Paragraph("No competing food service within 3-mile radius during contract + 6 months post-termination",BODY_S),
     Paragraph("Protects venue's market position in the Houston zoo/entertainment corridor",BODY_S)],
]
contract_t = Table(contract_data, colWidths=[90, 165, CONTENT_W-255])
contract_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("FONTNAME",(0,0),(-1,0),HEAD_FONT),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,BORDER),
    ("FONTSIZE",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("BACKGROUND",(0,5),(-1,5),HexColor("#FFF8E0")),
]))
story.append(contract_t)
story.append(sp(5))
story.append(tbox(
    "<b>Non-Negotiable Protections (applies to every deal):</b>  "
    "(1) Alcohol control and revenue stay 100% with the venue — always.  "
    "(2) No single operator receives rights to multiple revenue streams in one agreement.  "
    "(3) Menu, pricing, and brand identity are always subject to venue override.  "
    "(4) Venue may terminate for cause with immediate effect on quality or legal violations."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════
# PAGE 4 — Operator Sourcing & Next Steps
# ═══════════════════════════════════════════════════════
story.append(PageBanner(4, "Operator Sourcing & Next Steps",
    "Identifying, evaluating, and onboarding the right concession partner in Houston", CONTENT_W))
story.append(sp(5))

# Operator types
story.append(SectionBar("A.  OPERATOR TYPES TO TARGET — HOUSTON MARKET", CONTENT_W))
story.append(sp(3))
op_data = [
    [Paragraph("<b>Type</b>",LBL),Paragraph("<b>Description & Fit</b>",LBL)],
    [Paragraph("Local Restaurant Groups",BODY_S),
     Paragraph("Houston-based multi-unit operators managing 2–5 concepts. Proven F&B execution, scaled food production, and event environment experience.",BODY_S)],
    [Paragraph("Food Truck Operators (Upgrade Path)",BODY_S),
     Paragraph("Established Houston trucks with 3+ years of operation, event catering history, and food safety infrastructure. Familiar with campus-style contexts.",BODY_S)],
    [Paragraph("Zoo / Attraction Concession Specialists",BODY_S),
     Paragraph("Operators with experience at zoos, aquariums, or museums. Sources: IAAPA, AZA member networks. Understand attraction guest mix and throughput demands.",BODY_S)],
    [Paragraph("Regional Catering Companies",BODY_S),
     Paragraph("Houston-market event caterers seeking a permanent venue anchor. Often have licensing, staff, and supplier relationships already in place.",BODY_S)],
    [Paragraph("Franchise-Affiliated Independents",BODY_S),
     Paragraph("Operators holding a franchise license who run independently — bring franchise-level systems without corporate control risk. Evaluate brand fit carefully.",BODY_S)],
]
story.append(grid(op_data,[125,CONTENT_W-125]))
story.append(sp(3))

# Evaluation criteria
story.append(SectionBar("B.  EVALUATION CRITERIA", CONTENT_W))
story.append(sp(2))
eval_data = [
    [Paragraph("<b>Criterion</b>",LBL),Paragraph("<b>What to Assess</b>",LBL),Paragraph("<b>Weight</b>",LBL)],
    [Paragraph("Operational Experience",BODY_S),
     Paragraph("Min. 3 years managing comparable volume (150K+ guests/yr or equivalent event load)",BODY_S),
     Paragraph("High",BODY_S)],
    [Paragraph("References",BODY_S),
     Paragraph("3 verifiable venue references; speak directly to owners/operators — not just provided contacts",BODY_S),
     Paragraph("High",BODY_S)],
    [Paragraph("Financial Stability",BODY_S),
     Paragraph("2 years P&L + bank statements. Can they fund inventory and payroll without venue advances?",BODY_S),
     Paragraph("High",BODY_S)],
    [Paragraph("Menu Quality",BODY_S),
     Paragraph("Tasting review required. Does food align with Studio Giraffe guest experience and brand?",BODY_S),
     Paragraph("Medium",BODY_S)],
    [Paragraph("Brand Compatibility",BODY_S),
     Paragraph("Will operator comply with branding subordination? No competing visual identity on site.",BODY_S),
     Paragraph("Medium",BODY_S)],
    [Paragraph("Insurance Coverage",BODY_S),
     Paragraph("Proof of $1M+ per occurrence GL and active workers' comp before trial begins",BODY_S),
     Paragraph("Required",BODY_S)],
    [Paragraph("Staffing Plan",BODY_S),
     Paragraph("How will they staff peak days — events, weekends, holidays? What is their backup plan?",BODY_S),
     Paragraph("Medium",BODY_S)],
]
story.append(grid(eval_data,[115,CONTENT_W-185,65]))
story.append(sp(3))

# Timeline
story.append(SectionBar("C.  OUTREACH PLAN & TIMELINE", CONTENT_W))
story.append(sp(2))
tl_data = [
    [Paragraph("<b>Phase</b>",LBL),Paragraph("<b>Stage</b>",LBL),
     Paragraph("<b>Timing</b>",LBL),Paragraph("<b>Key Actions</b>",LBL)],
    [Paragraph("1",BODY_S),Paragraph("<b>Source</b>",BODY_S),Paragraph("Wks 1–3",BODY_S),
     Paragraph("Identify 8–12 candidates via IAAPA, Houston Restaurant Association, referrals. Prepare one-page venue + deal summary.",BODY_S)],
    [Paragraph("2",BODY_S),Paragraph("<b>Interview</b>",BODY_S),Paragraph("Wks 4–6",BODY_S),
     Paragraph("Campus tours + in-person interviews. Collect references and financials. Narrow to 2 finalists.",BODY_S)],
    [Paragraph("3",BODY_S),Paragraph("<b>Trial Agmt</b>",BODY_S),Paragraph("Wks 7–8",BODY_S),
     Paragraph("Execute 6-month trial (Option B). Define quality standards, reporting cadence, 30-day termination.",BODY_S)],
    [Paragraph("4",BODY_S),Paragraph("<b>Operations</b>",BODY_S),Paragraph("Mo 3–8",BODY_S),
     Paragraph("Monitor POS reports, guest feedback, and compliance. Mid-trial review at month 3.",BODY_S)],
    [Paragraph("5",BODY_S),Paragraph("<b>Evaluate</b>",BODY_S),Paragraph("Mo 8–9",BODY_S),
     Paragraph("Full performance review. Extend trial, convert to 1-year Option A, or terminate.",BODY_S)],
    [Paragraph("6",BODY_S),Paragraph("<b>Long-Term</b>",BODY_S),Paragraph("Mo 10+",BODY_S),
     Paragraph("Execute 1-year renewable (Option A). 3-year term only after successful renewal cycle.",BODY_S)],
]
tl_t = Table(tl_data, colWidths=[28, 80, 65, CONTENT_W-173])
tl_t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),WHITE),
    ("FONTNAME",(0,0),(-1,0),HEAD_FONT),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,BG_LIGHT]),
    ("GRID",(0,0),(-1,-1),0.3,BORDER),
    ("FONTSIZE",(0,0),(-1,-1),8),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("LEFTPADDING",(0,0),(-1,-1),6),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ALIGN",(0,1),(0,-1),"CENTER"),
    ("BACKGROUND",(0,1),(0,1),TEAL),("TEXTCOLOR",(0,1),(0,1),WHITE),
    ("BACKGROUND",(0,2),(0,2),NAVY),("TEXTCOLOR",(0,2),(0,2),WHITE),
    ("BACKGROUND",(0,3),(0,3),TEAL),("TEXTCOLOR",(0,3),(0,3),WHITE),
    ("BACKGROUND",(0,4),(0,4),NAVY),("TEXTCOLOR",(0,4),(0,4),WHITE),
    ("BACKGROUND",(0,5),(0,5),TEAL),("TEXTCOLOR",(0,5),(0,5),WHITE),
    ("BACKGROUND",(0,6),(0,6),NAVY),("TEXTCOLOR",(0,6),(0,6),WHITE),
]))
story.append(tl_t)
story.append(sp(5))

# Contact box
story.append(tbox(
    "<b>Primary Contact / Decision Maker:</b><br/>"
    "Name: ____________________________________    Title: ______________________________<br/>"
    "Phone: ___________________________________    Email: ______________________________<br/><br/>"
    "<b>Immediate Next Steps:</b>  (1) Finalize base rent placeholder in deal framework.  "
    "(2) Assign sourcing lead and build Phase 1 operator list.  "
    "(3) Draft one-page outreach brief for candidate operators.  "
    "(4) Set 30-day check-in to review sourcing progress.",
    TEAL_LITE, TEAL,
    st=S("CB2",fontName=BODY_FONT,fontSize=8,leading=11.5,textColor=HexColor("#004A4B"))))

# ─────────────────────────────────────────────────────────────────────────────
# Build
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/FOOD_RETAIL_OPERATOR_MODEL.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=0.42*inch,
    bottomMargin=0.42*inch,
    title="Food & Retail Operator Model — Strategy Document",
    author="Perplexity Computer",
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF saved to: {OUTPUT}")
