from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError
from pf.models.models import Paciente
from pf.conexion.conexion import connect

# Listar todos los pacientes
def select_all_pacientes():
    engine = connect()
    with Session(engine) as session:
        consulta = select(Paciente)
        pacientes = session.exec(consulta)
        # print(pacientes)
        return pacientes.all()

# Buscar paciente por cédula
def select_paciente_por_cedula(cedula: str):
    engine = connect()    
    with Session(engine) as session:
        consulta = select(Paciente).where(Paciente.cedula == cedula)
        resultado = session.exec(consulta)
        return resultado.all()

# Crear un paciente
def crear_paciente(paciente: Paciente):
    engine = connect()
    try:
        with Session(engine) as session:
            session.add(paciente)
            session.commit()
            print(paciente)
            session.refresh(paciente)
            return paciente
    except SQLAlchemyError as e:
        print(e)
        return None

# Eliminar un paciente por ID
def eliminar_paciente(id: int):
    engine = connect()
    try:
        with Session(engine) as session:
            consulta = select(Paciente).where(Paciente.id == id)
            paciente = session.exec(consulta).one_or_none()
            if paciente:
                session.delete(paciente)
                session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(e)
        return False
