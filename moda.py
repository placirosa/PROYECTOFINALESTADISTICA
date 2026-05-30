import pandas as pd

# 1. Carga de datos
df_est = pd.read_csv("datos_estudiantes.csv")

# 2. Cálculo de la Moda (usando 'edad' en minúscula)
serie_moda = df_est['edad'].mode()

print("--- MODA ---")
if not serie_moda.empty:
    moda_edad = serie_moda.iloc[0]
    print(f"La edad más común (moda) entre los estudiantes es: {moda_edad} años")
else:
    print("No se pudo calcular la moda para la columna 'edad'.")
    
    