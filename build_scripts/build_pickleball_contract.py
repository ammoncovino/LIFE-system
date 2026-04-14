"""
Pickleball Contract Revision PDF
Internal memo + redline summary for Honcho Pickleball contract renegotiation.
"""

import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ─── Fonts ────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

def download_font(name, url, filename):
    path = FONT_DIR / filename
    if not path.exists():
        print(f"  Downloading {name}…")
        urllib.request.urlretrieve(url, path)
    pdfmetrics.registerFont(TTFont(name, str(path)))

# Work Sans (headings) and Inter (body)
download_font(
    "WorkSans-Bold",
    "https://github.com/google/fonts/raw/main/ofl/worksans/WorkSans%5Bwght%5D.ttf",
    "WorkSans.ttf",
)
download_font(
    "Inter",
    "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
    "Inter.ttf",
)

# ─── Palette ──────────────────────────────────────────────────────────────────
NAVY       = HexColor("#2C3481")
NAVY_LIGHT = HexColor("#3D4BA3")
BG_ALT     = HexColor("#F5F6FA")
BORDER     = HexColor("#C8CBE0")
TEXT       = HexColor("#1E1E2E")
MUTED      = HexColor("#5A5C72")
TEAL       = HexColor("#01696F")
RED_OLD    = HexColor("#A13544")
GREEN_NEW  = HexColor("#437A22")
AMBER      = HexColor("#964219")
ROW_EVEN   = HexColor("#F0F1F8")

# ─── Styles ───────────────────────────────────────────────────────────────────
SS = getSampleStyleSheet()

def make_style(name, font="Inter", size=10, leading=15, color=TEXT,
               bold=False, space_before=0, space_after=6, indent=0,
               alignment=0):
    fn = "WorkSans-Bold" if bold else font
    return ParagraphStyle(
        name,
        fontName=fn,
        fontSize=size,
        leading=leading,
        textColor=color,
        spaceAfter=space_after,
        spaceBefore=space_before,
        leftIndent=indent,
        alignment=alignment,
    )

doc_title_style = make_style("DocTitle", bold=True, size=18, leading=22,
                              color=NAVY, space_after=3, space_before=0)
doc_subtitle_style = make_style("DocSubtitle", size=10, leading=14,
                                 color=MUTED, space_after=2)
doc_meta_style   = make_style("DocMeta", size=8.5, leading=12, color=MUTED, space_after=8)
h1_style         = make_style("H1", bold=True, size=12, leading=16,
                               color=NAVY, space_before=8, space_after=4)
h2_style         = make_style("H2", bold=True, size=10, leading=14,
                               color=NAVY, space_before=7, space_after=3)
body_style       = make_style("Body", size=9, leading=13, color=TEXT, space_after=4)
body_bold_style  = make_style("BodyBold", bold=True, size=9, leading=13,
                               color=TEXT, space_after=4)
bullet_style     = make_style("Bullet", size=9, leading=13, color=TEXT,
                               space_after=2, indent=10)
callout_style    = make_style("Callout", size=8.5, leading=12, color=MUTED,
                               space_after=3, indent=10)
label_style      = make_style("Label", bold=True, size=8, leading=11,
                               color=white)
table_hdr_style  = make_style("TblHdr", bold=True, size=8.5, leading=12,
                               color=white, space_after=0)
table_cell_style = make_style("TblCell", size=8.5, leading=12, color=TEXT,
                               space_after=0)
table_cell_old   = make_style("TblCellOld", size=8.5, leading=12, color=RED_OLD,
                               space_after=0)
table_cell_new   = make_style("TblCellNew", size=8.5, leading=12, color=GREEN_NEW,
                               space_after=0)
section_tag_style= make_style("SectionTag", bold=True, size=7, leading=10,
                               color=MUTED, space_after=1)
footer_style     = make_style("Footer", size=7.5, leading=10, color=MUTED,
                               alignment=1)

