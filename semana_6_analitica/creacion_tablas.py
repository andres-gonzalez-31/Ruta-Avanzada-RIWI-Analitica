# crear_tablas.py
from sqlalchemy import text
from conexion import get_engine

def crear_tablas():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS alumnos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50),
                edad INTEGER,
                genero VARCHAR(10),
                ciudad VARCHAR(50)
            );
            CREATE TABLE IF NOT EXISTS clases (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(50),
                nivel VARCHAR(20),
                estilo VARCHAR(30),
                duracion INTEGER,
                precio NUMERIC
            );
            CREATE TABLE IF NOT EXISTS inscripciones (
                id SERIAL PRIMARY KEY,
                alumno_id INTEGER REFERENCES alumnos(id),
                clase_id INTEGER REFERENCES clases(id),
                fecha DATE,
                pagado BOOLEAN
            );
        """))

if __name__ == "__main__":
    crear_tablas()
