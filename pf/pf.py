import reflex as rx
from pf.Component.navbar import render_navbar
from pf.Component.header import header
from pf.Component.footer import pie_de_pagina
from pf.views.cita_view import citas_page
from pf.views.paciente_page import pacientes_page
from pf.views.medico_page import medico_page
from pf.views.horarios_page import horarios_page
from pf.servicios.cita_servicio import servicio_citas_all
from rxconfig import configS

class State(rx.State):
    """The app state."""
    pass

def index() -> rx.Component:
    trabajos = [
        {
            'titulo': 'Reserva de citas',
            'descripcion': 'Proyecto de gestión de citas médicas',
            'image_url': 'iconos/citas.png'
        },
        {
            'titulo': 'Gestión de médicos',
            'descripcion': 'Proyecto de gestión de información de médicos',
            'image_url': 'iconos/medicos.png'
        },
    ]
    citas = servicio_citas_all()

    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            render_navbar(),
            header(),
            lista_proyecto(trabajos),
            lista_citas(citas),
            pie_de_pagina(),
        ),
        rx.logo(),
    )

def lista_proyecto(trabajos):
    return rx.hstack(*[
        rx.box(
            rx.image(src=trabajo['image_url']),
            rx.text(trabajo['titulo']),
            rx.text(trabajo['descripcion']),
            key=trabajo['titulo']
        ) for trabajo in trabajos
    ])

def lista_citas(citas):
    return rx.hstack(*[
        rx.box(
            rx.text(f"Cita con el Dr. {cita.medico_id} para el paciente {cita.paciente_id}"),
            rx.text(f"Fecha: {cita.fecha} Hora: {cita.hora}"),
            key=cita.id
        ) for cita in citas
    ])

app = rx.App()
app.add_page(index)
app.add_page(citas_page, route="/citas")
app.add_page(pacientes_page, route="/pacientes")
app.add_page(horarios_page, route="/horarios")
app.add_page(medico_page, route="/medicos")
