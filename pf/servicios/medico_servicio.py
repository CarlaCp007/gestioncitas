from ..models.models import Medico
from ..conexion.medico_conexion import (select_all, 
                                         select_by_especialidad,
                                         crear_medico, 
                                         eliminar_medico, 
                                         select_by_id)

def servicio_medicos_all():
    medicos = select_all()
    print(medicos)
    return medicos

def servicio_consultar_especialidad(especialidad: str):
    if len(especialidad) != 0:
        medicos = select_by_especialidad(especialidad)
        print(medicos)
        return medicos
    else:
        return select_all()

def servicio_consultar_id(id: int):
    medico = select_by_id(id)
    print(medico)
    return medico
    
def servicio_crear_medico( usuario_id: int, especialidad: str):
    medico = servicio_consultar_id(id)
    if not medico:
        nuevo_medico = Medico(usuario_id=usuario_id, especialidad=especialidad)
        return crear_medico(nuevo_medico)
    else:
        return "El medico ya existe"

def servicio_eliminar_medico(id: int):
    return eliminar_medico(id)
