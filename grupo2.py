import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gmean, hmean

# -----------------------------------------------------------------------------
# 1. CONFIGURACIÓN E INTERFAZ VISUAL PREMIUM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Inteligente UAP - Grupo 1",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS avanzados (Simulando un diseño basado en Bootstrap/Tailwind)
st.markdown("""
    <style>
    /* Estilo global de la app */
    .stApp {
        background-color: #f8fafc;
    }
    /* Títulos e Identidad */
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 8px solid #38bdf8;
    }
    .main-title {
        font-size: 32px;
        color: #ffffff;
        font-weight: 800;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-size: 15px;
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
        font-size: 14px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 36px;
        color: #1e293b;
        font-weight: 700;
    }
    /* Caja de insights para conclusiones en vivo */
    .insight-box {
        background-color: #eff6ff;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #2563eb;
        color: #1e3a8a;
        font-size: 14px;
        margin-top: 15px;
        line-height: 1.6;
    }
    .insight-box-success {
        background-color: #f0fdf4;
        padding: 18px;
        border-radius: 8px;
        border-left: 5px solid #16a34a;
        color: #14532d;
        font-size: 14px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado del Banner Principal Estilizado
st.markdown("""
<div class="header-container">
    <div class="main-title">📊 SISTEMA INTEGRADO DE ANALÍTICA MULTIDIMENSIONAL</div>
    <div class="subtitle">UNIVERSIDAD AMAZÓNICA DE PANDO (UAP) &bull; INVESTIGADOR: PLACIKDS788 &bull; RU: 38992</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PROCESAMIENTO INMUNE A ERRORES
# -----------------------------------------------------------------------------
@st.cache_data
def cargar_datos_limpios():
    df = pd.read_csv("ENCUESTA ESTUDIANTIL  - Respuestas de formulario 1 (4).csv")
    df = df.drop_duplicates(subset=['RU'], keep='last')
    df = df[~df['RU'].isin([45427])]
    df = df[df['NOMBRE COMPLETO'].str.contains('Germán Ayaviri Negrete', na=False) == False]
    
    mapeo = {
        'Ing. de Sistemas': 'Ing. de Sistemas', 'Ingeniería Biomedica': 'Ing. Biomédica',
        'Ingeniería Civil': 'Ing. Civil', 'Ingeniería industrial': 'Ing. Industrial',
        'Derecho': 'Derecho', 'Medicina veterinaria y zootecnia': 'Vet. y Zootecnia',
        'Medicina': 'Medicina', 'Ingeniería Financiera': 'Ing. Financiera', 'Psicología': 'Psicología'
    }
    df['CARRERA'] = df['CARRERA'].replace(mapeo)
    
    qual_map = {'Muy mala': 1, 'Mala': 2, 'Regular': 3, 'Buena': 4, 'Exelente': 5}
    int_map = {'Nunca': 1, 'Raramente': 2, 'Aveces': 3, 'Frecuentemente': 4, 'Siempre': 5}
    frec_map = {'Nunca': 1, 'Aveces': 2, 'Diaria': 3}
    
    df['calidad_num'] = df['Calidad percibida de tu conexión para actividades académicas'].map(qual_map)
    df['interrupciones_num'] = df['¿Con qué frecuencia experimentas interrupciones durante clases/trabajo en línea?'].map(int_map)
    df['frecuencia_acceso_num'] = df['Frecuencia de acceso a plataformas:'].map(frec_map)
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

# Template visual unificado para todos los gráficos interactivos de Plotly
PLOTLY_TEMPLATE = "plotly_white"
COLOR_PALETTE = px.colors.qualitative.Prism

# -----------------------------------------------------------------------------
# 3. CONTROL DE FILTROS Y NAVEGACIÓN EN LA BARRA LATERAL
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 20px;">
    <h3 style="color: #1e293b; font-weight: 700; margin: 0;">MENÚ DEL SISTEMA</h3>
    <p style="color: #64748b; font-size: 12px; margin: 5px 0 0 0;">Gestión de Módulos</p>
</div>
""", unsafe_allow_html=True)

secciones = [
    "📡 Conexión e Interrupciones",
    "🛸 Plataformas Utilizadas",
    "⏱️ Frecuencia de Acceso",
    "🎯 Actividades Frecuentes",
    "🏛️ Análisis por Carrera",
    "📐 Tendencia Central Avanzada"
]
ventana_activa = st.sidebar.radio("Seleccione el indicador:", secciones)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎛️ Segmentación en Tiempo Real**")
carreras_filtro = ["Todas"] + list(df_base["CARRERA"].unique())
carrera_sel = st.sidebar.selectbox("Filtro de cohorte:", carreras_filtro)

if carrera_sel != "Todas":
    df_visualizacion = df_base[df_base["CARRERA"] == carrera_sel]
else:
    df_visualizacion = df_base.copy()

st.sidebar.markdown("---")
csv_buffer = df_base.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("📥 Exportar Datos Limpios", data=csv_buffer, file_name="encuesta_uap_clean.csv", mime="text/csv", use_container_width=True)

# -----------------------------------------------------------------------------
# 4. COMPONENTES DE MÉTRICAS (KPIs GRID ESTILO BOOTSTRAP)
# -----------------------------------------------------------------------------
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

with kpi_col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Muestra Activa (n)</div>
        <div class="kpi-value">{len(df_visualizacion)}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #10b981;">
        <div class="kpi-title">Unidades Académicas</div>
        <div class="kpi-value">{df_visualizacion["CARRERA"].nunique()}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    dispositivo_predominante = df_visualizacion["Dispositivo que usas PRINCIPALMENTE para estudiar:"].mode()[0].split()[0]
    st.markdown(f"""
    <div class="kpi-card" style="border-top-color: #8b5cf6;">
        <div class="kpi-title">Hardware Predominante</div>
        <div class="kpi-value">{dispositivo_predominante}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. CONTENEDOR LOGÍSTICO MULTIPÁGINA
# -----------------------------------------------------------------------------

# VENTANA 1: CONEXIÓN E INTERRUPCIONES
if "Conexión e Interrupciones" in ventana_activa:
    st.markdown('<div class="section-header">Infraestructura Crítica: Estabilidad y Cortes de Red</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    frec_int = df_visualizacion['¿Con qué frecuencia experimentas interrupciones durante clases/trabajo en línea?'].value_counts().reset_index()
    frec_int.columns = ['Frecuencia de Cortes', 'Alumnos (fi)']
    frec_int['hi%'] = ((frec_int['Alumnos (fi)'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Estructura de Distribución de Frecuencias</h5>", unsafe_allow_html=True)
        st.dataframe(frec_int.style.format({'hi%': '{:.2f}%'}), use_container_width=True)
        st.markdown("""
        <div class="insight-box">
            <b>Evidencia para Defensa:</b> La inestabilidad de la red inalámbrica actúa como una barrera técnica primaria. Los datos demuestran un alto índice de cortes intermitentes que desestabilizan las sesiones síncronas.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig = px.bar(
            frec_int, x='Alumnos (fi)', y='Frecuencia de Cortes', orientation='h',
            color='Alumnos (fi)', color_continuous_scale='Blues', template=PLOTLY_TEMPLATE,
            text='hi%'
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, margin=dict(t=0, b=0, l=0, r=0))
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 2: PLATAFORMAS UTILIZADAS
elif "Plataformas Utilizadas" in ventana_activa:
    st.markdown('<div class="section-header">Apropiación Tecnológica: Penetración de Software Educativo</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    series_plat = desagregar_columna(df_visualizacion, 'Plataformas que has utilizado (marca hasta 3):')
    df_plat = series_plat.value_counts().reset_index()
    df_plat.columns = ['Plataforma', 'Menciones (fi)']
    df_plat['Tasa de Adopción'] = ((df_plat['Menciones (fi)'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Métricas de Cobertura de Software</h5>", unsafe_allow_html=True)
        st.dataframe(df_plat.style.format({'Tasa de Adopción': '{:.2f}%'}), use_container_width=True)
        st.markdown("""
        <div class="insight-box">
            <b>Hallazgo Clave:</b> Las soluciones comerciales no gestionadas directamente por la universidad ostentan tasas de adopción sustancialmente mayores que las herramientas propietarias de la institución.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        main_four = ['Zoom/Google Meet', 'Google Classroom', 'Moodle', 'WhatsApp educativo']
        df_four = df_plat[df_plat['Plataforma'].isin(main_four)]
        
        fig = px.bar(
            df_four, x='Plataforma', y='Menciones (fi)', color='Plataforma',
            color_discrete_sequence=COLOR_PALETTE, template=PLOTLY_TEMPLATE, text='Tasa de Adopción'
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 3: FRECUENCIA DE ACCESO
elif "Frecuencia de Acceso" in ventana_activa:
    st.markdown('<div class="section-header">Intensidad del Uso: Patrones e Instancia de Acceso</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    frec_acc = df_visualizacion['Frecuencia de acceso a plataformas:'].value_counts().reset_index()
    frec_acc.columns = ['Hábito de Ingreso', 'Estudiantes (fi)']
    frec_acc['Porcentaje (%)'] = ((frec_acc['Estudiantes (fi)'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Frecuencia de Interacción Asíncrona</h5>", unsafe_allow_html=True)
        st.dataframe(frec_acc.style.format({'Porcentaje (%)': '{:.2f}%'}), use_container_width=True)
        st.markdown("""
        <div class="insight-box">
            <b>Patrón de Comportamiento:</b> Predomina un acceso condicionado o reactivo ("A veces"). Esto denota que los sistemas no forman parte de una rutina de autoaprendizaje diario automatizado.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig = px.pie(
            frec_acc, values='Estudiantes (fi)', names='Hábito de Ingreso',
            color='Hábito de Ingreso',
            color_discrete_map={'Aveces': '#f59e0b', 'Diaria': '#10b981', 'Nunca': '#ef4444'},
            template=PLOTLY_TEMPLATE, hole=0.45
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 4: ACTIVIDADES FRECUENTES
elif "Actividades Frecuentes" in ventana_activa:
    st.markdown('<div class="section-header">Uso Funcional: Tipo de Actividades en el Campus Virtual</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    
    series_act = desagregar_columna(df_visualizacion, 'Actividad que realizas CON MÁS FRECUENCIA en plataformas:')
    df_act = series_act.value_counts().reset_index()
    df_act.columns = ['Tipo de Actividad', 'Menciones Absolutas']
    df_act['Porcentaje de Uso'] = ((df_act['Menciones Absolutas'] / len(df_visualizacion)) * 100).round(2)
    
    with col1:
        st.markdown("<h5 style='color:#1e293b;'>Mapeo Operativo Estudiantil</h5>", unsafe_allow_html=True)
        st.dataframe(df_act.style.format({'Porcentaje de Uso': '{:.2f}%'}), use_container_width=True)
        st.markdown("""
        <div class="insight-box">
            <b>Diagnóstico Pedagógico:</b> Las herramientas multimedia operan primordialmente bajo un modelo de <i>repositorio estático transaccional</i> (recepción y entrega de tareas), relegando los espacios de co-creación y debate social a segundo plano.
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        fig = px.bar(
            df_act, x='Menciones Absolutas', y='Tipo de Actividad', orientation='h',
            color='Menciones Absolutas', color_continuous_scale='Cividis', template=PLOTLY_TEMPLATE
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 5: ANÁLISIS POR CARRERA (MULTIVARIANTE)
elif "Análisis por Carrera" in ventana_activa:
    st.markdown('<div class="section-header">Análisis Multivariante: Asimetrías Tecnológicas Cruzadas</div>', unsafe_allow_html=True)
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
        st.markdown("<h5 style='color:#1e293b;'>Matriz de Contingencia (Carrera vs. Software)</h5>", unsafe_allow_html=True)
        st.dataframe(df_cross, use_container_width=True)
        st.markdown("""
        <div class="insight-box" style="border-left-color: #8b5cf6; background-color: #f5f3ff; color: #4c1d95;">
            <b>Punto Clave de Defensa:</b> Note la asimetría de apropiación. Moodle domina significativamente en <i>Ingeniería de Sistemas</i> debido a su naturaleza técnica. Sin embargo, en las demás ciencias analizadas, los estudiantes emigran a ecosistemas externos (Classroom).
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        df_melted = pd.melt(df_cross, id_vars=['Carrera'], value_vars=['Moodle', 'Google Classroom', 'Zoom/Meet', 'WhatsApp'], var_name='Plataforma', value_name='Estudiantes')
        fig = px.bar(
            df_melted, x='Carrera', y='Estudiantes', color='Plataforma', barmode='group',
            color_discrete_sequence=px.colors.qualitative.Bold, template=PLOTLY_TEMPLATE,
            title="Distribución Cruzada de Preferencia de Entornos Virtuales"
        )
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

# VENTANA 6: TENDENCIA CENTRAL AVANZADA
elif "Tendencia Central Avanzada" in ventana_activa:
    st.markdown('<div class="section-header">Auditoría Teórica: Estadísticos de Tendencia Central</div>', unsafe_allow_html=True)
    
    variable_sel = st.selectbox(
        "Seleccione el vector matemático a auditar:",
        ["CARRERA", "Dispositivo que usas PRINCIPALMENTE para estudiar:", "Frecuencia de acceso a plataformas:", "calidad_num", "interrupciones_num", "frecuencia_acceso_num"]
    )
    
    col_info, col_calc = st.columns([1, 1])
    datos_vector = df_visualizacion[variable_sel].dropna()
    
    with col_info:
        if variable_sel in ["CARRERA", "Dispositivo que usas PRINCIPALMENTE para estudiar:", "Frecuencia de acceso a plataformas:"]:
            st.markdown("""
            <div class="insight-box" style="border-left-color: #f59e0b; background-color: #fffbeb; color: #78350f;">
                <b>Variable Categórica / Cualitativa:</b><br>
                Por axioma estadístico fundamental, los datos cualitativos nominales no poseen propiedades aditivas ni de orden escalar. En consecuencia, **el único estadístico central matemáticamente válido es la Moda**. Operadores como la mediana o las medias no son aplicables.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="insight-box-success">
                <b>Variable Ordinal Cuantificada / Escala Discreta:</b><br>
                Al mapear de forma secuencial las categorías ordinales a valores enteros, el vector califica para operaciones de agregación aritmética. Se demuestra la desigualdad asintótica clásica de la estadística: $M_h \\leq M_g \\leq \\bar{X} \\leq RMS$.
            </div>
            """, unsafe_allow_html=True)
            
    with col_calc:
        if not datos_vector.empty:
            if variable_sel in ["CARRERA", "Dispositivo que usas PRINCIPALMENTE para estudiar:", "Frecuencia de acceso a plataformas:"]:
                st.markdown(f"""
                ### Posición de Tendencia Nominal:
                * **Moda ($Mo$ - Elemento Dominante):** `{datos_vector.mode()[0]}`
                * **Media Aritmética ($\mu$):** No Aplicable $\varnothing$
                * **Mediana ($Me$):** No Aplicable $\varnothing$
                """)
            else:
                valores = datos_vector.values
                mean_art = np.mean(valores)
                median_val = np.median(valores)
                moda_val = datos_vector.mode()[0]
                
                try:
                    mean_geo = gmean(valores)
                    mean_arm = hmean(valores)
                except:
                    mean_geo = 0.0
                    mean_arm = 0.0
                    
                mean_quad = np.sqrt(np.mean(valores**2))
                
                st.markdown(f"""
                ### Resultados del Rigor Estadístico:
                * **Media Aritmética ($\\|bar{{X}}$):** `{mean_art:.4f}`
                * **Mediana ($Me$):** `{median_val:.1f}`
                * **Moda ($Mo$):** `{moda_val}`
                * **Media Geométrica ($M_g$):** `{mean_geo:.4f if mean_geo > 0 else "N/A"}`
                * **Media Armónica ($M_h$):** `{mean_arm:.4f if mean_arm > 0 else "N/A"}`
                * **Media Cuadrática ($RMS$):** `{mean_quad:.4f}`
                """)
        else:
            st.warning("No se registran observaciones suficientes para procesar la tendencia central.")