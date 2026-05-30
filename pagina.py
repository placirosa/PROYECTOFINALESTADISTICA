import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import hmean, gmean

# Configuracion de la interfaz de la aplicacion
st.set_page_config(
    page_title="Laboratorio 1 - Procesamiento Estadistico",
    layout="wide"
)

# Encabezado principal del proyecto
st.markdown("""
<div style="background-color:#1e293b; padding:20px; border-radius:10px; margin-bottom:30px;">
    <h1 style="color:white; text-align:center; font-family:sans-serif;">
        PROYECTO - ESTADÍSTICA DESCRIPTIVA
    </h1>
    <p style="color:#cbd5e1; text-align:center; font-size:18px;">
        CRUZ PAREDES PLACIDO RAUL ----- RU: 38992
    </p>
</div>
""", unsafe_allow_html=True)

# csv
df_est=pd.read_csv("datos_estudiantes.csv")

# Despliegue de indicadores generales de la muestra
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Total Registros (n)", len(df_est))
with col_m2:
    st.metric("Promedio General de Edad", round(df_est["edad"].mean(), 2))
with col_m3:
    st.metric("Carreras Evaluadas", df_est["carrera"].nunique())

# FASE 2: TRATAMIENTO DE VARIABLE CUALITATIVA (CARRERAS)

st.markdown("""
<h2 style="color:#1e3a8a; border-bottom:2px solid #93c5fd; padding-bottom:10px;">
    FASE 2: VARIABLE CUALITATIVA NOMINAL (CARRERA)
</h2>
""", unsafe_allow_html=True)

# Generacion de las frecuencias mediante agregacion por conteo
frec_cualita = df_est["carrera"].value_counts().reset_index()
frec_cualita.columns = ["Carrera", "fi"]

# Calculos de frecuencias relativas y acumuladas sucesivas
frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)
frec_cualita["hip"] = frec_cualita["hi"] * 100
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

# Construccion e inyeccion manual de la tabla en HTML
filas_tabla = ""
for _, fila in frec_cualita.iterrows():
    filas_tabla += f"""<tr>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Carrera']}</td>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['fi']}</td>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['hi']:.4f}</td>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['hip']:.2f}%</td>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Fi']}</td>
        <td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Hi']:.4f}</td>
    </tr>"""

tabla_html = f"""
<table style="width:100%; border-collapse:collapse; font-family:sans-serif; text-align:left; margin-bottom:20px;">
    <thead>
        <tr style="background-color:#1e3a8a; color:white;">
            <th style="padding:12px;">Carrera</th>
            <th style="padding:12px;">fi</th>
            <th style="padding:12px;">hi</th>
            <th style="padding:12px;">hip %</th>
            <th style="padding:12px;">Fi</th>
            <th style="padding:12px;">Hi</th>
        </tr>
    </thead>
    <tbody>
        {filas_tabla}
    </tbody>
</table>
"""
st.html(tabla_html)

# Representaciones graficas asociadas a la variable nominal
plt.style.use("seaborn-v0_8-whitegrid")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig_bar, ax_bar = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x="Carrera", y="fi", data=frec_cualita, 
        hue="Carrera", palette="viridis", legend=False, ax=ax_bar
    )
    ax_bar.set_title("DISTRIBUCIÓN POR CARRERA", fontweight="bold")
    ax_bar.set_xlabel("Carreras Universitarias")
    ax_bar.set_ylabel("Cantidad de Estudiantes (fi)")
    st.pyplot(fig_bar)

with col_graf2:
    fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
    ax_pie.pie(
        frec_cualita["fi"], labels=frec_cualita["Carrera"], 
        autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel")
    )
    ax_pie.set_title("PORCENTAJE DE ESTUDIANTES POR CARRERA", fontweight="bold")
    st.pyplot(fig_pie)


# FASE 3: VARIABLE CUANTITATIVA DISCRETA (MATERIAS APROBADAS)

st.markdown("""
<br><h2 style="color:#0f766e; border-bottom:2px solid #99f6e4; padding-bottom:10px;">
    FASE 3: VARIABLE CUANTITATIVA DISCRETA (MATERIAS APROBADAS)
</h2>
""", unsafe_allow_html=True)

# Conteo y ordenacion formal por indice de la variable materias_aprobadas
tabla_discreta = df_est["materias_aprobadas"].value_counts().sort_index().reset_index()
tabla_discreta.columns = ["Materias_X", "fi"]

# Distribucion de frecuencias absolutas, relativas y acumuladas Fi, Hi
tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()
tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()
tabla_discreta["hip"] = tabla_discreta["hi"] * 100

