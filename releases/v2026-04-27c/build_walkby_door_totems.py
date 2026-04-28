"""Walk-by door totems v2026-04-27c.

For non-encounter species — 10 walk-by exhibits, HOU + SA each = 20 PDFs.

Key differences from encounter door totems:
  - NO pay-here band, NO QR, NO fee
  - Header: "EXHIBIT ENTRY  ·  WALK-BY"
  - Two columns: "WHO YOU'RE MEETING" and "HOW TO BE A GOOD GUEST"
  - Bottom: 3-second teaser drawn from canonical content (q1_sense first item)

Locked: brown/cream/gold palette, "Animals are TEACHERS not attractions",
       "Manager on duty has final say", environment-shapes-design footer.
"""
import sys, json
from pathlib import Path

V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))
import build_diet_cards_v23 as v23

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from pypdf import PdfWriter, PdfReader

VERSION = "v2026-04-27c"
OUT = Path(f"/tmp/walkby_door_totems_{VERSION}")
OUT.mkdir(parents=True, exist_ok=True)

# Palette (locked)
CREAM = HexColor("#F4EBD9")
COFFEE = HexColor("#3B2A1A")
WALNUT = HexColor("#5C4124")
GOLD = HexColor("#B8860B")
GOLD_LIGHT = HexColor("#E5C56A")
PAPER = HexColor("#FFFFFF")
RULE = HexColor("#C9B58A")
MUTED = HexColor("#7A6A55")

CANONICAL = json.load(open("/tmp/LIFE-push/releases/canonical/LIFE_totem_content_18.json"))
BY_SLUG = {s["slug"]: s for s in CANONICAL["species"]}

WALK_BY_SPECIES = [
    "rabbit",
    "patagonian-mara",
    "bennetts-wallaby",
    "alpaca",
    "monkey-tailed-skink",
    "geoffroys-spider-monkey",
    "sailfin-dragon",
    "nine-banded-armadillo",
    "sulcata-tortoise",
    "toco-toucan",
]

# Per-species behavior bullets sourced from canonical q1_sense / q3_signals.
# Two columns: "WHO YOU'RE MEETING" (3-4 facts) and "HOW TO BE A GOOD GUEST" (4 rules).


def species_meeting_bullets(s):
    """Pick 4 short bullets — one each from where, q1, q3, q5."""
    bullets = []
    bullets.append(f"<b>Lives:</b> {s['where_lives']}")
    bullets.append(f"<b>Senses:</b> {s['q1_sense'][0]}")
    bullets.append(f"<b>Signals:</b> {s['q3_signals'][0]}")
    bullets.append(f"<b>Watch for:</b> {s['q4_change'][0]}")
    return bullets


GUEST_RULES = [
    "Quiet voices — they hear you before you see them.",
    "No tapping the glass or barriers.",
    "No flash photography.",
    "Stand back if the animal moves toward the back — they're telling you something.",
]


def wrap(c, text, x, y_top, w, font, size, leading=12, color=None, align="LEFT"):
    style = ParagraphStyle("_w", fontName=font, fontSize=size, leading=leading,
                           textColor=color or COFFEE,
                           alignment={"LEFT": 0, "CENTER": 1, "RIGHT": 2}[align])
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 999)
    p.drawOn(c, x, y_top - ph)
    return ph


def auto_fit_title(c, text, x_center, y, max_w, max_pt=30, min_pt=18, font=None):
    font = font or v23.DISPLAY
    pt = max_pt
    while pt > min_pt:
        c.setFont(font, pt)
        if c.stringWidth(text, font, pt) <= max_w:
            break
        pt -= 1
    c.setFont(font, pt)
    c.drawCentredString(x_center, y, text)


