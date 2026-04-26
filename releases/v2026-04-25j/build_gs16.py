#!/usr/bin/env python3
"""Build the 16 missing Gold Standard posters for v2026-04-25j.

Reuses build_gold_standard_posters.build_poster + a new content table
modeled after LIFE_diet_content_gs10_v2026-04-25e.json.
"""
import json
import sys
from pathlib import Path

# Wire up the existing builder
GS_BUILDER_DIR = Path("/tmp/LIFE-push/releases/gold_standard_v2026-04-25/source")
sys.path.insert(0, str(GS_BUILDER_DIR))

# v23 base
V23_SRC = Path("/tmp/LIFE-push/releases/v2026-04-23/source")
sys.path.insert(0, str(V23_SRC))

import build_diet_cards_v23 as v23  # noqa: E402
import build_gold_standard_posters as gsbuilder  # noqa: E402

# Add slug aliases for any new species (renderer falls back to [photo] if missing)
v23.SPECIES_SLUG.update({
    "yellow_footed_tortoise": "yellow_footed_tortoise",
    "leopard_tortoise": "leopard_tortoise",
    "russian_tortoise": "russian_tortoise",
    "chinese_water_dragon": "chinese_water_dragon",
    "veiled_chameleon": "veiled_chameleon",
})

OUT_DIR = Path("/tmp/LIFE-push/releases/v2026-04-25j/posters_GS_16_new")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Banner table — explicit per session-locked authority decisions
BANNERS = {
    "capybara": "USDA",
    "patagonian_mara": "USDA",
    "rabbit": "USDA",
    "wallaby": "USDA",
    "two_toed_sloth": "USDA",
    "spider_monkey": "USDA + Harris County",
    "kinkajou": "USDA",
    "prehensile_tailed_porcupine": "USDA",
    "toco_toucan": "USDA",
    "argentine_tegu": "(no banner — exempt)",
    "nine_banded_armadillo": "USDA",
    "chinese_water_dragon": "(no banner — exempt)",
    "veiled_chameleon": "(no banner — exempt)",
    "leopard_tortoise": "(no banner — exempt)",
    "russian_tortoise": "(no banner — exempt)",
    "yellow_footed_tortoise": "(no banner — exempt)",
}


def gs(slug, common, sci, category, what, correct, correct_foods, wrong, wrong_foods,
       simple, prep, three_sec, source, morning, encounter, daily="Per posted portion chart",
       sites=("Houston", "San Antonio")):
    return {
        "slug": slug,
        "common_name": common,
        "scientific_name": sci,
        "category": category,
        "what_this_animal_is": what,
        "correct": correct,
        "correct_foods": correct_foods,
        "wrong": wrong,
        "wrong_foods": wrong_foods,
        "simple_build": simple,
        "prep_rule": prep,
        "three_second_check": three_sec,
        "source_line": source,
        "verbatim": True,
        "morning_feed": morning,
        "encounter_portion": encounter,
        "daily_weight": daily,
        "sites": list(sites),
    }