# ─── Page layout ──────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
LEFT_M = RIGHT_M = 0.85 * inch
TOP_M = 0.75 * inch
BOT_M = 0.65 * inch
CONTENT_W = PAGE_W - LEFT_M - RIGHT_M

OUTPUT = "/home/user/workspace/LIFE_system/print_ready/PICKLEBALL_CONTRACT_REVISION.pdf"

# ─── Header / Footer callback ─────────────────────────────────────────────────
def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Top bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, PAGE_H - 0.32 * inch, PAGE_W, 0.32 * inch, fill=1, stroke=0)
    canvas_obj.setFont("WorkSans-Bold", 7.5)
    canvas_obj.setFillColor(white)
    canvas_obj.drawString(LEFT_M, PAGE_H - 0.22 * inch,
                          "INTERNAL MEMO — CONFIDENTIAL")
    canvas_obj.drawRightString(PAGE_W - RIGHT_M, PAGE_H - 0.22 * inch,
                               "Honcho Pickleball — Contract Revision Analysis")
    # Bottom rule + page number
    canvas_obj.setStrokeColor(BORDER)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(LEFT_M, 0.45 * inch, PAGE_W - RIGHT_M, 0.45 * inch)
    canvas_obj.setFont("Inter", 7.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(LEFT_M, 0.3 * inch, "Prepared by Perplexity Computer")
    canvas_obj.drawRightString(PAGE_W - RIGHT_M, 0.3 * inch,
                               f"Page {doc.page}")
    canvas_obj.restoreState()

# ─── Helper: section divider ──────────────────────────────────────────────────
def section_rule():
    return HRFlowable(width="100%", thickness=0.75, color=BORDER,
                      spaceAfter=6, spaceBefore=0)

def navy_rule():
    return HRFlowable(width="100%", thickness=2, color=NAVY,
                      spaceAfter=6, spaceBefore=0)

def tag(text):
    """Small uppercase label tag above a heading."""
    return Paragraph(text.upper(), section_tag_style)

# ─── Helper: color-coded bullet ───────────────────────────────────────────────
def bullet(text, color=None):
    if color:
        return Paragraph(f'<font color="{color.hexval()}">\u2022</font>  {text}', bullet_style)
    return Paragraph(f"\u2022  {text}", bullet_style)

# ─── Build story ──────────────────────────────────────────────────────────────
story = []

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — EXECUTIVE SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

story.append(Spacer(1, 0.05 * inch))
story.append(Paragraph("Honcho Pickleball", doc_title_style))
story.append(Paragraph("Contract Revision Analysis", doc_subtitle_style))
story.append(Paragraph("Internal Memo  •  Prepared by Perplexity Computer", doc_meta_style))
story.append(navy_rule())
story.append(Spacer(1, 0.04 * inch))

# ── Current Deal Snapshot ────────────────────────────────────────────────────
story.append(tag("Section 1"))
story.append(Paragraph("Current Contract — Deal Snapshot", h1_style))
story.append(section_rule())

snap_data = [
    [Paragraph("Term", table_hdr_style),
     Paragraph("Value", table_hdr_style),
     Paragraph("Notes", table_hdr_style)],
    [Paragraph("Duration", table_cell_style),
     Paragraph("5 seasons (~50 weeks)", table_cell_style),
     Paragraph("Long-term lock with no performance triggers", table_cell_style)],
    [Paragraph("Courts", table_cell_style),
     Paragraph("2 courts", table_cell_style),
     Paragraph("Sunday only; underutilizes facility capacity", table_cell_style)],
    [Paragraph("Time Block", table_cell_style),
     Paragraph("Sunday 3:00 PM – 8:00 PM", table_cell_style),
     Paragraph("5 hours/week per court", table_cell_style)],
    [Paragraph("Rate", table_cell_style),
     Paragraph("$10/hr per court", table_cell_style),
     Paragraph("Well below market; no revenue share provision", table_cell_style)],
    [Paragraph("Weekly Revenue", table_cell_style),
     Paragraph("$100 ($10 × 2 courts × 5 hrs)", table_cell_style),
     Paragraph("Gross; no variable upside", table_cell_style)],
    [Paragraph("Per-Season Revenue", table_cell_style),
     Paragraph("~$1,000", table_cell_style),
     Paragraph("Based on ~10-week season", table_cell_style)],
    [Paragraph("Total Contract Value", table_cell_style),
     Paragraph("~$5,000", table_cell_style),
     Paragraph("Over full 5-season term", table_cell_style)],
    [Paragraph("Marketing Obligation", table_cell_style),
     Paragraph("Venue bears burden", table_cell_style),
     Paragraph("No operator marketing commitment specified", table_cell_style)],
    [Paragraph("Termination (without cause)", table_cell_style),
     Paragraph("120-day notice required", table_cell_style),
     Paragraph("Refund obligation if terminated early — critical risk", table_cell_style)],
]

snap_table = Table(snap_data, colWidths=[1.3*inch, 1.7*inch, 3.5*inch])
snap_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR",  (0, 0), (-1, 0), white),
    ("FONTNAME",   (0, 0), (-1, 0), "WorkSans-Bold"),
    ("FONTSIZE",   (0, 0), (-1, -1), 8.5),
    ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
    ("GRID",       (0, 0), (-1, -1), 0.4, BORDER),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ROW_EVEN]),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    # Highlight risk row
    ("BACKGROUND", (0, 9), (-1, 9), HexColor("#FFF0F2")),
    ("TEXTCOLOR",  (2, 9), (2, 9), RED_OLD),
]))
story.append(snap_table)
story.append(Spacer(1, 0.07 * inch))

