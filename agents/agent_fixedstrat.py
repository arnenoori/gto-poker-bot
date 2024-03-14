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
        self.preflop_strategy = {
            'UTG': ['AA', 'KK', 'QQ', 'JJ', 'AKs', 'AQs'],
            'MP': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', 'AKs', 'AQs', 'AJs', 'KQs'],
            'CO': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs'],
            'BTN': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs'],
            'SB': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs'],
            'BB': ['AA', 'KK', 'QQ', 'JJ', 'TT', '99', '88', '77', '66', '55', 'AKs', 'AQs', 'AJs', 'ATs', 'KQs', 'KJs', 'KTs', 'QJs', 'QTs', 'JTs']
        }
        self.postflop_strategy = {
            'strong_hand': Action.RAISE,
            'medium_hand': Action.CALL,
            'weak_hand': Action.FOLD
        }

    def action(self, action_space, observation, info):
        stage = observation['stage']
        if stage == 'preflop':
            return self.preflop_action(observation)
        else:
            return self.postflop_action(action_space, observation, info)

    def preflop_action(self, observation):
        position = observation['position']
        hole_cards = observation['hole_cards']
        hole_cards_str = ''.join(sorted(hole_cards))
        if hole_cards_str in self.preflop_strategy[position]:
            return Action.RAISE
        else:
            return Action.FOLD

    def postflop_action(self, action_space, observation, info):
        hand_strength, hand_type = self.evaluate_hand_strength(observation)

        # Adjust the decision thresholds based on the hand type or strength
        if hand_type in ['StraightFlush', 'FourOfAKind', 'FullHouse', 'Flush', 'Straight']:
            action = self.postflop_strategy['strong_hand']
        elif hand_type in ['ThreeOfAKind', 'TwoPair', 'Pair']:
            action = self.postflop_strategy['medium_hand']
        else:
            action = self.postflop_strategy['weak_hand']

        # Bluff with a certain probability if the bot thinks the opponent has a weak hand
        if hand_type not in ['StraightFlush', 'FourOfAKind', 'FullHouse', 'Flush', 'Straight'] and self.opponent_weak_hand_probability(observation) > 0.7:
            if random.random() < 0.3:  # Bluff 30% of the time
                action = Action.RAISE

        # Ensure the chosen action is legal
        if action not in action_space:
            if Action.CHECK in action_space:
                action = Action.CHECK
            else:
                action = Action.FOLD

        return action

    def evaluate_hand_strength(self, observation):
        player_hand = observation['hole_cards']
        table_cards = observation['community_cards']
        _, hand_type = get_winner([player_hand], table_cards)
        return hand_type

    def opponent_weak_hand_probability(self, observation):
        # Implement a more sophisticated logic to estimate the probability of the opponent having a weak hand
        # This can be based on factors like the opponent's previous actions, the community cards, etc.
        # For simplicity, we'll just return a random probability for now
        return random.random()

    def __str__(self):
        return "GTOAgent"