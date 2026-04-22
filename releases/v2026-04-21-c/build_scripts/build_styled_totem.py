"""Build 'Styled' Student Totems for all 18 species.

Layout (LETTER portrait, 8.5 x 11 in):
  - Full-page parchment background
  - Top 'wood' band:  Title (Cinzel Bold, cream)  +  Scientific name (Cormorant Italic, cream)
  - Body grid:
      Left column  (~47% width): 8 Q blocks stacked, body text on parchment
      Right column (~50% width): full-bleed painterly animal image
  - 'Think About This' band (wood): per-species reflection question, cream italic
  - Footer band (wood):   'What a living thing can sense becomes its reality.'
                          'Environment shapes design.'
"""

import io
import json
import os
from pathlib import Path
from PIL import Image
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame

from think_about_this import THINK_ABOUT_THIS

# ---- Config ------------------------------------------------------------------
WORKSPACE   = Path("/home/user/workspace")
K5_DIR      = WORKSPACE / "LIFE_k5_locked"
MASTER_JSON = WORKSPACE / "LIFE_totem_content_18.json"
IMG_DIR     = WORKSPACE
PARCHMENT   = WORKSPACE / "bg_parchment_clean.png"
WOOD        = WORKSPACE / "bg_wood_band.png"
OUT_DIR     = WORKSPACE / "LIFE_styled_totems"
OUT_DIR.mkdir(exist_ok=True)

# Color
CREAM       = HexColor("#F2E3C4")    # title cream
CREAM_SOFT  = HexColor("#E9D9B6")
INK         = HexColor("#241F18")    # body text (dark warm brown)
INK_SOFT    = HexColor("#3A2F21")
HEADER_INK  = HexColor("#2A1E10")    # question headings
ACCENT      = HexColor("#7A3E1D")    # warm rust
RULE        = HexColor("#B8A676")    # aged gold

# Fonts
pdfmetrics.registerFont(TTFont("Cinzel",       "/tmp/fonts/Cinzel[wght].ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-It", "/tmp/fonts/CormorantGaramond-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Cormorant-Bd", "/tmp/fonts/CormorantGaramond-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter",        "/tmp/fonts/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bd",     "/tmp/fonts/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-It",     "/tmp/fonts/InterVariable-Italic.ttf"))

# ---- Locked 8-question spine -------------------------------------------------
LOCKED_QUESTIONS = [
    "What can it see, hear, or feel?",
    "Where does it live \u2014 and why?",
    "How does it send messages?",
    "What does it do when something changes?",
    "How does it learn?",
    "How does it have babies?",
    "What are its limits?",
    "What does this teach us?",
]

FOOTER_LINES = [
    "What a living thing can sense becomes its reality.",
    "Environment shapes design.",
]

# ---- Layout ------------------------------------------------------------------
PAGE_W, PAGE_H   = LETTER
MARGIN           = 0.30 * inch

TITLE_BAND_H     = 1.10 * inch
THINK_BAND_H     = 0.95 * inch
FOOTER_BAND_H    = 0.65 * inch

BODY_TOP         = PAGE_H - TITLE_BAND_H
BODY_BOTTOM      = THINK_BAND_H + FOOTER_BAND_H
BODY_H           = BODY_TOP - BODY_BOTTOM

# Left text column and right image column
LEFT_X           = MARGIN
LEFT_W           = 4.40 * inch
GUTTER           = 0.15 * inch
IMG_X            = LEFT_X + LEFT_W + GUTTER
IMG_W            = PAGE_W - IMG_X - MARGIN
IMG_Y            = BODY_BOTTOM + 0.05 * inch
IMG_H            = BODY_H - 0.10 * inch

# ---- Styles ------------------------------------------------------------------
Q_HEAD = ParagraphStyle(
    "qhead",
    fontName="Cormorant-Bd",
    fontSize=13,
    leading=14,
    textColor=HEADER_INK,
    spaceAfter=1,
)

Q_BODY = ParagraphStyle(
    "qbody",
    fontName="Inter",
    fontSize=9,
    leading=11.5,
    textColor=INK,
    spaceAfter=0,
)

