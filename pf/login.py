import reflex as rx
import requests as rq


@rx.page(route="/login", title="Inicio")
def Inicio() -> rx.Component:
    return rx.section(
        rx.image(src="/logo.png",width="300px")
    )