# ── Problem Statement ─────────────────────────────────────────────────────────
story.append(tag("Section 1B"))
story.append(Paragraph("Problem Statement", h1_style))
story.append(section_rule())

story.append(Paragraph(
    "The current agreement reflects initial launch terms negotiated before operator "
    "traction was established. Four structural deficiencies expose the venue to "
    "significant revenue loss and operational risk over the full five-season term:",
    body_style))

problems = [
    ("<b>Underpriced courts.</b> At $10/hr per court, the venue earns 20–40% of market "
     "rates for activated indoor pickleball space ($25–$40/hr). Over 5 seasons this "
     "represents $12,500–$25,000 in uncaptured revenue."),
    ("<b>No revenue-share upside.</b> Player registration fees and tournament revenue flow "
     "entirely to the operator. The venue provides parking, foot traffic, F&amp;B presence, "
     "and brand visibility — yet holds zero participation in program growth."),
    ("<b>Long-term lock without performance triggers.</b> A 5-season commitment with "
     "120-day notice and a refund obligation prevents reallocation if utilization is low "
     "or a better operator emerges. Violates the rule: short-term before long-term."),
    ("<b>Marketing burden on venue.</b> Current terms do not obligate the operator to "
     "drive player acquisition — leaving promotional costs to the venue, inconsistent "
     "with courts as activation space, not merely rental space."),
]
for p in problems:
    story.append(bullet(p))

story.append(Spacer(1, 0.04 * inch))

# Owner's guiding rules — inline paragraph instead of callout box
story.append(Paragraph(
    "<i>Owner rules applied: short-term contracts before long-term; never give away "
    "multiple revenue layers; courts are activation space, not just rental space; "
    "nothing is approved until it is written and signed.</i>",
    make_style("Inline", size=8.5, leading=12, color=MUTED, space_after=6, indent=0)))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — RECOMMENDED REVISIONS
# ══════════════════════════════════════════════════════════════════════════════

story.append(Spacer(1, 0.04 * inch))
story.append(tag("Section 2"))
story.append(Paragraph("Recommended Contract Revisions", h1_style))
story.append(navy_rule())
story.append(Spacer(1, 0.03 * inch))

