#!/usr/bin/env python3
"""
Build LIFE v2026.04.23 diet content.

Start from base 18-species content; add:
  - New framing fields: morning_feed, encounter_portion, daily_weight
  - 3 new species from Mia's feedback:
      keel_billed_toucan, southern_three_banded_armadillo, six_banded_armadillo
  - 5 new reptile species:
      chinese_water_dragon, veiled_chameleon, leopard_tortoise,
      russian_tortoise, yellow_foot_tortoise
  - Per-site availability (Houston, SAA, etc.) for print subset lists
"""
import json
from pathlib import Path

BASE = Path("/home/user/workspace/LIFE_v2026-04-23/content/LIFE_diet_content_18_base.json")
OUT = Path("/home/user/workspace/LIFE_v2026-04-23/content/LIFE_diet_content_v23.json")

# Universal framing band defaults by diet category
# Applied to each species based on its category. Species can override.
DEFAULT_FRAMING = {
    "GRAZER": {
        "morning_feed": "Whole hay pile. Greens in large leaves, stems intact. No chopping.",
        "encounter_portion": "Pulled fistfuls of hay or whole leafy stems for hand-feeding. Drawn from daily allocation.",
    },
    "FOLIVORE": {
        "morning_feed": "Whole leaves, browse branches. Keep stems — they're enrichment.",
        "encounter_portion": "Single leaves or short stem sections for keeper-guided offering.",
    },
    "FRUGIVORE": {
        "morning_feed": "Fruit in 2-3 inch chunks. Softbill/primate chow as prescribed.",
        "encounter_portion": "Bite-sized cubes (1/2 inch) for hand or tong delivery. Part of daily allocation, not extra.",
    },
    "OMNIVORE": {
        "morning_feed": "Main components whole or in large chunks. Minimal processing.",
        "encounter_portion": "Bite-sized pieces of approved items for guided interaction.",
    },
    "INSECTIVORE": {
        "morning_feed": "Insect diet in flat bowl. Live feeders per SOP.",
        "encounter_portion": "Live feeders offered by tongs during keeper encounter. Count toward daily allocation.",
    },
    "ROOT_LEAF": {
        "morning_feed": "Whole roots or halved large roots. Leafy greens whole.",
        "encounter_portion": "Root chunks (1 inch) for hand-feeding during encounter.",
    },
    "MIXED_PRIMATE": {
        "morning_feed": "Balanced bowl: fruit chunks, whole greens, chow as prescribed.",
        "encounter_portion": "Bite-sized cubes. Forage scatter permitted if keeper supervises.",
    },
    "HAY_ONLY": {
        "morning_feed": "Grass hay pile only. No supplementation.",
        "encounter_portion": "Whole hay handfuls for hand-feeding. Nothing else.",
    },
    "REPTILE_OMNIVORE": {
        "morning_feed": "Greens dominant, protein/fruit minor. Chopped to fit mouth size.",
        "encounter_portion": "Targeted single-piece feeding by tongs during keeper encounter.",
    },
}


def infer_framing_key(category: str) -> str:
    c = category.upper()
    if "GRAZER" in c: return "GRAZER"
    if "FOLIVORE" in c: return "FOLIVORE"
    if "FRUGIVORE" in c: return "FRUGIVORE"
    if "OMNIVORE" in c and "REPTILE" not in c:
        # Tegu
        return "OMNIVORE"
    if "INSECTIVORE" in c: return "INSECTIVORE"
    if "ROOT" in c: return "ROOT_LEAF"
    if "MIXED" in c or "PRIMATE" in c: return "MIXED_PRIMATE"
    if "HAY" in c: return "HAY_ONLY"
    if "REPTILE" in c or "DRAGON" in c or "CHAMELEON" in c:
        return "REPTILE_OMNIVORE"
    return "OMNIVORE"


def attach_framing(sp: dict) -> dict:
    """Add morning_feed + encounter_portion + daily_weight if missing."""
    if "morning_feed" not in sp or "encounter_portion" not in sp:
        key = infer_framing_key(sp.get("category", ""))
        defaults = DEFAULT_FRAMING.get(key, DEFAULT_FRAMING["OMNIVORE"])
        sp.setdefault("morning_feed", defaults["morning_feed"])
        sp.setdefault("encounter_portion", defaults["encounter_portion"])
    # daily weight fallback — will be refined per species below
    sp.setdefault("daily_weight", "Per posted portion chart")
    sp.setdefault("sites", ["Houston", "SAA", "Other"])  # default: all sites
    return sp


# ============================================================
# NEW SPECIES — Mia's feedback + reptile expansion
# ============================================================

