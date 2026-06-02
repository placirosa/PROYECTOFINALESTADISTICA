import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")

# TABLA DE FRECUENCIAS PARA LA VARIABLE CUANTITATIVA DISCRETA EDAD
n = len(df_est)

# CORRECCIÓN: Cambiar "df" por "df_est" y unificar el nombre de la columna a "edad" (en minúscula)
rango = df_est['edad'].max() - df_est['edad'].min()

# Aplicación de la Regla de Sturges (Rigor académico)
# ceil redondea hacia arriba
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k
print(f"n: {n}, Rango: {rango}, Intervalos (k): {k}, Amplitud: {amplitud}")

# divide el rango en k partes en tipo array
cortes = np.arange(df_est["edad"].min(), df_est["edad"].max() + amplitud, amplitud)

#Definicion de intervalos
#include_lowest=True incluye el primer intervalo
#right=False indica que el intervalo es [a,b)
df_est["intervalos"]=pd.cut(df_est["edad"],bins=cortes,include_lowest=True,right=False)
#a partir de los intervalos se cuentan las frecuencias
tabla_grupada=df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_grupada.columns=["intervalos","fi"]
#nos permite calcular la media de los intervalos
#lambda se usa para aplicar una funcion a cada elemento de la columna
tabla_grupada["marca_class"]=tabla_grupada["intervalos"].apply(lambda x: x.mid)
#frecuencia relativa
tabla_grupada["hi"]=tabla_grupada["fi"]/len(df_est)
#frecuencia relativa porcentual
tabla_grupada["hip"]=tabla_grupada["hi"]*100
#frecuencia acumulada
tabla_grupada["Fi"]=tabla_grupada["fi"].cumsum()
#frecuencia relativa acumulada
tabla_grupada["Hi"]=tabla_grupada["hi"].cumsum()
print(tabla_grupada)

