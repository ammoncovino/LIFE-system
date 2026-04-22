"""v3 totem builder - clean modern layout.

Key differences from v2:
  - Clean solid-cream paper panel (bg_layout_v3_clean.png), no burn/deckle
  - Compact top bark band, larger title
  - Bolder question headings, slightly larger body text
  - Smaller, tighter footer
  - Reality Door sits in its own separate boxed panel (photo-ready for LLM)
  - QR code placeholder with 'Scan for AI guide' caption
"""

import io
import json
import os
from pathlib import Path
from PIL import Image
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle

from think_about_this import THINK_ABOUT_THIS
from reality_doors import (
    get_reality_door, STANDARD_CARE_BULLETS, BRIDGE_LINE,
)

import qrcode

# ---- Config ------------------------------------------------------------------
WORKSPACE = Path("/home/user/workspace")
K5_DIR    = WORKSPACE / "LIFE_k5_locked"
MASTER_JSON = WORKSPACE / "LIFE_totem_content_18.json"
IMG_DIR   = WORKSPACE
BG        = WORKSPACE / "bg_layout_v3_clean.png"
OUT_DIR   = WORKSPACE / "LIFE_totems_v3"
OUT_DIR.mkdir(exist_ok=True)

# Colors
CREAM       = HexColor("#F4EAD0")    # paper base
CREAM_BR    = HexColor("#FFF6DB")    # brighter cream for dark-bg text
INK         = HexColor("#1F1608")    # body text on paper
HEADER_INK  = HexColor("#120A04")    # Q headings (darker)
ACCENT      = HexColor("#7A3416")    # warm rust (headings accent)
GOLD        = HexColor("#C9A960")    # thin rules
DARK_PANEL  = HexColor("#1A1208")    # Reality Door panel bg (solid dark brown)

# Fonts
pdfmetrics.registerFont(TTFont("Cinzel",       "/tmp/fonts/Cinzel[wght].ttf"))
pdfmetrics.registerFont(TTFont("Inter",        "/tmp/fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold",   "/tmp/fonts/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-It", "/tmp/fonts/CormorantGaramond-Italic.ttf"))

PAGE_W, PAGE_H = LETTER  # 8.5 x 11
MARGIN = 0.30 * inch

# bg_layout_v3_clean.png measured zones:
#   Top bark band:   y = 9.10 -> 11.00 in  (~1.90 in)
#   Clean paper:     y = 2.25 ->  9.07 in  (~6.82 in)
#   Bottom bark:     y = 0.00 ->  2.20 in  (~2.20 in)

TOP_BARK_BOTTOM = 9.07 * inch
BOT_BARK_TOP    = 2.25 * inch

# Title placement (on top bark band)
TITLE_BASELINE = PAGE_H - 0.70 * inch
TITLE_SCI_Y    = PAGE_H - 1.00 * inch

# Dual-column split: paper left ~48% / forest right ~52%
# Paper edge approx at x = 3.85 in (from 0) per bg
PAPER_LEFT_EDGE  = 0.55 * inch
PAPER_RIGHT_EDGE = 3.85 * inch

# Allocate vertical space inside paper:
#   8 Q blocks:      top 55% of paper
#   Reality Door:    bottom 40% of paper (needs real room)
# Paper zone is 6.82 in tall -> split at 55% from top = 3.75 in down from paper top

PAPER_TOP    = TOP_BARK_BOTTOM - 0.15 * inch   # 8.92
PAPER_BOTTOM = BOT_BARK_TOP + 0.15 * inch      # 2.40
PAPER_H      = PAPER_TOP - PAPER_BOTTOM        # 6.52

# 8 Q block on clean paper
BODY_X      = PAPER_LEFT_EDGE + 0.05 * inch
BODY_W      = PAPER_RIGHT_EDGE - PAPER_LEFT_EDGE - 0.10 * inch  # ~3.20 in
BODY_TOP    = PAPER_TOP - 0.05 * inch
# Paper is 6.52 in. Give 8 Qs ~4.40 in, Reality Door ~2.00 in, small gap.
BODY_BOTTOM = PAPER_BOTTOM + 2.05 * inch

