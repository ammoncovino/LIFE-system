"""
Print Approval Bundle — v2026-04-25k

Outputs:
  1. LIFE_Student_Totems_Omnibus_v2026-04-25k.pdf  (all 18 student totems)
  2. LIFE_Print_Approval_Sheet_v2026-04-25k.pdf  (one row per totem with QC checklist + 8 missing flagged)
  3. print_approval_manifest.json
"""
import hashlib
import json
import io
import os
from pathlib import Path
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import pypdfium2 as pdfium

# Fonts
FONT_DIR = "/tmp/fonts"
pdfmetrics.registerFont(TTFont("DMSans-Bold", f"{FONT_DIR}/DMSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DMSans", f"{FONT_DIR}/DMSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DMSans-Italic", f"{FONT_DIR}/DMSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DMSans-SemiBold", f"{FONT_DIR}/DMSans-SemiBold.ttf"))

# Palette
BROWN_DEEP = HexColor("#3B2A1A")
BROWN_MID = HexColor("#6B4F32")
BROWN_WARM = HexColor("#8B6F47")
CREAM = HexColor("#F5EDDF")
PAPER = HexColor("#FBF6EC")
USDA_GOLD = HexColor("#A87B2B")
SUCCESS = HexColor("#3F6B2A")
WARN = HexColor("#A8731B")
MISSING = HexColor("#8E2A1F")
SOFT_GRAY = HexColor("#7A6A55")

ROOT = Path("/tmp/LIFE-push")
TOTEMS_DIR = ROOT / "releases/totems"
OUT_DIR = ROOT / "releases/v2026-04-25k/print_approval"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Mapping: GS-26 slug -> existing totem filename (or None if missing)
TOTEM_MAP = {
    # Mammals — USDA
    "alpaca":                          "Totem_alpaca.pdf",
    "black_and_white_ruffed_lemur":    "Totem_black_and_white_ruffed_lemur.pdf",
    "red_ruffed_lemur":                "Totem_red_ruffed_lemur.pdf",
    "ring_tailed_lemur":               "Totem_ring_tailed_lemur.pdf",
    "capybara":                        "Totem_capybara.pdf",
    "patagonian_mara":                 "Totem_patagonian_mara.pdf",
    "kinkajou":                        "Totem_kinkajou.pdf",
    "prehensile_tailed_porcupine":     "Totem_prehensile_tailed_porcupine.pdf",
    "rabbit":                          "Totem_rabbit.pdf",
    "spider_monkey":                   "Totem_geoffroys_spider_monkey.pdf",
    "two_toed_sloth":                  "Totem_linnes_two_toed_sloth.pdf",
    "wallaby":                         "Totem_bennetts_wallaby.pdf",
    "nine_banded_armadillo":           "Totem_nine_banded_armadillo.pdf",
    "six_banded_armadillo":            None,  # MISSING
    "southern_three_banded_armadillo": None,  # MISSING
    # Birds — USDA
    "toco_toucan":                     "Totem_toco_toucan.pdf",
    "keel_billed_toucan":              None,  # MISSING
    # Reptiles — exempt
    "argentine_tegu":                  "Totem_argentine_tegu.pdf",
    "monkey_tailed_skink":             "Totem_monkey_tailed_skink.pdf",
    "sailfin_dragon":                  "Totem_sailfin_dragon.pdf",
    "chinese_water_dragon":            None,  # MISSING
    "veiled_chameleon":                None,  # MISSING
    "sulcata_tortoise":                "Totem_sulcata_tortoise.pdf",
    "leopard_tortoise":                None,  # MISSING
    "russian_tortoise":                None,  # MISSING
    "yellow_footed_tortoise":          None,  # MISSING
}

