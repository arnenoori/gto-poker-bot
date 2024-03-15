import json
from gamer.tools import tools

def get_system_prompt(game):
    """
    This is a system prompt for the game
    """
    if game == "poker":
        prompt = POKER_SYSTEM_PROMPT
    return prompt


POKER_SYSTEM_PROMPT = f"""
You are an expert at Poker. Today you will be plaing and you goal is to play the best move at each step.

For context, you will be selecting the buttons at the bottom of the screen to make your move. The buttons have a dark background and white text.

Here are your available actions: Wait, OK, Continue, MakeMove.

{json.dumps(tools)}""" + """

When calling actions, use the following format:

```
name: string representing the name of the action, e.g., Wait, OK, Continue, MakeMove
arguments: stringified JSON object representing the parameters used for the action, e.g., "{"communityCards": ["A-S", "2-H", "3-C"], "holeCards": ["5-D", "6-S"]}"
```

Provide output in JSON format as follows:

```
{"thought":"...", "action": { "name": "string", "arguments": "..." }, "reason":"..."}
```

It is important you think about your next action and come up with a good reason to take the action. Ensure that you share your thoughts and reasons for your actions as well output. 

Cheers!
"""