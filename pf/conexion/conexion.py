from sqlmodel import create_engine, SQLModel

def connect():
    usuario = "admin"
    clave=""
    host="localhost"
    puerto="3000"
    engine= create_engine(f"mariadb+mariadbconnector://{"admin"}:{""}@localhost/hospital")
    SQLModel.metadata.create_all(engine)
    return engine




