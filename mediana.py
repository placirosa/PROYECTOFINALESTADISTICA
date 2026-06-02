import pandas as pd

df_est = pd.read_csv("datos_estudiantes.csv")

mediana_edad = df_est['edad'].median()

print("--- MEDIANA ---")
print(f"La mediana de la edad es: {mediana_edad:.1f} años")