# Reality Door panel — its own boxed container, BELOW the 8 Qs on the paper
RD_X      = PAPER_LEFT_EDGE + 0.05 * inch
RD_W      = PAPER_RIGHT_EDGE - PAPER_LEFT_EDGE - 0.10 * inch
RD_TOP    = BODY_BOTTOM - 0.08 * inch
RD_BOTTOM = PAPER_BOTTOM + 0.05 * inch

# Image region (right of paper, covers forest bokeh)
IMG_X = PAPER_RIGHT_EDGE + 0.15 * inch
IMG_W = PAGE_W - IMG_X - 0.30 * inch
IMG_TOP    = PAPER_TOP
IMG_BOTTOM = PAPER_BOTTOM
IMG_Y = IMG_BOTTOM
IMG_H = IMG_TOP - IMG_BOTTOM

# QR code (bottom right, over bark)
QR_SIZE = 0.95 * inch
# Position so chip (QR_SIZE + 0.55in) is fully inside margin
QR_X    = PAGE_W - QR_SIZE - MARGIN - 0.30 * inch
QR_Y    = 0.85 * inch

# Lower band (Think About This + footer) - compact
LOWER_TOP    = BOT_BARK_TOP - 0.10 * inch
LOWER_BOTTOM = 0.20 * inch

# ---- Loaders -----------------------------------------------------------------

def load_data(slug):
    with open(K5_DIR / f"{slug}.json") as f:
        k5 = json.load(f)
    with open(MASTER_JSON) as f:
        master = json.load(f)
    sp = next((s for s in master["species"] if s["slug"] == slug), None)
    if not sp:
        sp = {"common_name": k5.get("species", slug), "scientific_name": k5.get("scientific_name", "")}
    return k5, sp


# ---- Background --------------------------------------------------------------

_BG_CACHE = {}
def _optimized_bg():
    key = str(BG)
    if key in _BG_CACHE:
        return _BG_CACHE[key]
    pil = Image.open(BG).convert("RGB")
    pil.thumbnail((1700, 2200), Image.LANCZOS)
    tmp = "/tmp/" + BG.stem + "_opt.jpg"
    pil.save(tmp, format="JPEG", quality=82, optimize=True)
    _BG_CACHE[key] = tmp
    return tmp


def draw_background(c):
    c.drawImage(_optimized_bg(), 0, 0, width=PAGE_W, height=PAGE_H,
                preserveAspectRatio=False, mask=None)


# ---- Title -------------------------------------------------------------------

def fit_title_font(c, text, max_w, start=42, min_size=26):
    size = start
    while size > min_size:
        w = c.stringWidth(text, "Cinzel", size)
        if w <= max_w:
            return size
        size -= 1
    return min_size


def draw_title(c, title_text, sci_name):
    """Title on the compact top bark band.

    Compact band means we skip the earlier heavy dark overlay.  Instead use a
    narrow semi-transparent strip only behind the title text so it stays
    legible against moss/bark while feeling modern.
    """
    title = title_text.upper()
    max_w = PAGE_W - 2 * MARGIN - 0.4 * inch
    size = fit_title_font(c, title, max_w, start=42, min_size=26)

    # Measure and draw a compact dark strip behind title for legibility
    tw = c.stringWidth(title, "Cinzel", size)
    strip_h = 0.95 * inch
    strip_y = PAGE_H - 1.05 * inch
    c.setFillColor(Color(0.05, 0.03, 0.02, alpha=0.55))
    c.rect(MARGIN, strip_y, PAGE_W - 2 * MARGIN, strip_h, fill=1, stroke=0)

    c.setFillColor(CREAM)
    c.setFont("Cinzel", size)
    c.drawString(MARGIN + 0.25 * inch, TITLE_BASELINE, title)

    c.setFillColor(CREAM_BR)
    c.setFont("Cormorant-It", 14)
    c.drawString(MARGIN + 0.30 * inch, TITLE_SCI_Y, sci_name)


# ---- Animal photo ------------------------------------------------------------

