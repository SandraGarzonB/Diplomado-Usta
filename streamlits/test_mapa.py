import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
import os

st.set_page_config(page_title="Mapa Choropleth", layout="wide")

st.title("🗺️ Mapa Interactivo de Colombia")

# =======================
# 📁 Verifica archivo geojson
# =======================
geojson_path = "streamlits/Colombia.geo.json"  # Ajusta si está en otra carpeta

if not os.path.exists(geojson_path):
    st.error(f"❌ El archivo GeoJSON no se encontró en: {geojson_path}")
    st.stop()

try:
    with open(geojson_path, encoding="utf-8") as f:
        geojson_data = json.load(f)
except Exception as e:
    st.error(f"❌ Error al leer el archivo GeoJSON: {e}")
    st.stop()

# =======================
# 🧪 Simula valores para colorear
# =======================
codigos_dpto = [str(f"{i:02d}") for i in range(1, 33)]  # '01' a '32'
valores = [i * 3 for i in range(1, 33)]
df_valores = pd.DataFrame({
    "DPTO": codigos_dpto,
    "valor": valores
})

# =======================
# 🗺️ Crea el mapa con Folium
# =======================
try:
    m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_valores,
        columns=["DPTO", "valor"],
        key_on="feature.properties.DPTO",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color="gray",
        legend_name="Valor Simulado",
        highlight=True
    ).add_to(m)

    st.subheader("🌐 Mapa Choropleth por Departamento")
    st_folium(m, width=900, height=600)

except Exception as e:
    st.error(f"❌ Error al generar el mapa: {e}")

