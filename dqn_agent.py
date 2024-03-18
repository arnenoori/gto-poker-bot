import numpy as np
import random
from collections import Counter, deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam

# Constants
NUM_CARDS = 52
MAX_STEPS_PER_EPISODE = 4  # Preflop, flop, turn, river
STARTING_STACK = 1000
SMALL_BLIND = 10
BIG_BLIND = 20

suits = ['♠', '♥', '♦', '♣']
rank_str = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class PokerEnv:
    def __init__(self):
        self.action_space = [0, 1, 2]  # 0: Fold, 1: Call, 2: Raise
        self.reset()

    def reset(self):
        self.deck = list(range(NUM_CARDS))
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.opponent_hand = [self.deck.pop(), self.deck.pop()]
        self.community_cards = []
        self.state = [0] * (NUM_CARDS + 4)  # Including pot, player_stack, opponent_stack, current_bet
        self.pot = 0
        self.player_stack = STARTING_STACK
        self.opponent_stack = STARTING_STACK
        self.current_bet = 0
        self.done = False
        self.betting_round = 0  # 0: Preflop, 1: Flop, 2: Turn, 3: River
        self.last_action = None  # Track the last action to manage betting rounds
        self.post_blinds()
        self.update_state(None)  # Pass None as the initial action
        return self.state

    def post_blinds(self):
        # Automatically post small and big blinds
        self.player_stack -= SMALL_BLIND
        self.opponent_stack -= BIG_BLIND
        self.pot += SMALL_BLIND + BIG_BLIND
        self.current_bet = BIG_BLIND

    def print_cards(self, cards):
        """Convert card indices to readable strings and print."""
        card_strs = [f"{rank_str[card % 13]}{suits[card // 13]}" for card in cards]
        print(" ".join(card_strs))

    def update_state(self, action):
        round_names = ['Preflop', 'Flop', 'Turn', 'River']
        print(f"\n--- {round_names[self.betting_round]} ---")
        print("Player's hand: ", end='')
        self.print_cards(self.player_hand)
        print("Community cards: ", end='')
        self.print_cards(self.community_cards)
        if action is not None:
            actions = ['Fold', 'Call', 'Raise']
            print(f"Action taken: {actions[action]}")

    def step(self, action):
        reward = 0
        if action == 0:  # Fold
            reward = -self.current_bet
            self.done = True
            print("Player folds.")
        else:
            self.handle_action(action)
            self.betting_round += 1
            if self.betting_round >= MAX_STEPS_PER_EPISODE or self.done:
                reward = self.calculate_final_reward()
                self.done = True
                print("End of hand.")
            else:
                self.deal_community_cards()
                print("Dealing community cards...")
        
        # Ensure betting_round doesn't exceed the maximum number of betting rounds
        self.betting_round = min(self.betting_round, MAX_STEPS_PER_EPISODE - 1)
        
        self.update_state(action)
        return self.state, reward, self.done, {}

    def handle_action(self, action):
        if action == 1:  # Call
            self.match_current_bet()
        elif action == 2:  # Raise
            self.raise_bet()

    def match_current_bet(self):
        bet_amount = self.current_bet - (self.pot // 2)  # Assuming player always acts second for simplicity
        self.player_stack -= bet_amount
        self.pot += bet_amount

    def opponent_decision(self):
        # Simple heuristic: opponent decides based on a combination of randomness and hand strength
        opponent_strength = self.estimate_hand_strength(self.opponent_hand + self.community_cards)
        decision = np.random.choice(['fold', 'call', 'raise'], p=[0.2, 0.5, 0.3])  # Placeholder probabilities
        if opponent_strength < 2:  # Assuming weak hand
            decision = 'fold' if np.random.random() < 0.5 else 'call'
        elif opponent_strength >= 6:  # Assuming strong hand
            decision = 'raise'
        return decision

    def execute_opponent_action(self, decision):
        if decision == 'fold':
            # End the round, player wins the pot
            self.done = True
        elif decision == 'call':
            self.opponent_stack -= self.current_bet
            self.pot += self.current_bet
        elif decision == 'raise':
            # For simplicity, let's set a fixed raise amount
            raise_amount = BIG_BLIND
            self.current_bet += raise_amount
            self.opponent_stack -= self.current_bet
            self.pot += self.current_bet


    def raise_bet(self):
        raise_amount = self.player_stack // 10
        self.current_bet += raise_amount
        self.player_stack -= raise_amount
        self.pot += raise_amount

    def deal_community_cards(self):
        if self.betting_round == 1:  # Flop
            self.community_cards.extend([self.deck.pop() for _ in range(3)])
        elif self.betting_round in [2, 3]:  # Turn, River
            self.community_cards.append(self.deck.pop())

    def calculate_final_reward(self):
        # Determine the winner and calculate reward based on the pot size
        player_score = self.calculate_hand_score(self.player_hand + self.community_cards)
        opponent_score = self.calculate_hand_score(self.opponent_hand + self.community_cards)
        if player_score > opponent_score:
            return self.pot
        elif player_score < opponent_score:
            return -self.pot
        else:
            return 0  # Draw case
    
    def calculate_hand_score(self, cards):
            ranks = [card % 13 for card in cards]
            suits = [card // 13 for card in cards]
            rank_counts = Counter(ranks)
            suit_counts = Counter(suits)

            # Hand ranking scores, higher is better
            score = 0
            is_flush = max(suit_counts.values()) >= 5
            is_straight = self.is_straight(ranks)

            if is_flush and is_straight:
                score = 8  # Straight flush
            elif 4 in rank_counts.values():
                score = 7  # Four of a kind
            elif sorted(rank_counts.values()) == [2, 3]:
                score = 6  # Full house
            elif is_flush:
                score = 5  # Flush
            elif is_straight:
                score = 4  # Straight
            elif 3 in rank_counts.values():
                score = 3  # Three of a kind
            elif len([x for x in rank_counts.values() if x == 2]) == 2:
                score = 2  # Two pair
            elif 2 in rank_counts.values():
                score = 1  # One pair

            return score

    def is_straight(self, ranks):
        """Check if the hand contains a straight."""
        unique_ranks = set(ranks)
        for i in range(max(ranks) - 4):
            if all(j in unique_ranks for j in range(i, i + 5)):
                return True
        # Special case for Ace-low straight
        if set([0, 1, 2, 3, 12]).issubset(unique_ranks):
            return True
        return False
    
# Define the Deep Q-Network
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)  # Use deque for efficient popping
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        """Builds a deep neural network model."""
        model = Sequential()
        model.add(Input(shape=(self.state_size,)))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        """Stores experiences in the replay memory."""
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """Returns actions for given state as per current policy."""
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(np.array([state]))
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        """Trains the model using randomly sampled experiences from the memory."""
        minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
        for state, action, reward, next_state, done in minibatch:
            target = reward if done else reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][action] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def play_game(env, agent):
    state = env.reset()  # Reset the environment for a new game
    done = False
    total_reward = 0
    
    while not done:
        action = agent.act(state)  # Agent chooses an action
        next_state, reward, done, _ = env.step(action)  # Environment responds
        agent.remember(state, action, reward, next_state, done)  # Remember the experience
        state = next_state
        total_reward += reward
        if done:
            print(f"Game Over. Total Reward: {total_reward}")
    
    return total_reward

def train_agent(env, agent, episodes=1000, batch_size=32, verbose=True):
    for e in range(episodes):
        total_reward = play_game(env, agent)
        if verbose:
            print(f"Episode: {e+1}/{episodes}, Total Reward: {total_reward}")
        
        if len(agent.memory) > batch_size:
            agent.replay(batch_size)

        # Decay epsilon
        agent.epsilon = max(agent.epsilon_min, agent.epsilon_decay * agent.epsilon)


if __name__ == "__main__":
    NUM_CARDS = 52  # Assuming this constant is defined
    env = PokerEnv()  # Assuming the environment is initialized correctly
    state_size = NUM_CARDS + 4  # Adjust according to your environment's state representation
    action_size = 3  # Possible actions: Fold, Call, Raise
    
    agent = DQNAgent(state_size, action_size)
    train_agent(env, agent, episodes=1000)