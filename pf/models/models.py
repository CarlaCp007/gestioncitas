import reflex as rx
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel

class Usuario(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True)
    email: str
    tipo: str  

    def __init__(self, nombre: str, email: str, tipo: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre
        self.email = email
        self.tipo = tipo

class Medico(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    especialidad: str
    horarios: List["Horario"] = Relationship(back_populates="medico")
    citas: List["Cita"] = Relationship(back_populates="medico")

"""     def __init__(self, usuario_id: int, especialidad: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario_id = usuario_id
        self.especialidad = especialidad """

class Paciente(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    cedula: str = Field(index=True)
    nombres: str
    apellidos: str
    citas: List["Cita"] = Relationship(back_populates="paciente")

"""     def __init__(self, usuario_id: int, cedula: str, nombres: str, apellidos: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario_id = usuario_id
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos  """

class Especialidad(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

    def __init__(self, nombre: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombre = nombre

class Cita(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    paciente_id: int = Field(foreign_key="paciente.id")
    medico_id: int = Field(foreign_key="medico.id")
    fecha: str
    hora: str
    paciente: Optional[Paciente] = Relationship(back_populates="citas")
    medico: Optional[Medico] = Relationship(back_populates="citas")

    def __init__(self, paciente_id: int, medico_id: int, fecha: str, hora: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        self.fecha = fecha
        self.hora = hora 

class Horario(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    medico_id: int = Field(foreign_key="medico.id")
    dia: str
    hora_inicio: str
    hora_fin: str
    medico: Optional[Medico] = Relationship(back_populates="horarios")

"""     def __init__(self, medico_id: int, dia: str, hora_inicio: str, hora_fin: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.medico_id = medico_id
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin """
