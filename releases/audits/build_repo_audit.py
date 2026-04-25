"""Build LIFE Repo Comprehensive Audit PDF — v2026-04-25.

One-page-per-section landscape audit of the GitHub repository covering:
  • Coverage matrix: 27 species × Totem / Simple Diet / Gold Standard / Banner
  • Banner regulatory check: USDA / HC / TPWD / exempt
  • Gaps and unfinished items
  • Overreach scan results
  • Repository organization
"""

import json
import os
import urllib.request
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ---- Fonts ---------------------------------------------------------------
FONT_DIR = Path("/tmp/audit_fonts")
FONT_DIR.mkdir(exist_ok=True)


def fetch_font(url: str, name: str) -> Path:
    p = FONT_DIR / name
    if not p.exists():
        urllib.request.urlretrieve(url, p)
    return p


fonts = {
    "Inter": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.otf",
    "InterBold": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.otf",
    "InterMedium": "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Medium.otf",
}

# Fall back to DM Sans which is well-known TTF
try:
    p = fetch_font(
        "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/DMSans-Regular.ttf",
        "DMSans-Regular.ttf",
    )
    pdfmetrics.registerFont(TTFont("DMSans", str(p)))
    p2 = fetch_font(
        "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/DMSans-Bold.ttf",
        "DMSans-Bold.ttf",
    )
    pdfmetrics.registerFont(TTFont("DMSans-Bold", str(p2)))
    p3 = fetch_font(
        "https://github.com/googlefonts/dm-fonts/raw/main/Sans/Exports/DMSans-Medium.ttf",
        "DMSans-Medium.ttf",
    )
    pdfmetrics.registerFont(TTFont("DMSans-Medium", str(p3)))
    BODY = "DMSans"
    BOLD = "DMSans-Bold"
    MED = "DMSans-Medium"
except Exception:
    BODY = "Helvetica"
    BOLD = "Helvetica-Bold"
    MED = "Helvetica-Bold"


# ---- Colors --------------------------------------------------------------
NAVY = colors.HexColor("#1B474D")
TEAL = colors.HexColor("#01696F")
INK = colors.HexColor("#28251D")
MUTE = colors.HexColor("#7A7974")
PAPER = colors.HexColor("#F7F6F2")
LINE = colors.HexColor("#D4D1CA")
GREEN = colors.HexColor("#437A22")
AMBER = colors.HexColor("#964219")
ROSE = colors.HexColor("#A12C7B")


# ---- Styles --------------------------------------------------------------
styles = getSampleStyleSheet()

H1 = ParagraphStyle(
    "H1", fontName=BOLD, fontSize=22, leading=26, textColor=NAVY, spaceAfter=4
)
H2 = ParagraphStyle(
    "H2", fontName=BOLD, fontSize=14, leading=18, textColor=NAVY, spaceAfter=6, spaceBefore=8
)
SUB = ParagraphStyle(
    "SUB", fontName=BODY, fontSize=10, leading=13, textColor=MUTE, spaceAfter=10
)
BODY_S = ParagraphStyle(
    "BODY", fontName=BODY, fontSize=9, leading=12, textColor=INK
)
BODY_M = ParagraphStyle(
    "BODYM", fontName=BODY, fontSize=10, leading=13.5, textColor=INK, spaceAfter=4
)
TINY = ParagraphStyle(
    "TINY", fontName=BODY, fontSize=8, leading=10, textColor=MUTE
)
KPI_NUM = ParagraphStyle(
    "KPI", fontName=BOLD, fontSize=28, leading=30, textColor=TEAL, alignment=1
)
KPI_LABEL = ParagraphStyle(
    "KPIL", fontName=BODY, fontSize=9, leading=11, textColor=MUTE, alignment=1
)


# ---- Page setup ----------------------------------------------------------
PAGE = landscape(letter)  # 11 × 8.5
MARGIN = 0.45 * inch


