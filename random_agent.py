import random

class RandomAgent:
    def __init__(self, action_size):
        self.action_size = action_size

    def act(self, community_cards, player_hand, pot, current_bet):
        return random.randint(0, self.action_size - 1)

def calculate_action(agent, community_cards, player_hand, pot, current_bet):
    action_idx = agent.act(community_cards, player_hand, pot, current_bet)
    return ['fold', 'call', 'raise'][action_idx]