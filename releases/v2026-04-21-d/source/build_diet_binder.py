"""Combine all 18 diet cards into a single master binder PDF."""
from pypdf import PdfWriter, PdfReader
from pathlib import Path

SLUGS = [
    "capybara","rabbit","patagonian_mara","wallaby","alpaca","two_toed_sloth",
    "monkey_tailed_skink","spider_monkey","red_ruffed_lemur",
    "black_and_white_ruffed_lemur","toco_toucan","kinkajou","argentine_tegu",
    "nine_banded_armadillo","prehensile_tailed_porcupine","ring_tailed_lemur",
    "sulcata_tortoise","sailfin_dragon",
]

src = Path("/home/user/workspace/LIFE_system/diet_cards")
out = Path("/home/user/workspace/LIFE_system/LIFE_diet_cards_all_18_v2026-04-21-d.pdf")

writer = PdfWriter()
for slug in SLUGS:
    pdf_path = src / f"DietCard_{slug}.pdf"
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        writer.add_page(page)

writer.add_metadata({
    "/Title": "LIFE Diet Cards — All 18 (v2026.04.21-d)",
    "/Author": "Perplexity Computer",
})

with open(out, "wb") as f:
    writer.write(f)

print(f"Wrote {out} — {out.stat().st_size:,} bytes, {len(SLUGS)} cards")
