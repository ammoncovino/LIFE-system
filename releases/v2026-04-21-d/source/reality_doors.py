"""Reality Door content per species — v2026.04.21-d LOCKED.

A Reality Door is an honest, non-ideological explanation block sitting in its own
boxed panel on each totem. It answers the one question every visitor has:

    "Why is this animal here instead of the wild?"

Framing rules (owner-approved):
  - No attacks on groups, no "PETA", no religion, no "go back to school".
  - Honest bridge-habitat language. Factual about habitat pressure.
  - Explains why human care is a bridge, not a permanent answer.
  - Names small actions that matter.

STANDARDIZED STRUCTURE (every species, no exceptions):
  opening:        one short line stating why it is here.
  habitat_lines:  exactly 2 lines on habitat + pressure.
  shrink_bullets: exactly 3 things that happen when habitat shrinks.
  life_park_note: optional line about LIFE Park's specific role.

Rendering adds the standardized bridge line (BRIDGE_LINE) after the bullets.
"""

STANDARD_ROLE_BULLETS = [
    "protecting forests and wild places",
    "supporting conservation work",
    "learning how animals actually live",
]

BRIDGE_LINE = "This place is not their natural home, but it can help keep the species alive."


REALITY_DOORS = {
    # ================= LEMURS =================
    "red-ruffed-lemur": {
        "opening": "Red ruffed lemurs live in only one small corner of Madagascar.",
        "habitat_lines": [
            "Most of their rainforest has been cut down or changed by people.",
            "What is left is broken into small, isolated patches.",
        ],
        "shrink_bullets": [
            "fruit and food trees disappear",
            "groups become cut off from each other",
            "survival gets harder each year",
        ],
        "life_park_note": (
            "LIFE Park cares for one of the largest lemur populations "
            "in the United States, acting as a bridge while the wild recovers."
        ),
    },
    "black-and-white-ruffed-lemur": {
        "opening": "Black and white ruffed lemurs live only in Madagascar's eastern rainforests.",
        "habitat_lines": [
            "Their forests are being cleared for farms, charcoal, and roads.",
            "They depend on big old trees that take decades to replace.",
        ],
        "shrink_bullets": [
            "ripe fruit becomes rare and seasonal",
            "family groups lose the tall trees they nest in",
            "they become one of the most endangered mammals on Earth",
        ],
        "life_park_note": (
            "LIFE Park helps care for part of one of the largest lemur populations "
            "in the United States."
        ),
    },
    "ring-tailed-lemur": {
        "opening": "Ring-tailed lemurs live in the dry forests of southern Madagascar.",
        "habitat_lines": [
            "Drought, fire, and land clearing keep shrinking their habitat.",
            "The dry forests they need are disappearing faster than they can recover.",
        ],
        "shrink_bullets": [
            "food and water become harder to find each year",
            "troops lose the sunning rocks and trees they depend on",
            "wild numbers have dropped sharply in recent decades",
        ],
        "life_park_note": (
            "LIFE Park helps care for part of one of the largest lemur populations "
            "in the United States."
        ),
    },

    # ================= NEW WORLD MAMMALS =================
    "capybara": {
        "opening": "Capybaras live near wetlands, rivers, and ponds across South America.",
        "habitat_lines": [
            "Wetlands are being drained for farming and building.",
            "Capybaras need both water and open grass to stay safe and cool.",
        ],
        "shrink_bullets": [
            "less water means fewer places to hide from predators",
            "family groups get pushed onto smaller, drier patches of land",
            "wild wetlands — home to many species — keep shrinking",
        ],
    },
    "geoffroys-spider-monkey": {
        "opening": "Spider monkeys live high in the rainforest canopy of Central America.",
        "habitat_lines": [
            "Their forests are being cut for farmland, cattle, and timber.",
            "They need tall, connected trees to swing and feed across huge areas.",
        ],
        "shrink_bullets": [
            "gaps in the canopy cut families off from food",
            "slow breeding means lost groups are hard to replace",
            "they are listed as endangered across most of their range",
        ],
    },
    "kinkajou": {
        "opening": "Kinkajous live in the rainforest canopies of Central and South America.",
        "habitat_lines": [
            "Their forests are being cleared for logging and agriculture.",
            "They need tall, connected trees to move safely at night.",
        ],
        "shrink_bullets": [
            "flowering and fruiting trees become scarce",
            "they are pushed to the ground, where danger is higher",
            "they are also taken from the wild for the pet trade",
        ],
    },
    "linnes-two-toed-sloth": {
        "opening": "Two-toed sloths live in the rainforests of Central and South America.",
        "habitat_lines": [
            "Their forests are fragmented by roads, power lines, and farms.",
            "Sloths move so slowly they cannot cross open ground safely.",
        ],
        "shrink_bullets": [
            "they get stranded in small patches of trees",
            "crossing roads and wires injures or kills many",
            "low numbers of young make populations slow to recover",
        ],
    },
    "nine-banded-armadillo": {
        "opening": "Nine-banded armadillos live across the Americas, from Argentina to the southern U.S.",
        "habitat_lines": [
            "Unlike most species here, they are expanding — not shrinking.",
            "Warmer winters and new farmland let them spread farther north.",
        ],
        "shrink_bullets": [
            "other native species get displaced as armadillos move in",
            "road deaths are one of the biggest pressures they face",
            "human landscapes still shape where they can and cannot live",
        ],
    },
    "patagonian-mara": {
        "opening": "Maras live in the dry grasslands of central and southern Argentina.",
        "habitat_lines": [
            "Their grasslands are being plowed for farming and ranching.",
            "They need wide, open ground to run from predators.",
        ],
        "shrink_bullets": [
            "fences and crops cut their grasslands into pieces",
            "pairs lose the open space they need to raise young",
            "their wild range keeps shrinking each decade",
        ],
    },
    "prehensile-tailed-porcupine": {
        "opening": "Prehensile-tailed porcupines live high in Central and South American forests.",
        "habitat_lines": [
            "Their forests are being cleared for farms, cattle, and roads.",
            "They need connected canopies to move between trees at night.",
        ],
        "shrink_bullets": [
            "broken canopies force them down to dangerous ground",
            "fewer trees mean fewer leaves, bark, and fruit to eat",
            "small, slow-breeding groups are easy to lose",
        ],
    },
    "alpaca": {
        "opening": "Alpacas are a domesticated species, shaped by people over thousands of years.",
        "habitat_lines": [
            "They come from the high Andes of Peru, Bolivia, and Chile.",
            "Today they live almost entirely on farms and ranches, not in the wild.",
        ],
        "shrink_bullets": [
            "their wild ancestor, the vicuña, was nearly hunted to extinction",
            "mountain ecosystems in the Andes are changing with climate and grazing",
            "careful, small-scale farming still supports Andean communities",
        ],
    },
    "rabbit": {
        "opening": "Domestic rabbits come from the European rabbit, still wild in parts of Europe.",
        "habitat_lines": [
            "Wild European rabbits are now endangered across much of their range.",
            "Disease, habitat loss, and hunting have reduced their numbers sharply.",
        ],
        "shrink_bullets": [
            "fewer wild rabbits means less food for lynx, eagles, and foxes",
            "whole ecosystems depend on this one small animal",
            "domestic rabbits need careful care — they are not disposable pets",
        ],
    },

    # ================= MARSUPIAL =================
    "bennetts-wallaby": {
        "opening": "Bennett's wallabies live in the forests and grasslands of eastern Australia and Tasmania.",
        "habitat_lines": [
            "Fires, drought, and land clearing keep reshaping their habitat.",
            "Roads, fences, and new development keep them cut off from old paths.",
        ],
        "shrink_bullets": [
            "food becomes patchy after major bushfires",
            "family groups are split by roads and fenced land",
            "predators like feral cats and foxes make survival harder",
        ],
    },

    # ================= BIRDS =================
    "toco-toucan": {
        "opening": "Toco toucans live in the woodlands, savannas, and forest edges of South America.",
        "habitat_lines": [
            "Their tropical forests are being cleared for soy, cattle, and timber.",
            "They need tall, hollow trees to nest in and plenty of fruit trees to feed.",
        ],
        "shrink_bullets": [
            "nesting holes become rare as old trees are cut",
            "fruiting trees get scattered and harder to reach",
            "they are also captured for the illegal pet trade",
        ],
    },

    # ================= REPTILES =================
    "argentine-tegu": {
        "opening": "Argentine tegus live in the grasslands and forests of central South America.",
        "habitat_lines": [
            "Their habitat is being cleared for farming and cattle.",
            "They also face pressure from the pet trade and road deaths.",
        ],
        "shrink_bullets": [
            "nesting and basking sites are lost to farmland",
            "released pets have started invading new places like Florida",
            "invasions hurt native wildlife where tegus do not belong",
        ],
    },
    "monkey-tailed-skink": {
        "opening": "Monkey-tailed skinks live only in the Solomon Islands, high in rainforest trees.",
        "habitat_lines": [
            "Their forests are being logged for timber export.",
            "They are also heavily collected for the international pet trade.",
        ],
        "shrink_bullets": [
            "they give birth to just one large baby at a time",
            "losing even a few adults hurts the whole population",
            "they are listed as one of the most threatened skinks in the world",
        ],
    },
    "sailfin-dragon": {
        "opening": "Sailfin dragons live along rivers and streams in the Philippines and Indonesia.",
        "habitat_lines": [
            "Their riverside forests are being cleared and polluted.",
            "They are also collected from the wild for the pet trade.",
        ],
        "shrink_bullets": [
            "cleaner, cooler streams are harder to find",
            "riverbank trees they need for basking are lost",
            "wild populations keep shrinking across their range",
        ],
    },
    "sulcata-tortoise": {
        "opening": "Sulcata tortoises live in the dry grasslands south of the Sahara Desert.",
        "habitat_lines": [
            "Their grasslands are drying out and being converted to farmland.",
            "They are also collected heavily for the pet trade worldwide.",
        ],
        "shrink_bullets": [
            "food and water become harder to find in a drying climate",
            "pet tortoises grow huge and often outlive their owners",
            "released pets rarely survive and cannot always go back",
        ],
    },

    # ================= HOMO SAPIENS =================
    # Treated as a peer species, not a throne above.
    "homo-sapiens": {
        "opening": "Humans are one species among many — shaped by the same forces of evolution.",
        "habitat_lines": [
            "We live in almost every habitat on Earth, from deserts to cities.",
            "Our choices now shape the habitats of almost every other species.",
        ],
        "shrink_bullets": [
            "our farms, roads, and cities replace wild habitats",
            "our climate choices change weather, water, and food everywhere",
            "every species on this totem walk depends on what we do next",
        ],
        "life_park_note": (
            "Understanding that we belong to the animal kingdom — "
            "not above it — is the first step toward protecting it."
        ),
    },
}


def get_reality_door(slug):
    """Return the Reality Door for a slug, or a safe factual fallback."""
    if slug in REALITY_DOORS:
        return REALITY_DOORS[slug]
    return {
        "opening": "This species is here as part of a bridge program.",
        "habitat_lines": [
            "Its wild habitat is under pressure from habitat change.",
            "Human care provides a safe, stable environment while the wild recovers.",
        ],
        "shrink_bullets": [
            "food and shelter become harder to find",
            "populations can get cut off from each other",
            "survival in the wild becomes harder",
        ],
    }


# Backwards compat (some earlier code imported this)
STANDARD_CARE_BULLETS = [
    "they cannot safely return to the wild",
    "their habitat no longer supports them",
    "they are part of breeding programs that protect the species",
]


if __name__ == "__main__":
    print(f"{len(REALITY_DOORS)} reality doors drafted")
    for slug in sorted(REALITY_DOORS):
        print(f"  {slug}")
