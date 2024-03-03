# Hand Classifcation Model

This model takes in a input of 10 integers, and out puts the highest hand.

Train off of the following [Dataset](https://www.kaggle.com/rasvob/uci-poker-hand-dataset?select=poker-hand-testing.data).


The input is the following with Ranks being values 0-13 and Suits being 0-4. The value 0 represents a missing card.

(1-4) representing {Hearts, Spades, Diamonds, Clubs} 
(1-13) representing (Ace, 2, 3, … , Queen, King) 


| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
| - | - | - | - | - | - | - | - | - | - | --
| Suit Card 1 | Rank Card 1 | Suit Card 2 | Rank Card 2 | Suit Card 3 | Rank Card 3 | Suit Card 4 | Rank Card 4 | Suit Card 5 | Rank Card 5 