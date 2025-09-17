import os
import pandas as pd
import psycopg2

# 📌 Configuración de conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Andy310823*",
        dbname="agrovida"
    )

# 📁 Carpeta donde están los CSV
csv_folder = "agrovida_csvs"

# ⚡ Orden correcto de inserción según dependencias
orden_tablas = [
    "tipo_suelo",
    "sistema_riego",
    "tipo_sensor",
    "cultivo",
    "tecnico",
    "finca",
    "variedad_cultivo",
    "sensor",
    "medicion",
    "finca_cultivo",
    "asignacion_tecnico",
    "fertilizacion"
]

def insertar_csvs():
    conn = get_connection()
    cur = conn.cursor()

    for tabla in orden_tablas:
        filename = f"{tabla}.csv"
        ruta = os.path.join(csv_folder, filename)

        if not os.path.exists(ruta):
            print(f"⚠️ No existe el archivo: {filename}")
            continue

        # ⚠️ Vaciar la tabla antes de insertar (elimina sus datos previos)
        cur.execute(f'TRUNCATE TABLE "{tabla}" RESTART IDENTITY CASCADE')
        conn.commit()

        # 📥 Leer CSV
        df = pd.read_csv(ruta)

        # 🧹 Quitar filas completamente vacías
        df = df.dropna(how='all')

        # 🗑️ Eliminar columnas ID autogeneradas si existen
        id_cols = [c for c in df.columns if c.startswith("id_")]
        if id_cols:
            df = df.drop(columns=id_cols)

        # Reemplazar NaN por None (NULL)
        df = df.where(pd.notnull(df), None)

        # ⚠️ Si después de limpiar no quedan filas, saltar esta tabla
        if df.empty:
            print(f"⚠️ El archivo {filename} no tiene filas válidas, se omite.")
            continue

        columnas = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f'INSERT INTO "{tabla}" ({columnas}) VALUES ({placeholders})'

        # Insertar fila por fila
        for fila in df.itertuples(index=False, name=None):
            cur.execute(sql, fila)

        conn.commit()
        print(f"✅ Insertados {len(df)} registros en la tabla '{tabla}'")

    cur.close()
    conn.close()

if __name__ == "__main__":
    insertar_csvs()
