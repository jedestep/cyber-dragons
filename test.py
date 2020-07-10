import opti
import util

card_counts = {
    'core': 3,
    'og': 1,
    'cfs': 1,
    'econ': 2,
    'vier': 2,
    'gate': 1,
    'herald': 1,
    'cosmic': 3,
    'cyberload': 3,
    'overflow': 3
}
print(f"total prob {util.prob_any([0.5, 0.5])}")
print(f"total prob {util.prob_any([0.5, 0.5, 0.5])}")

h1 = ['core']
h2 = ['og', 'cfs']
print(f"conjunction is {util.hand_conjunction(card_counts,h1,h2)}")

good_hands_2 = opti.load_hands(opti.GOOD_HANDS_2)
conjs = util.find_nonzero_conjunction_hands(card_counts, good_hands_2, 20)
print(f"list of all conjunctions from GH2 is {conjs}")
