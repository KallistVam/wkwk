from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from config import PRIMARY_COLOR, SECONDARY_COLOR


class Sidebar(BoxLayout):
    def __init__(self, navigate_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_x = None
        self.width = 220
        self.padding = 12
        self.spacing = 10
        self.navigate_callback = navigate_callback

        title = Label(
            text="[b]CS SIMULATOR[/b]",
            markup=True,
            font_size=19,
            size_hint_y=None,
            height=65
        )
        self.add_widget(title)

        self.add_menu("Dashboard", "dashboard")
        self.add_menu("System Simulation", "system")
        self.add_menu("File Manager", "files")
        self.add_menu("Process Manager", "process")

        self.add_widget(Widget())

        self.add_widget(Label(
            text="Computer System\nSimulator v1.0",
            font_size=11,
            size_hint_y=None,
            height=45
        ))

    def add_menu(self, title, screen_name):
        button = Button(
            text=title,
            size_hint_y=None,
            height=46,
            background_normal="",
            background_down="",
            background_color=SECONDARY_COLOR
        )
        button.bind(
            on_release=lambda instance, target=screen_name:
                self.navigate_callback(target)
        )
        self.add_widget(button)
