"""
Build LIFE System Master PDF
Converts LIFE_SYSTEM_MASTER.md into a professional print-ready PDF (LIFE System Master).
"""

import re
import os
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether, Flowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Brand Colors ──────────────────────────────────────────────────────────────
NAVY   = HexColor("#2C3481")
TEAL   = HexColor("#00AAAD")
DARK   = HexColor("#1A1A1A")
MUTED  = HexColor("#666666")
LIGHT  = HexColor("#F5F6FA")
WHITE  = HexColor("#FFFFFF")
STRIPE = HexColor("#EEF0F8")  # alternating table row

# ── Font Registration ─────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")

def register_fonts():
    # Static font instances (properly extracted from variable fonts)
    fonts = [
        ("Inter",           FONT_DIR / "Inter-Regular.ttf"),
        ("Inter-Bold",      FONT_DIR / "Inter-Bold.ttf"),
        ("Inter-SemiBold",  FONT_DIR / "Inter-SemiBold.ttf"),
        ("DMSans",          FONT_DIR / "DMSans-Static-Regular.ttf"),
        ("DMSans-Bold",     FONT_DIR / "DMSans-Static-SemiBold.ttf"),
        ("DMSans-Medium",   FONT_DIR / "DMSans-Static-Medium.ttf"),
    ]
    for name, path in fonts:
        if path.exists():
            pdfmetrics.registerFont(TTFont(name, str(path)))
            print(f"  Registered: {name}")
        else:
            print(f"  MISSING: {name} at {path}")

    # Register font families for bold/italic markup
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("Inter", normal="Inter", bold="Inter-Bold",
                       italic="Inter", boldItalic="Inter-Bold")
    registerFontFamily("DMSans", normal="DMSans", bold="DMSans-Bold",
                       italic="DMSans", boldItalic="DMSans-Bold")

register_fonts()

# ── Page Setup ────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter   # 612 x 792 pts
MARGIN = 0.75 * inch
CONTENT_W = PAGE_W - 2 * MARGIN
CONTENT_H = PAGE_H - 2 * MARGIN

