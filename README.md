# Advanced Poker Bot Using Reinforcement Learning

Getting started:
------

- brew install poetry
- poetry env use python3.11

Run:

- Install Python 3.11, I would also recommend to install PyCharm.
- Install Poetry with ``curl -sSL https://install.python-poetry.org | python3 -``
- Create a virtual environment with ``poetry env use python3.11``
- Activate it with ``poetry shell``
- Install all required packages with ``poetry install --no-root``
- Run 6 random players playing against each other:
  ``poetry run python main.py selfplay random`` or
- To manually control the players:``poetry run python main.py selfplay keypress``
- Example of genetic algorithm with self improvement: ``poetry run python main.py selfplay equity_improvement --improvement_rounds=20 --episodes=10``
- In order to use the C++ version of the equity calculator, you will also need to install Visual Studio 2019 (or GCC over Cygwin may work as well). To use it, use the -c option when running main.py.
- For more advanced users: ``poetry run python main.py selfplay dqn_train -c`` will start training the deep Q agent with C++ Monte Carlo for faster calculation

### agents
---
Please add your model based agents here.

-  ``agent_random.py``: an agent making random decisions
-  ``agent_keypress.py``: an agent taking decision via keypress
-  ``agent_consider_equity.py``: an agent considering equity information
-  ``agent_keras_rl_dqn.py``: Deep Q learning agent, using keras-rl for deep reinforcement learning
-  ``agent_custom_q1.py``: Custom implementation of deep q learning

Note that the observation property is a dictionary that contains all the information about the players and table that can be used to make a decision.

### neuronpoker toolkit

-  ``hand_evaluator.py``: evaluate the best hand of multiple players
-  ``helper.py``: helper functions
-  ``montecarlo_numpy2.py``: fast numpy based montecarlo simulation to
   calculate equity. Not yet working correctly. Some tests are failing. Feel free to fix them.
-  ``montecarlo_python.py``: relatively slow python based montecarlo for equity calculation. Supports
   preflight ranges for other players.
-  ``montecarlo_cpp``: c++ implementation of equity calculator. Around 500x faster than python version

### testing

-  ``test_gym_env.py``: tests for the end.
-  ``test_montecarlo.py``: tests for the hands evaluator and python
   based equity calculator.
-  ``test_montecarlo_numpy.py``: tests for the numpy montecarlo
-  ``test_pylint.py``: pylint and pydoc tests to ensure pep8 standards and static code analysis


## Replicating Results

Reinforcement learning: Deep Q agent
------------------

``neuron_poker.agents.agent_dqn`` implements a deep q agent with help of keras-rl.
A number of parameters can be se:

- nb_max_start_steps = 20  # maximum of random actions at the beginning
- nb_steps_warmup = 75  # before training starts, should be higher than start steps
- nb_steps = 10000  # total number of steps
- memory_limit = int(nb_steps / 3)  # limiting the memory of experience replay
- batch_size = 500  # number of items sampled from memory to train

Training can be observed via tensorboard (run ``tensorboard --logdir=./Graph`` from command line)
|image2|

In ``main.py`` an agent is launched as follows (here adding 6 random
agents to the table). To edit what is accepted to main.py via command
line, simply add another line in the docstring at the top of main.py.

.. code:: python

    def random_action(render):
        """Create an environment with 6 random players"""
        env_name = 'neuron_poker-v0'
        stack = 500
        self.env = gym.make(env_name, num_of_players=6, initial_stacks=stack)
        for _ in range(num_of_plrs):
            player = RandomPlayer(500)
            self.env.add_player(player)

        self.env.reset()

As you can see, as a first step, the environment needs to be created. As a second step, different agents need to be
added to the table. As a third step the game is kicked off with a reset. Agents with autoplay set to True will automatically
play, by having the action method called of their class. Alternatively you can use the PlayerShell class
and the environment will require you call call the step function manually and loop over it. This may be helpful
when using other packages which are designed to interface with the gym, such as keras-rl.

Adding a new model / agent
^^^^^^^^^^^^^^^^^^^^^^^^^^

An example agent can be seen in random\_agent.py

To build a new agent, an agent needs to be created, where the follwing
function is modified. You will need to use the observation parameter,
which contains the current state of the table, the players and and the
agent itself, as a parameter to determine the best action.

.. code:: python

    def action(self, action_space, observation):  # pylint: disable=no-self-use
        """Mandatory method that calculates the move based on the observation array and the action space."""
        _ = observation  # not using the observation for random decision
        this_player_action_space = {Action.FOLD, Action.CHECK, Action.CALL, Action.RAISE_POT, Action.RAISE_HAlF_POT}
        possible_moves = this_player_action_space.intersection(set(action_space))
        action = random.choice(list(possible_moves))
        return action

Observing the state
---------~

The state is represented as a numpy array that contains the following
information:

.. code:: python

    class CommunityData:
        def __init__(self, num_players):
            self.current_player_position = [False] * num_players  # ix[0] = dealer
            self.stage = [False] * 4  # one hot: preflop, flop, turn, river
            self.community_pot: float: the full pot of this hand
            self.current_round_pot: float: the pot of funds added in this round
            self.active_players = [False] * num_players  # one hot encoded, 0 = dealer
            self.big_blind
            self.small_blind


    class StageData:  # as a list, 8 times:
        """Preflop, flop, turn and river, 2 rounds each"""

        def __init__(self, num_players):
            self.calls = [False] * num_players  # ix[0] = dealer
            self.raises = [False] * num_players  # ix[0] = dealer
            self.min_call_at_action = [0] * num_players  # ix[0] = dealer
            self.contribution = [0] * num_players  # ix[0] = dealer
            self.stack_at_action = [0] * num_players  # ix[0] = dealer
            self.community_pot_at_action = [0] * num_players  # ix[0] = dealer


    class PlayerData:
        "Player specific information"

        def __init__(self):
            self.position: one hot encoded, 0=dealer
            self.equity_to_river: montecarlo
            self.equity_to_river_2plr: montecarlo
            self.equity_to_river_3plr: montecarlo
            self.stack: current player stack

### Getting started with running an online match via self-operating commuter:

Create venv
```
python3 -m venv env
```
Activate it (Mac)
```
source env/bin/activate
```
Install requirements
```
pip install -r requirements.txt
```
Add OpenAI Key
```
export OPENAI_API_KEY=yourkeyhere
```
Run it
```
python play.py
```

### Access the hand classifier model that from the UCI dataset:

This model takes in a input of 10 integers, and out puts the highest hand.

Train off of the following [Dataset](https://www.kaggle.com/rasvob/uci-poker-hand-dataset?select=poker-hand-testing.data).


The input is the following with Ranks being values 0-13 and Suits being 0-4. The value 0 represents a missing card.

(1-4) representing {Hearts, Spades, Diamonds, Clubs} 
(1-13) representing (Ace, 2, 3, … , Queen, King) 


| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
| - | - | - | - | - | - | - | - | - | - | --
| Suit Card 1 | Rank Card 1 | Suit Card 2 | Rank Card 2 | Suit Card 3 | Rank Card 3 | Suit Card 4 | Rank Card 4 | Suit Card 5 | Rank Card 5 


