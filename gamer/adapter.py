class Adapter:
    def __init__(self):
        self.verbose = False

    def poker(self, operation):
        x = operation.get("x")
        y = operation.get("y")

        operation = {
            "operation": "click",
            "x": x,
            "y": y,
        }

        return [operation]