import reflex as rx
from ..models.models import Medico
from ..servicios.medico_servicio import *

class MedicoState(rx.State):
    medicos: list[Medico]
    buscar_especialidad: str = ""

    @rx.background
    async def get_todos_medicos(self):
        async with self:
            self.medicos = servicio_medicos_all()
            print(self.medicos)

    rx.background
    def get_medico_especialidad(self):
        self.medicos = servicio_consultar_especialidad(self.buscar_especialidad)

    def buscar_onchange(self, value: str):
        self.buscar_especialidad = value

    # Crear el método para guardar un registro en la BD
    @rx.background
    async def crear_medico(self, data: dict):
        async with self:
            try:
                print(data)
                self.medicos = servicio_crear_medico(
                    data['usuario_id'], data['especialidad']
                )
                self.medicos = servicio_medicos_all()
            except Exception as e:
                print(e)

# Página que muestra el listado de médicos
@rx.page(route="/medicos", title="Lista de Médicos", on_load=MedicoState.get_todos_medicos)
def medico_page() -> rx.Component:
    return rx.flex(
        rx.heading("Médicos", title="Médicos", size="5", center=True),
        rx.vstack(
            buscar_medico_especialidad(),
            dialog_medico_form(),
            tabla_medicos(MedicoState.medicos),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

# Crear el componente de la tabla para la lista de médicos
def tabla_medicos(lista_medicos: list[Medico]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                #rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Usuario ID"),
                rx.table.column_header_cell("Especialidad"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_medicos, row_table)
        ),
    )

def row_table(medico: Medico) -> rx.Component:
    return rx.table.row(
        rx.table.cell(medico.id),
        rx.table.cell(medico.usuario_id),
        rx.table.cell(medico.especialidad),
        rx.table.cell(
            rx.hstack(
                rx.button("Editar", variant="outline"),
                rx.button("Eliminar", variant="outline"),
            )
        ),
    )

def buscar_medico_especialidad() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Especialidad", on_change=MedicoState.buscar_onchange),
        rx.button("Buscar médico", on_click=MedicoState.get_medico_especialidad)
    )

def dialog_medico_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear médico", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear médico"),
                crear_medico_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancelar", variant="soft", color_scheme="red"),
                ),
                spacing="2",
                justify="end",
                margin_top="10px",
            ),
            style={"width": "400px"},
        ),
    )

def crear_medico_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Usuario ID", name="usuario_id"),
            rx.input(placeholder="Especialidad", name="especialidad"),
            rx.dialog.close(
                rx.button("Crear médico", type="submit"),
            ),
        ),
        on_submit=MedicoState.crear_medico,
    )
