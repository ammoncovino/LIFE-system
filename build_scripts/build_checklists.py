#!/usr/bin/env python3
"""
LIFE System — Opening Checklists PDF Builder
Generates a print-ready Opening Checklists PDF for all departments at 3 aquarium locations.
"""

import json
import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# ─── Brand Colors ────────────────────────────────────────────────────────────
NAVY       = HexColor("#2C3481")
DARK_BROWN = HexColor("#271610")
LIGHT_BLUE = HexColor("#E8EAF6")  # very light navy tint for section bg
MEDIUM_BLUE= HexColor("#C5CAE9")  # slightly darker for dept header
OFF_WHITE  = HexColor("#F9F8F5")
BORDER     = HexColor("#D4D1CA")
MUTED      = HexColor("#7A7974")
ACCENT     = HexColor("#4A5299")  # mid-tone navy for sub-headers

PAGE_W, PAGE_H = letter  # 612 x 792 pt
MARGIN_L = 0.75 * inch
MARGIN_R = 0.75 * inch
MARGIN_T = 0.75 * inch
MARGIN_B = 0.6 * inch

CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ─── Fonts ───────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

def download_font(url, filename):
    path = FONT_DIR / filename
    if not path.exists():
        print(f"  Downloading {filename}...")
        urllib.request.urlretrieve(url, path)
    return str(path)

print("Downloading fonts...")
# DM Sans (headings) and Inter (body) — both clean sans-serifs
dm_sans_url      = "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf"
inter_reg_url    = "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"

try:
    dm_path   = download_font(dm_sans_url, "DMSans.ttf")
    inter_path= download_font(inter_reg_url, "Inter.ttf")
    pdfmetrics.registerFont(TTFont("DMSans",      dm_path))
    pdfmetrics.registerFont(TTFont("DMSans-Bold", dm_path))
    pdfmetrics.registerFont(TTFont("Inter",       inter_path))
    pdfmetrics.registerFont(TTFont("Inter-Bold",  inter_path))
    FONT_HEAD  = "DMSans-Bold"
    FONT_BODY  = "Inter"
    FONT_BOLD  = "Inter-Bold"
    print("  Custom fonts loaded.")
except Exception as e:
    print(f"  Font download failed ({e}), falling back to Helvetica.")
    FONT_HEAD = "Helvetica-Bold"
    FONT_BODY = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"

# ─── Load Data ───────────────────────────────────────────────────────────────
DATA_PATH = "/home/user/workspace/LIFE_system/build_specs/departments_final.json"
with open(DATA_PATH) as f:
    raw = json.load(f)

# ─── Organize Departments ────────────────────────────────────────────────────
# For opening checklists we use:
#   - 'opening' tasks if present (non-empty)
#   - else 'flat_tasks' (for "Daily Duties" depts with no explicit opening block)
# We include ONLY AM / opening-relevant content (not PM depts for an opening checklist)
# PM depts are excluded from opening checklists.

def get_opening_tasks(dept_data):
    """Return opening tasks: prefer 'opening' list, fall back to flat_tasks."""
    if dept_data.get('opening'):
        return dept_data['opening']
    return dept_data.get('flat_tasks', [])

def is_opening_dept(name):
    """True if this dept is relevant to opening (AM duties or Daily duties, not PM-only)."""
    name_upper = name.upper()
    if " PM " in name_upper or name_upper.endswith(" PM DUTIES") or name_upper.endswith(" PM"):
        return False
    return True

