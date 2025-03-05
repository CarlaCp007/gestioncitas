from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError
from pf.models.models import Medico, Horario
from pf.conexion.conexion import connect

# Listar todos los horarios de un médico
def select_all_horarios(medico_id: int):
    engine = connect()
    with Session(engine) as session:
        consulta = select(Horario).where(Horario.medico_id == medico_id)
        horarios = session.exec(consulta)
        return horarios.all()

# Crear un horario para un médico
def crear_horario(horario: Horario):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(horario)
            session.commit()
            session.refresh(horario)
            return horario
    except SQLAlchemyError as e:
        print(e)
        return None

# Eliminar un horario por ID
def eliminar_horario(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Horario).where(Horario.id == id)
            horario = session.exec(consulta).one_or_none()
            if horario:
                session.delete(horario)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False
