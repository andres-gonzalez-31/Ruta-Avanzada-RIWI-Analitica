import psycopg2

try:
    conexion = psycopg2.connect(
        host="localhost",
        database="ejercicios_numpy_pandas",
        user="postgres",
        password="Andy310823*",
        port=5432
    )
    print("✅ Conexión exitosa a PostgreSQL")

    cursor = conexion.cursor()
    cursor.execute("SELECT version();")
    print("Versión del servidor:", cursor.fetchone())

except Exception as e:
    print("❌ Error en la conexión:", e)

finally:
    if conexion:
        cursor.close()
        conexion.close()
        print("🔒 Conexión cerrada")