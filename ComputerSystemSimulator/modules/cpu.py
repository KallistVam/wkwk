class CPU:
    """Small educational CPU model with an accumulator and instruction counter."""

    def __init__(self):
        self.reset()

    def execute(self, operation, a, b):
        operation = operation.upper()
        self.status = "Running"
        self.registers["IR"] = f"{operation} {a}, {b}"

        try:
            if operation == "ADD":
                result = a + b
            elif operation == "SUB":
                result = a - b
            elif operation == "MUL":
                result = a * b
            elif operation == "DIV":
                if b == 0:
                    self.status = "Error"
                    return "Error: division by zero"
                result = a / b
            else:
                self.status = "Error"
                return "Error: invalid instruction"

            self.registers["ACC"] = result
            self.registers["PC"] += 1
            self.history.append({
                "instruction": operation,
                "operand_a": a,
                "operand_b": b,
                "result": result,
            })
            self.status = "Idle"
            return result
        except (TypeError, ArithmeticError) as exc:
            self.status = "Error"
            return f"Error: {exc}"

    def get_status(self):
        return {
            "status": self.status,
            "registers": self.registers.copy(),
            "history": self.history.copy(),
        }

    def reset(self):
        self.registers = {"ACC": 0, "PC": 0, "IR": None}
        self.status = "Idle"
        self.history = []
