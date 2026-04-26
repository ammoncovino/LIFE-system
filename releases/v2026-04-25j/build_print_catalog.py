#!/usr/bin/env python3
"""Build a Gold Standard print catalog (all 26) for v2026-04-25j.

For each poster: thumbnail of page 1 + filename + sha256 + page count + size.
Prints 10 (locked) + 16 (new) = 26 entries.

Also produces:
  - LIFE_GS_All_26_Combined_v2026-04-25j.pdf (single-file omnibus)
  - print_catalog_manifest.json with checksums
"""
import hashlib
import io
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import sys

V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))
import build_diet_cards_v23 as v23  # noqa: E402

import pypdf
import pypdfium2

LOCKED_DIR = Path("/tmp/LIFE-push/releases/v2026-04-25e/posters_corrected")
NEW_DIR = Path("/tmp/LIFE-push/releases/v2026-04-25j/posters_GS_16_new")

CATALOG_OUT = Path("/tmp/LIFE-push/releases/v2026-04-25j/print_catalog/LIFE_GS_Print_Catalog_v2026-04-25j.pdf")
COMBINED_OUT = Path("/tmp/LIFE-push/releases/v2026-04-25j/print_catalog/LIFE_GS_All_26_Combined_v2026-04-25j.pdf")
MANIFEST_OUT = Path("/tmp/LIFE-push/releases/v2026-04-25j/print_catalog/print_catalog_manifest.json")
CATALOG_OUT.parent.mkdir(parents=True, exist_ok=True)


CREAM = HexColor("#F4EBD9")
COFFEE = HexColor("#3B2A1A")
GOLD = HexColor("#B8860B")
WALNUT = HexColor("#5C4124")
RULE = HexColor("#C9B58A")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#6B5847")
PAPER = HexColor("#FFFFFF")


