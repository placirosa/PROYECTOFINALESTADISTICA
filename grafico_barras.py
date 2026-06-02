import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")

# 2. Procesamiento de datos (Tablas de frecuencia)
frec_cualita = df_est["carrera"].value_counts().reset_index()
frec_cualita.columns = ["carrera", "fi"]

tabla_discreta = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()
tabla_discreta.columns = ['Materias_X', 'fi']

n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k
cortes = np.arange(df_est["edad"].min(), df_est["edad"].max() + amplitud, amplitud)
df_est["intervalos"] = pd.cut(df_est["edad"], bins=cortes, include_lowest=True, right=False)
tabla_grupada = df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_grupada.columns = ["intervalos", "fi"]

# 3. Configuración estética y graficado
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="carrera", y="fi", data=frec_cualita, ax=ax, palette="viridis")

ax.set_title('DISTRIBUCIÓN POR CARRERA', fontweight='bold')
ax.set_xlabel('Carreras Universitarias')
ax.set_ylabel('Cantidad de Estudiantes (fi)')

plt.show()