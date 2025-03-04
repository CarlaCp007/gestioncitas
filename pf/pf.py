"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from login import Inicio

from rxconfig import config



def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
        ),
    )


app = rx.App()
app.add_page(index)
