"""
Court Utilization Outreach PDF
2-page professional flyer for pickleball court partnership opportunities.
Brand: Navy #2C3481 headers, Teal #00AAAD accents, white background
"""

import urllib.request
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

def dl_font(name, url):
    p = FONT_DIR / name
    if not p.exists():
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, p)
    return str(p)

# DM Sans (headings) + Inter (body)
dm_bold = dl_font("DMSans-Bold.ttf",
    "https://github.com/google/fonts/raw/main/ofl/dmsans/static/DMSans-Bold.ttf")
dm_semi = dl_font("DMSans-SemiBold.ttf",
    "https://github.com/google/fonts/raw/main/ofl/dmsans/static/DMSans-SemiBold.ttf")
dm_reg  = dl_font("DMSans-Regular.ttf",
    "https://github.com/google/fonts/raw/main/ofl/dmsans/static/DMSans-Regular.ttf")
dm_med  = dl_font("DMSans-Medium.ttf",
    "https://github.com/google/fonts/raw/main/ofl/dmsans/static/DMSans-Medium.ttf")

pdfmetrics.registerFont(TTFont("DMSans-Bold",     dm_bold))
pdfmetrics.registerFont(TTFont("DMSans-SemiBold", dm_semi))
pdfmetrics.registerFont(TTFont("DMSans",          dm_reg))
pdfmetrics.registerFont(TTFont("DMSans-Medium",   dm_med))

# ── Colors ────────────────────────────────────────────────────────────────────
NAVY     = HexColor("#2C3481")
TEAL     = HexColor("#00AAAD")
TEAL_LT  = HexColor("#E6F7F7")
NAVY_LT  = HexColor("#ECEEF7")
DARK     = HexColor("#1A1A2E")
MID      = HexColor("#4A4A6A")
LIGHT    = HexColor("#F5F6FA")
WHITE    = white
BORDER   = HexColor("#D0D4E8")

W, H = letter  # 612 × 792 pt
MARGIN = 48

# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_rounded_rect(c, x, y, w, h, r=6, fill=None, stroke=None, stroke_width=0.5):
    """Draw a filled (and optionally stroked) rounded rectangle."""
    if fill:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(stroke_width)
    else:
        c.setStrokeColor(HexColor("#00000000"))
        c.setLineWidth(0)
    p = c.beginPath()
    p.roundRect(x, y, w, h, r)
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if stroke else 0)


def text(c, txt, x, y, font="DMSans", size=10, color=DARK, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, txt)
    elif align == "right":
        c.drawRightString(x, y, txt)
    else:
        c.drawString(x, y, txt)


def wrap_text(c, txt, x, y, max_width, font="DMSans", size=10, color=DARK, leading=14):
    """Simple word-wrap for canvas text. Returns final y position."""
    c.setFont(font, size)
    c.setFillColor(color)
    words = txt.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def divider(c, y, x0=MARGIN, x1=None, color=BORDER, width=0.5):
    x1 = x1 or (W - MARGIN)
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x0, y, x1, y)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1
# ══════════════════════════════════════════════════════════════════════════════

