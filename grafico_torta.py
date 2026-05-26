import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")


frec_cualita = df_est["carrera"].value_counts().reset_index()
frec_cualita.columns = ["carrera", "fi"]

# 3. Configuración estética y graficado del Diagrama de Sectores
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16

fig, ax = plt.subplots(figsize=(8, 8)) # Un lienzo cuadrado (8x8) hace que el círculo se vea perfecto

# Generamos el gráfico de pastel
ax.pie(
    frec_cualita["fi"], 
    labels=frec_cualita["carrera"], 
    autopct='%1.1f%%',          # Muestra el porcentaje con un decimal automáticamente
    startangle=90,              # Rota el inicio del gráfico para una mejor visualización
    colors=['#4f46e5', '#06b6d4', '#10b981', '#f59e0b'], # Paleta de colores limpios
    wedgeprops={'edgecolor': 'white', 'linewidth': 2} # Añade una separación elegante blanca entre sectores
)

# Título del gráfico
ax.set_title('DIAGRAMA DE SECTORES: DISTRIBUCIÓN POR CARRERA', fontweight='bold')

plt.show()