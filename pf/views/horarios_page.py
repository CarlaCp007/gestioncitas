# views/medico_page.py
import reflex as rx
from pf.models.models import Horario
from pf.servicios.horarios_servicio import (
    servicio_horarios_all,
    servicio_crear_horario,
    servicio_eliminar_horario
)

class HorarioState(rx.State):
    horarios: list[Horario] = []
    medico_id: int = None

    @rx.background
    async def get_todos_horarios(self):
        async with self:
            if self.medico_id:
                self.horarios = servicio_horarios_all(self.medico_id)

    @rx.background
    async def crear_horario(self, data: dict):
        async with self:
            try:
                if self.medico_id:
                    data['medico_id'] = self.medico_id
                    horario_creado = servicio_crear_horario(**data)
                    if horario_creado:
                        self.horarios.append(horario_creado)
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_horario(self, id: int):
        async with self:
            try:
                if servicio_eliminar_horario(id):
                    self.horarios = [h for h in self.horarios if h.id != id]
            except Exception as e:
                print(e)

@rx.page(route="/horarios", title="Gestión de Horarios", on_load=HorarioState.get_todos_horarios)
def horarios_page() -> rx.Component:
    return rx.flex(
        rx.heading("Horarios del Médico", title="Horarios", size="5", center=True),
        rx.vstack(
            dialog_horario_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_horarios(HorarioState.horarios),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_horarios(lista_horarios: list[Horario]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Día"),
                rx.table.column_header_cell("Hora Inicio"),
                rx.table.column_header_cell("Hora Fin"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_horarios, row_table_horario)
        ),
    )

def row_table_horario(horario: Horario) -> rx.Component:
    return rx.table.row(
        rx.table.cell(horario.id),
        rx.table.cell(horario.dia),
        rx.table.cell(horario.hora_inicio),
        rx.table.cell(horario.hora_fin),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: HorarioState.eliminar_horario(horario.id)),
            )
        ),
    )

def dialog_horario_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Agregar Horario", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Agregar Horario"),
                crear_horario_form(),
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

def crear_horario_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Día", name="dia"),
            rx.input(placeholder="Hora Inicio", name="hora_inicio", type="time"),
            rx.input(placeholder="Hora Fin", name="hora_fin", type="time"),
            rx.dialog.close(
                rx.button("Crear Horario", type="submit"),
            ),
        ),
        on_submit=HorarioState.crear_horario,
    )
