import pandas as pd
from scipy.stats import hmean
df_est = pd.read_csv("datos_estudiantes.csv")

columna_analizar = 'edad' 

# Filtrar para asegurar que no entren ceros o negativos
datos_filtrados = df_est[df_est[columna_analizar] > 0][columna_analizar]

print("--- MEDIA ARMÓNICA ---")
if not datos_filtrados.empty:
    media_arm = hmean(datos_filtrados)
    print(f"La media armónica de '{columna_analizar}' es: {media_arm:.2f}")
else:
    print(f"No hay valores válidos mayores a cero en '{columna_analizar}'.")
    
    

    