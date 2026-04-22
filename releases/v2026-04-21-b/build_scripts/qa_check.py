"""
QA spot-check across all 18 K-5 JSONs and corresponding Tier 1 JSONs.

Checks:
  - Exact question wording (locked 8, exact order)
  - 10-19 words per answer
  - No forbidden words (whole-word match)
  - Tagline format: "A [X] that lives in [Y]."
  - Closing prompt exact
  - Footer has BOTH locked lines
  - Tier 1 mirror has matching ground_truth_k5 text
  - Tier 2 has scientific_name, where_lives, conservation, master bullets, alpha/omega note
"""
import json, os, re, glob

K5 = "/home/user/workspace/LIFE_k5_locked"
TIER = "/home/user/workspace/LIFE_tier_content"

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
CLOSING = "LOOK AT THE ANIMAL: What do you see it doing right now?"
FOOTER = [
    "What a living thing can sense becomes its reality.",
    "Environment shapes design.",
]
FORBIDDEN = [
    "binocular", "canopy", "anogenital", "territory", "diurnal", "nocturnal",
    "brumation", "metabolic rate", "chemical particles", "perception",
    "vocalization", "psychological", "talk", "talks", "talking"
]

def word_count(s):
    return len(re.findall(r"\b\w+\b", s))

errors, warnings = [], []
species_count = 0

for p in sorted(glob.glob(os.path.join(K5, "*.json"))):
    species_count += 1
    with open(p) as f:
        d = json.load(f)
    slug = d["slug"]

    # tagline
    t = d["tagline"]
    if not (t.startswith("A ") and " that lives in " in t and t.endswith(".")):
        errors.append(f"{slug}: tagline format — '{t}'")

    # closing
    if d["closing_prompt"] != CLOSING:
        errors.append(f"{slug}: closing prompt mismatch — '{d['closing_prompt']}'")

    # footer
    if d["footer"] != FOOTER:
        errors.append(f"{slug}: footer mismatch")

    # 8 questions exact + 10-19 words + no forbidden
    for i in range(1, 9):
        a = d["answers"].get(str(i), {})
        if a.get("q") != LOCKED_QS[i-1]:
            errors.append(f"{slug} Q{i}: question wording mismatch — '{a.get('q')}'")
        ans = a.get("a", "")
        wc = word_count(ans)
        if wc < 10 or wc > 19:
            errors.append(f"{slug} Q{i}: {wc} words (must be 10-19) — '{ans}'")
        low = ans.lower()
        for bad in FORBIDDEN:
            if re.search(rf"\b{re.escape(bad)}\b", low):
                errors.append(f"{slug} Q{i}: FORBIDDEN '{bad}' — '{ans}'")

    # Tier 1 pairing
    t1_path = os.path.join(TIER, f"{slug}_tier1.json")
    if not os.path.exists(t1_path):
        errors.append(f"{slug}: missing Tier 1 file")
    else:
        with open(t1_path) as f:
            t1 = json.load(f)
        if t1.get("locked_questions") != LOCKED_QS:
            errors.append(f"{slug} Tier 1: locked_questions drift")
        # ground_truth_k5 matches the K-5 answers
        for i in range(1, 9):
            gt = t1["ground_truth_k5"][str(i)]
            if gt["q"] != LOCKED_QS[i-1]:
                errors.append(f"{slug} Tier 1 Q{i}: question mismatch")
            if gt["a_third_person"] != d["answers"][str(i)]["a"]:
                errors.append(f"{slug} Tier 1 Q{i}: answer drift vs K-5")

    # Tier 2 pairing
    t2_path = os.path.join(TIER, f"{slug}_tier2.json")
    if not os.path.exists(t2_path):
        errors.append(f"{slug}: missing Tier 2 file")
    else:
        with open(t2_path) as f:
            t2 = json.load(f)
        for req in ["scientific_name", "where_lives", "conservation",
                    "master_bullets_by_question", "alpha_omega_note",
                    "locked_questions"]:
            if req not in t2:
                errors.append(f"{slug} Tier 2: missing field '{req}'")
        # master bullets: each of 8 questions should have >=1 bullet
        if "master_bullets_by_question" in t2:
            for q in LOCKED_QS:
                if not t2["master_bullets_by_question"].get(q):
                    errors.append(f"{slug} Tier 2: no bullets for '{q}'")

print(f"Checked {species_count} species.")
print(f"Errors:   {len(errors)}")
print(f"Warnings: {len(warnings)}")
if errors:
    print("\n--- ERRORS ---")
    for e in errors:
        print("  -", e)
    raise SystemExit(1)
print("\nALL CHECKS PASSED.")