NEW_SPECIES = [
    # --- Mia's 3 ---
    {
        "slug": "keel_billed_toucan",
        "common_name": "KEEL-BILLED TOUCAN",
        "scientific_name": "Ramphastos sulfuratus",
        "category": "FRUGIVORE — Low Iron, Lower Sugar",
        "what_this_animal_is": "Fruit + low iron + sugar-sensitive",
        "correct": ["Fruit dominant · softbill · lower sugar"],
        "correct_foods": [
            "berries", "apple", "pear", "melon",
            "papaya", "leafy_greens_mix", "softbill_chow",
        ],
        "wrong": ["High-sugar fruit heavy · Iron-rich foods · Pellet heavy"],
        "wrong_foods": [
            "banana", "mango", "orange",
            "herbivore_pellets", "primate_chow",
        ],
        "simple_build": [
            "60–70% fruit (lower-sugar bias)",
            "Low-iron softbill chow",
            "Small leafy greens portion",
        ],
        "prep_rule": "Chunked fruit (2\" pieces). Low-iron softbill chow only. Limit banana/mango/papaya to trace amounts — these cause loose stool in keel-billed.",
        "three_second_check": "Do I see berries or pear — not banana or mango?",
        "morning_feed": "Fruit in 2\" chunks, lower-sugar bias (berries/apple/pear lead). Softbill chow in separate bowl. Fruit visible and dominant.",
        "encounter_portion": "1/2\" cubes of approved lower-sugar fruits for tong delivery. Never hand-feed banana or mango — even a small piece can cause loose stool.",
        "daily_weight": "~120–180 g fruit + chow (keeper posts exact portion)",
        "sites": ["Houston"],  # Houston has keel-billed per Mia
        "source_line": "DIETS-steward-export PART 7 §1C (frugivore low-iron) + Mia Ketsa field note (keel-billed sugar sensitivity)",
        "verbatim": False,
        "notes": "Keeper note (Mia, 4/22/26): 'Keel-billed are a little more sensitive to higher sugar diets — gives em the runs.' Lock low-sugar bias.",
    },
    {
        "slug": "southern_three_banded_armadillo",
        "common_name": "SOUTHERN THREE-BANDED ARMADILLO",
        "scientific_name": "Tolypeutes matacus",
        "category": "INSECTIVORE — Insects Dominant",
        "what_this_animal_is": "Insect-eating armored mammal",
        "correct": ["Insect diet dominant"],
        "correct_foods": [
            "insect_diet", "mealworms", "crickets", "cooked_egg",
        ],
        "wrong": ["Fruit heavy · Vegetable bowls · Large pieces"],
        "wrong_foods": ["apple", "mango", "carrot", "zucchini"],
        "simple_build": [
            "80–90% commercial insectivore diet",
            "Live feeders per SOP",
            "Trace cooked egg",
        ],
        "prep_rule": "Insectivore diet in flat shallow bowl. Live feeders (mealworms/crickets) per keeper SOP.",
        "three_second_check": "Do I see insect diet — not fruit?",
        "daily_weight": "~40–60 g insect diet + feeders",
        "sites": ["Houston", "SAA", "Other"],
        "source_line": "DIETS-steward-export PART 7 §1E (insectivore class)",
        "verbatim": False,
        "notes": "All LIFE sites have three-banded (per Mia, 4/22/26). No site has nine-banded at present. Nine-banded card retained in master binder for historical reference / future arrivals.",
    },
    {
        "slug": "six_banded_armadillo",
        "common_name": "SIX-BANDED ARMADILLO",
        "scientific_name": "Euphractus sexcinctus",
        "category": "OMNIVORE — Insects + Fruit + Veg",
        "what_this_animal_is": "Omnivorous armored mammal (broader diet than 3-banded)",
        "correct": ["Insect dominant + fruit + veg + small protein"],
        "correct_foods": [
            "insect_diet", "mealworms", "crickets",
            "cooked_egg", "apple", "sweet_potato_yam",
            "leafy_greens_mix", "raw_meat_ground",
        ],
        "wrong": ["Fruit only · Insect only · Commercial cat/dog food"],
        "wrong_foods": ["banana", "orange", "carrot"],
        "simple_build": [
            "50% insect diet / live feeders",
            "25% fruit + veg",
            "15% lean protein (egg / ground meat)",
            "10% leafy greens",
        ],
        "prep_rule": "Insect portion in one bowl, mixed fruit/veg/protein in second. Chop fruit/veg to 1/2\" cubes.",
        "three_second_check": "Do I see insects AND some fruit/veg?",
        "daily_weight": "~80–120 g total (keeper posts exact)",
        "sites": ["SAA"],  # only SAA per Mia
        "source_line": "DIETS-steward-export PART 7 §1E (insectivore baseline) + published AZA nutrition standards for Euphractus sexcinctus",
        "verbatim": False,
        "notes": "SAA-only species per Mia, 4/22/26. True omnivore — significantly broader diet than three-banded. Requires keeper confirmation of exact ratio before going live.",
    },
    # --- 5 new reptiles ---
    {
        "slug": "chinese_water_dragon",
        "common_name": "CHINESE WATER DRAGON",
        "scientific_name": "Physignathus cocincinus",
        "category": "REPTILE OMNIVORE — Insect + Plant",
        "what_this_animal_is": "Insectivorous-leaning omnivorous arboreal lizard",
        "correct": ["Insects dominant + greens + small fruit"],
        "correct_foods": [
            "crickets", "mealworms", "insect_diet",
            "leafy_greens_mix", "collard_greens",
            "berries", "papaya",
        ],
        "wrong": ["Dry pellets only · Iceberg lettuce · Citrus"],
        "wrong_foods": ["herbivore_pellets", "orange", "corn"],
        "simple_build": [
            "60–70% live insects (gut-loaded, dusted)",
            "20–30% leafy greens",
            "10% fruit (berry-biased)",
        ],
        "prep_rule": "Gut-loaded live feeders dusted with calcium + D3 per SOP. Greens and fruit chopped small and scattered for foraging. Fresh water daily.",
        "three_second_check": "Do I see live insects and greens?",
        "daily_weight": "~30–50 g (adult)",
        "sites": ["Houston", "Other"],
        "source_line": "AZA Reptile TAG nutrition guidelines (Physignathus cocincinus) + keeper SOP",
        "verbatim": False,
        "notes": "Species confirmation pending — placeholder portion/site data. Requires keeper sign-off before print.",
    },
    {
        "slug": "veiled_chameleon",
        "common_name": "VEILED CHAMELEON",
        "scientific_name": "Chamaeleo calyptratus",
        "category": "INSECTIVORE — Live Feeders Only",
        "what_this_animal_is": "Arboreal insectivore with small plant supplement",
        "correct": ["Live gut-loaded insects dominant"],
        "correct_foods": ["crickets", "mealworms", "collard_greens", "kale"],
        "wrong": ["Fruit heavy · Dead insects · Commercial chow"],
        "wrong_foods": ["apple", "banana", "herbivore_pellets"],
        "simple_build": [
            "85–95% live insects (gut-loaded, dusted)",
            "Small greens garnish",
            "Mist for water",
        ],
        "prep_rule": "Live feeders only — crickets, roaches, silkworms per SOP. Gut-load 24–48h prior. Dust calcium daily, D3 2x/week. Mist branches — chameleons drink droplets, not standing water.",
        "three_second_check": "Do I see live, moving feeders?",
        "daily_weight": "~10–20 live feeders/day (adult)",
        "sites": ["Houston", "Other"],
        "source_line": "AZA Reptile TAG + ARAV veterinary nutrition standards (Chamaeleo calyptratus)",
        "verbatim": False,
        "notes": "NOT a morning-feed species — live feeders offered during keeper SOP only. Cross-listed on master for completeness.",
    },
    {
        "slug": "leopard_tortoise",
        "common_name": "LEOPARD TORTOISE",
        "scientific_name": "Stigmochelys pardalis",
        "category": "HAY + GRASSES — Grazer (with limited greens)",
        "what_this_animal_is": "African grassland grazing tortoise",
        "correct": ["Grass hay + pasture grasses dominant"],
        "correct_foods": [
            "timothy_hay", "grass_hay", "browse_branches",
            "dandelion_greens", "mulberry_leaves", "collard_greens",
        ],
        "wrong": ["Fruit · Commercial tortoise pellets · High-protein greens"],
        "wrong_foods": ["apple", "banana", "kale", "herbivore_pellets"],
        "simple_build": [
            "80% grass hay + fresh grasses",
            "15% coarse greens (dandelion, mulberry)",
            "5% browse",
            "NO FRUIT",
        ],
        "prep_rule": "Whole hay pile. Fresh grasses cut long. Greens whole. NO fruit — leopard tortoises are strict grazers; fruit causes diarrhea and shell issues.",
        "three_second_check": "Do I see grass hay — and NO fruit?",
        "daily_weight": "Hay ad-lib + ~150–250 g fresh greens",
        "sites": ["Houston", "SAA", "Other"],
        "source_line": "AZA Chelonian TAG + Sulcata/Leopard nutrition guidelines",
        "verbatim": False,
        "notes": "Similar to sulcata — NO fruit rule is firm. Mia / keeper to confirm site availability before print.",
    },
    {
        "slug": "russian_tortoise",
        "common_name": "RUSSIAN TORTOISE",
        "scientific_name": "Testudo horsfieldii",
        "category": "HERBIVORE — Leafy Greens + Hay",
        "what_this_animal_is": "Steppe herbivore — broadleaf greens dominant",
        "correct": ["Broadleaf greens + hay dominant"],
        "correct_foods": [
            "dandelion_greens", "collard_greens", "kale",
            "romaine", "mulberry_leaves", "grass_hay",
        ],
        "wrong": ["Fruit · Spinach · Iceberg · High-oxalate greens"],
        "wrong_foods": ["apple", "banana", "berries", "orange"],
        "simple_build": [
            "70–80% broadleaf greens",
            "15% grass hay",
            "5% browse/weeds (dandelion, plantain)",
            "Trace fruit only (occasional)",
        ],
        "prep_rule": "Whole leaves. Rotate greens to prevent oxalate buildup. Fresh water daily. NO cruciferous excess (limit kale to 1–2x/week).",
        "three_second_check": "Do I see mixed leafy greens?",
        "daily_weight": "~80–120 g greens + hay ad-lib",
        "sites": ["Houston", "SAA", "Other"],
        "source_line": "AZA Chelonian TAG + Testudo nutrition standards",
        "verbatim": False,
        "notes": "Smaller than sulcata/leopard — separate portion chart. Avoid oxalate-heavy greens (spinach, beet greens).",
    },
    {
        "slug": "yellow_foot_tortoise",
        "common_name": "YELLOW-FOOTED TORTOISE",
        "scientific_name": "Chelonoidis denticulatus",
        "category": "OMNIVORE — Fruit + Greens + Trace Protein",
        "what_this_animal_is": "Amazonian forest tortoise — more frugivorous than grassland species",
        "correct": ["Fruit + greens + browse dominant"],
        "correct_foods": [
            "papaya", "mango", "berries", "melon",
            "collard_greens", "kale", "mulberry_leaves",
            "browse_branches",
        ],
        "wrong": ["Hay only · High-protein daily · Dog food"],
        "wrong_foods": ["timothy_hay", "raw_meat_ground"],
        "simple_build": [
            "40–50% fruit (tropical)",
            "30–40% leafy greens + browse",
            "5% trace protein (cooked egg, weekly)",
            "Water available",
        ],
        "prep_rule": "Fruit in 1\" chunks. Greens whole. Trace protein (cooked egg, mazuri pellet) 1–2x/week only. Humid environment — mist enclosure daily.",
        "three_second_check": "Do I see fruit AND greens?",
        "daily_weight": "~150–220 g mixed (keeper posts)",
        "sites": ["Houston", "Other"],
        "source_line": "AZA Chelonian TAG + Chelonoidis denticulatus nutrition standards",
        "verbatim": False,
        "notes": "IMPORTANT: Yellow-foot is rainforest, NOT grassland. Fruit IS appropriate — do not apply sulcata/leopard 'NO fruit' rule. Humidity 70–80%.",
    },
]


