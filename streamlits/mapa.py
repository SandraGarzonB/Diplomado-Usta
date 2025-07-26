import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium

def show_map_tab():
    st.header("🗺️ Mapa Interactivo por Departamento")

    # Verificación de datos transformados
    if not all(key in st.session_state for key in ['df_clean', 'dim_geo', 'dim_tiempo']):
        st.warning("⚠️ Asegúrate de haber transformado los datos correctamente en la pestaña de Transformación.")
        return

    df_fact = st.session_state['df_clean']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']

    # Unir con dimensiones
    df = df_fact.merge(dim_geo, on='id_geografico').merge(dim_tiempo, on='id_tiempo')

    # Selección de métrica
    metricas = {
        'Cobertura Neta (%)': 'cobertura_neta',
        'Cobertura Bruta (%)': 'cobertura_bruta',
        'Tasa de Matriculación 5-16 (%)': 'tasa_matriculaci_n_5_16'
    }
    metrica_label = st.selectbox("📊 Selecciona la métrica", list(metricas.keys()))
    metrica_col = metricas[metrica_label]

    # Selección de año
    años = sorted(df['id_tiempo'].unique())

    año_sel = st.selectbox("📅 Selecciona el año", años, index=len(años)-1)

    # Filtrar y agrupar datos
    df_filtrado = df[df['id_tiempo'] == año_sel]
    resumen = df_filtrado.groupby('c_digo_departamento')[metrica_col].mean().reset_index()
    resumen['c_digo_departamento'] = resumen['c_digo_departamento'].astype(str).str.zfill(2)

    # Leer archivo GeoJSON
    try:
        with open("streamlits/Colombia.geo.json", encoding="utf-8") as f:
            geojson_data = json.load(f)
    except Exception as e:
        st.error(f"❌ No se pudo leer el archivo GeoJSON: {e}")
        return

    # Crear el mapa
    try:
        m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")

        folium.Choropleth(
            geo_data=geojson_data,
            name="choropleth",
            data=resumen,
            columns=["c_digo_departamento", metrica_col],
            key_on="feature.properties.DPTO",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.2,
            nan_fill_color="gray",
            legend_name=f"{metrica_label} - {año_sel}",
            highlight=True
        ).add_to(m)

        folium.LayerControl().add_to(m)

        st.subheader(f"🧭 {metrica_label} por Departamento - {año_sel}")
        st_folium(m, width=750, height=550)

    except Exception as e:
        st.exception(f"🚨 Error al generar el mapa: {e}")