st.dataframe(tabla_discreta)

# Construccion manual del grafico de bastones con stem nativo
fig_baston, ax_baston = plt.subplots(figsize=(10, 4))
markerline, stemlines, baseline = ax_baston.stem(
    tabla_discreta["Materias_X"], tabla_discreta["fi"], 
    linefmt='b-', markerfmt='bo', basefmt=' '
)
plt.setp(stemlines, linewidth=2.5)
plt.setp(markerline, markersize=7)

ax_baston.set_title("AVANCE ACADÉMICO (VARIABLES DISCRETAS)", fontweight="bold")
ax_baston.set_xlabel("Número de Materias Aprobadas")
ax_baston.set_ylabel("Frecuencia Absoluta (fi)")
ax_baston.set_xticks(tabla_discreta["Materias_X"])
st.pyplot(fig_baston)

# FASE 4: VARIABLE CUANTITATIVA AGRUPADA (EDAD - REGLA DE STURGES)

st.markdown("""
<br><h2 style="color:#b45309; border-bottom:2px solid #fdba74; padding-bottom:10px;">
    FASE 4: VARIABLE CUANTITATIVA AGRUPADA POR INTERVALOS (EDAD)
</h2>
""", unsafe_allow_html=True)

# Calculos matematicos basados en el modelo algoritmico de Sturges
n_muestra = len(df_est)
rango_edad = df_est["edad"].max() - df_est["edad"].min()
k_intervalos = int(np.ceil(1 + 3.322 * np.log10(n_muestra)))
amplitud_clase = rango_edad / k_intervalos