def draw_image_panel(c, img_path):
    pil = Image.open(img_path).convert("RGB")
    pw, ph = pil.size
    panel_ratio = IMG_W / IMG_H
    img_ratio = pw / ph
    if img_ratio > panel_ratio:
        new_w = int(ph * panel_ratio)
        left = (pw - new_w) // 2
        pil = pil.crop((left, 0, left + new_w, ph))
    else:
        new_h = int(pw / panel_ratio)
        top = (ph - new_h) // 2
        pil = pil.crop((0, top, pw, top + new_h))
    target_w = int(IMG_W / inch * 220)
    target_h = int(IMG_H / inch * 220)
    if pil.size[0] > target_w:
        pil = pil.resize((target_w, target_h), Image.LANCZOS)
    tmp = f"/tmp/{Path(img_path).stem}_v3_panel.jpg"
    pil.save(tmp, format="JPEG", quality=85, optimize=True)
    c.drawImage(tmp, IMG_X, IMG_Y, width=IMG_W, height=IMG_H,
                preserveAspectRatio=False, mask=None)
    # Thin gold hairline
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.rect(IMG_X, IMG_Y, IMG_W, IMG_H, fill=0, stroke=1)


def draw_mirror_panel(c):
    """Homo sapiens only. The photo region becomes a cutout for a real mirror.

    Renders a subtle silver gradient placeholder, corner crop marks for the
    fabricator, a centered guest prompt, and a small install note outside the
    cut line so the cutout edge stays clean.
    """
    # 1. Subtle vertical silver gradient tile so the placeholder reads as
    #    'mirror' in the PDF preview without being glossy or noisy when printed.
    tile_w, tile_h = 120, 160
    grad = Image.new("RGB", (tile_w, tile_h), (230, 230, 230))
    px = grad.load()
    for y in range(tile_h):
        # soft band: light top, slightly darker middle, light bottom
        t = y / (tile_h - 1)
        v = int(232 - 18 * (1 - abs(0.5 - t) * 2))
        for x in range(tile_w):
            px[x, y] = (v, v, v + 2 if v + 2 <= 255 else 255)
    tmp = "/tmp/mirror_placeholder.jpg"
    grad.save(tmp, format="JPEG", quality=85, optimize=True)
    c.drawImage(tmp, IMG_X, IMG_Y, width=IMG_W, height=IMG_H,
                preserveAspectRatio=False, mask=None)

    # 2. Thin gold hairline (same as photo totems)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.rect(IMG_X, IMG_Y, IMG_W, IMG_H, fill=0, stroke=1)

    # 3. Corner crop marks for the mirror cutout (outside the hairline)
    mark = 0.18 * inch
    off = 0.04 * inch
    c.setStrokeColor(HEADER_INK)
    c.setLineWidth(0.6)
    for (x, y, dx1, dy1, dx2, dy2) in [
        # bottom-left
        (IMG_X - off, IMG_Y - off,  mark, 0,  0, mark),
        # bottom-right
        (IMG_X + IMG_W + off, IMG_Y - off, -mark, 0,  0, mark),
        # top-left
        (IMG_X - off, IMG_Y + IMG_H + off,  mark, 0,  0, -mark),
        # top-right
        (IMG_X + IMG_W + off, IMG_Y + IMG_H + off, -mark, 0,  0, -mark),
    ]:
        c.line(x, y, x + dx1, y + dy1)
        c.line(x, y, x + dx2, y + dy2)

    # 4. Centered guest-facing prompt
    c.setFillColor(HEADER_INK)
    c.setFont("Cinzel", 20)
    prompt = "YOU ARE LOOKING AT ONE"
    pw = c.stringWidth(prompt, "Cinzel", 20)
    center_x = IMG_X + IMG_W / 2
    center_y = IMG_Y + IMG_H / 2
    c.drawString(center_x - pw / 2, center_y + 0.10 * inch, prompt)

    c.setFont("Cormorant-It", 13)
    sub = "Answer the eight questions about yourself."
    sw = c.stringWidth(sub, "Cormorant-It", 13)
    c.drawString(center_x - sw / 2, center_y - 0.18 * inch, sub)

    # 5. Install spec chip inside the placeholder (bottom margin), small
    #    fabricator-facing note. Will be removed when the mirror is cut in.
    c.setFillColor(HEADER_INK)
    c.setFont("Inter-Bold", 7)
    spec = "FABRICATION NOTE — cut along crop marks; mount acrylic mirror flush."
    sw_spec = c.stringWidth(spec, "Inter-Bold", 7)
    c.drawString(center_x - sw_spec / 2, IMG_Y + 0.14 * inch, spec)
    c.setFont("Inter", 6.5)
    dims = (f"Mirror size: {IMG_W / inch:.2f} in \u00d7 {IMG_H / inch:.2f} in  ·  "
            f"1/8 in acrylic mirror, rounded corners")
    sw_dims = c.stringWidth(dims, "Inter", 6.5)
    c.drawString(center_x - sw_dims / 2, IMG_Y + 0.06 * inch, dims)


