import reflex as rx
from pf.models.models import Paciente
from pf.servicios.paciente_servicio import (
    servicio_paciente_all,
    servicio_consultar_cedula,
    servicio_crear_paciente,
    servicio_eliminar_paciente
)

class PacienteState(rx.State):
    pacientes: list[Paciente] = []
    buscar_cedula: str = ""

    @rx.background
    async def get_todos_pacientes(self):
        async with self:
            self.pacientes = servicio_paciente_all()
            print("Pacientes page",self.pacientes)

    @rx.background
    async def get_paciente_cedula(self):
        async with self:
            self.pacientes = servicio_consultar_cedula(self.buscar_cedula)

    def buscar_onchange(self, value: str):
        self.buscar_cedula = value

    @rx.background
    async def crear_paciente(self, data: dict):
        async with self:
            try:
                usuario_id = 1 
                data['usuario_id'] = usuario_id
                paciente_creado = servicio_crear_paciente(**data)
                if paciente_creado:
                    self.pacientes.append(paciente_creado)
            except Exception as e:
                print(e)

    @rx.background
    async def eliminar_paciente(self, id: int):
        async with self:
            try:
                if servicio_eliminar_paciente(id):
                    self.pacientes = [p for p in self.pacientes if p.id != id]
            except Exception as e:
                print(e)

@rx.page(route="/pacientes", title="Lista de Pacientes", on_load=PacienteState.get_todos_pacientes)
def pacientes_page() -> rx.Component:
    return rx.flex(
        rx.heading("Pacientes", title="Pacientes", size="5", center=True),
        rx.vstack(
            buscar_paciente_cedula(),
            dialog_paciente_form(),
            justify="center",
            style={"margin": "20px", 'width': "100%"},
        ),
        tabla_pacientes(PacienteState.pacientes),
        direction="column",
        justify="center",
        style={"margin": "auto", 'width': "100%"},
    )

def tabla_pacientes(lista_pacientes: list[Paciente]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Cédula"),
                rx.table.column_header_cell("Nombres"),
                rx.table.column_header_cell("Apellidos"),
                rx.table.column_header_cell("Acciones"),
            )
        ),
        rx.table.body(
            rx.foreach(lista_pacientes, row_table)
        ),
    )

def row_table(paciente: Paciente) -> rx.Component:
    return rx.table.row(
        rx.table.cell(paciente.id),
        rx.table.cell(paciente.cedula),
        rx.table.cell(paciente.nombres),
        rx.table.cell(paciente.apellidos),
        rx.table.cell(
            rx.hstack(
                rx.button("Eliminar", on_click=lambda: PacienteState.eliminar_paciente(paciente.id)),
            )
        ),
    )

def buscar_paciente_cedula() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Cédula", on_change=PacienteState.buscar_onchange),
        rx.button("Buscar Paciente", on_click=PacienteState.get_paciente_cedula)
    )

def dialog_paciente_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Crear Paciente", variant="outline"),
        ),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Paciente"),
                crear_paciente_form(),
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

def crear_paciente_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id", max_length=10),
            rx.input(placeholder="Cédula", name="cedula", max_length=10),
            rx.input(placeholder="Nombres", name="nombres"),
            rx.input(placeholder="Apellidos", name="apellidos"),
            rx.input(placeholder="Correo", name="correo"),
            rx.input(placeholder="Celular", name="celular"),
            rx.input(placeholder="Dirección", name="direccion"),
            rx.input(placeholder="Usuario", name="usuario_id"),
            rx.dialog.close(
                rx.button("Crear Paciente", type="submit"),
            ),
        ),
        on_submit=PacienteState.crear_paciente,
    )
