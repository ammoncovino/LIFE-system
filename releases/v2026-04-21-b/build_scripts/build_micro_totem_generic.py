"""
Generic Micro Totem builder — data-driven.

Reads /home/user/workspace/LIFE_k5_locked/{slug}.json + species photo,
writes /home/user/workspace/LIFE_system/student_totems/MICRO_{slug}.pdf.

Preserves EXACT layout and styling approved for the lemur pattern:
- LETTER page, 3.5 × 2.0 in business-card size, front on top, back on bottom
- Front: photo (cover-fit, clipped rounded), MEET banner, QR, TAKE-IT-HOME
- Back: navy title strip, tagline, pocket 5-Q/A (Q1,Q2,Q3,Q5,Q8 wording identical),
        ACCENT closing band, two-line locked footer with per-species URL
- Page headers + crop marks
"""
import os, json, glob
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import registerFontFamily

FONT_DIR = "/tmp/fonts"
pdfmetrics.registerFont(TTFont("DMSans-Bold", f"{FONT_DIR}/DMSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter", f"{FONT_DIR}/Inter-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Inter-Bold", f"{FONT_DIR}/Inter-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Inter-SemiBold", f"{FONT_DIR}/Inter-SemiBold.ttf"))
registerFontFamily("Inter", normal="Inter", bold="Inter-Bold",
                   italic="Inter", boldItalic="Inter-Bold")

NAVY   = HexColor("#2C3481")
INK    = HexColor("#1A1A1A")
MUTED  = HexColor("#555555")
LIGHT  = HexColor("#F5F5F2")
RULE   = HexColor("#D4D1CA")
ACCENT = HexColor("#EEF1F8")
WHITE  = HexColor("#FFFFFF")

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

# Short URL-friendly nickname for each species in the hosted URL
URL_MAP = {
    "alpaca":                        "alpaca",
    "argentine-tegu":                "tegu",
    "bennetts-wallaby":              "wallaby",
    "black-and-white-ruffed-lemur":  "lemur",
    "capybara":                      "capybara",
    "geoffroys-spider-monkey":       "spider-monkey",
    "kinkajou":                      "kinkajou",
    "linnes-two-toed-sloth":         "sloth",
    "monkey-tailed-skink":           "skink",
    "nine-banded-armadillo":         "armadillo",
    "patagonian-mara":               "mara",
    "prehensile-tailed-porcupine":   "porcupine",
    "rabbit":                        "rabbit",
    "red-ruffed-lemur":              "red-lemur",
    "ring-tailed-lemur":             "ring-lemur",
    "sailfin-dragon":                "sailfin",
    "sulcata-tortoise":              "tortoise",
    "toco-toucan":                   "toucan",
}

# "MEET" banner nickname (human-readable)
def meet_banner(data):
    # Use a short, title-cased common name
    nick = data["species"]
    # Compact: if contains "'s" or very long, shorten
    short = {
        "Black-and-White Ruffed Lemur": "THE LEMUR",
        "Red Ruffed Lemur":             "THE RED LEMUR",
        "Ring-Tailed Lemur":            "THE RING-TAILED LEMUR",
        "Capybara":                     "THE CAPYBARA",
        "Rabbit":                       "THE RABBIT",
        "Patagonian Mara":              "THE MARA",
        "Bennett's Wallaby":            "THE WALLABY",
        "Alpaca":                       "THE ALPACA",
        "Linnaeus's Two-Toed Sloth":    "THE SLOTH",
        "Monkey-Tailed Skink":          "THE SKINK",
        "Geoffroy's Spider Monkey":     "THE SPIDER MONKEY",
        "Kinkajou":                     "THE KINKAJOU",
        "Prehensile-Tailed Porcupine":  "THE PORCUPINE",
        "Nine-Banded Armadillo":        "THE ARMADILLO",
        "Sailfin Dragon":               "THE SAILFIN DRAGON",
        "Sulcata Tortoise":             "THE TORTOISE",
        "Toco Toucan":                  "THE TOUCAN",
        "Argentine Black-and-White Tegu": "THE TEGU",
    }.get(nick, "THE ANIMAL")
    return f"MEET {short}"

CARD_W = 3.5*inch
CARD_H = 2.0*inch
PAGE_W, PAGE_H = letter

def build_micro_totem(data_path, out_path, photo_path):
    with open(data_path) as f:
        data = json.load(f)

    slug = data["slug"]
    species_title = data["species"].upper()
    tagline = data["tagline"]
    url_nick = URL_MAP[slug]
    qr_url = f"https://life.family-fun-group.com/{url_nick}"

    # Pocket 5 of 8 — identical wording, positions from JSON
    pocket_idx = data["micro_pocket_questions"]  # [1,2,3,5,8]
    pocket_qa = [(data["answers"][str(i)]["q"], data["answers"][str(i)]["a"])
                 for i in pocket_idx]

    c = canvas.Canvas(out_path, pagesize=letter)
    c.setTitle(f"Micro Totem — {species_title}")
    c.setAuthor("Perplexity Computer")

    def txt(x, y, s, font="Inter", size=10, color=INK, align="left"):
        c.setFillColor(color); c.setFont(font, size)
        if align == "center": c.drawCentredString(x, y, s)
        elif align == "right": c.drawRightString(x, y, s)
        else: c.drawString(x, y, s)

    def para(text, x, y, w, h, font="Inter", size=10, leading=12.5, color=INK, align=TA_LEFT):
        style = ParagraphStyle(name="p", fontName=font, fontSize=size,
                               leading=leading, textColor=color, alignment=align)
        p = Paragraph(text, style)
        f = Frame(x, y, w, h, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
        f.addFromList([p], c)

    def crop_marks(cx, cy, w, h):
        c.setStrokeColor(HexColor("#888888")); c.setLineWidth(0.3)
        ml = 0.12*inch
        off = 0.05*inch
        for (x, y) in [(cx, cy), (cx+w, cy), (cx, cy+h), (cx+w, cy+h)]:
            c.line(x, y - (ml + off) if (y == cy) else y + off,
                   x, y - off        if (y == cy) else y + ml + off)
            c.line(x - (ml + off) if (x == cx) else x + off, y,
                   x - off        if (x == cx) else x + ml + off, y)

    # QR code
    qr = qrcode.QRCode(version=None,
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       box_size=12, border=2)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#2C3481", back_color="white")
    qr_path = f"/tmp/micro_qr_{slug}.png"
    qr_img.save(qr_path)

    front_x = (PAGE_W - CARD_W) / 2
    front_y = PAGE_H - 1.0*inch - CARD_H
    back_x  = front_x
    back_y  = 1.0*inch

    # ---------- FRONT ----------
    c.setStrokeColor(RULE); c.setLineWidth(0.6)
    c.roundRect(front_x, front_y, CARD_W, CARD_H, 6, fill=0, stroke=1)

    photo_w = 1.55*inch
    photo_h = CARD_H - 0.24*inch
    photo_x = front_x + 0.12*inch
    photo_y = front_y + 0.12*inch
    c.saveState()
    path = c.beginPath()
    path.roundRect(photo_x, photo_y, photo_w, photo_h, 4)
    c.clipPath(path, stroke=0, fill=0)
    try:
        img = ImageReader(photo_path)
        iw, ih = img.getSize()
        scale = max(photo_w/iw, photo_h/ih)
        dw, dh = iw*scale, ih*scale
        dx = photo_x + (photo_w - dw)/2
        dy = photo_y + (photo_h - dh)/2
        c.drawImage(img, dx, dy, width=dw, height=dh,
                    preserveAspectRatio=False, mask='auto')
    except Exception as e:
        c.setFillColor(LIGHT); c.rect(photo_x, photo_y, photo_w, photo_h, fill=1, stroke=0)
        txt(photo_x + photo_w/2, photo_y + photo_h/2, "[photo]",
            font="Inter", size=8, color=MUTED, align="center")
    c.restoreState()

    right_x = front_x + 1.75*inch
    right_w = CARD_W - 1.75*inch - 0.12*inch

    txt(right_x + 0.02*inch, front_y + CARD_H - 0.22*inch,
        meet_banner(data), font="DMSans-Bold", size=10, color=NAVY)
    txt(right_x + 0.02*inch, front_y + CARD_H - 0.38*inch,
        "Scan to meet this animal.", font="Inter-SemiBold", size=7.2, color=MUTED)

    qr_size = 0.95*inch
    qr_x = right_x + 0.10*inch
    qr_y = front_y + 0.35*inch
    c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size,
                preserveAspectRatio=True, mask='auto')

    txt(right_x + right_w/2 - 0.05*inch, front_y + 0.22*inch,
        "TAKE IT HOME",
        font="DMSans-Bold", size=7.2, color=NAVY, align="center")
    txt(right_x + right_w/2 - 0.05*inch, front_y + 0.10*inch,
        "Ask it anything.",
        font="Inter", size=7, color=MUTED, align="center")

    crop_marks(front_x, front_y, CARD_W, CARD_H)
    txt(front_x, front_y + CARD_H + 0.22*inch,
        "FRONT  ·  Micro Totem (3.5 × 2 in business-card size)",
        font="Inter-Bold", size=9, color=MUTED)

    # ---------- BACK ----------
    c.setStrokeColor(RULE); c.setLineWidth(0.6)
    c.roundRect(back_x, back_y, CARD_W, CARD_H, 6, fill=0, stroke=1)

    title_h = 0.28*inch
    c.setFillColor(NAVY)
    c.roundRect(back_x, back_y + CARD_H - title_h, CARD_W, title_h, 6, fill=1, stroke=0)
    c.rect(back_x, back_y + CARD_H - title_h, CARD_W, title_h/2, fill=1, stroke=0)

    # Auto-scale species title in strip
    title_size = 8.5
    if len(species_title) > 26:
        title_size = 7.3
    if len(species_title) > 32:
        title_size = 6.6
    txt(back_x + CARD_W/2, back_y + CARD_H - 0.19*inch,
        species_title, font="DMSans-Bold", size=title_size, color=WHITE, align="center")

    txt(back_x + CARD_W/2, back_y + CARD_H - title_h - 0.14*inch,
        tagline, font="Inter-SemiBold", size=7.3, color=MUTED, align="center")

    list_top = back_y + CARD_H - title_h - 0.22*inch
    list_bottom = back_y + 0.40*inch
    list_h = list_top - list_bottom
    row_h = list_h / 5.0

    def xml_esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    for i, (q, a) in enumerate(pocket_qa):
        row_top = list_top - i*row_h
        cir_x = back_x + 0.16*inch
        cir_y = row_top - 0.075*inch
        c.setFillColor(NAVY)
        c.circle(cir_x, cir_y, 0.065*inch, fill=1, stroke=0)
        txt(cir_x, cir_y - 0.035*inch, str(i+1),
            font="Inter-Bold", size=6, color=WHITE, align="center")
        html = f'<b>{xml_esc(q)}</b>  {xml_esc(a)}'
        para(html,
             cir_x + 0.11*inch, row_top - row_h,
             CARD_W - 0.32*inch, row_h,
             font="Inter", size=5.8, leading=7.2, color=INK)

    cb_h = 0.20*inch
    cb_y = back_y + 0.20*inch
    c.setFillColor(ACCENT)
    c.roundRect(back_x + 0.10*inch, cb_y, CARD_W - 0.20*inch, cb_h, 3, fill=1, stroke=0)
    txt(back_x + CARD_W/2, cb_y + 0.07*inch,
        "LOOK AT THE ANIMAL: What do you see it doing right now?",
        font="Inter-Bold", size=6.3, color=NAVY, align="center")

    txt(back_x + CARD_W/2, back_y + 0.11*inch,
        "What a living thing can sense becomes its reality.",
        font="Inter-SemiBold", size=5.6, color=MUTED, align="center")
    txt(back_x + CARD_W/2, back_y + 0.04*inch,
        f"Environment shapes design.   ·   life.family-fun-group.com/{url_nick}",
        font="Inter", size=5.2, color=MUTED, align="center")

    crop_marks(back_x, back_y, CARD_W, CARD_H)
    txt(back_x, back_y + CARD_H + 0.22*inch,
        "BACK  ·  Pocket spine (5 of 8 — identical wording; AI covers all 8)",
        font="Inter-Bold", size=9, color=MUTED)

    # Page header + footer
    species_clean = data["species"]
    txt(PAGE_W/2, PAGE_H - 0.45*inch,
        f"MICRO TOTEM — LIFE System  ·  {species_clean}",
        font="DMSans-Bold", size=14, color=INK, align="center")
    txt(PAGE_W/2, PAGE_H - 0.65*inch,
        "Business-card size (3.5 × 2 in)  ·  Print duplex, trim on crop marks  ·  QR → Lehi greets → age door → animal",
        font="Inter", size=9, color=MUTED, align="center")

    txt(PAGE_W/2, 0.55*inch,
        "Structure rule: identical wording to Student Totem. No new questions. AI covers all 8.",
        font="Inter-SemiBold", size=8.5, color=MUTED, align="center")
    txt(PAGE_W/2, 0.38*inch,
        "On first scan: Lehi the Giraffe greets the guest, then asks age. Under 13 → locked 8-question rail.  13+ → Alpha/Omega naturalist tier.",
        font="Inter", size=8, color=MUTED, align="center")

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
            print(f"SKIP (photo missing): {slug} — expected {photo_path}")
            continue
        out_path = os.path.join(out_dir, f"MICRO_{slug}.pdf")
        build_micro_totem(json_file, out_path, photo_path)
        wrote.append(out_path)
        print(f"WROTE {out_path}  ({os.path.getsize(out_path):,} bytes)")
    print()
    print(f"Built {len(wrote)} Micro Totems.")

if __name__ == "__main__":
    main()
