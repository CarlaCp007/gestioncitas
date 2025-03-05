from pf.models.models import Cita
from pf.conexion.conexion import connect
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

# Listar todas las citas
def select_all_citas():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Cita).options(selectinload(Cita.paciente), selectinload(Cita.medico))
        citas = session.exec(consulta)
        print(citas)
        return citas.all()

# Buscar cita por ID
def select_cita_por_id(cita_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Cita).where(Cita.id == cita_id)
        resultado = session.exec(consulta)
        return resultado.one_or_none()

# Crear una cita
def crear_cita(cita: Cita):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(cita)
            session.commit()
            print(cita)
            if cita.id is not None:
                consulta = select(Cita).where(Cita.id == cita.id)
                resultado = session.exec(consulta)
                return resultado.one_or_none()
            else:
                return None
    except SQLAlchemyError as e:
        print(e)
        return None

# Eliminar una cita por ID
def eliminar_cita(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Cita).where(Cita.id == id)
            cita = session.exec(consulta).one_or_none()
            if cita:
                session.delete(cita)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False

# Actualizar una cita
def actualizar_cita(cita: Cita):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Cita).where(Cita.id == cita.id)
            cita_actual = session.exec(consulta).one_or_none()
            if cita_actual:
                cita_actual.fecha = cita.fecha
                cita_actual.hora = cita.hora
                cita_actual.paciente_id = cita.paciente_id
                cita_actual.medico_id = cita.medico_id
                session.add(cita_actual)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False
