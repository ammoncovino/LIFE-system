"""Photorealistic documentary wildlife photo prompts for each species.

Locked prompt pattern (proven with red ruffed lemur):
  "Photorealistic photograph of a {species} {action} in {habitat}. {features}.
   Natural dappled sunlight, soft bokeh green/earth background. Sharp focus,
   three-quarter view. Shot with a DSLR telephoto lens, natural colors,
   documentary wildlife photography style. No illustrations, no painting style,
   no text, no borders."
"""

PHOTO_PROMPTS = {
    "black-and-white-ruffed-lemur": (
        "Photorealistic photograph of a black and white ruffed lemur sitting on a mossy rainforest branch. "
        "Distinctive black face and fluffy white-and-black fur, bright yellow eyes, long tail curled. "
        "Natural dappled sunlight through Madagascar rainforest canopy, soft bokeh green background. "
        "Sharp focus, three-quarter view. Shot with a DSLR telephoto lens, natural colors, "
        "documentary wildlife photography style. No illustrations, no painting style, no text, no borders."
    ),
    "ring-tailed-lemur": (
        "Photorealistic photograph of a ring-tailed lemur sitting upright on a sun-warmed rock, "
        "long black-and-white ringed tail draped. Gray fur, white belly, dark triangular face mask, "
        "amber eyes. Natural morning light in a dry Madagascar forest, soft bokeh tan and green background. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "capybara": (
        "Photorealistic photograph of a capybara resting at the edge of a South American wetland, "
        "half-submerged in shallow water. Barrel-shaped body, brown coarse fur, calm expression. "
        "Soft late-afternoon sunlight, reeds and water reflections in soft bokeh background. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "geoffroys-spider-monkey": (
        "Photorealistic photograph of a Geoffroy's spider monkey hanging from a rainforest tree limb "
        "by its prehensile tail, reaching with a long dark arm. Dark brown fur, pale face ring, expressive eyes. "
        "Warm filtered canopy light, deep green jungle bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "kinkajou": (
        "Photorealistic photograph of a kinkajou on a rainforest branch at twilight, "
        "large glossy eyes catching light, small rounded ears, golden-brown fur, long prehensile tail. "
        "Soft bluish dusk light with warm highlights, deep green bokeh canopy background. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "linnes-two-toed-sloth": (
        "Photorealistic photograph of a Linne's two-toed sloth hanging upside down from a rainforest branch, "
        "shaggy greenish-brown fur, sleepy half-closed eyes, curved claws gripping the limb. "
        "Warm filtered rainforest light, lush green bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "nine-banded-armadillo": (
        "Photorealistic photograph of a nine-banded armadillo foraging on the forest floor, "
        "hard banded shell, long pointed snout, pink nose close to fallen leaves, tail extended behind. "
        "Golden late-afternoon sunlight, leaf litter and soft brown bokeh background. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "patagonian-mara": (
        "Photorealistic photograph of a Patagonian mara standing alert on dry Argentine grassland, "
        "long legs, hare-like face, gray-brown back with white belly, large dark eyes. "
        "Soft golden-hour sunlight, wide open pampas bokeh in soft tan and olive tones. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "prehensile-tailed-porcupine": (
        "Photorealistic photograph of a prehensile-tailed porcupine climbing a rainforest branch, "
        "yellowish quills, rounded dark face, pink nose, long gripping tail curled around the limb. "
        "Warm canopy light, deep green jungle bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "alpaca": (
        "Photorealistic photograph of an alpaca standing in an Andean highland pasture, "
        "thick fleece, alert ears, gentle dark eyes, soft distant mountains behind. "
        "Clean high-altitude sunlight, green pasture bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "rabbit": (
        "Photorealistic photograph of a European rabbit sitting in a meadow, "
        "soft gray-brown fur, large alert ears, dark eyes, whiskers catching light. "
        "Soft morning sunlight, wildflower meadow bokeh in green and gold. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "bennetts-wallaby": (
        "Photorealistic photograph of a Bennett's wallaby standing upright on Tasmanian grassland, "
        "reddish-brown fur, pale chest, upright tail, long hind legs, alert pointed ears. "
        "Soft overcast light, eucalyptus forest edge bokeh in soft green-grey. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "toco-toucan": (
        "Photorealistic photograph of a toco toucan perched on a tropical tree branch, "
        "massive orange bill, striking blue eye-ring, black body and white bib. "
        "Warm tropical sunlight, lush green rainforest bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "argentine-tegu": (
        "Photorealistic photograph of an Argentine black and white tegu lizard basking on a sun-warmed rock, "
        "muscular body with black-and-white banded scales, thick tail, alert eye. "
        "Warm low sunlight, grassland bokeh in soft green-brown. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "monkey-tailed-skink": (
        "Photorealistic photograph of a monkey-tailed skink on a mossy rainforest branch, "
        "large green-and-black scaled body, prehensile tail curled around the limb, alert dark eye. "
        "Warm filtered canopy light, deep green rainforest bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "sailfin-dragon": (
        "Photorealistic photograph of a sailfin dragon lizard perched on a mossy log beside a jungle stream, "
        "tall crested sail along its back, green-and-tan scales, long whip tail, alert golden eye. "
        "Soft filtered jungle light, bokeh of green ferns and water highlights. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),
    "sulcata-tortoise": (
        "Photorealistic photograph of a sulcata tortoise walking across dry savanna grassland, "
        "large domed brown-and-tan shell with growth ridges, thick scaled legs, calm face. "
        "Warm golden sunlight, soft dry-grass bokeh. "
        "Sharp focus, three-quarter view. DSLR telephoto, natural colors, documentary wildlife style. "
        "No illustrations, no painting style, no text, no borders."
    ),

    # Homo sapiens: science-forward, respectful, non-confrontational
    "homo-sapiens": (
        "Photorealistic photograph of a modern Homo sapiens — a person of mixed heritage — "
        "in soft natural outdoor light, looking thoughtfully toward the camera, "
        "warm skin tones, gentle expression. Earth-tone clothing. "
        "Soft green-and-gold bokeh natural background. "
        "Sharp focus, three-quarter portrait view. DSLR telephoto, natural colors, documentary style. "
        "No illustrations, no painting style, no text, no borders."
    ),
}
