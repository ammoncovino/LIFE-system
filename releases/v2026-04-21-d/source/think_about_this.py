"""Per-species 'Think About This' reflection questions.
Grounded in the master bullets for each species. 12-20 words.
Designed to sit where the locked 'LOOK AT THE ANIMAL' prompt would normally go.
Plain, K-5 safe, no forbidden words.
"""

THINK_ABOUT_THIS = {
    "alpaca": "If your ears could turn to catch every tiny sound, how would you know which noises to trust?",
    "argentine-tegu": "If your tongue could taste the air to find food, where would you point it first?",
    "bennetts-wallaby": "If your back legs were your main way to move, how would you choose a safe place to rest?",
    "black-and-white-ruffed-lemur": "If loud calls told your family where you were, what would your call sound like?",
    "capybara": "If you could stay calm around almost any other animal, who would you want as a neighbor?",
    "geoffroys-spider-monkey": "If your tail worked like an extra hand, what would you pick up first?",
    "kinkajou": "If you lived in the trees and came out only at night, how would you find your food?",
    "linnes-two-toed-sloth": "If moving slowly kept you safe, how would you decide when something is worth moving for?",
    "monkey-tailed-skink": "If you stayed with your family for years, what would you want them to teach you?",
    "nine-banded-armadillo": "If your nose did most of your searching, what would you try to find under the ground?",
    "patagonian-mara": "If you ran fast and bounced like a rabbit, where would you run to feel safe?",
    "prehensile-tailed-porcupine": "If your tail could grab branches like a hand, how would that change the way you climb?",
    "rabbit": "If small sounds could warn you of danger, how quiet would you have to be yourself?",
    "red-ruffed-lemur": "If you could only hear or smell instead of see, how different would your world be?",
    "ring-tailed-lemur": "If you lived in a big group, how would you know your place without anyone speaking?",
    "sailfin-dragon": "If you could run on water for a short time, when would you choose to do it?",
    "sulcata-tortoise": "If you carried your home on your back, what would you want that home to be made of?",
    "toco-toucan": "If your beak was huge but very light, how would you use it to reach the fruit you want?",
    "homo-sapiens": "If every other species on this walk depended on your choices, what would you decide to do differently?",
}

if __name__ == "__main__":
    import json
    for k, v in THINK_ABOUT_THIS.items():
        wc = len(v.split())
        flag = "" if 10 <= wc <= 25 else f"  <-- CHECK ({wc} words)"
        print(f"{wc:3d}  {k:34s}  {v}{flag}")
