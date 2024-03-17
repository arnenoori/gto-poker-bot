import json
from gamer.tools import tools

def get_system_prompt():
    """
    This is a system prompt for the game
    """
    return POKER_SYSTEM_PROMPT


POKER_SYSTEM_PROMPT = f"""
Your job is to look at an image of a poker table and output the current board state.

{json.dumps(tools)}""" + """

Output using the following format:

```
boardState: stringified JSON object representing the parameters used for the action, e.g.,
 "{
    "isGameOver": false,
    "communityCards": ["A-S", "2-H", "3-C"], 
    "holeCards": ["5-D", "6-S"], 
    "currentPotValue": 64,
    "whoRaised": [
        {
            "name": "John",
            "raise": 20,
        }
    ]
}"
```

Here is the domain for the card values: 
{'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'}

Here is the domain for the card suits: 
{'H', 'D', 'C', 'S'}


Provide output in JSON format as follows:

```
{ "boardState": "..." }
```

Remember, the communityCards are the cards on the table, the holeCards are the cards in your hand. There will ALWAYS be 2 holeCards.
"""