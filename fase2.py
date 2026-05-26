import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")
#variable cualitativa nominal nombre de las carreras
frec_cualita=df_est["carrera"].value_counts().reset_index()
#renombrar columnas
frec_cualita.columns=["carrera","fi"]
#frecuencia relativa
frec_cualita["hi"]=frec_cualita["fi"]/len(df_est)
#frecuencia relativa porcentual
frec_cualita["hip"]=frec_cualita["hi"]*100
#frecuencia acumulada
frec_cualita["Fi"]=frec_cualita["fi"].cumsum()
#frecuencia relativa acumulada
frec_cualita["Hi"]=frec_cualita["hi"].cumsum()
print("TABLA DE FRECUENCIAS: CARRERAS")
print(frec_cualita)