OUT_PATH = "/home/user/workspace/LIFE_system/print_ready/LIFE_SYSTEM_MASTER.pdf"
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    s = {}

    s["body"] = ParagraphStyle(
        "body",
        fontName="Inter", fontSize=11, leading=16,
        textColor=DARK, spaceAfter=6, spaceBefore=2,
        alignment=TA_LEFT,
    )
    s["body_small"] = ParagraphStyle(
        "body_small", parent=s["body"],
        fontSize=9, leading=13, spaceAfter=4,
    )
    s["body_bold"] = ParagraphStyle(
        "body_bold", parent=s["body"],
        fontName="Inter-Bold",
    )
    s["muted"] = ParagraphStyle(
        "muted", parent=s["body"],
        textColor=MUTED, fontSize=10, leading=14,
    )

    # Headings
    s["h1"] = ParagraphStyle(
        "h1", fontName="DMSans-Bold", fontSize=22, leading=28,
        textColor=NAVY, spaceBefore=18, spaceAfter=8,
        alignment=TA_LEFT,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="DMSans-Bold", fontSize=16, leading=22,
        textColor=NAVY, spaceBefore=14, spaceAfter=6,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="DMSans-Bold", fontSize=13, leading=18,
        textColor=NAVY, spaceBefore=10, spaceAfter=4,
    )
    s["h4"] = ParagraphStyle(
        "h4", fontName="DMSans-Medium", fontSize=11, leading=16,
        textColor=DARK, spaceBefore=8, spaceAfter=3,
    )

    # Part title (for section covers)
    s["part_title"] = ParagraphStyle(
        "part_title", fontName="DMSans-Bold", fontSize=24, leading=30,
        textColor=WHITE, alignment=TA_LEFT,
    )
    s["part_subtitle"] = ParagraphStyle(
        "part_subtitle", fontName="DMSans", fontSize=14, leading=20,
        textColor=HexColor("#C0C4E8"), alignment=TA_LEFT,
    )

    # Rule number (large teal number)
    s["rule_num"] = ParagraphStyle(
        "rule_num", fontName="DMSans-Bold", fontSize=36, leading=40,
        textColor=TEAL, spaceAfter=4,
    )

    # Blockquote / callout
    s["quote"] = ParagraphStyle(
        "quote", parent=s["body"],
        fontName="Inter", fontSize=10.5, leading=15,
        textColor=HexColor("#444466"),
        leftIndent=16, rightIndent=8,
        spaceAfter=8, spaceBefore=4,
        borderPad=8,
    )

    # Bullet list
    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"],
        leftIndent=18, firstLineIndent=-12,
        spaceAfter=3,
    )
    s["bullet2"] = ParagraphStyle(
        "bullet2", parent=s["bullet"],
        leftIndent=32, firstLineIndent=-12,
    )

    # Code block / monospace
    s["code"] = ParagraphStyle(
        "code", fontName="Inter", fontSize=9, leading=13,
        textColor=DARK, backColor=HexColor("#F0F0F8"),
        leftIndent=12, rightIndent=12,
        spaceBefore=4, spaceAfter=4,
    )

    # Table header
    s["table_hdr"] = ParagraphStyle(
        "table_hdr", fontName="DMSans-Bold", fontSize=10, leading=13,
        textColor=WHITE,
    )
    s["table_cell"] = ParagraphStyle(
        "table_cell", fontName="Inter", fontSize=9.5, leading=13,
        textColor=DARK,
    )

    # Sign-off line label
    s["signoff_label"] = ParagraphStyle(
        "signoff_label", fontName="Inter", fontSize=10, leading=14,
        textColor=MUTED,
    )

    # Cover styles
    s["cover_title"] = ParagraphStyle(
        "cover_title", fontName="DMSans-Bold", fontSize=40, leading=46,
        textColor=WHITE, alignment=TA_LEFT, spaceBefore=0, spaceAfter=6,
    )
    s["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontName="DMSans", fontSize=16, leading=22,
        textColor=HexColor("#9AA0D4"), alignment=TA_LEFT,
    )
    s["cover_facility"] = ParagraphStyle(
        "cover_facility", fontName="Inter", fontSize=13, leading=18,
        textColor=HexColor("#C0C4E8"), alignment=TA_LEFT,
    )
    s["cover_meta"] = ParagraphStyle(
        "cover_meta", fontName="Inter", fontSize=11, leading=16,
        textColor=HexColor("#8890C4"), alignment=TA_LEFT,
    )

    # TOC / How To Use intro
    s["intro"] = ParagraphStyle(
        "intro", parent=s["body"],
        fontSize=12, leading=18, spaceAfter=8, spaceBefore=4,
        textColor=DARK,
    )

    # Do Not List item
    s["dont"] = ParagraphStyle(
        "dont", parent=s["body"],
        fontName="Inter-Bold", textColor=HexColor("#8B1A1A"),
        leftIndent=18, firstLineIndent=-12, spaceAfter=4,
    )

    return s

STYLES = make_styles()

# ── Custom Flowables ──────────────────────────────────────────────────────────


# Global page map for two-pass TOC page numbering
PAGE_MAP = {}

class PageRecorder(Flowable):
    """Zero-size flowable that records which page it lands on."""
    _fixedWidth = 0
    _fixedHeight = 0
    width = 0
    height = 0

    def __init__(self, key):
        Flowable.__init__(self)
        self.key = key

    def draw(self):
        PAGE_MAP[self.key] = self.canv.getPageNumber()

    def wrap(self, availWidth, availHeight):
        return (0, 0)

