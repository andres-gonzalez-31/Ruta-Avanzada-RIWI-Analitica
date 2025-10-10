"""
Script: conexion_insersion_bd.py
Autor: Andrés Gonzalez
Fecha: 10 de octubre de 2025
Descripción:
Este script crea una base de datos relacional en PostgreSQL utilizando SQLAlchemy y Pandas.
Define tres tablas: departamentos, empleados y ventas. 
Primero elimina las tablas existentes (si las hay), luego genera datos falsos con Faker 
y los inserta en las tablas correspondientes. Finalmente, realiza una consulta de verificación.
"""

# Librerías utilizadas
from sqlalchemy import create_engine, text   # Para conectar con la base de datos y ejecutar sentencias SQL
import pandas as pd                         # Para manejar datos tabulares (DataFrames) y escribirlos en la base
from faker import Faker                     # Para generar datos falsos (nombres, correos, fechas)
import random                               # Para generar números aleatorios y asignar valores variables

# Conexión a PostgreSQL utilizando SQLAlchemy y el driver psycopg2
# Formato: postgresql+psycopg2://usuario:contraseña@host:puerto/nombre_base
engine = create_engine('postgresql+psycopg2://postgres:Andy310823*@localhost:5432/ejercicios_numpy_pandas')

# Inicialización de Faker para generar datos de prueba
fake = Faker()

# Eliminación de tablas previas si existen, en orden correcto (ventas → empleados → departamentos)
# Esto evita errores por dependencias de claves foráneas
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS ventas;"))
    conn.execute(text("DROP TABLE IF EXISTS empleados;"))
    conn.execute(text("DROP TABLE IF EXISTS departamentos;"))
    conn.commit()


# 4. Creación de las tablas con claves primarias y foráneas
create_tables = """
CREATE TABLE departamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100),
    salario NUMERIC(10,2),
    departamento_id INT REFERENCES departamentos(id)
);

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleados(id),
    fecha DATE,
    monto NUMERIC(10,2)
);
"""
with engine.connect() as conn:
    conn.execute(text(create_tables))
    conn.commit()




# Creación de la tabla "departamentos"
# Se define un listado de departamentos y se convierte en un DataFrame
departamentos = ['Ventas', 'Recursos Humanos', 'Finanzas', 'Tecnología', 'Marketing']
df_departamentos = pd.DataFrame({'nombre': departamentos})

# Inserción del DataFrame en la base de datos (crea o reemplaza la tabla si existe)
df_departamentos.to_sql('departamentos', con=engine, if_exists='append', index=False)

# Creación de la tabla "empleados" con datos falsos
# Se genera una lista de 50 empleados con nombre, correo, salario y relación a un departamento
empleados_data = []
for _ in range(50):
    empleados_data.append({
        'nombre': fake.name(),                         # Nombre completo
        'correo': fake.unique.email(),                  # Correo electrónico único
        'salario': round(random.uniform(1200, 5000), 2),# Salario aleatorio entre 1200 y 5000
        'departamento_id': random.randint(1, len(departamentos)) # Relación con un departamento existente
    })

# Conversión a DataFrame y escritura en la base de datos
df_empleados = pd.DataFrame(empleados_data)
df_empleados.to_sql('empleados', con=engine, if_exists='append', index=False)

# Creación de la tabla "ventas"
# Se generan 1000 registros que relacionan empleados con fechas y montos de venta
ventas_data = []
for _ in range(1000):
    ventas_data.append({
        'empleado_id': random.randint(1, len(df_empleados)),  # ID del empleado que realizó la venta
        'fecha': fake.date_this_year(),                       # Fecha dentro del año actual
        'monto': round(random.uniform(100, 2000), 2)          # Monto de la venta entre 100 y 2000
    })

# Conversión del conjunto de ventas a DataFrame y carga en la base de datos
df_ventas = pd.DataFrame(ventas_data)
df_ventas.to_sql('ventas', con=engine, if_exists='append', index=False)

# Mensaje de confirmación de creación y carga de datos
print("Tablas creadas y pobladas correctamente con datos falsos.")

# Consulta de verificación: muestra los primeros 5 registros de la tabla empleados
df_check = pd.read_sql("SELECT * FROM empleados LIMIT 5;", engine)
print(df_check)