# ---- Helpers -----------------------------------------------------------------
def load_data(slug):
    """Load K-5 JSON + master bullets for a species.

    Returns a dict with flat q1..q8 keys (answers only) plus common_name,
    scientific_name, tagline.
    """
    raw = json.loads((K5_DIR / f"{slug}.json").read_text())
    master = json.loads(MASTER_JSON.read_text())
    sp = next(s for s in master["species"] if s["slug"] == slug)
    k5 = {
        "common_name": raw.get("species", sp["common_name"]),
        "tagline": raw.get("tagline", ""),
    }
    for i in range(1, 9):
        k5[f"q{i}"] = raw["answers"][str(i)]["a"].strip()
    return k5, sp


# Cache downscaled textures globally to speed up + shrink PDFs
_BG_CACHE = {}


def _get_cached_texture(path, max_dim=1400, quality=78):
    """Downscale texture once and write as temp JPEG file.

    ReportLab embeds JPEG files on disk directly (no re-encoding), which
    keeps PDFs small.  Passing a BytesIO causes ReportLab to decode and
    re-embed raw pixels, bloating the output.
    """
    if path in _BG_CACHE:
        return _BG_CACHE[path]
    pil = Image.open(path).convert("RGB")
    if max(pil.size) > max_dim:
        pil.thumbnail((max_dim, max_dim), Image.LANCZOS)
    tmp = Path("/tmp") / (Path(path).stem + f"_opt_{max_dim}_{quality}.jpg")
    pil.save(str(tmp), format="JPEG", quality=quality, optimize=True)
    _BG_CACHE[path] = str(tmp)
    return str(tmp)


def draw_background(c):
    """Full-page parchment."""
    c.drawImage(_get_cached_texture(str(PARCHMENT), max_dim=1400, quality=80),
                0, 0, width=PAGE_W, height=PAGE_H,
                preserveAspectRatio=False, mask='auto')


def draw_wood_band(c, y, h):
    """Draw a dark wood band across the page width at y with height h."""
    c.drawImage(_get_cached_texture(str(WOOD), max_dim=1600, quality=78),
                0, y, width=PAGE_W, height=h,
                preserveAspectRatio=False, mask='auto')
    # Thin gold rule top & bottom
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    c.line(MARGIN, y + h, PAGE_W - MARGIN, y + h)


def fit_title_font(c, text, max_w, start=34, min_size=20):
    """Return the largest font size at which the title fits max_w."""
    size = start
    while size > min_size:
        w = c.stringWidth(text, "Cinzel", size)
        if w <= max_w:
            return size
        size -= 1
    return min_size


def draw_title_band(c, title_text, sci_name):
    y = PAGE_H - TITLE_BAND_H
    draw_wood_band(c, y, TITLE_BAND_H)

    # Title
    title = title_text.upper()
    max_w = PAGE_W - 2 * MARGIN - 0.2 * inch
    size  = fit_title_font(c, title, max_w, start=34, min_size=22)
    c.setFillColor(CREAM)
    c.setFont("Cinzel", size)
    # Baseline near top half of band
    ty = y + TITLE_BAND_H - 0.50 * inch
    c.drawString(MARGIN + 0.05 * inch, ty, title)

    # Scientific name (italic, below title)
    c.setFont("Cormorant-It", 14)
    c.setFillColor(CREAM_SOFT)
    c.drawString(MARGIN + 0.10 * inch, y + 0.22 * inch, sci_name)


