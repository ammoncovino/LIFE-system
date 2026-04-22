"""
Generic Student Totem builder — data-driven.

Reads /home/user/workspace/LIFE_k5_locked/{slug}.json + species photo,
writes /home/user/workspace/LIFE_system/student_totems/STUDENT_{slug}.pdf.

Preserves EXACT layout and styling approved for the lemur pattern:
- LETTER portrait
- Title (DMSans-Bold 22, centered)
- Tagline (Inter-SemiBold 12, muted, centered)
- Photo backdrop (2.3in tall, LIGHT fill, photo inset)
- 2×4 grid of numbered Q&A cells
- Closing band (ACCENT, navy label + ink prompt)
- Footer (two LOCKED lines + hairline)
"""
import os, json, sys, glob
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# ---- Fonts ----
FONT_DIR = "/tmp/fonts"
pdfmetrics.registerFont(TTFont("DMSans-Bold", f"{FONT_DIR}/DMSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter", f"{FONT_DIR}/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", f"{FONT_DIR}/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", f"{FONT_DIR}/Inter-SemiBold.ttf"))

# ---- Palette (LOCKED) ----
NAVY   = HexColor("#2C3481")
INK    = HexColor("#1A1A1A")
MUTED  = HexColor("#555555")
LIGHT  = HexColor("#F5F5F2")
RULE   = HexColor("#D4D1CA")
ACCENT = HexColor("#EEF1F8")
WHITE  = HexColor("#FFFFFF")

# Slug -> photo filename in LIFE_system/species_photos
PHOTO_MAP = {
    "alpaca":                        "alpaca.jpg",
    "argentine-tegu":                "tegu.jpg",
    "bennetts-wallaby":              "wallaby.jpg",
    "black-and-white-ruffed-lemur":  "black_and_white_ruffed_lemur.jpg",
    "capybara":                      "capybara.jpg",
    "geoffroys-spider-monkey":       "spider_monkey.jpg",
    "kinkajou":                      "kinkajou.jpg",
    "linnes-two-toed-sloth":         "two_toed_sloth.jpg",
    "monkey-tailed-skink":           "monkey_tailed_skink.jpg",
    "nine-banded-armadillo":         "armadillo.jpg",
    "patagonian-mara":               "patagonian_mara.jpg",
    "prehensile-tailed-porcupine":   "porcupine.jpg",
    "rabbit":                        "rabbit.jpg",
    "red-ruffed-lemur":              "red_ruffed_lemur.jpg",
    "ring-tailed-lemur":             "ring_tailed_lemur.jpg",
    "sailfin-dragon":                "sailfin_dragon.jpg",
    "sulcata-tortoise":              "sulcata_tortoise.jpg",
    "toco-toucan":                   "toco_toucan.jpg",
}

PAGE_W, PAGE_H = letter
MARGIN = 0.6*inch

