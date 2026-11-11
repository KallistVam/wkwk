from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from config import CARD_COLOR, PRIMARY_COLOR, TEXT_COLOR


def make_label(text, size=16, color=TEXT_COLOR, **kwargs):
    label = Label(
        text=str(text),
        font_size=size,
        color=color,
        halign="left",
        valign="middle",
        **kwargs
    )
    label.bind(size=lambda instance, value: setattr(instance, "text_size", value))
    return label


def make_button(text, callback, height=44):
    button = Button(
        text=text,
        size_hint_y=None,
        height=height,
        background_normal="",
        background_down="",
        background_color=PRIMARY_COLOR,
        color=TEXT_COLOR
    )
    button.bind(on_release=callback)
    return button


def make_card(background=CARD_COLOR):
    card = BoxLayout(
        orientation="vertical",
        padding=15,
        spacing=10
    )
    with card.canvas.before:
        Color(*background)
        card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])
    card.bind(
        pos=lambda instance, value: setattr(card.rect, "pos", value),
        size=lambda instance, value: setattr(card.rect, "size", value)
    )
    return card
