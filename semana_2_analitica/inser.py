import csv
import psycopg2
import os

# Obtiene la ruta absoluta de donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_CSV = os.path.join(BASE_DIR, "agrovida_csvs")  # <<--- carpeta donde están los CSV

# Conexión a la base de datos
def get_db_connection():
    return psycopg2.connect(
        host='localhost',
        database='agrovida',
        user='postgres',
        password='Andy310823*'
    )

def insertar_csv_en_tabla(nombre_csv, nombre_tabla, columnas):
    ruta_csv = os.path.join(CARPETA_CSV, nombre_csv)  # <<--- ahora busca en agrovida_csvs

    if not os.path.exists(ruta_csv):
        print(f"⚠️ No se encontró el archivo: {ruta_csv}")
        return

    with open(ruta_csv, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)  # Saltar encabezado

        conn = get_db_connection()
        cur = conn.cursor()

        for fila in lector:
            if not any(fila) or any(c.strip().lower() == 'nan' for c in fila):
                continue

            placeholders = ', '.join(['%s'] * len(fila))
            columnas_str = ', '.join(columnas)
            consulta = f'INSERT INTO {nombre_tabla} ({columnas_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
            cur.execute(consulta, fila)

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ Insertados {lector.line_num - 1} registros en la tabla '{nombre_tabla}'")

def insertar_csvs():
    insertar_csv_en_tabla('tipo_suelo.csv', 'tipo_suelo', ['nombre_tipo_suelo'])
    insertar_csv_en_tabla('sistema_riego.csv', 'sistema_riego', ['nombre_sistema_riego'])
    insertar_csv_en_tabla('tipo_sensor.csv', 'tipo_sensor', ['nombre_tipo_sensor'])
    insertar_csv_en_tabla('cultivo.csv', 'cultivo', ['tipo_cultivo'])
    insertar_csv_en_tabla('unidad_medida.csv', 'unidad_medida', ['nombre'])
    insertar_csv_en_tabla('tecnico.csv', 'tecnico', ['nombre_tecnico'])
    insertar_csv_en_tabla('finca.csv', 'finca', ['nombre_finca','region','es_organico','id_tipo_suelo','id_sistema_riego'])
    insertar_csv_en_tabla('variedad_cultivo.csv', 'variedad_cultivo', ['nombre_variedad','id_cultivo'])
    insertar_csv_en_tabla('sensor.csv', 'sensor', ['id_sensor','estado_sensor','fecha_mantenimiento','id_finca','id_tipo_sensor'])
    insertar_csv_en_tabla('medicion.csv', 'medicion', ['id_sensor','valor','fecha_hora'])
    insertar_csv_en_tabla('finca_cultivo.csv', 'finca_cultivo', ['id_finca','id_variedad','produccion_toneladas'])
    insertar_csv_en_tabla('asignacion_tecnico.csv', 'asignacion_tecnico', ['id_finca','id_tecnico','fecha_inicio','fecha_fin'])
    insertar_csv_en_tabla('fertilizacion.csv', 'fertilizacion', ['id_finca','fertilizante_usado','fecha_aplicacion'])

if __name__ == "__main__":
    insertar_csvs()