def draw_page1(c):
    # ── Full-bleed navy header bar ───────────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, H - 130, W, 130, fill=1, stroke=0)

    # Teal accent stripe on top
    c.setFillColor(TEAL)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)

    # Header text
    text(c, "COURT & EVENT SPACE", MARGIN, H - 42, "DMSans-Bold", 9,
         TEAL, "left")
    text(c, "Partnership Opportunities", MARGIN, H - 68, "DMSans-Bold", 26,
         WHITE, "left")
    text(c, "Fill your courts. Grow your revenue. Build lasting community partnerships.",
         MARGIN, H - 92, "DMSans", 10.5, HexColor("#B8BEDD"), "left")

    # Small logo area (top-right corner of header)
    draw_rounded_rect(c, W - MARGIN - 80, H - 108, 80, 34, r=4, fill=TEAL)
    text(c, "PICKLEBALL", W - MARGIN - 40, H - 90, "DMSans-Bold", 8, WHITE, "center")
    text(c, "COURTS", W - MARGIN - 40, H - 100, "DMSans-Bold", 7, WHITE, "center")

    # ── Key Stats Row ────────────────────────────────────────────────────────
    stats_y = H - 175
    stats = [
        ("4", "Pickleball Courts"),
        ("600+", "Parking Spaces"),
        ("300K", "Annual Visitors"),
        ("Food & Bev", "On-Site"),
    ]
    card_w = (W - 2 * MARGIN - 15) / 4
    for i, (val, label) in enumerate(stats):
        cx = MARGIN + i * (card_w + 5)
        draw_rounded_rect(c, cx, stats_y - 52, card_w, 58, r=6, fill=NAVY_LT)
        c.setFillColor(TEAL)
        c.rect(cx, stats_y + 5, card_w, 2, fill=1, stroke=0)
        text(c, val, cx + card_w/2, stats_y - 16, "DMSans-Bold", 20, NAVY, "center")
        text(c, label, cx + card_w/2, stats_y - 34, "DMSans", 8, MID, "center")

    # ── Section: Availability Grid ───────────────────────────────────────────
    sec_y = stats_y - 80
    text(c, "COURT AVAILABILITY — TIME BLOCKS", MARGIN, sec_y, "DMSans-Bold", 8.5, TEAL)
    c.setFillColor(TEAL)
    c.rect(MARGIN, sec_y + 11, 36, 2, fill=1, stroke=0)

    grid_top = sec_y - 14
    col_labels = ["Time Block", "Weekdays", "Saturdays", "Sundays"]
    rows = [
        ("Morning\n6AM–11AM",  "Schools / Camps / Youth", "Open", "Open"),
        ("Afternoon\n11AM–5PM","Training / Fitness / Lessons", "Tournaments", "Special Events"),
        ("Evening\n5PM–10PM", "Leagues / Social Sports", "Leagues", "Corporate / Private"),
        ("Full Day",          "Event Packages", "Tournament Hosting", "Tournament Hosting"),
    ]

    col_w = [(W - 2*MARGIN) * p for p in [0.24, 0.26, 0.25, 0.25]]
    col_x = [MARGIN]
    for cw in col_w[:-1]:
        col_x.append(col_x[-1] + cw)

    row_h = 38
    # Header row
    for j, lbl in enumerate(col_labels):
        bg = NAVY if j == 0 else NAVY
        c.setFillColor(bg)
        c.rect(col_x[j], grid_top - 20, col_w[j], 22, fill=1, stroke=0)
        text(c, lbl, col_x[j] + col_w[j]/2, grid_top - 13, "DMSans-Bold", 8, WHITE, "center")

    for i, (time_lbl, *cells) in enumerate(rows):
        row_y = grid_top - 20 - (i + 1) * row_h
        for j in range(4):
            bg = NAVY_LT if j == 0 else (TEAL_LT if i % 2 == 0 else WHITE)
            draw_rounded_rect(c, col_x[j], row_y, col_w[j], row_h - 2, r=0,
                              fill=bg, stroke=BORDER, stroke_width=0.3)
            if j == 0:
                parts = time_lbl.split("\n")
                text(c, parts[0], col_x[j] + 8, row_y + row_h - 14, "DMSans-Bold", 8.5, NAVY)
                if len(parts) > 1:
                    text(c, parts[1], col_x[j] + 8, row_y + row_h - 25, "DMSans", 7.5, MID)
            else:
                cell_txt = cells[j-1]
                tw = c.stringWidth(cell_txt, "DMSans", 8)
                fx = col_x[j] + col_w[j]/2
                fy = row_y + row_h/2 - 4
                text(c, cell_txt, fx, fy, "DMSans", 8, DARK, "center")

    grid_bottom = grid_top - 20 - len(rows) * row_h

    # ── Section: Partner Types ────────────────────────────────────────────────
    pts_y = grid_bottom - 26
    text(c, "WHO WE'RE LOOKING FOR", MARGIN, pts_y, "DMSans-Bold", 8.5, TEAL)
    c.setFillColor(TEAL)
    c.rect(MARGIN, pts_y + 11, 36, 2, fill=1, stroke=0)

    partners = [
        ("Pickleball\nLeagues",    "PB"),
        ("Corporate\nGroups",      "CORP"),
        ("Schools &\nCamps",       "SCH"),
        ("Fitness\nOperators",     "FIT"),
        ("Tournament\nOrganizers", "TOUR"),
    ]
    p_top = pts_y - 16
    pw = (W - 2*MARGIN - 20) / 5
    for i, (lbl, icon) in enumerate(partners):
        px = MARGIN + i * (pw + 5)
        draw_rounded_rect(c, px, p_top - 54, pw, 58, r=6, fill=LIGHT,
                          stroke=BORDER, stroke_width=0.5)
        # Teal top accent
        c.setFillColor(TEAL)
        c.rect(px, p_top + 3, pw, 3, fill=1, stroke=0)
        # Icon circle
        c.setFillColor(NAVY)
        c.circle(px + pw/2, p_top - 12, 13, fill=1, stroke=0)
        text(c, icon, px + pw/2, p_top - 16, "DMSans-Bold", 6.5, WHITE, "center")
        lines = lbl.split("\n")
        text(c, lines[0], px + pw/2, p_top - 32, "DMSans-Bold", 8, NAVY, "center")
        if len(lines) > 1:
            text(c, lines[1], px + pw/2, p_top - 43, "DMSans-Bold", 8, NAVY, "center")

    partner_bottom = p_top - 54

    # ── Section: Venue Advantages ─────────────────────────────────────────────
    adv_y = partner_bottom - 26
    text(c, "VENUE ADVANTAGES", MARGIN, adv_y, "DMSans-Bold", 8.5, TEAL)
    c.setFillColor(TEAL)
    c.rect(MARGIN, adv_y + 11, 36, 2, fill=1, stroke=0)

    advantages = [
        ("P", "600+ Parking Spaces", "Free, on-site — no competition for spots"),
        ("F", "Food & Beverage On-Site", "Restaurant & concessions available"),
        ("E", "Entertainment Campus", "Zoo/Aquarium, Studio Giraffe venue"),
        ("V", "300K Annual Visitors", "High visibility, built-in foot traffic"),
    ]

    adv_top = adv_y - 16
    adv_col_w = (W - 2*MARGIN - 12) / 2
    for i, (icon_lbl, title, sub) in enumerate(advantages):
        col = i % 2
        row = i // 2
        ax = MARGIN + col * (adv_col_w + 12)
        ay = adv_top - row * 44
        # Icon circle
        c.setFillColor(TEAL)
        c.circle(ax + 14, ay - 12, 12, fill=1, stroke=0)
        text(c, icon_lbl, ax + 14, ay - 16, "DMSans-Bold", 9, WHITE, "center")
        text(c, title, ax + 34, ay - 8, "DMSans-Bold", 9, NAVY)
        text(c, sub,   ax + 34, ay - 20, "DMSans", 8, MID)

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = 28
    c.setFillColor(NAVY)
    c.rect(0, 0, W, footer_y + 6, fill=1, stroke=0)
    text(c, "Turn idle courts into revenue. Build community. Create lasting partnerships.",
         W/2, footer_y - 6, "DMSans", 8.5, HexColor("#B8BEDD"), "center")
    text(c, "1 of 2", W - MARGIN, footer_y - 6, "DMSans", 7.5, HexColor("#6B7099"), "right")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════════════════════════