# Authority tier
AUTHORITY = {
    # USDA
    **{s: "USDA" for s in [
        "alpaca", "black_and_white_ruffed_lemur", "red_ruffed_lemur", "ring_tailed_lemur",
        "capybara", "patagonian_mara", "kinkajou", "prehensile_tailed_porcupine", "rabbit",
        "spider_monkey", "two_toed_sloth", "wallaby", "nine_banded_armadillo",
        "six_banded_armadillo", "southern_three_banded_armadillo",
        "toco_toucan", "keel_billed_toucan",
    ]},
    # Exempt reptiles
    **{s: "EXEMPT" for s in [
        "argentine_tegu", "monkey_tailed_skink", "chinese_water_dragon", "veiled_chameleon",
        "sulcata_tortoise", "leopard_tortoise", "russian_tortoise", "yellow_footed_tortoise",
    ]},
    # Sailfin special
    "sailfin_dragon": "USDA + CITES II / USFWS",
}

# Pretty labels
def pretty(slug: str) -> str:
    return slug.replace("_", " ").title()


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def thumb_first_page(pdf_path: Path, max_w: int = 220) -> bytes:
    """Render first page to PNG bytes."""
    doc = pdfium.PdfDocument(str(pdf_path))
    page = doc[0]
    pil = page.render(scale=1.4).to_pil()
    pil.thumbnail((max_w, 9999))
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    return buf.getvalue()


# ==============================================================================
# 1. Combined Omnibus PDF
# ==============================================================================
def build_omnibus():
    out = OUT_DIR / "LIFE_Student_Totems_Omnibus_v2026-04-25k.pdf"
    writer = PdfWriter()
    appended = 0
    for slug, filename in TOTEM_MAP.items():
        if filename is None:
            continue
        path = TOTEMS_DIR / filename
        if not path.exists():
            print(f"  ! MISSING ON DISK: {path}")
            continue
        reader = PdfReader(str(path))
        for p in reader.pages:
            writer.add_page(p)
        appended += 1
    writer.add_metadata({
        "/Title": "LIFE Student Totems Omnibus v2026-04-25k",
        "/Author": "Perplexity Computer",
        "/Subject": f"{appended} student totems combined for print",
    })
    with open(out, "wb") as f:
        writer.write(f)
    print(f"omnibus: {out}  ({appended} totems)")
    return out, appended


# ==============================================================================
# 2. Print Approval Sheet
# ==============================================================================
def chip(c, x, y, w, h, label, fill, text_color=HexColor("#FFFFFF"), font_size=8):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, h / 2, stroke=0, fill=1)
    c.setFillColor(text_color)
    c.setFont("DMSans-Bold", font_size)
    tw = c.stringWidth(label, "DMSans-Bold", font_size)
    c.drawString(x + (w - tw) / 2, y + (h - font_size) / 2 + 1.5, label)


def qc_box(c, x, y, label):
    c.setStrokeColor(BROWN_MID)
    c.setLineWidth(0.7)
    c.rect(x, y, 9, 9, stroke=1, fill=0)
    c.setFont("DMSans", 8.5)
    c.setFillColor(BROWN_DEEP)
    c.drawString(x + 13, y + 1.5, label)


