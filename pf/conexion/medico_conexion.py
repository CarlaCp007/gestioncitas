from ..models.models import Medico
from .conexion import connect
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError

# Listar todos los médicos
def select_all():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Medico)
        medicos = session.exec(consulta)
        print("estos son los medicos",medicos)
        return medicos.all()

# Buscar médico por especialidad
def select_by_especialidad(especialidad: str):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Medico).where(Medico.especialidad == especialidad)
        resultado = session.exec(consulta)
        return resultado.all()

#Crear un medico
def crear_medico(medico: Medico):
    engine = connect()
    try:
        with Session(engine) as session:
            print(medico)
            session.add(medico)
            session.commit()
            print("Guarda los datos",medico.especialidad)
            if medico.id is not None:
                consulta = select(Medico).where(Medico.id == medico.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)

# Eliminar médico
def eliminar_medico(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Medico).where(Medico.id == id)
            medico = session.exec(consulta).one_or_none()
            if medico:
                session.delete(medico)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)

# Actualizar médico
def actualizar_medico(medico: Medico):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Medico).where(Medico.id == medico.id)
            medico_actual = session.exec(consulta).one_or_none()
            if medico_actual:
                session.update(medico)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)

def select_by_id(id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Medico).where(Medico.id == id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()