from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from modules.file_manager import FileManager
from widgets.components import make_button, make_label
from widgets.sidebar import Sidebar


class FilesScreen(Screen):
    def __init__(self, navigate_callback, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = FileManager()

        root = BoxLayout(orientation="horizontal", padding=12, spacing=12)
        root.add_widget(Sidebar(navigate_callback))

        content = BoxLayout(orientation="vertical", padding=18, spacing=8)
        content.add_widget(make_label("Virtual File Manager", 27, size_hint_y=None, height=44))

        self.filename = TextInput(
            hint_text="Filename (example: notes.txt)", multiline=False,
            size_hint_y=None, height=40
        )
        self.new_filename = TextInput(
            hint_text="New filename for copy / rename", multiline=False,
            size_hint_y=None, height=40
        )
        self.file_content = TextInput(
            hint_text="File content", multiline=True,
            size_hint_y=None, height=100
        )
        content.add_widget(self.filename)
        content.add_widget(self.new_filename)
        content.add_widget(self.file_content)

        actions = [
            ("Create", self.create_file),
            ("Read", self.read_file),
            ("Delete", self.delete_file),
            ("Rename", self.rename_file),
            ("Copy", self.copy_file),
            ("Refresh list", self.refresh_files),
        ]
        for label, callback in actions:
            content.add_widget(make_button(label, callback, height=38))

        self.output = make_label("Files in virtual_files will appear here.", 13)
        content.add_widget(self.output)

        root.add_widget(content)
        self.add_widget(root)
        self.refresh_files(None)

    def create_file(self, instance):
        ok = self.file_manager.create_file(self.filename.text, self.file_content.text)
        self.output.text = "File created." if ok else "Could not create file. Check the name or whether it already exists."
        self.refresh_files(None)

    def read_file(self, instance):
        value = self.file_manager.read_file(self.filename.text)
        self.output.text = "File not found or could not be read." if value is None else f"Content:\n{value}"

    def delete_file(self, instance):
        ok = self.file_manager.delete_file(self.filename.text)
        self.output.text = "File deleted." if ok else "File not found."
        self.refresh_files(None)

    def rename_file(self, instance):
        ok = self.file_manager.rename_file(self.filename.text, self.new_filename.text)
        self.output.text = "File renamed." if ok else "Rename failed. Check both names."
        self.refresh_files(None)

    def copy_file(self, instance):
        ok = self.file_manager.copy_file(self.filename.text, self.new_filename.text)
        self.output.text = "File copied." if ok else "Copy failed. Check both names."
        self.refresh_files(None)

    def refresh_files(self, instance):
        names = self.file_manager.list_files()
        listing = "\n".join(names) if names else "(no files yet)"
        self.output.text = f"Virtual files:\n{listing}"
