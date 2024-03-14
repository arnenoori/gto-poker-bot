# Advanced Poker Bot Using Reinforcement Learning

## Machine Learing Areas:

## Tech Scope:

## Local Setup:

## Project Description

This project aims to develop an intelligent poker bot capable of playing no-limit Texas Hold'em at a high level. The bot uses reinforcement learning, specifically Q-learning, and machine learning techniques like Naive Bayes and clustering for hand strength prediction and opponent modeling.

The bot processes a comprehensive set of game state data, including its own hand, community cards, betting history, opponent actions, and the stage of the game. It outputs strategic decisions such as betting, calling, folding, or raising.

## Data

The training data for this project is generated programmatically using initial simple AI models to simulate poker games. We also use existing datasets from poker competitions and repositories. The data undergoes preprocessing for cleaning, handling missing values, and converting it into a format suitable for machine learning algorithms.

## Platform

The bot is developed using TensorFlow and Keras for building and training the neural network models, and Python for its extensive support for machine learning libraries and ease of integration with TensorFlow and Keras. The development and testing of the bot are done on local machines initially, with potential migration to a cloud environment for enhanced computing power during intensive training phases.

## Implementation Plan

The project follows a comprehensive implementation plan, starting from data collection and preprocessing, feature engineering, hand strength prediction, opponent modeling, reinforcement learning, training and evaluation, iteration and improvement, to integration and testing.

## Testing Plan

The bot is tested in various poker scenarios, including different hand combinations, opponent behaviors, and different stages of a game. Performance metrics include win rate, decision accuracy, and adaptability. User testing and automated testing are also part of the testing plan.

## Future Expansion

Future expansions of the project include expanding game varieties, improved opponent modeling, user learning module, community integration, expanding to multi-player scenarios, user feedback system, advanced GTO strategies, and personalized learning.

## Authors

- Arne Noori
- Ido Pesok
- Wes Convery


## Quick install

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
