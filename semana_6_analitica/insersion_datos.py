# insertar_datos.py
import pandas as pd
from faker import Faker
import random
from conexion import get_engine

fake = Faker()
engine = get_engine()

def insertar_alumnos():
    alumnos = []
    for _ in range(80):
        alumnos.append({
            'nombre': fake.name(),
            'edad': random.randint(10, 60),
            'genero': random.choice(['Masculino', 'Femenino']),
            'ciudad': fake.city()
        })
    pd.DataFrame(alumnos).to_sql('alumnos', engine, if_exists='append', index=False)

def insertar_clases():
    estilos = ['Salsa', 'Ballet', 'Hip Hop', 'Jazz', 'Contemporáneo', 'Flamenco']
    niveles = ['Principiante', 'Intermedio', 'Avanzado']
    clases = []
    for _ in range(15):
        clases.append({
            'nombre': fake.word().capitalize(),
            'nivel': random.choice(niveles),
            'estilo': random.choice(estilos),
            'duracion': random.choice([60, 90, 120]),
            'precio': round(random.uniform(80, 350), 2)
        })
    pd.DataFrame(clases).to_sql('clases', engine, if_exists='append', index=False)

def insertar_inscripciones():
    inscripciones = []
    for _ in range(200):
        inscripciones.append({
            'alumno_id': random.randint(1, 80),
            'clase_id': random.randint(1, 15),
            'fecha': fake.date_between(start_date='-1y', end_date='today'),
            'pagado': random.choice([True, False])
        })
    pd.DataFrame(inscripciones).to_sql('inscripciones', engine, if_exists='append', index=False)

if __name__ == "__main__":
    insertar_alumnos()
    insertar_clases()
    insertar_inscripciones()
