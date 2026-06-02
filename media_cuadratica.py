import pandas as pd
import numpy as np
df_est = pd.read_csv("datos_estudiantes.csv")

media_cuad = np.sqrt(np.mean(df_est['edad']**2))

print("--- MEDIA CUADRÁTICA ---")
print(f"La media cuadrática de la edad es: {media_cuad:.2f}")


