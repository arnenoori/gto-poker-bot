tools = [
    {
        "type": "function",
        "function": {
            "name": "wait",
            "description": "Wait for a few seconds if it is not your turn.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ok",
            "description": "Click OK to finalize the Raise action after choosing to Raise and setting the betting amount on the scale.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "continue",
            "description": "Choose to continue to the next game after someone wins the hand.",
            "parameters": {},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "makeMove",
            "description": "Calculate the optimal move (fold, check, call, or raise) based on the community cards and the cards in hand.",
            "parameters": {
                "type": "object",
                "properties": {
                    "communityCards": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A card in the format of 'rank-suit', e.g., '10-H' for 10 of Hearts",
                        },
                        "description": "The community cards on the table.",
                    },
                    "holeCards": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A card in the format of 'rank-suit', e.g., 'A-S' for Ace of Spades",
                        },
                        "description": "The cards in the player's hand.",
                    },
                },
                "required": ["communityCards", "holeCards"],
            },
        },
    },
]