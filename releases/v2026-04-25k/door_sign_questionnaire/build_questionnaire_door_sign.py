"""
Encounter Door Sign — Questionnaire / Fill-In Edition
v2026-04-25k

Replaces the rules-heavy v2026-04-25j door sign per user direction:
  - Take all the rules away.
  - USDA-governed framing is most prominent.
  - Encounter philosophy is a paragraph, not a bullet list.
  - Age rule explicit: 5+ with adult; 12+ alone (NOT in alone, but they may attend).
    Actually per user: "the youngest you could probably go in there would be like 12 by yourself"
    so 5+ accompanied; under 5 cannot enter — instead the harness/field-trip program.
  - Each substantive content block has FILL-IN lines so the user can author the text.
  - Multiple-choice radio buttons next to options where ambiguity exists.
  - Two sites: HOU (Houston Interactive Aquarium & Animal Preserve) + SA (San Antonio Aquarium).
  - Brown palette, locked.

This is an APPROVAL DRAFT — printed, marked up by Ammon, then re-rendered as final.
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# --- Fonts ---
FONT_DIR = "/tmp/fonts"
pdfmetrics.registerFont(TTFont("DMSans-Bold", f"{FONT_DIR}/DMSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DMSans-SemiBold", f"{FONT_DIR}/DMSans-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("DMSans", f"{FONT_DIR}/DMSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DMSans-Italic", f"{FONT_DIR}/DMSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Inter", f"{FONT_DIR}/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", f"{FONT_DIR}/Inter-Bold.ttf"))

# --- Brown palette (locked) ---
BROWN_DEEP = HexColor("#3B2A1A")     # body text, dominant
BROWN_MID = HexColor("#6B4F32")      # secondary
BROWN_WARM = HexColor("#8B6F47")     # accent, dividers
CREAM = HexColor("#F5EDDF")          # background panels
PAPER = HexColor("#FBF6EC")          # page background
USDA_GOLD = HexColor("#A87B2B")      # USDA banner
RULE_LINE = HexColor("#C9B89A")      # fill-in line color
SOFT_GRAY = HexColor("#7A6A55")
INK_BLACK = HexColor("#1F1810")

# --- Page (tabloid portrait 11x17) ---
PAGE_W, PAGE_H = 11 * inch, 17 * inch
MARGIN = 0.55 * inch


def text_w(c, txt, font, size):
    return c.stringWidth(txt, font, size)


def fill_line(c, x, y, w, label=None, label_size=7):
    """A single fill-in rule line with optional muted label below."""
    c.setStrokeColor(RULE_LINE)
    c.setLineWidth(0.7)
    c.line(x, y, x + w, y)
    if label:
        c.setFont("DMSans-Italic", label_size)
        c.setFillColor(SOFT_GRAY)
        c.drawString(x, y - 11, label)


def fill_block(c, x, y, w, lines, line_gap=22, label=None):
    """Multiple fill-in lines stacked. y is TOP of the block."""
    for i in range(lines):
        ly = y - (i + 1) * line_gap
        c.setStrokeColor(RULE_LINE)
        c.setLineWidth(0.7)
        c.line(x, ly, x + w, ly)
    if label:
        c.setFont("DMSans-Italic", 7.5)
        c.setFillColor(SOFT_GRAY)
        c.drawString(x, y - lines * line_gap - 11, label)
    return y - lines * line_gap - 16


def radio_row(c, x, y, options, label, font_size=10):
    """Draw a label then a horizontal row of empty circles + option text."""
    c.setFont("DMSans-SemiBold", font_size)
    c.setFillColor(BROWN_DEEP)
    c.drawString(x, y, label)
    label_w = text_w(c, label, "DMSans-SemiBold", font_size)
    cur_x = x + label_w + 14
    c.setFont("DMSans", font_size)
    for opt in options:
        # circle
        c.setStrokeColor(BROWN_MID)
        c.setLineWidth(0.9)
        c.circle(cur_x + 5, y + 3.5, 4.5, stroke=1, fill=0)
        c.setFillColor(BROWN_DEEP)
        c.drawString(cur_x + 14, y, opt)
        cur_x += 14 + text_w(c, opt, "DMSans", font_size) + 16


def section_header(c, x, y, w, num, title, color=BROWN_DEEP):
    c.setFillColor(color)
    c.setFont("DMSans-Bold", 11)
    c.drawString(x, y, f"{num}")
    c.setFont("DMSans-Bold", 13)
    c.drawString(x + 22, y, title.upper())
    # underline
    c.setStrokeColor(BROWN_WARM)
    c.setLineWidth(1.2)
    c.line(x, y - 6, x + w, y - 6)


def draw_page(c, site_label):
    # Background
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    y = PAGE_H - MARGIN

    # ---------- USDA BANNER (most prominent) ----------
    banner_h = 0.95 * inch
    c.setFillColor(USDA_GOLD)
    c.rect(MARGIN, y - banner_h, PAGE_W - 2 * MARGIN, banner_h, stroke=0, fill=1)
    # white text
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("DMSans-Bold", 22)
    text = "USDA-GOVERNED EDUCATIONAL EXHIBIT"
    tw = text_w(c, text, "DMSans-Bold", 22)
    c.drawString(MARGIN + (PAGE_W - 2 * MARGIN - tw) / 2, y - 36, text)
    c.setFont("DMSans", 11)
    sub = "This is not a game. Animals are teachers, not attractions."
    sw = text_w(c, sub, "DMSans", 11)
    c.drawString(MARGIN + (PAGE_W - 2 * MARGIN - sw) / 2, y - 56, sub)
    y -= banner_h + 60  # ample clearance below banner
    # site + license strip below banner
    c.setFillColor(BROWN_DEEP)
    c.setFont("DMSans-Bold", 11)
    c.drawString(MARGIN, y, f"SITE: {site_label.upper()}")
    # USDA license fill-in on right side of strip
    c.setFont("DMSans-SemiBold", 10)
    c.drawRightString(PAGE_W - MARGIN - 170, y, "USDA LICENSE #")
    fill_line(c, PAGE_W - MARGIN - 165, y - 2, 165)
    y -= 18

    # ---------- TITLE ----------
    c.setFillColor(BROWN_DEEP)
    c.setFont("DMSans-Bold", 30)
    c.drawString(MARGIN, y - 8, "Lemur Encounter")
    c.setFont("DMSans-Italic", 12)
    c.setFillColor(BROWN_MID)
    c.drawString(MARGIN, y - 28, "Approval draft — please mark up each section, then we re-render.")
    y -= 56

    # ---------- SECTION 1: WHAT THIS IS (philosophy) ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "01", "What This Encounter Is")
    y -= 22
    c.setFont("DMSans", 10.5)
    c.setFillColor(BROWN_DEEP)
    intro = ("Guests come in. Staff explain how to observe. The lemurs decide. "
             "If a lemur stations as trained and accepts a treat, you may open your hand. "
             "Two or three minutes, photos, then we rotate out. We move 10 to 200 guests "
             "through this room each day — quietly.")
    for line in simpleSplit(intro, "DMSans", 10.5, PAGE_W - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 14
    y -= 6
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y, "Edits / your wording for this section:")
    y -= 4
    y = fill_block(c, MARGIN, y, PAGE_W - 2 * MARGIN, lines=4)

    # ---------- SECTION 2: WHO MAY ENTER (with multiple choice) ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "02", "Who May Enter")
    y -= 24

    # Age 5+ with adult
    c.setFont("DMSans-SemiBold", 11)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Minimum age to enter the room:")
    radio_row(c, MARGIN + 230, y, ["4", "5", "6", "7"], "")
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y - 14, "Default per your direction: 5 years old, must be accompanied by an adult.")
    y -= 32

    c.setFont("DMSans-SemiBold", 11)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Minimum age to enter without an adult:")
    radio_row(c, MARGIN + 260, y, ["10", "12", "14", "16"], "")
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y - 14, "Default per your direction: 12.")
    y -= 32

    c.setFont("DMSans-SemiBold", 11)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Under 5: cannot enter — instead, see the field-trip program in section 06.")
    y -= 22

    # ---------- SECTION 3: HOW WE OBSERVE ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "03", "How We Observe")
    y -= 22
    c.setFont("DMSans", 10.5)
    c.setFillColor(BROWN_DEEP)
    obs = ("One sense at a time. Eyes, then ears, then — only if a lemur offers — hands. "
           "We do not stack random facts on top of an experience. Staff stay quiet so guests can "
           "actually feel what is happening.")
    for line in simpleSplit(obs, "DMSans", 10.5, PAGE_W - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 14
    y -= 4
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y, "Your edits:")
    y -= 4
    y = fill_block(c, MARGIN, y, PAGE_W - 2 * MARGIN, lines=3)

    # ---------- SECTION 4: HOW WE ANSWER QUESTIONS ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "04", "How Staff Answer Questions")
    y -= 22
    c.setFont("DMSans", 10.5)
    c.setFillColor(BROWN_DEEP)
    qa = ("We reroute every question with another question. A guest asks "
          "\u201cwhere are they from?\u201d — staff answer \u201cwhere do you think they\u2019re from?\u201d "
          "Then we wait. The point is the guest\u2019s own observation, not our recital.")
    for line in simpleSplit(qa, "DMSans", 10.5, PAGE_W - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 14
    y -= 4
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y, "Your edits / additional examples:")
    y -= 4
    y = fill_block(c, MARGIN, y, PAGE_W - 2 * MARGIN, lines=3)

    # ---------- SECTION 5: GROUP SIZE & ROTATION ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "05", "Group Size and Rotation")
    y -= 26

    c.setFont("DMSans-SemiBold", 11)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Guests per rotation:")
    radio_row(c, MARGIN + 165, y, ["4", "5", "6", "7"], "")
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y - 14, "Default: 5\u20136. Encounter ends 2\u20133 minutes after photos. Then rotate.")
    y -= 32

    c.setFont("DMSans-SemiBold", 11)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Daily volume range:")
    c.setFont("DMSans", 11)
    c.drawString(MARGIN + 160, y, "from")
    fill_line(c, MARGIN + 200, y - 2, 60)
    c.drawString(MARGIN + 270, y, "to")
    fill_line(c, MARGIN + 295, y - 2, 60)
    c.drawString(MARGIN + 360, y, "guests / day")
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y - 14, "Default per your direction: 10 to 200.")
    y -= 56

    # ---------- SECTION 6: UNDER-5 / FIELD TRIP PROGRAM ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "06", "Under 5 — Harness / Field-Trip Program")
    y -= 22
    c.setFont("DMSans", 10.5)
    c.setFillColor(BROWN_DEEP)
    ft = ("Children under 5 cannot enter the encounter room, but they are not excluded from "
          "the experience. We harness a lemur and bring them out. The handler holds the lemur "
          "in their lap; the lemur may bounce on the ground. Guests observe at the handler\u2019s "
          "pace. Touching is rare and only if the handler invites it.")
    for line in simpleSplit(ft, "DMSans", 10.5, PAGE_W - 2 * MARGIN):
        c.drawString(MARGIN, y, line)
        y -= 14
    y -= 4
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y, "Your edits / what to call this program / when it runs:")
    y -= 4
    y = fill_block(c, MARGIN, y, PAGE_W - 2 * MARGIN, lines=3)

    # ---------- SECTION 7: PRICING (fill-in) ----------
    section_header(c, MARGIN, y, PAGE_W - 2 * MARGIN, "07", "Encounter Fee")
    y -= 26
    c.setFont("DMSans-SemiBold", 12)
    c.setFillColor(BROWN_DEEP)
    c.drawString(MARGIN, y, "Per-guest fee:  $")
    fill_line(c, MARGIN + 130, y - 2, 90)
    c.drawString(MARGIN + 240, y, "Gratuity at exit:")
    radio_row(c, MARGIN + 360, y, ["15%", "20%", "25%"], "")
    c.setFont("DMSans-Italic", 9)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, y - 14, "Pay at the door. Gratuity prompted at exit (handled by payment processor).")
    y -= 30

    # ---------- FOOTER ----------
    c.setFillColor(BROWN_WARM)
    c.setLineWidth(0.6)
    c.setStrokeColor(BROWN_WARM)
    c.line(MARGIN, MARGIN + 30, PAGE_W - MARGIN, MARGIN + 30)
    c.setFillColor(BROWN_DEEP)
    c.setFont("DMSans-Italic", 9.5)
    foot = "What a living thing can sense becomes its reality. Environment shapes design."
    fw = text_w(c, foot, "DMSans-Italic", 9.5)
    c.drawString(MARGIN + (PAGE_W - 2 * MARGIN - fw) / 2, MARGIN + 14, foot)
    c.setFont("DMSans", 8)
    c.setFillColor(SOFT_GRAY)
    c.drawString(MARGIN, MARGIN, "v2026-04-25k  \u00b7  Door Sign \u2014 Questionnaire / Approval Draft")
    c.drawRightString(PAGE_W - MARGIN, MARGIN, f"{site_label}")


def build(site_label: str, out_path: Path):
    c = canvas.Canvas(str(out_path), pagesize=(PAGE_W, PAGE_H))
    c.setTitle(f"Lemur Encounter Door Sign — {site_label} — v2026-04-25k")
    c.setAuthor("Perplexity Computer")
    draw_page(c, site_label)
    c.showPage()
    c.save()
    print(f"wrote {out_path}")


if __name__ == "__main__":
    out = Path("/tmp/LIFE-push/releases/v2026-04-25k/door_sign_questionnaire")
    out.mkdir(parents=True, exist_ok=True)
    build("Houston Interactive Aquarium & Animal Preserve",
          out / "Lemur_Encounter_Door_Sign_Questionnaire_HOU_v2026-04-25k.pdf")
    build("San Antonio Aquarium",
          out / "Lemur_Encounter_Door_Sign_Questionnaire_SA_v2026-04-25k.pdf")
