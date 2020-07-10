import math

from functools import reduce
from itertools import combinations

from scipy.special import comb

CARD_NAME_N_IDX = {
    "core": 0,
    "vier": 1,
    "og": 2,
    "cyberload": 3,
    "overflow": 4,
    "herald": 5,
    "gate": 6,
    "cosmic": 7,
    "cfs": 8,
    "econ": 9,
}

CARD_NAME_R_IDX = {
    0: "core",
    1: "vier",
    2: "og",
    3: "cyberload",
    4: "overflow",
    5: "herald",
    6: "gate",
    7: "cosmic",
    8: "cfs",
    9: "econ",
}


def mult(*args):
    return reduce(lambda x, y: x * y, args)

def prob_any(args):
    total_prob = 0
    n = len(args)
    for k in range(1, n+1):
        sign = (-1) ** (k+1)
        all_tuples = [ele for ele in combinations(args, k)]
        for t in all_tuples:
            total_prob += sign * mult(*t)
    return total_prob

def prob_specific_hand(card_counts, hand_cards, deck_size, hand_size=4):
    numerator = 1
    # positive terms for each hand card; do this _without_ replacement
    picked_so_far = {}
    for card in hand_cards:
        card_count = card_counts[card]
        numerator *= comb(math.ceil(card_count) - picked_so_far.get(card, 0), 1, exact=False, repetition=False)
        if card not in picked_so_far:
            picked_so_far[card] = 0
        picked_so_far[card] += 1
    # draw arbitrary additional cards, if the specific hand we got was nonspecific
    extra_cards = hand_size - len(hand_cards)
    if extra_cards > 0:
        numerator *= comb(deck_size - len(hand_cards), extra_cards)
    denominator = comb(deck_size, hand_size)
    return numerator / denominator

def prob_any_given_hand(x, hands, deck_size, hand_size=4):
    hand_probs = []
    card_counts = { CARD_NAME_R_IDX[i]: ct for i, ct in enumerate(x) }
    for hand in hands:
        hand_probs.append(prob_specific_hand(card_counts, hand, deck_size, hand_size))
    extra_counted_hands = find_nonzero_conjunction_hands(card_counts, hands, deck_size, hand_size)
    extra_hand_probs = []
    for hand in extra_counted_hands:
        prob = prob_specific_hand(card_counts, hand, deck_size, hand_size)
        k = len(hand)
        prob = prob * ((-1) ** (k+1))
        extra_hand_probs.append(prob)

    positive_counts = sum(hand_probs)
    negative_counts = sum(extra_hand_probs)
    return positive_counts + negative_counts
    """
    ret = prob_any(hand_probs)
    return ret
    """

def find_nonzero_conjunction_hands(card_counts, hands, deck_size, hand_size=4):
    hands_queue = hands.copy()
    all_conjunctions = []
    while hands_queue:
        hand = hands_queue.pop()
        for other_hand in hands_queue:
            conjunction = hand_conjunction(card_counts, hand, other_hand, hand_size)
            if conjunction:
                all_conjunctions.append(conjunction)
                hands_queue.append(conjunction)
    return all_conjunctions

def hand_conjunction(card_counts, hand, other_hand, hand_size=4):
    hand_d = convert_hand_to_dict(hand)
    other_hand_d = convert_hand_to_dict(other_hand)

    for card, ct in other_hand_d.items():
        if card not in hand_d:
            hand_d[card] = 0
        hand_d[card] += ct

    # validate that the conjunction is legal
    # if it's illegal, return None
    if sum(hand_d.values()) > hand_size:
        return
    for card, ct in hand_d.items():
        if ct > card_counts[card]:
            return

    # convert back to hand format
    out = []
    for card, ct in hand_d.items():
        for i in range(ct):
            out.append(card)
    return out

def convert_hand_to_dict(hand):
    d = {}
    for card in hand:
        if card not in d:
            d[card] = 0
        d[card] += 1
    return d