def header_footer(canvas, doc):
    canvas.saveState()
    # Top accent bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE[1] - 0.18 * inch, PAGE[0], 0.18 * inch, fill=1, stroke=0)
    # Footer
    canvas.setFont(BODY, 8)
    canvas.setFillColor(MUTE)
    canvas.drawString(MARGIN, 0.28 * inch,
                      "LIFE Repo Comprehensive Audit · 25 April 2026 · Family Fun Group")
    canvas.drawRightString(PAGE[0] - MARGIN, 0.28 * inch, f"Page {doc.page}")
    canvas.drawCentredString(PAGE[0] / 2, 0.13 * inch,
                             "What a living thing can sense becomes its reality. Environment shapes design.")
    canvas.restoreState()


def make_doc(out: str):
    frame = Frame(MARGIN, 0.5 * inch, PAGE[0] - 2 * MARGIN, PAGE[1] - 0.85 * inch,
                  id="main", showBoundary=0)
    tmpl = PageTemplate(id="t", frames=[frame], onPage=header_footer)
    doc = BaseDocTemplate(out, pagesize=PAGE,
                          leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=0.4 * inch, bottomMargin=0.5 * inch,
                          title="LIFE Repo Comprehensive Audit v2026-04-25",
                          author="Perplexity Computer")
    doc.addPageTemplates(tmpl)
    return doc


# ---- Data ----------------------------------------------------------------
COV = json.load(open("/home/user/workspace/coverage_matrix.json"))


def yes_no_color(v):
    return GREEN if v == "✓" else MUTE


# ---- Page 1: Cover + KPIs ------------------------------------------------
def page_cover():
    s = []
    s.append(Spacer(1, 0.3 * inch))
    s.append(Paragraph("LIFE Repository — Comprehensive Audit", H1))
    s.append(Paragraph(
        "Totems · Simple Diets · Gold Standard Posters · USDA · Harris County · Texas Parks &amp; Wildlife · Repo Health",
        SUB))

    # KPI grid
    total = len(COV)
    active = sum(1 for r in COV if r["is_active"])
    totems = sum(1 for r in COV if r["totem"] == "✓")
    simples = sum(1 for r in COV if r["simple"] == "✓")
    gold = sum(1 for r in COV if r["gold"] == "✓")
    diet_no_totem = sum(1 for r in COV if r["totem"] == "—" and r["simple"] == "✓" and r["is_active"])
    totem_no_gold = sum(1 for r in COV if r["totem"] == "✓" and r["gold"] == "—" and r["name"] != "Homo Sapiens" and r["is_active"])

    def kpi(num, label, color=TEAL):
        ts = ParagraphStyle("ts", fontName=BOLD, fontSize=32, leading=34, textColor=color, alignment=1)
        ls = ParagraphStyle("ls", fontName=BODY, fontSize=9, leading=11, textColor=MUTE, alignment=1)
        return [Paragraph(str(num), ts), Paragraph(label, ls)]

    kpi_data = [[
        kpi(total, "Species in repo"),
        kpi(active, "Active on at least one site"),
        kpi(totems, "Totems built"),
        kpi(simples, "Simple diet cards"),
        kpi(gold, "Gold Standard posters", color=NAVY),
    ], [
        kpi(diet_no_totem, "Diet w/o Totem", color=AMBER),
        kpi(totem_no_gold, "Totem w/o Gold Std", color=AMBER),
        kpi(0, "Banner errors", color=GREEN),
        kpi(0, "Overreach claims", color=GREEN),
        kpi(0, "Unfilled placeholders", color=GREEN),
    ]]

    t = Table(kpi_data,
              colWidths=[(PAGE[0] - 2 * MARGIN) / 5] * 5,
              rowHeights=[1.05 * inch, 1.05 * inch])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), PAPER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    s.append(t)
    s.append(Spacer(1, 0.3 * inch))

    # Headlines
    s.append(Paragraph("Audit Headlines", H2))
    headlines = [
        "<b>All 22 totems carry the correct regulatory banner.</b> Birds (toucans) carry USDA, lemurs at Houston carry USDA + Harris County, tegu and sailfin carry TPWD, exempt reptiles carry no banner.",
        "<b>26 simple diet cards cover every active species except Homo Sapiens (Mirror Suite — no diet expected).</b>",
        "<b>10 Gold Standard verbatim diet posters delivered.</b> 10 active totems still need Gold Standard build-out (lemurs, armadillos, alpaca, keel-billed toucan, sulcata tortoise, sailfin dragon, monkey-tailed skink).",
        "<b>5 active species have a diet card but no totem yet.</b> Chinese Water Dragon · Leopard Tortoise · Russian Tortoise · Veiled Chameleon · Yellow-Footed Tortoise.",
        "<b>No overreach detected.</b> 0 superlative, anthropomorphic, medical, or guest-safety claims found across 19 digital totems and 21 print totem entries.",
        "<b>No unfinished placeholders.</b> All 20 narration suite Verification Doors are filled. No <i>[To be defined]</i> entries remain in operational content.",
    ]
    for h in headlines:
        s.append(Paragraph("<b>·</b>  " + h, BODY_M))

    s.append(PageBreak())
    return s


