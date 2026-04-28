#!/usr/bin/env python3
"""
Build all 11 staff deployment PDFs for the LIFE System.
NO cover pages — content starts on page 1 with a navy header bar
matching the LIFE System Master PDF style.
"""

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Output Directories ──────────────────────────────────────────────────────
QR_DIR = Path("/home/user/workspace/staff_deploy/quick_ref")
SM_DIR = Path("/home/user/workspace/staff_deploy/complete")
QR_DIR.mkdir(parents=True, exist_ok=True)
SM_DIR.mkdir(parents=True, exist_ok=True)

# ── Font Registration ────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Inter", "/tmp/fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", "/tmp/fonts/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", "/tmp/fonts/Inter-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("DMSans", "/tmp/fonts/DMSans-Static-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DMSans-Bold", "/tmp/fonts/DMSans-Static-SemiBold.ttf"))

registerFontFamily("Inter", normal="Inter", bold="Inter-Bold",
                   italic="Inter", boldItalic="Inter-Bold")
registerFontFamily("DMSans", normal="DMSans", bold="DMSans-Bold",
                   italic="DMSans", boldItalic="DMSans-Bold")

# ── Brand Colors ─────────────────────────────────────────────────────────────
NAVY = HexColor("#2C3481")
TEAL = HexColor("#00AAAD")
DARK = HexColor("#1A1A1A")
MUTED = HexColor("#666666")
RED = HexColor("#C0392B")
LIGHT_BG = HexColor("#F5F6FA")
WHITE = white

W, H = letter
CW = W - 1.2 * inch  # content width within margins


# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM FLOWABLES
# ══════════════════════════════════════════════════════════════════════════════