# Revisions as a compact two-column table
revisions_table_data = [
    [Paragraph("Area", table_hdr_style),
     Paragraph("Recommended Revision", table_hdr_style)],
    # Pricing
    [Paragraph("Pricing", make_style("RH", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "<b>Option A:</b> Increase flat rate to $25–$40/hr per court (vs. current $10/hr).  "
         "<b>Option B:</b> $10/hr base + 15–20% of gross player registration revenue. "
         "Weekly target: $250–$400 (Option A) or $100 + share (Option B). Annual target: $12,500–$20,000.",
         table_cell_style)],
    # Term
    [Paragraph("Contract Term", make_style("RH2", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "Shorten from 5 seasons to <b>2 seasons</b> with performance-gated renewal option (+1–2 seasons). "
         "Renewal requires 75% utilization AND $3,000/season gross player revenue minimum.",
         table_cell_style)],
    # Termination
    [Paragraph("Termination", make_style("RH3", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "Reduce notice from 120 to <b>60 days</b> without cause. No refund obligation when venue provides "
         "timely notice and courts remain available.",
         table_cell_style)],
    # Refund
    [Paragraph("Refund Obligation", make_style("RH4", bold=True, size=8.5, leading=12, color=RED_OLD, space_after=0)),
     Paragraph(
         "<b>CRITICAL — Eliminate or cap.</b> Pre-paid fees non-refundable after 30 days of season start. "
         "Termination for cause: no refund. Termination without cause: cap at unused pre-paid court fees only; "
         "never projected profits.",
         table_cell_style)],
    # Marketing
    [Paragraph("Marketing", make_style("RH5", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "Remove venue marketing burden. Operator solely responsible for player acquisition. "
         "Require operator co-branding (venue logo on all materials; 2 co-branded posts/month). "
         "Venue retains right to self-promote without operator approval.",
         table_cell_style)],
    # Performance
    [Paragraph("Performance Triggers", make_style("RH6", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "Utilization below 50% for 2 consecutive months → venue may reduce courts or terminate (30 days notice). "
         "Revenue below $1,500/season → venue may renegotiate rate. "
         "Quarterly attendance + revenue report due within 15 days of season end.",
         table_cell_style)],
    # Non-Exclusivity
    [Paragraph("Non-Exclusivity", make_style("RH7", bold=True, size=8.5, leading=12, color=NAVY, space_after=0)),
     Paragraph(
         "Explicit non-exclusivity: venue may contract additional operators for other time blocks "
         "or run venue-operated programs. Avoids single-partner dependency.",
         table_cell_style)],
]

rev_table = Table(revisions_table_data, colWidths=[1.35*inch, 5.15*inch])
rev_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR",     (0, 0), (-1, 0), white),
    ("FONTNAME",      (0, 0), (-1, 0), "WorkSans-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
    ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, ROW_EVEN]),
    ("TOPPADDING",    (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    # Highlight refund row
    ("BACKGROUND",    (0, 4), (-1, 4), HexColor("#FFF0F2")),
]))
story.append(rev_table)

story.append(Spacer(1, 0.08 * inch))
story.append(tag("Section 3"))
story.append(Paragraph("Current Terms vs. Proposed Terms", h1_style))
story.append(navy_rule())
story.append(Spacer(1, 0.03 * inch))

story.append(Paragraph(
    "Red = current unfavorable terms. Green = proposed improvements. "
    "All proposed terms are subject to negotiation; see fallback positions on page 4.",
    body_style))
story.append(Spacer(1, 0.03 * inch))

cmp_data = [
    # Header row
    [Paragraph("Clause", table_hdr_style),
     Paragraph("Current Terms", table_hdr_style),
     Paragraph("Proposed Terms", table_hdr_style),
     Paragraph("Priority", table_hdr_style)],
    # Pricing
    [Paragraph("Pricing", table_cell_style),
     Paragraph("$10/hr per court (flat)", table_cell_old),
     Paragraph("$25–$40/hr flat  OR  $10/hr + 15–20% player registration revenue share", table_cell_new),
     Paragraph("HIGH", body_bold_style)],
    # Term
    [Paragraph("Contract Term", table_cell_style),
     Paragraph("5 seasons (~50 weeks)", table_cell_old),
     Paragraph("2 seasons with option to renew (performance-gated)", table_cell_new),
     Paragraph("HIGH", body_bold_style)],
    # Termination
    [Paragraph("Termination\n(without cause)", table_cell_style),
     Paragraph("120-day notice required", table_cell_old),
     Paragraph("60-day notice; no refund obligation with timely notice", table_cell_new),
     Paragraph("HIGH", body_bold_style)],
    # Refund obligation
    [Paragraph("Refund Obligation", table_cell_style),
     Paragraph("Full refund if terminated early — CRITICAL RISK", table_cell_old),
     Paragraph("Non-refundable after 30 days of season start; capped at pre-paid court fees only if terminated before season start", table_cell_new),
     Paragraph("CRITICAL", body_bold_style)],
    # Marketing
    [Paragraph("Marketing Burden", table_cell_style),
     Paragraph("Venue bears promotional costs", table_cell_old),
     Paragraph("Operator responsible for all player acquisition; co-branding required", table_cell_new),
     Paragraph("MED", body_bold_style)],
    # Performance triggers
    [Paragraph("Performance Triggers", table_cell_style),
     Paragraph("None", table_cell_old),
     Paragraph("Min. 75% utilization + $3,000/season gross revenue for renewal; 50% threshold triggers court reduction", table_cell_new),
     Paragraph("HIGH", body_bold_style)],
    # Non-exclusivity
    [Paragraph("Exclusivity", table_cell_style),
     Paragraph("Not specified (implied exclusivity for time block)", table_cell_old),
     Paragraph("Explicit non-exclusivity: venue may contract additional operators for other time blocks", table_cell_new),
     Paragraph("MED", body_bold_style)],
    # Revenue share
    [Paragraph("Revenue Participation", table_cell_style),
     Paragraph("Zero — all player fees to operator", table_cell_old),
     Paragraph("15–20% of gross player registration revenue (Option B) or flat rate at market rate (Option A)", table_cell_new),
     Paragraph("HIGH", body_bold_style)],
    # Reporting
    [Paragraph("Reporting", table_cell_style),
     Paragraph("None required", table_cell_old),
     Paragraph("Quarterly attendance + revenue summary within 15 days of season end", table_cell_new),
     Paragraph("MED", body_bold_style)],
    # Indemnification
    [Paragraph("Indemnification", table_cell_style),
     Paragraph("Mutual (both directions) — retain", table_cell_style),
     Paragraph("Retain mutual indemnification; no change", table_cell_style),
     Paragraph("LOW", body_bold_style)],
    # Liability
    [Paragraph("Liability Limitation", table_cell_style),
     Paragraph("Present — retain", table_cell_style),
     Paragraph("Retain liability cap; ensure cap applies to operator refund claims", table_cell_new),
     Paragraph("MED", body_bold_style)],
    # Jurisdiction
    [Paragraph("Jurisdiction", table_cell_style),
     Paragraph("Texas — retain", table_cell_style),
     Paragraph("Texas — no change", table_cell_style),
     Paragraph("LOW", body_bold_style)],
    # Independent contractor
    [Paragraph("Relationship", table_cell_style),
     Paragraph("Independent contractor — retain", table_cell_style),
     Paragraph("Independent contractor — no change", table_cell_style),
     Paragraph("LOW", body_bold_style)],
]

cmp_table = Table(cmp_data, colWidths=[1.1*inch, 2.0*inch, 2.85*inch, 0.55*inch])
cmp_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR",     (0, 0), (-1, 0), white),
    ("FONTNAME",      (0, 0), (-1, 0), "WorkSans-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8),
    ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, ROW_EVEN]),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    # CRITICAL row highlight
    ("BACKGROUND",    (0, 4), (-1, 4), HexColor("#FFF0F2")),
    # Priority column centering
    ("ALIGN",         (3, 0), (3, -1), "CENTER"),
    # Color-code priority column
    ("TEXTCOLOR",     (3, 1), (3, 3),  RED_OLD),   # HIGH rows 1-3
    ("TEXTCOLOR",     (3, 4), (3, 4),  RED_OLD),   # CRITICAL
    ("TEXTCOLOR",     (3, 5), (3, 8),  AMBER),     # MED/HIGH
    ("TEXTCOLOR",     (3, 9), (3, 10), AMBER),     # MED
    ("TEXTCOLOR",     (3, 11),(3, 13), HexColor("#5A5C72")),  # LOW
    ("FONTNAME",      (3, 1), (3, -1), "WorkSans-Bold"),
    ("FONTSIZE",      (3, 1), (3, -1), 8),
]))
story.append(cmp_table)