def draw_page2(c):
    # ── Header ────────────────────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, H - 110, W, 110, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, H - 6, W, 6, fill=1, stroke=0)

    text(c, "PARTNERSHIP MODELS", MARGIN, H - 42, "DMSans-Bold", 9, TEAL)
    text(c, "Flexible Structures for Every Operator", MARGIN, H - 66,
         "DMSans-Bold", 24, WHITE)
    text(c, "Choose the model that works for your organization — or combine them.",
         MARGIN, H - 88, "DMSans", 10, HexColor("#B8BEDD"))

    # ── Partnership Model Cards ───────────────────────────────────────────────
    models = [
        {
            "tag": "HOURLY RENTAL",
            "title": "$__  / hour per court",
            "desc": ("Flexible drop-in or scheduled bookings by the hour. "
                     "Ideal for training sessions, private lessons, or one-off "
                     "events. No long-term commitment required."),
            "bullets": [
                "Single court or multi-court bookings",
                "Advance online booking portal",
                "Minimum 1-hour block",
            ],
            "best": "Private coaches • One-off events • Casual groups",
        },
        {
            "tag": "BLOCK BOOKING",
            "title": "Discounted rate — recurring time slots",
            "desc": ("Reserve a consistent weekly or monthly time block at a "
                     "reduced rate. Lock in your schedule and save. Perfect for "
                     "leagues, schools, and fitness operators with regular programs."),
            "bullets": [
                "Weekly or monthly recurring blocks",
                "Priority scheduling & guaranteed courts",
                "10–20% discount vs. hourly rate",
            ],
            "best": "School programs • Fitness operators • Fitness clubs",
        },
        {
            "tag": "REVENUE SHARE",
            "title": "Partner earns % of paid programming",
            "desc": ("Run your own paid classes, leagues, or clinics on our courts. "
                     "We provide the space and amenities; you bring the participants "
                     "and programming expertise. Revenue split negotiated per agreement."),
            "bullets": [
                "Operator retains majority of program revenue",
                "Venue provides courts, parking & facilities",
                "Co-marketing opportunities available",
            ],
            "best": "League operators • Fitness instructors • Program directors",
        },
        {
            "tag": "TOURNAMENT HOSTING",
            "title": "Full-day & multi-day packages",
            "desc": ("Host your tournament on 4 dedicated pickleball courts with "
                     "600+ parking spaces, on-site food & beverage, and the excitement "
                     "of our entertainment campus as a backdrop."),
            "bullets": [
                "All 4 courts available for full-day events",
                "On-site food & beverage for players/spectators",
                "Studio Giraffe venue available for awards/banquets",
            ],
            "best": "Tournament directors • Sports associations • Corporate events",
        },
    ]

    card_top = H - 128
    cw = (W - 2 * MARGIN - 12) / 2
    ch = 152

    for i, m in enumerate(models):
        col = i % 2
        row = i // 2
        cx = MARGIN + col * (cw + 12)
        cy = card_top - row * (ch + 8) - ch

        draw_rounded_rect(c, cx, cy, cw, ch, r=8, fill=LIGHT,
                          stroke=BORDER, stroke_width=0.5)
        # Left teal accent bar
        c.setFillColor(TEAL)
        c.rect(cx, cy, 4, ch, fill=1, stroke=0)

        # Tag pill
        tag_w = c.stringWidth(m["tag"], "DMSans-Bold", 7) + 14
        draw_rounded_rect(c, cx + 14, cy + ch - 20, tag_w, 14, r=4, fill=TEAL)
        text(c, m["tag"], cx + 14 + tag_w/2, cy + ch - 14,
             "DMSans-Bold", 7, WHITE, "center")

        # Title
        text(c, m["title"], cx + 14, cy + ch - 34, "DMSans-Bold", 10, NAVY)

        # Desc (wrapped)
        desc_y = cy + ch - 48
        desc_words = m["desc"].split()
        line = ""
        max_w = cw - 28
        for word in desc_words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "DMSans", 7.5) <= max_w:
                line = test
            else:
                text(c, line, cx + 14, desc_y, "DMSans", 7.5, MID)
                desc_y -= 11
                line = word
        if line:
            text(c, line, cx + 14, desc_y, "DMSans", 7.5, MID)
            desc_y -= 11

        # Bullets
        desc_y -= 3
        for bullet in m["bullets"]:
            c.setFillColor(TEAL)
            c.circle(cx + 20, desc_y + 3, 2.5, fill=1, stroke=0)
            text(c, bullet, cx + 28, desc_y, "DMSans", 7.5, DARK)
            desc_y -= 11

        # "Best for" row
        desc_y -= 3
        text(c, "Best for: ", cx + 14, desc_y, "DMSans-Bold", 7, NAVY)
        bfw = c.stringWidth("Best for: ", "DMSans-Bold", 7)
        text(c, m["best"], cx + 14 + bfw, desc_y, "DMSans", 7, MID)

    bottom_of_cards = card_top - 2 * (ch + 8) - ch

    # ── Next Steps ────────────────────────────────────────────────────────────
    ns_y = bottom_of_cards - 14
    text(c, "NEXT STEPS", MARGIN, ns_y, "DMSans-Bold", 8.5, TEAL)
    c.setFillColor(TEAL)
    c.rect(MARGIN, ns_y + 11, 36, 2, fill=1, stroke=0)

    steps = [
        ("1", "Reach out", "Contact us to discuss your program or event needs."),
        ("2", "Site Visit", "Schedule a court walkthrough and venue tour."),
        ("3", "Propose", "We'll put together a custom partnership proposal."),
        ("4", "Launch", "Execute the agreement and start building your program."),
    ]

    step_top = ns_y - 14
    sw = (W - 2*MARGIN - 18) / 4
    for i, (num, title, desc) in enumerate(steps):
        sx = MARGIN + i * (sw + 6)
        draw_rounded_rect(c, sx, step_top - 52, sw, 56, r=6, fill=LIGHT,
                          stroke=BORDER, stroke_width=0.5)
        # Number circle
        c.setFillColor(NAVY)
        c.circle(sx + sw/2, step_top - 6, 11, fill=1, stroke=0)
        text(c, num, sx + sw/2, step_top - 10, "DMSans-Bold", 9, WHITE, "center")
        text(c, title, sx + sw/2, step_top - 25, "DMSans-Bold", 8, NAVY, "center")
        # desc wrapped
        desc_words = desc.split()
        line = ""
        dy = step_top - 36
        for word in desc_words:
            test = (line + " " + word).strip()
            if c.stringWidth(test, "DMSans", 7) <= sw - 8:
                line = test
            else:
                text(c, line, sx + sw/2, dy, "DMSans", 7, MID, "center")
                dy -= 10
                line = word
        if line:
            text(c, line, sx + sw/2, dy, "DMSans", 7, MID, "center")

    steps_bottom = step_top - 52

    # ── Contact CTA Banner ────────────────────────────────────────────────────
    cta_y = steps_bottom - 14
    draw_rounded_rect(c, MARGIN, cta_y - 56, W - 2*MARGIN, 60, r=8, fill=NAVY)
    c.setFillColor(TEAL)
    c.rect(MARGIN, cta_y - 56, 6, 60, fill=1, stroke=0)

    text(c, "LET'S TALK", MARGIN + 22, cta_y - 10,
         "DMSans-Bold", 11, TEAL)
    text(c, "Ready to fill your calendar and grow your community?",
         MARGIN + 22, cta_y - 26, "DMSans", 9, WHITE)

    # Contact placeholders
    text(c, "[Contact Name]  |  [Email Address]  |  [Phone Number]",
         MARGIN + 22, cta_y - 42, "DMSans-Bold", 9.5, HexColor("#B8BEDD"))

    # ── Footer ────────────────────────────────────────────────────────────────
    footer_y = 28
    c.setFillColor(NAVY)
    c.rect(0, 0, W, footer_y + 6, fill=1, stroke=0)
    text(c, "All rates and terms subject to availability. Contact us for a custom proposal.",
         W/2, footer_y - 6, "DMSans", 8, HexColor("#6B7099"), "center")
    text(c, "2 of 2", W - MARGIN, footer_y - 6, "DMSans", 7.5, HexColor("#6B7099"), "right")


# ── Build PDF ─────────────────────────────────────────────────────────────────
OUT = "/home/user/workspace/LIFE_system/print_ready/COURT_UTILIZATION_OUTREACH.pdf"

c = canvas.Canvas(OUT, pagesize=letter)
c.setTitle("Court Utilization — Partnership Opportunities")
c.setAuthor("Perplexity Computer")

draw_page1(c)
c.showPage()
draw_page2(c)
c.save()

print(f"PDF saved → {OUT}")