def build_approval_sheet():
    out = OUT_DIR / "LIFE_Print_Approval_Sheet_v2026-04-25k.pdf"
    PAGE_W, PAGE_H = LETTER
    c = canvas.Canvas(str(out), pagesize=LETTER)
    c.setTitle("LIFE Print Approval Sheet v2026-04-25k")
    c.setAuthor("Perplexity Computer")

    margin = 0.45 * inch
    rows_per_page = 4
    row_h = (PAGE_H - 2 * margin - 0.85 * inch) / rows_per_page

    # ----- Cover content drawn on page 1 above first 4 rows -----
    def draw_cover(y_top):
        c.setFillColor(BROWN_DEEP)
        c.setFont("DMSans-Bold", 22)
        c.drawString(margin, y_top - 4, "LIFE Student Totems — Print Approval")
        c.setFont("DMSans", 10.5)
        c.setFillColor(BROWN_MID)
        c.drawString(margin, y_top - 22, "v2026-04-25k  ·  Mark each totem APPROVED, REVISE, or HOLD before sending to print.")
        c.setStrokeColor(BROWN_WARM)
        c.setLineWidth(0.8)
        c.line(margin, y_top - 32, PAGE_W - margin, y_top - 32)

    def draw_row(slug: str, filename, y_top: float):
        """Draw one row at the top y_top, height row_h."""
        x = margin
        w = PAGE_W - 2 * margin
        # Row container
        c.setStrokeColor(BROWN_WARM)
        c.setLineWidth(0.5)
        c.line(x, y_top - row_h + 4, x + w, y_top - row_h + 4)

        # Thumbnail (or MISSING block)
        thumb_w = 1.55 * inch
        thumb_h = row_h - 0.18 * inch
        thumb_x = x
        thumb_y = y_top - thumb_h - 0.05 * inch
        if filename is not None:
            path = TOTEMS_DIR / filename
            if path.exists():
                try:
                    img_bytes = thumb_first_page(path, max_w=260)
                    img = Image.open(io.BytesIO(img_bytes))
                    aspect = img.width / img.height
                    box_aspect = thumb_w / thumb_h
                    if aspect > box_aspect:
                        draw_w = thumb_w
                        draw_h = thumb_w / aspect
                    else:
                        draw_h = thumb_h
                        draw_w = thumb_h * aspect
                    tmp = OUT_DIR / f"_thumb_{slug}.png"
                    with open(tmp, "wb") as f:
                        f.write(img_bytes)
                    c.drawImage(str(tmp),
                                thumb_x + (thumb_w - draw_w) / 2,
                                thumb_y + (thumb_h - draw_h) / 2,
                                width=draw_w, height=draw_h, mask='auto')
                    tmp.unlink(missing_ok=True)
                except Exception as e:
                    print(f"  ! thumb fail {slug}: {e}")
        else:
            # MISSING block
            c.setFillColor(HexColor("#F5E5E2"))
            c.rect(thumb_x, thumb_y, thumb_w, thumb_h, stroke=0, fill=1)
            c.setFillColor(MISSING)
            c.setFont("DMSans-Bold", 12)
            c.drawCentredString(thumb_x + thumb_w / 2, thumb_y + thumb_h / 2 + 6, "NOT YET BUILT")
            c.setFont("DMSans-Italic", 8.5)
            c.drawCentredString(thumb_x + thumb_w / 2, thumb_y + thumb_h / 2 - 8, "needs content + render")

        # Name + meta
        col2_x = x + thumb_w + 0.18 * inch
        c.setFillColor(BROWN_DEEP)
        # Long names: shrink font to fit
        name = pretty(slug)
        name_size = 13
        max_name_w = 2.85 * inch
        while c.stringWidth(name, "DMSans-Bold", name_size) > max_name_w and name_size > 9:
            name_size -= 0.5
        c.setFont("DMSans-Bold", name_size)
        c.drawString(col2_x, y_top - 14, name)
        # authority chip
        auth = AUTHORITY.get(slug, "—")
        if auth.startswith("USDA"):
            chip_color = USDA_GOLD
        elif auth == "EXEMPT":
            chip_color = HexColor("#5C7A3F")
        else:
            chip_color = BROWN_MID
        chip(c, col2_x, y_top - 32, 92, 13, auth if len(auth) <= 22 else auth, chip_color, font_size=7.5)

        # Filename + sha + pages + size
        c.setFont("DMSans", 8.5)
        c.setFillColor(BROWN_MID)
        if filename is not None:
            path = TOTEMS_DIR / filename
            if path.exists():
                size_kb = path.stat().st_size / 1024
                try:
                    pages = len(PdfReader(str(path)).pages)
                except Exception:
                    pages = "?"
                sha = sha256_of(path)
                c.drawString(col2_x, y_top - 50, f"file: {filename}")
                c.drawString(col2_x, y_top - 62, f"pages: {pages}   size: {size_kb:.0f} KB")
                c.setFont("DMSans", 7)
                c.drawString(col2_x, y_top - 73, f"sha256: {sha[:48]}\u2026")
        else:
            c.drawString(col2_x, y_top - 50, "file: —")
            c.drawString(col2_x, y_top - 62, "TODO: author content JSON, render with build_totem_v3")

        # QC checklist column
        col3_x = col2_x + 3.05 * inch
        c.setFont("DMSans-SemiBold", 9)
        c.setFillColor(BROWN_DEEP)
        c.drawString(col3_x, y_top - 14, "QC CHECKLIST")
        items = [
            "Trim & bleed correct",
            "Photos sharp at 300 DPI",
            "Diet matches Master Doc",
            "USDA banner correct",
            "No typos",
        ]
        for i, it in enumerate(items):
            qc_box(c, col3_x, y_top - 32 - i * 13, it)

        # Approval column
        col4_x = col3_x + 1.75 * inch
        c.setFont("DMSans-SemiBold", 9)
        c.setFillColor(BROWN_DEEP)
        c.drawString(col4_x, y_top - 14, "APPROVAL")
        for i, (lbl, color) in enumerate([
            ("APPROVED", SUCCESS),
            ("REVISE", WARN),
            ("HOLD", MISSING),
        ]):
            c.setStrokeColor(color)
            c.setLineWidth(1.0)
            c.circle(col4_x + 5, y_top - 28 - i * 14, 5, stroke=1, fill=0)
            c.setFillColor(BROWN_DEEP)
            c.setFont("DMSans", 9)
            c.drawString(col4_x + 14, y_top - 31 - i * 14, lbl)

        # Notes line
        c.setFont("DMSans-Italic", 7.5)
        c.setFillColor(SOFT_GRAY)
        c.drawString(col4_x, y_top - 78, "Notes:")
        c.setStrokeColor(BROWN_WARM)
        c.setLineWidth(0.5)
        c.line(col4_x + 30, y_top - 78, x + w, y_top - 78)

    # ----- Lay out rows across pages -----
    slugs = list(TOTEM_MAP.keys())
    page_idx = 0
    for i, slug in enumerate(slugs):
        if i % rows_per_page == 0:
            if i != 0:
                c.showPage()
            page_idx += 1
            top = PAGE_H - margin
            if page_idx == 1:
                draw_cover(top)
                top -= 0.85 * inch
            row_top = top
        else:
            row_top -= row_h
        draw_row(slug, TOTEM_MAP[slug], row_top)

    # Footer on last page
    c.setFillColor(BROWN_WARM)
    c.setLineWidth(0.5)
    c.setStrokeColor(BROWN_WARM)
    c.line(margin, 0.55 * inch, PAGE_W - margin, 0.55 * inch)
    c.setFillColor(SOFT_GRAY)
    c.setFont("DMSans-Italic", 8)
    c.drawString(margin, 0.4 * inch,
                 "What a living thing can sense becomes its reality. Environment shapes design.")
    c.drawRightString(PAGE_W - margin, 0.4 * inch, "v2026-04-25k")
    c.showPage()
    c.save()
    print(f"approval sheet: {out}")
    return out