# ---- 8 Q blocks on clean paper -----------------------------------------------

def _q_styles(body_size, heading_size, leading):
    head = ParagraphStyle(
        name="head", fontName="Inter-Bold", fontSize=heading_size,
        leading=heading_size + 1.5, textColor=HEADER_INK,
        spaceBefore=0, spaceAfter=1)
    body = ParagraphStyle(
        name="body", fontName="Inter", fontSize=body_size,
        leading=leading, textColor=INK, spaceBefore=0, spaceAfter=6)
    return head, body


def _build_story(k5, body_size, heading_size, leading):
    """Each Q is prefixed with a rust-accent number + period, bold Inter heading.
    Standardized format across all 18 species."""
    head, body = _q_styles(body_size, heading_size, leading)
    story = []
    ans = k5["answers"]
    for i in range(1, 9):
        q = ans[str(i)]["q"]
        a = ans[str(i)]["a"]
        # Rust accent number + period, then Q in bold ink
        story.append(Paragraph(
            f'<font color="#7A3416"><b>{i}.</b></font>  {q}', head))
        story.append(Paragraph(a, body))
    return story


def _story_fits(story, frame_w, frame_h):
    """True dry-run: use a real Frame on a throwaway canvas to see if anything
    overflows. This matches actual rendering exactly."""
    from reportlab.pdfgen.canvas import Canvas as _C
    dummy = _C("/tmp/_fit.pdf", pagesize=LETTER)
    f = Frame(0, 0, frame_w, frame_h,
              leftPadding=4, rightPadding=4, topPadding=2, bottomPadding=2,
              showBoundary=0)
    remaining = list(story)
    f.addFromList(remaining, dummy)
    return len(remaining) == 0


def draw_q_blocks(c, k5):
    """Pick the largest font size that fits all 8 Q blocks in the body frame.

    Uses a real Frame dry-run so what we measure matches what we render.
    """
    sizes = [
        (10.5, 11.5, 14.2),
        (10.0, 11.0, 13.6),
        (9.5,  10.5, 13.0),
        (9.0,  10.0, 12.4),
        (8.5,  9.5,  11.8),
        (8.0,  9.0,  11.2),
        (7.5,  8.5,  10.6),
        (7.0,  8.0,  10.0),
    ]
    frame_w = BODY_W
    frame_h = BODY_TOP - BODY_BOTTOM

    chosen = sizes[-1]
    for body_s, head_s, leading in sizes:
        story = _build_story(k5, body_s, head_s, leading)
        if _story_fits(story, frame_w, frame_h):
            chosen = (body_s, head_s, leading)
            break
    body_s, head_s, leading = chosen
    story = _build_story(k5, body_s, head_s, leading)
    f = Frame(BODY_X, BODY_BOTTOM, BODY_W, BODY_TOP - BODY_BOTTOM,
              leftPadding=4, rightPadding=4, topPadding=2, bottomPadding=2,
              showBoundary=0)
    f.addFromList(story, c)


# ---- Reality Door (its own boxed panel) --------------------------------------

