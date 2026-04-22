"""
Generate 18 canonical K-5 JSON files — one per species.

Rule: "We simplify ANSWERS, not STRUCTURE."
- Locked 8 questions (exact wording, exact order)
- K-5 ceiling, K-2 floor
- 10-19 words per answer
- Real vocab allowed (rainforest, predators, keen, plentiful, environment)
- Forbidden: binocular, canopy, anogenital, territory, diurnal, nocturnal,
  brumation, metabolic rate, chemical particles, perception, vocalization,
  psychological, talk/talks/talking
- Tagline: "A [X] [Y] that lives in [Z]."
- Pocket pattern: [1, 2, 3, 5, 8]

Each JSON is derived from its master bullets (LIFE_master_per_species/{slug}.txt).
"""
import json, os, re

OUT_DIR = "/home/user/workspace/LIFE_k5_locked"
os.makedirs(OUT_DIR, exist_ok=True)

VERSION = "v2026.04.21-b"
LOCKED_AT = "2026-04-21"

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
POCKET = [1, 2, 3, 5, 8]

# --- Per-species K-5 data ---------------------------------------------------
# Each entry: species name, slug, character_name, tagline, and 8 K-5 answers.
# Answers: 10-19 words, real vocab, forbidden words excluded, derived from bullets.

