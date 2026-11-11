class InputOutput:
    """Records simulated input and output events."""

    def __init__(self):
        self.input_history = []
        self.output_history = []

    def receive_input(self, value):
        self.input_history.append(value)
        return value

    def send_output(self, value):
        self.output_history.append(value)
        return value

    def get_input_history(self):
        return self.input_history.copy()

    def get_output_history(self):
        return self.output_history.copy()

    def clear(self):
        self.input_history.clear()
        self.output_history.clear()
