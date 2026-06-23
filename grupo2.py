import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN E INTERFAZ VISUAL PREMIUM (ESTILO BOOTSTRAP LIGHT)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Tecnológico UAP - Grupo 1",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados basados en un diseño Tailwind/Bootstrap Limpio
st.markdown("""
    <style>
    /* Estilo global de la app */
    .stApp {
        background-color: #f8fafc;
    }
    /* Títulos e Identidad Ejecutiva */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 8px solid #3b82f6;
    }
    .main-title {
        font-size: 30px;
        color: #ffffff;
        font-weight: 800;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin: 8px 0 0 0;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
    }
    /* Encabezados de Sección estilo Bootstrap Cards */
    .section-header {
        font-size: 24px;
        color: #1e1b4b;
        font-weight: 700;
        padding-bottom: 10px;
        margin-top: 10px;
        margin-bottom: 25px;
        border-bottom: 3px solid #3b82f6;
    }
    /* Tarjetas de Métricas (KPI Cards) */
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        border-top: 4px solid #3b82f6;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-title {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 34px;
        color: #1e293b;
        font-weight: 700;
    }
    /* Caja de Interpretación Estadística Directa */
    .insight-box {
        background-color: #f0fdf4;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #16a34a;
        color: #14532d;
        font-size: 14.5px;
        margin-top: 15px;
        line-height: 1.7;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .insight-box b {
        color: #16a34a;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado del Banner Principal Estilizado en Light Mode
st.markdown("""
<div class="header-container">
    <div class="main-title">📊 SISTEMA DE ANALÍTICA DEL ECOSISTEMA TECNOLÓGICO DIGITAL</div>
    <div class="subtitle">UNIVERSIDAD AMAZÓNICA DE PANDO (UAP) &bull; INVESTIGADOR: CRUZ PAREDES PLACIDO RAUL &bull; RU: 38992</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PROCESAMIENTO INMUNE A ERRORES E INICIALIZACIÓN (N = 173 DATOS)
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_datos_limpios():
    df = pd.read_csv("ENCUESTA ESTUDIANTIL  - Respuestas de formulario 1 (4).csv")
    
    mapeo = {
        'Ing. de Sistemas': 'Ing. de Sistemas', 'Ingeniería Biomedica': 'Ing. Biomédica',
        'Ingeniería Civil': 'Ing. Civil', 'Ingeniería industrial': 'Ing. Industrial',
        'Derecho': 'Derecho', 'Medicina veterinaria y zootecnia': 'Vet. y Zootecnia',
        'Medicina': 'Medicina', 'Ingeniería Financiera': 'Ing. Financiera', 'Psicología': 'Psicología'
    }
    df['CARRERA'] = df['CARRERA'].replace(mapeo)
    return df

try:
    df_base = cargar_datos_limpios()
except Exception as e:
    st.error("⚠️ Error de Redirección: Verifique que el dataset CSV esté adjunto en el directorio raíz.")
    st.stop()

def desagregar_columna(dataframe, columna):
    expanded = dataframe[columna].dropna().str.split(',\s*')
    all_items = [item.strip() for sublist in expanded for item in sublist if item.strip()]
    return pd.Series(all_items)

PLOTLY_TEMPLATE = "plotly_white"
COLOR_PALETTE = px.colors.qualitative.Prism

# -----------------------------------------------------------------------------
# 3. CONTROL DE NAVEGACIÓN EN LA BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="color: #1e293b; font-weight: 700; margin: 0;">MENÚ TECNOLÓGICO</h3>
    <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">Análisis de Componentes</p>
</div>
""", unsafe_allow_html=True)

secciones = [
    "🛸 Plataformas más utilizadas",
    "⏱️ Frecuencia de acceso",
    "🎯 Actividades más frecuentes en plataformas",
    "🏛️ Uso de plataformas por carrera"
]
ventana_activa = st.sidebar.radio("Seleccione el indicador:", secciones)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎛️ Filtro de Cohorte Dinámico**")
carreras_filtro = ["Todas"] + list(df_base["CARRERA"].unique())
carrera_sel = st.sidebar.selectbox("Filtrar por Unidad Académica:", carreras_filtro)

if carrera_sel != "Todas":
    df_visualizacion = df_base[df_base["CARRERA"] == carrera_sel]
else:
    df_visualizacion = df_base.copy()

st.sidebar.markdown("---")
csv_buffer = df_base.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Exportar Datos Tecnológicos", data=csv_buffer, file_name="tecnologia_uap_clean.csv", mime="text/csv", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. COMPONENTES DE MÉTRICAS (KPIs GRID ESTILO BOOTSTRAP LIGHT)
# -----------------------------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Muestra Tecnológica Activa (n)</div>
        <div class="kpi-value">{len(df_visualizacion)}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #10b981;">
        <div class="kpi-title">Unidades Académicas Auditadas</div>
        <div class="kpi-value">{df_visualizacion["CARRERA"].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    dispositivo_predominante = df_visualizacion["Dispositivo que usas PRINCIPALMENTE para estudiar:"].mode()[0].split()[0]
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #8b5cf6;">
        <div class="kpi-title">Terminal Predominante</div>
        <div class="kpi-value">{dispositivo_predominante}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. CONTENEDOR LOGÍSTICO MULTIPÁGINA REFORMULADO E INTERPRETADO
# -----------------------------------------------------------------------------

# VENTANA 1: PLATAFORMAS MÁS UTILIZADAS -> (CUALITATIVO NOMINAL)
if "Plataformas más utilizadas" in ventana_activa:
    st.markdown('<div class="section-header">Apropiación Tecnológica: Plataformas más utilizadas por el Alumnado</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    series_plat = desagregar_columna(df_visualizacion, 'Plataformas que has utilizado (marca hasta 3):')
    df_plat = series_plat.value_counts().reset_index()
    df_plat.columns = ['Entorno Virtual de Aprendizaje', 'Menciones (fi)']
    df_plat['Tasa de Adopción'] = ((df_plat['Menciones (fi)'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Niveles de Cobertura de Software</h5>", unsafe_allow_html=True)
        st.dataframe(df_plat.style.format({'Tasa de Adopción': '{:.2f}%'}), use_container_width=True, hide_index=True)
        
        plat_top = df_plat.iloc[0]['Entorno Virtual de Aprendizaje']
        tasa_top = df_plat.iloc[0]['Tasa de Adopción']
        st.markdown(f"""
        <div class="insight-box">
            <b>📖 Interpretación y Aplicación de Estadígrafos:</b><br>
            • <b>Tipo de Dato:</b> Cualitativo Nominal (Respuesta Múltiple).<br>
            • <b>Moda (Categoría Modal):</b> Corresponde a <b>{plat_top}</b> con una tasa de penetración del <b>{tasa_top}%</b> del total poblacional (N = 173).<br>
            • <b>Media, Mediana y Desviación Estándar:</b> <b>NO APLICAN</b>. Al ser atributos categóricos sin valor numérico intrínseco ni orden jerárquico, las operaciones aritméticas de suma, promedio o dispersión cuadrática carecen de validez metodológica.<br><br>
            <b>Diagnóstico Técnico:</b> Se confirma estadísticamente una marcada asimetría hacia las soluciones externas no gestionadas directamente por la universidad, superando por amplio margen a la plataforma centralizada Moodle.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        df_completo_grafica = df_plat.sort_values(by='Menciones (fi)', ascending=False)
        
        fig = px.bar(
            df_completo_grafica, x='Entorno Virtual de Aprendizaje', y='Menciones (fi)',
            color='Entorno Virtual de Aprendizaje', color_discrete_sequence=COLOR_PALETTE,
            template=PLOTLY_TEMPLATE, text='Tasa de Adopción', title="Gráfico de Barras: Penetración Completa de Software Educativo"
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 2: FRECUENCIA DE ACCESO -> (CUALITATIVO ORDINAL)
elif "Frecuencia de acceso" in ventana_activa:
    st.markdown('<div class="section-header">Intensidad del Uso: Frecuencia de acceso al Ecosistema Virtual</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    frec_acc = df_visualizacion['Frecuencia de acceso a plataformas:'].value_counts().reset_index()
    frec_acc.columns = ['Hábitos de Ingreso', 'Estudiantes (fi)']
    frec_acc['Porcentaje (%)'] = ((frec_acc['Estudiantes (fi)'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Periodicidad Estudiantil en el Sistema</h5>", unsafe_allow_html=True)
        st.dataframe(frec_acc.style.format({'Porcentaje (%)': '{:.2f}%'}), use_container_width=True, hide_index=True)
        
        acc_top = frec_acc.iloc[0]['Hábitos de Ingreso']
        porc_acc = frec_acc.iloc[0]['Porcentaje (%)']
        st.markdown(f"""
        <div class="insight-box">
            <b>📖 Interpretación y Aplicación de Estadígrafos:</b><br>
            • <b>Tipo de Dato:</b> Cualitativo Ordinal (Posee orden de intensidad lógica).<br>
            • <b>Moda:</b> Se ubica en la opción <b>"{acc_top}"</b> con el <b>{porc_acc}%</b> de las observaciones.<br>
            • <b>Mediana:</b> Al ordenar jerárquicamente las categorías (<i>Nunca < A veces < Diaria</i>), la mediana se posiciona en el intervalo de <b>"A veces"</b>, indicando el punto donde se divide exactamente al 50% de la población.<br>
            • <b>Media y Desviación Estándar:</b> <b>NO APLICAN</b>. Al ser variables de texto ordenado sin propiedades de intervalo métrico numérico, no es factible estimar un promedio matemático o una desviación típica estándar de forma directa.<br><br>
            <b>Diagnóstico Técnico:</b> El ritmo asíncrono predominante refleja un comportamiento intermitente y reactivo ante eventos académicos puntuales.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig = px.pie(
            frec_acc, values='Estudiantes (fi)', names='Hábitos de Ingreso',
            color='Hábitos de Ingreso',
            color_discrete_map={'Aveces': '#f59e0b', 'Diaria': '#10b981', 'Nunca': '#ef4444'},
            template=PLOTLY_TEMPLATE, title="Gráfico de Torta: Distribución Porcentual del Ritmo Asíncrono"
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 3: ACTIVIDADES MÁS FRECUENTES EN PLATAFORMAS -> (CUALITATIVO NOMINAL)
elif "Actividades más frecuentes" in ventana_activa:
    st.markdown('<div class="section-header">Uso Funcional: Actividades más frecuentes en plataformas virtuales</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    series_act = desagregar_columna(df_visualizacion, 'Actividad que realizas CON MÁS FRECUENCIA en plataformas:')
    df_act = series_act.value_counts().reset_index()
    df_act.columns = ['Tipo de Actividad Virtual', 'Menciones']
    df_act['Porcentaje de Uso'] = ((df_act['Menciones'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Análisis Operativo Funcional</h5>", unsafe_allow_html=True)
        st.dataframe(df_act.style.format({'Porcentaje de Uso': '{:.2f}%'}), use_container_width=True, hide_index=True)
        
        act_top = df_act.iloc[0]['Tipo de Actividad Virtual']
        porc_act = df_act.iloc[0]['Porcentaje de Uso']
        st.markdown(f"""
        <div class="insight-box">
            <b>📖 Interpretación y Aplicación de Estadígrafos:</b><br>
            • <b>Tipo de Dato:</b> Cualitativo Nominal.<br>
            • <b>Moda (Actividad Modal):</b> Es la categoría <b>{act_top}</b>, representando el <b>{porc_act}%</b> del flujo operativo virtual.<br>
            • <b>Media, Mediana y Desviación Estándar:</b> <b>NO APLICAN</b>. Debido a que las categorías de uso funcional son excluyentes y nominales, no poseen propiedades algebraicas aritméticas.<br><br>
            <b>Diagnóstico Técnico:</b> El gráfico de barras apiladas consolida un perfil transaccional elemental enfocado en el envío de asignaciones, relegando los espacios de discusión social o debate colaborativo interactivo a un plano secundario.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig = px.bar(
            df_act, x='Menciones', y='Tipo de Actividad Virtual',
            color='Tipo de Actividad Virtual', color_discrete_sequence=px.colors.diverging.Tealrose,
            orientation='h', template=PLOTLY_TEMPLATE, title="Gráfico de Barras Apiladas: Distribución Operativa"
        )
        fig.update_layout(barmode='stack', showlegend=False, margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 4: USO DE PLATAFORMAS POR CARRERA -> (ANÁLISIS MULTIVARIANTE)
elif "Uso de plataformas por carrera" in ventana_activa:
    st.markdown('<div class="section-header">Análisis Multivariante: Uso de plataformas por carrera (Sistemas vs Biomédica vs Financiera vs Psicología)</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.4])
    
    carreras_clave = ['Ing. de Sistemas', 'Ing. Biomédica', 'Ing. Financiera', 'Psicología']
    df_main = df_base[df_base['CARRERA'].isin(carreras_clave)].copy()
    
    plat_rows = []
    for idx, row in df_main.iterrows():
        plat_str = str(row['Plataformas que has utilizado (marca hasta 3):']).lower()
        plat_rows.append({
            'Carrera': row['CARRERA'],
            'Moodle': 1 if 'moodle' in plat_str else 0,
            'Google Classroom': 1 if 'classroom' in plat_str else 0,
            'Zoom/Meet': 1 if any(x in plat_str for x in ['zoom', 'meet']) else 0,
            'WhatsApp': 1 if 'whatsapp' in plat_str else 0
        })
    df_cross = pd.DataFrame(plat_rows).groupby('Carrera').sum().reset_index()
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Matriz de Contingencia Bidimensional Cruzada</h5>", unsafe_allow_html=True)
        st.dataframe(df_cross, use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        <div class="insight-box" style="border-left-color: #8b5cf6; background-color: #f5f3ff; color: #4c1d95;">
            <b>📖 Interpretación y Aplicación de Estadígrafos Cruzados:</b><br>
            • <b>Tipo de Análisis:</b> Matriz de Contingencia para Variables Cualitativas Cruzadas Nominales.<br>
            • <b>Modas por Estrato Académico:</b> Se detecta una asimetría estructural. La moda en el estrato de <i>Ingeniería de Sistemas</i> es la plataforma institucional <b>Moodle</b>, mientras que en las cohortes de <i>Biomédica, Financiera y Psicología</i> la moda migra drásticamente hacia el ecosistema externo <b>Google Classroom</b>.<br>
            • <b>Media, Mediana y Desviación Estándar:</b> <b>NO APLICAN</b>. Para medir la variabilidad o asociación entre dos variables categóricas, la estadística descriptiva multivariante descarta los estadígrafos lineales y recurre al análisis dimensional de contingencia y pruebas de independencia.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        df_melted = pd.melt(df_cross, id_vars=['Carrera'], value_vars=['Moodle', 'Google Classroom', 'Zoom/Meet', 'WhatsApp'], var_name='Plataforma', value_name='Estudiantes')
        
        fig = px.bar(
            df_melted, x='Carrera', y='Estudiantes', color='Plataforma', barmode='group',
            color_discrete_sequence=COLOR_PALETTE, template=PLOTLY_TEMPLATE,
            title="Preferencia de Entornos Virtuales por Área de Conocimiento"
        )
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)