SPECIES = [
    {
        "species": "Black-and-White Ruffed Lemur",
        "slug": "black-and-white-ruffed-lemur",
        "character_name": "Luna the Lemur",
        "tagline": "A fruit-eating lemur that lives in Madagascar.",
        "answers": [
            "It uses sharp eyes, strong ears, and a keen nose to find ripe fruit and sense danger nearby.",
            "It lives high in Madagascar's rainforest trees, where fruit is plentiful and predators cannot reach it.",
            "It uses loud barking calls to warn the group of danger and to keep family members in contact.",
            "When something changes, it may freeze and watch, or leap quickly to a safer branch above.",
            "Young lemurs learn by watching older ones and copying how they find food and avoid danger.",
            "Mothers build nests in the trees, and babies depend on the group for food and protection.",
            "It needs tall rainforest trees and quiet space. Without its forest, it cannot survive.",
            "Every animal survives based on what its senses can reach and what its environment provides.",
        ],
    },
    {
        "species": "Red Ruffed Lemur",
        "slug": "red-ruffed-lemur",
        "character_name": "Rosa the Red Lemur",
        "tagline": "A fruit-eating lemur that lives in one small Madagascar forest.",
        "answers": [
            "It smells scent marks, listens for barking alarms, and uses sharp eyes to judge branch to branch.",
            "It lives only in one rainforest corner of Madagascar, where tall trees carry fruit all year.",
            "It gives loud barking calls to warn of danger and roars with the group to claim its home.",
            "When a predator is near, it calls out, moves quietly together, and hides in the thick trees.",
            "Babies follow their mother, watch which trees hold ripe fruit, and learn alarm calls early in life.",
            "A mother builds a high nest and has two or three babies; other adults help guard them.",
            "It needs a large, healthy rainforest. With so little left, it is critically endangered.",
            "An animal that depends on one small forest teaches us how fragile an environment can be.",
        ],
    },
    {
        "species": "Ring-Tailed Lemur",
        "slug": "ring-tailed-lemur",
        "character_name": "Rin the Ring-Tailed Lemur",
        "tagline": "A striped-tailed lemur that lives in dry Madagascar forests.",
        "answers": [
            "It reads scents on branches, hears group alarms, and greets friends by sniffing noses.",
            "It lives in Madagascar's dry forests, spending more time on the ground than most lemurs.",
            "Males rub scent on their striped tails and wave them, and the group calls out to warn of danger.",
            "It sunbathes to warm up, and the whole group moves together when a leader spots a threat.",
            "Babies ride on their mother, then copy adults to learn which plants are safe to eat.",
            "A mother has one baby after about 135 days, and the whole group helps protect it.",
            "It needs tall trees for sleeping safely and a healthy dry forest that is quickly disappearing.",
            "Using scent as a message shows that animals can trade information without teeth or claws.",
        ],
    },
    {
        "species": "Capybara",
        "slug": "capybara",
        "character_name": "Cappy the Capybara",
        "tagline": "A grass-eating rodent that lives in rivers and wetlands.",
        "answers": [
            "Its eyes sit high, its ears pick up soft splashes, and its nose knows every friend in the group.",
            "It lives near rivers and flooded grasslands, where water is an escape and mud keeps skin cool.",
            "It barks a sharp warning, hums and purrs to stay in contact, and uses scent to mark plants.",
            "When startled, the whole group rushes into the water, and it can hold its breath for minutes.",
            "Young ones follow adults to feeding spots and learn which sounds mean danger is coming.",
            "A mother has two to eight babies, and several females take turns nursing the whole group's young.",
            "Without water close by, it cannot hide from big predators or cool off in the heat.",
            "One animal watching the water's edge can keep the whole group safe.",
        ],
    },
    {
        "species": "Rabbit",
        "slug": "rabbit",
        "character_name": "Roo the Rabbit",
        "tagline": "A grass-eating mammal that lives in meadows and field edges.",
        "answers": [
            "Long ears swivel toward sounds, wide-set eyes watch all around, and a sniffing nose checks for danger.",
            "It lives in meadows and woodland edges, with soft soil to dig a tunnel system called a warren.",
            "It thumps its back feet hard to warn others, and a flash of white tail tells rabbits to run.",
            "When something changes, it freezes, then bolts in a zigzag toward the nearest cover.",
            "Young rabbits watch their mother and older rabbits to learn safe feeding spots and alarm signals.",
            "A mother has five or six blind, hairless babies in a hidden nest, and visits them at night.",
            "Open ground with no cover forces it to stay near its burrow, ready to sprint for safety.",
            "A calm rabbit is still watching and smelling everything — sensing trouble before it arrives.",
        ],
    },
    {
        "species": "Patagonian Mara",
        "slug": "patagonian-mara",
        "character_name": "Mira the Mara",
        "tagline": "A long-legged rodent that lives in the open grasslands of Argentina.",
        "answers": [
            "Big eyes and long ears watch flat land far away, and its nose knows its mate and pups.",
            "It lives in open grassland where it can see predators coming from a long way off.",
            "It leaps high to show strength, and males mark their partner with scent to warn other males.",
            "When danger comes, the male runs out in front, and the pair stays close together.",
            "Pups follow their parents, watch which plants to eat, and learn alarm calls in their first weeks.",
            "Pairs bond for life and share big dens, but each mother only nurses her own pups.",
            "Dense plants block its view, so loss of open grassland leaves it without food or safety.",
            "Open space looks empty to us but is full of signals to an animal that lives there.",
        ],
    },
    {
        "species": "Bennett's Wallaby",
        "slug": "bennetts-wallaby",
        "character_name": "Willa the Wallaby",
        "tagline": "A grass-eating marsupial that lives in Australian forests.",
        "answers": [
            "Each ear turns on its own, wide eyes see almost all around, and its feet feel ground vibrations.",
            "It lives in eucalypt forest with open grassy spots — shade to rest and grass to graze.",
            "It thumps a back foot to warn other wallabies, and a heavy, fast hop tells the group to scatter.",
            "It rests in shade during the hottest part of the day and hops into thick brush when scared.",
            "A joey travels in its mother's pouch and watches what she eats before grazing on its own.",
            "A tiny newborn crawls into the pouch and grows there, nursing for about nine months.",
            "It needs both open grass and dense cover, so clearing the forest leaves it exposed to dogs.",
            "Its daily routine is timed around heat, not just hunger — environment shapes its whole day.",
        ],
    },
    {
        "species": "Alpaca",
        "slug": "alpaca",
        "character_name": "Alo the Alpaca",
        "tagline": "A woolly grazer that lives in the high Andes Mountains.",
        "answers": [
            "Tall ears turn toward sounds, wide eyes spot movement on open slopes, and its nose knows the herd.",
            "It lives on cold mountain grasslands very high up, where the herd shares warmth and safety.",
            "It hums quietly to its herd, gives a sharp alarm call, and can spit if crowded too close.",
            "When alarmed, the whole herd groups tightly together and watches before deciding to move.",
            "A baby alpaca stays close to its mother, copies her grazing, and learns alarm signals from adults.",
            "A mother has one baby after about eleven months, and it stands within an hour of birth.",
            "Sudden cold or storms high in the mountains can drive the herd down to lower ground fast.",
            "Its thick coat traps warm air — a quiet example of environment shaping design.",
        ],
    },
    {
        "species": "Linnaeus's Two-Toed Sloth",
        "slug": "linnes-two-toed-sloth",
        "character_name": "Sol the Sloth",
        "tagline": "A slow-moving mammal that lives in rainforest trees.",
        "answers": [
            "Sharp hearing picks up tree movement, a keen nose finds food, and claws feel every branch firmly.",
            "It lives high in the rainforest, hanging upside down, with green algae in its fur as camouflage.",
            "It is mostly silent, but hisses when threatened, slashes with its claws, and stays still to hide.",
            "When disturbed, it moves slowly into thicker leaves and holds still to stay out of sight.",
            "A young sloth clings to its mother for up to a year and learns which leaves to eat.",
            "A mother has one baby while hanging upside down, and carries it everywhere she goes.",
            "It produces little body heat, so on the ground it is nearly helpless against predators.",
            "Being slow and still is a real survival plan, not weakness — it fits the whole forest.",
        ],
    },
    {
        "species": "Monkey-Tailed Skink",
        "slug": "monkey-tailed-skink",
        "character_name": "Mimi the Monkey-Tailed Skink",
        "tagline": "A leaf-eating lizard that lives in Solomon Islands forests.",
        "answers": [
            "Its flickering tongue tastes the air, its eyes see in dim light, and it senses movement on branches.",
            "It lives high in island forest trees, where its gripping tail holds on as it reaches for leaves.",
            "It hisses as a warning, bites if ignored, and rubs scent on branches its family group shares.",
            "When threatened, it grips tight with its tail, turns sideways, and hisses at the approaching danger.",
            "Young skinks stay in the family group for months, and adults protect them as they learn the trees.",
            "A mother carries one big baby inside her body and gives birth live — unusual for a lizard.",
            "It needs special forest plants, so when trees are cut, both its food and its home disappear.",
            "A lizard that lives in a family group teaches us that reptiles can cooperate too.",
        ],
    },
    {
        "species": "Geoffroy's Spider Monkey",
        "slug": "geoffroys-spider-monkey",
        "character_name": "Gia the Spider Monkey",
        "tagline": "A fruit-eating monkey that lives in rainforest trees.",
        "answers": [
            "Forward-facing eyes judge jumps, sharp ears catch faraway calls, and its nose checks if fruit is ripe.",
            "It lives in the tops of huge rainforest trees, where many fruit trees must share one home.",
            "It barks to warn of predators, whinnies to stay in touch, and shakes branches when threatened.",
            "When danger comes, it climbs higher fast, and the group splits up to find food safely.",
            "Babies cling to their mother for more than a year and watch adults to learn safe fruiting trees.",
            "A mother has one baby every two or three years and carries it close for the first months.",
            "It needs huge, unbroken rainforests, so cutting the trees into small pieces starves the group.",
            "Spread out to find food, gather again to rest — the group's shape follows the forest.",
        ],
    },
    {
        "species": "Kinkajou",
        "slug": "kinkajou",
        "character_name": "Kiki the Kinkajou",
        "tagline": "A fruit-eating mammal that lives in rainforest trees at night.",
        "answers": [
            "Big eyes gather dim light, a keen nose finds ripe fruit, and a long tongue reaches into flowers.",
            "It lives high in the rainforest, sleeping in tree holes by day and visiting fruit trees by night.",
            "It greets friends with a snort-weedle call, hisses when angry, and marks branches with its scent.",
            "By day it sleeps deep in its den, and if woken at night it moves quickly to other trees.",
            "Young kinkajous travel with their mother and learn the path from fruit tree to fruit tree.",
            "A mother has one baby with eyes closed, and other group members share the den for protection.",
            "Daylight is a hard limit — and without tall trees, it loses both its food and its bed.",
            "A night out for a kinkajou is a precise, learned journey — memory, not chance.",
        ],
    },
    {
        "species": "Prehensile-Tailed Porcupine",
        "slug": "prehensile-tailed-porcupine",
        "character_name": "Pip the Porcupine",
        "tagline": "A slow climber that lives in South American rainforest trees.",
        "answers": [
            "Long whiskers feel for branches at night, its nose finds food, and its ears catch sounds from below.",
            "It lives in the top of the rainforest, sleeping in high branches and eating leaves, bark, and fruit.",
            "It raises its quills, turns sideways to look bigger, and moans or hisses at predators.",
            "By day it stays hidden and still; at night it wakes up and climbs to a different tree.",
            "A single baby stays with its mother and learns which trees to visit before foraging alone.",
            "A mother has one baby with soft spines that harden in hours, and it can grip branches right away.",
            "It cannot jump, so when trees are cut down, it loses the branches it needs to travel.",
            "Never needing the ground, this animal is shaped entirely by the trees above.",
        ],
    },
    {
        "species": "Nine-Banded Armadillo",
        "slug": "nine-banded-armadillo",
        "character_name": "Andy the Armadillo",
        "tagline": "A digging mammal that lives in grasslands and forest edges.",
        "answers": [
            "Its nose smells bugs deep underground, its ears hear danger, and it stands up to sniff the air.",
            "It lives in grasslands and forest edges, where soft soil lets it dig burrows for sleeping.",
            "Mates make a soft chucking sound, and it stamps its feet and stands tall when alarmed.",
            "When startled, it jumps straight up in the air and then runs quickly into thick cover.",
            "Babies follow their mother, watch where she digs, and learn which soil holds the most bugs.",
            "A mother always has four identical babies, born with eyes open and soft shells that harden.",
            "Cold slows it down fast, and hard rocky ground stops it from digging the burrows it needs.",
            "A sensitive nose is more useful than eyes in its underground world.",
        ],
    },
    {
        "species": "Sailfin Dragon",
        "slug": "sailfin-dragon",
        "character_name": "Sage the Sailfin Dragon",
        "tagline": "A plant-eating lizard that lives in Philippine rivers.",
        "answers": [
            "A small third eye senses light, sharp eyes spot fruit and movement, and it feels currents in the water.",
            "It lives along rivers and mangroves in the Philippines, basking in trees right above the water.",
            "Males raise a tall sail on their back, turn darker, and bob their heads to show they are boss.",
            "When a predator gets close, it drops from a branch into the river and hides underwater.",
            "Hatchlings are on their own from day one and learn by practicing swimming and diving.",
            "A mother digs a nest near water and lays two to eight eggs that hatch after about sixty days.",
            "Without a river nearby, it has no escape, and loss of bank trees takes its basking spots.",
            "The river is a refuge, a travel route, and a place to hide — all in one.",
        ],
    },
    {
        "species": "Sulcata Tortoise",
        "slug": "sulcata-tortoise",
        "character_name": "Tilly the Tortoise",
        "tagline": "A grass-eating tortoise that lives in the African Sahel grasslands.",
        "answers": [
            "Its nose finds dry grass, its eyes spot movement, and it feels vibrations through the ground.",
            "It lives in Africa's dry grasslands, digging deep burrows to escape the midday heat.",
            "Males make a loud mating call, ram each other with their shells, and move to water after rain.",
            "In peak heat it hides in its burrow; in very dry times it moves less to save energy.",
            "Young tortoises hatch alone and learn by trying which plants to eat in their new home.",
            "A mother digs a nest and lays up to thirty eggs, which hatch about ninety days later.",
            "Cold is dangerous for it, and without burrows or shade, it can quickly overheat and die.",
            "Slow body, dry diet, and deep burrows all work together as one survival system.",
        ],
    },
    {
        "species": "Toco Toucan",
        "slug": "toco-toucan",
        "character_name": "Tico the Toucan",
        "tagline": "A fruit-eating bird that lives in South American forest edges.",
        "answers": [
            "Its long bill reaches fruit on thin branches, its eyes spot ripe color, and its ears hear other toucans.",
            "It lives in forest edges and open woodland, where tree holes make safe nests high up.",
            "It gives a deep, repeated croaking call, clacks its bill at rivals, and poses to show mood.",
            "When alarmed, it flies in a quick, bouncing path and watches the danger from a high perch.",
            "Young toucans beg loudly for food and follow their parents to learn which trees hold ripe fruit.",
            "A pair lays two to four eggs in a tree hole, and both parents take turns sitting and feeding.",
            "It cannot carve its own nest, so cutting down big old trees takes away its only nesting site.",
            "Its big bill reaches food, signals to other birds, and helps keep its body cool.",
        ],
    },
    {
        "species": "Argentine Black-and-White Tegu",
        "slug": "argentine-tegu",
        "character_name": "Tego the Tegu",
        "tagline": "A big lizard that lives in South American forests and savanna.",
        "answers": [
            "Its forked tongue tastes the air, its nose finds bugs under leaves, and it feels ground vibrations.",
            "It lives in forest edges and savanna, digging deep burrows for shelter, winter rest, and eggs.",
            "It hisses when cornered, puffs up its body at rivals, and males leave scent trails for females.",
            "If threatened, it runs or stands and hisses; in cold months, it rests in its burrow without eating.",
            "Young tegus hatch alone and learn by trying — flicking their tongue to check new things.",
            "A mother lays eggs in a burrow or termite mound and guards the nest with her own body heat.",
            "Without warm basking spots, it cannot digest food, and cold forces it underground for months.",
            "Activity, digestion, and having babies all tie directly to temperature for this lizard.",
        ],
    },
]

