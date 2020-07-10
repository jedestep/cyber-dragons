import math

import numpy as np

from scipy.optimize import LinearConstraint, Bounds, minimize

import util

GOOD_HANDS_1 = 'good_hands_1.txt'
GOOD_HANDS_2 = 'good_hands_2.txt'

def load_hands(fname):
    with open(fname) as f:
        lines = f.readlines()
    hands = []
    for line in lines:
        hands.append(list(map(lambda x: x.strip(), line.split(','))))
    return hands

def card_count_bounds():
    return Bounds(0, 3)

def deck_size_constraint():
    coeff_matrix = np.array([[1] * len(util.CARD_NAME_R_IDX)])
    return LinearConstraint(coeff_matrix, 20, 21)

def hand_negativity_objective(x, good_hands_1, good_hands_2, hand_size=4):
    deck_size = sum(x)
    prob_any_good_hand_t1 = util.prob_any_given_hand(x, good_hands_1, deck_size, hand_size)
    prob_any_good_hand_t2 = util.prob_any_given_hand(x, good_hands_2, deck_size, hand_size+1)

    prob_non_good_hand_t1 = 0.5 * (1 - prob_any_good_hand_t1)
    prob_non_good_hand_t2 = 0.5 * (1 - prob_any_good_hand_t2)

    return prob_non_good_hand_t1 + prob_non_good_hand_t2 - (prob_non_good_hand_t1 * prob_non_good_hand_t2)

def progress_callback(xk, cur_state):
    print(f"""
---
Iteration number: {cur_state.nit}
Current solution attempt: {xk}
Best known solution: {cur_state.x}
---""")

def main():
    good_hands_1 = load_hands(GOOD_HANDS_1)
    good_hands_2 = load_hands(GOOD_HANDS_2)
    x0 = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    result = minimize(hand_negativity_objective, x0,
                      args=(good_hands_1, good_hands_2),
                      method='trust-constr',
                      bounds=card_count_bounds(),
                      constraints=deck_size_constraint(),
                      callback=progress_callback)
    print("Computed decklist")
    total_ct = 0
    for i, count in enumerate(result.x):
        physical_ct = math.ceil(count)
        print(f"{util.CARD_NAME_R_IDX[i]} x{physical_ct}")
        total_ct += physical_ct
    print(f"Deck size: {total_ct} cards")
    print(f"Coin-weighted good hand probability: {result.fun}")


if __name__ == '__main__':
    main()
