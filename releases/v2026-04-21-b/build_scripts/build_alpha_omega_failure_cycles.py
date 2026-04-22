"""
Build per-species Alpha/Omega failure cycles (Option A, four-part).

Each species gets a structured object with four lists derived from
its master bullets only (no outside research):

  alpha_omega_failure_cycle:
    broadly_accepted:             [species-specific solid claims]
    still_debated:                [species-specific edges / open questions]
    common_failure_modes:         [mistakes people commonly make about THIS species]
    species_specific_guardrails:  [hard rules the LLM must follow for THIS species]

The structure is identical across species, but every line of content is
written per-species from its master bullets. No reuse of language between
species beyond normal grammar words.

Outputs overwrite /home/user/workspace/LIFE_tier_content/{slug}_tier2.json,
replacing the previous generic 'alpha_omega_note' string with the new
'alpha_omega_failure_cycle' object.
"""
import json, os

MASTER = "/home/user/workspace/LIFE_totem_content_18.json"
TIER_DIR = "/home/user/workspace/LIFE_tier_content"

# Per-species failure cycles.
# Each entry maps slug -> 4 lists. All content is species-specific.
CYCLES = {
    "black-and-white-ruffed-lemur": {
        "broadly_accepted": [
            "Predominantly frugivorous, dependent on ripe fruit from large-crowned rainforest trees.",
            "Uses loud, coordinated barking calls to warn the group of predators.",
            "Builds nests in the upper trees for infants (unusual compared to many other primates).",
            "Lives in Madagascar's lowland rainforests and is severely affected by deforestation.",
        ],
        "still_debated": [
            "How stable long-term social groupings are outside of feeding congregations.",
            "Exact role of scent marking in mediating between different female lineages.",
            "How much individual recognition is carried in specific call variations.",
        ],
        "common_failure_modes": [
            "Lumping behavior with red ruffed or ring-tailed lemurs (different species, different ecology).",
            "Assuming zoo group structure matches wild group structure.",
            "Treating the barking alarm as 'language' rather than a context-specific signal.",
        ],
        "species_specific_guardrails": [
            "Do not extrapolate from other lemur species without naming the source species.",
            "Do not describe as 'nocturnal' \u2014 this species is day-active.",
            "Do not state precise troop sizes without flagging as 'varies widely by site.'",
        ],
    },
    "red-ruffed-lemur": {
        "broadly_accepted": [
            "Endemic to a single region in northeastern Madagascar (Masoala Peninsula).",
            "Critically endangered with habitat loss and hunting as leading drivers.",
            "Relies on large, mature fruiting trees that ripen at different times of year.",
            "Uses roar-shriek choruses that coordinate between groups, not just within.",
        ],
        "still_debated": [
            "How much of the 'territory' signaling is about space vs. access to specific fruiting trees.",
            "Extent of cooperative infant guarding across unrelated adults.",
            "Precise effect of fruit-crop failure years on reproductive success.",
        ],
        "common_failure_modes": [
            "Confusing its range with the much wider range of the black-and-white ruffed lemur.",
            "Reporting captive litter sizes as if they match wild outcomes.",
            "Calling it 'endangered' when the IUCN listing is 'critically endangered.'",
        ],
        "species_specific_guardrails": [
            "Always use the correct conservation status: Critically Endangered.",
            "Do not generalize Masoala-specific ecology to all of Madagascar.",
            "Do not claim identical behavior to the black-and-white ruffed lemur.",
        ],
    },
    "ring-tailed-lemur": {
        "broadly_accepted": [
            "Spends more time on the ground than almost any other lemur species.",
            "Female-led troop social structure with matriline dominance.",
            "Males use wrist and tail scent glands in 'stink fight' displays during mating season.",
            "Restricted to dry deciduous forest and scrubland in southern Madagascar.",
        ],
        "still_debated": [
            "Whether stink fights are settled ranking contests or opportunistic displays.",
            "How much individual identity vs. group membership is coded into scent marks.",
            "The real cognitive complexity behind troop-wide coordinated movement.",
        ],
        "common_failure_modes": [
            "Assuming behavior seen in captivity (e.g., extended sunbathing on demand) maps 1:1 to the wild.",
            "Confusing it with the other lemurs in our collection because 'lemur' is used loosely in public.",
            "Treating the striped tail as camouflage rather than a scent-carrying signal.",
        ],
        "species_specific_guardrails": [
            "Do not call the species 'common' \u2014 IUCN lists it as Endangered.",
            "Do not describe troop decisions as male-led.",
            "Do not equate 'stink fight' with physical combat \u2014 it is a scent display.",
        ],
    },
    "capybara": {
        "broadly_accepted": [
            "Fully semi-aquatic; water is the primary escape route from jaguars, pumas, and caiman.",
            "Lives in tightly social groups with shared sentinel behavior.",
            "Young can swim within the first week of life.",
            "Several females in a group may nurse each other's young.",
        ],
        "still_debated": [
            "How formal the 'dominance' hierarchy is outside breeding season.",
            "Whether humming and purring carry specific information or just contact-keeping.",
            "How group size adjusts to local predator density over years.",
        ],
        "common_failure_modes": [
            "Over-stating how much it tolerates terrestrial habitat without water access.",
            "Treating its calm temperament in viral video clips as the default wild state.",
            "Confusing 'common in the wild' with 'unaffected by habitat loss.'",
        ],
        "species_specific_guardrails": [
            "Do not imply it is a pet or low-maintenance animal.",
            "Never describe it away from water as a long-term viable state.",
            "Do not compare its group behavior to domestic livestock.",
        ],
    },
    "rabbit": {
        "broadly_accepted": [
            "Sensory system is weighted toward hearing, smell, and wide peripheral vision over central focus.",
            "Lives in warren systems \u2014 networks of burrows, not single dens.",
            "Young are altricial: born blind, hairless, and fully dependent on the nest.",
            "Mother rabbits visit the nest briefly at night and otherwise leave young alone.",
        ],
        "still_debated": [
            "How much social information is coded in chin-rubbing versus fecal pellet placement.",
            "The role of the white-tail flash \u2014 alarm, pursuit deterrent, or both.",
            "Exact population impact of modern predator shifts (domestic cats, etc.).",
        ],
        "common_failure_modes": [
            "Applying domestic pet-rabbit behavior to wild rabbit biology.",
            "Describing solitary behavior when wild rabbits are social within warrens.",
            "Interpreting freezing as 'being scared' rather than as a hard-wired first response.",
        ],
        "species_specific_guardrails": [
            "Do not confuse Oryctolagus cuniculus with hares (Lepus), jackrabbits, or cottontails.",
            "Do not describe the mother abandoning young \u2014 brief visits are normal.",
            "Do not say rabbits 'purr' \u2014 the sound is tooth-grinding, not a vocal purr.",
        ],
    },
    "patagonian-mara": {
        "broadly_accepted": [
            "Forms lifelong monogamous pair bonds \u2014 unusual among large rodents.",
            "Lives in open grassland where long-distance sight lines are essential to survival.",
            "Multiple pairs share communal den areas, but each female nurses only her own pups.",
            "Locomotion is more like a small hoofed animal than a typical rodent.",
        ],
        "still_debated": [
            "Why mara use settlement (communal dens) when pairs are otherwise independent.",
            "How stable pair bonds are under drought or high-mortality years.",
            "Whether urine-marking by males actually deters rivals or just signals identity.",
        ],
        "common_failure_modes": [
            "Calling it a 'hare' \u2014 it is a caviid, not a lagomorph.",
            "Describing it as a herd animal like capybaras \u2014 mara society is built around the pair.",
            "Over-confidence in population stability; it is listed Near Threatened.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as nocturnal; peak activity is dawn and dusk in open daylight.",
            "Do not mix male and female roles \u2014 male guards, female nurses.",
            "Do not extend mara pair-bonding to rabbits or cavies.",
        ],
    },
    "bennetts-wallaby": {
        "broadly_accepted": [
            "Has embryonic diapause: the female can pause development until her pouch is empty.",
            "Spends the hottest hours resting in dense cover and feeds at dawn and dusk.",
            "The joey is born extremely underdeveloped and completes development in the pouch.",
            "Native to Tasmania and mainland Australia in eucalypt forest and coastal heath.",
        ],
        "still_debated": [
            "How much of the thump-warning is aimed at kin vs. all nearby wallabies.",
            "How flexibly the species adapts to fragmented, human-modified landscapes.",
            "Whether forearm-licking is primarily thermoregulation or has a signaling role.",
        ],
        "common_failure_modes": [
            "Using 'kangaroo' interchangeably \u2014 Bennett's is a wallaby, not a kangaroo.",
            "Describing the joey leaving the pouch as 'independent' \u2014 it returns to nurse for months.",
            "Assuming all Australian marsupials share this species' ecology.",
        ],
        "species_specific_guardrails": [
            "Do not call it a kangaroo.",
            "Do not describe a fixed breeding season; diapause shifts timing.",
            "Do not treat predator threats as uniform \u2014 dingoes, foxes, and dogs affect it differently.",
        ],
    },
    "alpaca": {
        "broadly_accepted": [
            "Domesticated from the wild vicu\u00f1a in the Andes thousands of years ago.",
            "Physiologically adapted to high-altitude, low-oxygen mountain grasslands.",
            "Lives in herds where alarm signaling protects all animals simultaneously.",
            "Crias are typically born standing and ready to walk within an hour.",
        ],
        "still_debated": [
            "How much of current herd behavior is domestication vs. inherited wild vicu\u00f1a patterns.",
            "Whether spit signaling is primarily conflict de-escalation or dominance enforcement.",
            "How well individual alpacas recognize humans vs. other alpacas.",
        ],
        "common_failure_modes": [
            "Confusing alpacas with llamas (related, but distinct domesticated species).",
            "Assuming alpacas can thrive at low elevations without management adjustments.",
            "Treating the whole herd as interchangeable; alpacas have strong individual bonds.",
        ],
        "species_specific_guardrails": [
            "Do not call an alpaca a llama or a vicu\u00f1a.",
            "Do not describe it as 'wild' \u2014 it is a domestic species.",
            "Do not imply it is solitary; herd living is required for well-being.",
        ],
    },
    "linnes-two-toed-sloth": {
        "broadly_accepted": [
            "Spends almost its entire life in the trees, only descending roughly once a week to defecate.",
            "Has algae growing in its fur, providing visual camouflage in the leaves.",
            "Very low body-heat production is a core part of its biology, not a bug.",
            "Gives birth while hanging upside down in the branches.",
        ],
        "still_debated": [
            "How much of the weekly descent is ritual vs. flexible under pressure.",
            "The exact ecological role of the fur-algae-moth symbiosis.",
            "Whether apparent stillness reflects low cognition or deliberate concealment.",
        ],
        "common_failure_modes": [
            "Treating slowness as weakness rather than as a working predator-avoidance strategy.",
            "Assuming all sloth species have the same diet or daily rhythm (two-toed vs. three-toed differ).",
            "Describing sloths on the ground as 'normal' \u2014 ground exposure is a high-risk state.",
        ],
        "species_specific_guardrails": [
            "Do not confuse two-toed (Choloepus) with three-toed (Bradypus) sloths.",
            "Never describe it as upright or ground-living in day-to-day life.",
            "Do not claim it 'rarely moves' \u2014 it moves constantly, just slowly.",
        ],
    },
    "monkey-tailed-skink": {
        "broadly_accepted": [
            "One of the only reptiles known to live in stable family groups.",
            "Gives birth to one unusually large, live young \u2014 rare among lizards.",
            "Fully arboreal, using a prehensile tail as a fifth limb in island forest.",
            "Diet is specialized on specific forest plant species in the Solomon Islands.",
        ],
        "still_debated": [
            "How group members coordinate defense of shared branches.",
            "Whether tongue-flicking patterns encode recognition of specific individuals.",
            "The precise impact of pet-trade collection on remaining island populations.",
        ],
        "common_failure_modes": [
            "Describing it as solitary like most reptiles \u2014 family group life is a key feature.",
            "Assuming diet overlap with other skinks \u2014 it is highly specialized.",
            "Confusing its prehensile tail with that of a primate or possum.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as egg-laying; it is live-bearing.",
            "Do not claim its diet 'works for any skink' \u2014 it is species-specific.",
            "Do not imply it is low-risk; IUCN lists it as Vulnerable.",
        ],
    },
    "geoffroys-spider-monkey": {
        "broadly_accepted": [
            "Uses a fission\u2013fusion society: groups split to forage and rejoin to rest.",
            "Prehensile tail functions as a true fifth limb for feeding and travel.",
            "Requires large, connected blocks of rainforest with many fruiting trees.",
            "Reproduces slowly \u2014 one infant every two to three years \u2014 making recovery slow.",
        ],
        "still_debated": [
            "How finely individual recognition is encoded in whinny calls.",
            "How much of the group's movement is led by specific older females vs. consensus.",
            "How well translocated individuals integrate into existing wild groups.",
        ],
        "common_failure_modes": [
            "Lumping with other spider monkey species (Ateles genus has several).",
            "Describing infant independence too early \u2014 mothers carry young well past a year.",
            "Treating fragmented forest as 'enough' habitat when it isn't.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as a small monkey; it is a large-bodied atelid.",
            "Do not claim it can breed 'annually' \u2014 inter-birth interval is multi-year.",
            "Do not conflate with howler or capuchin monkeys in the same range.",
        ],
    },
    "kinkajou": {
        "broadly_accepted": [
            "Active almost exclusively at night; strongly photosensitive.",
            "Travels a learned canopy route between known fruiting trees.",
            "Pollinates certain tropical flowers while feeding with its long tongue.",
            "Not a primate \u2014 it is a procyonid (raccoon family) with convergent climbing traits.",
        ],
        "still_debated": [
            "How stable shared dens and social groupings really are over seasons.",
            "Whether the snort-weedle greeting call carries individual identity.",
            "Full role of scent marking at fruiting trees vs. at sleeping sites.",
        ],
        "common_failure_modes": [
            "Calling it a primate or monkey because of its tail and behavior.",
            "Describing it as a pet-friendly species despite its strict night-active biology.",
            "Attributing group-wide cooperation without clear field evidence.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as a monkey.",
            "Do not suggest daytime activity as normal \u2014 daylight is a hard limit.",
            "Do not state cooperative group defense as fact; it is contested.",
        ],
    },
    "prehensile-tailed-porcupine": {
        "broadly_accepted": [
            "Spends over 85% of its time in the canopy and rarely touches the ground.",
            "Cannot jump \u2014 every between-tree move requires a physical branch connection.",
            "Raises quills and turns sideways as a staged threat display before contact defense.",
            "Produces a single well-developed young with soft spines that harden within hours.",
        ],
        "still_debated": [
            "How scent gland marking interacts with tree-use overlap between individuals.",
            "Whether the young truly becomes independent before reaching adult body size.",
            "How much daytime activity is possible under specific low-pressure conditions.",
        ],
        "common_failure_modes": [
            "Describing it as similar to North American porcupines \u2014 different genus, different ecology.",
            "Assuming it 'shoots' its quills \u2014 it does not.",
            "Underestimating canopy-connectivity requirements when discussing habitat.",
        ],
        "species_specific_guardrails": [
            "Do not say porcupines throw or shoot quills.",
            "Do not treat fragmented forest as survivable habitat; it cannot cross gaps.",
            "Do not confuse with Old World porcupines (Hystrix) \u2014 different family.",
        ],
    },
    "nine-banded-armadillo": {
        "broadly_accepted": [
            "Always gives birth to four identical young from a single fertilized egg (monozygotic quadruplets).",
            "Has poor eyesight but a highly sensitive nose for underground prey.",
            "Can jump straight up when startled \u2014 a real, measurable reflex.",
            "Can swim by swallowing air to increase buoyancy.",
        ],
        "still_debated": [
            "How much its expanding range is climate-driven vs. human-landscape driven.",
            "Whether the startle-jump reflex evolved for predator avoidance, vehicle avoidance, or both.",
            "How strongly scent is used to mark re-used foraging areas.",
        ],
        "common_failure_modes": [
            "Treating 'armadillo' as one species when there are about twenty.",
            "Describing it as nocturnal when it frequently shifts based on disturbance.",
            "Overstating leprosy transmission risk without context.",
        ],
        "species_specific_guardrails": [
            "Do not generalize from Dasypus novemcinctus to the giant or three-banded armadillos.",
            "Do not claim it 'rolls into a ball' \u2014 that's the three-banded species.",
            "Do not describe its shell as pure bone; it is bone plus keratinous scutes.",
        ],
    },
    "sailfin-dragon": {
        "broadly_accepted": [
            "Has a functional parietal ('third') eye on the top of its head used for light sensing.",
            "Drops from basking branches directly into the river to escape predators.",
            "Juveniles can briefly run across the water surface.",
            "Endemic to the Philippines and tied to freshwater river systems.",
        ],
        "still_debated": [
            "How long individuals can actually remain submerged without stress.",
            "The exact signaling function of the male's sail crest beyond dominance.",
            "Population trends in river systems that receive intermittent protection.",
        ],
        "common_failure_modes": [
            "Calling it an iguana \u2014 it is an agamid, different family on a different continent.",
            "Treating all 'sailfin' lizards as one species.",
            "Ignoring its strict freshwater requirement when designing off-exhibit habitat.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as fully terrestrial; it requires a river or equivalent water source.",
            "Do not call it an iguana.",
            "Do not describe juvenile water-running as a long-distance behavior \u2014 it is brief.",
        ],
    },
    "sulcata-tortoise": {
        "broadly_accepted": [
            "Digs deep burrows that are essential shelter from Sahel-region midday heat.",
            "Diet is based on dry, fibrous grasses; soft, watery produce causes problems.",
            "Extremely long-lived, with shell growth tracking decades of its life.",
            "Cold is a genuine health risk \u2014 built for heat, not cold tolerance.",
        ],
        "still_debated": [
            "How far an individual's home range actually extends over multi-year periods.",
            "The relative weight of ram-combat vs. scent signaling in male-male interactions.",
            "How drought years shape long-term reproductive output.",
        ],
        "common_failure_modes": [
            "Feeding watery vegetables as if they were safe staples.",
            "Assuming all tortoises share the same temperature needs.",
            "Underestimating adult size when planning for long-term care.",
        ],
        "species_specific_guardrails": [
            "Do not treat it as a small or short-lived pet species.",
            "Do not offer lettuce, cucumber, or fruit as staples.",
            "Do not expose to sustained cold; burrow access or equivalent shelter is mandatory.",
        ],
    },
    "toco-toucan": {
        "broadly_accepted": [
            "Requires existing hollow tree cavities for nesting \u2014 cannot excavate its own.",
            "The oversized bill has a real thermoregulation role, not just a signaling role.",
            "Both parents incubate and feed the young.",
            "Occurs widely across South American forest edges, open woodland, and savanna.",
        ],
        "still_debated": [
            "How much bill-clacking carries information beyond general excitement.",
            "How sensitive nesting pairs are to specific types of disturbance vs. general human presence.",
            "The species' real long-term response to old-growth tree loss.",
        ],
        "common_failure_modes": [
            "Describing it as a rainforest specialist \u2014 it also uses savanna and edges.",
            "Assuming its diet is 'fruit only' \u2014 it opportunistically takes insects, eggs, and small vertebrates.",
            "Using the big bill as an explanation for everything.",
        ],
        "species_specific_guardrails": [
            "Do not describe the bill as solid bone; it is a light, structured keratin-covered form.",
            "Do not treat all toucan species as ecologically interchangeable.",
            "Do not describe it as deep-forest only.",
        ],
    },
    "argentine-tegu": {
        "broadly_accepted": [
            "Enters a seasonal low-activity period in the burrow during cold months.",
            "Can raise body temperature several degrees above ambient during breeding season.",
            "Females actively guard nests and regulate nest temperature.",
            "Omnivorous \u2014 eats eggs, insects, small vertebrates, fruit, and carrion.",
        ],
        "still_debated": [
            "How widespread facultative endothermy is across the year, not just breeding.",
            "How strongly scent trails carry identity vs. simple location information.",
            "Invasive-population dynamics in areas outside its native range.",
        ],
        "common_failure_modes": [
            "Calling it cold-blooded in the simple sense \u2014 breeding-season physiology is more complex.",
            "Treating it as a monitor lizard \u2014 tegus are teiids, not varanids.",
            "Ignoring its impact where it has been introduced outside South America.",
        ],
        "species_specific_guardrails": [
            "Do not describe it as a monitor lizard.",
            "Do not claim it is fully ectothermic year-round without qualification.",
            "Do not ignore invasive-population concerns when discussing distribution.",
        ],
    },
}