def draw_image_panel(c, img_path):
    """Draw a soft-edged panel with the painterly illustration.

    The image is cropped to panel aspect, downsized to ~300dpi for the
    panel size, re-encoded as quality-82 JPEG, then embedded.  This keeps
    each PDF <2 MB.
    """
    # Outer warm frame
    c.setFillColor(HexColor("#6B4226"))
    c.roundRect(IMG_X - 2, IMG_Y - 2, IMG_W + 4, IMG_H + 4, 6, fill=1, stroke=0)
    # Crop to panel aspect
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
    # Downsize to panel-appropriate pixel count (~220 dpi)
    target_w = int(IMG_W / inch * 220)
    target_h = int(IMG_H / inch * 220)
    if pil.size[0] > target_w:
        pil = pil.resize((target_w, target_h), Image.LANCZOS)
    # Write to temp JPEG file so ReportLab embeds it verbatim (small).
    tmp = Path("/tmp") / (Path(img_path).stem + "_panel.jpg")
    pil.save(str(tmp), format="JPEG", quality=82, optimize=True)
    c.drawImage(str(tmp), IMG_X, IMG_Y, width=IMG_W, height=IMG_H,
                preserveAspectRatio=False, mask=None)

    # Gold hairline border
    c.setStrokeColor(RULE)
    c.setLineWidth(0.7)
    c.rect(IMG_X, IMG_Y, IMG_W, IMG_H, fill=0, stroke=1)


def draw_q_blocks(c, k5):
    """Draw 8 question blocks in a single left column, flowing frame."""
    # Compute per-Q available height
    top_y    = BODY_TOP - 0.10 * inch
    bottom_y = BODY_BOTTOM + 0.05 * inch
    col_h    = top_y - bottom_y

    story = []
    for qidx in range(1, 9):
        q_text = LOCKED_QUESTIONS[qidx - 1]
        a_text = k5.get(f"q{qidx}", "").strip()
        story.append(Paragraph(q_text, Q_HEAD))
        story.append(Paragraph(a_text, Q_BODY))
        # small spacer paragraph
        story.append(Paragraph("&nbsp;", ParagraphStyle(
            "spacer", fontName="Inter", fontSize=3, leading=3)))

    frame = Frame(
        LEFT_X, bottom_y, LEFT_W, col_h,
        leftPadding=2, rightPadding=2, topPadding=2, bottomPadding=2,
        showBoundary=0,
    )
    frame.addFromList(story, c)
    if story:
        # If anything overflowed, shrink body size and retry once
        return False
    return True


def _measure_story(story, width, height):
    """Return True if the entire story fits within (width, height).
    Uses the flowable wrap() API to estimate heights without drawing.
    """
    used = 0.0
    for flow in story:
        w, h = flow.wrap(width, height - used)
        used += h
        if used > height:
            return False
    return True


def draw_q_blocks_autofit(c, k5):
    """Render 8 Q blocks in left column; auto-shrink text until it fits.

    We measure first (no drawing) and only commit to a successful size.
    """
    top_y    = BODY_TOP - 0.10 * inch
    bottom_y = BODY_BOTTOM + 0.05 * inch
    col_h    = top_y - bottom_y
    col_w    = LEFT_W - 4  # account for frame padding

    sizes = [
        (10.0, 12.4, 13.5, 4),
        (9.5,  11.8, 13.0, 4),
        (9.0,  11.2, 12.6, 3),
        (8.6,  10.7, 12.2, 3),
        (8.2,  10.2, 11.8, 3),
        (7.8,  9.7,  11.4, 2),
        (7.5,  9.3,  11.0, 2),
        (7.2,  9.0,  10.7, 2),
    ]

    chosen = None
    for body_size, lead, head_size, gap in sizes:
        head_style = ParagraphStyle(
            "qh", fontName="Cormorant-Bd", fontSize=head_size,
            leading=head_size + 1, textColor=HEADER_INK, spaceAfter=1,
        )
        body_style = ParagraphStyle(
            "qb", fontName="Inter", fontSize=body_size,
            leading=lead, textColor=INK, spaceAfter=gap,
        )
        story = []
        for qidx in range(1, 9):
            story.append(Paragraph(LOCKED_QUESTIONS[qidx - 1], head_style))
            story.append(Paragraph(k5.get(f"q{qidx}", "").strip(), body_style))
        if _measure_story(story, col_w, col_h):
            chosen = (story, head_style, body_style)
            break

    if chosen is None:
        # Last resort: use the smallest setting even if it overflows slightly
        body_size, lead, head_size, gap = sizes[-1]
        head_style = ParagraphStyle(
            "qh", fontName="Cormorant-Bd", fontSize=head_size,
            leading=head_size + 1, textColor=HEADER_INK, spaceAfter=1,
        )
        body_style = ParagraphStyle(
            "qb", fontName="Inter", fontSize=body_size,
            leading=lead, textColor=INK, spaceAfter=gap,
        )
        story = []
        for qidx in range(1, 9):
            story.append(Paragraph(LOCKED_QUESTIONS[qidx - 1], head_style))
            story.append(Paragraph(k5.get(f"q{qidx}", "").strip(), body_style))
        chosen = (story, head_style, body_style)

    story, _, _ = chosen
    frame = Frame(LEFT_X, bottom_y, LEFT_W, col_h,
                  leftPadding=2, rightPadding=2,
                  topPadding=2, bottomPadding=2, showBoundary=0)
    frame.addFromList(list(story), c)