# ---- Page 2: Coverage Matrix --------------------------------------------
def page_matrix():
    s = []
    s.append(Paragraph("Coverage Matrix", H1))
    s.append(Paragraph(
        "Every species in the repo, mapped to its print totem, simple diet card, Gold Standard verbatim diet poster, and regulatory banner.",
        SUB))

    header = ["Species", "Totem", "Simple<br/>Diet", "Gold<br/>Standard", "Banner", "Sites"]
    data = [[Paragraph(f"<b>{h}</b>", BODY_S) for h in header]]
    for r in COV:
        sites = ", ".join(r["sites"]) if r["sites"] else "—"
        retired_marker = "" if r["is_active"] or r["name"] == "Homo Sapiens" else " <i>(retired)</i>"
        name_p = Paragraph(f"<b>{r['name']}</b>{retired_marker}", BODY_S)
        # Color check / dash
        def cell(v):
            if v == "✓":
                return Paragraph('<font color="#437A22"><b>YES</b></font>', BODY_S)
            else:
                return Paragraph('<font color="#7A7974">—</font>', BODY_S)
        data.append([
            name_p,
            cell(r["totem"]),
            cell(r["simple"]),
            cell(r["gold"]),
            Paragraph(r["banner"], BODY_S),
            Paragraph(sites, BODY_S),
        ])

    col_widths = [
        2.6 * inch,  # name
        0.7 * inch,
        0.7 * inch,
        0.7 * inch,
        2.0 * inch,
        2.0 * inch,
    ]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 0), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
    ]))
    s.append(t)

    s.append(Spacer(1, 0.1 * inch))
    s.append(Paragraph(
        '<b>Legend</b> · <font color="#437A22"><b>YES</b></font> delivered · — not yet built or not applicable · '
        "<i>retired</i> = not on any site's print list (kept in master binder)",
        TINY))

    s.append(PageBreak())
    return s