# ==============================================================================
# 3. Manifest
# ==============================================================================
def build_manifest(omnibus_path, omnibus_count, approval_path):
    rows = []
    for slug, filename in TOTEM_MAP.items():
        if filename is None:
            rows.append({"slug": slug, "status": "MISSING",
                         "authority": AUTHORITY.get(slug)})
        else:
            path = TOTEMS_DIR / filename
            if path.exists():
                rows.append({
                    "slug": slug,
                    "status": "READY",
                    "authority": AUTHORITY.get(slug),
                    "file": filename,
                    "pages": len(PdfReader(str(path)).pages),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_of(path),
                })
    out = OUT_DIR / "print_approval_manifest.json"
    with open(out, "w") as f:
        json.dump({
            "version": "v2026-04-25k",
            "totems": rows,
            "summary": {
                "total_species_in_GS26": len(TOTEM_MAP),
                "totems_ready": sum(1 for r in rows if r["status"] == "READY"),
                "totems_missing": sum(1 for r in rows if r["status"] == "MISSING"),
            },
            "deliverables": {
                "omnibus_pdf": str(omnibus_path.relative_to(ROOT)),
                "omnibus_count": omnibus_count,
                "approval_sheet_pdf": str(approval_path.relative_to(ROOT)),
            },
        }, f, indent=2)
    print(f"manifest: {out}")


if __name__ == "__main__":
    omni, n = build_omnibus()
    appr = build_approval_sheet()
    build_manifest(omni, n, appr)
