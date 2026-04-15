#!/usr/bin/env python3
"""
Build Student Totem PDFs for 11 species — single multi-page PDF, one page per species.
"""

import urllib.request
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle

# ── Fonts ──────────────────────────────────────────────────────────────────
FONT_DIR = Path("/tmp/fonts")
FONT_DIR.mkdir(exist_ok=True)

FONT_URLS = {
    "DMSans-Regular": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "DMSans-Bold": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
    "DMSans-Italic": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans-Italic%5Bopsz%2Cwght%5D.ttf",
}

# Download and register fonts
for name, url in FONT_URLS.items():
    path = FONT_DIR / f"{name}.ttf"
    if not path.exists():
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, path)

pdfmetrics.registerFont(TTFont("DMSans", str(FONT_DIR / "DMSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Bold", str(FONT_DIR / "DMSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DMSans-Italic", str(FONT_DIR / "DMSans-Italic.ttf")))

# ── Colors ─────────────────────────────────────────────────────────────────
NAVY = HexColor("#2C3481")
TEAL = HexColor("#00AAAD")
DARK_TEXT = HexColor("#1E1E2E")
LIGHT_GRAY = HexColor("#F0F2F5")
MID_GRAY = HexColor("#6B7280")
BORDER_GRAY = HexColor("#D1D5DB")

# ── Page dimensions ────────────────────────────────────────────────────────
W, H = letter  # 612 x 792
MARGIN_L = 54
MARGIN_R = 54
MARGIN_T = 48
MARGIN_B = 42
CONTENT_W = W - MARGIN_L - MARGIN_R

# ── Styles for Paragraph rendering ─────────────────────────────────────────
style_q = ParagraphStyle(
    "Question",
    fontName="DMSans-Bold",
    fontSize=9.5,
    leading=12.5,
    textColor=NAVY,
    spaceAfter=1,
)
style_a = ParagraphStyle(
    "Answer",
    fontName="DMSans",
    fontSize=9,
    leading=12,
    textColor=DARK_TEXT,
    spaceAfter=0,
)

# ── Species Data ───────────────────────────────────────────────────────────
species_data = [
    {
        "common": "Red Ruffed Lemur",
        "scientific": "Varecia rubra",
        "questions": [
            ("What can it sense?",
             "Red ruffed lemurs have a strong sense of smell and good hearing. They depend on scent glands on their wrists and backsides to recognize group members and mark their territory."),
            ("Where does it live?",
             "They live high in the rainforest canopy on the Masoala Peninsula of Madagascar. They rarely come down to the ground."),
            ("How does it move?",
             "They leap between tree branches and hang upside down to reach fruit. Their strong hands and feet grip branches tightly."),
            ("How does it communicate?",
             "They bark, shriek, and roar to warn about predators and keep the group together. Different alarm calls tell the group whether danger is in the air or on the ground."),
            ("How does it learn?",
             "Young lemurs learn which fruits are safe to eat and which trees to use by following their mothers. They also learn alarm calls by watching how adults react to threats."),
            ("What are its limits?",
             "They can only live in tropical rainforest and depend on ripe fruit. If the forest is cut down, they have nowhere else to go. They are critically endangered."),
            ("What does this teach us?",
             "An animal that uses smell more than sight experiences the forest very differently than we do. The same place can feel like a different world depending on your senses."),
            ("Think About This",
             "If you could smell who had walked through a room hours earlier, how would that change the way you understood your school?"),
        ],
    },
    {
        "common": "Ring-Tailed Lemur",
        "scientific": "Lemur catta",
        "questions": [
            ("What can it sense?",
             "Ring-tailed lemurs have a powerful sense of smell but relatively poor eyesight. They can recognize individual friends by matching a scent to a voice."),
            ("Where does it live?",
             "They live in dry forests and scrubby areas in southern Madagascar. Unlike most lemurs, they spend a lot of time on the ground."),
            ("How does it move?",
             "They walk on all fours on the ground and climb through trees. They hold their striped tails high in the air so the group can follow each other."),
            ("How does it communicate?",
             'Males have "stink fights" — they rub scent from their wrists onto their tails and wave them at rivals. They also purr, howl, and bark.'),
            ("How does it learn?",
             "Young lemurs stay close to their mothers for over a year, learning where to find food, which plants are safe, and how to behave in the group."),
            ("What are its limits?",
             "They need warm weather and cannot survive cold winters. Their habitat in Madagascar is shrinking, making them endangered."),
            ("What does this teach us?",
             "Ring-tailed lemurs show that communication is not just about sounds — a smell can carry a message just as clearly as a word."),
            ("Think About This",
             "Why might holding your tail high in the air be a good way to help your friends follow you through tall grass?"),
        ],
    },
    {
        "common": "Black-and-White Ruffed Lemur",
        "scientific": "Varecia variegata",
        "questions": [
            ("What can it sense?",
             "They have excellent hearing and a strong sense of smell. They use scent glands to mark branches and recognize other group members."),
            ("Where does it live?",
             "They live in the rainforests of eastern Madagascar, spending most of their time in the highest parts of the tree canopy."),
            ("How does it move?",
             "They leap long distances between trees and can hang upside down by their feet to reach fruit. They move on all fours along branches."),
            ("How does it communicate?",
             "They have some of the loudest calls of any primate. Whole groups join in roaring choruses that can be heard far through the forest to warn about predators."),
            ("How does it learn?",
             "Mothers build nests high in the trees and \"park\" their babies there while foraging. Young lemurs learn to find food and respond to calls by watching adults."),
            ("What are its limits?",
             "They are the most fruit-dependent of all lemurs. When fruit is scarce, the group must split into smaller parties to find enough food. They are critically endangered."),
            ("What does this teach us?",
             "When your entire group screams together, the sound is bigger than any one voice. Sometimes survival depends on teamwork."),
            ("Think About This",
             "Why do you think the whole group joins in the alarm call instead of just one lemur calling out?"),
        ],
    },
    {
        "common": "Giraffe",
        "scientific": "Giraffa camelopardalis",
        "questions": [
            ("What can it sense?",
             "Giraffes have excellent eyesight and can spot a predator from very far away. They also hum at frequencies too low for humans to hear."),
            ("Where does it live?",
             "They live in African savannahs, grasslands, and open woodlands. Their height lets them eat leaves that no other animal can reach."),
            ("How does it move?",
             "They walk by swinging both legs on the same side at once, which makes them sway gracefully. They can run up to 35 miles per hour in short bursts."),
            ("How does it communicate?",
             "Giraffes communicate mostly through staring — a long, steady look can warn others of danger or tell them to stay away. They also use low-frequency hums and snorts."),
            ("How does it learn?",
             "Calves stand up within an hour of birth and learn which trees are safe to eat from by watching their mothers. Young males learn fighting skills through gentle neck-sparring with other young males."),
            ("What are its limits?",
             "Drinking water is dangerous — they must spread their legs wide and lower their long neck, leaving them vulnerable to predators. Their height makes it hard to hide."),
            ("What does this teach us?",
             "The same feature that gives an advantage — a long neck for reaching food — also creates a weakness. Every adaptation comes with a trade-off."),
            ("Think About This",
             "If you were as tall as a giraffe, what everyday things would become easier — and what would become harder?"),
        ],
    },
    {
        "common": "Two-Toed Sloth",
        "scientific": "Choloepus didactylus",
        "questions": [
            ("What can it sense?",
             "Sloths have an excellent sense of smell and their ears are tuned to low-frequency sounds. Their eyesight is not very sharp."),
            ("Where does it live?",
             "They live high in the canopy of tropical rainforests in Central and South America. They spend almost their entire life in the trees."),
            ("How does it move?",
             "They move very slowly, hanging upside down from branches with long, curved claws. They come down from the trees about once a week to go to the bathroom."),
            ("How does it communicate?",
             "They are mostly silent animals. When upset, they hiss like a deflating balloon. Babies make soft squealing sounds to call their mothers."),
            ("How does it learn?",
             "Baby sloths cling to their mothers for months, learning which leaves are safe to eat. Young sloths may inherit their mother's home range of trees."),
            ("What are its limits?",
             "They move so slowly they cannot run from predators — they rely on camouflage instead. Green algae grows on their fur, helping them blend in with the leaves."),
            ("What does this teach us?",
             "Being slow is not always a disadvantage. Moving slowly saves energy and helps sloths avoid being noticed — a completely different survival strategy than speed."),
            ("Think About This",
             "Can you think of a time when slowing down helped you notice something you would have missed if you were rushing?"),
        ],
    },
    {
        "common": "Blue-and-Gold Macaw",
        "scientific": "Ara ararauna",
        "questions": [
            ("What can it sense?",
             "They have sharp eyesight with excellent color vision. They can see ultraviolet light that is invisible to humans, which helps them find ripe fruit."),
            ("Where does it live?",
             "They live in tropical forests, woodlands, and swamps from Central America to South America. They nest in holes high up in dead palm trees."),
            ("How does it move?",
             "They are strong fliers with long wings, and they can also climb through trees using their beaks as a third grip. Their feet have two toes forward and two back for gripping."),
            ("How does it communicate?",
             "They make loud squawks and screaming calls that carry over long distances. They also blush — their bare white face skin turns pink to show emotion, and they ruffle their head feathers."),
            ("How does it learn?",
             "They are very intelligent and can learn to use tools, solve puzzles, and mimic human speech. Young macaws stay with their parents for up to three years, learning what to eat and how to behave."),
            ("What are its limits?",
             "They need large, old trees for nesting. When forests are cut, they lose their homes. They also mate for life, so losing a partner is a serious problem."),
            ("What does this teach us?",
             "Macaws show that intelligence comes in many forms. A bird that can solve problems, blush, and talk is using a brain very different from ours to do surprisingly similar things."),
            ("Think About This",
             "If a macaw can learn words but doesn't understand their meaning the way we do, is it really \"talking\"? What makes communication real?"),
        ],
    },
    {
        "common": "Lorikeet",
        "scientific": "Trichoglossus moluccanus",
        "questions": [
            ("What can it sense?",
             "Lorikeets have excellent color vision that helps them spot brightly colored flowers. They can also see ultraviolet patterns on petals that guide them to nectar."),
            ("Where does it live?",
             "They live along the coasts of eastern Australia in forests, parks, and gardens — anywhere flowering trees like eucalyptus grow."),
            ("How does it move?",
             "They are fast, agile fliers that travel in noisy flocks. They use their strong feet to hang upside down from branches while feeding on flowers."),
            ("How does it communicate?",
             "They screech, chatter, and make rolling calls, especially in flight. Large groups roost together at dusk and are extremely noisy. Some can learn to mimic human words."),
            ("How does it learn?",
             "Young lorikeets learn which flowers to visit and how to use their brush-tipped tongue by watching adults. They are curious and quick to explore new things."),
            ("What are its limits?",
             "Their special brush-like tongue is perfect for nectar but cannot crack hard seeds. They depend on flowering trees — without blooming plants, they cannot survive."),
            ("What does this teach us?",
             "A lorikeet's tongue is shaped like a tiny paintbrush, built perfectly for one job. Being specialized makes you very good at one thing — but dependent on it."),
            ("Think About This",
             "Their scientific name Trichoglossus means \"hairy tongue.\" Why would a tiny brush on your tongue be useful for drinking nectar from deep inside a flower?"),
        ],
    },
    {
        "common": "Cownose Ray",
        "scientific": "Rhinoptera bonasus",
        "questions": [
            ("What can it sense?",
             "Cownose rays can detect the tiny electrical signals that all living things give off. Special sensors on their snout called electroreceptors help them find prey hidden under sand."),
            ("Where does it live?",
             "They live in warm ocean waters along the Atlantic coast of the Americas. They swim in large schools that can include thousands of rays."),
            ("How does it move?",
             'They "fly" through the water by flapping their wide, flat pectoral fins like wings. They can also leap out of the water and land with a loud belly slap.'),
            ("How does it communicate?",
             "They communicate through body movements like leaping and by sensing each other's electrical fields. Scientists believe they may use water pressure changes to stay together in large schools."),
            ("How does it learn?",
             "Baby rays are born live and can swim immediately. They learn to dig for clams by flapping their fins to stir up sand and using suction to uncover hidden prey."),
            ("What are its limits?",
             "Their flat teeth can crush shells but cannot bite or chew other food. They can only eat what lives on or under the ocean floor, like clams, oysters, and crabs."),
            ("What does this teach us?",
             "Cownose rays have a sense that humans completely lack — electroreception. There are signals all around us that we cannot detect without special tools."),
            ("Think About This",
             "If you could feel the electricity given off by every living thing near you, how would a walk through a garden feel different?"),
        ],
    },
    {
        "common": "Sulcata Tortoise",
        "scientific": "Centrochelys sulcata",
        "questions": [
            ("What can it sense?",
             "Sulcata tortoises can sense vibrations through the ground and may use the Earth's magnetic field to navigate. They have a good sense of smell to find food."),
            ("Where does it live?",
             "They live at the edge of the Sahara Desert in Africa, in hot, dry grasslands and scrubland. It is one of the harshest places on Earth."),
            ("How does it move?",
             "They walk slowly on sturdy, elephant-like legs, conserving energy. They dig deep burrows — sometimes over 10 feet underground — to escape extreme heat."),
            ("How does it communicate?",
             "Males ram each other during contests and make grunting sounds. They communicate mostly through body position and movement rather than sound."),
            ("How does it learn?",
             "Hatchlings must find their own food from day one. They learn to seek shade, dig burrows, and find moisture-rich plants to survive the desert."),
            ("What are its limits?",
             "As cold-blooded reptiles, they cannot control their body temperature from the inside. They must move between sun and shade or retreat to burrows to stay the right temperature."),
            ("What does this teach us?",
             "Sulcata tortoises show that survival in a harsh desert depends on building the right shelter. Their burrows are an engineering solution to a temperature problem."),
            ("Think About This",
             "They get almost all their water from the plants they eat, not from drinking. What would you have to eat if you could never drink a glass of water?"),
        ],
    },
    {
        "common": "Veiled Chameleon",
        "scientific": "Chamaeleo calyptratus",
        "questions": [
            ("What can it sense?",
             "Each eye moves independently, giving them nearly 360-degree vision. They can see ultraviolet light and spot tiny insects from 5 to 10 meters away."),
            ("Where does it live?",
             "They live in trees and bushes on the Arabian Peninsula in Yemen and Saudi Arabia, in habitats from mountain forests to dry valleys."),
            ("How does it move?",
             "They grip branches with pincer-like feet and move in a slow, swaying walk that mimics a leaf blowing in the wind. Their tongue shoots out at lightning speed to catch insects."),
            ("How does it communicate?",
             "They change color to send signals — bright colors warn rivals, and females show their mood through color patterns. They also send tiny vibrations through branches that other chameleons can feel."),
            ("How does it learn?",
             "Young chameleons are on their own from birth. They must quickly learn to hunt with their tongue, change color for camouflage, and identify threats."),
            ("What are its limits?",
             "They cannot hear airborne sounds well and have no outer ear. They are solitary and stressed by the presence of other chameleons in a small space."),
            ("What does this teach us?",
             "Chameleons show that changing your appearance is a form of language. Color is their voice — they speak by changing what they look like."),
            ("Think About This",
             "If your skin changed color to show how you felt, would it be easier or harder to get along with your friends?"),
        ],
    },
    {
        "common": "Chinchilla",
        "scientific": "Chinchilla lanigera",
        "questions": [
            ("What can it sense?",
             "Chinchillas have very large ears and sharp hearing to detect predators in the dark. They also have big eyes with vertical pupils for seeing in low light."),
            ("Where does it live?",
             "They live high in the Andes Mountains of South America, up to 14,000 feet, in rocky, cold, dry areas. They shelter in crevices between boulders."),
            ("How does it move?",
             "They are amazing jumpers and can leap up to 6 feet. They hop and bounce across rocks with great agility, even in near-darkness."),
            ("How does it communicate?",
             "They chirp when happy, bark to warn of danger, and chatter their teeth when annoyed. A colony has at least one lookout who whistles if a predator appears."),
            ("How does it learn?",
             "Baby chinchillas are born with fur and open eyes, ready to explore. They learn which plants to eat and where danger lurks by following adults in the colony."),
            ("What are its limits?",
             "Their fur is so thick — up to 80 hairs per follicle — that it cannot dry if it gets wet, which could cause dangerous fungal infections. They must bathe in dust instead of water."),
            ("What does this teach us?",
             "The chinchilla's super-dense fur is perfect for freezing mountain nights but creates a problem with water. Every amazing adaptation has a hidden cost."),
            ("Think About This",
             "If you had fur so thick that water could never dry out of it, how would you stay clean? What would you invent?"),
        ],
    },
]


# ── Build PDF ──────────────────────────────────────────────────────────────
OUTPUT = "/home/user/workspace/LIFE_system/print_ready/STUDENT_TOTEMS_ALL_SPECIES.pdf"

c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("Student Totems — K-5 Signs — LIFE System")
c.setAuthor("Perplexity Computer")

for sp_idx, sp in enumerate(species_data):
    y = H - MARGIN_T

    # ── Top accent bar ─────────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.rect(0, H - 6, W, 6, stroke=0, fill=1)

    # ── Species common name ────────────────────────────────────────────
    y -= 4
    c.setFillColor(NAVY)
    c.setFont("DMSans-Bold", 22)
    c.drawString(MARGIN_L, y, sp["common"].upper())
    y -= 18

    # ── Scientific name ────────────────────────────────────────────────
    c.setFillColor(MID_GRAY)
    c.setFont("DMSans-Italic", 11)
    c.drawString(MARGIN_L, y, sp["scientific"])
    y -= 16

    # ── Divider line ───────────────────────────────────────────────────
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.5)
    c.line(MARGIN_L, y, W - MARGIN_R, y)
    y -= 16

    # ── Subtitle / Tagline ─────────────────────────────────────────────
    c.setFillColor(NAVY)
    c.setFont("DMSans-Italic", 9)
    c.drawString(MARGIN_L, y, "\"What a living thing can sense becomes its reality.\"")
    y -= 18

    # ── Image placeholder box ──────────────────────────────────────────
    img_box_h = 72
    img_box_w = CONTENT_W
    c.setStrokeColor(BORDER_GRAY)
    c.setLineWidth(0.75)
    c.setFillColor(LIGHT_GRAY)
    c.roundRect(MARGIN_L, y - img_box_h, img_box_w, img_box_h, 6, stroke=1, fill=1)
    c.setFillColor(MID_GRAY)
    c.setFont("DMSans", 10)
    c.drawCentredString(W / 2, y - img_box_h / 2 - 4, f"[ {sp['common']} Image ]")
    y -= img_box_h + 14

    # ── Questions ──────────────────────────────────────────────────────
    for q_idx, (q_label, answer) in enumerate(sp["questions"]):
        num = q_idx + 1
        is_think = q_label == "Think About This"

        # Number circle
        circle_r = 8
        circle_x = MARGIN_L + circle_r
        circle_y = y - circle_r + 2

        if is_think:
            # Special styling for Think About This
            c.setFillColor(NAVY)
            c.roundRect(MARGIN_L, y - 44, CONTENT_W, 46, 6, stroke=0, fill=1)
            c.setFillColor(white)
            c.setFont("DMSans-Bold", 9.5)
            c.drawString(MARGIN_L + 12, y - 2, f"{num}. Think About This")
            # Render answer as paragraph inside the box
            think_style = ParagraphStyle(
                "ThinkAnswer",
                fontName="DMSans-Italic",
                fontSize=8.5,
                leading=11.5,
                textColor=white,
            )
            p = Paragraph(answer, think_style)
            pw, ph = p.wrap(CONTENT_W - 24, 100)
            p.drawOn(c, MARGIN_L + 12, y - 2 - ph - 6)
            y -= 56
        else:
            # Teal number circle
            c.setFillColor(TEAL)
            c.circle(circle_x, circle_y, circle_r, stroke=0, fill=1)
            c.setFillColor(white)
            c.setFont("DMSans-Bold", 9)
            c.drawCentredString(circle_x, circle_y - 3.5, str(num))

            # Question text
            text_x = MARGIN_L + circle_r * 2 + 8
            text_w = CONTENT_W - circle_r * 2 - 8

            c.setFillColor(NAVY)
            c.setFont("DMSans-Bold", 9.5)
            c.drawString(text_x, y, q_label)
            y -= 13

            # Answer using Paragraph for wrapping
            p = Paragraph(answer, style_a)
            pw, ph = p.wrap(text_w, 200)
            p.drawOn(c, text_x, y - ph + 2)
            y -= ph + 10

    # ── Footer ─────────────────────────────────────────────────────────
    # Bottom accent bar
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 28, stroke=0, fill=1)
    c.setFillColor(white)
    c.setFont("DMSans-Bold", 8)
    c.drawCentredString(W / 2, 10, "LIFE  —  Language  ·  Intelligence  ·  Form  ·  Ecology")

    # Teal accent line above footer
    c.setStrokeColor(TEAL)
    c.setLineWidth(2)
    c.line(0, 28, W, 28)

    if sp_idx < len(species_data) - 1:
        c.showPage()

c.save()
print(f"✓ PDF saved: {OUTPUT}")
print(f"  Pages: {len(species_data)}")