story.append(Spacer(1, 0.1 * inch))
story.append(tag("Section 4"))
story.append(Paragraph("Negotiation Strategy &amp; Next Steps", h1_style))
story.append(navy_rule())
story.append(Spacer(1, 0.02 * inch))

# ── Leverage Points ───────────────────────────────────────────────────────────
story.append(Paragraph("4A  |  Venue Leverage Points", h2_style))
story.append(Paragraph(
    "The venue holds meaningful leverage that should be named in negotiations:",
    body_style))

leverage = [
    ("<b>Parking and access.</b> On-site parking is a scarce resource for recreational "
     "sports programs. Competing facilities often charge for parking or lack adequate supply."),
    ("<b>Built-in foot traffic.</b> Existing venue visitors (food &amp; beverage, fitness, "
     "events) provide organic player discovery — a value the operator receives for free."),
    ("<b>Brand association and visibility.</b> The venue's established reputation reduces "
     "the operator's marketing cost of trust-building in the local market."),
    ("<b>Facility infrastructure.</b> HVAC, restrooms, lighting, and maintenance are "
     "provided. Comparable standalone pickleball facilities charge $25–$45/hr and "
     "pass all overhead to players."),
    ("<b>Flexible scheduling upside.</b> Venue can offer additional time blocks or "
     "tournament day rentals — a bargaining chip for rate negotiation."),
]
for l in leverage:
    story.append(bullet(l, TEAL))
