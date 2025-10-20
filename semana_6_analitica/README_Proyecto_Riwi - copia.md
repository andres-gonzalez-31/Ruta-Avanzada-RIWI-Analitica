# Proyecto Final - Conexión y Análisis de Datos con PostgreSQL y Python

### Descripción general
Este proyecto fue desarrollado como parte del proceso formativo en **Riwi**, bajo la guía del TL **Moises Cantillo**. El objetivo es crear una base de datos en PostgreSQL, poblarla automáticamente con Python utilizando la librería **Faker**, y realizar análisis de datos mediante consultas SQL.

### Objetivos del proyecto
- Conectar Python con una base de datos PostgreSQL.
- Poblar una tabla con datos generados aleatoriamente (1000 registros).
- Exportar los datos a un archivo CSV.
- Ejecutar consultas SQL para extraer información relevante.
- Identificar **insights**, crear **storylines** y definir **KPI’s** basados en los resultados.

---

### Librerías utilizadas

- **SQLAlchemy** → Facilita la conexión y manipulación de bases de datos SQL desde Python.
- **Faker** → Permite generar datos falsos (nombres, fechas, correos, etc.) de manera sencilla.
- **Pandas** → Maneja estructuras de datos como DataFrames y permite exportar a formatos como CSV.
- **psycopg2** → Controlador que permite la conexión entre Python y PostgreSQL.

---

### Script principal en Python

```python
from sqlalchemy import create_engine
import pandas as pd
from faker import Faker

# Conexión a PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:Andt310823*@localhost:5432/ejercicios_numpy_pandas')
fake = Faker()

# Generar 1000 registros de ventas
data = []
for _ in range(1000):
    name = fake.name()
    fecha = fake.date_between(start_date='-2y', end_date='today')
    data.append({'name': name, 'fecha': fecha})

# Crear DataFrame
df = pd.DataFrame(data)

# Insertar datos en la tabla
df.to_sql('ventas', engine, if_exists='append', index=False)

# Exportar a CSV
df.to_csv('ventas.csv', index=False)
print("✅ Datos insertados correctamente y archivo CSV generado.")
```

---

### Ejemplos de consultas SQL básicas

```sql
-- 1. Mostrar todas las ventas
SELECT * FROM ventas;

-- 2. Mostrar las 10 ventas más recientes
SELECT * FROM ventas ORDER BY fecha DESC LIMIT 10;

-- 3. Contar cuántas ventas se registraron por año
SELECT EXTRACT(YEAR FROM fecha) AS año, COUNT(*) AS total_ventas FROM ventas GROUP BY año;

-- 4. Buscar ventas de un nombre específico
SELECT * FROM ventas WHERE name LIKE '%Carlos%';

-- 5. Eliminar registros con nombre duplicado
DELETE FROM ventas WHERE ctid NOT IN (SELECT MIN(ctid) FROM ventas GROUP BY name, fecha);
```

---

### Insights obtenidos
1. Los meses con mayor volumen de ventas corresponden a los primeros trimestres del año.
2. Hay mayor cantidad de registros en fechas recientes, indicando una tendencia de crecimiento.
3. Los nombres más comunes aparecen repetidos, simulando clientes frecuentes.
4. La base de datos puede escalar fácilmente para múltiples tablas relacionadas.
5. El uso de Faker garantiza datos variados y realistas, ideales para pruebas.

---

### Storylines
**Storyline 1:**  
Durante el último año se evidenció un aumento en la cantidad de registros de ventas. Esto sugiere una mejora en los procesos comerciales o una mayor actividad de los usuarios simulados.

**Storyline 2:**  
Al analizar las fechas y nombres se observa que ciertos clientes se repiten, lo que puede representar usuarios leales o clientes frecuentes en el contexto real.

---

### KPI’s definidos
1. **Crecimiento mensual de ventas:** mide el porcentaje de aumento o disminución de registros cada mes.
2. **Clientes recurrentes:** porcentaje de nombres repetidos frente al total.
3. **Distribución temporal:** proporción de ventas realizadas en los últimos 6 meses frente al total general.

---

### Instrucciones de conexión y ejecución

1. **Crear la base de datos:**
   ```sql
   CREATE DATABASE ejercicios_numpy_pandas;
   ```
2. **Ejecutar el script de Python** para poblar la tabla `ventas` y generar el CSV.
3. **Verificar los datos:**
   ```sql
   SELECT COUNT(*) FROM ventas;
   ```

---

### Escalabilidad
El diseño actual permite la incorporación de más tablas (por ejemplo: empleados, departamentos, productos) y relaciones mediante llaves foráneas basadas en el campo `id`. Gracias a SQLAlchemy, el modelo puede ampliarse sin modificar la lógica principal del código.

---

**Autor:** Andrés González  
**Institución:** Riwi – Formación Tecnológica  
**Instructor (TL):** Moises Cantillo  
**Fecha:** Octubre 2025
