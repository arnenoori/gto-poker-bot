import random
from typing import List
from dqn_agent import PokerEnv, DQNAgent
from gamer.fixed import calculate_action
import matplotlib.pyplot as plt

# Constants
NUM_CARDS = 52
STARTING_STACK = 1000
SMALL_BLIND = 10
BIG_BLIND = 20

def simulate_hand(env: PokerEnv, dqn_agent: DQNAgent, fixed_model, hand_num: int):
    state = env.reset()
    done = False
    actions = []
    print(f"\nHand {hand_num + 1}:")
    while not done:
        if env.current_player == 0:  # DQN agent's turn
            action = dqn_agent.act(state, eval_mode=True)
            print(f"DQN Agent action: {env.action_space[action]}")
        else:  # Fixed model's turn
            action = fixed_model(env.community_cards, env.player_hand, env.pot, env.current_bet)
            action = env.action_space.index(action)
            print(f"Fixed Model action: {env.action_space[action]}")
        actions.append(action)
        next_state, reward, done, _ = env.step(action)
        state = next_state
    print(f"Hand {hand_num + 1} result: {'DQN Agent wins' if reward > 0 else 'Fixed Model wins' if reward < 0 else 'Tie'}")
    return reward, actions

def simulate_game(env: PokerEnv, dqn_agent: DQNAgent, fixed_model, num_hands: int):
    dqn_wins = 0
    fixed_wins = 0
    ties = 0
    dqn_win_history = []
    fixed_win_history = []
    tie_history = []
    for hand_num in range(num_hands):
        reward, _ = simulate_hand(env, dqn_agent, fixed_model, hand_num)
        if reward > 0:
            dqn_wins += 1
        elif reward < 0:
            fixed_wins += 1
        else:
            ties += 1
        dqn_win_history.append(dqn_wins)
        fixed_win_history.append(fixed_wins)
        tie_history.append(ties)
    print(f"\nResults after {num_hands} hands:")
    print(f"DQN Agent Wins: {dqn_wins}")
    print(f"Fixed Model Wins: {fixed_wins}")
    print(f"Ties: {ties}")
    
    # Visualize the results
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_hands + 1), dqn_win_history, label='DQN Agent Wins')
    plt.plot(range(1, num_hands + 1), fixed_win_history, label='Fixed Model Wins')
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
    
    num_hands = 1000
    simulate_game(env, dqn_agent, calculate_action, num_hands)