# ---------------- helpers ----------------
def build_student_totem(data_path, out_path, photo_path):
    with open(data_path) as f:
        data = json.load(f)

    species_title = data["species"].upper()
    tagline = data["tagline"]
    answers = data["answers"]
    closing = data["closing_prompt"]
    footer = data["footer"]

    # Closing is "LOOK AT THE ANIMAL: What do you see it doing right now?"
    if ":" in closing:
        label_part, text_part = closing.split(":", 1)
        closing_label = label_part.strip() + ":"
        closing_text = text_part.strip()
    else:
        closing_label = "LOOK AT THE ANIMAL:"
        closing_text = closing

    questions = [(answers[str(i)]["q"], answers[str(i)]["a"]) for i in range(1, 9)]

    c = canvas.Canvas(out_path, pagesize=letter)
    c.setTitle(f"{data['species']} — Student Totem (LOCKED 8-Question Spine)")
    c.setAuthor("Perplexity Computer")

    def txt(x, y, s, font="Inter", size=10, color=INK, align="left"):
        c.setFillColor(color); c.setFont(font, size)
        if align == "center": c.drawCentredString(x, y, s)
        elif align == "right": c.drawRightString(x, y, s)
        else: c.drawString(x, y, s)

    def para(text, x, y, w, h, font="Inter", size=10, leading=13, color=INK, align=TA_LEFT):
        style = ParagraphStyle(name="p", fontName=font, fontSize=size,
                               leading=leading, textColor=color, alignment=align)
        p = Paragraph(text, style)
        f = Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        f.addFromList([p], c)

    # TITLE
    title_y = PAGE_H - 0.75*inch
    # Auto-scale title down if very long so it fits on one line
    title_size = 22
    # narrow check — species names up to ~34 chars fit at 22pt. Longer, shrink.
    if len(species_title) > 28:
        title_size = 19
    if len(species_title) > 34:
        title_size = 17
    txt(PAGE_W/2, title_y, species_title,
        font="DMSans-Bold", size=title_size, color=INK, align="center")

    # TAGLINE
    txt(PAGE_W/2, title_y - 0.30*inch, tagline,
        font="Inter-SemiBold", size=12, color=MUTED, align="center")

    # PHOTO
    photo_top_y = title_y - 0.55*inch
    photo_h     = 2.3*inch
    photo_w     = PAGE_W - 2*MARGIN
    photo_x     = MARGIN
    photo_y     = photo_top_y - photo_h

    c.setFillColor(LIGHT)
    c.roundRect(photo_x, photo_y, photo_w, photo_h, 6, fill=1, stroke=0)

    inset = 0.08*inch
    try:
        from reportlab.lib.utils import ImageReader
        img = ImageReader(photo_path)
        iw, ih = img.getSize()
        target_w = photo_w - 2*inset
        target_h = photo_h - 2*inset
        scale = min(target_w/iw, target_h/ih)
        dw, dh = iw*scale, ih*scale
        dx = photo_x + (photo_w - dw)/2
        dy = photo_y + (photo_h - dh)/2
        c.drawImage(img, dx, dy, width=dw, height=dh,
                    preserveAspectRatio=True, mask='auto')
    except Exception as e:
        txt(PAGE_W/2, photo_y + photo_h/2, f"[photo missing: {e}]",
            font="Inter", size=9, color=MUTED, align="center")

    # QUESTIONS grid
    q_top      = photo_y - 0.30*inch
    q_bottom   = 1.55*inch
    q_area_h   = q_top - q_bottom
    GAP_X      = 0.22*inch
    ROWS, COLS = 4, 2
    col_w = (PAGE_W - 2*MARGIN - GAP_X) / COLS
    row_h = q_area_h / ROWS

    for i, (q, a) in enumerate(questions):
        row = i // COLS
        col = i %  COLS
        cell_x = MARGIN + col*(col_w + GAP_X)
        cell_y = q_top - (row+1)*row_h

        cir_x = cell_x + 0.18*inch
        cir_y = cell_y + row_h - 0.22*inch
        c.setFillColor(NAVY)
        c.circle(cir_x, cir_y, 0.14*inch, fill=1, stroke=0)
        txt(cir_x, cir_y - 0.045*inch, str(i+1),
            font="Inter-Bold", size=10, color=WHITE, align="center")

        q_text_x = cir_x + 0.22*inch
        q_frame_h = 0.48*inch
        q_frame_y = cir_y - 0.40*inch
        para(q,
             q_text_x, q_frame_y,
             col_w - 0.50*inch, q_frame_h,
             font="Inter-Bold", size=10.5, leading=12.5, color=INK)

        ans_top_y = q_frame_y - 0.05*inch
        ans_h     = ans_top_y - (cell_y + 0.05*inch)
        para(a,
             cell_x + 0.18*inch, cell_y + 0.05*inch,
             col_w - 0.30*inch, ans_h,
             font="Inter", size=10, leading=12.5, color=INK)

    # CLOSING BAND
    cb_h = 0.70*inch
    cb_y = 0.80*inch
    c.setFillColor(ACCENT)
    c.roundRect(MARGIN, cb_y, PAGE_W - 2*MARGIN, cb_h, 6, fill=1, stroke=0)
    txt(PAGE_W/2, cb_y + cb_h - 0.28*inch, closing_label,
        font="Inter-Bold", size=11, color=NAVY, align="center")
    txt(PAGE_W/2, cb_y + 0.18*inch, closing_text,
        font="DMSans-Bold", size=14, color=INK, align="center")

    # FOOTER
    txt(PAGE_W/2, 0.50*inch, footer[0],
        font="Inter-SemiBold", size=10, color=MUTED, align="center")
    txt(PAGE_W/2, 0.32*inch, footer[1],
        font="Inter-SemiBold", size=10, color=MUTED, align="center")
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(MARGIN, 0.68*inch, PAGE_W - MARGIN, 0.68*inch)

    c.showPage()
    c.save()

def main():
    src_dir = "/home/user/workspace/LIFE_k5_locked"
    out_dir = "/home/user/workspace/LIFE_system/student_totems"
    photo_dir = "/home/user/workspace/LIFE_system/species_photos"
    os.makedirs(out_dir, exist_ok=True)

    wrote = []
    for json_file in sorted(glob.glob(os.path.join(src_dir, "*.json"))):
        slug = os.path.splitext(os.path.basename(json_file))[0]
        photo_file = PHOTO_MAP.get(slug)
        if not photo_file:
            print(f"SKIP (no photo map): {slug}")
            continue
        photo_path = os.path.join(photo_dir, photo_file)
        if not os.path.exists(photo_path):
            print(f"SKIP (photo missing on disk): {slug} — expected {photo_path}")
            continue
        out_path = os.path.join(out_dir, f"STUDENT_{slug}.pdf")
        build_student_totem(json_file, out_path, photo_path)
        wrote.append(out_path)
        print(f"WROTE {out_path}  ({os.path.getsize(out_path):,} bytes)")
    print()
    print(f"Built {len(wrote)} Student Totems.")

if __name__ == "__main__":
    main()
