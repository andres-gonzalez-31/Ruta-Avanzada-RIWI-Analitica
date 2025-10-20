# conexion.py
from sqlalchemy import create_engine

try:
    engine = create_engine('postgresql+psycopg2://postgres:Andy310823*@localhost:5432/aprendizaje_analitica')
    print("Conexión exitosa a la base de datos 'aprendizaje_analitica'")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")