def _build_rd_story(door, lbl_s, title_s, body_s, bullet_s):
    lbl = ParagraphStyle(
        name="rd_lbl", fontName="Inter-Bold", fontSize=lbl_s,
        leading=lbl_s + 1.5, textColor=HEADER_INK, spaceBefore=0, spaceAfter=0.5)
    title = ParagraphStyle(
        name="rd_title", fontName="Inter-Bold", fontSize=title_s,
        leading=title_s + 2, textColor=HEADER_INK, spaceBefore=0, spaceAfter=1.5)
    body = ParagraphStyle(
        name="rd_body", fontName="Inter", fontSize=body_s,
        leading=body_s + 2.2, textColor=INK, spaceBefore=0, spaceAfter=1)
    bullet = ParagraphStyle(
        name="rd_bul", fontName="Inter", fontSize=bullet_s,
        leading=bullet_s + 2, textColor=INK, spaceBefore=0, spaceAfter=0.3,
        leftIndent=10, bulletIndent=0)

    story = [
        Paragraph("WHY IS THIS ANIMAL HERE?", title),
        Paragraph(door["opening"], body),
    ]
    for line in door["habitat_lines"]:
        story.append(Paragraph(line, body))
    story.append(Paragraph("When its habitat shrinks:", lbl))
    for b in door["shrink_bullets"]:
        story.append(Paragraph(f"&#8226; {b}", bullet))
    story.append(Paragraph(BRIDGE_LINE, body))
    if door.get("life_park_note"):
        story.append(Paragraph(door["life_park_note"], body))
    return story


def draw_reality_door(c, door, tagline=None):
    """Draw the Reality Door as a visually distinct boxed panel on the paper.

    Auto-fits fonts so every line (including bridge line and LIFE Park note)
    is visible and photo-ready for an LLM to read.
    """
    # Panel
    c.setFillColor(CREAM_BR)
    c.setStrokeColor(HEADER_INK)
    c.setLineWidth(1.3)
    c.rect(RD_X, RD_BOTTOM, RD_W, RD_TOP - RD_BOTTOM, fill=1, stroke=1)

    # Font size ladder: (label, title, body, bullet)
    sizes = [
        (9.0, 11.0, 9.0,  8.5),
        (8.5, 10.5, 8.5,  8.0),
        (8.0, 10.0, 8.0,  7.5),
        (7.5,  9.5, 7.5,  7.0),
        (7.0,  9.0, 7.0,  6.5),
        (6.5,  8.5, 6.5,  6.0),
    ]
    inner_w = RD_W - 16  # leftPadding + rightPadding = 16
    inner_h = (RD_TOP - RD_BOTTOM) - 12  # topPadding + bottomPadding = 12

    chosen = sizes[-1]
    for s in sizes:
        story = _build_rd_story(door, *s)
        if _story_fits(story, inner_w, inner_h):
            chosen = s
            break
    story = _build_rd_story(door, *chosen)

    f = Frame(RD_X, RD_BOTTOM, RD_W, RD_TOP - RD_BOTTOM,
              leftPadding=8, rightPadding=8, topPadding=6, bottomPadding=6,
              showBoundary=0)
    f.addFromList(list(story), c)


# ---- QR code -----------------------------------------------------------------

def draw_qr(c, slug, common_name):
    url = f"https://life.park/ai/{slug}"
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    tmp = f"/tmp/qr_{slug}.png"
    img.save(tmp)

    # White cream chip behind the QR with a caption (large enough for full label)
    chip_w = QR_SIZE + 0.75 * inch
    chip_h = QR_SIZE + 0.65 * inch
    chip_x = QR_X - 0.38 * inch
    chip_y = QR_Y - 0.52 * inch

    c.setFillColor(CREAM_BR)
    c.setStrokeColor(HEADER_INK)
    c.setLineWidth(1.0)
    c.roundRect(chip_x, chip_y, chip_w, chip_h, 6, fill=1, stroke=1)

    c.drawImage(tmp, QR_X, QR_Y, width=QR_SIZE, height=QR_SIZE)

    c.setFillColor(HEADER_INK)
    c.setFont("Inter-Bold", 9.5)
    cap1 = "SCAN TO LEARN MORE"
    w1 = c.stringWidth(cap1, "Inter-Bold", 9.5)
    # Center caption vertically in the band between chip bottom and QR bottom.
    # Band height = QR_Y - chip_y = 0.52in. Font cap-height ~7pt = 0.097in.
    # Baseline at chip_y + (band - cap)/2 + cap ~= chip_y + 0.26in puts glyph center at band center.
    c.drawString(chip_x + (chip_w - w1) / 2, chip_y + 0.24 * inch, cap1)


