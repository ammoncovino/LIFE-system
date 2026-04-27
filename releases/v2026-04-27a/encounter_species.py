"""Per-species copy for encounter door totems.

Each species needs:
- title (display)
- species_key (file name)
- group_size, duration, age_min — keeper-led encounter rules
- contact_rule — what's allowed/not (touch vs. observe)
- food_note — match the bowl reminder, species-specific
- caution — species-specific risk (bite/scratch/etc.) for staff awareness only
"""

ENCOUNTERS = {
    "red_ruffed_lemur": {
        "title": "RED-RUFFED LEMUR ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "5+",
        "contact_rule": "Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "food_note": "Food is from the daily allocation only. Never extra. No fruit beyond the wild-range list.",
        "caution": "Critically endangered. Sensitive to handling stress. Keeper has full authority.",
    },
    "black_and_white_ruffed_lemur": {
        "title": "BLACK & WHITE RUFFED LEMUR ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "5+",
        "contact_rule": "Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "food_note": "Food is from the daily allocation only. Never extra. No fruit beyond the wild-range list.",
        "caution": "Critically endangered. Sensitive to handling stress. Keeper has full authority.",
    },
    "ring_tailed_lemur": {
        "title": "RING-TAILED LEMUR ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "5+",
        "contact_rule": "Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "food_note": "Food is from the daily allocation only. Never extra. Match the bowl.",
        "caution": "Will scent-mark. Will attempt to take food from hands or pockets. Keeper leads.",
    },
    "two_toed_sloth": {
        "title": "TWO-TOED SLOTH ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "5+",
        "contact_rule": "Observe at keeper's direction. No grabbing. No lifting. No flash photography.",
        "food_note": "Food is from the daily allocation only. Leaves and browse — no human food.",
        "caution": "Slow but strong. Long claws. Stress shows quietly — keeper calls when to end.",
    },
    "kinkajou": {
        "title": "KINKAJOU ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "8+",
        "contact_rule": "Keeper-mediated only. No direct hand-feeding by guests. Quiet, low light.",
        "food_note": "Food is from the daily allocation only. Fruit and nectar — no sugar additions.",
        "caution": "Sharp teeth. Nocturnal — bright light or loud noise ends the encounter immediately.",
    },
    "capybara": {
        "title": "CAPYBARA ENCOUNTER",
        "duration": "10 minutes",
        "group_size": "6 guests",
        "age_min": "5+",
        "contact_rule": "Side-touch only at keeper's call. No face contact. Stay seated.",
        "food_note": "Hay and wild-range greens only. No human snacks. Match the bowl.",
        "caution": "Large rodent — calm but powerful. Teeth are continuous-growing. Keeper sets pace.",
    },
    "argentine_tegu": {
        "title": "ARGENTINE TEGU ENCOUNTER",
        "duration": "8 minutes",
        "group_size": "4 guests",
        "age_min": "8+",
        "contact_rule": "Keeper holds the animal. Guests touch the back at keeper's signal. No tail contact.",
        "food_note": "Daily allocation only — eggs, prey, fruit per the wild-range list.",
        "caution": "Strong jaws. Tail can whip. Keeper controls the head and tail at all times.",
    },
    "prehensile_tailed_porcupine": {
        "title": "PREHENSILE-TAILED PORCUPINE ENCOUNTER",
        "duration": "8 minutes",
        "group_size": "4 guests",
        "age_min": "8+",
        "contact_rule": "Keeper-mediated only. No hand contact. Observe and ask questions.",
        "food_note": "Leaves, bark, and wild-range fruit only. No human food. Match the bowl.",
        "caution": "Quills release on contact. Backs into threats. Keeper maintains full control.",
    },
}
