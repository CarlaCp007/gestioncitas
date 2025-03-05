from pf.models.models import Paciente
from pf.conexion.paciente_conexion import (
    select_all_pacientes,
    select_paciente_por_cedula,
    crear_paciente,
    eliminar_paciente
)

def servicio_paciente_all():
    pacientes = select_all_pacientes()
    print("Salida pacientes",pacientes)
    return pacientes

def servicio_consultar_cedula(cedula: str):
    if len(cedula) != 0:
        pacientes = select_paciente_por_cedula(cedula)
        print(pacientes)
        return pacientes
    else:
        return select_all_pacientes()
    
def servicio_crear_paciente(id: int,
                            usuario_id: int,
                            nombres: str, 
                            apellidos: str, 
                            cedula: str, 
                            correo: str, 
                            celular: str, 
                            direccion: str):
    
    paciente = servicio_consultar_cedula(cedula)
    print(paciente)
    if not paciente:
        nuevo_paciente = Paciente(id=id,usuario_id=usuario_id, nombres=nombres, apellidos=apellidos, cedula=cedula, correo=correo, celular=celular, direccion=direccion)
        return crear_paciente(nuevo_paciente)
    else:
        return "El paciente ya existe"


def servicio_eliminar_paciente(id: int):
    return eliminar_paciente(id)
