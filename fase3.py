import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")

# 1. Conteo de frecuencias para la variable discreta 'materias_aprobadas'
tabla_discreta = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()

# 2. Renombramos las columnas para que coincidan con tu Guía Metodológica
tabla_discreta.columns = ['Materias_X', 'fi']
#calculo de Frecuencia relativa
tabla_discreta['hi']=tabla_discreta['fi']/len(df_est)
# 3. Cálculo de Frecuencias Acumuladas (Fi)
# El método .cumsum() realiza la suma sucesiva que explicaste en el PDF
tabla_discreta['Fi'] = tabla_discreta['fi'].cumsum()
tabla_discreta['Hi']=tabla_discreta['hi'].cumsum()
tabla_discreta['hip']=tabla_discreta['hi']*100

print("TABLA DE FRECUENCIAS: MATERIAS APROBADAS")
print(tabla_discreta)