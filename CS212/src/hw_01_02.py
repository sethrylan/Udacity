
black_wilds = ['?B', [(n + suit) for n in ['2','3','4','5','6','7','8','9','T','J','Q','K','A'] for suit in ['S','C']]]
red_wilds = ['?R', [(n + suit) for n in ['2','3','4','5','6','7','8','9','T','J','Q','K','A'] for suit in ['H','D']]]

import itertools


def replace_wildcards(hand):
    if black_wilds[0] in hand:
        hand.remove(black_wilds[0])
        return itertools.product([hand], black_wilds[1])

#        return itertools.izip([hand], black_wilds[1])
#        return (i[0].extend(i[1]) for i in itertools.product([hand], black_wilds[1]))

if __name__ == "__main__":

    hand = "6C 7C 8C 9C TC 5C ?B".split()
    hands = []
    for i in replace_wildcards(hand):
        hands.append(i[0].append(i[1]))
    for h in hands:
        print h