story.append(Spacer(1, 0.04 * inch))

# ── Fallback Positions ────────────────────────────────────────────────────────
story.append(Paragraph("4B  |  Fallback Positions by Clause", h2_style))

fb_data = [
    [Paragraph("Clause", table_hdr_style),
     Paragraph("Ideal Ask", table_hdr_style),
     Paragraph("Acceptable Fallback", table_hdr_style),
     Paragraph("Walk-Away Line", table_hdr_style)],
    [Paragraph("Court Rate", table_cell_style),
     Paragraph("$35–$40/hr", table_cell_style),
     Paragraph("$25/hr flat or $10 + 18% rev share", table_cell_style),
     Paragraph("Below $20/hr flat with no share", table_cell_style)],
    [Paragraph("Contract Term", table_cell_style),
     Paragraph("2 seasons", table_cell_style),
     Paragraph("3 seasons with annual exit option", table_cell_style),
     Paragraph("5 seasons without exit/trigger clauses", table_cell_style)],
    [Paragraph("Termination Notice", table_cell_style),
     Paragraph("60 days", table_cell_style),
     Paragraph("90 days with no refund obligation", table_cell_style),
     Paragraph("120 days + full refund on early exit", table_cell_style)],
    [Paragraph("Refund Obligation", table_cell_style),
     Paragraph("Eliminated entirely", table_cell_style),
     Paragraph("Capped at pre-paid court fees, 30-day window only", table_cell_style),
     Paragraph("Full profit guarantee refund", table_cell_style)],
    [Paragraph("Revenue Share", table_cell_style),
     Paragraph("20% of gross player fees", table_cell_style),
     Paragraph("15% after $5,000 threshold", table_cell_style),
     Paragraph("Flat rate below $20/hr with zero share", table_cell_style)],
    [Paragraph("Performance Trigger", table_cell_style),
     Paragraph("75% utilization + $3K/season", table_cell_style),
     Paragraph("60% utilization + $2K/season", table_cell_style),
     Paragraph("No trigger clauses at any term length", table_cell_style)],
]