SPECIES = [
    # ===== USDA grazers =====
    gs("capybara", "CAPYBARA", "Hydrochoerus hydrochaeris",
       "GRAZER — Hay + Pellet + Greens",
       "Largest rodent — South American wetlands, social grazer",
       ["Hay base", "daily herbivore pellet", "whole-leaf greens"],
       ["timothy_hay", "herbivore_pellets", "kale", "collard_greens", "romaine"],
       ["Fruit-heavy", "Pet kibble", "Sugary guest treats"],
       ["banana", "apple", "corn", "sweet_potato_yam"],
       ["Hay base always available", "Mazuri herbivore pellet ration", "Whole-leaf greens"],
       "Hay first. Pellet weighed per SOP. Greens whole-leaf, not chopped.",
       "Hay + pellet + greens visible?",
       "v23 catalog · Grazer rodent class · Master Doc 'Hay-Eating Animals'",
       "Whole hay base. Mazuri herbivore pellet. Whole-leaf greens.",
       "Whole-leaf green or hay strand for hand-feeding. Drawn from daily allocation."),

    gs("patagonian_mara", "PATAGONIAN MARA", "Dolichotis patagonum",
       "GRAZER — Hay + Pellet + Greens",
       "Long-legged rodent — Argentine grasslands",
       ["Hay base", "small pellet ration", "greens"],
       ["timothy_hay", "herbivore_pellets", "collard_greens", "kale", "dandelion_greens"],
       ["Fruit-heavy", "Sugary treats", "Pet kibble"],
       ["banana", "apple", "corn", "sweet_potato_yam"],
       ["Hay base always available", "Small Mazuri herbivore pellet ration", "Whole-leaf greens"],
       "Hay first. Small pellet ration weighed. Greens whole-leaf.",
       "Hay + pellet + greens visible?",
       "v23 catalog · Grazer rodent class",
       "Whole hay (timothy, grass) as base. Small pellet ration. Whole-leaf greens.",
       "Whole-leaf green or hay strand for hand-feeding. Drawn from daily allocation."),

    gs("rabbit", "RABBIT", "Oryctolagus cuniculus (domestic)",
       "GRAZER — Hay + Pellet + Greens",
       "Domestic rabbit — strict herbivore, hindgut fermenter",
       ["Hay base", "small timothy pellet", "whole-leaf greens"],
       ["timothy_hay", "herbivore_pellets", "kale", "collard_greens", "dandelion_greens"],
       ["Carrots daily", "Sugary fruit", "Pet kibble"],
       ["carrot", "banana", "apple", "corn"],
       ["Timothy hay base", "Small timothy-based pellet", "Whole-leaf greens"],
       "Timothy hay first. Carrot is a treat, not a daily food. No iceberg.",
       "Hay + pellet + greens visible?",
       "v23 catalog · Grazer class · House Rabbit Society standards",
       "Whole timothy hay as base. Small pellet ration. Whole-leaf greens.",
       "Whole-leaf green for hand-feeding. Drawn from daily allocation."),

    gs("wallaby", "BENNETT'S WALLABY", "Notamacropus rufogriseus",
       "GRAZER — Hay + Macropod Pellet + Greens",
       "Macropod — Tasmania / SE Australia, hay-eating browser",
       ["Hay", "macropod pellet", "greens"],
       ["timothy_hay", "grass_hay", "herbivore_pellets", "kale", "collard_greens"],
       ["Fruit-heavy", "Bread", "Pet kibble", "Sugary treats"],
       ["banana", "apple", "corn"],
       ["Hay base", "Macropod (Mazuri Wallaby/Kangaroo) pellet ration", "Whole-leaf greens"],
       "Hay first. Pellet weighed. NO bread, NO sugary guest treats.",
       "Hay + macropod pellet + greens visible?",
       "v23 catalog · Grazer macropod class · Master Doc PART 4 'Hay-Eating Animals'",
       "Whole hay base. Macropod pellet ration. Whole-leaf greens.",
       "Whole-leaf green or hay strand for hand-feeding. Drawn from daily allocation."),

    # ===== Folivores / chow-base =====
    gs("two_toed_sloth", "TWO-TOED SLOTH", "Choloepus didactylus",
       "FOLIVORE — Leaf + Chow Base",
       "Slow arboreal folivore — neotropical rainforest canopy",
       ["Chow base", "leafy greens", "browse with stems"],
       ["primate_chow", "kale", "collard_greens", "mulberry_leaves", "browse_branches"],
       ["Vegetable salad bowls", "Romaine-only", "No chow"],
       ["banana", "apple", "corn", "sweet_potato_yam"],
       ["Mazuri leaf-eater chow as the base", "Whole-leaf greens", "Browse branches WITH stems left on"],
       "Stems ARE enrichment — leave them on. Chow base is non-negotiable.",
       "Is the chow base there? Stems left on?",
       "v23 PART 4 §9 · Folivore class · Restored from drift v2026-04-25d",
       "Mazuri leaf-eater chow as base. Whole-leaf greens. Browse — stems ARE enrichment.",
       "Single leaf for slow hand-feeding. Drawn from daily allocation."),

    gs("spider_monkey", "GEOFFROY'S SPIDER MONKEY", "Ateles geoffroyi",
       "PRIMATE — Frugivore",
       "Brachiating primate — Central American forests",
       ["Fruit primary", "leaves secondary", "primate chow daily"],
       ["mango", "papaya", "berries", "primate_chow", "kale", "collard_greens"],
       ["Citrus", "Sugar-heavy fruit", "Starchy vegetables", "Pellets used as base"],
       ["orange", "corn", "sweet_potato_yam"],
       ["Fruit primary in golf-ball pieces (~1 inch)", "Whole-leaf greens secondary", "Mazuri primate chow daily"],
       "Many small pieces, not few large. Mazuri primate chow daily as small ration.",
       "Is fruit dominant? Is the chow there?",
       "v23 catalog · primate class · USDA + Harris County primate licensing",
       "Fruit in golf-ball pieces (~1 inch). Whole-leaf greens. Mazuri primate chow daily.",
       "Bite-sized fruit cubes (½ inch). Drawn from daily allocation, not extra."),

    gs("kinkajou", "KINKAJOU", "Potos flavus",
       "FRUGIVORE — Soft-Mouthed",
       "Arboreal procyonid — Central / South American rainforest",
       ["Soft fruit", "daily frugivore pellet", "trace protein"],
       ["primate_chow", "papaya", "melon", "berries", "banana"],
       ["Citrus", "Hard fruit", "Cat / dog food"],
       ["orange", "corn", "raw_meat_ground"],
       ["Mazuri Frugivore Diet ration", "Soft fruit in golf-ball pieces (~1 inch)", "Trace cooked egg or insect protein"],
       "Soft fruit only. Pieces ~1 inch. Pellet weighed.",
       "Is fruit soft and small? Pellet visible?",
       "v23 catalog · Soft-mouth frugivore class",
       "Mazuri Frugivore Diet. Soft fruit in golf-ball pieces (~1 inch). Trace egg/insect protein.",
       "Single fruit cube (½ inch) for tong or hand. Drawn from daily allocation."),

    gs("prehensile_tailed_porcupine", "PREHENSILE-TAILED PORCUPINE", "Coendou prehensilis",
       "FOLIVORE — Leaves + Browse + Pellet",
       "Arboreal porcupine — South American forest canopy",
       ["Leaves", "browse", "small chow ration"],
       ["kale", "mulberry_leaves", "collard_greens", "browse_branches", "primate_chow"],
       ["Fruit-heavy", "Cat / dog food", "Pellet used as base"],
       ["banana", "apple", "corn"],
       ["Whole-leaf greens", "Browse branches with stems", "Small Mazuri leaf-eater chow ration"],
       "Leaves whole. Browse with stems. Sweet potato slice as occasional supplement only.",
       "Leaves + browse + chow visible?",
       "v23 catalog · Folivore mammal class",
       "Whole-leaf greens. Browse with stems. Mazuri leaf-eater chow ration.",
       "Single leaf for hand-feeding. Drawn from daily allocation."),

    # ===== Toucan =====
    gs("toco_toucan", "TOCO TOUCAN", "Ramphastos toco",
       "FRUGIVORE — Low Iron",
       "Largest toucan — South American forest edge",
       ["Low-iron softbill chow", "low-sugar fruit"],
       ["softbill_chow", "papaya", "melon", "berries", "apple"],
       ["High-iron foods", "Citrus", "Banana", "Mango"],
       ["banana", "mango", "orange"],
       ["Mazuri low-iron softbill chow weighed first", "Low-sugar fruit only in ½-inch cubes", "NO citrus / NO banana / NO mango"],
       "Iron storage disease prevention is the mission. Citrus boosts iron absorption — never serve.",
       "Is the chow low-iron? No citrus / no banana / no mango?",
       "v23 catalog · Softbill Frugivore class · Iron Storage Disease protocol",
       "Low-iron softbill chow weighed first. Fruit ½-inch, low-sugar only. NO citrus / banana / mango.",
       "Single ½-inch fruit cube for tong-delivery. Drawn from daily allocation."),

    # ===== Tegu (exempt) =====
    gs("argentine_tegu", "ARGENTINE BLACK-AND-WHITE TEGU", "Salvator merianae",
       "OMNIVORE — Protein-Driven",
       "Large terrestrial lizard — South American grasslands",
       ["40-60% protein", "greens", "small fruit"],
       ["raw_meat_ground", "cooked_egg", "kale", "berries", "collard_greens"],
       ["No protein", "Fruit-heavy", "Banana / mango heavy", "Cat or dog food"],
       ["banana", "mango", "corn"],
       ["Lean ground meat or cooked egg per SOP", "Whole-leaf greens", "Small ½-inch fruit pieces"],
       "Protein measured per SOP. No pet food substitute. Tegu is EXEMPT.",
       "Is protein visible?",
       "v23 PART 4 §11 · Tegu — Protein-Driven Omnivore · Banner corrected to Exempt",
       "Lean ground meat or cooked egg per SOP. Whole-leaf greens. Small fruit pieces (½-inch).",
       "Single small protein cube or fruit cube for tong-delivery. Drawn from daily allocation."),

    # ===== Nine-banded armadillo =====
    gs("nine_banded_armadillo", "NINE-BANDED ARMADILLO", "Dasypus novemcinctus",
       "INSECTIVORE — Pellet-Base + Live Feeders",
       "Insectivore mammal — North/Central American grasslands",
       ["Insect diet dominant", "live feeders"],
       ["insect_diet", "mealworms", "crickets", "cooked_egg"],
       ["Fruit-heavy bowls", "Vegetable bowls", "Pet kibble"],
       ["banana", "apple", "corn"],
       ["Mazuri insectivore diet in flat bowl", "Live feeders (mealworms, crickets) per SOP", "Trace cooked egg occasional"],
       "Insectivore pellet is the base. Live feeders supplement, not replace.",
       "Is the insectivore pellet dominant?",
       "v23 PART 7 §1E · insectivore class",
       "Mazuri insectivore diet flat bowl. Live feeders (mealworms, crickets) per SOP.",
       "Single mealworm for tong-delivery. Drawn from daily allocation."),

    # ===== Chinese Water Dragon (exempt) =====
    gs("chinese_water_dragon", "CHINESE WATER DRAGON", "Physignathus cocincinus",
       "OMNIVORE — Insect-Leaning",
       "Arboreal lizard — SE Asian streamside forest",
       ["Insects + greens", "occasional fruit"],
       ["crickets", "mealworms", "kale", "mulberry_leaves", "berries"],
       ["Fruit-heavy bowls", "Pet kibble", "Large dry pellets"],
       ["banana", "apple", "corn"],
       ["Live feeders (crickets, dubia roaches) per SOP — base", "Small leafy greens (kale, mulberry leaves)", "Occasional ½-inch fruit cubes"],
       "Live feeders are the base. No daily pellet.",
       "Are live feeders the base?",
       "v23 catalog · Insect-leaning omnivore lizard class",
       "Live feeders per SOP — base. Small leafy greens. Occasional ½-inch fruit cubes.",
       "Single cricket for tong-delivery. Drawn from daily allocation."),

    # ===== Veiled Chameleon (exempt) =====
    gs("veiled_chameleon", "VEILED CHAMELEON", "Chamaeleo calyptratus",
       "INSECTIVORE — With Greens",
       "Arboreal chameleon — Arabian Peninsula montane",
       ["Live feeders", "leafy greens", "occasional fruit"],
       ["crickets", "mealworms", "collard_greens", "dandelion_greens", "kale"],
       ["Mealworms as base (chitin)", "Fruit-heavy", "Pet kibble"],
       ["banana", "apple", "corn"],
       ["Gut-loaded live feeders per SOP", "Whole-leaf greens (collard, dandelion)", "Small fruit accent occasional"],
       "Mealworms NOT base (chitin too high). Gut-load all feeders before serving.",
       "Are live feeders set? Are greens whole-leaf?",
       "v23 catalog · Insectivore-with-greens lizard class",
       "Gut-loaded live feeders per SOP. Whole-leaf greens (collard, dandelion). Small fruit accent occasional.",
       "No guest hand-feed for chameleons (stress). Tong-delivery by trained keeper only."),

    # ===== Tortoises (exempt — three differentiated diets) =====
    gs("leopard_tortoise", "LEOPARD TORTOISE", "Stigmochelys pardalis",
       "GRAZING TORTOISE — Hay + Grasses + Limited Greens",
       "Grazing tortoise — African savanna; STRICT GRAZER, NOT a Sulcata",
       ["80% grass hay + grasses", "15% coarse greens", "5% browse · NO FRUIT"],
       ["timothy_hay", "grass_hay", "dandelion_greens", "mulberry_leaves", "browse_branches"],
       ["Fruit", "Commercial tortoise pellets", "High-protein greens (kale daily)"],
       ["banana", "apple", "mango", "berries"],
       ["Grass hay + fresh grass dominant", "Coarse greens (dandelion, mulberry, collard) whole", "Browse branches"],
       "Strict grazer. NO FRUIT. Differs from Sulcata in tolerating limited coarse greens.",
       "Is grass hay dominant? Any fruit visible? (should be NONE)",
       "AZA Chelonian TAG · Sulcata/Leopard nutrition guidelines",
       "Whole hay pile. Fresh grass cut long. Coarse greens whole. Browse branches.",
       "Single coarse green leaf or grass strand for hand-feeding. Drawn from daily allocation."),

    gs("russian_tortoise", "RUSSIAN TORTOISE", "Testudo horsfieldii",
       "STEPPE HERBIVORE — Broadleaf Greens + Hay",
       "Steppe tortoise — Central Asia; broadleaf grazer, NOT a hay-only species",
       ["70-80% broadleaf greens", "15% grass hay", "5% browse / weeds"],
       ["dandelion_greens", "collard_greens", "kale", "mulberry_leaves", "grass_hay"],
       ["Hay only (this is NOT a Sulcata)", "Spinach", "Iceberg", "Daily fruit"],
       ["banana", "apple", "corn", "romaine"],
       ["Broadleaf greens dominant", "Grass hay secondary", "Browse and weeds (dandelion, plantain)"],
       "NOT a Sulcata — broadleaf greens dominant, hay is secondary. Trace fruit only.",
       "Are broadleaf greens dominant? Is hay present?",
       "AZA Chelonian TAG · Testudo nutrition standards",
       "Broadleaf greens dominant (dandelion, collard, kale, mulberry). Grass hay secondary. Browse + weeds.",
       "Single dandelion green or mulberry leaf for hand-feeding. Drawn from daily allocation."),

    gs("yellow_footed_tortoise", "YELLOW-FOOTED TORTOISE", "Chelonoidis denticulatus",
       "RAINFOREST OMNIVORE — Fruit + Greens + Trace Protein",
       "Forest tortoise — Amazon basin; fruit-tolerant, hay-intolerant as base",
       ["40-50% fruit (tropical)", "30-40% greens + browse", "5% trace protein weekly"],
       ["papaya", "mango", "melon", "berries", "collard_greens", "mulberry_leaves"],
       ["Hay only (this is NOT a Sulcata)", "Daily commercial pellet", "Daily high-protein"],
       ["corn", "carrot", "sweet_potato_yam"],
       ["Fruit in 1-inch chunks (papaya, mango, melon, berries)", "Whole-leaf greens (collard, kale, mulberry)", "Browse branches"],
       "Mazuri Tortoise Diet (LS) 1-2×/week only — NOT daily, NOT base. Trace egg/pellet weekly.",
       "Is fruit visible? Is humidity OK?",
       "AZA Chelonian TAG · Chelonoidis denticulatus standards",
       "Fruit in 1-inch chunks. Whole-leaf greens. Mazuri tortoise diet 1-2×/week. Trace protein.",
       "Single fruit cube (½ inch) for hand-feeding. Drawn from daily allocation."),
]


