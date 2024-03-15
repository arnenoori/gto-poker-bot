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

# Define the poker environment
class PokerEnv:
    def __init__(self):
        self.action_space = [0, 1, 2]  # 0: Fold, 1: Call, 2: Raise
        self.observation_space = NUM_CARDS
        self.state = None
        self.done = False

    def reset(self):
        self.deck = list(range(NUM_CARDS))
        random.shuffle(self.deck)
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.state = self.player_hand
        self.done = False
        return self.state

    def step(self, action):
        if action == 0:  # Fold
            reward = -1
            self.done = True
        elif action == 1:  # Call
            player_score = self.calculate_hand_score(self.player_hand)
            dealer_score = self.calculate_hand_score(self.dealer_hand)
            if player_score > dealer_score:
                reward = 1
            elif player_score < dealer_score:
                reward = -1
            else:
                reward = 0
            self.done = True
        else:  # Raise
            player_score = self.calculate_hand_score(self.player_hand)
            dealer_score = self.calculate_hand_score(self.dealer_hand)
            if player_score > dealer_score:
                reward = 2
            else:
                reward = -2
            self.done = True

        return self.state, reward, self.done, {}

    def calculate_hand_score(self, hand):
        ranks = [card % 13 for card in hand]
        suits = [card // 13 for card in hand]
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
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        states, targets_f = [], []
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            states.append(state[0])
            targets_f.append(target_f[0])
        self.model.fit(np.array(states), np.array(targets_f), epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Train the Deep Q-Network
if __name__ == "__main__":
    env = PokerEnv()
    state_size = env.observation_space
    action_size = len(env.action_space)
    agent = DQNAgent(state_size, action_size)

    for e in range(NUM_EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(100):
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"Episode: {e}/{NUM_EPISODES}, Score: {time}")
                break
        if len(agent.memory) > BATCH_SIZE:
            agent.replay(BATCH_SIZE)
