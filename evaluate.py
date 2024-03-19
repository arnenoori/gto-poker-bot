import random
from typing import List
from dqn_agent import PokerEnv, DQNAgent
from gamer.fixed import calculate_action as fixed_calculate_action
from random_agent import RandomAgent, calculate_action as random_calculate_action
import matplotlib.pyplot as plt

# Evaluate 1000 games between random action, fixed action, and DQN agent

# Constants
NUM_CARDS = 52
STARTING_STACK = 1000
SMALL_BLIND = 10
BIG_BLIND = 20

class PokerEnvEvaluator(PokerEnv):
    def __init__(self):
        super().__init__()
        self.current_player = 0

    def reset(self):
        state = super().reset()
        self.current_player = 0
        return state

    def step(self, action):
        next_state, reward, done, _ = super().step(action)
        if not done:
            # Switch to the other player
            self.current_player = (self.current_player + 1) % 3  # Modify this line
        return next_state, reward, done, _

def random_action(community_cards, player_hand, pot, current_bet):
    return random.choice(['fold', 'call', 'raise'])

def simulate_hand(env: PokerEnvEvaluator, dqn_agent: DQNAgent, fixed_model, random_model, hand_num: int):
    state = env.reset()
    done = False
    actions = []
    print(f"\nHand {hand_num + 1}:")
    while not done:
        if env.current_player == 0:  # DQN agent's turn
            action = dqn_agent.act(state, eval_mode=True)
            print(f"DQN Agent action: {env.action_space[action]}")
        elif env.current_player == 1:  # Fixed model's turn
            # Convert card indices to readable strings
            rank_values = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: '10', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
            suits = ['♠', '♥', '♦', '♣']
            community_cards = [f"{rank_values[card % 13]}-{suits[card // 13]}" for card in env.community_cards]
            player_hand = [f"{rank_values[card % 13]}-{suits[card // 13]}" for card in env.player_hand]
            
            action = fixed_model(community_cards, player_hand, env.pot, [env.current_bet])  # Pass current_bet as a list
            if action not in env.action_space:
                # Handle the case when the fixed model returns an invalid action
                if action == 'fold':
                    action = 0  # Map 'fold' to the corresponding index in action_space
                elif action == 'call':
                    action = 1  # Map 'call' to the corresponding index in action_space
                elif action == 'raise':
                    action = 2  # Map 'raise' to the corresponding index in action_space
                else:
                    action = 1  # Default to 'call' action if an unknown action is returned
            print(f"Fixed Model action: {env.action_space[action]}")
        else:  # Random model's turn
            action = random_model(None, None, None, None)  # Pass dummy values
            if action not in env.action_space:
                action = 1  # Default to 'call' action if an unknown action is returned
            print(f"Random Model action: {env.action_space[action]}")
        actions.append(action)
        next_state, reward, done, _ = env.step(action)
        state = next_state
    print(f"Hand {hand_num + 1} result: {'DQN Agent wins' if reward > 0 else 'Fixed Model wins' if reward < 0 else 'Tie'}")
    return reward, actions

def simulate_game(env: PokerEnv, dqn_agent: DQNAgent, fixed_model, random_model, num_hands: int):
    dqn_wins = 0
    fixed_wins = 0
    random_wins = 0
    ties = 0
    dqn_win_history = []
    fixed_win_history = []
    random_win_history = []
    tie_history = []
    for hand_num in range(num_hands):
        reward, _ = simulate_hand(env, dqn_agent, fixed_model, random_model, hand_num)
        if reward > 0:
            dqn_wins += 1
        elif reward < 0:
            if env.current_player == 1:
                fixed_wins += 1
            else:
                random_wins += 1
        else:
            ties += 1
        dqn_win_history.append(dqn_wins)
        fixed_win_history.append(fixed_wins)
        random_win_history.append(random_wins)
        tie_history.append(ties)
    print(f"\nResults after {num_hands} hands:")
    print(f"DQN Agent Wins: {dqn_wins}")
    print(f"Fixed Model Wins: {fixed_wins}")
    print(f"Random Model Wins: {random_wins}")
    print(f"Ties: {ties}")
    
    # Visualize the results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_hands + 1), dqn_win_history, label='DQN Agent Wins')
    plt.plot(range(1, num_hands + 1), fixed_win_history, label='Fixed Model Wins')
    plt.plot(range(1, num_hands + 1), random_win_history, label='Random Model Wins')
    plt.plot(range(1, num_hands + 1), tie_history, label='Ties')
    plt.xlabel('Number of Hands')
    plt.ylabel('Cumulative Wins/Ties')
    plt.title('Cumulative Wins/Ties Over Hands')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    env = PokerEnv()
    state_size = NUM_CARDS + 4
    action_size = 3
    dqn_agent = DQNAgent(state_size, action_size)
    dqn_agent.load("trained_model.h5")

    random_agent = RandomAgent(action_size)

    num_hands = 1000
    simulate_game(env, dqn_agent, fixed_calculate_action, random_calculate_action, num_hands)