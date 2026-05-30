import pandas as pd
from scipy.stats import gmean

# 1. Carga de datos
df_est = pd.read_csv("datos_estudiantes.csv")

# 2. Cálculo de la Media Geométrica
media_geom = gmean(df_est['edad'])

print("--- MEDIA GEOMÉTRICA ---")
print(f"La media geométrica de la edad es: {media_geom:.2f}")