def main():
    # sanity: one entry per species
    with open(MASTER) as f:
        master = json.load(f)
    master_slugs = {sp["slug"] for sp in master["species"]}
    cycle_slugs = set(CYCLES.keys())
    missing = master_slugs - cycle_slugs
    extra   = cycle_slugs - master_slugs
    if missing or extra:
        print("SLUG MISMATCH")
        print("  missing cycles for:", missing)
        print("  extra cycles:", extra)
        raise SystemExit(1)

    wrote = 0
    for slug, cycle in CYCLES.items():
        t2_path = os.path.join(TIER_DIR, f"{slug}_tier2.json")
        if not os.path.exists(t2_path):
            print(f"SKIP (no Tier 2 file): {slug}")
            continue
        with open(t2_path) as f:
            data = json.load(f)
        # Remove old generic note, add new structured object
        data.pop("alpha_omega_note", None)
        data["alpha_omega_failure_cycle"] = {
            "description": (
                "Four-part per-species failure cycle. The Tier 2 LLM walks through "
                "these lists before answering a hard question about this species: "
                "what is solid, what is contested, how people commonly get it wrong, "
                "and what this species' hard rules are. Content is species-specific "
                "and derived from master bullets."
            ),
            "broadly_accepted":           cycle["broadly_accepted"],
            "still_debated":              cycle["still_debated"],
            "common_failure_modes":       cycle["common_failure_modes"],
            "species_specific_guardrails": cycle["species_specific_guardrails"],
        }
        with open(t2_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        wrote += 1
        print(f"WROTE {t2_path}")

    print()
    print(f"Updated {wrote} Tier 2 files with per-species failure cycles.")

if __name__ == "__main__":
    main()