# ---- Bottom band (Think About This + footer) ---------------------------------

def _wrap_text(c, text, font, size, max_w):
    words = text.split()
    if not words:
        return []
    lines, line = [], words[0]
    for w in words[1:]:
        test = line + " " + w
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            lines.append(line)
            line = w
    lines.append(line)
    return lines


def draw_bottom_band(c, think_q, common_name):
    """Compact dark overlay for Think About This + footer, sitting on bottom bark.

    Leaves room on the right for the QR chip.
    """
    band_x = MARGIN
    band_w = PAGE_W - 2 * MARGIN - QR_SIZE - 0.35 * inch  # leave QR space
    band_top = LOWER_TOP
    band_bottom = 0.25 * inch

    c.setFillColor(Color(0.05, 0.03, 0.02, alpha=0.72))
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.7)
    c.roundRect(band_x, band_bottom, band_w, band_top - band_bottom,
                6, fill=1, stroke=1)

    y = band_top - 0.20 * inch

    # "Think About This" label
    c.setFillColor(CREAM_BR)
    c.setFont("Inter-Bold", 10)
    label = "THINK ABOUT THIS"
    lw = c.stringWidth(label, "Inter-Bold", 10)
    c.drawString(band_x + (band_w - lw) / 2, y, label)
    y -= 0.22 * inch

    # Reflection question (can wrap)
    c.setFont("Cormorant-It", 12)
    lines = _wrap_text(c, think_q, "Cormorant-It", 12, band_w - 0.35 * inch)
    for line in lines:
        lw = c.stringWidth(line, "Cormorant-It", 12)
        c.drawString(band_x + (band_w - lw) / 2, y, line)
        y -= 0.19 * inch

    # Thin gold rule
    y -= 0.05 * inch
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.line(band_x + 0.4 * inch, y, band_x + band_w - 0.4 * inch, y)
    y -= 0.16 * inch

    # Footer (compact, smaller per user request)
    c.setFillColor(CREAM_BR)
    c.setFont("Cormorant-It", 10)
    line1 = "What a living thing can sense becomes its reality."
    line2 = "Environment shapes design."
    w1 = c.stringWidth(line1, "Cormorant-It", 10)
    c.drawString(band_x + (band_w - w1) / 2, y, line1)
    y -= 0.15 * inch
    w2 = c.stringWidth(line2, "Cormorant-It", 10)
    c.drawString(band_x + (band_w - w2) / 2, y, line2)


# ---- Build one totem ---------------------------------------------------------

def build_totem(slug, out_path):
    k5, sp = load_data(slug)
    title = sp["common_name"]
    sci   = sp["scientific_name"]
    tagline = k5.get("tagline", "")
    img = IMG_DIR / f"photo_{slug}.png"
    if not img.exists():
        img = IMG_DIR / f"totem_img_{slug}.png"
    think = THINK_ABOUT_THIS[slug]
    door = get_reality_door(slug)

    c = canvas.Canvas(str(out_path), pagesize=LETTER)
    c.setTitle(f"LIFE Totem — {title}")
    c.setAuthor("Perplexity Computer")

    draw_background(c)
    draw_title(c, title, sci)
    if slug == "homo-sapiens":
        draw_mirror_panel(c)
    else:
        draw_image_panel(c, img)
    draw_q_blocks(c, k5)
    draw_reality_door(c, door, tagline=tagline)
    draw_qr(c, slug, title)
    draw_bottom_band(c, think, title)

    c.showPage()
    c.save()
    return out_path


def main():
    slugs = sorted(p.stem for p in K5_DIR.glob("*.json"))
    ok, fail = 0, 0
    for slug in slugs:
        out = OUT_DIR / f"TOTEM_{slug}.pdf"
        try:
            build_totem(slug, out)
            print(f"  ✓ {slug}")
            ok += 1
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
            fail += 1
    print(f"\ndone · ok {ok} · fail {fail}")


if __name__ == "__main__":
    main()
