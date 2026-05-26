import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")

n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k

cortes = np.arange(df_est["edad"].min(), df_est["edad"].max() + amplitud, amplitud)
df_est["intervalos"] = pd.cut(df_est["edad"], bins=cortes, include_lowest=True, right=False)

tabla_grupada = df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_grupada.columns = ["intervalos", "fi"]
# La marca de clase es el punto medio de cada barra
tabla_grupada["marca_clase"] = tabla_grupada["intervalos"].apply(lambda x: x.mid)

# 3. Configuración estética y graficado
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

fig, ax = plt.subplots(figsize=(12, 6))

# --- HISTOGRAMA ---
# Usamos las marcas de clase como posición X y definimos el ancho de barra exacto (amplitud)
ax.bar(
    tabla_grupada["marca_clase"], 
    tabla_grupada["fi"], 
    width=amplitud, 
    color="skyblue", 
    edgecolor="black", 
    alpha=0.7, 
    label="Histograma"
)

# --- POLÍGONO DE FRECUENCIAS ---
# Conectamos los puntos medios (marcas de clase) con una línea continua
ax.plot(
    tabla_grupada["marca_clase"], 
    tabla_grupada["fi"], 
    color="red", 
    marker="o", 
    linewidth=2, 
    label="Polígono de frecuencias"
)

# Personalización
ax.set_title('HISTOGRAMA Y POLÍGONO DE FRECUENCIAS: EDAD', fontweight='bold')
ax.set_xlabel('Edad (Marcas de Clase)')
ax.set_ylabel('Cantidad de Estudiantes (fi)')

# Forzar a que el eje X muestre exactamente los cortes de los intervalos
ax.set_xticks(cortes)

ax.legend() # Muestra las etiquetas en el gráfico
plt.show()