# Build structured location → category → departments
HOUSTON_GROUPS = {
    "Area 1 — Mammals": [
        "HA - Camel & Goat Daily Duties",
        "HA - Equine Daily Duties",
        "HA 1 African Crested Porcupine Daily Duties",
        "HA 1 Alpaca Daily Duties",
        "HA 1 Capybara Daily Duties",
        "HA 1 Cavy Daily Duties",
        "HA 1 Goat and Sheep Daily Duties",
        "HA 1 Kangaroo Daily Duties",
        "HA 1 Mini Pig Daily Duties",
        "HA 1 Tack shed Daily Duties",
        "HA 1 Warthog Daily Duties",
        "HA 1 Warthog and Pig Daily Duties",
    ],
    "Area 2 — Primates": [
        "HA 2 Black & White Ruffed Daily Duties",
        "HA 2 Prep Room Daily Duties",
        "HA 2 Red Ruffed Daily Duties",
        "HA 2 Ringtail Daily Duties",
    ],
    "Area 3 — Small Mammals": [
        "HA 3 Armadillo Daily Duties",
        "HA 3 Hedgehog Daily Duties",
        "HA 3 Kinkajou Off Exhibit Daily Duties",
        "HA 3 PTP Daily Duties",
        "HA 3 Rabbit Daily Duties",
        "HA 3 Sloth Daily Duties",
        "HA 3 Tamandua Daily Duties",
    ],
    "Area 4 — Giraffe": [
        "HA 4 Giraffe & Donkey Daily Duties",
    ],
    "Birds": [
        "HA Bird Daily Duties",
        "HA Big Bird Daily Duties",
        "HA Emu Daily Duties",
        "HA Indoor Aviary Daily Duties",
        "HA Outdoor Aviary Daily Duties",
        "HA Toucan Daily Duties",
    ],
    "Marine": [
        "HA Marine AM Duties",
    ],
    "Reptile": [
        "HA Reptile AM Duties",
        "HA Reptile Daily Duties",
    ],
    "Custodial": [
        "HA Custodial AM Duties",
        "HA Custodial Daily Duties",
    ],
    "Otters": [
        "HA Otters Daily Duties",
    ],
}

SA_GROUPS = {
    "Mammals — Lemurs & Primates": [
        "SA B&W Ruffed Lemur AM Duties",
        "SA Brown Lemur AM Duties",
        "SA Red Ruffed Lemur AM Duties",
        "SA Ring-Tailed Lemur AM Duties",
        "Tamandua AM Duties",
    ],
    "Mammals — Other": [
        "SA Alpacas and Goat AM Duties",
        "SA Porcupine AM Duties",
        "SA Red Kangaroo AM Duties",
        "SA Woodchuck Cavy AM Duties",
    ],
    "Reptile": [
        "SA Reptile AM Duties",
    ],
    "Marine / Jelly": [
        "SA Jelly Lab & Sea Turtle Daily Duties",
        "SA Marine Daily Duties",
    ],
}

AA_GROUPS = {
    "Mammals — Lemurs & Primates": [
        "Spider Monkey AM Duties",
        "B&W Ruffed Lemur AM Duties",
        "Troop 1 Red Ruffed Lemur AM Duties",
        "Troop 2 Red Ruffed Lemurs AM Duties",
        "Troop 3 Red Ruffed Lemurs AM Duties",
        "Sloth AM Duties",
        "Armadillo AM Duties",
        "PTP AM Duties",
        "Capybara AM Duties",
        "Wallaby AM Duties",
    ],
    "Birds": [
        "AA Bird AM Duties",
        "AA Indoor Aviary AM Duties",
        "AA Parakeet AM Duties",
        "AA Toucan AM Duties",
    ],
    "Marine": [
        "AA Marine AM Duties",
    ],
    "Reptile": [
        "AA Reptile AM Duties",
    ],
    "Penguins": [
        "AA Penguins AM Duties",
    ],
    "Prep Area": [
        "Prep Area Daily Duties",
    ],
}

LOCATIONS = [
    {
        "name": "Houston",
        "code": "HA",
        "subtitle": "Houston Interactive Aquarium",
        "groups": HOUSTON_GROUPS,
        "data": raw["Houston"],
    },
    {
        "name": "San Antonio",
        "code": "SA",
        "subtitle": "San Antonio Aquarium",
        "groups": SA_GROUPS,
        "data": raw["San Antonio"],
    },
    {
        "name": "Austin",
        "code": "AA",
        "subtitle": "Austin Aquarium",
        "groups": AA_GROUPS,
        "data": raw["Austin"],
    },
]

