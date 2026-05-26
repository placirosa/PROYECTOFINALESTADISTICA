import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")
#mostrar los primeros 5 registros
print(df_est.head())