fb_table = Table(fb_data, colWidths=[1.1*inch, 1.55*inch, 1.95*inch, 1.9*inch])
fb_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, 0), NAVY),
    ("TEXTCOLOR",     (0, 0), (-1, 0), white),
    ("FONTNAME",      (0, 0), (-1, 0), "WorkSans-Bold"),
    ("FONTSIZE",      (0, 0), (-1, -1), 8),
    ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
    ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
    ("ROWBACKGROUNDS",(0, 1), (-1, -1), [white, ROW_EVEN]),
    ("TOPPADDING",    (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LEFTPADDING",   (0, 0), (-1, -1), 5),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    # Walk-away column in red
    ("TEXTCOLOR",     (3, 1), (3, -1), RED_OLD),
    ("FONTNAME",      (3, 1), (3, -1), "WorkSans-Bold"),
    ("FONTSIZE",      (3, 0), (3, -1), 8),
]))
story.append(fb_table)
story.append(Spacer(1, 0.04 * inch))

# ── Next Steps ────────────────────────────────────────────────────────────────
story.append(Paragraph("4C  |  Recommended Next Steps", h2_style))

steps = [
    ("<b>Step 1 — Legal review.</b> All proposed revisions must be reviewed and drafted by "
     "Texas-licensed counsel. Nothing approved until written and signed."),
    ("<b>Step 2 — Operator outreach.</b> Schedule renewal discussion 60–90 days before "
     "agreement end. Frame as 'partnership review,' not adversarial renegotiation."),
    ("<b>Step 3 — Rate research.</b> Collect 3–5 comparable pickleball court rental rates "
     "in local market as evidence for the $25–$40/hr ask."),
    ("<b>Step 4 — Parallel operator options.</b> Identify 1–2 alternative operators. "
     "Do not reveal, but use as internal leverage. Avoids single-partner dependency."),
    ("<b>Step 5 — Confirm refund exposure.</b> Audit pre-paid fees collected and calculate "
     "maximum current refund obligation — most urgent financial risk."),
    ("<b>Step 6 — Redline and counter.</b> Present formal redline. No verbal commitments. "
     "All changes written, reviewed, and signed."),
]
for i, s in enumerate(steps, 1):
    story.append(bullet(s, NAVY_LIGHT))

story.append(Spacer(1, 0.04 * inch))

# Financial upside summary box
upside_data = [[
    Paragraph(
        "<b>Financial Upside Summary:</b>  Current total contract value ~$5,000 over 5 seasons.  "
        "Option A at $25/hr: ~$12,500/season × 2 seasons = $25,000 total (+400%).  "
        "Option B at $10 + 18% share on $5,000/season player revenue: ~$5,900/season × 2 seasons = $11,800 (+136%) with growth upside.  "
        "Either path recovers the revenue gap within the first renegotiated season.",
        callout_style)
]]
upside_table = Table(upside_data, colWidths=[CONTENT_W])
upside_table.setStyle(TableStyle([
    ("BACKGROUND",    (0, 0), (-1, -1), HexColor("#EDF8F0")),
    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
    ("TOPPADDING",    (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ("BOX",           (0, 0), (-1, -1), 1.5, TEAL),
]))
story.append(upside_table)

# ─── Build PDF ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    title="Honcho Pickleball — Contract Revision Analysis",
    author="Perplexity Computer",
    leftMargin=LEFT_M,
    rightMargin=RIGHT_M,
    topMargin=TOP_M + 0.35 * inch,  # account for header bar
    bottomMargin=BOT_M + 0.2 * inch,
)

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF written to: {OUTPUT}")
