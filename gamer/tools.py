tools = [
    {
        "type": "function",
        "function": {
            "name": "outputBoardState",
            "description": "Output the current board state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "isGameOver": {
                        "type": "boolean",
                        "description": "Whether the game is over.",
                    },
                    "communityCards": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A card in the format of 'rank-suit', e.g., '10-H' for 10 of Hearts",
                        },
                        "description": "The community cards on the table visible to the public. Empty array if there are none.",
                    },
                    "holeCards": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A card in the format of 'rank-suit', e.g., 'A-S' for Ace of Spades",
                        },
                        "description": "The cards in the player's hand, private from the other players.",
                    },
                    "currentPotValue": {
                        "type": "number",
                        "description": "The current pot value.",
                    },
                    "whoRaised": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the player who raised.",
                                },
                                "raise": {
                                    "type": "number",
                                    "description": "The amount the player raised.",
                                },
                            },
                        },
                        "description": "The players who raised and the amount they raised.",
                    },
                },
                "required": ["isGameOver", "communityCards", "holeCards", "currentPotValue", "whoRaised"],
            },
        },
    },
]