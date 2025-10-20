# conexion.py
from sqlalchemy import create_engine

def get_engine():
    engine = create_engine('postgresql+psycopg2://postgres:Andy310823*@localhost:5432/gestion_inventario_practica')
    return engine
