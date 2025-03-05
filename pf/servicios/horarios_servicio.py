from sqlmodel import Session, select
from ..conexion.conexion import connect
from ..models.models import Horario

def servicio_horarios_all(medico_id):
    engine = connect()
    with Session(engine) as session:
        statement = select(Horario).where(Horario.medico_id == medico_id)
        results = session.exec(statement)
        return results.all()

def servicio_crear_horario(medico_id, dia, hora_inicio, hora_fin):
    engine = connect()
    with Session(engine) as session:
        horario = Horario(medico_id=medico_id, dia=dia, hora_inicio=hora_inicio, hora_fin=hora_fin)
        session.add(horario)
        session.commit()
        return horario

def servicio_eliminar_horario(horario_id):
    engine = connect()
    with Session(engine) as session:
        horario = session.get(Horario, horario_id)
        if horario:
            session.delete(horario)
            session.commit()
            return True
    return False
