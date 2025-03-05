import reflex as rx
from pf.models.models import Cita
from pf.servicios.cita_servicio import (
    servicio_citas_all,
    servicio_consultar_id,
    servicio_crear_cita,
    servicio_eliminar_cita,
    servicio_actualizar_cita
)

class CitaState(rx.State):
    citas: list[Cita] = []
    buscar_id: int = 0

    @rx.background
    async def get_todas_citas(self):
        async with self:
            self.citas = servicio_citas_all()

    @rx.background
    async def get_cita_id(self):
        async with self:
            self.citas = servicio_consultar_id(self.buscar_id)

    def buscar_onchange(self, value: str):
        self.buscar_id = int(value)

    @rx.background
    async def crear_cita(self, data: dict):
        async with self:
            print('DATA DE SERVICIO ',data)
            try:
                nueva_cita = Cita(
                    id=data.get('id'),
                    paciente_id=data.get('paciente_id'),
                    medico_id=data.get('medico_id'),
                    fecha=data.get('fecha'),
                    hora=data.get('hora')
                )
                self.citas.append(servicio_crear_cita(nueva_cita))
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_cita(self, id: int):
        async with self:
            try:
                servicio_eliminar_cita(id)
                await self.get_todas_citas()
            except Exception as e:
                print(e)


@rx.page(route="/citas", title="Lista de Citas", on_load=CitaState.get_todas_citas)
def citas_page() -> rx.Component:
    return rx.flex(
        rx.heading("Citas", title="Citas", size="5", center=True),
        rx.vstack(
            buscar_cita_id(),
            dialog_cita_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_citas(CitaState.citas),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )


def tabla_citas(lista_citas: list[Cita]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Paciente ID"),
                rx.table.column_header_cell("Médico ID"),
                rx.table.column_header_cell("Fecha"),
                rx.table.column_header_cell("Hora"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_citas, row_table_cita)
        ),
    )


def row_table_cita(cita: Cita) -> rx.Component:
    return rx.table.row(
        rx.table.cell(cita.id),
        rx.table.cell(cita.paciente_id),
        rx.table.cell(cita.medico_id),
        rx.table.cell(cita.fecha),
        rx.table.cell(cita.hora),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: CitaState.eliminar_cita(cita.id)),
            )
        ),
    )


def buscar_cita_id() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="ID de Cita", on_change=CitaState.buscar_onchange),
        rx.button("Buscar Cita", on_click=CitaState.get_cita_id)
    )


def dialog_cita_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Cita", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Cita"),
                crear_cita_form(),
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

def crear_cita_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", style={"width": "100px"}, max_length=5),
            rx.input(placeholder="ID del Paciente", name="paciente_id", type="number"),
            rx.input(placeholder="ID del Médico", name="medico_id", type="number"),
            rx.input(placeholder="Fecha", name="fecha", type="date"),
            rx.input(placeholder="Hora", name="hora", type="time"),
            rx.dialog.close(
                rx.button("Crear Cita", type="submit"),
            ),
        ),
        on_submit=CitaState.crear_cita,
    )
