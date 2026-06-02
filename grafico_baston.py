import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")

tabla_discreta = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()
tabla_discreta.columns = ['Materias_X', 'fi']

# 3. Configuración estética del gráfico
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

# Crear el lienzo
fig, ax = plt.subplots(figsize=(12, 6))

# -----------------------------------------------------------------------------
# GRÁFICO DE BASTÓN (Utilizando ax.stem)
# -----------------------------------------------------------------------------
markerline, stemlines, baseline = ax.stem(
    tabla_discreta['Materias_X'], 
    tabla_discreta['fi'], 
    linefmt='b-',      # Color azul para las líneas (bastones)
    markerfmt='bo',     # Puntos azules en la parte superior
    basefmt=' '         # Oculta la línea base horizontal para un diseño más limpio
)

# Ajustes visuales opcionales para los bastones y los puntos
plt.setp(stemlines, linewidth=2.5)  # Grosor del bastón
plt.setp(markerline, markersize=7)   # Tamaño del punto superior

# Personalización de títulos y ejes
ax.set_title('GRÁFICO DE BASTONES: MATERIAS APROBADAS', fontweight='bold')
ax.set_xlabel('Cantidad de Materias Aprobadas')
ax.set_ylabel('Cantidad de Estudiantes (fi)')

# Asegurar que se muestren todos los valores enteros en el eje X
ax.set_xticks(tabla_discreta['Materias_X'])

# Mostrar el gráfico
plt.show()