def main():
    base = json.loads(BASE.read_text())
    species = base["species"]

    # Add framing fields + site lists to existing 18
    # Site mapping: per user, Houston and SAA have different rosters; master binder is the union.
    # Default for existing species: all sites unless known-specific.
    for sp in species:
        attach_framing(sp)
        if sp["slug"] == "nine_banded_armadillo":
            sp["sites"] = []  # historical — no current site
            sp["notes"] = "Historical reference. No current LIFE site has nine-banded as of v2026.04.23. See three-banded + six-banded cards for live species."
        if sp["slug"] == "toco_toucan":
            sp["sites"] = []  # historical — no current site has Toco per Mia
            sp["notes"] = "Historical reference. No current LIFE site has Toco toucan as of v2026.04.23. Houston has keel-billed — see separate card."

    # Add new species (already have framing)
    for sp in NEW_SPECIES:
        attach_framing(sp)
        species.append(sp)

    # Schema version bump
    base["_schema_version"] = "2026.04.23"
    base["_changes"] = [
        "Added morning_feed + encounter_portion + daily_weight fields to all species",
        "Added per-site availability (sites field)",
        "Added 8 new species: keel-billed toucan, southern 3-banded armadillo, six-banded armadillo, chinese water dragon, veiled chameleon, leopard tortoise, russian tortoise, yellow-foot tortoise",
        "Marked toco_toucan and nine_banded_armadillo as historical (no current site)",
    ]
    base["species"] = species

    OUT.write_text(json.dumps(base, indent=2, ensure_ascii=False))
    print(f"✓ Wrote {OUT}")
    print(f"  Total species: {len(species)}")
    print(f"  Historical (no site): {sum(1 for s in species if not s.get('sites'))}")
    print(f"  Active: {sum(1 for s in species if s.get('sites'))}")
    for sp in species:
        sites = sp.get("sites", [])
        tag = f"[{','.join(sites)}]" if sites else "[HIST]"
        print(f"  {tag:20s} {sp['common_name']}")


if __name__ == "__main__":
    main()
