from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from config import BG_COLOR
from widgets.components import make_card, make_label
from widgets.sidebar import Sidebar


class DashboardScreen(Screen):
    def __init__(self, navigate_callback, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="horizontal", spacing=12, padding=12)

        root.add_widget(Sidebar(navigate_callback))

        content = BoxLayout(orientation="vertical", padding=18, spacing=16)
        content.add_widget(make_label("Dashboard", 28, size_hint_y=None, height=48))
        content.add_widget(make_label(
            "Welcome to Computer System Simulator. Select a module to begin.",
            16, size_hint_y=None, height=40
        ))

        cards = BoxLayout(orientation="horizontal", spacing=12)
        card_info = [
            ("CPU", "Execute arithmetic instructions", "system"),
            ("RAM", "Read and write simulated memory", "system"),
            ("Processes", "Manage simulated processes", "process"),
        ]
        for title, description, target in card_info:
            card = make_card()
            card.add_widget(make_label(title, 21, size_hint_y=None, height=38))
            card.add_widget(make_label(description, 13))
            cards.add_widget(card)
        content.add_widget(cards)

        content.add_widget(make_label(
            "Modules\n• System Simulation\n• Virtual File Manager\n• Process Manager",
            16
        ))
        root.add_widget(content)

        with self.canvas.before:
            Color(*BG_COLOR)
            self.background = Rectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda instance, value: setattr(self.background, "pos", value),
            size=lambda instance, value: setattr(self.background, "size", value)
        )
        self.add_widget(root)
