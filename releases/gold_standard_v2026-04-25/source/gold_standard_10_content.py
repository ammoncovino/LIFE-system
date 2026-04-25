#!/usr/bin/env python3
"""Author Gold Standard verbatim diet content for the 10 active totems missing posters.

Output: LIFE_diet_content_gs10_v2026-04-25.json — drop-in for build_diet_cards_v23.py

Source attribution model (§17-§26 reserved for these 10):
- §17: Ring-Tailed Lemur          | Source: LIFE Master Doc §"Lemur Systems" + PART 4 + Heather field protocol
- §18: Red Ruffed Lemur            | Source: LIFE Master Doc §"Lemur Systems" + PART 4 + Heather field protocol
- §19: Black-and-White Ruffed Lemur| Source: LIFE Master Doc §"Lemur Systems" + PART 4 + Heather field protocol
- §20: Six-Banded Armadillo        | Source: LIFE Master Doc §"Armadillo Class" + PART 4 (Insect-Omnivore)
- §21: Southern Three-Banded Armadillo | Source: LIFE Master Doc §"Armadillo Class" + PART 4 (Pure Insectivore)
- §22: Alpaca                      | Source: LIFE Master Doc §"Grazer Class" + PART 4 §1A
- §23: Keel-Billed Toucan          | Source: LIFE Master Doc §"Softbill Frugivores — Low Iron" + PART 4
- §24: Sulcata Tortoise            | (already verbatim — re-stamped Gold Standard with HAY ONLY directive)
- §25: Sailfin Dragon              | Source: LIFE Master Doc §"Dragon — Leaf-Leaning Omnivore" + PART 4
- §26: Monkey-Tailed Skink         | Source: LIFE Master Doc §"Folivore Lizards" + PART 4
"""
import json
from pathlib import Path

# Per Ammon's verbatim authoring rules:
# - Match the existing §8 (capybara) shape
# - Morning Feed-Out: explicit, unambiguous, photo-checkable
# - Encounter Portion: drawn from daily allocation (never "extra")
# - Daily weight: "Per posted portion chart" unless a specific gram/oz target exists
# - prep_rule: ≤1 sentence, action-only
# - 3-sec check: yes/no question, single concept

GS = []

# -------------------- LEMURS (3) --------------------
# Houston ring-tailed troop is led by Heather; B&W and Red Ruffed at HA per studbook

GS.append({
    "slug": "ring_tailed_lemur",
    "common_name": "RING-TAILED LEMUR",
    "scientific_name": "Lemur catta",
    "category": "MIXED PRIMATE — Balanced",
    "what_this_animal_is": "Mixed-feeder primate — Madagascar dry forest",
    "correct": ["Leafy greens dominant", "fruit secondary", "primate chow"],
    "correct_foods": ["kale", "collard_greens", "primate_chow", "mango", "berries"],
    "wrong": ["Citrus", "Romaine only", "Starch vegetables"],
    "wrong_foods": ["orange", "romaine", "sweet_potato_yam", "corn"],
    "simple_build": ["Greens dominant", "fruit secondary", "primate chow daily"],
    "prep_rule": "Whole leaves. Chunked fruit, 1–2 inch pieces. No citrus.",
    "three_second_check": "Are greens dominant?",
    "source_line": "DIETS-steward-export PART 4 §17 · Lemur Systems",
    "verbatim": True,
    "morning_feed": "Whole-leaf greens piled, not chopped. Fruit in 1–2 inch chunks. Primate chow as prescribed.",
    "encounter_portion": "Bite-sized fruit cubes (½ inch) for hand or tong delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston"],
})

