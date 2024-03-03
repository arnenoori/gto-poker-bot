from gym_env.enums import Action
import random
from tools.hand_evaluator import get_winner

"""
TODO:
- add a check for the hand type
- add a check for the hand strength
- add a check for the opponent hand strength and then randomly bluff if the bot thinks the probability of the opponent having a weak hand is high and if the bot has a weak hand
- postflop strategy
- 1v1 last round strategy

- better print output using ascii in terminal
"""

class GTOAgent:
    def __init__(self):
        # preflop strategy as defined previously
        self.preflop_strategy = {
            'UTG': ['AA', 'KK', 'QQ', 'JJ', 'AKs', 'AQs'],
            'MP': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AQs', 'AJs', 'KQs'],
            'CO': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs'],
            'BTN': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs'],
            'SB': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs'],
            'BB': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs', 'JTs']
        }
        # simplified postflop strategy
        self.postflop_strategy = {
            'strong_hand': Action.RAISE,
            'medium_hand': Action.CALL,
            'weak_hand': Action.FOLD
        }

    def action(self, observation):
        # simplified action decision based on preflop and postflop strategy
        stage = observation['stage']
        if stage == 'preflop':
            return self.preflop_action(observation)
        else:
            return self.postflop_action(observation)

    def preflop_action(self, observation):
        position = observation['position']
        hole_cards = observation['hole_cards']
        hole_cards_str = ''.join(sorted(hole_cards))

        if hole_cards_str in self.preflop_strategy[position]:
            return Action.RAISE
        else:
            return Action.FOLD

    def postflop_action(self, observation):
        # Use the hand evaluator for a more accurate hand strength assessment
        hand_strength, hand_type = self.evaluate_hand_strength(observation)
         
         # Adjust the decision thresholds based on the hand type or strength
        if hand_type in ['StraightFlush', 'FourOfAKind', 'FullHouse', 'Flush', 'Straight']:
            return self.postflop_strategy['strong_hand']
        elif hand_type in ['ThreeOfAKind', 'TwoPair', 'Pair']:
            return self.postflop_strategy['medium_hand']
        else:
            return self.postflop_strategy['weak_hand']

    def evaluate_hand_strength(self, observation):
        # Use the hand evaluator to determine the hand's strength
        player_hand = observation['hole_cards']
        table_cards = observation['community_cards']
        _, hand_type = get_winner([player_hand], table_cards)
        # For simplicity, we're not calculating a numeric strength but returning the hand type
        # In a more sophisticated implementation, you might calculate a more nuanced hand strength
        return hand_type
    