def main():
    built = []
    for sp in SPECIES:
        banner = BANNERS[sp["slug"]]
        out = OUT_DIR / f"GoldStandard_{sp['slug']}.pdf"
        gsbuilder.build_poster(sp, banner, out)
        built.append({"slug": sp["slug"], "name": sp["common_name"], "banner": banner, "file": out.name})
        print(f"  built {sp['common_name']:40s} | {banner:32s} -> {out.name}")

    # Manifest
    manifest = {
        "version": "v2026-04-25j",
        "subset": "GS_16_new",
        "count": len(built),
        "scope": "16 active totems missing Gold Standard verbatim posters",
        "items": built,
    }
    (OUT_DIR.parent / "GS_16_manifest.json").write_text(json.dumps(manifest, indent=2))
    # Also save the full GS16 content json
    content = {
        "_source": "v23 + v2026-04-25f drift catalog",
        "_rules": [
            "Match the bowl. Don't interpret.",
            "Encounter portions come FROM daily allocation, never extra.",
            "Multi-animal habitats use golf-ball pieces (~1 inch).",
            "Pellet (Mazuri / Missouri) is a component, not a base.",
            "Hay-only is Sulcata only — other tortoises have different diets.",
        ],
        "_schema_version": "gs10-compatible",
        "species": SPECIES,
    }
    (OUT_DIR.parent / "LIFE_diet_content_gs16_v2026-04-25j.json").write_text(json.dumps(content, indent=2))
    print(f"\nWrote {len(built)} posters + manifest + content -> {OUT_DIR}")


if __name__ == "__main__":
    main()