class PageOneHeaderBar(Flowable):
    """
    Navy header bar for page 1 — matches LIFE System Master style:
    80pt tall, teal accent stripe on left, part label small at top,
    title large and white below.
    """
    def __init__(self, title, part_label="LIFE System Master", width=CW):
        super().__init__()
        self.title = title
        self.part_label = part_label
        self.width = width
        self.height = 80

    def wrap(self, avW, avH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # Navy background
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        # Teal accent stripe on left
        c.setFillColor(TEAL)
        c.rect(0, 0, 5, self.height, fill=1, stroke=0)
        # Part label (small, top-left)
        c.setFillColor(HexColor("#9AA0D4"))
        c.setFont("DMSans", 10)
        c.drawString(16, self.height - 22, self.part_label)
        # Title — auto-size to fit
        max_w = self.width - 32
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


class SectionHeaderBar(Flowable):
    """Smaller navy header bar for section breaks within content."""
    def __init__(self, text, width=CW, height=36):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height

    def wrap(self, avW, avH):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(NAVY)
        c.rect(0, 0, self.width, self.height, fill=1, stroke=0)
        c.setFillColor(TEAL)
        c.rect(0, 0, self.width, 3, fill=1, stroke=0)
        if self.text:
            c.setFillColor(WHITE)
            c.setFont("DMSans-Bold", 14)
            c.drawString(12, 10, self.text)
        c.restoreState()


class TealDivider(Flowable):
    """Thin teal divider line."""
    def __init__(self, width=CW):
        super().__init__()
        self.width = width
        self.height = 6

    def wrap(self, avW, avH):
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(TEAL)
        self.canv.setLineWidth(1.5)
        self.canv.line(0, 3, self.width, 3)


# ══════════════════════════════════════════════════════════════════════════════
# STYLES
# ══════════════════════════════════════════════════════════════════════════════

def make_qr_styles():
    """Quick Reference Cards — 12pt body."""
    s = {}
    s['body'] = ParagraphStyle('QRBody', fontName='Inter', fontSize=12, leading=16, textColor=DARK, spaceAfter=4)
    s['body_bold'] = ParagraphStyle('QRBodyBold', fontName='Inter-Bold', fontSize=12, leading=16, textColor=DARK, spaceAfter=4)
    s['h1'] = ParagraphStyle('QRH1', fontName='DMSans-Bold', fontSize=18, leading=22, textColor=NAVY, spaceAfter=8, spaceBefore=14)
    s['h2'] = ParagraphStyle('QRH2', fontName='DMSans-Bold', fontSize=14, leading=18, textColor=NAVY, spaceAfter=6, spaceBefore=10)
    s['h3'] = ParagraphStyle('QRH3', fontName='DMSans-Bold', fontSize=13, leading=16, textColor=DARK, spaceAfter=4, spaceBefore=8)
    s['bullet'] = ParagraphStyle('QRBullet', fontName='Inter', fontSize=12, leading=16, textColor=DARK, leftIndent=18, bulletIndent=4, spaceAfter=3)
    s['bullet_bold'] = ParagraphStyle('QRBulletBold', fontName='Inter-Bold', fontSize=12, leading=16, textColor=DARK, leftIndent=18, bulletIndent=4, spaceAfter=3)
    s['red_bullet'] = ParagraphStyle('QRRedBullet', fontName='Inter-Bold', fontSize=13, leading=17, textColor=RED, leftIndent=18, bulletIndent=4, spaceAfter=4)
    s['emphasis'] = ParagraphStyle('QREmphasis', fontName='Inter-SemiBold', fontSize=12, leading=16, textColor=NAVY, spaceAfter=6)
    s['small'] = ParagraphStyle('QRSmall', fontName='Inter', fontSize=10, leading=13, textColor=MUTED, spaceAfter=2)
    s['large_bold'] = ParagraphStyle('QRLargeBold', fontName='Inter-Bold', fontSize=14, leading=18, textColor=DARK, spaceAfter=4)
    s['stop'] = ParagraphStyle('QRStop', fontName='DMSans-Bold', fontSize=18, leading=24, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)
    return s


def make_sm_styles():
    """Complete Manuals — 11pt body."""
    s = {}
    s['body'] = ParagraphStyle('SMBody', fontName='Inter', fontSize=11, leading=15, textColor=DARK, spaceAfter=6)
    s['body_bold'] = ParagraphStyle('SMBodyBold', fontName='Inter-Bold', fontSize=11, leading=15, textColor=DARK, spaceAfter=6)
    s['h1'] = ParagraphStyle('SMH1', fontName='DMSans-Bold', fontSize=20, leading=26, textColor=NAVY, spaceAfter=10, spaceBefore=18)
    s['h2'] = ParagraphStyle('SMH2', fontName='DMSans-Bold', fontSize=15, leading=20, textColor=NAVY, spaceAfter=8, spaceBefore=14)
    s['h3'] = ParagraphStyle('SMH3', fontName='DMSans-Bold', fontSize=13, leading=17, textColor=DARK, spaceAfter=4, spaceBefore=10)
    s['h4'] = ParagraphStyle('SMH4', fontName='Inter-SemiBold', fontSize=11, leading=15, textColor=NAVY, spaceAfter=4, spaceBefore=8)
    s['bullet'] = ParagraphStyle('SMBullet', fontName='Inter', fontSize=11, leading=15, textColor=DARK, leftIndent=18, bulletIndent=4, spaceAfter=3)
    s['bullet_bold'] = ParagraphStyle('SMBulletBold', fontName='Inter-Bold', fontSize=11, leading=15, textColor=DARK, leftIndent=18, bulletIndent=4, spaceAfter=3)
    s['red_bullet'] = ParagraphStyle('SMRedBullet', fontName='Inter-Bold', fontSize=11, leading=15, textColor=RED, leftIndent=18, bulletIndent=4, spaceAfter=3)
    s['red_text'] = ParagraphStyle('SMRedText', fontName='Inter-Bold', fontSize=11, leading=15, textColor=RED, spaceAfter=6)
    s['emphasis'] = ParagraphStyle('SMEmphasis', fontName='Inter-SemiBold', fontSize=11, leading=15, textColor=NAVY, spaceAfter=6)
    s['small'] = ParagraphStyle('SMSmall', fontName='Inter', fontSize=9, leading=12, textColor=MUTED, spaceAfter=2)
    s['quote'] = ParagraphStyle('SMQuote', fontName='Inter-SemiBold', fontSize=12, leading=16, textColor=NAVY, leftIndent=24, rightIndent=24, spaceAfter=8, spaceBefore=8)
    s['indent'] = ParagraphStyle('SMIndent', fontName='Inter', fontSize=11, leading=15, textColor=DARK, leftIndent=18, spaceAfter=3)
    s['toc'] = ParagraphStyle('SMTOC', fontName='Inter', fontSize=11, leading=18, textColor=DARK, spaceAfter=2, leftIndent=12)
    return s


# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def make_footer_func(doc_name):
    """Return a footer callback that draws footer on every page."""
    def _footer(canvas_obj, doc):
        canvas_obj.saveState()
        canvas_obj.setFont("Inter", 8)
        canvas_obj.setFillColor(MUTED)
        canvas_obj.drawString(54, 28, f"LIFE System Master \u2014 {doc_name}")
        canvas_obj.drawRightString(W - 54, 28, f"Page {doc.page}")
        canvas_obj.setStrokeColor(TEAL)
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(54, 42, W - 54, 42)
        canvas_obj.restoreState()
    return _footer


def build_pdf(out_dir, filename, title, doc_name, story):
    """Build a PDF with footer on ALL pages (including page 1). No cover page."""
    path = str(out_dir / filename)
    doc = SimpleDocTemplate(
        path, pagesize=letter,
        title=title, author="Perplexity Computer",
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.6 * inch, bottomMargin=0.7 * inch,
    )
    footer_fn = make_footer_func(doc_name)
    # Same footer on first and later pages — no separate cover treatment
    doc.build(story, onFirstPage=footer_fn, onLaterPages=footer_fn)
    print(f"  Built: {path}")
    return path


# ══════════════════════════════════════════════════════════════════════════════
# QR_01: Top Twenty Rules
# ══════════════════════════════════════════════════════════════════════════════

def build_qr01():
    print("Building QR_01_Top_Twenty_Rules.pdf ...")
    s = make_qr_styles()
    story = []

    # Page 1 header bar
    story.append(PageOneHeaderBar("Top Twenty Rules"))
    story.append(Spacer(1, 12))

    # --- Operational Top 10 ---
    story.append(SectionHeaderBar("OPERATIONAL STANDARDS"))
    story.append(Spacer(1, 10))

    story.append(Paragraph('These are the ten rules that govern everything. They are posted on every wall. They are non-negotiable. If you violate these rules, you will be corrected, warned, or disciplined. There are no exceptions.', s['body']))
    story.append(Spacer(1, 6))

    op_rules = [
        ("Rule 1", "If it is not assigned, written, or approved \u2014 do not do it.", "No action without authorization. No exceptions."),
        ("Rule 2", "Animal welfare overrides everything.", "Biology first. Convenience never."),
        ("Rule 3", "Follow the written diet exactly.", "No substitutions. No guessing. No skipping steps."),
        ("Rule 4", "Nothing gets thrown away. All food follows the Zero Waste loop.", "Uneaten food goes to collection. Not the trash."),
        ("Rule 5", "If you are not sure \u2014 STOP. ASK. WAIT.", "Uncertainty is not a reason to act. It is a reason to pause."),
        ("Rule 6", "No record = did not happen.", "Documentation is proof. Everything is verified."),
        ("Rule 7", "Do not move, modify, or add anything to any exhibit.", "Nothing changes without written approval."),
        ("Rule 8", "Do not introduce, adopt, or use any software or system without owner approval.", "If it was not approved, it does not exist."),
        ("Rule 9", "Only authorized individuals approve purchases, sign contracts, or modify operations.", "If you did not get written approval to spend money or change a system, stop."),
        ("Rule 10", "Workspaces are for work. Not storage. Not socializing. Not sitting.", "If you are clocked in, you are working."),
    ]

    for num, title, desc in op_rules:
        story.append(Paragraph(f'<b>{num}:</b> {title}', s['body_bold']))
        story.append(Paragraph(desc, s['small']))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph('<b>Violation of these rules will result in corrective action. These are non-negotiable.</b>', s['emphasis']))

    story.append(PageBreak())

    # --- Guest-Facing Top 10 ---
    story.append(SectionHeaderBar("GUEST-FACING STANDARDS"))
    story.append(Spacer(1, 10))

    story.append(Paragraph('These rules govern how guests experience this facility. Guests judge us in the first 30 seconds. Every second after that confirms or corrects their first impression.', s['body']))
    story.append(Spacer(1, 6))

    guest_rules = [
        ("Rule 1", "You are on stage. Smile. Greet every guest.", "Guests see you before they see the animals. Your energy sets their experience."),
        ("Rule 2", "The facility must be visibly clean at all times.", "If it looks dirty, it is dirty. Fix it now."),
        ("Rule 3", "The facility must smell clean.", "No odor from waste, food prep, or neglect should reach guest areas. Ever."),
        ("Rule 4", "Animals must appear healthy, active, and in a quality environment.", "If an exhibit looks neglected, they see it. Standards are not negotiable."),
        ("Rule 5", "Guest interaction is personal. Make eye contact. Be present.", "You are the reason someone remembers this place."),
        ("Rule 6", "If a guest asks a question you cannot answer, say so honestly.", '"That is a great question. Let me find someone who can help, or scan the QR code for more."'),
        ("Rule 7", "Education is always on. Signs, screens, and QR codes must be correct.", "If a screen is wrong or a sign is missing, report it immediately."),
        ("Rule 8", "Encounters are joyful. Most are free. Feeding costs money; joy does not.", "Do not make guests feel like every experience costs money."),
        ("Rule 9", "No personal items, clutter, food, or drinks visible in guest areas.", "Your phone, your water bottle, your bag \u2014 not on the floor, not on a ledge, not in sight."),
        ("Rule 10", "Orderly and organized. Every area a guest can see must look intentional.", "No exposed cords, no random supplies, no half-finished setups."),
    ]

    for num, title, desc in guest_rules:
        story.append(Paragraph(f'<b>{num}:</b> {title}', s['body_bold']))
        story.append(Paragraph(desc, s['small']))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph('<b>Guests judge us in the first 30 seconds. Every second after confirms or corrects.</b>', s['emphasis']))

    build_pdf(QR_DIR, "QR_01_Top_Twenty_Rules.pdf", "Top Twenty Rules", "Top Twenty Rules", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_02: Feeding Protocol
# ══════════════════════════════════════════════════════════════════════════════

def build_qr02():
    print("Building QR_02_Feeding_Protocol.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("Feeding Protocol"))
    story.append(Spacer(1, 12))

    # 3-Step Protocol
    story.append(SectionHeaderBar("3-STEP FEEDING PROTOCOL"))
    story.append(Spacer(1, 10))

    story.append(Paragraph('<b>Step 1 \u2014 PREPARE</b>', s['h2']))
    story.append(Paragraph('Use the written diet sheet. The diet sheet tells you exactly what to prepare, how much, and how. No substitutions. If you run out of an item, you do not replace it with something else. You report it.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('<b>Step 2 \u2014 VERIFY</b>', s['h2']))
    story.append(Paragraph('Before you move forward, confirm the items and quantities against the diet sheet. Check that nothing is missing. Check that the amounts are correct.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('<b>Step 3 \u2014 DELIVER</b>', s['h2']))
    story.append(Paragraph('Place the food according to the protocol for that species. Follow the delivery instructions on the diet sheet.', s['body']))
    story.append(Spacer(1, 10))

    story.append(TealDivider())
    story.append(Spacer(1, 10))

    # Key Rules
    story.append(SectionHeaderBar("KEY FEEDING RULES"))
    story.append(Spacer(1, 8))

    rules = [
        "No guessing.",
        'No "close enough."',
        "If something is wrong: Stop \u2192 Correct \u2192 Redo.",
        "No animal fed to fullness before guest hours.",
        "No substitutions without approval.",
        "Incorrect feeding is corrected immediately.",
        "Unsure \u2192 Pause \u2192 Ask \u2192 Escalate.",
        "All feeding quantities use whole items \u2014 a papaya, a mango, a count of bananas. No grams. No weight measurements. Cut items in half at most.",
        "Diets are written by the owner or owner-designated authority ONLY. No staff member can create or modify diet sheets.",
        "If a diet sheet does not have the owner's signature, it does not exist.",
        "Leftovers go in Ziploc, marked with source exhibit, in the fridge. Morning: serve leftovers FIRST. As they decline, feed to birds. Do NOT throw food away.",
    ]

    for r in rules:
        story.append(Paragraph(f'\u2022 {r}', s['bullet']))

    story.append(PageBreak())

    # Exhibit Feeding Summary
    story.append(SectionHeaderBar("EXHIBIT FEEDING SUMMARY"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>GIRAFFE</b> \u2014 Hybrid (Guest-Led During Guest Hours)', s['h3']))
    story.append(Paragraph('\u2022 Before guest hours: baseline nutrition only', s['bullet']))
    story.append(Paragraph('\u2022 During guest hours: guest feeding is primary enrichment', s['bullet']))
    story.append(Paragraph('\u2022 Do NOT feed giraffes to fullness before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 Approved foods: acacia / approved browse (guest), limited granules (baseline)', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>LARGE PARROTS / MACAWS</b> \u2014 Hybrid (Motivation Required)', s['h3']))
    story.append(Paragraph('\u2022 No full bowls before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 Portions sized to maintain engagement', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>SMALL BIRDS / LORIKEETS</b> \u2014 Guest-Motivated During Guest Hours', s['h3']))
    story.append(Paragraph('\u2022 Minimal baseline before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 No substitutions. No early full bowls.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>TORTOISES</b> \u2014 HAY ONLY', s['h3']))
    story.append(Paragraph('\u2022 Before guest hours: baseline hay only', s['bullet']))
    story.append(Paragraph('\u2022 During guest hours: guest feeding encouraged (hay only)', s['bullet']))
    story.append(Paragraph('\u2022 Approved foods: HAY ONLY \u2014 no greens, no vegetables, no fruit', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>STINGRAYS / AQUATIC TOUCH POOLS</b>', s['h3']))
    story.append(Paragraph('\u2022 ZERO staff feeding of stingrays, fish, or sharks.', s['red_bullet']))
    story.append(Paragraph('\u2022 Stingray feeding is guest-interaction only during guest hours, using approved food at the station.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>SMALL MAMMALS</b> \u2014 Hybrid (Motivation Required)', s['h3']))
    story.append(Paragraph('\u2022 Baseline only before guest hours. Fresh food only. No early full bowls.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>CHAMELEON &amp; SENSITIVE REPTILES</b> \u2014 Staff-Prepared, Guest-Observed', s['h3']))
    story.append(Paragraph('\u2022 Diet per diet sheet only. Active drip hydration at all times.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>SNAKES</b> \u2014 Staff-Prepared / Staff-Controlled', s['h3']))
    story.append(Paragraph('\u2022 Feed outside peak guest interaction windows. Species-specific diet per diet sheet.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>FISH / AQUATIC EXHIBITS (NON-TOUCH)</b>', s['h3']))
    story.append(Paragraph('\u2022 ZERO staff feeding of fish, sharks, or aquatic exhibits.', s['red_bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>HAY-EATING ANIMALS</b> \u2014 Kangaroos, goats, horses, tortoises, capybaras', s['h3']))
    story.append(Paragraph('\u2022 Make sure they are NOT getting fed other things by guests.', s['bullet']))
    story.append(Paragraph('\u2022 Hay goes OUTSIDE exhibit, given to guests a little at a time through guest contact.', s['bullet']))

    build_pdf(QR_DIR, "QR_02_Feeding_Protocol.pdf", "Feeding Protocol Quick Reference", "Feeding Protocol", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_03: Do Not List
# ══════════════════════════════════════════════════════════════════════════════

def build_qr03():
    print("Building QR_03_Do_Not_List.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("The Do Not List"))
    story.append(Spacer(1, 12))

    story.append(Paragraph('These are the things you must never do. This is not a suggestion list. These are absolute prohibitions.', s['body']))
    story.append(Spacer(1, 8))

    do_nots = [
        "Do not act without authorization.",
        "Do not substitute diet items.",
        "Do not throw away food.",
        "Do not improvise or guess.",
        "Do not move, modify, or add to exhibits.",
        "Do not relocate animals.",
        "Do not use unapproved software or systems.",
        "Do not edit checklists or procedures.",
        "Do not make up facts about animals.",
        "Do not sit in offices doing nothing.",
        "Do not create your own signs, materials, or educational content.",
        "Do not bring in outside vendors without owner approval.",
        "Do not sign contracts or agreements on behalf of the facility.",
        "Do not order product without owner approval.",
        "Do not change any system, no matter how small, without approval.",
        "Do not move any animal without upper manager approval.",
        "Do not take any animal to the vet without upper manager approval.",
        "Do not hold meetings longer than 15 minutes without authorization.",
        "Do not rake exhibits to bare dirt \u2014 maintain natural biome.",
        "Do not use grams or weight measurements for feeding \u2014 use whole items only.",
        "Do not remove hay from the ground \u2014 horses and hay-eating animals eat it there.",
    ]

    for item in do_nots:
        story.append(Paragraph(f'\u2022 {item}', s['red_bullet']))

    story.append(Spacer(1, 14))
    story.append(Paragraph('When in doubt: STOP \u2192 ASK \u2192 WAIT.', s['stop']))

    build_pdf(QR_DIR, "QR_03_Do_Not_List.pdf", "The Do Not List", "Do Not List", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_04: Zero Waste
# ══════════════════════════════════════════════════════════════════════════════

def build_qr04():
    print("Building QR_04_Zero_Waste.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("Zero Waste Food Loop"))
    story.append(Spacer(1, 12))

    story.append(SectionHeaderBar("THE 7 STAGES"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Main Loop:</b> Food waste \u2192 Compost \u2192 Insect biomass \u2192 Chickens \u2192 Eggs \u2192 Animal feed', s['body_bold']))
    story.append(Paragraph('<b>Parallel Loop:</b> Barley \u2192 Sprouting \u2192 Chicken feed \u2192 Egg production support', s['body_bold']))
    story.append(Paragraph('<b>Exclusion:</b> The outside aviary is excluded from the collection process.', s['body']))
    story.append(Spacer(1, 8))

    stages = [
        ("Stage 1 \u2014 Collection", "Capture ALL uneaten food from designated exhibits into ONE central bin. Every exhibit has a collection protocol. Follow it."),
        ("Stage 2 \u2014 Sorting", "Separate collected material into three categories:"),
        ("Stage 3 \u2014 Compost", "Break down organic material. Requires moisture balance, airflow, and warmth. Follow the composting protocol."),
        ("Stage 4 \u2014 Insect Conversion", "Black soldier fly larvae convert compost into protein biomass. This is a managed biological process."),
        ("Stage 5 \u2014 Chicken Feeding", "Insects from Stage 4 plus barley sprouts feed the chickens."),
        ("Stage 6 \u2014 Egg Production", "Chickens produce eggs \u2014 a high-density nutrient package."),
        ("Stage 7 \u2014 Animal Feed", "Eggs are returned to the broader animal feeding system."),
    ]

    for title, desc in stages:
        story.append(Paragraph(f'<b>{title}</b>', s['h3']))
        story.append(Paragraph(desc, s['body']))
        if "Stage 2" in title:
            story.append(Paragraph('\u2022 A) Primary Compost: Fruits, vegetables, grains, plant material', s['bullet']))
            story.append(Paragraph('\u2022 B) Controlled: Meat, eggs, protein', s['bullet']))
            story.append(Paragraph('\u2022 C) Reject / Escalate: Plastic, trash, anything unknown \u2014 ASK if unsure', s['bullet']))
        story.append(Spacer(1, 4))

    story.append(TealDivider())
    story.append(Spacer(1, 8))

    # What Goes Where
    story.append(SectionHeaderBar("WHAT GOES WHERE"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('\u2022 <b>Compost bin:</b> Fruits, vegetables, grains, plant material', s['bullet']))
    story.append(Paragraph('\u2022 <b>Controlled bin:</b> Meat, eggs, protein', s['bullet']))
    story.append(Paragraph('\u2022 <b>Reject:</b> Plastic, trash, anything unknown \u2014 ASK if unsure', s['bullet']))
    story.append(Spacer(1, 8))

    story.append(Paragraph('\u2022 <b>DO NOT throw food in the trash.</b> If you are about to throw something away \u2014 STOP. You are breaking the system.', s['red_bullet']))

    story.append(Spacer(1, 10))
    story.append(TealDivider())
    story.append(Spacer(1, 8))

    # Enforcement Rules
    story.append(SectionHeaderBar("ENFORCEMENT RULES"))
    story.append(Spacer(1, 8))

    enforcement = [
        "Every action must have a named owner.",
        'Verbal claim required before execution: "I will take this assignment."',
        "Documentation is proof of execution \u2014 no record = incomplete.",
        "No silent decisions \u2014 uncertainty triggers STOP \u2192 ASK \u2192 WAIT.",
        "Throwing away material is a system VIOLATION.",
    ]
    for e in enforcement:
        story.append(Paragraph(f'\u2022 {e}', s['bullet']))

    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Core Laws:</b>', s['h3']))
    laws = [
        "INPUT QUALITY = OUTPUT QUALITY",
        "VISIBILITY CONTROLS PERFORMANCE (invisible systems fail)",
        "SIMPLICITY DRIVES ADOPTION",
        "WHAT YOU ALLOW BECOMES THE SYSTEM",
        "SYSTEM MUST SURVIVE WITHOUT YOU",
    ]
    for law in laws:
        story.append(Paragraph(f'\u2022 {law}', s['bullet_bold']))

    build_pdf(QR_DIR, "QR_04_Zero_Waste.pdf", "Zero Waste Food Loop Quick Reference", "Zero Waste", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_05: Cleaning
# ══════════════════════════════════════════════════════════════════════════════

def build_qr05():
    print("Building QR_05_Cleaning.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("Cleaning Standards"))
    story.append(Spacer(1, 12))

    story.append(SectionHeaderBar("CLEANING STANDARDS"))
    story.append(Spacer(1, 10))

    story.append(Paragraph('<b>Acrylic Windows</b>', s['h2']))
    story.append(Paragraph('Blue rags + distilled water ONLY. Nothing else. No Windex. No paper towels. No cleaning sprays. Blue rags and distilled water. That is it.', s['body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Exhibits</b>', s['h2']))
    story.append(Paragraph('Virkon for disinfection. Follow the label instructions exactly. If you do not know the correct dilution ratio, ask before mixing.', s['body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Food Prep Areas</b>', s['h2']))
    story.append(Paragraph('Clean, sanitize, document completion. Every food prep surface must be cleaned and sanitized after each use.', s['body']))
    story.append(Spacer(1, 12))

    story.append(TealDivider())
    story.append(Spacer(1, 10))

    # From Part 2 - guest-facing cleaning rules
    story.append(SectionHeaderBar("GUEST-AREA CLEANING"))
    story.append(Spacer(1, 10))

    story.append(Paragraph('<b>The facility must be visibly clean at all times.</b>', s['h2']))
    story.append(Paragraph('Floors, glass, exhibits, restrooms, walkways. If it looks dirty, it is dirty. Fix it now.', s['body']))
    story.append(Paragraph('Do not walk past trash. Do not walk past a smudged window. Do not walk past a dirty floor and tell yourself someone else will handle it. If you see it, you own it. Pick it up, wipe it down, report it. Guests notice everything.', s['body']))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>The facility must smell clean.</b>', s['h2']))
    story.append(Paragraph('No odor from waste, food prep, or neglect should reach guest areas. Ever.', s['body']))
    story.append(Paragraph('Guests may forgive a small visual issue. They will not forgive a bad smell. If you can smell waste, food residue, or neglect in any guest-accessible area, it is an emergency. Fix it immediately or report it.', s['body']))

    build_pdf(QR_DIR, "QR_05_Cleaning.pdf", "Cleaning Standards Quick Reference", "Cleaning", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_06: Guest Interaction
# ══════════════════════════════════════════════════════════════════════════════

def build_qr06():
    print("Building QR_06_Guest_Interaction.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("Guest Interaction Standards"))
    story.append(Spacer(1, 12))

    story.append(Paragraph('These rules govern how guests experience this facility. Guests judge us in the first 30 seconds. Every second after that confirms or corrects their first impression.', s['body']))
    story.append(Spacer(1, 8))

    rules = [
        ("Rule 1: You are on stage. Smile. Greet every guest.",
         "From the moment you clock in, you are performing. Not performing a fake character \u2014 being genuinely present and welcoming. Make eye contact. Say hello. If a family walks by and you ignore them, you just told them they do not matter. That is not how we operate."),
        ("Rule 2: The facility must be visibly clean at all times.",
         "Do not walk past trash. Do not walk past a smudged window. Do not walk past a dirty floor and tell yourself someone else will handle it. If you see it, you own it. Pick it up, wipe it down, report it. Guests notice everything."),
        ("Rule 3: The facility must smell clean.",
         "Guests may forgive a small visual issue. They will not forgive a bad smell. If you can smell waste, food residue, or neglect in any guest-accessible area, it is an emergency. Fix it immediately or report it."),
        ("Rule 4: Animals must appear healthy, active, and in a quality environment.",
         "Guests look at exhibits the way you look at a restaurant kitchen. If it looks off, they lose trust. Animals must be active and engaged during guest hours. Exhibits must be clean, well-maintained, and properly lit. If an animal appears unwell, report it immediately \u2014 do not wait for the end of your shift."),
        ("Rule 5: Guest interaction is personal. Make eye contact. Be present.",
         "The difference between a forgettable visit and a memorable one is you. When a guest approaches you, give them your full attention. Put your phone away. Stop what you are doing. Be present. Be helpful. Be real."),
        ("Rule 6: If a guest asks a question you cannot answer, say so honestly.",
         '"That is a great question. Let me find someone who can help, or scan the QR code for more." Do not make up facts about animals. Do not guess at information. Do not pretend to know something you do not know. Honesty builds trust. Making things up destroys it.'),
        ("Rule 7: Education is always on. Signs, screens, and QR codes must be correct.",
         "This facility runs an education system called LIFE \u2014 Language, Intelligence, Form, Ecology. It is not a gimmick. Every sign, QR code, and exhibit teaches visitors something real. If you notice a screen displaying wrong information, a missing sign, or a broken QR code, report it immediately. Do not try to fix it yourself."),
        ("Rule 8: Encounters are joyful. Most are free. Feeding costs money; joy does not.",
         "Most animal encounters at this facility are free. That is by design. The joy of touching, seeing, and learning about animals is the core experience. Feeding is what costs money. Do not push paid experiences. Do not make guests feel like they need to pay to have a good time."),
        ("Rule 9: No personal items, clutter, food, or drinks visible in guest areas.",
         "Guest areas must look intentional and professional at all times. Your personal belongings are not part of the guest experience. Keep them in designated areas. If a guest can see your stuff, you are doing it wrong."),
        ("Rule 10: Orderly and organized. Every area a guest can see must look intentional.",
         "Guests should never see behind the curtain. No extension cords draped across walkways. No boxes of supplies stacked in corners. No partially assembled displays. If a guest-visible area looks messy, unfinished, or chaotic, fix it before they see it."),
    ]

    for title, desc in rules:
        story.append(Paragraph(f'<b>{title}</b>', s['body_bold']))
        story.append(Paragraph(desc, s['body']))
        story.append(Spacer(1, 6))

    build_pdf(QR_DIR, "QR_06_Guest_Interaction.pdf", "Guest Interaction Standards Quick Reference", "Guest Interaction", story)


# ══════════════════════════════════════════════════════════════════════════════
# QR_07: How We Work
# ══════════════════════════════════════════════════════════════════════════════

def build_qr07():
    print("Building QR_07_How_We_Work.pdf ...")
    s = make_qr_styles()
    story = []

    story.append(PageOneHeaderBar("How We Work Here"))
    story.append(Spacer(1, 12))

    # Three Questions
    story.append(SectionHeaderBar("THE THREE QUESTIONS"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Before you do anything, ask yourself:', s['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>1. Was it assigned?</b>', s['large_bold']))
    story.append(Paragraph('<b>2. Is it written?</b>', s['large_bold']))
    story.append(Paragraph('<b>3. Was it approved?</b>', s['large_bold']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('If the answer to all three is no \u2014 you do not do it. You stop and you ask.', s['emphasis']))
    story.append(Spacer(1, 10))

    # Claim-Based System
    story.append(SectionHeaderBar("THE CLAIM-BASED WORK SYSTEM"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>1.</b> A task is posted. It appears on the task board, in a message, or from a manager.', s['body']))
    story.append(Paragraph('<b>2.</b> You claim it. You say: "I will take this." That means it is now yours.', s['body']))
    story.append(Paragraph('<b>3.</b> You do it. You execute the task according to the written procedure.', s['body']))
    story.append(Paragraph('<b>4.</b> It gets verified. A manager confirms it was done correctly.', s['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('If you do not claim it, it is not yours. If nobody claims it, we have a problem \u2014 and that problem gets escalated immediately.', s['body']))
    story.append(Spacer(1, 10))

    # Authorization
    story.append(SectionHeaderBar("AUTHORIZATION"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('\u2022 <b>Owner:</b> Sets direction, standards, and policy. Final authority on system changes, exhibit design, diet formulas, and policy changes.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Upper Managers:</b> Approve all purchases (credit card holders limited to $350 max). Approve vendor contracts. Approve animal moves and vet visits. Identify issues BEFORE they become problems.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Staff:</b> Execute claimed tasks within existing procedures. Cannot approve anything. If something requires approval, escalate to a manager.', s['bullet']))
    story.append(Spacer(1, 10))

    # Escalation
    story.append(SectionHeaderBar("ESCALATION LADDER"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('\u2022 <b>Strike 1: Correction.</b> You made a mistake. You are told what you did wrong and how to fix it.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Strike 2: Formal warning + retraining.</b> Same mistake again or a serious error. Formal warning issued. Retraining completed.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Strike 3: Disciplinary action.</b> Behavior continues after correction and warning. May include suspension, reassignment, or termination.', s['bullet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('This applies to everyone. Staff, managers, everyone.', s['emphasis']))
    story.append(Spacer(1, 10))

    # Purchasing
    story.append(SectionHeaderBar("PURCHASING"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('\u2022 No purchases without upper manager approval.', s['bullet']))
    story.append(Paragraph('\u2022 Credit card holders have a $350 maximum per purchase.', s['bullet']))
    story.append(Paragraph('\u2022 Only the owner can approve new vendors.', s['bullet']))
    story.append(Paragraph('\u2022 All purchases require documentation (what, from whom, how much, why).', s['bullet']))
    story.append(Spacer(1, 10))

    # Meetings
    story.append(SectionHeaderBar("MEETINGS"))
    story.append(Spacer(1, 8))
    story.append(Paragraph('Team meetings: maximum 15 minutes, every morning before work. Manager meetings: maximum 15 minutes. No meetings over 15 minutes without authorization.', s['body']))

    build_pdf(QR_DIR, "QR_07_How_We_Work.pdf", "How We Work Here Quick Reference", "How We Work", story)


# ══════════════════════════════════════════════════════════════════════════════
# SM_01: Feeding Complete
# ══════════════════════════════════════════════════════════════════════════════

def build_sm01():
    print("Building SM_01_Feeding_Complete.pdf ...")
    s = make_sm_styles()
    story = []

    story.append(PageOneHeaderBar("Feeding Complete Manual"))
    story.append(Spacer(1, 12))

    # TOC on page 1 below header bar
    story.append(Paragraph('TABLE OF CONTENTS', s['h1']))
    toc_items = [
        "1. Animal Care and Diet",
        "2. Zero Waste Food Loop",
        "3. Exhibit-Specific Feeding Addendums",
        "4. Diet Enforcement \u2014 3-Strike Ladder",
        "5. Feeding Authority",
        "6. The Governing Principle",
        "7. Gold Standard Diet System",
        "8. Gold Standard Species Diet Posters",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s['toc']))
    story.append(PageBreak())

    # ============ PART 4: ANIMAL CARE AND DIET ============
    story.append(SectionHeaderBar("ANIMAL CARE AND DIET"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Animal care is not optional. It is the core obligation of this facility. Every animal depends on us to feed it correctly, house it correctly, and care for it correctly. There are no shortcuts.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Diet Verification Protocol', s['h2']))
    story.append(Paragraph('This is the step-by-step process for every feeding, every time.', s['body']))

    story.append(Paragraph('Step 1 \u2014 Prepare', s['h3']))
    story.append(Paragraph('Use the written diet sheet. The diet sheet tells you exactly what to prepare, how much, and how. No substitutions. If you run out of an item, you do not replace it with something else. You report it.', s['body']))

    story.append(Paragraph('Step 2 \u2014 Verify', s['h3']))
    story.append(Paragraph('Before you move forward, confirm the items and quantities against the diet sheet. Check that nothing is missing. Check that the amounts are correct.', s['body']))

    story.append(Paragraph('Step 3 \u2014 Deliver', s['h3']))
    story.append(Paragraph('Place the food according to the protocol for that species. Follow the delivery instructions on the diet sheet.', s['body']))

    story.append(Paragraph('Rules', s['h3']))
    for r in ["No guessing.", 'No "close enough."', "If something is wrong: Stop \u2192 Correct \u2192 Redo.", "No animal fed to fullness before guest hours."]:
        story.append(Paragraph(f'\u2022 {r}', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('<b>Position:</b> Top-down. No shadows. No filters.', s['body']))
    story.append(Paragraph('<b>Caption format:</b> Animal Name \u2013 Date \u2013 Your Initials', s['body']))
    story.append(Paragraph('<b>Errors not allowed:</b> Missing items. Blurry images. Late posting.', s['body']))
    story.append(Spacer(1, 6))

    # Manager Sign-Off
    story.append(Paragraph('Manager Sign-Off System', s['h2']))
    story.append(Paragraph('Managers must:', s['body']))
    story.append(Paragraph('\u2022 Review ALL diet compliance daily.', s['bullet']))
    story.append(Paragraph('\u2022 Confirm accuracy.', s['bullet']))
    story.append(Paragraph('\u2022 Respond "Verified \u2013 [Initials]."', s['bullet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('If a feeding is incorrect:', s['body']))
    story.append(Paragraph('\u2022 Require correction.', s['bullet']))
    story.append(Paragraph('\u2022 Document the issue.', s['bullet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>No silent approvals.</b> If a manager does not respond "Verified," the feeding is not verified. Silence is not acceptance.', s['body_bold']))

    # Diet Authority
    story.append(Paragraph('Diet Authority', s['h2']))
    story.append(Paragraph('<b>Diets are written by the owner or owner-designated authority ONLY.</b>', s['body_bold']))
    story.append(Paragraph('\u2022 No staff member can create or modify diet sheets.', s['bullet']))
    story.append(Paragraph('\u2022 No software can create or modify diet sheets.', s['bullet']))
    story.append(Paragraph('\u2022 No vendor can create or modify diet sheets.', s['bullet']))
    story.append(Paragraph('\u2022 Every diet sheet must be signed and dated by the authority.', s['bullet']))
    story.append(Paragraph('\u2022 Any diet sheet without an authority signature is void \u2014 do not use it.', s['bullet']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Rule:</b> If a diet sheet does not have the owner\'s signature, it does not exist.', s['body_bold']))
    story.append(Paragraph('Animals cannot be moved without upper manager approval. Animals cannot go to vet without upper manager approval.', s['body']))

    # Feeding Measurements
    story.append(Paragraph('Feeding Measurements', s['h2']))
    story.append(Paragraph('All feeding quantities use whole items \u2014 a papaya (the whole thing), a mango, a count of bananas. No grams. No weight measurements. Cut items in half at most.', s['body']))

    # Mulberry, Horses, etc.
    story.append(Paragraph('Mulberry Branches', s['h2']))
    story.append(Paragraph('Go in a plastic vase, zip-tied tight to exhibit. Water deep. Branches zip-tied so animals cannot pull them out. Stay wet, like a tree to hold on to. Old mulberry branches go to aviaries for birds to make nests and for foraging. Same with bamboo.', s['body']))

    story.append(Paragraph('Horses', s['h2']))
    story.append(Paragraph('Only fed hay. Guests can feed hay only on slow days. Put bale on ground. Remove hangers everywhere \u2014 hay falls, they consider it garbage and throw it away. Just leave hay on ground.', s['body']))

    story.append(Paragraph('Exhibit Ground Maintenance', s['h2']))
    story.append(Paragraph('Do not rake up poop everywhere. Leave exhibits as natural biome. Ground becomes what it is instead of scraped hard dirt. Let grass grow, water it.', s['body']))

    story.append(Paragraph('Hay-Eating Animals', s['h2']))
    story.append(Paragraph('Kangaroos, goats, horses, tortoises (almost entirely hay), capybaras. Make sure they are NOT getting fed other things by guests.', s['body']))

    story.append(Paragraph('Guest Feeding of Hay', s['h2']))
    story.append(Paragraph('Hay goes OUTSIDE exhibit, given to guests a little at a time through guest contact.', s['body']))

    story.append(Paragraph('Water Dishes', s['h2']))
    story.append(Paragraph('Just clean water. Building water is already filtered \u2014 any water used is filtered.', s['body']))

    story.append(PageBreak())

    # ============ PART 6: ZERO WASTE ============
    story.append(SectionHeaderBar("ZERO WASTE FOOD LOOP"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Main Loop:</b> Food waste \u2192 Compost \u2192 Insect biomass \u2192 Chickens \u2192 Eggs \u2192 Animal feed', s['body_bold']))
    story.append(Paragraph('<b>Parallel Loop:</b> Barley \u2192 Sprouting \u2192 Chicken feed \u2192 Egg production support', s['body_bold']))
    story.append(Paragraph('<b>Exclusion:</b> The outside aviary is excluded from the collection process.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The 7 Stages', s['h2']))

    zw_stages = [
        ("Stage 1 \u2014 Collection", "Capture ALL uneaten food from designated exhibits into ONE central bin. Every exhibit has a collection protocol. Follow it."),
        ("Stage 2 \u2014 Sorting", "Separate collected material into three categories:\n\u2022 A) Primary Compost: Fruits, vegetables, grains, plant material\n\u2022 B) Controlled: Meat, eggs, protein\n\u2022 C) Reject / Escalate: Plastic, trash, anything unknown \u2014 ASK if unsure"),
        ("Stage 3 \u2014 Compost", "Break down organic material. Requires moisture balance, airflow, and warmth. Follow the composting protocol."),
        ("Stage 4 \u2014 Insect Conversion", "Black soldier fly larvae convert compost into protein biomass. This is a managed biological process."),
        ("Stage 5 \u2014 Chicken Feeding", "Insects from Stage 4 plus barley sprouts feed the chickens."),
        ("Stage 6 \u2014 Egg Production", "Chickens produce eggs \u2014 a high-density nutrient package."),
        ("Stage 7 \u2014 Animal Feed", "Eggs are returned to the broader animal feeding system."),
    ]

    for title, desc in zw_stages:
        story.append(Paragraph(f'<b>{title}</b>', s['h3']))
        for line in desc.split('\n'):
            if line.startswith('\u2022'):
                story.append(Paragraph(line, s['bullet']))
            else:
                story.append(Paragraph(line, s['body']))
        story.append(Spacer(1, 4))

    story.append(Paragraph('Enforcement Rules', s['h2']))
    for e in [
        "Every action must have a named owner.",
        'Verbal claim required before execution: "I will take this assignment."',
        "Documentation is proof of execution \u2014 no record = incomplete.",
        "No silent decisions \u2014 uncertainty triggers STOP \u2192 ASK \u2192 WAIT.",
        "Throwing away material is a system VIOLATION.",
    ]:
        story.append(Paragraph(f'\u2022 {e}', s['bullet']))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Core Laws', s['h2']))
    for law in [
        "INPUT QUALITY = OUTPUT QUALITY",
        "VISIBILITY CONTROLS PERFORMANCE (invisible systems fail)",
        "SIMPLICITY DRIVES ADOPTION",
        "WHAT YOU ALLOW BECOMES THE SYSTEM",
        "SYSTEM MUST SURVIVE WITHOUT YOU",
    ]:
        story.append(Paragraph(f'\u2022 {law}', s['bullet_bold']))

    story.append(PageBreak())

    # ============ PART 7: EXHIBIT-SPECIFIC FEEDING ADDENDUMS ============
    story.append(SectionHeaderBar("EXHIBIT-SPECIFIC FEEDING ADDENDUMS"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('These addendums are mandatory and apply to all staff and managers. If this document conflicts with habit or memory, this document overrides.', s['body']))
    story.append(Spacer(1, 6))

    # Large Animals & Birds
    story.append(Paragraph('GIRAFFE \u2014 Feeding &amp; Guest Interaction', s['h2']))
    story.append(Paragraph('Feeding Model: Hybrid (Guest-Led During Guest Hours)', s['body']))
    story.append(Paragraph('\u2022 Before guest hours: baseline nutrition only', s['bullet']))
    story.append(Paragraph('\u2022 During guest hours: guest feeding is primary enrichment', s['bullet']))
    story.append(Paragraph('\u2022 After guest hours: staff may complete nutrition if required', s['bullet']))
    story.append(Paragraph('\u2022 Do NOT feed giraffes to fullness before guest hours.', s['bullet_bold']))
    story.append(Paragraph('\u2022 Approved foods: acacia / approved browse (guest), limited granules (baseline)', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('LARGE PARROTS / MACAWS', s['h2']))
    story.append(Paragraph('Feeding Model: Hybrid (Motivation Required During Guest Hours)', s['body']))
    story.append(Paragraph('\u2022 No full bowls before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 Portions sized to maintain engagement', s['bullet']))
    story.append(Paragraph('\u2022 No early feeding that keeps birds disengaged', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('SMALL BIRDS / LORIKEETS', s['h2']))
    story.append(Paragraph('Feeding Model: Guest-Motivated During Guest Hours', s['body']))
    story.append(Paragraph('\u2022 Minimal baseline before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 No substitutions', s['bullet']))
    story.append(Paragraph('\u2022 No early full bowls', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('CHAMELEON &amp; SENSITIVE REPTILES', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Prepared, Guest-Observed', s['body']))
    story.append(Paragraph('\u2022 Diet per diet sheet only', s['bullet']))
    story.append(Paragraph('\u2022 Active drip hydration at all times', s['bullet']))
    story.append(Paragraph('\u2022 Multiple offerings through the day', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Universal Rules:</b> No substitutions without approval. Incorrect feeding is corrected immediately. Unsure \u2192 Pause \u2192 Ask \u2192 Escalate.', s['emphasis']))

    story.append(TealDivider())
    story.append(Spacer(1, 8))

    # Tortoises, Touch Pools, etc.
    story.append(Paragraph('TORTOISES \u2014 Feeding &amp; Guest Interaction', s['h2']))
    story.append(Paragraph('Feeding Model: Hybrid (Guest Interaction Supported)', s['body']))
    story.append(Paragraph('\u2022 Before guest hours: baseline hay only', s['bullet']))
    story.append(Paragraph('\u2022 During guest hours: guest feeding encouraged when appropriate (hay only)', s['bullet']))
    story.append(Paragraph('\u2022 Do NOT feed tortoises to fullness before guest hours.', s['bullet_bold']))
    story.append(Paragraph('\u2022 Approved foods: HAY ONLY \u2014 no greens, no vegetables, no fruit', s['bullet_bold']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('STINGRAYS / AQUATIC TOUCH POOLS', s['h2']))
    story.append(Paragraph('\u2022 ZERO staff feeding of stingrays, fish, or sharks.', s['red_bullet']))
    story.append(Paragraph('\u2022 Stingray feeding is guest-interaction only during guest hours, using approved food provided at the station.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('SMALL MAMMALS (GUEST-CONTACT)', s['h2']))
    story.append(Paragraph('Feeding Model: Hybrid (Motivation Required)', s['body']))
    story.append(Paragraph('\u2022 Baseline only before guest hours', s['bullet']))
    story.append(Paragraph('\u2022 Fresh food only', s['bullet']))
    story.append(Paragraph('\u2022 No early full bowls', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('ADDITIONAL REPTILES (MIXED DIET / SENSITIVE)', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Prepared, Species-Specific', s['body']))
    story.append(Paragraph('\u2022 Diet per diet sheet only', s['bullet']))
    story.append(Paragraph('\u2022 Active hydration via drip or mist at all times', s['bullet']))
    story.append(Paragraph('\u2022 No generic bowls or unapproved produce.', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Universal Rules:</b> No substitutions without approval. Incorrect feeding corrected immediately. Unsure \u2192 Pause \u2192 Ask \u2192 Escalate.', s['emphasis']))

    story.append(TealDivider())
    story.append(Spacer(1, 8))

    # Snakes, Amphibians, etc.
    story.append(Paragraph('SNAKES (ALL SPECIES)', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Prepared / Staff-Controlled', s['body']))
    story.append(Paragraph('\u2022 Feed outside peak guest interaction windows', s['bullet']))
    story.append(Paragraph('\u2022 Species-specific diet and schedule only per diet sheet', s['bullet']))
    story.append(Paragraph('\u2022 No substitutions', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('AMPHIBIANS', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Prepared / Environmental', s['body']))
    story.append(Paragraph('\u2022 Multiple small feedings preferred', s['bullet']))
    story.append(Paragraph('\u2022 Diet per diet sheet only', s['bullet']))
    story.append(Paragraph('\u2022 Hydration systems active at all times', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('INVERTEBRATES', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Prepared / Species-Specific', s['body']))
    story.append(Paragraph('\u2022 Exact diet per SOP only', s['bullet']))
    story.append(Paragraph('\u2022 Remove uneaten food as required', s['bullet']))
    story.append(Paragraph('\u2022 No mixing diets', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('FISH / AQUATIC EXHIBITS (NON-TOUCH)', s['h2']))
    story.append(Paragraph('\u2022 ZERO staff feeding of fish, sharks, or aquatic exhibits.', s['red_bullet']))
    story.append(Paragraph('\u2022 Water quality checks maintained', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('NO-FEED / DISPLAY-ONLY EXHIBITS', s['h2']))
    story.append(Paragraph('Feeding Model: Staff-Only / Off-View', s['body']))
    story.append(Paragraph('\u2022 No guest feeding', s['bullet']))
    story.append(Paragraph('\u2022 Feeding occurs off-view when applicable', s['bullet']))
    story.append(Paragraph('\u2022 No exceptions', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Universal Rules:</b> No substitutions without approval. Incorrect feeding corrected immediately. Unsure \u2192 Pause \u2192 Ask \u2192 Escalate.', s['emphasis']))

    story.append(PageBreak())

    # ============ PART 8: DIET ENFORCEMENT ============
    story.append(SectionHeaderBar("DIET ENFORCEMENT"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Diet errors are not minor clerical issues. An incorrect feeding is an animal welfare event. It is treated as such in this system.', s['body']))
    story.append(Spacer(1, 6))

    # 3-Strike Ladder
    story.append(Paragraph('The 3-Strike Escalation Ladder \u2014 Diet Enforcement', s['h2']))
    story.append(Paragraph('This ladder applies to every feeding-related error: wrong food, wrong quantity, substitution without approval, wrong species diet, skipped feeding, incorrect documentation.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Strike 1 \u2014 Immediate Correction', s['h3']))
    story.append(Paragraph('The error is identified and corrected immediately. An internal note is made documenting what happened, when, and by whom. The correct feeding is completed and documented. The staff member is informed of what went wrong and what the correct procedure is.', s['body']))
    story.append(Paragraph('<b>Tone:</b> Corrective, not punitive. Everyone makes mistakes. This is where mistakes are caught and fixed.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Strike 2 \u2014 Formal Warning + Retraining', s['h3']))
    story.append(Paragraph('The same type of error has occurred again, OR a serious diet error has occurred. A formal written warning is issued. A one-on-one meeting is conducted with the staff member. The correct procedure is retrained in full. The staff member provides written acknowledgment that they understand the correct procedure and the consequences of continued errors. This documentation goes into the staff member\'s file.', s['body']))
    story.append(Paragraph('<b>Tone:</b> Serious and clear. The standard exists. It was explained. It was not followed. That cannot continue.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Strike 3 \u2014 Disciplinary Review', s['h3']))
    story.append(Paragraph('The staff member has been corrected. They have been formally warned. They have been retrained. The behavior has continued. A formal disciplinary review is initiated. This may result in: reassignment to a non-animal-care role, suspension, or termination. The decision is made by management in consultation with the owner.', s['body']))
    story.append(Paragraph('<b>Tone:</b> This is not a surprise. Every prior step was a warning. This is the consequence of not responding to those warnings.', s['body']))
    story.append(Spacer(1, 6))

    # Management Failure Clause
    story.append(Paragraph('Management Failure Clause', s['h2']))
    story.append(Paragraph('The 3-Strike Escalation Ladder applies equally to supervisory and management roles.', s['body']))
    story.append(Paragraph('If a manager approves incorrect feedings, allows substitutions without escalating, does not issue corrections when errors are observed, or signs off on incomplete or non-compliant feeding records \u2014 that manager is subject to the same 3-Strike Escalation Ladder.', s['body']))
    story.append(Paragraph('<b>Management Failure = same ladder. Same consequences. No exceptions.</b>', s['body_bold']))

    story.append(TealDivider())
    story.append(Spacer(1, 8))

    # Feeding Authority
    story.append(Paragraph('Feeding Authority is Steward-to-Steward Only', s['h2']))
    story.append(Paragraph('All feeding information comes directly from the owner. No software-generated diets. No third-party diet recommendations. No unauthorized software may generate or modify feeding protocols. If a diet sheet does not trace directly to the owner\'s instruction, it is void.', s['body']))

    # Governing Principle
    story.append(Paragraph('The Governing Principle', s['h2']))
    story.append(Paragraph('<b>Animal welfare overrides convenience. Consistency protects everyone.</b>', s['quote']))
    story.append(Paragraph('This is not a motivational phrase. It is the operational logic behind every diet rule in this system. When you follow the diet correctly, every time, you protect the animal. When you protect the animal, you protect the facility. When you protect the facility, you protect your job, your team, and every guest who walks through the door.', s['body']))
    story.append(Paragraph('Convenience has never been a valid reason to substitute a food item or feed an animal incorrectly. It never will be.', s['body']))

    story.append(PageBreak())

    # ============ GOLD STANDARD DIET SYSTEM ============
    story.append(SectionHeaderBar("GOLD STANDARD DIET SYSTEM"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>Purpose:</b> To eliminate SOP misinterpretation, staff inconsistency, diet drift, overprocessing (cutting, mixing, guessing), and incorrect species feeding. Replace with: visual pattern recognition + binary decision system.', s['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Core Principle:</b> "Match the bowl. Don\'t interpret."', s['body_bold']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('System Architecture \u2014 5 Integrated Layers', s['h2']))

    story.append(Paragraph('<b>1. BIOLOGICAL TRUTH LAYER</b>', s['h3']))
    story.append(Paragraph('Defines what each species actually is, what they naturally eat, and what breaks their system. Each animal classified by Diet Type and Primary Nutritional Driver.', s['body']))

    story.append(Paragraph('<b>2. DIET STRUCTURE MODEL</b>', s['h3']))
    story.append(Paragraph('Each species mapped into: A. CORRECT STRUCTURE (ratios, components, priorities) and B. WRONG STRUCTURE (common failure patterns, misinterpretations).', s['body']))

    story.append(Paragraph('<b>3. VISUAL ENFORCEMENT SYSTEM</b>', s['h3']))
    story.append(Paragraph('Replaces SOP reading, verbal instruction, and interpretation with visual pattern recognition. Components: Posters (per species), Side-by-Side Images, Binary Labels, Enforcement Line.', s['body']))

    story.append(Paragraph('<b>4. OPERATIONAL CONTROL SYSTEM</b>', s['h3']))
    story.append(Paragraph('Rules: No interpretation allowed. If it does not match the diet sheet, it is wrong. Food must visually match species pattern.', s['body']))

    story.append(Paragraph('<b>5. AI GOVERNANCE LAYER</b>', s['h3']))
    story.append(Paragraph('AI is used to display diets, generate posters, and support system enforcement. Diets are finalized \u2014 no AI modification of diets is permitted.', s['body']))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Universal Failure Patterns', s['h2']))
    for fp in [
        "VEGETABLE DRIFT \u2014 Staff default to carrots, squash, zucchini, mixed veg",
        "CHOPPING HABIT \u2014 Cutting everything unnecessarily, creating \"salad bowls\"",
        "PELLET OVERUSE \u2014 Pellets used as base, convenience feeding",
        "FRUIT MISUSE \u2014 Too much fruit, wrong species getting fruit",
        "MISSING CORE DIET \u2014 No hay (grazers), no protein (tegus), no root (porcupines)",
    ]:
        story.append(Paragraph(f'\u2022 {fp}', s['bullet']))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Core Control Mechanism', s['h2']))
    story.append(Paragraph('<b>Visual Matching Instead of Thinking:</b> Staff are not asked to understand biology, interpret ratios, or read SOPs. They are told: "Match the picture."', s['body']))
    story.append(Paragraph('<b>Binary Decisions:</b> correct / wrong. feed / fix. No gray area.', s['body']))
    story.append(Paragraph('<b>Removal of Cognitive Load:</b> No calculation. No interpretation. No memory required.', s['body']))

    story.append(PageBreak())

    # ============ GOLD STANDARD SPECIES DIET POSTERS ============
    story.append(SectionHeaderBar("GOLD STANDARD SPECIES DIET POSTERS"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('<b>MATCH THE BOWL \u2014 DO NOT GUESS</b>', s['body_bold']))
    story.append(Paragraph('Use the least processing necessary. Match the picture, don\'t interpret.', s['body']))
    story.append(Spacer(1, 6))

    species_posters = [
        ("RABBIT", "Grass grazer", "Hay = the diet", "Hay dominant, whole leafy greens, minimal extras", "Chopped lettuce, vegetable bowls, pellet heavy", "90% hay, small greens, rare fruit", "No cutting, no mixing", "Do I see hay?"),
        ("CAPYBARA", "Grass grazer", "", "Hay dominant, small greens", "Vegetable bowls, no hay", "80\u201390% hay, small greens", "", "Do I see hay?"),
        ("SLOTH", "Leaf fermenter", "", "Chow + fiber leaves", "Vegetable salad, no chow", "Chow base, leafy greens", "", "Do I see chow + leaves?"),
        ("PORCUPINE", "Leaf + root feeder", "", "Leaves + one root + fruit", "No root, soft salad", "Leaves dominant, one root, small fruit", "", "Do I see a root?"),
        ("TEGU", "Protein-driven omnivore", "", "Protein visible, greens, small fruit", "No protein, fruit heavy", "40\u201360% protein, greens, small fruit", "", "Do I see protein?"),
        ("KINKAJOU", "Fruit specialist", "", "Fruit dominant, small chow", "Pellet heavy, vegetable mix", "60\u201370% fruit, 20\u201330% chow", "", "Do I see mostly fruit?"),
        ("SPIDER MONKEY", "Fruit specialist", "", "Fruit dominant, browse, small chow", "Vegetables, no fruit", "65\u201375% fruit, 20\u201325% leaves", "", "Is fruit dominant?"),
        ("WALLABY", "Grass grazer", "", "Hay dominant", "Vegetable bowls, fruit", "80\u201390% hay", "", "Do I see hay?"),
        ("PATAGONIAN CAVY", "Grass grazer", "", "Hay dominant", "Vegetables, fruit", "80\u201390% hay", "", "Do I see hay?"),
        ("TOUCAN", "Fruit + low iron", "", "Fruit dominant, softbill", "Pellet heavy, vegetables", "60\u201370% fruit", "", "Do I see fruit?"),
    ]

    for name, animal_type, extra_type, correct, wrong, build, prep, check in species_posters:
        blk = []
        blk.append(Paragraph(f'<b>{name}</b> \u2014 GOLD STANDARD DIET', s['h3']))
        type_text = f'<b>What this animal is:</b> {animal_type}'
        if extra_type:
            type_text += f'. {extra_type}'
        blk.append(Paragraph(type_text, s['body']))
        blk.append(Paragraph(f'<b>Correct:</b> {correct}', s['body']))
        blk.append(Paragraph(f'<b>Wrong:</b> {wrong}', s['body']))
        blk.append(Paragraph(f'<b>Simple Build:</b> {build}', s['body']))
        if prep:
            blk.append(Paragraph(f'<b>Prep Rule:</b> {prep}', s['body']))
        blk.append(Paragraph(f'<b>3-Second Check:</b> {check}', s['body']))
        blk.append(Spacer(1, 6))
        story.append(KeepTogether(blk))

    build_pdf(SM_DIR, "SM_01_Feeding_Complete.pdf", "Feeding Complete Manual", "Feeding Complete", story)


# ══════════════════════════════════════════════════════════════════════════════
# SM_02: Operations Complete
# ══════════════════════════════════════════════════════════════════════════════

def build_sm02():
    print("Building SM_02_Operations_Complete.pdf ...")
    s = make_sm_styles()
    story = []

    story.append(PageOneHeaderBar("Operations Complete Manual"))
    story.append(Spacer(1, 12))

    # TOC on page 1
    story.append(Paragraph('TABLE OF CONTENTS', s['h1']))
    toc_items = [
        "1. Operational Standards (Part 1)",
        "2. How We Work Here (Part 3)",
        "3. The Do Not List (Part 9)",
        "4. Cleaning and Maintenance (Part 5)",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s['toc']))
    story.append(PageBreak())

    # ============ PART 1: OPERATIONAL STANDARDS ============
    story.append(SectionHeaderBar("OPERATIONAL STANDARDS"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('These are the ten rules that govern everything. They are posted on every wall. They are non-negotiable. If you violate these rules, you will be corrected, warned, or disciplined. There are no exceptions.', s['body']))
    story.append(Spacer(1, 6))

    op_rules = [
        ("Rule 1: If it is not assigned, written, or approved \u2014 do not do it.",
         "No action without authorization. No exceptions.",
         "This is the single most important rule in this facility. It prevents unauthorized changes, unapproved purchases, improvised procedures, and system drift. If nobody told you to do it, if it is not written down somewhere as your task, if nobody approved it \u2014 you do not do it. You stop and you ask."),
        ("Rule 2: Animal welfare overrides everything.",
         "Biology first. Convenience never.",
         "Every animal in this facility depends on you. Their diet, their habitat, their health \u2014 all of it comes before your convenience, your schedule, or your opinion. If you are rushing and an animal needs care, the animal wins. If you think something is wrong with an animal, you report it immediately. You do not wait."),
        ("Rule 3: Follow the written diet exactly.",
         "No substitutions. No guessing. No skipping steps.",
         "The diet sheet tells you exactly what to prepare, how much, and how. You do not change it. You do not substitute items because you ran out of something. You do not guess at quantities. After you prepare the food, verify it matches the diet sheet visually. Then you deliver it. If the diet sheet is wrong, you report it. You do not fix it yourself.\n\nQuantities are listed as whole items \u2014 a papaya, a mango, a count of bananas. Not by weight, not by grams. Cut items in half at most."),
        ("Rule 4: Nothing gets thrown away. All food follows the Zero Waste loop.",
         "Uneaten food goes to collection. Not the trash.",
         "We were throwing away 15 pounds of food and produce every day. That is over. Nothing goes in the trash. Uneaten food goes in the collection bin. It gets sorted into compost, controlled protein, or reject. If you are about to throw something away \u2014 stop. You are breaking the system.\n\nLeftovers Protocol: At end of day, do not leave food overnight. Place in a Ziploc container marked with source exhibit. Put it in the fridge. Morning: serve leftovers FIRST. As they decline in freshness, feed to birds. Do NOT throw food away."),
        ("Rule 5: If you are not sure \u2014 STOP. ASK. WAIT.",
         "Uncertainty is not a reason to act. It is a reason to pause.",
         "If you do not know how to do something, do not guess. If you are not sure whether you should do something, do not try it. If you think something might be wrong but you are not sure, do not ignore it. Stop what you are doing. Ask someone who has authority to answer. Wait for the answer before you act."),
        ("Rule 6: No record = did not happen.",
         "Documentation is proof. Everything is verified.",
         "If you did a task but there is no record, it did not happen as far as the system is concerned. This applies to feedings, cleaning, food prep, waste sorting, and any task that requires verification."),
        ("Rule 7: Do not move, modify, or add anything to any exhibit.",
         "Nothing changes without written approval.",
         "Exhibits are designed for biological and behavioral reasons you may not understand. That is fine. It is not your job to understand the design. It is your job to leave it alone. Do not place toy animals inside exhibits. Do not relocate any animal from its assigned exhibit. Do not add decorations, objects, or personal items."),
        ("Rule 8: Do not introduce, adopt, or use any software or system without owner approval.",
         "If it was not approved, it does not exist.",
         "This rule exists because unauthorized software adoption has caused significant operational damage in the past. That will not happen again. If a vendor offers you a tool, the answer is no until the owner evaluates it."),
        ("Rule 9: Only authorized individuals approve purchases, sign contracts, or modify operations.",
         "If you did not get written approval to spend money or change a system, stop.",
         "You cannot order product without upper manager approval. You cannot sign a vendor contract without upper manager approval. Credit card holders have a $350 maximum per purchase."),
        ("Rule 10: Workspaces are for work. Not storage. Not socializing. Not sitting.",
         "If you are clocked in, you are working.",
         "Every desk, drawer, and cabinet must be clean and organized. If something is broken, report it. If you are clocked in, you are actively working \u2014 not sitting in an office, not hanging out in a back room, not scrolling your phone. This applies to everyone. Managers too."),
    ]

    for title, subtitle, desc in op_rules:
        story.append(Paragraph(f'<b>{title}</b>', s['h3']))
        story.append(Paragraph(subtitle, s['emphasis']))
        for para in desc.split('\n\n'):
            story.append(Paragraph(para, s['body']))
        story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Violation of these rules will result in corrective action. These are non-negotiable.</b>', s['body_bold']))

    story.append(PageBreak())

    # ============ PART 3: HOW WE WORK HERE ============
    story.append(SectionHeaderBar("HOW WE WORK HERE"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('This section defines the operating system of this facility. How tasks work, how authority works, and what happens when things go wrong.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Three Questions', s['h2']))
    story.append(Paragraph('Before you do anything, ask yourself:', s['body']))
    story.append(Paragraph('\u2022 <b>1. Was it assigned?</b>', s['bullet_bold']))
    story.append(Paragraph('\u2022 <b>2. Is it written?</b>', s['bullet_bold']))
    story.append(Paragraph('\u2022 <b>3. Was it approved?</b>', s['bullet_bold']))
    story.append(Paragraph('If the answer to all three is no \u2014 you do not do it. You stop and you ask.', s['emphasis']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Claim-Based Work System', s['h2']))
    story.append(Paragraph('<b>1.</b> A task is posted. It appears on the task board, in a message, or from a manager.', s['body']))
    story.append(Paragraph('<b>2.</b> You claim it. You say: "I will take this." That means it is now yours.', s['body']))
    story.append(Paragraph('<b>3.</b> You do it. You execute the task according to the written procedure.', s['body']))
    story.append(Paragraph('<b>4.</b> It gets verified. A manager confirms it was done correctly.', s['body']))
    story.append(Paragraph('If you do not claim it, it is not yours. If nobody claims it, we have a problem \u2014 and that problem gets escalated immediately.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Authorization Model', s['h2']))
    story.append(Paragraph('\u2022 <b>Owner:</b> Sets direction, standards, and policy. Final authority on system changes, exhibit design, diet formulas, and policy changes.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Upper Managers:</b> Approve all purchases (credit card holders limited to $350 max). Approve vendor contracts. Approve animal moves and vet visits. Identify issues BEFORE they become problems \u2014 notify the owner for decisions.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Staff:</b> Execute claimed tasks within existing procedures. Cannot approve anything. If something requires approval, escalate to a manager. If the manager cannot approve it, it goes to the owner.', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Escalation Ladder', s['h2']))
    story.append(Paragraph('\u2022 <b>Strike 1: Correction.</b> You made a mistake. You are told what you did wrong and how to fix it. Everyone makes mistakes. This is normal.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Strike 2: Formal warning + retraining.</b> You made the same mistake again, or you made a serious error. You receive a formal warning. You are retrained on the correct procedure. This goes in your file.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Strike 3: Disciplinary action.</b> You have been corrected and warned. The behavior continues. At this point, disciplinary action is taken. This may include suspension, reassignment, or termination.', s['bullet']))
    story.append(Paragraph('<b>This applies to everyone.</b> Staff, managers, everyone. Animal welfare overrides convenience, and accountability overrides seniority.', s['body_bold']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Technology and Software Governance', s['h2']))
    story.append(Paragraph('<b>Rule: No software, app, or tracking system is adopted without owner written approval.</b>', s['body_bold']))
    story.append(Paragraph('\u2022 No apps for task management without owner approval.', s['bullet']))
    story.append(Paragraph('\u2022 No scheduling software without owner approval.', s['bullet']))
    story.append(Paragraph('\u2022 No diet or feeding software without owner approval.', s['bullet']))
    story.append(Paragraph('\u2022 No communication platforms (beyond what we already use) without owner approval.', s['bullet']))
    story.append(Paragraph('\u2022 If a vendor offers a tool, the answer is NO until the owner evaluates it.', s['bullet']))
    story.append(Paragraph('<b>If you are currently using any software that was not explicitly approved by the owner, stop using it and report it.</b>', s['body_bold']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Purchasing Authority', s['h2']))
    story.append(Paragraph('<b>Rule: No purchases without upper manager approval.</b>', s['body_bold']))
    story.append(Paragraph('\u2022 Only upper managers or owner-designated individuals can order product.', s['bullet']))
    story.append(Paragraph('\u2022 Only the owner can approve new vendors.', s['bullet']))
    story.append(Paragraph('\u2022 All purchases require documentation (what was ordered, from whom, how much, why).', s['bullet']))
    story.append(Paragraph('\u2022 Credit card holders have a $350 maximum. Anything above that goes to the owner.', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Meeting Rules', s['h2']))
    story.append(Paragraph('Team meetings: maximum 15 minutes, every morning before work. Manager meetings: maximum 15 minutes. No meetings over 15 minutes without authorization.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Employee Recognition', s['h2']))
    story.append(Paragraph('Employee of the Week: $50 bonus. Happiest Employee of the Week: $50 bonus.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Staff Appearance', s['h2']))
    story.append(Paragraph('Appropriate shirt or vest worn at all times. Recognition pins: 1-year, 2-year, 3-year, etc. Wear appropriate pin for your tenure. Identification tag: shows which animals you are skilled at and which department you belong to.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Miranda Rights Doctrine', s['h2']))
    story.append(Paragraph('Before any correction or escalation, three questions must be answered:', s['body']))
    story.append(Paragraph('\u2022 1. What constraint existed?', s['bullet']))
    story.append(Paragraph('\u2022 2. Was the action discretionary or required?', s['bullet']))
    story.append(Paragraph('\u2022 3. Is this a one-time situation or a repeated pattern?', s['bullet']))
    story.append(Paragraph('If any answer is unclear, escalation pauses. No public correction without clarification. No attributing intent without verification.', s['body']))
    story.append(Paragraph('<b>Core statement: Observe first. Clarify constraints. Then decide.</b>', s['body_bold']))

    story.append(PageBreak())

    # ============ PART 9: DO NOT LIST ============
    story.append(SectionHeaderBar("THE DO NOT LIST"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('These are the things you must never do. This is not a suggestion list. These are absolute prohibitions.', s['body']))
    story.append(Spacer(1, 8))

    do_nots = [
        "Do not act without authorization.",
        "Do not substitute diet items.",
        "Do not throw away food.",
        "Do not improvise or guess.",
        "Do not move, modify, or add to exhibits.",
        "Do not relocate animals.",
        "Do not use unapproved software or systems.",
        "Do not edit checklists or procedures.",
        "Do not make up facts about animals.",
        "Do not sit in offices doing nothing.",
        "Do not create your own signs, materials, or educational content.",
        "Do not bring in outside vendors without owner approval.",
        "Do not sign contracts or agreements on behalf of the facility.",
        "Do not order product without owner approval.",
        "Do not change any system, no matter how small, without approval.",
        "Do not move any animal without upper manager approval.",
        "Do not take any animal to the vet without upper manager approval.",
        "Do not hold meetings longer than 15 minutes without authorization.",
        "Do not rake exhibits to bare dirt \u2014 maintain natural biome.",
        "Do not use grams or weight measurements for feeding \u2014 use whole items only.",
        "Do not remove hay from the ground \u2014 horses and hay-eating animals eat it there.",
    ]

    for item in do_nots:
        story.append(Paragraph(f'\u2022 {item}', s['red_bullet']))

    story.append(Spacer(1, 8))
    story.append(Paragraph('<b>When in doubt: STOP \u2192 ASK \u2192 WAIT.</b>', s['body_bold']))

    story.append(PageBreak())

    # ============ PART 5: CLEANING ============
    story.append(SectionHeaderBar("CLEANING AND MAINTENANCE"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('Acrylic Windows', s['h2']))
    story.append(Paragraph('Blue rags + distilled water ONLY. Nothing else. No Windex. No paper towels. No cleaning sprays. Blue rags and distilled water. That is it.', s['body']))

    story.append(Paragraph('Exhibits', s['h2']))
    story.append(Paragraph('Virkon for disinfection. Follow the label instructions exactly. If you do not know the correct dilution ratio, ask before mixing.', s['body']))

    story.append(Paragraph('Food Prep Areas', s['h2']))
    story.append(Paragraph('Clean, sanitize, document completion. Every food prep surface must be cleaned and sanitized after each use.', s['body']))

    build_pdf(SM_DIR, "SM_02_Operations_Complete.pdf", "Operations Complete Manual", "Operations Complete", story)


# ══════════════════════════════════════════════════════════════════════════════
# SM_03: Guest Experience Complete
# ══════════════════════════════════════════════════════════════════════════════

def build_sm03():
    print("Building SM_03_Guest_Experience_Complete.pdf ...")
    s = make_sm_styles()
    story = []

    story.append(PageOneHeaderBar("Guest Experience Complete Manual"))
    story.append(Spacer(1, 12))

    # TOC on page 1
    story.append(Paragraph('TABLE OF CONTENTS', s['h1']))
    toc_items = [
        "1. Guest-Facing Standards (Part 2)",
        "2. The Education System: LIFE (Part 11)",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s['toc']))
    story.append(PageBreak())

    # ============ PART 2: GUEST-FACING ============
    story.append(SectionHeaderBar("GUEST-FACING STANDARDS"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('These rules govern how guests experience this facility. Guests judge us in the first 30 seconds. Every second after that confirms or corrects their first impression.', s['body']))
    story.append(Spacer(1, 6))

    guest_rules = [
        ("Rule 1: You are on stage. Smile. Greet every guest.",
         "Guests see you before they see the animals. Your energy sets their experience.",
         "From the moment you clock in, you are performing. Not performing a fake character \u2014 being genuinely present and welcoming. Make eye contact. Say hello. If a family walks by and you ignore them, you just told them they do not matter. That is not how we operate."),
        ("Rule 2: The facility must be visibly clean at all times.",
         "Floors, glass, exhibits, restrooms, walkways. If it looks dirty, it is dirty. Fix it now.",
         "Do not walk past trash. Do not walk past a smudged window. Do not walk past a dirty floor and tell yourself someone else will handle it. If you see it, you own it. Pick it up, wipe it down, report it. Guests notice everything."),
        ("Rule 3: The facility must smell clean.",
         "No odor from waste, food prep, or neglect should reach guest areas. Ever.",
         "Guests may forgive a small visual issue. They will not forgive a bad smell. If you can smell waste, food residue, or neglect in any guest-accessible area, it is an emergency. Fix it immediately or report it."),
        ("Rule 4: Animals must appear healthy, active, and in a quality environment.",
         "Guests observe. If an exhibit looks neglected, they see it. Standards are not negotiable.",
         "Guests look at exhibits the way you look at a restaurant kitchen. If it looks off, they lose trust. Animals must be active and engaged during guest hours. Exhibits must be clean, well-maintained, and properly lit. If an animal appears unwell, report it immediately \u2014 do not wait for the end of your shift."),
        ("Rule 5: Guest interaction is personal. Make eye contact. Be present.",
         "You are not a body in a uniform. You are the reason someone remembers this place.",
         "The difference between a forgettable visit and a memorable one is you. When a guest approaches you, give them your full attention. Put your phone away. Stop what you are doing. Be present. Be helpful. Be real."),
        ("Rule 6: If a guest asks a question you cannot answer, say so honestly.",
         '"That is a great question. Let me find someone who can help, or scan the QR code for more."',
         "Do not make up facts about animals. Do not guess at information. Do not pretend to know something you do not know. Honesty builds trust. Making things up destroys it. Every exhibit has QR codes that lead to accurate information. Direct guests to those resources if you are unsure."),
        ("Rule 7: Education is always on. Signs, screens, and QR codes must be correct.",
         "If a screen is wrong or a sign is missing, report it immediately. Do not ignore it.",
         "This facility runs an education system called LIFE \u2014 Language, Intelligence, Form, Ecology. It is not a gimmick. Every sign, QR code, and exhibit teaches visitors something real. If you notice a screen displaying wrong information, a missing sign, or a broken QR code, report it immediately. Do not try to fix it yourself. Do not create your own replacement. Report it and let the system handle it."),
        ("Rule 8: Encounters are joyful. Most are free. Feeding costs money; joy does not.",
         "Do not make guests feel like every experience costs money. Free interaction is the product.",
         "Most animal encounters at this facility are free. That is by design. The joy of touching, seeing, and learning about animals is the core experience. Feeding is what costs money. Do not push paid experiences. Do not make guests feel like they need to pay to have a good time. If they want to feed an animal, tell them the cost. If they just want to interact, welcome them warmly."),
        ("Rule 9: No personal items, clutter, food, or drinks visible in guest areas.",
         "Your phone, your water bottle, your bag \u2014 not on the floor, not on a ledge, not in sight.",
         "Guest areas must look intentional and professional at all times. Your personal belongings are not part of the guest experience. Keep them in designated areas. If a guest can see your stuff, you are doing it wrong."),
        ("Rule 10: Orderly and organized. Every area a guest can see must look intentional.",
         "No exposed cords, no random supplies, no half-finished setups. If it looks like backstage, fix it.",
         "Guests should never see behind the curtain. No extension cords draped across walkways. No boxes of supplies stacked in corners. No partially assembled displays. If a guest-visible area looks messy, unfinished, or chaotic, fix it before they see it."),
    ]

    for title, subtitle, desc in guest_rules:
        story.append(Paragraph(f'<b>{title}</b>', s['h3']))
        story.append(Paragraph(subtitle, s['emphasis']))
        story.append(Paragraph(desc, s['body']))
        story.append(Spacer(1, 4))

    story.append(Paragraph('<b>Guests judge us in the first 30 seconds. Every second after confirms or corrects.</b>', s['body_bold']))

    story.append(PageBreak())

    # ============ PART 11: EDUCATION SYSTEM ============
    story.append(SectionHeaderBar("THE EDUCATION SYSTEM: LIFE"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('What LIFE Means', s['h2']))
    story.append(Paragraph('<b>LIFE</b> stands for <b>Language, Intelligence, Form, Ecology.</b>', s['body']))
    story.append(Paragraph('It is a non-ideological, mechanism-first education system. That means:', s['body']))
    story.append(Paragraph('\u2022 It teaches how systems work, not what to believe.', s['bullet']))
    story.append(Paragraph('\u2022 It avoids persuasion, ideology, and moral imposition.', s['bullet']))
    story.append(Paragraph('\u2022 It is based on observation first, interpretation second.', s['bullet']))
    story.append(Paragraph('\u2022 It scales across children, adults, and staff.', s['bullet']))
    story.append(Paragraph('<b>Your role in the education system is simple: Do not get in the way of it.</b>', s['body_bold']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Core Principles', s['h2']))
    story.append(Paragraph('\u2022 <b>1. Reality-Based Education.</b> Everything taught here is based on observable reality. Not opinion. Not ideology. Not belief.', s['bullet']))
    story.append(Paragraph('\u2022 <b>2. Experiential Learning.</b> Visitors learn by interacting with real systems \u2014 real animals, real habitats, real biological processes.', s['bullet']))
    story.append(Paragraph('\u2022 <b>3. Responsibility &amp; Consequence.</b> Actions have results. That is what we teach. Not morals, not lessons \u2014 consequences.', s['bullet']))
    story.append(Paragraph('\u2022 <b>4. Continuity of Knowledge.</b> What you learn here connects to what you learn everywhere else.', s['bullet']))
    story.append(Paragraph('\u2022 <b>5. Reflection &amp; Metacognition.</b> We encourage visitors to think about how they think.', s['bullet']))
    story.append(Paragraph('\u2022 <b>6. Reality-First Governor.</b> If something cannot be tested, updated, or proven wrong, it gets labeled as speculation \u2014 not fact.', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Epistemic Gating \u2014 Who Sees What', s['h2']))
    story.append(Paragraph("<b>Children's Lens:</b> Observation-first. No ideology. No burden. Keep it simple. Let them see, touch, and ask questions.", s['body']))
    story.append(Paragraph('<b>Adult Lens:</b> May destabilize beliefs. Requires voluntary engagement. Adults can handle complexity, contradiction, and discomfort \u2014 but they choose to engage. We do not force it.', s['body']))
    story.append(Paragraph('<b>Staff Lens:</b> Learning through building. Accountability through ownership. You learn the system by operating it.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('What Staff Must Know About Education', s['h2']))
    story.append(Paragraph('\u2022 <b>Do not get in the way of the system.</b> The education system runs through signs, QR codes, digital totems, and narrative suites. You do not need to "teach" visitors anything.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Do not make up facts about animals.</b> If you do not know something, say so. Direct guests to the QR code for accurate information.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Do not move, edit, or remove signs.</b> Signs are part of the education system. If a sign is wrong, missing, or damaged \u2014 report it. Do not replace it with your own version.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Do not create your own materials.</b> No handwritten signs. No printed sheets from the internet. No personal educational displays. All education content comes from central control.', s['bullet']))
    story.append(Paragraph('\u2022 <b>Do not tell visitors what to think.</b> The system is designed to let visitors observe and reach their own conclusions. You are not here to persuade anyone of anything.', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Visitor Entry Script', s['h2']))
    story.append(Paragraph('Welcome to LIFE \u2014 Language, Intelligence, Form, Ecology.', s['quote']))
    story.append(Paragraph('This is an education environment. You are not here to be persuaded. You will encounter systems and limits.', s['quote']))
    story.append(Paragraph('Observe before judging. You may move at your own pace. Staff can read signage with you.', s['quote']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('The Micro-Sign System', s['h2']))
    story.append(Paragraph('Every zone in the facility has a micro-sign. The sign says:', s['body']))
    story.append(Paragraph('<b>Observe first. Then ask your AI.</b>', s['body_bold']))
    story.append(Paragraph('"What system is this, and what does it need to work?"', s['body']))
    story.append(Spacer(1, 4))
    story.append(Paragraph('Optional prompts:', s['body']))
    story.append(Paragraph('\u2022 What makes this possible?', s['bullet']))
    story.append(Paragraph('\u2022 What makes this impossible?', s['bullet']))
    story.append(Paragraph('\u2022 What changes if one part is removed?', s['bullet']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Structure vs. Transmission', s['h2']))
    story.append(Paragraph('<b>Structure</b> = truth. The actual mechanisms, systems, and facts.', s['body']))
    story.append(Paragraph('<b>Transmission</b> = delivery. How we present that truth \u2014 stories, metaphors, visuals.', s['body']))
    story.append(Paragraph('Structure is fixed. It does not change based on the audience. Transmission is flexible. It changes based on who is learning.', s['body']))
    story.append(Paragraph('<b>If structure and transmission ever conflict, structure wins.</b> Always.', s['body_bold']))

    build_pdf(SM_DIR, "SM_03_Guest_Experience_Complete.pdf", "Guest Experience Complete Manual", "Guest Experience", story)


# ══════════════════════════════════════════════════════════════════════════════
# SM_04: New Hire Packet
# ══════════════════════════════════════════════════════════════════════════════

def build_sm04():
    print("Building SM_04_New_Hire_Packet.pdf ...")
    s = make_sm_styles()
    story = []

    story.append(PageOneHeaderBar("New Hire Packet"))
    story.append(Spacer(1, 12))

    # TOC on page 1
    story.append(Paragraph('TABLE OF CONTENTS', s['h1']))
    toc_items = [
        "1. Employee Packet",
        "2. Staff Packet",
        "3. The Do Not List",
        "4. Sign-Off Sheet",
    ]
    for item in toc_items:
        story.append(Paragraph(item, s['toc']))
    story.append(PageBreak())

    # ============ EMPLOYEE PACKET ============
    story.append(SectionHeaderBar("EMPLOYEE PACKET"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('This packet explains exactly how employees are expected to work on the floor, with animals, and with guests. These are rules, not suggestions.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Your Role', s['h2']))
    story.append(Paragraph('Your job is to be visible, helpful, and engaged. If a guest can see you, you should be interacting or assisting. If you pass a guest without acknowledging them, you missed your job. We are on stage all day. This is a performance role.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Guest Interaction \u2014 REQUIRED', s['h2']))
    story.append(Paragraph('\u2022 Smile and greet guests when they enter your area', s['bullet']))
    story.append(Paragraph('\u2022 Offer help or information proactively', s['bullet']))
    story.append(Paragraph('\u2022 Do not hide in back rooms', s['bullet']))
    story.append(Paragraph('\u2022 Phones away when guest-facing', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Animal Interaction \u2014 BASELINE RULES (LOCKED)', s['h2']))
    story.append(Paragraph('Animals that participate in guest interactions are not fed to fullness before guest hours.', s['body']))
    story.append(Paragraph('\u2022 Baseline nutrition only before opening', s['bullet']))
    story.append(Paragraph('\u2022 Guest feeding is primary enrichment where applicable', s['bullet']))
    story.append(Paragraph('\u2022 No substitutions or extra food', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Feeding Execution', s['h2']))
    story.append(Paragraph('\u2022 Follow the exhibit feeding SOP exactly', s['bullet']))
    story.append(Paragraph('\u2022 Food prepared fresh daily', s['bullet']))
    story.append(Paragraph('\u2022 If unsure, stop and ask a manager', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Cleanliness \u2014 CONTINUOUS', s['h2']))
    story.append(Paragraph('\u2022 Pick up visible trash immediately', s['bullet']))
    story.append(Paragraph('\u2022 Do not walk past litter', s['bullet']))
    story.append(Paragraph('\u2022 Clean as you go', s['bullet']))
    story.append(Paragraph('\u2022 Your mother does not work here \u2014 clean up after yourself', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Clean-for-Feed Program', s['h2']))
    story.append(Paragraph('Guests may exchange found trash for animal food at staff discretion. This is encouraged and controlled by staff.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Field Trips \u2014 IMPORTANT', s['h2']))
    story.append(Paragraph('\u2022 Encounters are included', s['bullet']))
    story.append(Paragraph('\u2022 Do not charge', s['bullet']))
    story.append(Paragraph('\u2022 Do not refuse experiences', s['bullet']))
    story.append(Paragraph('If a group has a question, get a manager.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('What NOT to Do', s['h2']))
    story.append(Paragraph('\u2022 Do not make up prices or rules', s['bullet']))
    story.append(Paragraph('\u2022 Do not deny included experiences', s['bullet']))
    story.append(Paragraph('\u2022 Do not alter exhibits or drill into acrylic', s['bullet']))
    story.append(Paragraph('\u2022 Do not feed animals incorrectly', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('When to Escalate', s['h2']))
    story.append(Paragraph('If something feels wrong or unclear: Stop. Ask a manager. Do not guess. Consistency protects animals and guests.', s['body']))

    story.append(PageBreak())

    # ============ STAFF PACKET ============
    story.append(SectionHeaderBar("STAFF PACKET"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('This packet explains how to work here day-to-day. It is not a philosophy document. It tells you what to do, what not to do, and what is expected while you are clocked in.', s['body']))
    story.append(Spacer(1, 6))

    story.append(Paragraph('Your Role', s['h2']))
    story.append(Paragraph('If you are clocked in, your job is to be visible, guest-facing, and engaged unless you are on a specific assigned task. This is a performance expectation, not a personality judgment.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Guest Interaction', s['h2']))
    story.append(Paragraph('\u2022 Acknowledge guests when you pass them', s['bullet']))
    story.append(Paragraph('\u2022 Smile and offer help naturally', s['bullet']))
    story.append(Paragraph('\u2022 Follow staff guidance language', s['bullet']))
    story.append(Paragraph('\u2022 Point to signs and screens rather than explaining', s['bullet']))
    story.append(Paragraph('Passing a guest without acknowledgment is a failure of the role.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Animals Come First', s['h2']))
    story.append(Paragraph('Animals choose how and when to engage. If an animal does not want to interact, the interaction pauses or ends. Staff guide interactions calmly and protect animal comfort at all times.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Free vs Paid Experiences', s['h2']))
    story.append(Paragraph('Most animal interactions are free. Payment applies only when food, preparation, or extended staff time is required. Staff may offer free experiences at their discretion when appropriate.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Discretion', s['h2']))
    story.append(Paragraph('You may offer free experiences to create goodwill or when a guest appears unable to pay. You do not need to justify reasonable discretion. If unsure, ask a lead.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Where You Work', s['h2']))
    story.append(Paragraph('\u2022 Default position is on the floor', s['bullet']))
    story.append(Paragraph('\u2022 Back rooms are for assigned, time-limited tasks only', s['bullet']))
    story.append(Paragraph('\u2022 Back rooms are not places to hide', s['bullet']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Cleanup Responsibility', s['h2']))
    story.append(Paragraph('Clean as you go. Reset your space. Do not leave work for others. Your mother does not work here.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('What Not to Do', s['h2']))
    story.append(Paragraph('\u2022 Do not negotiate rules or pricing', s['bullet']))
    story.append(Paragraph('\u2022 Do not improvise explanations', s['bullet']))
    story.append(Paragraph('\u2022 Do not create signs or instructions', s['bullet']))
    story.append(Paragraph('\u2022 Do not argue with guests', s['bullet']))
    story.append(Paragraph('If there is a problem, escalate to a lead.', s['body']))
    story.append(Spacer(1, 4))

    story.append(Paragraph('Final Reminder', s['h2']))
    story.append(Paragraph('When systems are followed: Guests feel calm. Animals feel safe. Staff feel protected. Work runs smoothly.', s['body']))

    story.append(PageBreak())

    # ============ DO NOT LIST ============
    story.append(SectionHeaderBar("THE DO NOT LIST"))
    story.append(Spacer(1, 8))

    story.append(Paragraph('These are the things you must never do. This is not a suggestion list. These are absolute prohibitions.', s['body']))
    story.append(Spacer(1, 8))

    do_nots = [
        "Do not act without authorization.",
        "Do not substitute diet items.",
        "Do not throw away food.",
        "Do not improvise or guess.",
        "Do not move, modify, or add to exhibits.",
        "Do not relocate animals.",
        "Do not use unapproved software or systems.",
        "Do not edit checklists or procedures.",
        "Do not make up facts about animals.",
        "Do not sit in offices doing nothing.",
        "Do not create your own signs, materials, or educational content.",
        "Do not bring in outside vendors without owner approval.",
        "Do not sign contracts or agreements on behalf of the facility.",
        "Do not order product without owner approval.",
        "Do not change any system, no matter how small, without approval.",
        "Do not move any animal without upper manager approval.",
        "Do not take any animal to the vet without upper manager approval.",
        "Do not hold meetings longer than 15 minutes without authorization.",
        "Do not rake exhibits to bare dirt \u2014 maintain natural biome.",
        "Do not use grams or weight measurements for feeding \u2014 use whole items only.",
        "Do not remove hay from the ground \u2014 horses and hay-eating animals eat it there.",
    ]

    for item in do_nots:
        story.append(Paragraph(f'\u2022 {item}', s['red_bullet']))

    story.append(Spacer(1, 8))
    story.append(Paragraph('<b>When in doubt: STOP \u2192 ASK \u2192 WAIT.</b>', s['body_bold']))

    story.append(PageBreak())

    # ============ SIGN-OFF ============
    story.append(SectionHeaderBar("SIGN-OFF"))
    story.append(Spacer(1, 8))

    signoff_items = [
        "I have read this entire document.",
        "I understand the Owner's Top Ten \u2014 Operational Standards.",
        "I understand the Owner's Top Ten \u2014 Guest-Facing Standards.",
        "I understand how tasks work (claim-based system).",
        "I understand the authorization model.",
        "I understand the diet verification protocol.",
        "I understand the Zero Waste Food Loop.",
        "I understand the cleaning standards.",
        "I understand the education system (LIFE).",
        "I understand the exhibit integrity rules.",
        "I understand the technology governance rules.",
        "I understand the purchasing authority rules.",
        "I understand the workspace standards.",
        "I understand the Do Not List.",
        "I understand the escalation process: correction, warning, disciplinary action.",
        "I had the opportunity to ask questions.",
        "I understand that if I am unsure about something, I will stop and ask before acting.",
        "I understand the Miranda Rights doctrine and the three-question checklist.",
        "I understand that feeding uses whole items \u2014 no grams, no weight measurements.",
        "I understand that upper managers approve purchases and animal moves.",
    ]

    for item in signoff_items:
        story.append(Paragraph(item, s['body']))

    story.append(Spacer(1, 20))

    # Signature lines
    sig_style = ParagraphStyle('SigLine', fontName='Inter', fontSize=11, leading=22, textColor=DARK)
    story.append(Paragraph('<b>Employee Name (print):</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Employee Signature:</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Date:</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 16))
    story.append(Paragraph('<b>Conducted By (print):</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Conductor Signature:</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>Date:</b> _______________________________________________', sig_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph('<i>This document is retained by management. A copy may be provided to the employee upon request.</i>', s['small']))

    build_pdf(SM_DIR, "SM_04_New_Hire_Packet.pdf", "New Hire Packet", "New Hire Packet", story)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("Building ALL 11 Staff Deployment PDFs (No Covers)")
    print("=" * 60)
    print()

    # Quick Reference Cards
    print("--- Quick Reference Cards ---")
    build_qr01()
    build_qr02()
    build_qr03()
    build_qr04()
    build_qr05()
    build_qr06()
    build_qr07()

    print()

    # Complete Manuals
    print("--- Complete Manuals ---")
    build_sm01()
    build_sm02()
    build_sm03()
    build_sm04()

    print()
    print("=" * 60)
    print("All 11 PDFs built successfully!")
    print("=" * 60)