def draw_walkby(out_path, slug, site_label):
    s = BY_SLUG[slug]
    PAGE_W, PAGE_H = letter
    c = canvas.Canvas(str(out_path), pagesize=letter)
    c.setTitle(f"LIFE Walk-By Door Totem — {s['common_name']} — {site_label}")
    c.setAuthor("Perplexity Computer")

    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # Top GOLD bar
    band_h = 0.46 * 72
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 17)
    c.drawCentredString(PAGE_W / 2, PAGE_H - band_h / 2 - 6, "EXHIBIT ENTRY  ·  WALK-BY")

    # Site
    site_h = 0.30 * 72
    y_site = PAGE_H - band_h - site_h
    c.setFillColor(WALNUT)
    c.rect(0, y_site, PAGE_W, site_h, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.BODY_SEMI, 10)
    c.drawCentredString(PAGE_W / 2, y_site + site_h / 2 - 3, site_label.upper())

    # Title + scientific
    margin = 0.6 * 72
    content_w = PAGE_W - 2 * margin
    y = y_site - 0.45 * 72

    c.setFillColor(COFFEE)
    auto_fit_title(c, s["common_name"], PAGE_W / 2, y, content_w - 8, max_pt=32, min_pt=18)
    y -= 22

    c.setFont(v23.DISPLAY, 11)
    c.setFillColor(WALNUT)
    c.drawCentredString(PAGE_W / 2, y, f"{s['scientific_name']}  ·  Animals are TEACHERS, not attractions.")
    y -= 14
    c.setFillColor(MUTED)
    c.setFont(v23.BODY, 9)
    c.drawCentredString(PAGE_W / 2, y, f"{s['conservation']}  ·  Manager on duty has final say.")
    y -= 18

    # Two columns
    col_h = 2.85 * 72
    col_top = y
    col_w = (content_w - 14) / 2

    # LEFT — WHO YOU'RE MEETING
    lx = margin
    c.setFillColor(PAPER)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(lx, col_top - col_h, col_w, col_h, 6, stroke=1, fill=1)
    c.setFillColor(GOLD)
    c.rect(lx, col_top - 0.30 * 72, col_w, 0.30 * 72, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 11)
    c.drawString(lx + 10, col_top - 0.21 * 72, "WHO YOU'RE MEETING")
    c.setFillColor(COFFEE)
    bullets = species_meeting_bullets(s)
    body_left = "<br/><br/>".join(bullets)
    wrap(c, body_left, lx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 9, leading=12.5)

    # RIGHT — HOW TO BE A GOOD GUEST
    rx = lx + col_w + 14
    c.setFillColor(PAPER)
    c.roundRect(rx, col_top - col_h, col_w, col_h, 6, stroke=1, fill=1)
    c.setFillColor(WALNUT)
    c.rect(rx, col_top - 0.30 * 72, col_w, 0.30 * 72, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.DISPLAY, 11)
    c.drawString(rx + 10, col_top - 0.21 * 72, "HOW TO BE A GOOD GUEST")
    c.setFillColor(COFFEE)
    rules_md = "<br/><br/>".join(f"•  {r}" for r in GUEST_RULES)
    rules_md += "<br/><br/><b>If something looks off → tell a keeper.</b><br/>If you're unsure → <b>Pause · Ask · Escalate</b>."
    wrap(c, rules_md, rx + 10, col_top - 0.40 * 72, col_w - 20, v23.BODY, 9, leading=12.5)

    y = col_top - col_h - 22

    # 3-SECOND CHECK band
    chk_h = 0.95 * 72
    c.setFillColor(COFFEE)
    c.roundRect(margin, y - chk_h, content_w, chk_h, 8, stroke=0, fill=1)
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.DISPLAY, 10)
    c.drawString(margin + 14, y - 16, "3-SECOND CHECK BEFORE YOU MOVE ON")
    c.setFillColor(PAPER)
    teaser = s["q1_prompt"]
    wrap(c, f"<b>{teaser}</b>", margin + 14, y - 26, content_w - 28, v23.DISPLAY, 14, leading=18, color=PAPER)
    c.setFillColor(GOLD_LIGHT)
    c.setFont(v23.BODY, 8.5)
    c.drawString(margin + 14, y - chk_h + 14, "More questions inside the exhibit. Keepers love being asked.")

    y -= chk_h + 18

    # Footer principle band
    foot_h = 0.42 * 72
    c.setFillColor(WALNUT)
    c.rect(0, 0.45 * 72, PAGE_W, foot_h, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.DISPLAY, 9.5)
    c.drawCentredString(PAGE_W / 2, 0.45 * 72 + foot_h / 2 + 2,
                        "What a living thing can sense becomes its reality. Environment shapes design.")
    c.setFont(v23.BODY, 7.5)
    c.drawCentredString(PAGE_W / 2, 0.45 * 72 + 4,
                        "Manager on duty has final say  ·  Exhibit rules posted at each habitat")

    c.setFillColor(GOLD)
    c.rect(0, 0, PAGE_W, 0.22 * 72, stroke=0, fill=1)
    c.setFillColor(WALNUT)
    c.setFont(v23.BODY, 6.5)
    c.drawString(margin, 0.08 * 72, f"LIFE Walk-By Door Totem  ·  {VERSION}  ·  {slug}")
    c.drawRightString(PAGE_W - margin, 0.08 * 72, "Animals are TEACHERS, not attractions.")

    c.save()
    return out_path


def main():
    sites = [
        ("HOU", "Houston Interactive Aquarium & Animal Preserve"),
        ("SA", "San Antonio Aquarium"),
    ]
    built = []
    for slug in WALK_BY_SPECIES:
        for code, full in sites:
            out = OUT / f"WalkBy_Totem_{slug.replace('-', '_')}_{code}_{VERSION}.pdf"
            draw_walkby(out, slug, full)
            built.append(out)
            print(f"  built {out.name}")

    master = OUT / f"LIFE_WalkBy_Door_Totems_All_{VERSION}.pdf"
    writer = PdfWriter()
    for p in built:
        for page in PdfReader(str(p)).pages:
            writer.add_page(page)
    with open(master, "wb") as f:
        writer.write(f)
    print(f"\n  built {master.name} ({len(built)} pages)")
    return built, master


if __name__ == "__main__":
    main()
