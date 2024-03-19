# Advanced Poker Bot Using Reinforcement Learning

![Poker](media/cowboy_bebop_poker.gif)

<!-- 
Acknowledges that this is a project in CSC 481 - Knowledge Based Systems at Cal Poly and includes the instructor's name
Gives credit to any external resources the project is based on (libraries, competition frameworks, etc.)
Has clear instructions for how to install any dependencies and how to run the main use cases with various parameters.
For example, if you implemented various agents that play tic-tac-toe on a board of any size versus either a human or another agent , your readme should inform the reader how to play as a human versus any of the agents, on a board of any size.
Either has instructions for how to reproduce the main results in your report, or has links to any tables, graphics and summarizations of the result.
For example, if you validated a heuristic agent and a tree search agent by having them play 10k matches against each other, your readme should also inform the reader how to run that evaluation scenario. If you collected data about a high number of agents, it should also include a table that summarizes the result of each match-up.

-->

## Getting started (replicating results):
------
Clone the repository
```
git clone https://github.com/arnenoori/gto-poker-bot
```

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

Go on your poker website of choice. We used www.247freepoker.com and played against bots.

To run the agent with the fixed strategy agent (default), simply run:
```
python play.py
```

or you can also run with
```
python play.py --fixed
```

To run the agent with the DQN agent first train the agent by running:
```
python dqn_agent.py
```
Then run:
```
python play.py --dqn
```

Or if you want to run the random agent:
```
python play.py --random
```

### agents
---
Please add your model based agents here.

-  ``agent_random.py``: an agent making random decisions (used for testing and comparison)
-  ``agent_dqn.py``: a deep q agent
-  ``fixed.py``: a fixed model

## Repository Structure
---

* [gamer/](./group-project/gamer)
  * [adapter.py](./group-project/gamer/adapter.py)
  * [api.py](./group-project/gamer/api.py)
  * [config.py](./group-project/gamer/config.py)
  * [fixed.py](./group-project/gamer/fixed.py)
  * [operating_system.py](./group-project/gamer/operating_system.py)
  * [prompts.py](./group-project/gamer/prompts.py)
  * [tools.py](./group-project/gamer/tools.py)
  * [utils.py](./group-project/gamer/utils.py)
* [media/](./group-project/media)
  * [cowboy_bebop_poker.gif](./group-project/media/cowboy_bebop_poker.gif)
* [report/](./group-project/report)
  * [proposal/](./group-project/report/proposal)
    * [CSC481_Project_Proposal.pdf](./group-project/report/proposal/CSC481_Project_Proposal.pdf)
    * [projectproposal.md](./group-project/report/proposal/projectproposal.md)
  * [481_report.md](./group-project/report/481_report.md)
  * [487_report.md](./group-project/report/487_report.md)
  * [final_presentation.pdf](./group-project/report/final_presentation.pdf)
* [.env](./group-project/.env)
* [.gitignore](./group-project/.gitignore)
* [README.md](./group-project/README.md)
* [dqn_agent.py](./group-project/dqn_agent.py)
* [evaluate.py](./group-project/evaluate.py)
* [play.py](./group-project/play.py)
* [random_agent.py](./group-project/random_agent.py)
* [requirements.txt](./group-project/requirements.txt)

How it works:

Image of the bot 

## Results

Results after 1000 hands:
DQN Agent Wins: 51
Fixed Model Wins: 927
Random Model Wins: 6
Ties: 16