class NavyHeaderBar(Flowable):
    """Full-width navy background bar with white title text."""
    def __init__(self, part_label, title, width=CONTENT_W):
        super().__init__()
        self.part_label = part_label
        self.title = title
        self.width = width
        self.height = 80

    def wrap(self, avW, avH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # Background
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # Teal accent stripe on left
        c.setFillColor(TEAL)
        c.rect(0, 0, 5, self.height, fill=1, stroke=0)
        # Part label (small, top-left)
        c.setFillColor(HexColor("#9AA0D4"))
        c.setFont("DMSans", 10)
        c.drawString(16, self.height - 22, self.part_label)
        # Title — auto-size to fit within bar
        max_w = self.width - 32  # 16px padding each side
        font_size = 20
        while font_size > 12:
            tw = c.stringWidth(self.title, "DMSans-Bold", font_size)
            if tw <= max_w:
                break
            font_size -= 1
        c.setFillColor(WHITE)
        c.setFont("DMSans-Bold", font_size)
        c.drawString(16, 18, self.title)
        c.restoreState()


class TealDivider(Flowable):
    """Thin teal horizontal rule."""
    def __init__(self, width=CONTENT_W, thickness=1.5):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.height = self.thickness + 4

    def wrap(self, avW, avH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(TEAL)
        c.setLineWidth(self.thickness)
        c.line(0, self.thickness / 2, self.width, self.thickness / 2)
        c.restoreState()


class RuleBlock(Flowable):
    """A numbered rule block with navy left bar."""
    def __init__(self, number, title, body_text, width=CONTENT_W):
        super().__init__()
        self.number = number
        self.title = title
        self.body_text = body_text
        self.width = width
        self._para = None
        self._title_para = None
        self._h = None

    def _build_paras(self):
        if self._para is None:
            self._title_para = Paragraph(
                f"Rule {self.number}: {self.title}", STYLES["h3"])
            self._para = Paragraph(self.body_text, STYLES["body"])

    def wrap(self, avW, avH):
        self._build_paras()
        tw = self.width - 24  # account for left bar + padding
        _, th = self._title_para.wrap(tw, avH)
        _, bh = self._para.wrap(tw, avH)
        self._h = th + bh + 20
        return self.width, self._h

    def draw(self):
        self._build_paras()
        c = self.canv
        c.saveState()
        h = self._h
        # Left navy bar
        c.setFillColor(NAVY)
        c.rect(0, 0, 4, h, fill=1, stroke=0)
        # Light background
        c.setFillColor(HexColor("#F5F6FA"))
        c.rect(4, 0, self.width - 4, h, fill=1, stroke=0)
        # Rule number (teal, top right)
        c.setFillColor(TEAL)
        c.setFont("DMSans-Bold", 28)
        c.drawRightString(self.width - 8, h - 32, str(self.number))
        # Title
        tw = self.width - 24
        _, th = self._title_para.wrap(tw, h)
        self._title_para.drawOn(c, 12, h - th - 8)
        # Body
        _, bh = self._para.wrap(tw, h)
        self._para.drawOn(c, 12, 8)
        c.restoreState()


class CalloutBox(Flowable):
    """A teal-accented callout / blockquote box."""
    def __init__(self, text, width=CONTENT_W):
        super().__init__()
        self.text = text
        self.width = width
        self._para = None
        self._h = None

    def _build(self):
        if self._para is None:
            self._para = Paragraph(self.text, STYLES["quote"])

    def wrap(self, avW, avH):
        self._build()
        _, ph = self._para.wrap(self.width - 28, avH)
        self._h = ph + 16
        return self.width, self._h

    def draw(self):
        self._build()
        c = self.canv
        c.saveState()
        # Background
        c.setFillColor(HexColor("#EEF0F8"))
        c.roundRect(0, 0, self.width, self._h, 4, fill=1, stroke=0)
        # Left teal stripe
        c.setFillColor(TEAL)
        c.roundRect(0, 0, 4, self._h, 2, fill=1, stroke=0)
        # Text
        _, ph = self._para.wrap(self.width - 28, self._h)
        self._para.drawOn(c, 14, (self._h - ph) / 2)
        c.restoreState()


# ── Header / Footer callbacks ─────────────────────────────────────────────────

def cover_page(canvas, doc):
    """First page: full navy background cover."""
    canvas.saveState()
    w, h = PAGE_W, PAGE_H
    # Full background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Teal accent bar at bottom
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, w, 6, fill=1, stroke=0)
    # Top teal stripe
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 6, w, 6, fill=1, stroke=0)
    canvas.restoreState()


def later_pages(canvas, doc):
    """Header + footer for all pages after cover."""
    canvas.saveState()
    w, h = PAGE_W, PAGE_H

    # ── Top header bar ──
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 28, w, 28, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 28, 4, 28, fill=1, stroke=0)

    canvas.setFont("DMSans-Bold", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(MARGIN, h - 18, "THE LIFE SYSTEM MASTER")
    canvas.setFont("Inter", 7.5)
    canvas.setFillColor(HexColor("#9AA0D4"))
    canvas.drawRightString(w - MARGIN, h - 18,
                           "San Antonio Aquarium | Houston Interactive Aquarium | Austin Aquarium")

    # ── Bottom footer ──
    canvas.setStrokeColor(HexColor("#D0D4E8"))
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 30, w - MARGIN, 30)

    canvas.setFont("Inter", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 18, "Confidential — Internal Use Only")
    canvas.drawString(MARGIN, 8, "Owner: Family Fun Group | Author: Ammon Covino | Effective: April 2026")

    # Page number
    canvas.setFont("DMSans-Bold", 9)
    canvas.setFillColor(NAVY)
    canvas.drawRightString(w - MARGIN, 18, f"Page {doc.page}")

    canvas.restoreState()


# ── Markdown Parser → Flowables ───────────────────────────────────────────────