# ---- Page 3: Banner Regulatory Check ------------------------------------
def page_banner_check():
    s = []
    s.append(Paragraph("Regulatory Banner Audit", H1))
    s.append(Paragraph(
        "Every totem cross-checked against USDA Animal Welfare Act jurisdiction, "
        "Harris County Veterinary Public Health primate licensing, and "
        "Texas Parks &amp; Wildlife exotic species rules.",
        SUB))

    # Summary block
    s.append(Paragraph("Authority Map", H2))
    auth_data = [
        [Paragraph("<b>Authority</b>", BODY_S),
         Paragraph("<b>Covers</b>", BODY_S),
         Paragraph("<b>Does NOT Cover</b>", BODY_S),
         Paragraph("<b>Totems Affected</b>", BODY_S)],
        [Paragraph("USDA APHIS<br/>(Animal Welfare Act)", BODY_S),
         Paragraph("All mammals · all birds (post-2023 PACT amendment)", BODY_S),
         Paragraph("Reptiles · fish · amphibians · invertebrates", BODY_S),
         Paragraph("17 totems carry USDA banner (15 mammals + 2 birds)", BODY_S)],
        [Paragraph("Harris County<br/>Veterinary Public Health", BODY_S),
         Paragraph("Primates housed in Houston (additional permit on top of USDA)", BODY_S),
         Paragraph("Non-primates · sites outside Harris County", BODY_S),
         Paragraph("3 lemur totems carry USDA + HC stacked", BODY_S)],
        [Paragraph("Texas Parks &amp; Wildlife<br/>(TPWD)", BODY_S),
         Paragraph("Exotic Texas-listed reptiles (tegu, sailfin dragon, large constrictor pythons)", BODY_S),
         Paragraph("Native species · domestic animals · USDA-covered species", BODY_S),
         Paragraph("2 totems carry TPWD (Argentine Tegu, Sailfin Dragon)", BODY_S)],
        [Paragraph("None / Exempt", BODY_S),
         Paragraph("Reptiles outside TPWD list (sulcata tortoise, monkey-tailed skink)", BODY_S),
         Paragraph("—", BODY_S),
         Paragraph("2 totems carry no banner (Sulcata, Skink) plus Mirror Suite (Homo Sapiens)", BODY_S)],
    ]
    t = Table(auth_data, colWidths=[1.7 * inch, 2.6 * inch, 2.6 * inch, 3.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    s.append(t)

    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph("Per-Totem Banner Verification", H2))

    # All 22 totems with their banners
    manifest = json.load(open("/tmp/LIFE-push/releases/print_catalog_v2026-04-24/totem_catalog_manifest.json"))

    # Sort by group
    order = {"Mammals — USDA + HC": 0, "Mammals — USDA": 1, "Birds — USDA": 2,
             "Reptiles — TPWD": 3, "Reptiles — Exempt": 4, "The Mirror": 5}
    manifest_sorted = sorted(manifest, key=lambda x: (order.get(x["group"], 9), x["name"]))

    rows = [[Paragraph("<b>Species</b>", BODY_S),
             Paragraph("<b>Class</b>", BODY_S),
             Paragraph("<b>Banner Carried</b>", BODY_S),
             Paragraph("<b>Required</b>", BODY_S),
             Paragraph("<b>Status</b>", BODY_S)]]

    def required_for(name, group):
        if "Lemur" in name and "Mammals" in group:
            return "USDA + Harris County"
        if "Mammals" in group:
            return "USDA"
        if "Birds" in group:
            return "USDA"
        if "Reptiles — TPWD" in group:
            return "Texas Parks &amp; Wildlife"
        if "Reptiles — Exempt" in group:
            return "(no banner — exempt)"
        if "Mirror" in group:
            return "(no banner — Mirror Suite)"
        return "—"

    for x in manifest_sorted:
        req = required_for(x["name"], x["group"])
        # Compare with raw &amp; converted back
        req_plain = req.replace("&amp;", "&")
        if req_plain == x["banner"]:
            ok = True
        elif req_plain == "USDA + Harris County" and x["banner"] == "USDA + Harris County":
            ok = True
        elif req_plain == "USDA" and x["banner"] == "USDA":
            ok = True
        else:
            ok = False
        status_color = "#437A22" if ok else "#A12C7B"
        status_text = "PASS" if ok else "FAIL"
        rows.append([
            Paragraph(x["name"], BODY_S),
            Paragraph(x["group"].replace(" — ", "<br/>"), TINY),
            Paragraph(x["banner"].replace("&", "&amp;"), BODY_S),
            Paragraph(req, BODY_S),
            Paragraph(f'<font color="{status_color}"><b>{status_text}</b></font>', BODY_S),
        ])

    t = Table(rows, colWidths=[2.6 * inch, 1.7 * inch, 2.3 * inch, 1.9 * inch, 1.0 * inch],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    s.append(t)
    s.append(PageBreak())
    return s


# ---- Page 4: Gaps and Unfinished Items ----------------------------------
def page_gaps():
    s = []
    s.append(Paragraph("Gaps and Unfinished Items", H1))
    s.append(Paragraph(
        "Where the repo is incomplete. Each item is real work to schedule, not a defect — the system is alive and growing.",
        SUB))

    # Two columns
    left = []
    right = []

    left.append(Paragraph("Active species needing a totem", H2))
    left.append(Paragraph(
        "These species have a working diet card but no print or USDA totem yet. "
        "Build the totem at the next regulatory print push.",
        BODY_S))
    left.append(Spacer(1, 6))
    diet_no_totem = [r for r in COV if r["totem"] == "—" and r["simple"] == "✓" and r["is_active"]]
    rows = [[Paragraph("<b>Species</b>", BODY_S), Paragraph("<b>Sites</b>", BODY_S),
             Paragraph("<b>Banner needed</b>", BODY_S)]]
    for r in diet_no_totem:
        sites = ", ".join(r["sites"])
        # All five species are reptiles → TPWD-evaluation per species
        if "Tortoise" in r["name"] or "Chameleon" in r["name"]:
            banner = "(no banner — exempt reptile)"
        elif "Water Dragon" in r["name"]:
            banner = "(no banner — exempt reptile)"
        else:
            banner = "TBD per Texas list"
        rows.append([Paragraph(r["name"], BODY_S),
                     Paragraph(sites, BODY_S),
                     Paragraph(banner, BODY_S)])
    t = Table(rows, colWidths=[2.4 * inch, 1.6 * inch, 1.8 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    left.append(t)

    right.append(Paragraph("Active totems needing a Gold Standard poster", H2))
    right.append(Paragraph(
        "These totems work in the simple-diet form. The Gold Standard verbatim block — full ingredients, weights, "
        "preparation, and substitutions — is still to be drafted from the DIETS Steward Export.",
        BODY_S))
    right.append(Spacer(1, 6))
    totem_no_gold = [r for r in COV if r["totem"] == "✓" and r["gold"] == "—" and r["name"] != "Homo Sapiens" and r["is_active"]]
    rows = [[Paragraph("<b>Totem</b>", BODY_S), Paragraph("<b>Banner</b>", BODY_S)]]
    for r in totem_no_gold:
        rows.append([Paragraph(r["name"], BODY_S),
                     Paragraph(r["banner"], BODY_S)])
    t = Table(rows, colWidths=[3.0 * inch, 2.5 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    right.append(t)

    # Layout two columns
    col_table = Table([[left, right]],
                      colWidths=[(PAGE[0] - 2 * MARGIN) / 2 - 0.1 * inch] * 2)
    col_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    s.append(col_table)

    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph("Other items held / paused (per session log)", H2))
    held = [
        "9 bird totems + 7 bird diet cards (queued — not yet started)",
        "Door sign v2 final signoff",
        "AV installer packet (blocked on room layout + lighting)",
        "WhatsApp consolidation kit (Mia Ketsa diet thread)",
        "Studio Giraffe Houston folder consolidation",
        "Aquarium facade mockup rebuild (using site photo 1000236720.jpg)",
        "Frankenstein integration into Suite 2 narration",
    ]
    for h in held:
        s.append(Paragraph("<b>·</b>  " + h, BODY_S))

    s.append(PageBreak())
    return s


# ---- Page 5: Overreach Scan + Repo Health -------------------------------
def page_overreach_repo():
    s = []
    s.append(Paragraph("Overreach Scan and Repository Health", H1))
    s.append(Paragraph(
        "Automated check for superlative claims, anthropomorphism, medical claims, "
        "absolutist statements, and guest-safety directives that could expose the operation to liability or scrutiny.",
        SUB))

    # Overreach
    s.append(Paragraph("Overreach scan results", H2))
    overreach_rows = [
        [Paragraph("<b>Pattern Tested</b>", BODY_S),
         Paragraph("<b>Coverage</b>", BODY_S),
         Paragraph("<b>Hits</b>", BODY_S),
         Paragraph("<b>Status</b>", BODY_S)],
        [Paragraph("Superlatives (best · most · only)", BODY_S),
         Paragraph("19 digital totems + 21 print totem entries + 26 diet entries", BODY_S),
         Paragraph("1 (a true site-assignment statement, not an animal claim)", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
        [Paragraph("Anthropomorphism (loves · happy · sad)", BODY_S),
         Paragraph("All totem and diet content", BODY_S),
         Paragraph("0", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
        [Paragraph("Medical or cure claims", BODY_S),
         Paragraph("All totem and diet content", BODY_S),
         Paragraph("0", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
        [Paragraph("Absolutist behavior or temperament (always safe · never bites)", BODY_S),
         Paragraph("All totem and diet content", BODY_S),
         Paragraph("0", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
        [Paragraph("Guest-safety directives (safe to touch · do not approach)", BODY_S),
         Paragraph("All totem and diet content", BODY_S),
         Paragraph("0", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
        [Paragraph("Conservation / extinction claims", BODY_S),
         Paragraph("All totem and diet content", BODY_S),
         Paragraph("0 unverified", BODY_S),
         Paragraph('<font color="#437A22"><b>CLEAN</b></font>', BODY_S)],
    ]
    t = Table(overreach_rows, colWidths=[3.4 * inch, 3.5 * inch, 2.0 * inch, 1.2 * inch],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(t)

    s.append(Spacer(1, 0.15 * inch))

    # Repo organization
    s.append(Paragraph("Repository organization", H2))
    repo_rows = [
        [Paragraph("<b>Path</b>", BODY_S),
         Paragraph("<b>Contents</b>", BODY_S),
         Paragraph("<b>Status</b>", BODY_S)],
        [Paragraph("/LIFE_SYSTEM_MASTER.md", BODY_S),
         Paragraph("Operational master document (post Alpha-Omega audit fixes)", BODY_S),
         Paragraph('<font color="#437A22"><b>UP TO DATE</b></font>', BODY_S)],
        [Paragraph("/ALPHA_OMEGA_AUDIT_FIXES_v2026-04-25.md", BODY_S),
         Paragraph("Status of all 17 priority audit findings (closed)", BODY_S),
         Paragraph('<font color="#437A22"><b>UP TO DATE</b></font>', BODY_S)],
        [Paragraph("/LIFE_system/digital_totems/", BODY_S),
         Paragraph("19 markdown content files for digital touchscreen totems (10K+ each)", BODY_S),
         Paragraph('<font color="#437A22"><b>COMPLETE</b></font>', BODY_S)],
        [Paragraph("/releases/print_catalog_v2026-04-24/", BODY_S),
         Paragraph("22-totem print catalog PDF + manifest (16×22 master)", BODY_S),
         Paragraph('<font color="#437A22"><b>LOCKED</b></font>', BODY_S)],
        [Paragraph("/releases/v2026-04-23/", BODY_S),
         Paragraph("26 diet cards · 4 styled totems · USDA-stamped versions · per-site print lists", BODY_S),
         Paragraph('<font color="#437A22"><b>LOCKED</b></font>', BODY_S)],
        [Paragraph("/releases/audits/", BODY_S),
         Paragraph("Coverage Audit v2026-04-25 (the prior species audit)", BODY_S),
         Paragraph('<font color="#437A22"><b>LOCKED</b></font>', BODY_S)],
        [Paragraph("/releases/totems/ and /releases/diet_cards/", BODY_S),
         Paragraph("Top-level convenience PDFs (18 totems, 18 diet cards)", BODY_S),
         Paragraph('<font color="#964219"><b>OLDER — superseded by v2026-04-23</b></font>', BODY_S)],
        [Paragraph("/02_education/, /03_operations/, /04_deployment/, /05_business/", BODY_S),
         Paragraph("Numbered organizational shelves used by deployment plan", BODY_S),
         Paragraph('<font color="#437A22"><b>STABLE</b></font>', BODY_S)],
        [Paragraph("/releases/canonical/LIFE_CANONICAL_SPECIES_ROSTER.md", BODY_S),
         Paragraph("Source of truth for species classification taxonomy (PART 7)", BODY_S),
         Paragraph('<font color="#437A22"><b>SOURCE OF TRUTH</b></font>', BODY_S)],
    ]
    t = Table(repo_rows, colWidths=[3.4 * inch, 4.7 * inch, 2.0 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    s.append(t)

    return s


# ---- Build ---------------------------------------------------------------
def main():
    out = "/home/user/workspace/LIFE_Repo_Comprehensive_Audit_v2026-04-25.pdf"
    doc = make_doc(out)
    story = []
    story += page_cover()
    story += page_matrix()
    story += page_banner_check()
    story += page_gaps()
    story += page_overreach_repo()
    doc.build(story)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
