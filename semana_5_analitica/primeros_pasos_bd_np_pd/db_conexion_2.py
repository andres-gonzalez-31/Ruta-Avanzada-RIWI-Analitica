from sqlalchemy import create_engine
import pandas as pd
from faker import Faker

#  Conexión con la base de datos PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:Andy310823*@localhost:5432/ejercicios_numpy_pandas')

# 2Inicializar Faker
fake = Faker()

# 3Generar 1000 filas de datos falsos
data = []
for _ in range(1000):
    data.append({
        'name': fake.name(),          # Nombre del cliente
        'fecha': fake.date_this_year()  # Fecha de la venta (año actual)
    })

# 4️⃣ Crear el DataFrame con los datos
df = pd.DataFrame(data)

# 5️⃣ Insertar el DataFrame en la base de datos
#     - if_exists='replace' crea o reemplaza la tabla
#     - index=False evita insertar el índice como columna
df.to_sql('ventas', con=engine, if_exists='replace', index=False)

# 6️⃣ Leer los datos de nuevo desde la base de datos para verificar
df_leido = pd.read_sql("SELECT * FROM ventas", engine)

# 7️⃣ Mostrar las primeras filas
print(df_leido.head())

# 8️⃣ Guardar los datos en un archivo CSV
df_leido.to_csv('ventas_generadas.csv', index=False)

print("\n✅ Se insertaron 1000 registros en la tabla 'ventas' y se guardaron en 'ventas_generadas.csv'")