# Unicode sanitization — replace emojis/symbols not in Inter/DMSans with safe text
UNICODE_MAP = {
    '\U0001F537': '*',       # 🔷 blue diamond → bullet
    '\U0001F449': '>>',      # 👉 pointing right → arrows
    '\U0001F33E': '[grain]', # 🌾 sheaf of rice
    '\U0001F33F': '[leaf]',  # 🌿 herb
    '\U0001F34E': '[fruit]', # 🍎 red apple
    '\U0001F952': '[veggie]',# 🥒 cucumber
    '\U0001F954': '[tuber]', # 🥔 potato
    '\U0001F6AB': '[X]',     # 🚫 prohibited
    '\U0001F7E4': '*',       # 🟤 brown circle
    '\U0001F5FA': '[map]',   # 🗺 world map
    '\u27A1': '>>',          # ➡ right arrow
    '\uFE0F': '',            # variation selector — strip
    '\u2714': '[Y]',         # ✔ check mark
    '\u2716': '[X]',         # ✖ heavy multiplication X
    '\u2190': '<<',          # ← left arrow
}

def sanitize_unicode(text):
    """Replace emojis and unsupported glyphs with text-safe equivalents."""
    for char, replacement in UNICODE_MAP.items():
        text = text.replace(char, replacement)
    return text


