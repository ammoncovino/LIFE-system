#!/usr/bin/env python3
"""
Studio Giraffe — 12-Month Event Calendar PDF
May 2026 – April 2027
Uses ReportLab Canvas API, landscape letter pages.
"""

import calendar
import urllib.request
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

FONTS = {
    "WorkSans-Regular": "https://github.com/google/fonts/raw/main/ofl/worksans/WorkSans%5Bwght%5D.ttf",
    "DMSans-Regular":   "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
}

def download_font(name, url):
    path = FONT_DIR / f"{name}.ttf"
    if not path.exists():
        print(f"  Downloading {name}…")
        urllib.request.urlretrieve(url, path)
    return str(path)

try:
    ws_path  = download_font("WorkSans", FONTS["WorkSans-Regular"])
    dms_path = download_font("DMSans",   FONTS["DMSans-Regular"])
    pdfmetrics.registerFont(TTFont("WorkSans", ws_path))
    pdfmetrics.registerFont(TTFont("DMSans",   dms_path))
    FONT_HEADING = "WorkSans"
    FONT_BODY    = "DMSans"
    print("  Custom fonts loaded.")
except Exception as e:
    print(f"  Font download failed ({e}), falling back to Helvetica.")
    FONT_HEADING = "Helvetica-Bold"
    FONT_BODY    = "Helvetica"

# ── Brand colours ─────────────────────────────────────────────────────────────
COL_BG        = HexColor("#F7F6F2")      # warm off-white
COL_DARK      = HexColor("#1C1B19")      # near-black
COL_MED       = HexColor("#7A7974")      # muted text
COL_BORDER    = HexColor("#D4D1CA")      # grid lines
COL_ACCENT    = HexColor("#01696F")      # primary teal

# Event category colours
EC = {
    "Music Night":      {"bg": HexColor("#00AAAD"), "text": white},
    "Comedy Night":     {"bg": HexColor("#EE773D"), "text": white},
    "Themed Event":     {"bg": HexColor("#CB3C56"), "text": white},
    "Vendor Weekend":   {"bg": HexColor("#F9EE6D"), "text": HexColor("#1C1B19")},
    "Flex Date":        {"bg": HexColor("#CAE8E4"), "text": HexColor("#1C1B19")},
    "Broadcast Event":  {"bg": HexColor("#422616"), "text": white},
}

# ── Page setup ────────────────────────────────────────────────────────────────
PAGE_LS  = landscape(letter)        # 792 × 612
PAGE_PT  = letter                   # 612 × 792  (cover)
OUT_PATH = "/home/user/workspace/LIFE_system/print_ready/STUDIO_GIRAFFE_12MO_CALENDAR.pdf"

