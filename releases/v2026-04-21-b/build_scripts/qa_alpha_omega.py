"""
QA pass for Alpha/Omega failure cycles.

Checks:
  1. Every Tier 2 file has alpha_omega_failure_cycle with all 4 sections.
  2. Minimum items per section (>=3).
  3. UNIQUENESS across species: no identical string is reused in the same
     section across two different species.
  4. No line is near-duplicate (Jaccard >=0.85 on token sets) across species
     in the same section.
  5. Content references the species or its biology (not purely generic).
"""
import json, os, glob, re
from itertools import combinations

TIER = "/home/user/workspace/LIFE_tier_content"

SECTIONS = [
    "broadly_accepted",
    "still_debated",
    "common_failure_modes",
    "species_specific_guardrails",
]
MIN_ITEMS = 3

def tok(s):
    return set(re.findall(r"[a-z]{3,}", s.lower()))

def jaccard(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

errors, warnings = [], []

# Load all tier2 files
files = sorted(glob.glob(os.path.join(TIER, "*_tier2.json")))
data = {}
for p in files:
    with open(p) as f:
        d = json.load(f)
    slug = d["slug"]
    data[slug] = d

print(f"Loaded {len(data)} Tier 2 files.\n")

# 1 + 2: presence + min items
for slug, d in data.items():
    if "alpha_omega_note" in d:
        errors.append(f"{slug}: still has old 'alpha_omega_note' field")
    if "alpha_omega_failure_cycle" not in d:
        errors.append(f"{slug}: missing 'alpha_omega_failure_cycle'")
        continue
    cyc = d["alpha_omega_failure_cycle"]
    for sec in SECTIONS:
        if sec not in cyc:
            errors.append(f"{slug}: missing section '{sec}'")
            continue
        if not isinstance(cyc[sec], list):
            errors.append(f"{slug}.{sec}: not a list")
            continue
        if len(cyc[sec]) < MIN_ITEMS:
            errors.append(f"{slug}.{sec}: only {len(cyc[sec])} items (need >= {MIN_ITEMS})")

# 3: exact-string duplicates across species in same section
for sec in SECTIONS:
    bucket = {}  # string -> [slugs]
    for slug, d in data.items():
        cyc = d.get("alpha_omega_failure_cycle", {})
        for item in cyc.get(sec, []):
            bucket.setdefault(item.strip(), []).append(slug)
    for item, slugs in bucket.items():
        if len(slugs) > 1:
            errors.append(
                f"EXACT DUPLICATE in {sec}: '{item[:70]}...' shared by {slugs}"
            )

# 4: near-duplicates across species in same section
NEAR_DUP = 0.85
for sec in SECTIONS:
    pool = []  # (slug, idx, text, tokens)
    for slug, d in data.items():
        cyc = d.get("alpha_omega_failure_cycle", {})
        for i, item in enumerate(cyc.get(sec, [])):
            pool.append((slug, i, item, tok(item)))
    for (s1, i1, t1, k1), (s2, i2, t2, k2) in combinations(pool, 2):
        if s1 == s2:
            continue
        sim = jaccard(k1, k2)
        if sim >= NEAR_DUP:
            warnings.append(
                f"NEAR-DUPLICATE ({sim:.2f}) in {sec}:\n"
                f"   {s1}: {t1[:80]}\n"
                f"   {s2}: {t2[:80]}"
            )

# 5: species references (or species-specific biology) \u2014 weak check: each item
# should not be *purely* generic. We flag items whose tokens are all in a
# very common-word set.
COMMON = {
    "what","when","where","why","how","this","that","with","from","into","the",
    "and","but","not","for","are","its","their","they","them","have","has","does",
    "can","cannot","about","some","more","most","many","few","still","broadly",
    "accepted","debated","do","not","describe","treat","assume","confuse","call",
    "lens","we","confident","animal","species","wild","field","think",
}
for slug, d in data.items():
    cyc = d.get("alpha_omega_failure_cycle", {})
    for sec in SECTIONS:
        for i, item in enumerate(cyc.get(sec, [])):
            content_tokens = tok(item) - COMMON
            if len(content_tokens) < 3:
                warnings.append(
                    f"{slug}.{sec}[{i}]: thin content (tokens={content_tokens}) \u2014 '{item}'"
                )

# Summary
print("======= QA SUMMARY =======")
print(f"Errors:   {len(errors)}")
print(f"Warnings: {len(warnings)}")
print()
if errors:
    print("--- ERRORS ---")
    for e in errors:
        print("  -", e)
    print()
if warnings:
    print("--- WARNINGS ---")
    for w in warnings:
        print("  -", w)
    print()

# Aggregate uniqueness stats per section
print("--- UNIQUENESS STATS ---")
for sec in SECTIONS:
    all_items = []
    for slug, d in data.items():
        all_items.extend(d.get("alpha_omega_failure_cycle", {}).get(sec, []))
    total = len(all_items)
    unique = len(set(all_items))
    print(f"{sec:30s}  total={total:3d}  unique={unique:3d}  "
          f"({'PASS' if unique == total else 'FAIL'})")

if errors:
    raise SystemExit(1)
print("\nALL HARD CHECKS PASSED.")
