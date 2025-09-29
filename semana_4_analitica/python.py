import pandas as pd

ruta = "dataset_tienda_deportes_Q4_2025.xlsx"  # o la ruta completa
df = pd.read_excel(ruta)  # primera hoja por defecto
print(df.head())