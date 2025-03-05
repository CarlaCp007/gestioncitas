from pf.models.models import Cita
from pf.conexion.cita_conexion import (
    select_all_citas,
    select_cita_por_id,
    crear_cita,
    eliminar_cita,
    actualizar_cita
)

def servicio_citas_all():
    citas = select_all_citas()
    print("Salida citas", citas)
    return citas

def servicio_consultar_id(cita_id: int):
    if cita_id != 0:
        cita = select_cita_por_id(cita_id)
        print(cita)
        return cita
    else:
        return select_all_citas()

def servicio_crear_cita(id: int,
                        paciente_id: int,
                        medico_id: int,
                        fecha: str,
                        hora: str):
    
    cita = servicio_consultar_id(id)
    print(cita)
    if not cita:
        nueva_cita = Cita(id=id, paciente_id=paciente_id, medico_id=medico_id, fecha=fecha, hora=hora)
        return crear_cita(nueva_cita)
    else:
        return "La cita ya existe"

def servicio_eliminar_cita(id: int):
    return eliminar_cita(id)

def servicio_actualizar_cita(id: int,
                             paciente_id: int,
                             medico_id: int,
                             fecha: str,
                             hora: str):
    cita = servicio_consultar_id(id)
    if cita:
        cita_actualizada = Cita(id=id, paciente_id=paciente_id, medico_id=medico_id, fecha=fecha, hora=hora)
        return actualizar_cita(cita_actualizada)
    else:
        return "La cita no existe"
