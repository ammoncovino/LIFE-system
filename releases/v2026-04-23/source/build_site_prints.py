"""Generate per-site print subset lists (markdown) from LIFE_diet_content_v23.json."""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/user/workspace/LIFE_v2026-04-23")
CONTENT = ROOT / "content" / "LIFE_diet_content_v23.json"
OUT_DIR = ROOT / "site_prints"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Slug mapping: diet-content slug (underscore) -> totem slug (hyphen)
DIET_TO_TOTEM = {
    "capybara": "capybara",
    "rabbit": "rabbit",
    "patagonian_mara": "patagonian-mara",
    "wallaby": "bennetts-wallaby",
    "alpaca": "alpaca",
    "two_toed_sloth": "linnes-two-toed-sloth",
    "monkey_tailed_skink": "monkey-tailed-skink",
    "spider_monkey": "geoffroys-spider-monkey",
    "red_ruffed_lemur": "red-ruffed-lemur",
    "black_and_white_ruffed_lemur": "black-and-white-ruffed-lemur",
    "toco_toucan": "toco-toucan",
    "kinkajou": "kinkajou",
    "argentine_tegu": "argentine-tegu",
    "nine_banded_armadillo": "nine-banded-armadillo",
    "prehensile_tailed_porcupine": "prehensile-tailed-porcupine",
    "ring_tailed_lemur": "ring-tailed-lemur",
    "sulcata_tortoise": "sulcata-tortoise",
    "sailfin_dragon": "sailfin-dragon",
    "keel_billed_toucan": "keel-billed-toucan",
    "southern_three_banded_armadillo": "southern-three-banded-armadillo",
    "six_banded_armadillo": "six-banded-armadillo",
    "chinese_water_dragon": None,       # no totem this release
    "veiled_chameleon": None,
    "leopard_tortoise": None,
    "russian_tortoise": None,
    "yellow_foot_tortoise": None,
}

# USDA-regulated: all mammals + all birds get a totem with USDA banner
USDA_SLUGS = {
    "capybara", "rabbit", "patagonian-mara", "bennetts-wallaby", "alpaca",
    "linnes-two-toed-sloth", "geoffroys-spider-monkey", "red-ruffed-lemur",
    "black-and-white-ruffed-lemur", "toco-toucan", "kinkajou",
    "nine-banded-armadillo", "prehensile-tailed-porcupine", "ring-tailed-lemur",
    "keel-billed-toucan", "southern-three-banded-armadillo", "six-banded-armadillo",
}


def main():
    data = json.load(open(CONTENT))
    species = data["species"]
    by_site = defaultdict(list)

    for sp in species:
        for site in sp.get("sites", []):
            by_site[site].append(sp)

    sites = ["Houston", "SAA", "Other"]
    all_md = ["# LIFE v2026.04.23 — Per-Site Print Subset Lists\n",
              "*Generated from `content/LIFE_diet_content_v23.json`. Historical species are excluded (empty `sites` array).*\n"]

    for site in sites:
        entries = sorted(by_site[site], key=lambda s: s["common_name"])
        lines = [f"# LIFE — {site} Site Print List",
                 f"\n**{len(entries)} species on site.**\n",
                 "## Diet Cards to Print (one per species)\n",
                 "| # | Species | Diet Card PDF |",
                 "|---|---------|---------------|"]
        for i, sp in enumerate(entries, 1):
            slug = sp["slug"]
            pdf = f"diet_cards/DietCard_{slug}.pdf"
            lines.append(f"| {i} | {sp['common_name']} ({sp.get('scientific_name','')}) | `{pdf}` |")

        lines += ["\n## Totems to Print (USDA-stamped where applicable)\n",
                  "| # | Species | Totem PDF | USDA Banner |",
                  "|---|---------|-----------|-------------|"]
        n = 0
        for sp in entries:
            totem_slug = DIET_TO_TOTEM.get(sp["slug"])
            if not totem_slug:
                continue
            n += 1
            if totem_slug in USDA_SLUGS:
                pdf = f"totems_usda/TOTEM_{totem_slug}_USDA.pdf"
                usda = "✓"
            else:
                pdf = f"totems/STYLED2_{totem_slug}.pdf"
                usda = ""
            lines.append(f"| {n} | {sp['common_name']} | `{pdf}` | {usda} |")

        lines.append("\n---\n*Part of LIFE v2026.04.23 release — additions to master binder, not replacements.*\n")
        out = OUT_DIR / f"PRINT_LIST_{site}.md"
        out.write_text("\n".join(lines))
        print(f"  wrote {out}  ({len(entries)} species)")
        all_md.append(f"\n\n---\n\n")
        all_md.extend(lines)

    combined = OUT_DIR / "PRINT_LIST_ALL_SITES.md"
    combined.write_text("\n".join(all_md))
    print(f"  wrote {combined}")


if __name__ == "__main__":
    main()