# ─── PDF Canvas Helpers ───────────────────────────────────────────────────────
OUTPUT_PATH = "/home/user/workspace/LIFE_system/print_ready/CHECKLISTS_OPENING.pdf"

class PDFBuilder:
    def __init__(self, path):
        self.c = rl_canvas.Canvas(path, pagesize=letter)
        self.c.setTitle("LIFE System — Opening Checklists")
        self.c.setAuthor("Perplexity Computer")
        self.page_num = 0
        self.toc_entries = []  # [(label, page_number)]

    # ── Low-level drawing ──────────────────────────────────────────────────
    def new_page(self, footer=True, footer_label=None):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        if footer:
            self._draw_footer(footer_label)

    def _draw_footer(self, extra=None):
        c = self.c
        y = MARGIN_B - 0.2 * inch
        c.saveState()
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.line(MARGIN_L, y + 10, PAGE_W - MARGIN_R, y + 10)
        c.setFont(FONT_BODY, 7.5)
        c.setFillColor(MUTED)
        label = "LIFE System — Opening Checklists"
        if extra:
            label = f"{label} | {extra}"
        c.drawString(MARGIN_L, y, label)
        c.drawRightString(PAGE_W - MARGIN_R, y, f"Page {self.page_num}")
        c.restoreState()

    def _wrapped_text_lines(self, text, font, size, max_width):
        """Return list of lines that fit within max_width."""
        words = text.split()
        if not words:
            return ['']
        lines = []
        current = words[0]
        for word in words[1:]:
            test = current + ' ' + word
            if pdfmetrics.stringWidth(test, font, size) <= max_width:
                current = test
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def draw_wrapped_text(self, text, x, y, font, size, color, max_width):
        """Draw wrapped text, return new y position (lower)."""
        c = self.c
        c.setFont(font, size)
        c.setFillColor(color)
        leading = size * 1.4
        lines = self._wrapped_text_lines(text, font, size, max_width)
        for line in lines:
            c.drawString(x, y, line)
            y -= leading
        return y

    def text_height(self, text, font, size, max_width):
        """Return height consumed by wrapped text block."""
        lines = self._wrapped_text_lines(text, font, size, max_width)
        return len(lines) * size * 1.4

    # ── Cover Page ─────────────────────────────────────────────────────────
    def draw_cover(self):
        c = self.c
        self.new_page(footer=False)

        # Full background
        c.setFillColor(NAVY)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        # Decorative accent bar
        c.setFillColor(HexColor("#4A5299"))
        c.rect(0, PAGE_H * 0.38, PAGE_W, 4, fill=1, stroke=0)

        # Title
        c.setFillColor(white)
        c.setFont(FONT_HEAD, 42)
        title = "Opening Checklists"
        tw = pdfmetrics.stringWidth(title, FONT_HEAD, 42)
        c.drawString((PAGE_W - tw) / 2, PAGE_H * 0.55, title)

        # System name
        c.setFont(FONT_BODY, 16)
        c.setFillColor(HexColor("#C5CAE9"))
        sub = "LIFE System"
        sw = pdfmetrics.stringWidth(sub, FONT_BODY, 16)
        c.drawString((PAGE_W - sw) / 2, PAGE_H * 0.55 - 32, sub)

        # Locations
        c.setFont(FONT_BODY, 13)
        c.setFillColor(HexColor("#9FA8DA"))
        locs = "Houston  ·  San Antonio  ·  Austin"
        lw = pdfmetrics.stringWidth(locs, FONT_BODY, 13)
        c.drawString((PAGE_W - lw) / 2, PAGE_H * 0.55 - 56, locs)

        # Bottom meta
        c.setFont(FONT_BODY, 9)
        c.setFillColor(HexColor("#7986CB"))
        c.drawCentredString(PAGE_W / 2, MARGIN_B, "LIFE System — Opening Checklists | For Internal Use Only")

    # ── Table of Contents ──────────────────────────────────────────────────
    def draw_toc(self, entries):
        """entries: list of (indent_level, label, page_num)"""
        c = self.c
        self.new_page(footer=True)

        # Header bar
        c.setFillColor(NAVY)
        c.rect(MARGIN_L - 4, PAGE_H - MARGIN_T - 32, CONTENT_W + 8, 36, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont(FONT_HEAD, 16)
        c.drawString(MARGIN_L + 4, PAGE_H - MARGIN_T - 20, "Table of Contents")

        y = PAGE_H - MARGIN_T - 55
        row_h = 14
        bottom_stop = MARGIN_B + 0.4 * inch

        for level, label, pg in entries:
            if y < bottom_stop:
                self.new_page(footer=True)
                y = PAGE_H - MARGIN_T - 20

            if level == 0:
                # Location heading
                if y < PAGE_H - MARGIN_T - 55:
                    y -= 6
                c.setFillColor(LIGHT_BLUE)
                c.rect(MARGIN_L - 4, y - 3, CONTENT_W + 8, row_h + 4, fill=1, stroke=0)
                c.setFont(FONT_HEAD, 10)
                c.setFillColor(NAVY)
                c.drawString(MARGIN_L + 2, y, label)
                c.drawRightString(PAGE_W - MARGIN_R, y, str(pg))
                y -= row_h + 4
            elif level == 1:
                # Group heading
                c.setFont(FONT_BOLD, 9)
                c.setFillColor(DARK_BROWN)
                c.drawString(MARGIN_L + 14, y, label)
                c.setFont(FONT_BODY, 9)
                c.drawRightString(PAGE_W - MARGIN_R, y, str(pg))
                # dotted line
                dot_x = MARGIN_L + 14 + pdfmetrics.stringWidth(label, FONT_BOLD, 9) + 4
                dot_end = PAGE_W - MARGIN_R - pdfmetrics.stringWidth(str(pg), FONT_BODY, 9) - 4
                c.setFillColor(BORDER)
                c.setFont(FONT_BODY, 9)
                dots = ""
                while pdfmetrics.stringWidth(dots + ".", FONT_BODY, 9) < (dot_end - dot_x):
                    dots += "."
                c.drawString(dot_x, y, dots)
                y -= row_h + 2
            else:
                # Dept entry
                c.setFont(FONT_BODY, 8.5)
                c.setFillColor(DARK_BROWN)
                c.drawString(MARGIN_L + 28, y, label)
                c.drawRightString(PAGE_W - MARGIN_R, y, str(pg))
                dot_x = MARGIN_L + 28 + pdfmetrics.stringWidth(label, FONT_BODY, 8.5) + 4
                dot_end = PAGE_W - MARGIN_R - pdfmetrics.stringWidth(str(pg), FONT_BODY, 8.5) - 4
                c.setFillColor(BORDER)
                dots = ""
                while pdfmetrics.stringWidth(dots + ".", FONT_BODY, 8.5) < (dot_end - dot_x):
                    dots += "."
                c.drawString(dot_x, y, dots)
                y -= row_h

    # ── Location Section Header Page ───────────────────────────────────────
    def draw_location_header(self, name, subtitle):
        c = self.c
        self.new_page(footer=False)

        # Full navy bg
        c.setFillColor(NAVY)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        # Decorative horizontal stripe
        c.setFillColor(HexColor("#3D4DB7"))
        c.rect(0, PAGE_H * 0.45 - 2, PAGE_W, 6, fill=1, stroke=0)

        # White accent left strip
        c.setFillColor(white)
        c.rect(0, PAGE_H * 0.35, 8, PAGE_H * 0.3, fill=1, stroke=0)

        # "OPENING CHECKLISTS" label
        c.setFont(FONT_BODY, 11)
        c.setFillColor(HexColor("#9FA8DA"))
        label = "OPENING CHECKLISTS"
        lw = pdfmetrics.stringWidth(label, FONT_BODY, 11)
        c.drawString((PAGE_W - lw) / 2, PAGE_H * 0.56, label)

        # Location name — large
        c.setFont(FONT_HEAD, 52)
        c.setFillColor(white)
        nw = pdfmetrics.stringWidth(name, FONT_HEAD, 52)
        c.drawString((PAGE_W - nw) / 2, PAGE_H * 0.47, name)

        # Subtitle
        c.setFont(FONT_BODY, 14)
        c.setFillColor(HexColor("#C5CAE9"))
        sw = pdfmetrics.stringWidth(subtitle, FONT_BODY, 14)
        c.drawString((PAGE_W - sw) / 2, PAGE_H * 0.47 - 30, subtitle)

        return self.page_num

    # ── Department Checklist Page(s) ───────────────────────────────────────
    def draw_dept_checklist(self, dept_name, section, tasks, group_label, location_name):
        """Draw a department checklist. May span multiple pages."""
        c = self.c

        # Clean up dept name for display
        display_name = dept_name
        # Remove trailing "Daily Duties" / "AM Duties" for brevity on header
        for suffix in [" AM Duties", " Daily Duties", " Opening Duties"]:
            if display_name.endswith(suffix):
                display_name = display_name[:-len(suffix)].strip()
                break

        # Determine duty type label
        if "AM Duties" in dept_name:
            duty_type = "AM Opening Duties"
        elif "Daily Duties" in dept_name:
            duty_type = "Daily / Opening Duties"
        else:
            duty_type = "Opening Duties"

        def start_dept_page(is_first=True):
            self.new_page(footer=True, footer_label=location_name)
            y = PAGE_H - MARGIN_T

            # Department header bar
            header_h = 46 if is_first else 30
            c.setFillColor(NAVY)
            c.rect(MARGIN_L - 4, y - header_h, CONTENT_W + 8, header_h, fill=1, stroke=0)

            if is_first:
                # Group breadcrumb
                c.setFont(FONT_BODY, 8)
                c.setFillColor(HexColor("#9FA8DA"))
                c.drawString(MARGIN_L + 4, y - 13, f"{location_name}  ›  {group_label}")

                # Department name
                c.setFont(FONT_HEAD, 15)
                c.setFillColor(white)
                # Wrap if needed
                lines = self._wrapped_text_lines(display_name, FONT_HEAD, 15, CONTENT_W - 100)
                c.drawString(MARGIN_L + 4, y - 29, lines[0])
                if len(lines) > 1:
                    c.drawString(MARGIN_L + 4, y - 43, lines[1])

                # Duty type badge (right side)
                badge_text = duty_type
                badge_w = pdfmetrics.stringWidth(badge_text, FONT_BODY, 8) + 10
                c.setFillColor(HexColor("#4A5299"))
                c.roundRect(PAGE_W - MARGIN_R - badge_w - 4, y - 32, badge_w + 2, 16, 4, fill=1, stroke=0)
                c.setFont(FONT_BODY, 8)
                c.setFillColor(white)
                c.drawString(PAGE_W - MARGIN_R - badge_w, y - 27, badge_text)

                # Section subtitle
                if section:
                    c.setFont(FONT_BODY, 8)
                    c.setFillColor(MUTED)
                    # Trim overly long section strings
                    sec_display = section[:90] + "..." if len(section) > 90 else section
                    c.drawString(MARGIN_L + 4, y - 44, sec_display)
            else:
                # Continuation header
                c.setFont(FONT_HEAD, 13)
                c.setFillColor(white)
                c.drawString(MARGIN_L + 4, y - 20, f"{display_name} (continued)")

            return y - header_h - 8

        # Estimate if all tasks + signature block fit on one page
        TASK_LINE_H = 18      # height per task row (checkbox + text)
        SIG_BLOCK_H = 52      # height for signature fields
        TASK_TEXT_W = CONTENT_W - 30  # width for task text (after checkbox)

        def estimate_task_height(task_list):
            h = 0
            for t in task_list:
                n_lines = len(self._wrapped_text_lines(t, FONT_BODY, 9.5, TASK_TEXT_W))
                h += max(TASK_LINE_H, n_lines * 13 + 4)
            return h

        task_h = estimate_task_height(tasks)
        available_first = PAGE_H - MARGIN_T - 46 - 8 - MARGIN_B - 0.4 * inch - SIG_BLOCK_H

        # Start first page
        pg_start = self.page_num + 1
        y = start_dept_page(is_first=True)

        bottom_limit = MARGIN_B + 0.4 * inch + SIG_BLOCK_H + 10

        task_idx = 0
        while task_idx < len(tasks):
            task = tasks[task_idx]
            lines = self._wrapped_text_lines(task, FONT_BODY, 9.5, TASK_TEXT_W)
            row_h = max(TASK_LINE_H, len(lines) * 13 + 4)

            # If we'd overflow, start a new page (no sig block on non-last pages)
            if y - row_h < (MARGIN_B + 0.4 * inch + 10):
                # Is this the last task? If yes, add sig block check
                if task_idx == len(tasks) - 1:
                    # Won't fit: start new page
                    y = start_dept_page(is_first=False)
                else:
                    y = start_dept_page(is_first=False)

            # Draw checkbox
            cb_x = MARGIN_L + 2
            cb_y = y - 13
            cb_size = 10
            c.setStrokeColor(DARK_BROWN)
            c.setLineWidth(1)
            c.rect(cb_x, cb_y, cb_size, cb_size, fill=0, stroke=1)

            # Task text
            c.setFont(FONT_BODY, 9.5)
            c.setFillColor(DARK_BROWN)
            text_x = MARGIN_L + 20
            ty = y - 11
            for line in lines:
                c.drawString(text_x, ty, line)
                ty -= 13

            # Light separator line every other row for readability
            c.setStrokeColor(HexColor("#E8E8E0"))
            c.setLineWidth(0.3)
            c.line(MARGIN_L, y - row_h + 2, PAGE_W - MARGIN_R, y - row_h + 2)

            y -= row_h
            task_idx += 1

        # Ensure sig block fits on current page
        if y - SIG_BLOCK_H < MARGIN_B + 0.3 * inch:
            y = start_dept_page(is_first=False)

        # ── Signature Block ──────────────────────────────────────────────
        self._draw_sig_block(y)

        return pg_start

    def _draw_sig_block(self, y):
        c = self.c
        y -= 10

        # Thin separator
        c.setStrokeColor(NAVY)
        c.setLineWidth(0.75)
        c.line(MARGIN_L, y, PAGE_W - MARGIN_R, y)
        y -= 16

        # Row 1: Staff Initials + Date
        field_w = CONTENT_W / 2 - 10
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(NAVY)
        c.drawString(MARGIN_L, y, "Staff Initials:")
        c.setStrokeColor(DARK_BROWN)
        c.setLineWidth(0.5)
        c.line(MARGIN_L + 75, y - 2, MARGIN_L + field_w, y - 2)

        c.drawString(MARGIN_L + field_w + 20, y, "Date:")
        c.line(MARGIN_L + field_w + 20 + 35, y - 2, PAGE_W - MARGIN_R, y - 2)

        y -= 16

        # Row 2: Management Sign Off
        c.setFont(FONT_BOLD, 8.5)
        c.setFillColor(NAVY)
        c.drawString(MARGIN_L, y, "Management Sign Off:")
        c.setStrokeColor(DARK_BROWN)
        c.setLineWidth(0.5)
        c.line(MARGIN_L + 118, y - 2, PAGE_W - MARGIN_R, y - 2)

    def save(self):
        self.c.save()
        print(f"  PDF saved to {OUTPUT_PATH}")


# ─── Build PDF ────────────────────────────────────────────────────────────────

builder = PDFBuilder(OUTPUT_PATH)

# Cover page
builder.draw_cover()
print("  Cover page drawn.")

# We'll collect TOC entries then re-draw TOC at the end using a two-pass approach.
# Since ReportLab canvas doesn't support going back, we'll do a single pass and
# record page numbers, then draw the TOC on page 2 using a placeholder approach.
# Strategy: draw TOC page placeholder now, fill entries, then write TOC at end via
# a second canvas draw pass... Actually, we'll build pages in order and keep track,
# then insert TOC via a merge at the end using pypdf.

# For simplicity with canvas-only: build TOC entries as we go, then at the end
# we know all page numbers. We'll use a two-pass approach:
# Pass 1: build all content, track page numbers → save to temp
# Pass 2: insert TOC using page numbers from pass 1 → merge

# Actually, let's just build everything and note the TOC page is page 2.
# We'll write the TOC LAST as a separate canvas overlaid using pypdf.

# ─── First, build content pages and collect TOC data ─────────────────────────
toc_entries = []

for loc in LOCATIONS:
    loc_name    = loc["name"]
    loc_code    = loc["code"]
    loc_sub     = loc["subtitle"]
    loc_data    = loc["data"]
    loc_groups  = loc["groups"]

    # Location header page
    loc_pg = builder.draw_location_header(loc_name, loc_sub)
    toc_entries.append((0, loc_name, loc_pg))
    print(f"  Location header: {loc_name} (p{loc_pg})")

    for group_name, dept_list in loc_groups.items():
        group_first_pg = None

        for dept_name in dept_list:
            # Find dept in data (try exact match first, then partial)
            dept_data = loc_data.get(dept_name)
            if dept_data is None:
                # Try case-insensitive or slight variation
                for key in loc_data:
                    if key.lower() == dept_name.lower():
                        dept_data = loc_data[key]
                        break
            if dept_data is None:
                print(f"    WARNING: '{dept_name}' not found in {loc_name} data, skipping.")
                continue

            tasks = get_opening_tasks(dept_data)
            if not tasks:
                print(f"    SKIP (no tasks): {dept_name}")
                continue

            section = dept_data.get("section", "")

            pg = builder.draw_dept_checklist(
                dept_name=dept_name,
                section=section,
                tasks=tasks,
                group_label=group_name,
                location_name=loc_name,
            )

            if group_first_pg is None:
                group_first_pg = pg
                toc_entries.append((1, group_name, pg))

            # Clean display name for TOC
            disp = dept_name
            for suffix in [" AM Duties", " Daily Duties", " Opening Duties"]:
                if disp.endswith(suffix):
                    disp = disp[:-len(suffix)].strip()
                    break
            toc_entries.append((2, disp, pg))
            print(f"    Dept: {dept_name} (p{pg})")

# Now we have all pages. The TOC goes on page 2.
# We'll use pypdf to insert the TOC page after cover.
builder.save()

print(f"\nContent PDF built: {builder.page_num} pages total.")
print("TOC entries collected:", len(toc_entries))

# ─── Build TOC-only PDF ───────────────────────────────────────────────────────
TOC_PATH = "/tmp/toc_only.pdf"

toc_builder = PDFBuilder(TOC_PATH)
toc_builder.page_num = 1  # TOC will be page 2 in final
toc_builder.draw_toc(toc_entries)
toc_builder.save()

# ─── Merge: cover + TOC + content ────────────────────────────────────────────
import pypdf

cover_toc_content = pypdf.PdfWriter()

reader_main = pypdf.PdfReader(OUTPUT_PATH)
reader_toc  = pypdf.PdfReader(TOC_PATH)

# Page 0 = cover
cover_toc_content.add_page(reader_main.pages[0])

# TOC pages
for pg in reader_toc.pages:
    cover_toc_content.add_page(pg)

# Remaining content pages (skip cover = page 0)
for i in range(1, len(reader_main.pages)):
    cover_toc_content.add_page(reader_main.pages[i])

# Set metadata on merged PDF
cover_toc_content.add_metadata({
    "/Title":  "LIFE System — Opening Checklists",
    "/Author": "Perplexity Computer",
})

FINAL_PATH = "/home/user/workspace/LIFE_system/print_ready/CHECKLISTS_OPENING.pdf"
with open(FINAL_PATH, "wb") as f:
    cover_toc_content.write(f)

final_count = len(cover_toc_content.pages)
print(f"\nFinal merged PDF: {final_count} pages → {FINAL_PATH}")
print("Done.")
