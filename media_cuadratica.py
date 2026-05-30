import pandas as pd
import numpy as np

# 1. Carga de datos
df_est = pd.read_csv("datos_estudiantes.csv")

# 2. Cálculo de la Media Cuadrática: Raíz de la media de los cuadrados
media_cuad = np.sqrt(np.mean(df_est['edad']**2))

print("--- MEDIA CUADRÁTICA ---")
print(f"La media cuadrática de la edad es: {media_cuad:.2f}")