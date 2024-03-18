import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# Constants
NUM_CARDS = 52
NUM_ACTIONS = 3
NUM_EPISODES = 1000
BATCH_SIZE = 32
MAX_STEPS_PER_EPISODE = 10

# Define the poker environment
class PokerEnv:
    def __init__(self):
        self.action_space = [0, 1, 2]  # 0: Fold, 1: Call, 2: Raise
        self.observation_space = NUM_CARDS
        self.state = None
        self.done = False
        self.step_count = 0
        self.player_hand = []  # Initialize player_hand as an empty list
        self.community_cards = []  # Initialize community_cards as an empty list

    def reset(self):
        self.deck = list(range(NUM_CARDS))
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.community_cards = []
        self.state = self.player_hand + self.community_cards
        self.done = False
        self.step_count = 0
        return self.state
    
    def state_size(self):
        return len(self.player_hand) + len(self.community_cards)
    
    def step(self, action):
        self.step_count += 1

        if action == 0:  # Fold
            reward = -1
            self.done = True
        elif action == 1:  # Call
            self.done = True
            player_score = self.calculate_hand_score(self.player_hand + self.community_cards)
            reward = player_score
        else:  # Raise
            reward = 0
            self.done = False

        if not self.done:
            if len(self.community_cards) < 5:
                num_cards_to_deal = random.randint(1, min(3, 5 - len(self.community_cards)))
                self.community_cards.extend([self.deck.pop() for _ in range(num_cards_to_deal)])
                self.state = self.player_hand + self.community_cards
            else:
                self.done = True
                player_score = self.calculate_hand_score(self.player_hand + self.community_cards)
                reward = player_score

        if self.step_count >= MAX_STEPS_PER_EPISODE:
            self.done = True

        return self.state, reward, self.done, {}

    def calculate_hand_score(self, cards):
        ranks = [card % 13 for card in cards]
        suits = [card // 13 for card in cards]
        rank_count = {}
        for rank in ranks:
            if rank not in rank_count:
                rank_count[rank] = 0
            rank_count[rank] += 1

        # Check for flush
        flush = len(set(suits)) == 1

        # Check for straight
        unique_ranks = sorted(set(ranks))
        straight = len(unique_ranks) == 5 and unique_ranks[-1] - unique_ranks[0] == 4 or set(unique_ranks) == {0, 1, 2, 3, 12}

        # Check for hand types
        hand_types = {
            (4, 1): 7,  # Four of a kind
            (3, 2): 6,  # Full house
            (3, 1, 1): 3,  # Three of a kind
            (2, 2, 1): 2,  # Two pairs
            (2, 1, 1, 1): 1,  # Pair
            (1, 1, 1, 1, 1): 0  # High card
        }
        rank_count_tuple = tuple(sorted(rank_count.values(), reverse=True))
        score = hand_types.get(rank_count_tuple, 0)

        if flush and straight:
            score = 8  # Straight flush
            if set(ranks) == {8, 9, 10, 11, 12}:  # Special case: Royal flush
                score = 9
        elif flush:
            score = 5  # Flush
        elif straight:
            score = 4  # Straight

        return score
    
# Define the Deep Q-Network
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(64, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = np.reshape(state, [1, self.state_size])
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        states, targets_f = [], []
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = np.array(next_state)  # Convert next_state to a NumPy array
                next_state = np.reshape(next_state, (1, -1))  # Reshape next_state to (1, state_size)
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            state = np.reshape(state, [1, -1])  # Reshape state to (1, state_size)
            target_f = self.model.predict(state)
            target_f[0][action] = target
            states.append(state[0])
            targets_f.append(target_f[0])
        states = np.array(states)  # Convert states to a NumPy array
        targets_f = np.array(targets_f)  # Convert targets_f to a NumPy array
        self.model.fit(states, targets_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def play(self, state):
        state = np.reshape(state, [1, len(state)])
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

def play_game(env, agent):
    state = env.reset()
    done = False
    while not done:
        print(f"\nPlayer's Hand: {env.player_hand}")
        print(f"Community Cards: {env.community_cards}")
        state = np.reshape(state, [1, env.state_size()])
        action = agent.play(state)
        if action == 0:
            print("Agent action: Fold")
        elif action == 1:
            print("Agent action: Call")
        else:
            print("Agent action: Raise")
        next_state, reward, done, _ = env.step(action)
        state = next_state
        if done:
            print(f"Hand Score: {reward}")


# Train the Deep Q-Network
if __name__ == "__main__":
    env = PokerEnv()
    state_size = env.state_size()
    action_size = len(env.action_space)
    agent = DQNAgent(state_size, action_size)

    for e in range(NUM_EPISODES):
        state = env.reset()
        done = False
        score = 0
        while not done:
            if state_size > 0:
                state = np.reshape(np.array(state), [1, state_size])
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            score += reward
            if state_size > 0:
                next_state = np.reshape(np.array(next_state), [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"Episode: {e + 1}/{NUM_EPISODES}, Score: {score}")
                break
        if len(agent.memory) > BATCH_SIZE:
            agent.replay(BATCH_SIZE)

    # Play against the trained agent
    while True:
        play_game(env, agent)
        play_again = input("Play again? (y/n): ")
        if play_again.lower() != 'y':
            break