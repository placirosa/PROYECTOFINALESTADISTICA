# =============================================================================
# IMPORTACIÓN DE LIBRERÍAS
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# CONFIGURACIÓN DE STREAMLIT
# =============================================================================

st.set_page_config(
    page_title="Procesamiento Estadístico",
    layout="wide"
)

# =============================================================================
# TÍTULO PRINCIPAL
# =============================================================================

st.markdown("""
<div style="
background-color:#1e293b;
padding:20px;
border-radius:10px;
margin-bottom:30px;
">
<h1 style="
color:white;
text-align:center;
font-family:sans-serif;
">
GUÍA DE LABORATORIO - ESTADÍSTICA DESCRIPTIVA
</h1>

<p style="
color:#cbd5e1;
text-align:center;
font-size:18px;
">
Procesamiento Estadístico con Python y Streamlit
</p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# CARGA DEL ARCHIVO CSV
# =============================================================================

try:
    df_est = pd.read_csv("datos_estudiantes.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo 'datos_estudiantes.csv' en el directorio actual. Verifica la ruta.")
    st.stop()
except Exception as e:
    st.error(f"Ocurrió un error inesperado al cargar los datos: {e}")
    st.stop()

# =============================================================================
# MÉTRICAS
# =============================================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Cantidad de Estudiantes",
        len(df_est)
    )

with col2:
    st.metric(
        "Edad Promedio",
        round(df_est["edad"].mean(), 2)
    )

with col3:
    st.metric(
        "Carreras",
        df_est["carrera"].nunique()
    )

# =============================================================================
# FASE 2
# VARIABLE CUALITATIVA
# =============================================================================

st.markdown("""
<h2 style="
color:#1e3a8a;
border-bottom:2px solid #93c5fd;
padding-bottom:10px;
">
VARIABLE CUALITATIVA: CARRERAS
</h2>
""", unsafe_allow_html=True)

# =============================================================================
# TABLA DE FRECUENCIAS
# =============================================================================

frec_cualita = (
    df_est["carrera"]
    .value_counts()
    .reset_index()
)

frec_cualita.columns = ["Carrera", "fi"]

frec_cualita["hi"] = (
    frec_cualita["fi"] / len(df_est)
)

frec_cualita["hip"] = (
    frec_cualita["hi"] * 100
)

frec_cualita["Fi"] = (
    frec_cualita["fi"].cumsum()
)

frec_cualita["Hi"] = (
    frec_cualita["hi"].cumsum()
)

# =============================================================================
# TABLA HTML CORREGIDA (Línea limpia para renderizado directo)
# =============================================================================

filas = ""
for _, fila in frec_cualita.iterrows():
    filas += f"<tr><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Carrera']}</td><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['fi']}</td><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['hi']:.4f}</td><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['hip']:.2f}%</td><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Fi']}</td><td style='padding:10px; border-bottom:1px solid #ddd;'>{fila['Hi']:.4f}</td></tr>"

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
        {filas}
    </tbody>
</table>
"""

st.html(tabla_html)

# =============================================================================
# GRÁFICOS FASE 2
# =============================================================================

plt.style.use("seaborn-v0_8-whitegrid")

colA, colB = st.columns(2)

# =============================================================================
# DIAGRAMA DE BARRAS
# =============================================================================

with colA:
    fig1, ax1 = plt.subplots(figsize=(7, 4))

    sns.barplot(
        x="Carrera",
        y="fi",
        data=frec_cualita,
        hue="Carrera",
        palette="viridis",
        legend=False,
        ax=ax1
    )

    ax1.set_title(
        "DIAGRAMA DE BARRAS",
        fontweight="bold"
    )

    ax1.set_xlabel("Carrera")
    ax1.set_ylabel("Frecuencia")

    st.pyplot(fig1)

# =============================================================================
# GRÁFICO DE TORTA
# =============================================================================

with colB:
    fig2, ax2 = plt.subplots(figsize=(5, 5))

    ax2.pie(
        frec_cualita["fi"],
        labels=frec_cualita["Carrera"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.set_title(
        "GRÁFICO DE TORTA",
        fontweight="bold"
    )

    st.pyplot(fig2)

# =============================================================================
# FASE 3
# VARIABLE CUANTITATIVA DISCRETA
# =============================================================================

st.markdown("""
<br>

<h2 style="
color:#0f766e;
border-bottom:2px solid #99f6e4;
padding-bottom:10px;
">
VARIABLE CUANTITATIVA DISCRETA
</h2>
""", unsafe_allow_html=True)

tabla_discreta = (
    df_est["materias_aprobadas"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_discreta.columns = ["Materias", "fi"]

tabla_discreta["hi"] = (
    tabla_discreta["fi"] / len(df_est)
)

tabla_discreta["hip"] = (
    tabla_discreta["hi"] * 100
)

tabla_discreta["Fi"] = (
    tabla_discreta["fi"].cumsum()
)

tabla_discreta["Hi"] = (
    tabla_discreta["hi"].cumsum()
)

st.dataframe(tabla_discreta)

# =============================================================================
# GRÁFICO DE BASTONES
# =============================================================================

fig3, ax3 = plt.subplots(figsize=(10, 4))

markerline, stemlines, baseline = ax3.stem(
    tabla_discreta["Materias"],
    tabla_discreta["fi"]
)

plt.setp(stemlines, linewidth=2)
plt.setp(markerline, markersize=8)

ax3.set_title(
    "GRÁFICO DE BASTONES",
    fontweight="bold"
)

ax3.set_xlabel("Materias")
ax3.set_ylabel("Frecuencia")

st.pyplot(fig3)

# =============================================================================
# FASE 4
# VARIABLE CUANTITATIVA AGRUPADA
# =============================================================================

st.markdown("""
<br>

<h2 style="
color:#b45309;
border-bottom:2px solid #fdba74;
padding-bottom:10px;
">
VARIABLE CUANTITATIVA AGRUPADA
</h2>
""", unsafe_allow_html=True)

# =============================================================================
# REGLA DE STURGES
# =============================================================================

n = len(df_est)

rango = (
    df_est["edad"].max()
    -
    df_est["edad"].min()
)

k = int(
    np.ceil(
        1 + 3.322 * np.log10(n)
    )
)

amplitud = rango / k

st.markdown(f"""
<div style="
background-color:#fef3c7;
padding:20px;
border-radius:10px;
border:1px solid #f59e0b;
">

<h3 style="color:#92400e;">
Regla de Sturges
</h3>

<ul>
<li><b>Muestra:</b> {n}</li>
<li><b>Rango:</b> {rango}</li>
<li><b>Intervalos:</b> {k}</li>
<li><b>Amplitud:</b> {amplitud:.2f}</li>
</ul>

</div>
""", unsafe_allow_html=True)

# =============================================================================
# INTERVALOS CORREGIDOS (Formato string limpio sin left/right JSON)
# =============================================================================

cortes = np.linspace(
    df_est["edad"].min(),
    df_est["edad"].max(),
    k + 1
)

df_est["intervalos"] = pd.cut(
    df_est["edad"],
    bins=cortes,
    include_lowest=True
)

tabla_grupada = (
    df_est["intervalos"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_grupada.columns = ["Intervalos", "fi"]

# Calculamos y redondeamos la Marca de clase antes de mutar la columna Intervalos
tabla_grupada["Marca"] = (
    tabla_grupada["Intervalos"]
    .apply(lambda x: round(x.mid, 2))
)

# Convertimos los intervalos a un formato de texto amigable [Linf - Lsup)
tabla_grupada["Intervalos"] = (
    tabla_grupada["Intervalos"]
    .apply(lambda x: f"[{round(x.left, 1)} - {round(x.right, 1)})")
)

tabla_grupada["Fi"] = (
    tabla_grupada["fi"].cumsum()
)

st.dataframe(tabla_grupada)

# =============================================================================
# HISTOGRAMA Y POLÍGONO SUPERPUESTO (CORREGIDO Y ALINEADO)
# =============================================================================

colC, colD = st.columns(2)

with colC:
    fig4, ax4 = plt.subplots(figsize=(6, 4))

    frecuencias, bordes, parches = ax4.hist(
        df_est["edad"],
        bins=cortes,
        edgecolor="black",
        alpha=0.7,
        color="#3b82f6",
        label="Histograma"
    )

    # Puntos medios calculados estrictamente desde los bordes del histograma
    puntos_medios = [
        (bordes[i] + bordes[i+1]) / 2 
        for i in range(len(bordes)-1)
    ]
    
    frecuencias_ordenadas = list(tabla_grupada["fi"])

    ax4.plot(
        puntos_medios,
        frecuencias_ordenadas,
        color="#ef4444",
        marker="o",
        linewidth=2,
        label="Polígono"
    )

    ax4.set_title(
        "HISTOGRAMA Y POLÍGONO",
        fontweight="bold"
    )

    ax4.set_xticks(cortes)
    ax4.set_xlim(cortes[0] - 0.5, cortes[-1] + 0.5)
    
    ax4.set_xlabel("Edad")
    ax4.set_ylabel("Frecuencia")
    ax4.legend()

    st.pyplot(fig4)

# =============================================================================
# OJIVA (CORREGIDA Y ALINEADA)
# =============================================================================

with colD:
    fig5, ax5 = plt.subplots(figsize=(6, 4))

    limites = [cortes[0]] + [bordes[i+1] for i in range(len(bordes)-1)]
    y_ojiva = [0] + list(tabla_grupada["Fi"])

    ax5.plot(
        limites,
        y_ojiva,
        marker="o",
        linewidth=2,
        color="#10b981"
    )

    ax5.set_title(
        "OJIVA",
        fontweight="bold"
    )

    ax5.set_xticks(cortes)
    ax5.set_xlim(cortes[0] - 0.5, cortes[-1] + 0.5)
    
    ax5.set_xlabel("Edad")
    ax5.set_ylabel("Frecuencia Acumulada")

    st.pyplot(fig5)

# =============================================================================
# ESTADÍSTICAS DESCRIPTIVAS
# =============================================================================

st.markdown("""
<br>

<h2 style="
color:#7c3aed;
border-bottom:2px solid #c4b5fd;
padding-bottom:10px;
">
ESTADÍSTICAS DESCRIPTIVAS
</h2>
""", unsafe_allow_html=True)

media = df_est["edad"].mean()
mediana = df_est["edad"].median()
desv = df_est["edad"].std()

modas = df_est["edad"].mode().tolist()
moda_texto = ", ".join(map(str, modas))

st.markdown(f"""
<div style="
background-color:#ede9fe;
padding:20px;
border-radius:10px;
border:1px solid #8b5cf6;
">

<ul>
<li><b>Media:</b> {media:.2f}</li>
<li><b>Mediana:</b> {mediana}</li>
<li><b>Moda(s):</b> {moda_texto}</li>
<li><b>Desviación Estándar:</b> {desv:.2f}</li>
</ul>

</div>
""", unsafe_allow_html=True)