# --- Sanity check: word counts + forbidden words ----------------------------
def word_count(s):
    return len([w for w in re.findall(r"\b\w+\b", s)])

errors = []
for sp in SPECIES:
    # 8 answers required
    if len(sp["answers"]) != 8:
        errors.append(f"{sp['slug']}: needs 8 answers, has {len(sp['answers'])}")
        continue
    for i, a in enumerate(sp["answers"], 1):
        wc = word_count(a)
        if wc < 10 or wc > 19:
            errors.append(f"{sp['slug']} Q{i}: {wc} words — '{a}'")
        lower = a.lower()
        for bad in FORBIDDEN:
            # whole-word match (avoid false hit on e.g. "all talk" inside "small talk")
            if re.search(rf"\b{re.escape(bad)}\b", lower):
                errors.append(f"{sp['slug']} Q{i}: FORBIDDEN '{bad}' in '{a}'")
    # tagline format: "A [X] that lives in [Y]."
    t = sp["tagline"]
    if not (t.startswith("A ") and " that lives in " in t and t.endswith(".")):
        errors.append(f"{sp['slug']}: tagline bad format — '{t}'")

if errors:
    print("=== VALIDATION ERRORS ===")
    for e in errors:
        print("  -", e)
    # do not write files if errors
    raise SystemExit(1)

# --- Write 18 JSONs ---------------------------------------------------------
for sp in SPECIES:
    data = {
        "version": VERSION,
        "locked_at": LOCKED_AT,
        "species": sp["species"],
        "slug": sp["slug"],
        "character_name": sp["character_name"],
        "tagline": sp["tagline"],
        "reading_level": "K-5 ceiling, K-2 floor",
        "answers": {
            str(i+1): {"q": LOCKED_QS[i], "a": sp["answers"][i]} for i in range(8)
        },
        "closing_prompt": CLOSING,
        "footer": FOOTER,
        "micro_pocket_questions": POCKET,
        "forbidden_words": FORBIDDEN,
    }
    out_path = os.path.join(OUT_DIR, f"{sp['slug']}.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"WROTE {out_path}")

# Summary
print()
print(f"Generated {len(SPECIES)} K-5 JSONs in {OUT_DIR}")