def sha256_short(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def render_thumbnail(pdf_path: Path, scale: float = 0.45):
    pdf = pypdfium2.PdfDocument(str(pdf_path))
    page = pdf[0]
    pil = page.render(scale=scale).to_pil()
    bio = io.BytesIO()
    pil.save(bio, format="PNG")
    bio.seek(0)
    return ImageReader(bio)


def collect_entries():
    items = []
    for p in sorted(LOCKED_DIR.glob("GoldStandard_*.pdf")):
        items.append({
            "tier": "GS_10_locked",
            "path": p,
            "filename": p.name,
            "sha256": sha256_short(p),
            "size_kb": round(p.stat().st_size / 1024),
        })
    for p in sorted(NEW_DIR.glob("GoldStandard_*.pdf")):
        items.append({
            "tier": "GS_16_new",
            "path": p,
            "filename": p.name,
            "sha256": sha256_short(p),
            "size_kb": round(p.stat().st_size / 1024),
        })
    # add page counts
    for it in items:
        with open(it["path"], "rb") as f:
            r = pypdf.PdfReader(f)
            it["pages"] = len(r.pages)
    return items


def build_catalog(items):
    PAGE_W, PAGE_H = letter
    c = canvas.Canvas(str(CATALOG_OUT), pagesize=letter)
    c.setTitle("LIFE Gold Standard Poster Print Catalog v2026-04-25j")
    c.setAuthor("Perplexity Computer")

    # ---- Cover page ----
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H - 0.7 * 72, PAGE_W, 0.7 * 72, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont(v23.DISPLAY, 22)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.45 * 72, "GOLD STANDARD VERBATIM POSTERS")
    c.setFont(v23.BODY, 11)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 0.62 * 72, "Print Catalog  ·  v2026-04-25j  ·  26 species (10 locked + 16 new)")

    c.setFillColor(COFFEE)
    c.setFont(v23.DISPLAY, 12)
    c.drawString(0.7 * 72, PAGE_H - 1.4 * 72, "Print specs")
    c.setFont(v23.BODY, 10)
    specs = [
        "•  Letter portrait, 8.5 \u00d7 11 in (612 \u00d7 792 pt)",
        "•  Color: full process (CMYK or RGB simulated)",
        "•  Stock recommendation: 100 lb gloss text, laminated for animal areas",
        "•  Posting: at exhibit, alongside species; supersedes ALL prior diet cards",
        "•  Verification: sha256 first-12 hash listed below; rebuild from source if drift detected",
    ]
    y = PAGE_H - 1.6 * 72
    for s in specs:
        c.drawString(0.7 * 72, y, s)
        y -= 14

    c.setFont(v23.DISPLAY, 12)
    c.setFillColor(COFFEE)
    c.drawString(0.7 * 72, y - 12, "Locked tier (10) — DO NOT REBUILD")
    c.setFont(v23.BODY, 10)
    y -= 28
    locked_summary = ("Ring-tailed, Red-ruffed and B&W ruffed lemurs  \u00b7  "
                      "Sailfin dragon  \u00b7  Monkey-tailed skink  \u00b7  "
                      "Six-banded and Three-banded armadillos  \u00b7  "
                      "Sulcata tortoise  \u00b7  Alpaca  \u00b7  Keel-billed toucan")
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import Paragraph
    sty = ParagraphStyle("_lock", fontName=v23.BODY, fontSize=10, leading=13, textColor=COFFEE)
    p = Paragraph(locked_summary, sty)
    pw, ph = p.wrap(PAGE_W - 1.4 * 72, 999)
    p.drawOn(c, 0.7 * 72, y - ph)
    y -= ph + 14

    c.setFont(v23.DISPLAY, 12)
    c.setFillColor(COFFEE)
    c.drawString(0.7 * 72, y, "New tier (16) — built v2026-04-25j")
    y -= 16
    new_summary = ("Capybara  \u00b7  Patagonian mara  \u00b7  Rabbit  \u00b7  Bennett's wallaby  \u00b7  "
                   "Two-toed sloth  \u00b7  Spider monkey  \u00b7  Kinkajou  \u00b7  Prehensile-tailed porcupine  \u00b7  "
                   "Toco toucan  \u00b7  Argentine tegu  \u00b7  Nine-banded armadillo  \u00b7  Chinese water dragon  \u00b7  "
                   "Veiled chameleon  \u00b7  Leopard tortoise  \u00b7  Russian tortoise  \u00b7  Yellow-footed tortoise")
    p = Paragraph(new_summary, sty)
    pw, ph = p.wrap(PAGE_W - 1.4 * 72, 999)
    p.drawOn(c, 0.7 * 72, y - ph)

    # Footer
    c.setFillColor(WALNUT)
    c.rect(0, 0, PAGE_W, 0.4 * 72, stroke=0, fill=1)
    c.setFillColor(CREAM)
    c.setFont(v23.BODY, 8)
    c.drawCentredString(PAGE_W / 2, 0.18 * 72,
                        "Match the bowl. Don't interpret.  \u00b7  Animals are TEACHERS, not attractions.")
    c.showPage()

    # ---- Catalog pages — 4 entries per page ----
    margin = 0.55 * 72
    content_w = PAGE_W - 2 * margin
    cell_h = (PAGE_H - 1.6 * 72) / 4
    thumbs = {}

    for idx, it in enumerate(items):
        slot = idx % 4
        if slot == 0:
            # new page
            c.setFillColor(CREAM)
            c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
            c.setFillColor(GOLD)
            c.rect(0, PAGE_H - 0.40 * 72, PAGE_W, 0.40 * 72, stroke=0, fill=1)
            c.setFillColor(PAPER)
            c.setFont(v23.DISPLAY, 13)
            c.drawString(margin, PAGE_H - 0.27 * 72, "Gold Standard Poster Catalog")
            c.setFont(v23.BODY, 9)
            c.drawRightString(PAGE_W - margin, PAGE_H - 0.27 * 72,
                              f"v2026-04-25j  \u00b7  page {idx // 4 + 2}")

        cell_top = PAGE_H - 0.55 * 72 - slot * cell_h
        # cell box
        c.setFillColor(PAPER)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.roundRect(margin, cell_top - cell_h + 6, content_w, cell_h - 12, 4, stroke=1, fill=1)

        # thumbnail
        thumb_w = 1.4 * 72
        thumb_h = thumb_w * 11 / 8.5
        thumb = render_thumbnail(it["path"], scale=0.30)
        c.drawImage(thumb, margin + 8, cell_top - thumb_h - 4,
                    width=thumb_w, height=thumb_h, mask="auto")
        c.setStrokeColor(RULE)
        c.rect(margin + 8, cell_top - thumb_h - 4, thumb_w, thumb_h, stroke=1, fill=0)

        # text
        tx = margin + thumb_w + 22
        c.setFillColor(COFFEE)
        c.setFont(v23.DISPLAY, 14)
        title = it["filename"].replace("GoldStandard_", "").replace(".pdf", "").replace("_", " ").upper()
        c.drawString(tx, cell_top - 14, title)

        c.setFont(v23.BODY, 9)
        c.setFillColor(MUTED)
        c.drawString(tx, cell_top - 30,
                     f"Tier: {it['tier'].replace('_', ' ')}  \u00b7  Pages: {it['pages']}  \u00b7  Size: {it['size_kb']} KB")
        c.drawString(tx, cell_top - 44, f"sha256: {it['sha256']}")
        c.drawString(tx, cell_top - 58, f"File: {it['filename']}")

        # tier chip
        chip_color = GOLD if it["tier"] == "GS_10_locked" else WALNUT
        c.setFillColor(chip_color)
        chip_label = "LOCKED \u00b7 DO NOT REBUILD" if it["tier"] == "GS_10_locked" else "NEW \u00b7 v2026-04-25j"
        chip_w = c.stringWidth(chip_label, v23.DISPLAY, 8) + 18
        c.roundRect(tx, cell_top - 88, chip_w, 18, 3, stroke=0, fill=1)
        c.setFillColor(PAPER)
        c.setFont(v23.DISPLAY, 8)
        c.drawCentredString(tx + chip_w / 2, cell_top - 82, chip_label)

        if slot == 3 or idx == len(items) - 1:
            # footer of this page
            c.setFillColor(WALNUT)
            c.rect(0, 0, PAGE_W, 0.30 * 72, stroke=0, fill=1)
            c.setFillColor(CREAM)
            c.setFont(v23.BODY, 7)
            c.drawCentredString(PAGE_W / 2, 0.12 * 72,
                                "LIFE Gold Standard Catalog  \u00b7  v2026-04-25j  \u00b7  Match the bowl. Don't interpret.")
            c.showPage()

    c.save()


def build_combined(items):
    """Single omnibus PDF with all 26 posters in order."""
    writer = pypdf.PdfWriter()
    for it in items:
        with open(it["path"], "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                writer.add_page(page)
    writer.add_metadata({
        "/Title": "LIFE Gold Standard — All 26 Combined v2026-04-25j",
        "/Author": "Perplexity Computer",
    })
    with open(COMBINED_OUT, "wb") as f:
        writer.write(f)


def main():
    items = collect_entries()
    print(f"Found {len(items)} posters.")
    build_catalog(items)
    print(f"Wrote catalog -> {CATALOG_OUT}")
    build_combined(items)
    print(f"Wrote combined -> {COMBINED_OUT}")
    manifest = {
        "version": "v2026-04-25j",
        "total": len(items),
        "locked_count": sum(1 for it in items if it["tier"] == "GS_10_locked"),
        "new_count": sum(1 for it in items if it["tier"] == "GS_16_new"),
        "items": [
            {k: v for k, v in it.items() if k != "path"} | {"relative_path": str(it["path"]).replace("/tmp/LIFE-push/", "")}
            for it in items
        ],
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote manifest -> {MANIFEST_OUT}")


if __name__ == "__main__":
    main()
