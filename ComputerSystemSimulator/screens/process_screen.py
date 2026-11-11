from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from modules.process_manager import ProcessManager
from widgets.components import make_button, make_label
from widgets.sidebar import Sidebar


class ProcessScreen(Screen):
    def __init__(self, navigate_callback, **kwargs):
        super().__init__(**kwargs)
        self.process_manager = ProcessManager()

        root = BoxLayout(orientation="horizontal", padding=12, spacing=12)
        root.add_widget(Sidebar(navigate_callback))

        content = BoxLayout(orientation="vertical", padding=18, spacing=8)
        content.add_widget(make_label("Process Manager", 27, size_hint_y=None, height=44))

        self.process_name = TextInput(
            hint_text="Process name", multiline=False,
            size_hint_y=None, height=40
        )
        self.priority_input = TextInput(
            hint_text="Priority (1-10, default 1)", text="1",
            multiline=False, input_filter="int",
            size_hint_y=None, height=40
        )
        self.pid_input = TextInput(
            hint_text="PID for run / stop / delete", multiline=False,
            input_filter="int", size_hint_y=None, height=40
        )
        content.add_widget(self.process_name)
        content.add_widget(self.priority_input)
        content.add_widget(self.pid_input)

        actions = [
            ("Create process", self.create_process),
            ("Run process", self.run_process),
            ("Stop process", self.stop_process),
            ("Delete process", self.delete_process),
            ("Refresh list", self.refresh),
        ]
        for label, callback in actions:
            content.add_widget(make_button(label, callback, height=38))

        self.output = make_label("", 13)
        content.add_widget(self.output)
        root.add_widget(content)
        self.add_widget(root)
        self.refresh(None)

    def get_pid(self):
        try:
            return int(self.pid_input.text)
        except ValueError:
            return None

    def create_process(self, instance):
        process = self.process_manager.create_process(
            self.process_name.text, self.priority_input.text
        )
        self.output.text = (
            f"Created process with PID {process['pid']}."
            if process else "Could not create process. Enter a name and priority from 1 to 10."
        )
        self.refresh(None)

    def run_process(self, instance):
        pid = self.get_pid()
        ok = self.process_manager.run_process(pid) if pid is not None else False
        self.output.text = "Process is now Running." if ok else "Run failed. Check PID and status (must be Ready)."
        self.refresh(None)

    def stop_process(self, instance):
        pid = self.get_pid()
        ok = self.process_manager.stop_process(pid) if pid is not None else False
        self.output.text = "Process marked Terminated." if ok else "Stop failed. Check PID and status (must be Running)."
        self.refresh(None)

    def delete_process(self, instance):
        pid = self.get_pid()
        ok = self.process_manager.delete_process(pid) if pid is not None else False
        self.output.text = "Process deleted." if ok else "Delete failed. Check PID."
        self.refresh(None)

    def refresh(self, instance):
        processes = self.process_manager.get_processes()
        if not processes:
            listing = "(no processes yet)"
        else:
            listing = "\n".join(
                f"PID {p['pid']} | {p['name']} | {p['status']} | Priority {p['priority']}"
                for p in processes
            )
        self.output.text = f"Process list:\n{listing}"
