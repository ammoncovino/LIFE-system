"""
Build Tier 1 + Tier 2 JSON sources for each of the 18 species.

Tier 1 (under 13):
  - Species animal speaks in first person
  - K-5 voice, same 10-19 word ceiling as Student Totem
  - Uses the LOCKED 8 questions ONLY, exact wording, exact order
  - Forbidden words active

Tier 2 (13+):
  - Naturalist voice (third person, NOT the animal)
  - Full master bullets (from LIFE_totem_content_18.json)
  - Plus scientific name, where_lives, conservation, Alpha/Omega lens flags
  - Flagged "broadly accepted" vs "still debated" where relevant

Outputs:
  /home/user/workspace/LIFE_tier_content/{slug}_tier1.json
  /home/user/workspace/LIFE_tier_content/{slug}_tier2.json
"""
import json, os

MASTER = "/home/user/workspace/LIFE_totem_content_18.json"
K5_DIR = "/home/user/workspace/LIFE_k5_locked"
OUT_DIR = "/home/user/workspace/LIFE_tier_content"
os.makedirs(OUT_DIR, exist_ok=True)

with open(MASTER) as f:
    master = json.load(f)

FORBIDDEN = [
    "binocular", "canopy", "anogenital", "territory", "diurnal", "nocturnal",
    "brumation", "metabolic rate", "chemical particles", "perception",
    "vocalization", "psychological", "talk", "talks", "talking"
]

ALPHA_OMEGA_NOTE = (
    "Alpha/Omega lens: what we are confident about (sensory biology, "
    "behavior, habitat needs) vs. what is still debated (fine-grained "
    "social structure, exact cognitive limits, interpretation of specific "
    "signals). Separate 'broadly accepted' from 'still debated' when you answer."
)

# The 8 locked questions (exact wording, exact order)
LOCKED_QS = [
    "What can it see, hear, or feel?",
    "Where does it live \u2014 and why?",
    "How does it send messages?",
    "What does it do when something changes?",
    "How does it learn?",
    "How does it have babies?",
    "What are its limits?",
    "What does this teach us?",
]

count = 0
for sp in master["species"]:
    slug = sp["slug"]
    # Load matching K-5 JSON for Tier 1 answers
    k5_path = os.path.join(K5_DIR, f"{slug}.json")
    if not os.path.exists(k5_path):
        print(f"SKIP (no K-5 source): {slug}")
        continue
    with open(k5_path) as f:
        k5 = json.load(f)

    # ---------------- Tier 1 ----------------
    tier1 = {
        "version": "v2026.04.21-b",
        "tier": 1,
        "audience": "under 13",
        "voice": "first-person animal (e.g. 'I use sharp eyes...')",
        "rules": [
            "Use ONLY the locked 8 questions in the exact wording and order.",
            "Answers must match the K-5 ceiling: 10-19 words each.",
            "Real vocabulary allowed (rainforest, predators, keen, plentiful).",
            "Never use any forbidden word.",
            "The animal speaks; never break character.",
            "Never say 'talk/talks/talking' — use 'send messages', 'calls', 'signals'.",
        ],
        "forbidden_words": FORBIDDEN,
        "species": k5["species"],
        "slug": slug,
        "character_name": k5["character_name"],
        "tagline": k5["tagline"],
        "locked_questions": LOCKED_QS,
        # Ground-truth K-5 answers in animal-voice seed form.
        # The LLM rewrites to first person while preserving the facts and word count.
        "ground_truth_k5": {
            str(i): {
                "q": k5["answers"][str(i)]["q"],
                "a_third_person": k5["answers"][str(i)]["a"],
            } for i in range(1, 9)
        },
        "closing_prompt": k5["closing_prompt"],
        "footer": k5["footer"],
    }
    out1 = os.path.join(OUT_DIR, f"{slug}_tier1.json")
    with open(out1, "w") as f:
        json.dump(tier1, f, indent=2, ensure_ascii=False)

    # ---------------- Tier 2 ----------------
    # Collect master bullets per question from the master JSON.
    master_bullets = {}
    bullet_keys = [
        ("q1_sense",  "What can it see, hear, or feel?"),
        ("q2_habitat","Where does it live \u2014 and why?"),
        ("q3_signals","How does it send messages?"),
        ("q4_change", "What does it do when something changes?"),
        ("q5_learn",  "How does it learn?"),
        ("q6_babies", "How does it have babies?"),
        ("q7_limits", "What are its limits?"),
        ("q8_teaches","What does this teach us?"),
    ]
    for key, qtext in bullet_keys:
        master_bullets[qtext] = sp.get(key, [])

    tier2 = {
        "version": "v2026.04.21-b",
        "tier": 2,
        "audience": "13 and up",
        "voice": "naturalist, third-person (the animal is observed, not the speaker)",
        "rules": [
            "Keep the 8 locked questions as the structural spine of any answer set.",
            "Answers may use the full master bullet list and scientific vocabulary.",
            "Be explicit when something is broadly accepted vs. still debated.",
            "You may extend beyond the 8 questions only when a user asks a follow-up.",
            "Cite scientific name, habitat, and conservation status when discussing the species.",
            "Never pretend to be the animal — third-person, naturalist voice only.",
        ],
        "species": sp["common_name"],
        "slug": slug,
        "scientific_name": sp["scientific_name"],
        "where_lives": sp["where_lives"],
        "conservation": sp["conservation"],
        "locked_questions": LOCKED_QS,
        "master_bullets_by_question": master_bullets,
        "alpha_omega_note": ALPHA_OMEGA_NOTE,
        "closing_prompt": "LOOK AT THE ANIMAL: What do you see it doing right now?",
        "footer": [
            "What a living thing can sense becomes its reality.",
            "Environment shapes design.",
        ],
    }
    out2 = os.path.join(OUT_DIR, f"{slug}_tier2.json")
    with open(out2, "w") as f:
        json.dump(tier2, f, indent=2, ensure_ascii=False)

    count += 1
    print(f"WROTE {slug}_tier1.json + {slug}_tier2.json")

print()
print(f"Built {count} species × 2 tiers = {count*2} JSON files in {OUT_DIR}")