def escape_xml(text):
    """Escape XML special chars but preserve intended markup."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def process_inline(text):
    """
    Convert markdown inline formatting to ReportLab XML markup.
    Order matters: handle ** before *.
    """
    # Escape XML first
    text = text.replace("&", "&amp;")

    # Bold+italic ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic *text* or _text_
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Inline code `code`
    text = re.sub(r'`([^`]+)`',
                  r'<font name="Inter" size="9" color="#2C3481">\1</font>', text)
    # Em dashes
    text = text.replace(" — ", " \u2014 ")
    # Smart quotes already in source — just pass through

    # Fix any dangling & that weren't part of &amp;
    # (shouldn't occur after the escape above)
    return text


def make_table(headers, rows):
    """Build a styled ReportLab Table from header + data rows."""
    # Wrap header cells in Paragraphs
    hdr_cells = [Paragraph(process_inline(h), STYLES["table_hdr"]) for h in headers]
    data = [hdr_cells]
    for row in rows:
        data.append([Paragraph(process_inline(c), STYLES["table_cell"]) for c in row])

    # Distribute column widths equally
    n_cols = len(headers)
    col_w = CONTENT_W / n_cols

    tbl = Table(data, colWidths=[col_w] * n_cols, repeatRows=1)
    row_count = len(data)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR",  (0, 0), (-1, 0), WHITE),
        ("FONTNAME",   (0, 0), (-1, 0), "DMSans-Bold"),
        ("FONTSIZE",   (0, 0), (-1, 0), 10),
        ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("GRID",       (0, 0), (-1, -1), 0.4, HexColor("#C8CCDD")),
    ]
    # Alternating rows
    for i in range(1, row_count):
        bg = STRIPE if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def parse_markdown_table(lines):
    """Parse a markdown table block into (headers, rows)."""
    headers = []
    rows = []
    for i, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.match(r'^[-:]+$', c) for c in cells if c):
            continue  # separator row
        if not headers:
            headers = cells
        else:
            rows.append(cells)
    return headers, rows


def build_story(md_text):
    """Parse markdown and produce a list of Platypus flowables."""
    story = []
    lines = md_text.splitlines()

    # ── Cover Page Flowables ──
    # We push a special marker spacer so cover_page() callback draws the bg,
    # then we overlay content using canvas drawOn.
    # Instead, we use a large Spacer + direct canvas drawing in cover_page.
    # The cover content is drawn entirely in cover_page callback via a
    # special flag, so we just need content positioned correctly.

    # Build cover manually with Paragraphs on navy background
    # The cover page callback draws the background; we add content as flowables.
    story.append(Spacer(1, 1.6 * inch))
    story.append(Paragraph("THE LIFE SYSTEM MASTER", STYLES["cover_title"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Complete Operational &amp; Education Reference",
                            STYLES["cover_subtitle"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(TealDivider(width=CONTENT_W * 0.4, thickness=2))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("San Antonio Aquarium",
                            STYLES["cover_facility"]))
    story.append(Paragraph("Houston Interactive Aquarium &amp; Animal Preserve",
                            STYLES["cover_facility"]))
    story.append(Paragraph("Austin Aquarium",
                            STYLES["cover_facility"]))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Owner: Family Fun Group | Author: Ammon Covino", STYLES["cover_meta"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("Effective: April 2026", STYLES["cover_meta"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "This document replaces all previous systems, checklists, and procedures.",
        STYLES["cover_meta"]))
    # ── Table of Contents Page ──
    story.append(PageBreak())
    story.append(Spacer(1, 0.1 * inch))
    story.append(NavyHeaderBar("", "TABLE OF CONTENTS"))
    story.append(Spacer(1, 0.15 * inch))

    toc_style = ParagraphStyle(
        "toc_item", fontName="Inter", fontSize=9.5, leading=13,
        textColor=DARK, spaceAfter=1, spaceBefore=1,
    )
    toc_front_style = ParagraphStyle(
        "toc_front", fontName="Inter", fontSize=9.5, leading=13,
        textColor=MUTED, spaceAfter=1, spaceBefore=1,
    )

    # Front matter
    story.append(Paragraph("How to Use This Document", toc_front_style))
    story.append(Paragraph("Role Index", toc_front_style))
    story.append(Spacer(1, 0.06 * inch))
    story.append(TealDivider(width=CONTENT_W * 0.25, thickness=1))
    story.append(Spacer(1, 0.06 * inch))

    toc_parts = [
        ("Part 1",  "The Owner\u2019s Top Ten: Operational Standards"),
        ("Part 2",  "The Owner\u2019s Top Ten: Guest-Facing Standards"),
        ("Part 3",  "How We Work Here"),
        ("Part 4",  "Animal Care and Diet"),
        ("Part 5",  "Cleaning and Maintenance"),
        ("Part 6",  "The Zero Waste Food Loop"),
        ("Part 7",  "Exhibit-Specific Feeding Addendums"),
        ("Part 8",  "Diet Verification &amp; Enforcement"),
        ("Part 9",  "The Do Not List"),
        ("Part 10", "Sign-Off"),
        ("Part 11", "The Education System: LIFE"),
        ("Part 12", "Signage and Totems (Reference)"),
        ("Part 13", "Species Totems: Master Collection"),
        ("Part 14", "Narration Suites: Complete System"),
        ("Part 15", "Business and Revenue Systems"),
        ("Part 16", "Operational Spine: Core Systems Governance"),
        ("Part 17", "Studio Giraffe Venue System"),
        ("Part 18", "Role-Based Operational Packets"),
        ("Part 19", "Houston Operations SOP: Clarity &amp; Authority"),
        ("Part 20", "Terminology"),
        ("Part 21", "Key Decisions and Why"),
        ("Part 22", "System Architecture"),
        ("Part 23", "Signage System: Replacement Map"),
        ("Part 24", "Education Spine: Extended Framework"),
        ("Part 25", "Operator Roles &amp; School-Safe Materials"),
        ("Part 26", "Foundational Artifact Library (Reference Only)"),
    ]

    # TOC style with dot leaders and page numbers
    toc_with_page_style = ParagraphStyle(
        "toc_with_page", fontName="Inter", fontSize=9.5, leading=13,
        textColor=DARK, spaceAfter=1, spaceBefore=1,
    )

    for part_num, part_title in toc_parts:
        # Extract the PART key for page lookup (e.g., "Part 1" -> "PART 1")
        part_key = part_num.upper()
        page_num = PAGE_MAP.get(part_key, "")
        page_str = f'<font name="Inter" size="9" color="#666666"> {"·" * 3} p.{page_num}</font>' if page_num else ""
        story.append(Paragraph(
            f'<font name="DMSans-Bold" size="9.5" color="#2C3481">{part_num}</font>'
            f'<font name="Inter" size="9.5" color="#1A1A1A"> \u2014 {part_title}</font>'
            f'{page_str}',
            toc_with_page_style))

    # ── Parse body ──
    i = 0
    in_table = False
    table_lines = []
    in_code = False
    code_lines = []
    current_part = ""

    # Skip title block (already on cover)
    # Find where actual content starts (after the first ---)
    start_idx = 0
    dash_count = 0
    for idx, line in enumerate(lines):
        if line.strip() == "---":
            dash_count += 1
            if dash_count == 2:
                start_idx = idx + 1
                break

    lines = lines[start_idx:]

    def flush_table():
        nonlocal table_lines, in_table
        if table_lines:
            hdrs, rows = parse_markdown_table(table_lines)
            if hdrs:
                story.append(Spacer(1, 0.1 * inch))
                story.append(make_table(hdrs, rows))
                story.append(Spacer(1, 0.1 * inch))
        table_lines = []
        in_table = False

    def flush_code():
        nonlocal code_lines, in_code
        if code_lines:
            txt = "<br/>".join(escape_xml(l) for l in code_lines)
            story.append(Paragraph(txt, STYLES["code"]))
        code_lines = []
        in_code = False

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Code blocks ──
        if stripped.startswith("```"):
            if in_code:
                flush_code()
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # ── Table detection ──
        if stripped.startswith("|"):
            in_table = True
            table_lines.append(stripped)
            i += 1
            continue
        elif in_table:
            flush_table()

        # ── Horizontal rule ──
        if stripped == "---":
            story.append(Spacer(1, 0.06 * inch))
            story.append(HRFlowable(width=CONTENT_W, thickness=0.5,
                                    color=HexColor("#D0D4E8"), spaceAfter=6))
            i += 1
            continue

        # ── Page break for PART headers (# PART N) ──
        if re.match(r'^# PART \d+', stripped) or re.match(r'^# PART \d+ —', stripped):
            # Extract part label and title
            m = re.match(r'^# (PART \d+)[— ]*(.*)$', stripped)
            if m:
                part_label = m.group(1).strip()
                part_title = m.group(2).strip(" —").strip()
                current_part = f"{part_label}: {part_title}" if part_title else part_label
            else:
                current_part = stripped.lstrip("# ").strip()
                part_label = current_part
                part_title = ""

            story.append(PageBreak())
            story.append(PageRecorder(part_label))  # Record page number for TOC
            story.append(Spacer(1, 0.05 * inch))
            story.append(NavyHeaderBar(part_label, part_title or part_label))
            story.append(Spacer(1, 0.2 * inch))
            i += 1
            continue

        # ── HOW TO USE, ROLE INDEX, system-level headings ──
        if re.match(r'^# (HOW TO USE|ROLE INDEX)', stripped):
            title = stripped.lstrip("# ").strip()
            story.append(PageBreak())
            story.append(Spacer(1, 0.05 * inch))
            story.append(NavyHeaderBar("", title))
            story.append(Spacer(1, 0.2 * inch))
            i += 1
            continue

        # ── General H1 ──
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(process_inline(text), STYLES["h1"]))
            story.append(TealDivider())
            i += 1
            continue

        # ── H2 ──
        if stripped.startswith("## "):
            text = stripped[3:].strip()
            story.append(Spacer(1, 0.08 * inch))
            story.append(Paragraph(process_inline(text), STYLES["h2"]))
            i += 1
            continue

        # ── H3 ──
        if stripped.startswith("### "):
            text = stripped[4:].strip()
            story.append(Paragraph(process_inline(text), STYLES["h3"]))
            i += 1
            continue

        # ── H4 ──
        if stripped.startswith("#### "):
            text = stripped[5:].strip()
            story.append(Paragraph(process_inline(text), STYLES["h4"]))
            i += 1
            continue

        # ── Blockquote > ──
        if stripped.startswith(">"):
            # Collect consecutive blockquote lines
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                bq_lines.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            combined = " ".join(bq_lines)
            story.append(CalloutBox(process_inline(combined)))
            continue

        # ── Unordered list ──
        if re.match(r'^[-*] ', stripped):
            text = stripped[2:].strip()
            # Sub-indent check
            indent = len(line) - len(line.lstrip())
            if indent >= 4:
                style = STYLES["bullet2"]
            else:
                style = STYLES["bullet"]
            # Special: Do Not List items
            if stripped.startswith("- **Do not**"):
                story.append(Paragraph(
                    "\u2022 " + process_inline(text), STYLES["dont"]))
            else:
                story.append(Paragraph(
                    "\u2022 " + process_inline(text), style))
            i += 1
            continue

        # ── Numbered list ──
        m = re.match(r'^(\d+)\. (.+)$', stripped)
        if m:
            num = m.group(1)
            text = m.group(2).strip()
            story.append(Paragraph(
                f"{num}. {process_inline(text)}", STYLES["bullet"]))
            i += 1
            continue

        # ── Bold standalone line (used as sub-rule headers like **Rule 1:** ...) ──
        # Part rule headers: ## Rule N: title pattern
        m = re.match(r'^## Rule (\d+): (.+)$', stripped)
        if m:
            rule_num = int(m.group(1))
            rule_title = m.group(2).strip()
            # Collect the explanation paragraphs that follow
            i += 1
            body_parts = []
            # Skip a blank line
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            # Collect rule italicized subtitle (first non-blank line after heading)
            subtitle = ""
            if i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                subtitle = lines[i].strip()
                i += 1
            # Skip blank
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            # Collect body paragraphs until next ## or #
            while i < len(lines):
                l = lines[i].strip()
                if l.startswith("#"):
                    break
                if l == "---":
                    break
                body_parts.append(l)
                i += 1
            body_text = " ".join(p for p in body_parts if p)

            # Build rule block
            full_title = rule_title
            full_body = subtitle + ("\n\n" if subtitle and body_text else "") + body_text
            # Use a compact card
            elements = [
                Spacer(1, 6),
                Paragraph(f"<b>Rule {rule_num}: {process_inline(rule_title)}</b>",
                          STYLES["h3"]),
            ]
            if subtitle:
                elements.append(Paragraph(
                    f"<i>{process_inline(subtitle)}</i>", STYLES["muted"]))
            if body_text:
                elements.append(Paragraph(process_inline(body_text), STYLES["body"]))
            elements.append(Spacer(1, 4))
            story.append(KeepTogether(elements))
            continue

        # ── Step headers: ### Step N — ──
        m = re.match(r'^### Step (\d+)[— ]+(.+)$', stripped)
        if m:
            step_num = m.group(1)
            step_title = m.group(2).strip()
            story.append(Paragraph(
                f"<b>Step {step_num} — {process_inline(step_title)}</b>",
                STYLES["h3"]))
            i += 1
            continue

        # ── Stage headers: ### Stage N — ──
        m = re.match(r'^### Stage (\d+)[— ]+(.+)$', stripped)
        if m:
            stage_num = m.group(1)
            stage_title = m.group(2).strip()
            story.append(Paragraph(
                f"<b>Stage {stage_num} — {process_inline(stage_title)}</b>",
                STYLES["h3"]))
            i += 1
            continue

        # ── Bold block (**Text:** explanation pattern) ──
        m = re.match(r'^\*\*(.+?)\*\*[:.]?\s*(.*)', stripped)
        if m and stripped.startswith("**"):
            label = m.group(1).strip()
            rest = m.group(2).strip()
            if rest:
                story.append(Paragraph(
                    f"<b>{process_inline(label)}:</b> {process_inline(rest)}",
                    STYLES["body"]))
            else:
                story.append(Paragraph(
                    f"<b>{process_inline(label)}</b>", STYLES["body_bold"]))
            i += 1
            continue

        # ── Empty line ──
        if not stripped:
            story.append(Spacer(1, 0.04 * inch))
            i += 1
            continue

        # ── Default: body paragraph ──
        story.append(Paragraph(process_inline(stripped), STYLES["body"]))
        i += 1

    # Flush any remaining table/code
    if in_table:
        flush_table()
    if in_code:
        flush_code()

    return story


# ── Sign-Off Page ─────────────────────────────────────────────────────────────

def add_signoff_page(story):
    """
    The sign-off part (PART 10) already parsed from markdown, but we add
    a rich formatted version with actual signature lines.
    """
    story.append(PageBreak())
    story.append(PageRecorder("PART 10"))  # Record page for TOC
    story.append(Spacer(1, 0.05 * inch))
    story.append(NavyHeaderBar("PART 10", "Sign-Off"))
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph(
        "I have read this entire document and I understand:", STYLES["h2"]))
    story.append(Spacer(1, 0.1 * inch))

    items = [
        "The Owner's Top Ten — Operational Standards",
        "The Owner's Top Ten — Guest-Facing Standards",
        "How tasks work (claim-based system)",
        "The authorization model",
        "The diet verification protocol",
        "The Zero Waste Food Loop",
        "The cleaning standards",
        "The education system (LIFE)",
        "The exhibit integrity rules",
        "The technology governance rules",
        "The purchasing authority rules",
        "The workspace standards",
        "The Do Not List",
        "The escalation process: correction, warning, disciplinary action",
    ]
    for item in items:
        story.append(Paragraph(f"\u2713 {item}", STYLES["bullet"]))

    story.append(Spacer(1, 0.12 * inch))
    story.append(Paragraph(
        "I had the opportunity to ask questions. I understand that if I am unsure "
        "about something, I will stop and ask before acting.",
        STYLES["body"]))
    story.append(Spacer(1, 0.35 * inch))

    # Signature table
    sig_data = [
        [
            Paragraph("<b>Employee Name (print):</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
        [
            Paragraph("<b>Employee Signature:</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
        [
            Paragraph("<b>Date:</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
        [Paragraph("", STYLES["body"]), Paragraph("", STYLES["body"])],
        [
            Paragraph("<b>Conducted By (print):</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
        [
            Paragraph("<b>Conductor Signature:</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
        [
            Paragraph("<b>Date:</b>", STYLES["signoff_label"]),
            Paragraph("_" * 45, STYLES["signoff_label"]),
        ],
    ]
    sig_tbl = Table(sig_data, colWidths=[2 * inch, CONTENT_W - 2 * inch])
    sig_tbl.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("LINEBELOW", (1, 0), (1, 0), 0.8, HexColor("#C0C4E8")),
        ("LINEBELOW", (1, 1), (1, 1), 0.8, HexColor("#C0C4E8")),
        ("LINEBELOW", (1, 2), (1, 2), 0.8, HexColor("#C0C4E8")),
        ("LINEBELOW", (1, 4), (1, 4), 0.8, HexColor("#C0C4E8")),
        ("LINEBELOW", (1, 5), (1, 5), 0.8, HexColor("#C0C4E8")),
        ("LINEBELOW", (1, 6), (1, 6), 0.8, HexColor("#C0C4E8")),
    ]))
    story.append(sig_tbl)

    story.append(Spacer(1, 0.4 * inch))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.5,
                            color=TEAL, spaceAfter=8))
    story.append(Paragraph(
        "<i>This document is retained by management. "
        "A copy may be provided to the employee upon request.</i>",
        STYLES["muted"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "<b>LIFE + Studio Giraffe Integrated Operational System</b>",
        STYLES["body_bold"]))
    story.append(Paragraph(
        "Owner: Family Fun Group | Author: Ammon Covino | San Antonio Aquarium | "
        "Houston Interactive Aquarium &amp; Animal Preserve | Austin Aquarium | Effective: April 2026",
        STYLES["muted"]))


# ── Main ──────────────────────────────────────────────────────────────────────

def prepare_markdown():
    """Read and prepare the markdown source."""
    with open("/home/user/workspace/LIFE_SYSTEM_MASTER.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    # Sanitize Unicode — replace emojis with text-safe equivalents
    md_text = sanitize_unicode(md_text)

    # Remove PART 10 (SIGN-OFF) from markdown parse — we build it manually
    part10_match = re.search(r'\n# PART 10 — SIGN-OFF', md_text)
    if part10_match:
        part11_match = re.search(r'\n# PART 11', md_text[part10_match.start()+1:])
        if part11_match:
            md_core = md_text[:part10_match.start()] + md_text[part10_match.start() + 1 + part11_match.start():]
        else:
            md_core = md_text[:part10_match.start()]
    else:
        md_core = md_text

    # Strip the END OF DOCUMENT footer
    end_match = re.search(r'\n\*\*END OF DOCUMENT\*\*', md_core)
    if end_match:
        md_core = md_core[:end_match.start()]

    return md_core


def main():
    print("Reading source file...")
    md_core = prepare_markdown()

    # ── PASS 1: Build to collect page numbers ──
    print("Pass 1: Collecting page numbers...")
    PAGE_MAP.clear()
    story1 = build_story(md_core)
    add_signoff_page(story1)

    import io
    buf = io.BytesIO()
    doc1 = SimpleDocTemplate(
        buf,
        pagesize=letter,
        title="LIFE System Master",
        author="Perplexity Computer",
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 10,
        bottomMargin=MARGIN + 6,
    )
    doc1.build(story1, onFirstPage=cover_page, onLaterPages=later_pages)
    print(f"  Collected page numbers for {len(PAGE_MAP)} parts")
    for k, v in sorted(PAGE_MAP.items(), key=lambda x: x[1]):
        print(f"    {k}: page {v}")

    # ── PASS 2: Rebuild with page numbers in TOC ──
    print("Pass 2: Building final PDF with page numbers...")
    story2 = build_story(md_core)
    add_signoff_page(story2)

    print(f"Building PDF → {OUT_PATH}")
    doc2 = SimpleDocTemplate(
        OUT_PATH,
        pagesize=letter,
        title="LIFE System Master",
        author="Perplexity Computer",
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 10,
        bottomMargin=MARGIN + 6,
    )
    doc2.build(story2, onFirstPage=cover_page, onLaterPages=later_pages)
    print(f"PDF saved: {OUT_PATH}")

    # Quick stats
    import subprocess
    result = subprocess.run(["qpdf", "--show-npages", OUT_PATH],
                            capture_output=True, text=True)
    print(f"Page count: {result.stdout.strip()}")


if __name__ == "__main__":
    main()
