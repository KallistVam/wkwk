from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from modules.cpu import CPU
from modules.memory import Memory
from modules.input_output import InputOutput
from widgets.components import make_button, make_label
from widgets.sidebar import Sidebar


class SystemScreen(Screen):
    def __init__(self, navigate_callback, **kwargs):
        super().__init__(**kwargs)
        self.cpu = CPU()
        self.memory = Memory(capacity=1024)
        self.io = InputOutput()

        root = BoxLayout(orientation="horizontal", padding=12, spacing=12)
        root.add_widget(Sidebar(navigate_callback))

        content = BoxLayout(orientation="vertical", padding=18, spacing=9)
        content.add_widget(make_label("System Simulation", 27, size_hint_y=None, height=44))

        self.input_a = TextInput(
            hint_text="First number", multiline=False,
            size_hint_y=None, height=42, input_filter="float"
        )
        self.input_b = TextInput(
            hint_text="Second number", multiline=False,
            size_hint_y=None, height=42, input_filter="float"
        )
        content.add_widget(self.input_a)
        content.add_widget(self.input_b)

        operations = BoxLayout(orientation="horizontal", size_hint_y=None, height=44, spacing=7)
        for operation in ("ADD", "SUB", "MUL", "DIV"):
            operations.add_widget(make_button(
                operation,
                lambda instance, op=operation: self.calculate(op),
                height=44
            ))
        content.add_widget(operations)

        self.result = make_label("Result: -", 17, size_hint_y=None, height=72)
        content.add_widget(self.result)

        self.memory_status = make_label("RAM usage: 0 / 1024 addresses", 15, size_hint_y=None, height=35)
        content.add_widget(self.memory_status)

        content.add_widget(make_button("Reset CPU and RAM", self.reset_cpu))
        content.add_widget(make_label(
            "Model: Fetch/execute is represented by the CPU instruction register and program counter.",
            13
        ))

        root.add_widget(content)
        self.add_widget(root)

    def calculate(self, operation):
        try:
            a = float(self.input_a.text)
            b = float(self.input_b.text)
        except ValueError:
            self.result.text = "Please enter valid numbers in both fields."
            return

        self.io.receive_input((a, b, operation))
        result = self.cpu.execute(operation, a, b)

        if isinstance(result, str) and result.startswith("Error"):
            self.result.text = result
            return

        self.memory.write(0, result)
        self.io.send_output(result)
        usage = self.memory.get_usage()
        self.result.text = (
            f"Result: {result}\nCPU status: {self.cpu.status}\n"
            f"Instruction counter (PC): {self.cpu.registers['PC']}\n"
            f"Accumulator (ACC): {self.cpu.registers['ACC']}"
        )
        self.memory_status.text = (
            f"RAM usage: {usage['used']} / {usage['total']} addresses"
        )

    def reset_cpu(self, instance):
        self.cpu.reset()
        self.memory.clear()
        self.io.clear()
        self.result.text = "CPU and simulated RAM have been reset."
        self.memory_status.text = "RAM usage: 0 / 1024 addresses"
