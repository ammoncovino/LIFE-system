"""Per-species copy for encounter door totems — v2026-04-27b.

User-locked rules (this revision):
  - NO time stated (we set our own pace)
  - NO food references in "How It Works" (encounter ≠ feeding promise)
  - NO tip / gratuity section anywhere
  - Specific fee per species
  - All ages welcome EXCEPT lemurs (5+)
  - Tegu is FREE and NOT USDA-regulated
"""

ENCOUNTERS = {
    "red_ruffed_lemur": {
        "title": "RED-RUFFED LEMUR ENCOUNTER",
        "fee": "$12",
        "free": False,
        "usda": True,
        "group_size": "6 guests",
        "age_text": "ages 5+",
        "contact_rule": "Keeper-led. Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "promise_note": None,
    },
    "black_and_white_ruffed_lemur": {
        "title": "BLACK & WHITE RUFFED LEMUR ENCOUNTER",
        "fee": "$12",
        "free": False,
        "usda": True,
        "group_size": "6 guests",
        "age_text": "ages 5+",
        "contact_rule": "Keeper-led. Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "promise_note": None,
    },
    "ring_tailed_lemur": {
        "title": "RING-TAILED LEMUR ENCOUNTER",
        "fee": "$12",
        "free": False,
        "usda": True,
        "group_size": "6 guests",
        "age_text": "ages 5+",
        "contact_rule": "Keeper-led. Match the keeper, not the animal. No tail or limb contact. Quiet voices.",
        "promise_note": None,
    },
    "two_toed_sloth": {
        "title": "TWO-TOED SLOTH ENCOUNTER",
        "fee": "$20",
        "free": False,
        "usda": True,
        "group_size": "6 guests",
        "age_text": "all ages",
        "contact_rule": "Observe at keeper's direction. No grabbing, no lifting, no flash photography.",
        "promise_note": None,
    },
    "kinkajou": {
        "title": "KINKAJOU ENCOUNTER",
        "fee": "$3",
        "free": False,
        "usda": True,
        "group_size": "small group",
        "age_text": "all ages",
        "contact_rule": "Feeding through the hole only. No direct contact. Keeper opens and closes.",
        "promise_note": None,
    },
    "capybara": {
        "title": "CAPYBARA ENCOUNTER",
        "fee": "$3",
        "free": False,
        "usda": True,
        "group_size": "6 guests",
        "age_text": "all ages",
        "contact_rule": "Side-touch only at keeper's call. No face contact. Stay seated.",
        "promise_note": None,
    },
    "argentine_tegu": {
        "title": "ARGENTINE TEGU ENCOUNTER",
        "fee": "FREE",
        "free": True,
        "usda": False,
        "group_size": "small group",
        "age_text": "all ages",
        "contact_rule": "Keeper holds the animal. Guests touch the back at keeper's signal. No tail contact.",
        "promise_note": None,
    },
    "prehensile_tailed_porcupine": {
        "title": "PREHENSILE-TAILED PORCUPINE ENCOUNTER",
        "fee": "$20",
        "free": False,
        "usda": True,
        "group_size": "small group",
        "age_text": "all ages",
        "contact_rule": "Keeper-mediated only. No hand contact. Observe and ask questions.",
        "promise_note": "She comes down rarely. <b>No promise of touching or feeding</b> — you're paying for the chance.",
    },
}