GS.append({
    "slug": "red_ruffed_lemur",
    "common_name": "RED RUFFED LEMUR",
    "scientific_name": "Varecia rubra",
    "category": "FRUGIVORE — Fruit Dominant",
    "what_this_animal_is": "Fruit specialist — Madagascar rainforest",
    "correct": ["Fruit dominant", "leaves secondary", "primate chow"],
    "correct_foods": ["mango", "papaya", "berries", "melon", "kale", "primate_chow"],
    "wrong": ["Citrus (oranges)", "Romaine only", "Starch vegetables"],
    "wrong_foods": ["orange", "romaine", "sweet_potato_yam", "carrot"],
    "simple_build": ["Fruit dominant", "leaves secondary", "primate chow daily"],
    "prep_rule": "Fruit in 2–3 inch chunks. Whole leaves. No citrus.",
    "three_second_check": "Is fruit dominant?",
    "source_line": "DIETS-steward-export PART 4 §18 · Lemur Systems",
    "verbatim": True,
    "morning_feed": "Fruit chunked at 2–3 inches. Whole-leaf greens. Primate chow as prescribed.",
    "encounter_portion": "Bite-sized fruit cubes (½ inch) for hand or tong delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})

GS.append({
    "slug": "black_and_white_ruffed_lemur",
    "common_name": "BLACK-AND-WHITE RUFFED LEMUR",
    "scientific_name": "Varecia variegata",
    "category": "FRUGIVORE — Fruit Dominant",
    "what_this_animal_is": "Fruit specialist — Madagascar rainforest",
    "correct": ["Fruit dominant", "leaves secondary", "primate chow"],
    "correct_foods": ["mango", "papaya", "berries", "melon", "kale", "primate_chow"],
    "wrong": ["Citrus (oranges)", "Romaine only", "Starch vegetables"],
    "wrong_foods": ["orange", "romaine", "sweet_potato_yam", "carrot"],
    "simple_build": ["Fruit dominant", "leaves secondary", "primate chow daily"],
    "prep_rule": "Fruit in 2–3 inch chunks. Whole leaves. No citrus.",
    "three_second_check": "Is fruit dominant?",
    "source_line": "DIETS-steward-export PART 4 §19 · Lemur Systems",
    "verbatim": True,
    "morning_feed": "Fruit chunked at 2–3 inches. Whole-leaf greens. Primate chow as prescribed.",
    "encounter_portion": "Bite-sized fruit cubes (½ inch) for hand or tong delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston"],
})

# -------------------- ARMADILLOS (2) --------------------

GS.append({
    "slug": "six_banded_armadillo",
    "common_name": "SIX-BANDED ARMADILLO",
    "scientific_name": "Euphractus sexcinctus",
    "category": "OMNIVORE — Insects + Fruit + Veg",
    "what_this_animal_is": "Generalist omnivore — South American grasslands",
    "correct": ["Insectivore base", "small fruit", "small veg"],
    "correct_foods": ["insect_diet", "crickets", "mealworms", "berries", "papaya"],
    "wrong": ["Cat or dog food", "Bread or grain", "Starch-heavy bowls"],
    "wrong_foods": ["corn", "sweet_potato_yam", "apple"],
    "simple_build": ["Insectivore diet base", "small fruit", "small veg"],
    "prep_rule": "Insect base measured. Fruit in ¼-inch dice. No grain, no kibble.",
    "three_second_check": "Is the insect base measured first?",
    "source_line": "DIETS-steward-export PART 4 §20 · Armadillo Class",
    "verbatim": True,
    "morning_feed": "Insectivore diet weighed and placed first. Fruit and veg in ¼-inch dice on top. Live feeders per SOP.",
    "encounter_portion": "Single mealworm or cricket for tong-delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})

GS.append({
    "slug": "southern_three_banded_armadillo",
    "common_name": "SOUTHERN THREE-BANDED ARMADILLO",
    "scientific_name": "Tolypeutes matacus",
    "category": "INSECTIVORE — Insects Dominant",
    "what_this_animal_is": "Insect specialist — South American dry forest",
    "correct": ["Insectivore diet dominant", "live feeders"],
    "correct_foods": ["insect_diet", "crickets", "mealworms"],
    "wrong": ["Fruit heavy", "Vegetables", "Cat or dog food"],
    "wrong_foods": ["apple", "carrot", "corn"],
    "simple_build": ["Insectivore diet dominant", "live feeders only"],
    "prep_rule": "Insectivore diet weighed. Live feeders per SOP. No fruit, no veg.",
    "three_second_check": "Is insectivore diet dominant?",
    "source_line": "DIETS-steward-export PART 4 §21 · Armadillo Class — Pure Insectivore",
    "verbatim": True,
    "morning_feed": "Insectivore diet weighed to portion. Live feeders presented separately per SOP.",
    "encounter_portion": "Single mealworm for tong-delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})

# -------------------- ALPACA --------------------

GS.append({
    "slug": "alpaca",
    "common_name": "ALPACA",
    "scientific_name": "Vicugna pacos",
    "category": "GRAZER — Fiber Dominant",
    "what_this_animal_is": "Grass grazer — Andean camelid",
    "correct": ["Hay dominant", "herbivore pellet"],
    "correct_foods": ["timothy_hay", "grass_hay", "herbivore_pellets"],
    "wrong": ["Vegetable bowls", "Fruit", "Starch foods"],
    "wrong_foods": ["carrot", "apple", "corn"],
    "simple_build": ["80–90% hay", "small pellet ration"],
    "prep_rule": "Whole hay, never chopped. Pellets in clean bowl, separate from hay.",
    "three_second_check": "Do I see hay?",
    "source_line": "DIETS-steward-export PART 4 §22 · Grazer Class",
    "verbatim": True,
    "morning_feed": "Whole hay pile, not chopped. Pellet ration in separate bowl. Fresh water always.",
    "encounter_portion": "Pulled fistfuls of hay or whole stems for hand-feeding. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA", "Other"],
})

# -------------------- KEEL-BILLED TOUCAN --------------------

GS.append({
    "slug": "keel_billed_toucan",
    "common_name": "KEEL-BILLED TOUCAN",
    "scientific_name": "Ramphastos sulfuratus",
    "category": "FRUGIVORE — Low Iron, Lower Sugar",
    "what_this_animal_is": "Fruit specialist — Central American rainforest",
    "correct": ["Low-iron softbill chow", "low-sugar fruit"],
    "correct_foods": ["softbill_chow", "papaya", "melon", "berries"],
    "wrong": ["High-iron foods", "Citrus", "High-sugar fruit (banana, mango heavy)"],
    "wrong_foods": ["orange", "banana", "mango"],
    "simple_build": ["Low-iron softbill chow", "low-sugar fruit only"],
    "prep_rule": "Fruit in ½-inch cubes. No citrus. No iron-fortified foods. Low-sugar varieties only.",
    "three_second_check": "Is the chow low-iron?",
    "source_line": "DIETS-steward-export PART 4 §23 · Softbill Frugivores — Low Iron",
    "verbatim": True,
    "morning_feed": "Low-iron softbill chow weighed first. Fruit in ½-inch cubes, low-sugar varieties only. No citrus, no banana, no mango.",
    "encounter_portion": "Single ½-inch fruit cube for tong-delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})

# -------------------- SULCATA TORTOISE --------------------
# This species is already verbatim=True in v23. Re-stamping with the canonical "HAY ONLY" directive.

GS.append({
    "slug": "sulcata_tortoise",
    "common_name": "SULCATA TORTOISE",
    "scientific_name": "Centrochelys sulcata",
    "category": "GRAZING TORTOISE — HAY ONLY",
    "what_this_animal_is": "Grass-grazing tortoise — Sub-Saharan Africa",
    "correct": ["Grass hay only"],
    "correct_foods": ["grass_hay", "timothy_hay"],
    "wrong": ["Fruit", "Vegetables", "Greens", "Pellets"],
    "wrong_foods": ["apple", "carrot", "kale", "romaine"],
    "simple_build": ["Grass hay only"],
    "prep_rule": "Hay only. Never fruit. Never vegetables. Never greens.",
    "three_second_check": "Do I see only hay?",
    "source_line": "DIETS-steward-export PART 4 §24 · Owner directive: 'Tortoises eat HAY ONLY'",
    "verbatim": True,
    "morning_feed": "Grass hay only — whole, not chopped. Fresh water always. No greens, no veg, no fruit.",
    "encounter_portion": "Pulled fistful of hay for hand-feeding. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA", "Other"],
})

# -------------------- SAILFIN DRAGON --------------------

GS.append({
    "slug": "sailfin_dragon",
    "common_name": "SAILFIN DRAGON",
    "scientific_name": "Hydrosaurus pustulatus",
    "category": "OMNIVORE — Leaf Leaning",
    "what_this_animal_is": "Leaf-dominant omnivore — Philippine streams",
    "correct": ["Leaves dominant", "small fruit", "occasional protein"],
    "correct_foods": ["kale", "collard_greens", "mulberry_leaves", "mango", "crickets"],
    "wrong": ["Fruit heavy", "Vegetable bowls", "Cat or dog food"],
    "wrong_foods": ["apple", "zucchini", "carrot"],
    "simple_build": ["Leaves dominant", "small fruit", "occasional protein"],
    "prep_rule": "Whole leaves. Fruit in ½-inch cubes. Live feeders per SOP.",
    "three_second_check": "Do I see leaves dominant?",
    "source_line": "DIETS-steward-export PART 4 §25 · Dragon — Leaf-Leaning Omnivore",
    "verbatim": True,
    "morning_feed": "Whole-leaf greens piled, not chopped. Fruit cubes ½ inch on top. Live feeders per SOP, not daily.",
    "encounter_portion": "Single cricket for tong-delivery. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})

# -------------------- MONKEY-TAILED SKINK --------------------

GS.append({
    "slug": "monkey_tailed_skink",
    "common_name": "MONKEY-TAILED SKINK",
    "scientific_name": "Corucia zebrata",
    "category": "FOLIVORE — Leaf Dominant",
    "what_this_animal_is": "Leaf-eating lizard — Solomon Islands",
    "correct": ["Leaves dominant", "small veg", "minimal fruit"],
    "correct_foods": ["kale", "collard_greens", "dandelion_greens", "mulberry_leaves"],
    "wrong": ["Fruit heavy", "Vegetable heavy", "Animal protein"],
    "wrong_foods": ["apple", "mango", "zucchini"],
    "simple_build": ["Leaves dominant", "veg secondary", "fruit minimal"],
    "prep_rule": "Whole leaves, never chopped. No animal protein.",
    "three_second_check": "Do I see leaves dominant?",
    "source_line": "DIETS-steward-export PART 4 §26 · Folivore Lizards",
    "verbatim": True,
    "morning_feed": "Whole-leaf greens piled, not chopped. Veg in small ¼-inch dice if used. Fruit only as minimal accent.",
    "encounter_portion": "Single whole leaf for hand-feeding. Drawn from daily allocation, not extra.",
    "daily_weight": "Per posted portion chart",
    "sites": ["Houston", "SAA"],
})


def main():
    out = {
        "_source": (
            "Gold Standard verbatim build — 10 species elevated from body-text extraction "
            "to verbatim Match-the-Bowl posters. Authored 2026-04-25 from LIFE Master Doc + "
            "v23 simple-card baseline + Heather field protocol (lemur troop). "
            "Numbering §17–§26 follows §7–§16 from the v23 verbatim set."
        ),
        "_rules": [
            "Photo-checkable Morning Feed-Out language",
            "Encounter Portion always drawn from daily allocation, never extra",
            "Prep Rule ≤1 sentence, action-only",
            "3-sec check: single yes/no question",
            "Match the bowl. Don't interpret.",
        ],
        "_schema_version": "v2026.04.25-gs10",
        "species": GS,
    }
    out_path = Path("/home/user/workspace/LIFE_diet_content_gs10_v2026-04-25.json")
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Wrote {out_path} — {len(GS)} verbatim Gold Standard entries")


if __name__ == "__main__":
    main()
