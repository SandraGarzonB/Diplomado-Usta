

import streamlit as st


from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab
from mapa import show_map_tab


# ================================
# Configuración de la app
# ================================
st.set_page_config(
    page_title="Dashboard - Ministerio de Educación",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Dashboard  - MEN")
st.markdown("Análisis del comportamiento de la cobertura neta y tasa de matriculados a lo largo del tiempo, integrando fuentes de datos del MEN.")

# ================================
# Crear pestañas
# ================================
tabs = st.tabs([
    "📥 Carga de Datos",
    "🔧 Transformación y Métricas",
    "📊 Visualizaciones",
    "🗺️ Mapa Interactivo"
])

# ================================
# Contenido de cada pestaña
# ================================
with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_transform_tab()

with tabs[2]:
    show_visualization_tab()

with tabs[3]:
    show_map_tab()