st.markdown(f"""
<div style="background-color:#fef3c7; padding:20px; border-radius:10px; border:1px solid #f59e0b;">
    <h3 style="color:#92400e; margin-top:0;">Parametros de Sturges Calculados</h3>
    <ul>
        <li><b>Tamaño de la Muestra (n):</b> {n_muestra}</li>
        <li><b>Rango Extremo:</b> {rango_edad}</li>
        <li><b>Numero de Intervalos Requeridos (k):</b> {k_intervalos}</li>
        <li><b>Amplitud Exacta de Clase:</b> {amplitud_clase:.2f}</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Generacion dinamica del array de cortes delimitadores
cortes_limite = np.arange(df_est["edad"].min(), df_est["edad"].max() + amplitud_clase, amplitud_clase)

# Segmentacion fisica de los registros en los contenedores definidos
df_est["intervalos"] = pd.cut(
    df_est["edad"], bins=cortes_limite, include_lowest=True, right=False
)

# Agrupacion formal de la estructura y tabulacion
tabla_grupada = df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_grupada.columns = ["Intervalos", "fi"]

# Calculo manual de las marcas de clase midpoints
tabla_grupada["marca_clase"] = tabla_grupada["Intervalos"].apply(lambda x: round(x.mid, 2))

# Limpieza estetica de las cadenas de texto del intervalo
tabla_grupada["Intervalos"] = tabla_grupada["Intervalos"].apply(
    lambda x: f"[{round(x.left, 1)} - {round(x.right, 1)})"
)
tabla_grupada["Fi"] = tabla_grupada["fi"].cumsum()

st.dataframe(tabla_grupada)

# Construccion paralela de graficos agrupados (Histograma y Ojiva)
col_v1, col_v2 = st.columns(2)

with col_v1:
    fig_hist, ax_hist = plt.subplots(figsize=(6, 4))
    frecuencias_h, bordes_h, parches_h = ax_hist.hist(
        df_est["edad"], bins=cortes_limite, edgecolor="white", alpha=0.6, color="#11caa0"
    )
    
    # Mapeo de marcas para superposicion del poligono
    puntos_marca = [(bordes_h[i] + bordes_h[i+1]) / 2 for i in range(len(bordes_h)-1)]
    ax_hist.plot(
        puntos_marca, list(tabla_grupada["fi"]), 
        color="red", marker="D", linewidth=2, label="Polígono"
    )
    
    ax_hist.set_title("ANÁLISIS DE DISTRIBUCIÓN DE EDADES", fontweight="bold")
    ax_hist.set_xticks(cortes_limite)
    ax_hist.set_xlim(cortes_limite[0] - 0.5, cortes_limite[-1] + 0.5)
    ax_hist.set_xlabel("Intervalos de Clase (años) / Marca de Clase (Xi)")
    ax_hist.set_ylabel("Frecuencia Absoluta (fi)")
    ax_hist.legend()
    st.pyplot(fig_hist)

with col_v2:
    fig_ojiva, ax_ojiva = plt.subplots(figsize=(6, 4))
    
    limites_sup = [int(cortes_limite[0])] + [int(c) for c in cortes_limite[1:]]
    eje_x_ojiva = limites_sup
    eje_y_ojiva = [0] + list(tabla_grupada["Fi"])
    
    ax_ojiva.plot(
        eje_x_ojiva, eje_y_ojiva, marker="s", linewidth=2, color="red", label="Ojiva"
    )
    ax_ojiva.fill_between(
        eje_x_ojiva, eje_y_ojiva, color="purple", alpha=0.3
    )
    
    ax_ojiva.set_title("ANÁLISIS DE DISTRIBUCIÓN DE EDADES (OJIVA)", fontweight="bold")
    ax_ojiva.set_xticks(cortes_limite)
    ax_ojiva.set_xlim(cortes_limite[0] - 0.5, cortes_limite[-1] + 0.5)
    ax_ojiva.set_xlabel("Intervalos de Clase (años)")
    ax_ojiva.set_ylabel("Frecuencia Absoluta Acumulada (Fi)")
    ax_ojiva.legend()
    st.pyplot(fig_ojiva)

# FASE 5: ESTADÍGRAFOS CENTRALES, DISPERSIÓN Y PARAMETROS DE FORMA

st.markdown("""
<br><h2 style="color:#7c3aed; border-bottom:2px solid #c4b5fd; padding-bottom:10px;">
    INDICADORES CENTRALES, MEDIAS AVANZADAS Y MEDIDAS DE FORMA
</h2>
""", unsafe_allow_html=True)

# Centralizacion de variables estadisticas continuas (Edad)
target_col = "edad"
calc_media = df_est[target_col].mean()
calc_mediana = df_est[target_col].median()
calc_std = df_est[target_col].std()
array_modas = df_est[target_col].mode().tolist()
string_modas = ", ".join(map(str, array_modas))

# Filtros para prevencion de indeterminacion matematica en medias asimetricas
valores_filtrados = df_est[df_est[target_col] > 0][target_col]
calc_armonica = hmean(valores_filtrados) if not valores_filtrados.empty else 0
calc_geometrica = gmean(valores_filtrados) if not valores_filtrados.empty else 0
calc_cuadratica = np.sqrt(np.mean(df_est[target_col]**2))

# Calculo numerico de indicadores de forma de la distribucion
calc_skew = df_est[target_col].skew()
calc_kurt = df_est[target_col].kurt()

# Renderizado de los bloques informativos de salida
c_box1, c_box2, c_box3 = st.columns(3)

with c_box1:
    st.markdown(f"""
    <div style="background-color:#ede9fe; padding:20px; border-radius:10px; border:1px solid #8b5cf6; height: 100%;">
        <h3 style="color:#6d28d9; margin-top:0;">Tendencia Central y Dispersion</h3>
        <ul>
            <li><b>Media Aritmetica:</b> {calc_media:.2f} años</li>
            <li><b>Mediana:</b> {calc_mediana} años</li>
            <li><b>Moda(s) detectada(s):</b> {string_modas}</li>
            <li><b>Desviacion Estandar:</b> {calc_std:.2f}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c_box2:
    st.markdown(f"""
    <div style="background-color:#f5f3ff; padding:20px; border-radius:10px; border:1px solid #a78bfa; height: 100%;">
        <h3 style="color:#6d28d9; margin-top:0;">Modelos de Medias Avanzadas</h3>
        <ul>
            <li><b>Media Armonica:</b> {calc_armonica:.2f}</li>
            <li><b>Media Geometrica:</b> {calc_geometrica:.2f}</li>
            <li><b>Media Cuadratica (RMS):</b> {calc_cuadratica:.2f}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c_box3:
    st.markdown(f"""
    <div style="background-color:#f8fafc; padding:20px; border-radius:10px; border:1px solid #cbd5e1; height: 100%;">
        <h3 style="color:#475569; margin-top:0;">Analisis Lineal de Forma</h3>
        <ul>
            <li><b>Asimetria (Skewness):</b> {calc_skew:.4f}</li>
            <li><b>Curtosis (Kurtosis):</b> {calc_kurt:.4f}</li>
        </ul>
        <p style="font-size:11px; color:#64748b; margin-top:15px; margin-bottom:0;">
            * Parametros agregados para la descripcion formal de la silueta del histograma de edades.
        </p>
    </div>
    """, unsafe_allow_html=True)

