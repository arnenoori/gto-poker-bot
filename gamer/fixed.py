from typing import List

def calculate_action(community_cards: List[str], hole_cards: List[str], currentPotValue: int, raiseAmounts: List[int]) -> str:
    # Combine community cards and hole cards
    all_cards = community_cards + hole_cards

    # Determine the strength of the hand
    hand_strength = evaluate_hand_strength(all_cards, hole_cards)
    raisedBy = max(raiseAmounts) if raiseAmounts else 0
    betsBeenMade = raisedBy != 0

    # Calculate the pot odds
    call_amount = raisedBy
    pot_odds = call_amount / (currentPotValue + call_amount)

    # Estimate the probability of winning based on hand strength
    win_probability = hand_strength / 9

    print("\n\n\n")

    print('community_cards', community_cards)
    print('hole_cards', hole_cards)
    print('currentPotValue', currentPotValue)
    print('raiseAmounts', raiseAmounts)
    print('hand_strength', hand_strength)
    print('raisedBy', raisedBy)
    print('betsBeenMade', betsBeenMade)
    print('call_amount', call_amount)
    print('pot_odds', pot_odds / 2)
    print('win_probability', win_probability)

    print("\n\n\n")


    # Make a decision based on hand strength and pot odds
    if not community_cards:
        # Pre-flop
        if hand_strength < 1.45:
            return "fold"
        if betsBeenMade:
            if win_probability > pot_odds / 2:
                return "call"
            else:
                return "fold"
        return "call"
    else:
        # Post-flop
        if betsBeenMade:
            if win_probability > pot_odds:
                return "call"
            else:
                return "fold"
        else:
            return "check"
  

def evaluate_hand_strength(cards: List[str], hole_cards: List[str]) -> float:
    # Convert cards to a format suitable for evaluation
    formatted_cards = [card.split('-') for card in cards]
    ranks = [rank for rank, _ in formatted_cards]
    suits = [suit for _, suit in formatted_cards]
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    numeric_ranks = [rank_values[str(rank)] for rank in ranks]

    # Sort the numeric ranks in ascending order
    sorted_ranks = sorted(numeric_ranks)

    # Calculate the value of the hand based on the current heuristics
    hand_value = 0
    if is_flush(suits) and is_straight(sorted_ranks):
        hand_value = 9
    elif is_four_of_a_kind(sorted_ranks):
        hand_value = 8
    elif is_full_house(sorted_ranks):
        hand_value = 7
    elif is_flush(suits):
        hand_value = 6
    elif is_straight(sorted_ranks):
        hand_value = 5
    elif is_three_of_a_kind(sorted_ranks):
        hand_value = 4
    elif is_two_pair(sorted_ranks):
        hand_value = 3
    elif is_one_pair(sorted_ranks):
        hand_value = 2
    else:
        hand_value = 1

    hole_card_ranks = [rank_values[card.split('-')[0]] for card in hole_cards]
    hole_card_suits = [card.split('-')[1] for card in hole_cards]

    high_card = max(hole_card_ranks)
    low_card = min(hole_card_ranks)

    # Calculate the value of the hole cards (0-1) based on their ranks and suits
    hole_card_value = 0
    if hole_card_suits[0] == hole_card_suits[1]:
        if high_card == 14:  # Ace
            hole_card_value = 0.9
        elif high_card >= 12:  # Queen or higher
            hole_card_value = 0.8 - (high_card - 12) * 0.05
        elif high_card >= 8:  # Ten or higher
            hole_card_value = 0.6 - (high_card - 8) * 0.05
        else:
            hole_card_value = 0.4 - (high_card - 2) * 0.03
    elif abs(high_card - low_card) <= 4:
        if high_card == 14:  # Ace
            hole_card_value = 0.8
        elif high_card >= 12:  # Queen or higher
            hole_card_value = 0.7 - (high_card - 12) * 0.05
        elif high_card >= 8:  # Ten or higher
            hole_card_value = 0.5 - (high_card - 8) * 0.05
        else:
            hole_card_value = 0.3 - (high_card - 2) * 0.03
    else:
        if high_card == 14:  # Ace
            hole_card_value = 0.7
        elif high_card >= 12:  # Queen or higher
            hole_card_value = 0.6 - (high_card - 12) * 0.1
        elif high_card >= 8:  # Ten or higher
            hole_card_value = 0.4 - (high_card - 8) * 0.05
        else:
            hole_card_value = 0.2 - (high_card - 2) * 0.02

    # Add the hand value and the hole card value to get the total hand strength
    total_hand_strength = hand_value + hole_card_value

    return total_hand_strength

from itertools import combinations

def is_flush(suits: List[str]) -> bool:
    for hand in combinations(suits, 5):
        if len(set(hand)) == 1:
            return True
    return False

def is_straight(sorted_ranks: List[int]) -> bool:
    for hand in combinations(sorted_ranks, 5):
        if hand == tuple(range(min(hand), max(hand) + 1)):
            return True
    return False

def is_four_of_a_kind(ranks: List[int]) -> bool:
    for hand in combinations(ranks, 5):
        for rank in hand:
            if hand.count(rank) == 4:
                return True
    return False

def is_full_house(ranks: List[int]) -> bool:
    for hand in combinations(ranks, 5):
        if is_three_of_a_kind(hand) and is_one_pair(hand):
            return True
    return False

def is_three_of_a_kind(ranks: List[int]) -> bool:
    for hand in combinations(ranks, 5):
        for rank in hand:
            if hand.count(rank) == 3:
                return True
    return False

def is_two_pair(ranks: List[int]) -> bool:
    for hand in combinations(ranks, 5):
        pair_count = 0
        seen_ranks = []
        for rank in hand:
            if rank in seen_ranks:
                continue
            if hand.count(rank) == 2:
                pair_count += 1
            seen_ranks.append(rank)
        if pair_count == 2:
            return True
    return False

def is_one_pair(ranks: List[int]) -> bool:
    for hand in combinations(ranks, 5):
        seen_ranks = []
        for rank in hand:
            if rank in seen_ranks:
                return True
            seen_ranks.append(rank)
    return False