# ── Month data  (May 2026 – April 2027) ──────────────────────────────────────
MONTHS = [
    {
        "year": 2026, "month": 5, "name": "May 2026",
        "events": [
            ("5",  "Music Night",     "Cumbia & Latin Night"),
            ("9",  "Broadcast Event", "UFC / Boxing Broadcast"),
            ("16", "Themed Event",    "Cinco de Mayo Cultural Night"),
            ("23", "Comedy Night",    "Spring Comedy Showcase"),
            ("24", "Vendor Weekend",  "Memorial Day Vendor Fair"),
            ("25", "Vendor Weekend",  "Memorial Day Vendor Fair"),
            ("30", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "Cinco de Mayo promo push. Joe Hand broadcast TBD. Narration suites open.",
    },
    {
        "year": 2026, "month": 6, "name": "June 2026",
        "events": [
            ("6",  "Music Night",     "Summer Kickoff Concert"),
            ("13", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("20", "Themed Event",    "Pride Night Celebration"),
            ("21", "Vendor Weekend",  "Summer Solstice Market"),
            ("22", "Vendor Weekend",  "Summer Solstice Market"),
            ("27", "Comedy Night",    "Stand-Up Saturday"),
            ("30", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "Pride Night partnership outreach. Summer concert sponsorship package.",
    },
    {
        "year": 2026, "month": 7, "name": "July 2026",
        "events": [
            ("3",  "Themed Event",    "July 4th Pre-Party Spectacular"),
            ("4",  "Themed Event",    "Independence Day Celebration"),
            ("11", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("18", "Music Night",     "Summer Heat EDM Night"),
            ("25", "Comedy Night",    "Summer Comedy Series"),
            ("26", "Vendor Weekend",  "Mid-Summer Makers Market"),
            ("27", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "July 4th requires early city permit. Food truck coordination needed.",
    },
    {
        "year": 2026, "month": 8, "name": "August 2026",
        "events": [
            ("1",  "Vendor Weekend",  "Back to School Fair"),
            ("2",  "Vendor Weekend",  "Back to School Fair"),
            ("8",  "Broadcast Event", "UFC / Boxing Broadcast"),
            ("15", "Music Night",     "EDM Night — Bass Edition"),
            ("22", "Themed Event",    "Back to School Bash"),
            ("29", "Comedy Night",    "Late Summer Laughs"),
            ("31", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "Back-to-school promo with area schools/colleges. EDM talent TBD.",
    },
    {
        "year": 2026, "month": 9, "name": "September 2026",
        "events": [
            ("5",  "Vendor Weekend",  "Labor Day Vendor Fair"),
            ("6",  "Vendor Weekend",  "Labor Day Vendor Fair"),
            ("12", "Music Night",     "Hispanic Heritage Kickoff Concert"),
            ("19", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("26", "Themed Event",    "Hispanic Heritage Cultural Night"),
            ("27", "Comedy Night",    "Fall Comedy Showcase"),
            ("30", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "Hispanic Heritage Month (Sept 15 – Oct 15). Community org partnership.",
    },
    {
        "year": 2026, "month": 10, "name": "October 2026",
        "events": [
            ("3",  "Vendor Weekend",  "Oktoberfest Market"),
            ("4",  "Vendor Weekend",  "Oktoberfest Market"),
            ("10", "Themed Event",    "Oktoberfest Celebration"),
            ("17", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("24", "Music Night",     "Halloween Haunted Concert"),
            ("25", "Themed Event",    "Halloween Spectacular"),
            ("31", "Comedy Night",    "Halloween Comedy Fright Night"),
        ],
        "notes": "Two themed events this month — budget accordingly. Costume contest optional.",
    },
    {
        "year": 2026, "month": 11, "name": "November 2026",
        "events": [
            ("1",  "Themed Event",    "Día de los Muertos Night"),
            ("7",  "Comedy Night",    "Fall Comedy Special"),
            ("14", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("21", "Vendor Weekend",  "Thanksgiving Vendor Market"),
            ("22", "Vendor Weekend",  "Thanksgiving Vendor Market"),
            ("28", "Music Night",     "Holiday Season Opener Concert"),
            ("30", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "DdlM event on or near Nov 1. Holiday décor transition mid-month.",
    },
    {
        "year": 2026, "month": 12, "name": "December 2026",
        "events": [
            ("5",  "Vendor Weekend",  "Holiday Artisan Market"),
            ("6",  "Vendor Weekend",  "Holiday Artisan Market"),
            ("12", "Themed Event",    "Holiday Spectacular"),
            ("19", "Music Night",     "Winter Concert"),
            ("26", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("31", "Themed Event",    "NYE Countdown Gala"),
            ("20", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "NYE Gala — premium ticket tier, narration suites at full capacity.",
    },
    {
        "year": 2027, "month": 1, "name": "January 2027",
        "events": [
            ("2",  "Comedy Night",    "New Year Recovery Comedy Night"),
            ("9",  "Vendor Weekend",  "Winter Vendor Market"),
            ("10", "Vendor Weekend",  "Winter Vendor Market"),
            ("16", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("23", "Music Night",     "Winter Beats Concert"),
            ("30", "Themed Event",    "Winter Wonderland Night"),
            ("31", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "Post-holiday push. January is traditionally slow — vendor market drives foot traffic.",
    },
    {
        "year": 2027, "month": 2, "name": "February 2027",
        "events": [
            ("6",  "Music Night",     "Valentine's Date Night Concert"),
            ("13", "Vendor Weekend",  "Valentine's Artisan Market"),
            ("14", "Themed Event",    "Valentine's Day Special"),
            ("20", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("21", "Comedy Night",    "Comedy Valentine's Special"),
            ("27", "Flex Date",       "Open / Private Event"),
            ("28", "Vendor Weekend",  "Late February Makers Market"),
        ],
        "notes": "Valentine's double event (14th + 13th market). Strong narration suite demand.",
    },
    {
        "year": 2027, "month": 3, "name": "March 2027",
        "events": [
            ("6",  "Vendor Weekend",  "Spring Kickoff Market"),
            ("7",  "Vendor Weekend",  "Spring Kickoff Market"),
            ("13", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("14", "Music Night",     "SXSW Spillover Concert"),
            ("20", "Themed Event",    "Spring Equinox Night"),
            ("21", "Music Night",     "Spring Break Concert"),
            ("28", "Comedy Night",    "Spring Comedy Showcase"),
        ],
        "notes": "SXSW spillover — target Austin touring acts. Spring Break week drives younger demos.",
    },
    {
        "year": 2027, "month": 4, "name": "April 2027",
        "events": [
            ("3",  "Vendor Weekend",  "Easter Vendor Fair"),
            ("4",  "Vendor Weekend",  "Easter Vendor Fair"),
            ("10", "Broadcast Event", "UFC / Boxing Broadcast"),
            ("17", "Music Night",     "Spring Concert"),
            ("24", "Comedy Night",    "Anniversary Comedy Special"),
            ("25", "Themed Event",    "Anniversary Celebration Gala"),
            ("30", "Flex Date",       "Open / Private Event"),
        ],
        "notes": "1-year anniversary celebration. Recap deck for investors/sponsors.",
    },
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def hex_to_rgb01(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def set_fill(c, col):
    if hasattr(col, 'red'):
        c.setFillColorRGB(col.red, col.green, col.blue)
    else:
        c.setFillColor(col)

def set_stroke(c, col):
    if hasattr(col, 'red'):
        c.setStrokeColorRGB(col.red, col.green, col.blue)
    else:
        c.setStrokeColor(col)

def draw_rect_filled(c, x, y, w, h, fill_col, stroke_col=None, radius=3):
    set_fill(c, fill_col)
    if stroke_col:
        set_stroke(c, stroke_col)
        c.setLineWidth(0.5)
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.setLineWidth(0)
        c.roundRect(x, y, w, h, radius, stroke=0, fill=1)

def centered_text(c, text, x, y, font, size, col):
    c.setFont(font, size)
    set_fill(c, col)
    c.drawCentredString(x, y, text)

def left_text(c, text, x, y, font, size, col):
    c.setFont(font, size)
    set_fill(c, col)
    c.drawString(x, y, text)

def right_text(c, text, x, y, font, size, col):
    c.setFont(font, size)
    set_fill(c, col)
    c.drawRightString(x, y, text)

# ── COVER PAGE (portrait) ─────────────────────────────────────────────────────

def draw_cover(cv):
    pw, ph = PAGE_PT
    # Background
    cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
    cv.rect(0, 0, pw, ph, fill=1, stroke=0)

    # Decorative top band — teal
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.rect(0, ph - 12, pw, 12, fill=1, stroke=0)

    # Bottom band
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.rect(0, 0, pw, 8, fill=1, stroke=0)

    # Colour swatches — horizontal bar mid-cover
    swatch_y = ph * 0.52
    swatch_h = 6
    swatch_w = pw / len(EC)
    for i, (label, cols) in enumerate(EC.items()):
        cv.setFillColor(cols["bg"])
        cv.rect(i * swatch_w, swatch_y, swatch_w, swatch_h, fill=1, stroke=0)

    # Venue name
    cv.setFont(FONT_HEADING, 38)
    cv.setFillColorRGB(*hex_to_rgb01("#00AAAD"))
    cv.drawCentredString(pw / 2, ph * 0.62, "STUDIO GIRAFFE")

    # Title
    cv.setFont(FONT_BODY, 16)
    cv.setFillColorRGB(*hex_to_rgb01("#CDCCCA"))
    cv.drawCentredString(pw / 2, ph * 0.55, "12-Month Event Calendar")

    # Date range
    cv.setFont(FONT_BODY, 13)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawCentredString(pw / 2, ph * 0.49, "May 2026 – April 2027")

    # Tagline
    cv.setFont(FONT_BODY, 10)
    cv.setFillColorRGB(*hex_to_rgb01("#5A5957"))
    cv.drawCentredString(pw / 2, ph * 0.44, "An elevated entertainment experience at the heart of your zoo & aquarium park")

    # Legend block
    legend_x = 60
    legend_y = ph * 0.32
    cv.setFont(FONT_HEADING, 9)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(legend_x, legend_y + 14, "EVENT CATEGORIES")
    for i, (label, cols) in enumerate(EC.items()):
        row = i // 2
        col = i % 2
        bx = legend_x + col * 240
        by = legend_y - row * 20
        # colour swatch
        cv.setFillColor(cols["bg"])
        cv.roundRect(bx, by - 2, 12, 12, 2, fill=1, stroke=0)
        # label
        cv.setFont(FONT_BODY, 9)
        cv.setFillColorRGB(*hex_to_rgb01("#CDCCCA"))
        cv.drawString(bx + 18, by, label)

    # Revenue note
    cv.setFont(FONT_BODY, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#5A5957"))
    cv.drawCentredString(pw / 2, ph * 0.16,
        "Additional revenue: 20 Narration Suites ($300/night)  ·  Food Truck  ·  Alcohol Operations")
    cv.drawCentredString(pw / 2, ph * 0.14,
        "Target: 40–60 high-quality events annually")

    # Footer
    cv.setFont(FONT_BODY, 7)
    cv.setFillColorRGB(*hex_to_rgb01("#393836"))
    cv.drawCentredString(pw / 2, 20, "Confidential — Studio Giraffe Internal Planning Document")

# ── MONTH PAGE ────────────────────────────────────────────────────────────────

def draw_month_page(cv, month_data):
    pw, ph = PAGE_LS   # 792 × 612

    year  = month_data["year"]
    month = month_data["month"]
    mname = month_data["name"]
    events_raw = month_data["events"]
    notes = month_data["notes"]

    # Build a quick lookup: day_str -> [(cat, label), …]
    day_events = {}
    for (day_str, cat, label) in events_raw:
        day_events.setdefault(day_str, []).append((cat, label))

    # ── Page background
    cv.setFillColorRGB(*hex_to_rgb01("#F7F6F2"))
    cv.rect(0, 0, pw, ph, fill=1, stroke=0)

    # ── Left accent bar
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.rect(0, 0, 5, ph, fill=1, stroke=0)

    # ── Month name
    cv.setFont(FONT_HEADING, 34)
    cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
    cv.drawString(22, ph - 46, mname.upper())

    # ── "Studio Giraffe" sub-label
    cv.setFont(FONT_BODY, 9)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(22, ph - 60, "Studio Giraffe — Event Calendar")

    # ── Inline legend (top right)
    legend_items = list(EC.items())
    lx_start = pw - 18
    ly = ph - 24
    for label, cols in reversed(legend_items):
        # swatch
        sw = cv.stringWidth(label, FONT_BODY, 7) + 18
        lx_start -= sw
        cv.setFillColor(cols["bg"])
        cv.roundRect(lx_start, ly - 2, 10, 10, 1, fill=1, stroke=0)
        cv.setFont(FONT_BODY, 7)
        set_fill(cv, HexColor("#1C1B19"))
        cv.drawString(lx_start + 13, ly, label)
        lx_start -= 6  # gap

    # ── Calendar grid ────────────────────────────────────────────────────────
    MARGIN_L  = 18
    MARGIN_R  = 18
    TOP_Y     = ph - 72
    BOTTOM_Y  = 56       # leave space for notes

    grid_w = pw - MARGIN_L - MARGIN_R
    grid_h = TOP_Y - BOTTOM_Y

    # Header row: day names
    DAY_NAMES = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    cell_w = grid_w / 7
    hdr_h  = 18

    # Draw day-name headers
    for i, dn in enumerate(DAY_NAMES):
        hx = MARGIN_L + i * cell_w
        hy = TOP_Y - hdr_h
        # background
        cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
        cv.rect(hx, hy, cell_w, hdr_h, fill=1, stroke=0)
        # text
        cv.setFont(FONT_HEADING, 7)
        cv.setFillColorRGB(1, 1, 1)
        cv.drawCentredString(hx + cell_w / 2, hy + 5, dn)

    # Calendar cells
    # Determine first weekday (0=Mon in Python calendar) → we use Sun=0
    # calendar.monthrange returns (weekday of first day, number of days)
    # Python weekday: 0=Mon…6=Sun → Sun index = (weekday + 1) % 7
    first_wd_py, num_days = calendar.monthrange(year, month)
    first_col = (first_wd_py + 1) % 7   # Sun-based column index

    num_rows = ((first_col + num_days - 1) // 7) + 1
    cell_h = (grid_h - hdr_h) / num_rows

    for day in range(1, num_days + 1):
        cell_idx = first_col + day - 1
        row = cell_idx // 7
        col = cell_idx % 7
        cx = MARGIN_L + col * cell_w
        cy = TOP_Y - hdr_h - (row + 1) * cell_h

        # Cell background
        cv.setFillColorRGB(*hex_to_rgb01("#FBFBF9"))
        cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
        cv.setLineWidth(0.4)
        cv.rect(cx, cy, cell_w, cell_h, fill=1, stroke=1)

        # Day number
        cv.setFont(FONT_HEADING, 9)
        cv.setFillColorRGB(*hex_to_rgb01("#28251D"))
        cv.drawString(cx + 4, cy + cell_h - 12, str(day))

        # Events in this cell
        ev_list = day_events.get(str(day), [])
        ev_y = cy + cell_h - 24
        for (cat, ev_label) in ev_list:
            if ev_y < cy + 2:
                break
            bg  = EC[cat]["bg"]
            txt = EC[cat]["text"]
            pill_h = min(12, (cell_h - 20) / max(1, len(ev_list)) - 1)
            pill_h = max(pill_h, 9)
            # pill background
            cv.setFillColor(bg)
            cv.roundRect(cx + 2, ev_y - pill_h + 2, cell_w - 4, pill_h, 2, fill=1, stroke=0)
            # pill text — truncate to fit
            cv.setFont(FONT_BODY, 6)
            set_fill(cv, txt)
            max_chars = int((cell_w - 10) / 3.5)
            display = ev_label if len(ev_label) <= max_chars else ev_label[:max_chars - 1] + "…"
            cv.drawString(cx + 5, ev_y - pill_h + 4, display)
            ev_y -= pill_h + 2

    # ── Notes area ────────────────────────────────────────────────────────────
    notes_y  = BOTTOM_Y - 2
    notes_h  = 40
    notes_box_y = notes_y - notes_h + 14

    # Label
    cv.setFont(FONT_HEADING, 7)
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.drawString(MARGIN_L, notes_y, "NOTES / PROMOTER ASSIGNED")

    # Box
    cv.setFillColorRGB(*hex_to_rgb01("#F9F8F5"))
    cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
    cv.setLineWidth(0.4)
    cv.rect(MARGIN_L, notes_box_y, grid_w, 28, fill=1, stroke=1)

    # Pre-populated notes text
    cv.setFont(FONT_BODY, 7)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(MARGIN_L + 4, notes_box_y + 17, notes)
    cv.drawString(MARGIN_L + 4, notes_box_y + 6,
                  "Promoter: _______________________   Contact: _______________________   Budget: $___________")

    # ── Footer line ───────────────────────────────────────────────────────────
    cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
    cv.setLineWidth(0.4)
    cv.line(MARGIN_L, 12, pw - MARGIN_R, 12)
    cv.setFont(FONT_BODY, 6.5)
    cv.setFillColorRGB(*hex_to_rgb01("#BAB9B4"))
    cv.drawString(MARGIN_L, 4, "Studio Giraffe — 12-Month Event Calendar  |  May 2026 – April 2027  |  Confidential")
    cv.drawRightString(pw - MARGIN_R, 4, mname)

# ── SUMMARY PAGE ─────────────────────────────────────────────────────────────

def draw_summary_page(cv):
    pw, ph = PAGE_LS

    cv.setFillColorRGB(*hex_to_rgb01("#F7F6F2"))
    cv.rect(0, 0, pw, ph, fill=1, stroke=0)

    # Accent bar
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.rect(0, 0, 5, ph, fill=1, stroke=0)

    # Title
    cv.setFont(FONT_HEADING, 28)
    cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
    cv.drawString(22, ph - 46, "ANNUAL SUMMARY")
    cv.setFont(FONT_BODY, 9)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(22, ph - 60, "Studio Giraffe — May 2026 through April 2027")

    # ── Count events by category
    cat_counts = {k: 0 for k in EC}
    all_key_dates = []
    for md in MONTHS:
        for (day_str, cat, label) in md["events"]:
            cat_counts[cat] += 1
            all_key_dates.append((md["name"], day_str, cat, label))

    total = sum(cat_counts.values())

    # ── Category totals table
    table_x = 22
    table_y = ph - 90
    col_widths = [190, 60, 60]
    row_h = 20
    headers = ["Event Category", "Events", "% of Total"]

    # Header row
    cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
    cv.rect(table_x, table_y - row_h, sum(col_widths), row_h, fill=1, stroke=0)
    cv.setFont(FONT_HEADING, 8)
    cv.setFillColorRGB(1, 1, 1)
    for i, hdr in enumerate(headers):
        hx = table_x + sum(col_widths[:i]) + 4
        cv.drawString(hx, table_y - row_h + 6, hdr)

    for r, (cat, cnt) in enumerate(cat_counts.items()):
        ry = table_y - (r + 2) * row_h
        # alt row bg
        if r % 2 == 1:
            cv.setFillColorRGB(*hex_to_rgb01("#F9F8F5"))
            cv.rect(table_x, ry, sum(col_widths), row_h, fill=1, stroke=0)
        # swatch
        cv.setFillColor(EC[cat]["bg"])
        cv.roundRect(table_x + 2, ry + 5, 10, 10, 2, fill=1, stroke=0)
        # text
        cv.setFont(FONT_BODY, 8)
        cv.setFillColorRGB(*hex_to_rgb01("#28251D"))
        cv.drawString(table_x + 16, ry + 6, cat)
        cv.drawString(table_x + col_widths[0] + 20, ry + 6, str(cnt))
        pct = f"{cnt / total * 100:.0f}%"
        cv.drawString(table_x + col_widths[0] + col_widths[1] + 16, ry + 6, pct)
        # grid line
        cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
        cv.setLineWidth(0.3)
        cv.line(table_x, ry, table_x + sum(col_widths), ry)

    # Total row
    total_y = table_y - (len(cat_counts) + 2) * row_h
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.rect(table_x, total_y, sum(col_widths), row_h, fill=1, stroke=0)
    cv.setFont(FONT_HEADING, 8)
    cv.setFillColorRGB(1, 1, 1)
    cv.drawString(table_x + 4, total_y + 6, "TOTAL EVENTS")
    cv.drawString(table_x + col_widths[0] + 20, total_y + 6, str(total))
    cv.drawString(table_x + col_widths[0] + col_widths[1] + 16, total_y + 6, "100%")

    # ── Key Dates column
    kd_x = 370
    kd_y = ph - 90
    cv.setFont(FONT_HEADING, 9)
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.drawString(kd_x, kd_y, "KEY DATES AT A GLANCE")

    # Pick highlight events
    key_highlights = [
        ("May 2026",      "16", "Cinco de Mayo Cultural Night"),
        ("June 2026",     "20", "Pride Night Celebration"),
        ("July 2026",     "3-4","July 4th Spectacular"),
        ("October 2026",  "25", "Halloween Spectacular"),
        ("November 2026", "1",  "Día de los Muertos Night"),
        ("December 2026", "31", "NYE Countdown Gala"),
        ("February 2027", "14", "Valentine's Day Special"),
        ("March 2027",    "14", "SXSW Spillover Concert"),
        ("April 2027",    "25", "Anniversary Gala"),
    ]

    for i, (mon, day, ev) in enumerate(key_highlights):
        iy = kd_y - (i + 1) * 18
        cv.setFont(FONT_HEADING, 7)
        cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
        cv.drawString(kd_x, iy, f"{mon} {day}")
        cv.setFont(FONT_BODY, 8)
        cv.setFillColorRGB(*hex_to_rgb01("#28251D"))
        cv.drawString(kd_x + 110, iy, ev)

    # ── Revenue note box
    rev_y = kd_y - len(key_highlights) * 18 - 30
    cv.setFillColorRGB(*hex_to_rgb01("#CAE8E4"))
    cv.roundRect(kd_x, rev_y - 60, pw - kd_x - 22, 64, 4, fill=1, stroke=0)
    cv.setFont(FONT_HEADING, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.drawString(kd_x + 8, rev_y - 14, "ADDITIONAL REVENUE STREAMS")
    cv.setFont(FONT_BODY, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#1C1B19"))
    lines = [
        "20 Narration Suites @ $300/night — available every event night",
        "Food Truck operations (venue-operated)",
        "Alcohol operations & bar programming",
        "Joe Hand Promotions — UFC/Boxing broadcast licensing",
    ]
    for i, line in enumerate(lines):
        cv.drawString(kd_x + 8, rev_y - 28 - i * 10, f"• {line}")

    # ── Contact block
    contact_y = 60
    cv.setFillColorRGB(*hex_to_rgb01("#F9F8F5"))
    cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
    cv.setLineWidth(0.4)
    cv.rect(22, contact_y - 30, pw - 44, 44, fill=1, stroke=1)
    cv.setFont(FONT_HEADING, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.drawString(30, contact_y + 6, "PRIMARY CONTACT")
    cv.setFont(FONT_BODY, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(30, contact_y - 6, "Name: _______________________________   Title: ____________________________   Phone/Email: ________________________________")
    cv.setFont(FONT_HEADING, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#01696F"))
    cv.drawString(440, contact_y + 6, "JOE HAND PROMOTIONS")
    cv.setFont(FONT_BODY, 8)
    cv.setFillColorRGB(*hex_to_rgb01("#7A7974"))
    cv.drawString(440, contact_y - 6, "joehand.com  |  215-483-3455  |  Broadcast licensing for UFC & boxing events")

    # Footer
    cv.setStrokeColorRGB(*hex_to_rgb01("#D4D1CA"))
    cv.setLineWidth(0.4)
    cv.line(22, 14, pw - 22, 14)
    cv.setFont(FONT_BODY, 6.5)
    cv.setFillColorRGB(*hex_to_rgb01("#BAB9B4"))
    cv.drawString(22, 5, "Studio Giraffe — 12-Month Event Calendar  |  May 2026 – April 2027  |  Confidential")
    cv.drawRightString(pw - 22, 5, "Annual Summary")

# ── BUILD PDF ─────────────────────────────────────────────────────────────────

def build():
    print("Building PDF…")

    # We need mixed-size pages: portrait cover + landscape month pages
    # ReportLab canvas doesn't natively support per-page sizes easily,
    # but we can set pagesize on showPage then change it.
    # Trick: start with portrait for cover, then switch to landscape.

    cv = canvas.Canvas(OUT_PATH, pagesize=PAGE_PT)
    cv.setTitle("Studio Giraffe 12-Month Event Calendar")
    cv.setAuthor("Perplexity Computer")

    # Cover
    print("  Drawing cover…")
    draw_cover(cv)
    cv.showPage()

    # Switch to landscape for month pages
    cv.setPageSize(PAGE_LS)

    for i, md in enumerate(MONTHS):
        print(f"  Drawing {md['name']}…")
        draw_month_page(cv, md)
        cv.showPage()

    # Summary page (still landscape)
    print("  Drawing summary page…")
    draw_summary_page(cv)
    cv.showPage()

    cv.save()
    print(f"  Saved to {OUT_PATH}")

if __name__ == "__main__":
    build()
