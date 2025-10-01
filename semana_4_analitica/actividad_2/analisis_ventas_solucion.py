# analisis_ventas_solucion.py
# -----------------------------------------------------------
# Análisis comercial: carga -> limpieza -> KPIs (media/mediana/moda)
# Dataset esperado: dataset_tienda_deportes_Q4_2025.xlsx
# -----------------------------------------------------------

import pandas as pd
import numpy as np
from statistics import multimode

def main(path_excel="/mnt/data/dataset_tienda_deportes_Q4_2025.xlsx"):
    # 1) Carga
    df = pd.read_excel(path_excel, sheet_name=0)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(3))

    # 2) Selección de columnas clave
    cols_key = ["ID_Venta","Producto","Categoría","Precio_COP","Cantidad","Total_Venta","Ciudad","Fecha_Compra"]
    df = df[cols_key].copy()

    # 3) Limpieza básica
    # 3.1 Consistencia de Total_Venta
    df["Total_Venta_calc"] = df["Precio_COP"] * df["Cantidad"]
    mask_diff = np.isfinite(df["Total_Venta"]) & (np.abs(df["Total_Venta"] - df["Total_Venta_calc"]) > 0.01 * df["Total_Venta_calc"])
    df.loc[mask_diff, "Total_Venta"] = df.loc[mask_diff, "Total_Venta_calc"]

    # 3.2 Duplicados por ID_Venta
    before = len(df)
    df = df.drop_duplicates(subset=["ID_Venta"]).copy()
    print("Duplicados eliminados:", before - len(df))

    # 3.3 Validación de valores positivos
    df = df[(df["Cantidad"] > 0) & (df["Precio_COP"] > 0)].copy()

    # 4) Outliers en Total_Venta por IQR
    q1 = df["Total_Venta"].quantile(0.25)
    q3 = df["Total_Venta"].quantile(0.75)
    iqr = q3 - q1
    low_fence  = q1 - 1.5 * iqr
    high_fence = q3 + 1.5 * iqr
    outlier_mask = (df["Total_Venta"] < low_fence) | (df["Total_Venta"] > high_fence)
    print("Outliers detectados (Total_Venta):", int(outlier_mask.sum()))

    df_clean = df[~outlier_mask].copy()
    print("Filas finales (sin outliers):", df_clean.shape[0])

    # 5) KPIs (media/mediana/moda)
    media_tv   = df_clean["Total_Venta"].mean()
    mediana_tv = df_clean["Total_Venta"].median()
    moda_tv    = multimode(df_clean["Total_Venta"].round(2))

    print("\n[Estadísticos de Total_Venta]")
    print("Media   :", media_tv)
    print("Mediana :", mediana_tv)
    print("Moda(s) :", moda_tv)

    min_tv = df_clean["Total_Venta"].min()
    max_tv = df_clean["Total_Venta"].max()
    print("\n[Distribución de Total_Venta]")
    print("Mínimo  :", min_tv)
    print("Máximo  :", max_tv)
    print("Media   :", media_tv)
    print("Mediana :", mediana_tv)

    # Clasificación por rangos (percentiles) sin usar groupby avanzado
    p25 = df_clean["Total_Venta"].quantile(0.25)
    p50 = df_clean["Total_Venta"].quantile(0.50)
    p75 = df_clean["Total_Venta"].quantile(0.75)
    bins = [0, p25, p50, p75, df_clean["Total_Venta"].max() + 1]
    labels = ["bajo","medio-bajo","medio-alto","alto"]
    df_clean["Rango_Monto"] = pd.cut(df_clean["Total_Venta"], bins=bins, labels=labels, include_lowest=True)
    print("\n[Conteo por rangos de monto]")
    print(df_clean["Rango_Monto"].value_counts().sort_index())

    # Conteo por Ciudad (frecuencia simple)
    print("\n[Conteo de transacciones por Ciudad]")
    print(df_clean["Ciudad"].value_counts())

    # Promedio por 'alto/bajo' según mediana (paralelo conceptual)
    df_clean["Alto_Monto"] = (df_clean["Total_Venta"] >= p50).map({True:"Alto", False:"Bajo"})
    print("\n[Promedio de Total_Venta por (Bajo/Alto)]")
    print(df_clean.groupby("Alto_Monto")["Total_Venta"].mean())

if __name__ == "__main__":
    main()
