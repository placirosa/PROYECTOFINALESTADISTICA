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

# Calculamos la frecuencia acumulada (Fi) indispensable para la Ojiva
tabla_grupada["Fi"] = tabla_grupada["fi"].cumsum()

# Extraemos los límites superiores de cada intervalo para graficar correctamente la ojiva
limites_superiores = [intervalo.right for intervalo in tabla_grupada["intervalos"]]

# Para que la ojiva empiece desde cero, añadimos el límite inferior al inicio con frecuencia 0
x_ojiva = [cortes[0]] + limites_superiores
y_ojiva = [0] + list(tabla_grupada["Fi"])

# 3. Configuración estética y graficado de la Ojiva
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

fig, ax = plt.subplots(figsize=(12, 6))

# Dibujamos la línea de la Ojiva
ax.plot(
    x_ojiva, 
    y_ojiva, 
    color="purple", 
    marker="o", 
    linewidth=2.5, 
    label="Ojiva (Fi)"
)

# Personalización del gráfico
ax.set_title('OJIVA DE FRECUENCIAS ACUMULADAS: EDAD', fontweight='bold')
ax.set_xlabel('Límites de los Intervalos de Edad')
ax.set_ylabel('Frecuencia Acumulada (Fi)')

# Ajustamos el eje X para que coincida exactamente con los cortes de tus intervalos
ax.set_xticks(cortes)

ax.legend()
plt.show()