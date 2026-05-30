import pandas as pd

# 1. Carga de datos
df_est = pd.read_csv("datos_estudiantes.csv")

# 2. Cálculo de la Mediana
mediana_edad = df_est['edad'].median()

print("--- MEDIANA ---")
print(f"La mediana de la edad es: {mediana_edad:.1f} años")