def draw_think_band(c, question):
    y = FOOTER_BAND_H
    draw_wood_band(c, y, THINK_BAND_H)
    # Label
    c.setFont("Cormorant-Bd", 17)
    c.setFillColor(CREAM)
    label = "Think About This"
    lw = c.stringWidth(label, "Cormorant-Bd", 17)
    c.drawString((PAGE_W - lw) / 2, y + THINK_BAND_H - 0.35 * inch, label)
    # Small flanking rules
    rule_y = y + THINK_BAND_H - 0.30 * inch
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.line(MARGIN + 0.3 * inch, rule_y, (PAGE_W - lw) / 2 - 0.15 * inch, rule_y)
    c.line((PAGE_W + lw) / 2 + 0.15 * inch, rule_y, PAGE_W - MARGIN - 0.3 * inch, rule_y)

    # Question paragraph (centered)
    q_style = ParagraphStyle(
        "thq",
        fontName="Cormorant-It", fontSize=14, leading=17,
        textColor=CREAM, alignment=1,  # center
    )
    f = Frame(MARGIN + 0.4 * inch, y + 0.05 * inch,
              PAGE_W - 2 * MARGIN - 0.8 * inch, THINK_BAND_H - 0.55 * inch,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
              showBoundary=0)
    f.addFromList([Paragraph(question, q_style)], c)

    # LIFE locked closing (small, below the reflection): "LOOK AT THE ANIMAL..."
    # User chose 'Think About This' *instead of* the locked closing — we honor
    # that by not duplicating. The LIFE footer lines below handle the compliance.


def draw_footer_band(c):
    y = 0
    draw_wood_band(c, y, FOOTER_BAND_H)
    c.setFillColor(CREAM)
    c.setFont("Cormorant-It", 11)
    line1, line2 = FOOTER_LINES
    lw1 = c.stringWidth(line1, "Cormorant-It", 11)
    lw2 = c.stringWidth(line2, "Cormorant-It", 11)
    c.drawString((PAGE_W - lw1) / 2, y + 0.36 * inch, line1)
    c.drawString((PAGE_W - lw2) / 2, y + 0.14 * inch, line2)


# ---- Build one totem ---------------------------------------------------------

def build_totem(slug, out_path):
    k5, sp = load_data(slug)
    title = sp["common_name"]
    sci   = sp["scientific_name"]
    img   = IMG_DIR / f"totem_img_{slug}.png"
    think = THINK_ABOUT_THIS[slug]

    c = canvas.Canvas(str(out_path), pagesize=LETTER)
    c.setTitle(f"LIFE Totem \u2014 {title}")
    c.setAuthor("Perplexity Computer")

    draw_background(c)
    draw_title_band(c, title, sci)
    draw_image_panel(c, img)
    draw_think_band(c, think)
    draw_footer_band(c)
    # Draw text LAST so it lives above the parchment but beneath nothing
    draw_q_blocks_autofit(c, k5)

    c.showPage()
    c.save()
    return out_path


def main():
    slugs = sorted(p.stem for p in K5_DIR.glob("*.json"))
    print(f"Building {len(slugs)} styled totems \u2192 {OUT_DIR}")
    for slug in slugs:
        out = OUT_DIR / f"STYLED_{slug}.pdf"
        try:
            build_totem(slug, out)
            print(f"  \u2713 {slug}")
        except Exception as e:
            print(f"  \u2717 {slug}: {e}")


if __name__ == "__main__":
    main()
