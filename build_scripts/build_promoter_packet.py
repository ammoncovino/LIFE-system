"""
Studio Giraffe — Promoter Partnership Packet
2-page PDF using ReportLab Canvas API for precise layout control.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, Color
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Brand Colors ──────────────────────────────────────────────────────────────
TEAL        = HexColor("#00AAAD")
TEAL_DARK   = HexColor("#007F82")
BROWN       = HexColor("#422616")
CREAM       = HexColor("#F3F5D6")
CREAM_DARK  = HexColor("#E8EBC0")   # slightly deeper for contrast areas
WHITE       = white
MUTED       = HexColor("#7A7060")
BORDER      = HexColor("#C8CAA8")
LIGHT_TEAL  = HexColor("#E0F7F7")

OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STUDIO_GIRAFFE_PROMOTER_PACKET.pdf"

W, H = letter  # 612 x 792 pts


# ── Helper utilities ──────────────────────────────────────────────────────────

def filled_rect(c, x, y, w, h, fill, stroke=None, radius=0):
    c.saveState()
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.5)
    else:
        c.setStrokeColor(fill)
        c.setLineWidth(0)
    if radius:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    else:
        c.rect(x, y, w, h, fill=1, stroke=1 if stroke else 0)
    c.restoreState()


def h_line(c, x1, x2, y, color=BORDER, width=0.5):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)
    c.restoreState()


def draw_text(c, text, x, y, font="Helvetica", size=10, color=BROWN, align="left"):
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, text)
    elif align == "right":
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)
    c.restoreState()


def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=10, color=BROWN, leading=14):
    """Very simple manual word-wrap for canvas text."""
    c.saveState()
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    cur_y = y
    for word in words:
        test = (line + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            line = test
        else:
            if line:
                c.drawString(x, cur_y, line)
                cur_y -= leading
            line = word
    if line:
        c.drawString(x, cur_y, line)
    c.restoreState()
    return cur_y - leading  # return bottom y


def stat_block(c, x, y, w, h_block, value, label, teal_bg=True):
    """Draws a hero stat card."""
    bg = TEAL if teal_bg else CREAM_DARK
    txt_main = WHITE if teal_bg else BROWN
    txt_label = CREAM if teal_bg else MUTED
    filled_rect(c, x, y, w, h_block, bg, radius=4)
    cy = y + h_block / 2
    draw_text(c, value, x + w / 2, cy + 5, "Helvetica-Bold", 18, txt_main, "center")
    draw_text(c, label, x + w / 2, cy - 10, "Helvetica", 7.5, txt_label, "center")


def section_header(c, x, y, text, page_width=None, bar_width=None):
    """Draws a teal left-bar section label."""
    bar_w = 4
    bar_h = 13
    filled_rect(c, x, y, bar_w, bar_h, TEAL)
    draw_text(c, text.upper(), x + bar_w + 6, y + 2, "Helvetica-Bold", 9, TEAL)
    label_right = x + bar_w + 6 + c.stringWidth(text.upper(), "Helvetica-Bold", 9)
    if bar_width:
        h_line(c, label_right + 6, x + bar_width, y + 7, BORDER, 0.5)


def bullet_row(c, x, y, label, value, col_gap=130, color=BROWN):
    """Draws a label: value pair."""
    draw_text(c, label, x, y, "Helvetica-Bold", 9, TEAL)
    draw_text(c, value, x + col_gap, y, "Helvetica", 9, color)
    return y - 13


def bullet_item(c, x, y, text, font="Helvetica", size=9, color=BROWN, indent=10):
    c.saveState()
    c.setFillColor(TEAL)
    c.circle(x + 3, y + 3, 2, fill=1, stroke=0)
    c.restoreState()
    draw_text(c, text, x + indent, y, font, size, color)
    return y - 13


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VENUE OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page1(c):
    MARGIN_L = 0.65 * inch
    MARGIN_R = 0.65 * inch
    content_w = W - MARGIN_L - MARGIN_R

    # ── Full-width header band ─────────────────────────────────────────────
    header_h = 110
    filled_rect(c, 0, H - header_h, W, header_h, BROWN)

    # Decorative teal stripe top
    filled_rect(c, 0, H - 6, W, 6, TEAL)

    # Brand wordmark
    draw_text(c, "STUDIO", 36, H - 42, "Helvetica-Bold", 22, TEAL, "left")
    draw_text(c, "GIRAFFE", 36, H - 63, "Helvetica-Bold", 22, WHITE, "left")
    # Sub-tagline
    draw_text(c, "ELEVATED ENTERTAINMENT", 36, H - 79, "Helvetica", 7.5, CREAM, "left")

    # Right side — document label
    draw_text(c, "PROMOTER PARTNERSHIP PACKET", W - MARGIN_R, H - 42,
              "Helvetica-Bold", 9, TEAL, "right")
    draw_text(c, "Confidential — For Prospective Partners", W - MARGIN_R, H - 57,
              "Helvetica", 7.5, CREAM, "right")
    draw_text(c, "studiogiraffe.com", W - MARGIN_R, H - 72,
              "Helvetica", 7.5, CREAM, "right")

    # Teal bottom stripe on header
    filled_rect(c, 0, H - header_h, W, 4, TEAL)

    y = H - header_h - 22

    # ── Intro tagline ─────────────────────────────────────────────────────
    draw_text(c, "Where Live Entertainment Meets Immersive Experience",
              W / 2, y, "Helvetica-Bold", 13, BROWN, "center")
    y -= 14
    draw_text(c,
              "Studio Giraffe is a premium, fully integrated entertainment venue inside a zoo & aquarium destination.",
              W / 2, y, "Helvetica", 8.5, MUTED, "center")
    y -= 22

    # ── Hero Stats Row ────────────────────────────────────────────────────
    section_header(c, MARGIN_L, y, "VENUE AT A GLANCE", bar_width=content_w)
    y -= 20

    stat_w = (content_w - 12) / 4
    stats = [
        ("1,200", "Max Standing\nCapacity"),
        ("750", "Seated\nCapacity"),
        ("600–700", "Parking Spaces\n4-Acre Lot"),
        ("300K+", "Annual Zoo &\nAquarium Visitors"),
    ]
    for i, (val, lbl) in enumerate(stats):
        sx = MARGIN_L + i * (stat_w + 4)
        stat_block(c, sx, y - 46, stat_w, 52, val, lbl, teal_bg=(i % 2 == 0))

    y -= 62

    # Second stats row
    stat_w2 = (content_w - 8) / 3
    stats2 = [
        ("6,800 sq ft", "Indoor Venue Space"),
        ("1,000", "Outdoor Capacity\n(Front + Rear)"),
        ("20", "On-Site Narration\nSuites"),
    ]
    for i, (val, lbl) in enumerate(stats2):
        sx = MARGIN_L + i * (stat_w2 + 4)
        stat_block(c, sx, y - 46, stat_w2, 52, val, lbl, teal_bg=(i % 2 != 0))

    y -= 62

    # ── Two-column layout ─────────────────────────────────────────────────
    col_w = (content_w - 18) / 2
    col1_x = MARGIN_L
    col2_x = MARGIN_L + col_w + 18
    col_y = y - 10

    # ── Column 1: Indoor Specs ─────────────────────────────────────────────
    section_header(c, col1_x, col_y, "INDOOR VENUE SPECS", bar_width=col_w)
    col_y1 = col_y - 20

    specs = [
        ("Total Space", "~6,800 sq ft"),
        ("Primary Room", "80 × 60 ft"),
        ("Secondary Room", "40 × 50 ft"),
        ("Standing", "900 – 1,200 guests"),
        ("Seated", "600 – 750 guests"),
        ("Hybrid", "750 – 900 guests"),
        ("Entrance", "Separate venue entry"),
        ("Park Flow", "Optional zoo access"),
    ]
    for label, val in specs:
        col_y1 = bullet_row(c, col1_x + 6, col_y1, label, val, col_gap=110)

    # ── Column 2: Outdoor + Sub-brands ────────────────────────────────────
    section_header(c, col2_x, col_y, "OUTDOOR + SUB-BRANDS", bar_width=col_w)
    col_y2 = col_y - 20

    outdoor = [
        ("Front Terrace", "~500 capacity"),
        ("Rear Grounds", "~500 capacity"),
        ("Parking", "4 acres / 600–700 cars"),
    ]
    for label, val in outdoor:
        col_y2 = bullet_row(c, col2_x + 6, col_y2, label, val, col_gap=100)

    col_y2 -= 4
    h_line(c, col2_x + 6, col2_x + col_w, col_y2 + 4, BORDER)
    col_y2 -= 8

    draw_text(c, "SUB-BRAND SPACES", col2_x + 6, col_y2, "Helvetica-Bold", 8, BROWN)
    col_y2 -= 14

    sub_brands = [
        ("The Overlook", "Premium elevated lounge experience"),
        ("The Watering Hole", "Casual social bar environment"),
    ]
    for name, desc in sub_brands:
        draw_text(c, name, col2_x + 6, col_y2, "Helvetica-Bold", 9, TEAL)
        col_y2 -= 12
        draw_text(c, desc, col2_x + 16, col_y2, "Helvetica", 8.5, MUTED)
        col_y2 -= 14

    # ── Production Assets (full width) ────────────────────────────────────
    bottom_y = min(col_y1, col_y2) - 16

    h_line(c, MARGIN_L, W - MARGIN_R, bottom_y + 8, BORDER)
    section_header(c, MARGIN_L, bottom_y - 4, "PRODUCTION ASSETS", bar_width=content_w)
    prod_y = bottom_y - 22

    prod_items = [
        ("12 × 9 ft LED Screen", "High-res indoor display"),
        ("Projection Mapping", "Full immersive system"),
        ("Wave Lasers + Haze", "Professional atmospheric FX"),
        ("Professional Sound", "Full PA system"),
        ("Green Room", "Artist prep suite (under construction)"),
        ("Food Operations", "Indoor dining + food truck"),
        ("Alcohol Operations", "Venue-controlled bar program"),
        ("Narration Suites", "20 units at $300/night"),
    ]

    cols = 4
    item_w = content_w / cols
    for i, (asset, detail) in enumerate(prod_items):
        col_i = i % cols
        row_i = i // cols
        ix = MARGIN_L + col_i * item_w
        iy = prod_y - row_i * 28
        filled_rect(c, ix + 2, iy - 16, item_w - 6, 26, LIGHT_TEAL, radius=3)
        draw_text(c, asset, ix + 8, iy - 4, "Helvetica-Bold", 8, TEAL)
        draw_text(c, detail, ix + 8, iy - 15, "Helvetica", 7.5, MUTED)

    # ── Footer ────────────────────────────────────────────────────────────
    filled_rect(c, 0, 0, W, 28, BROWN)
    filled_rect(c, 0, 28, W, 2, TEAL)
    draw_text(c, "STUDIO GIRAFFE  |  ELEVATED ENTERTAINMENT", 36, 10,
              "Helvetica", 7, CREAM)
    draw_text(c, "Page 1 of 2", W - MARGIN_R, 10, "Helvetica", 7, CREAM, "right")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PARTNERSHIP MODEL
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page2(c):
    MARGIN_L = 0.65 * inch
    MARGIN_R = 0.65 * inch
    content_w = W - MARGIN_L - MARGIN_R

    # ── Header band (slimmer) ──────────────────────────────────────────────
    header_h = 70
    filled_rect(c, 0, H - header_h, W, header_h, BROWN)
    filled_rect(c, 0, H - 6, W, 6, TEAL)
    filled_rect(c, 0, H - header_h, W, 4, TEAL)

    draw_text(c, "STUDIO GIRAFFE", 36, H - 35, "Helvetica-Bold", 16, TEAL)
    draw_text(c, "PARTNERSHIP STRUCTURE & DEAL TERMS", 36, H - 52,
              "Helvetica-Bold", 9, WHITE)

    draw_text(c, "PROMOTER PARTNERSHIP PACKET", W - MARGIN_R, H - 35,
              "Helvetica-Bold", 9, TEAL, "right")
    draw_text(c, "Confidential — For Prospective Partners", W - MARGIN_R, H - 50,
              "Helvetica", 7.5, CREAM, "right")

    y = H - header_h - 24

    # ── Why Studio Giraffe? ───────────────────────────────────────────────
    section_header(c, MARGIN_L, y, "WHY PARTNER WITH US?", bar_width=content_w)
    y -= 20

    why_items = [
        "Built-in audience via 300,000+ annual zoo & aquarium visitors",
        "Multi-format flexibility: concerts, comedy, EDM, cultural events & festivals",
        "Venue-controlled alcohol program — eliminates promoter liability exposure",
        "20 on-site narration suites for artist/crew accommodation ($300/night)",
        "Co-branded marketing across zoo/aquarium digital and physical channels",
        "Multi-promoter ecosystem — no exclusivity, no single-anchor monopoly",
    ]
    for item in why_items:
        y = bullet_item(c, MARGIN_L + 4, y, item, size=9)
    y -= 6

    # ── Deal Structure Timeline ───────────────────────────────────────────
    section_header(c, MARGIN_L, y, "DEAL STRUCTURE TIMELINE", bar_width=content_w)
    y -= 20

    # Timeline bar
    phases = [
        ("PHASE 1\nYears 1–2", "50 / 50\nTicket Split", "Venue: F&B, Alcohol, Parking"),
        ("PHASE 2\nYears 3–4", "60 / 40\nVenue-Favorable", "Continued F&B & Alcohol Retention"),
        ("YEAR 5\n& Beyond", "Full\nRenegotiation", "Terms reset by mutual agreement"),
    ]
    phase_w = (content_w - 12) / 3
    for i, (title_txt, split, note) in enumerate(phases):
        px = MARGIN_L + i * (phase_w + 6)
        py = y
        ph = 68
        bg = TEAL if i == 0 else (CREAM_DARK if i == 1 else LIGHT_TEAL)
        tc = WHITE if i == 0 else BROWN
        mc = WHITE if i == 0 else MUTED
        nc = CREAM if i == 0 else MUTED

        filled_rect(c, px, py - ph, phase_w, ph, bg, radius=5)

        # Phase label
        lines = title_txt.split("\n")
        draw_text(c, lines[0], px + phase_w / 2, py - 14,
                  "Helvetica-Bold", 9, tc, "center")
        draw_text(c, lines[1], px + phase_w / 2, py - 25,
                  "Helvetica", 8, mc, "center")

        # Split
        sp_lines = split.split("\n")
        draw_text(c, sp_lines[0], px + phase_w / 2, py - 40,
                  "Helvetica-Bold", 13, tc, "center")
        draw_text(c, sp_lines[1], px + phase_w / 2, py - 52,
                  "Helvetica", 8, mc, "center")

        # Note
        draw_text(c, note, px + phase_w / 2, py - 65,
                  "Helvetica", 7, nc, "center")

    y -= 80

    # ── Two-column lower section ──────────────────────────────────────────
    col_w = (content_w - 18) / 2
    col1_x = MARGIN_L
    col2_x = MARGIN_L + col_w + 18

    # ── Col 1: Venue Terms ────────────────────────────────────────────────
    section_header(c, col1_x, y, "VENUE TERMS & PROTECTIONS", bar_width=col_w)
    col_y1 = y - 20

    terms = [
        ("Alcohol Control", "Retained exclusively by venue"),
        ("Final Approval", "Venue reserves right on all events"),
        ("Sub-Leasing", "Strictly prohibited"),
        ("Perpetual Rights", "No auto-renewal / no lock-in"),
        ("Promoter Rights", "Multi-promoter model; no monopoly"),
    ]
    for label, val in terms:
        col_y1 = bullet_row(c, col1_x + 6, col_y1, label, val, col_gap=110, color=BROWN)

    col_y1 -= 8

    # Monthly target note — height: label(14) + 5 items*11 + bottom pad(10) = 79
    box_h = 82
    filled_rect(c, col1_x + 4, col_y1 - box_h, col_w - 8, box_h, LIGHT_TEAL, radius=4)
    draw_text(c, "MONTHLY EVENT TARGET", col1_x + 10, col_y1 - 12,
              "Helvetica-Bold", 8, TEAL)
    monthly = [
        "2× Music Events",
        "1× Comedy Night",
        "1× Themed / Specialty Event",
        "1× Vendor Weekend",
        "1× Flex / Co-Promotion",
    ]
    for j, m in enumerate(monthly):
        draw_text(c, m, col1_x + 16, col_y1 - 24 - j * 11,
                  "Helvetica", 8, BROWN)

    col_y1 -= box_h + 8
    draw_text(c, "Targeting 40–60 events annually", col1_x + 6, col_y1,
              "Helvetica-Bold", 8.5, BROWN)

    # ── Col 2: Event Types ────────────────────────────────────────────────
    section_header(c, col2_x, y, "EVENT CATEGORIES WE SEEK", bar_width=col_w)
    col_y2 = y - 20

    event_types = [
        ("Live Music", "Local to regional touring acts"),
        ("Comedy", "Stand-up, improv & showcase nights"),
        ("EDM / Electronic", "DJ sets, raves, immersive experiences"),
        ("Cultural Events", "Heritage festivals, art & community"),
        ("Festivals", "Multi-day, multi-stage productions"),
        ("Vendor Weekends", "Markets, pop-ups, curated experiences"),
    ]
    for etype, desc in event_types:
        draw_text(c, etype, col2_x + 6, col_y2, "Helvetica-Bold", 9, TEAL)
        col_y2 -= 12
        draw_text(c, desc, col2_x + 16, col_y2, "Helvetica", 8.5, MUTED)
        col_y2 -= 14

    # ── Revenue Streams Note ──────────────────────────────────────────────
    col_y2 -= 4
    filled_rect(c, col2_x + 4, col_y2 - 36, col_w - 8, 42, CREAM_DARK, radius=4)
    draw_text(c, "VENUE REVENUE STREAMS", col2_x + 10, col_y2 - 8,
              "Helvetica-Bold", 8, BROWN)
    streams = "Ticket split  ·  F&B sales  ·  Alcohol service  ·  Parking fees  ·  Narration suites"
    draw_text(c, streams, col2_x + 10, col_y2 - 20,
              "Helvetica", 7.5, MUTED)
    draw_text(c, "All retained by venue except negotiated ticket split",
              col2_x + 10, col_y2 - 32,
              "Helvetica", 7.5, MUTED)

    # ── Next Steps / Contact ──────────────────────────────────────────────
    contact_y = 90
    filled_rect(c, 0, 30, W, contact_y, BROWN)
    filled_rect(c, 0, 30 + contact_y, W, 3, TEAL)

    draw_text(c, "READY TO BRING YOUR EVENT TO STUDIO GIRAFFE?",
              W / 2, 30 + contact_y - 18, "Helvetica-Bold", 11, TEAL, "center")
    draw_text(c,
              "We welcome introductory conversations with all promoter types. Reach out to start the conversation.",
              W / 2, 30 + contact_y - 33, "Helvetica", 8.5, CREAM, "center")

    # Contact box
    cx_box = MARGIN_L + content_w * 0.15
    box_w = content_w * 0.7
    filled_rect(c, cx_box, 30 + 16, box_w, 38, TEAL_DARK, radius=5)
    draw_text(c, "[Contact Name]  |  [Email]  |  [Phone]",
              W / 2, 30 + 38, "Helvetica-Bold", 10, WHITE, "center")
    draw_text(c, "studiogiraffe.com",
              W / 2, 30 + 25, "Helvetica", 8.5, CREAM, "center")

    # Page footer strip
    filled_rect(c, 0, 0, W, 30, HexColor("#2A1A0D"))
    filled_rect(c, 0, 28, W, 2, TEAL)
    draw_text(c, "STUDIO GIRAFFE  |  ELEVATED ENTERTAINMENT", 36, 10,
              "Helvetica", 7, CREAM)
    draw_text(c, "Page 2 of 2", W - MARGIN_R, 10, "Helvetica", 7, CREAM, "right")


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("Studio Giraffe — Promoter Partnership Packet")
    c.setAuthor("Perplexity Computer")

    # Page 1
    draw_page1(c)
    c.showPage()

    # Page 2
    draw_page2(c)
    c.showPage()

    c.save()
    print(f"PDF saved: {OUTPUT}")


if __name__ == "__main__":
    build()
