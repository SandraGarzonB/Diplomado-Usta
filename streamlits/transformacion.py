import streamlit as st
import pandas as pd
from streamlits.utils import normalizar_texto, corregir_departamentos, limpiar_metricas
import plotly.express as px

def show_transform_tab():
    st.title("🔧 Transformación de Datos")

    if 'df_raw' not in st.session_state:
        st.warning("⚠️ Primero carga los datos desde la pestaña anterior.")
        return

    df_raw = st.session_state['df_raw']
    total_original = df_raw.shape[0]

    columnas_relevantes = [
        'a_o', 'departamento', 'municipio', 'c_digo_departamento',
        'poblaci_n_5_16', 'tasa_matriculaci_n_5_16',
        'cobertura_neta', 'cobertura_bruta'
    ]

    columnas_faltantes = [c for c in columnas_relevantes if c not in df_raw.columns]
    if columnas_faltantes:
        st.error(f"❌ Columnas faltantes: {columnas_faltantes}")
        return

    # 🧼 Limpieza inicial
    df = df_raw[columnas_relevantes].copy()
    df = df.dropna(subset=['departamento', 'municipio', 'a_o'])
    df['c_digo_departamento'] = df['c_digo_departamento'].astype(str)

    for col in ["departamento", "municipio"]:
        df[col] = df[col].astype(str).apply(normalizar_texto)

    df = corregir_departamentos(df)
    df = limpiar_metricas(df)
    df = df.drop_duplicates()
    df["departamento"] = df["departamento"].str.strip().str.title()
    total_limpio = df.shape[0]

    # Tipos de datos
    df['a_o'] = pd.to_numeric(df['a_o'], errors='coerce').astype('Int64')
    df['poblaci_n_5_16'] = pd.to_numeric(df['poblaci_n_5_16'], errors='coerce')

    # 📌 1. Métricas de validación
    st.markdown("### 🔵 1. Limpieza y Validación de Datos")
    col1, col2 = st.columns(2)
    col1.metric("📄 Registros originales", total_original)
    col2.metric("✅ Registros válidos", total_limpio)

    # 🌍 2. Dimensiones del Modelo Estrella
    st.markdown("### 🟦 2. Dimensiones del Modelo Estrella")

    dim_tiempo = df[['a_o']].drop_duplicates().sort_values('a_o')
    dim_tiempo['id_tiempo'] = dim_tiempo['a_o']

    dim_geo = df[['c_digo_departamento', 'departamento', 'municipio']].drop_duplicates()
    dim_geo['id_geografico'] = (dim_geo['departamento'] + "_" + dim_geo['municipio']).str.replace(" ", "_").str.lower()

    col1, col2 = st.columns(2)
    col1.metric("📆 Dimensión Tiempo", dim_tiempo.shape[0])
    col2.metric("🗺️ Dimensión Geográfica", dim_geo.shape[0])

    st.markdown("**🗃️ Dimensión Geográfica (vista previa)**")
    st.dataframe(dim_geo.head())

    # 💾 3. Tabla de Hechos
    st.markdown("### 🟦 3. Tabla de Hechos")

    df['id_geografico'] = (df['departamento'] + "_" + df['municipio']).str.replace(" ", "_").str.lower()
    df['id_tiempo'] = df['a_o']

    tabla_hechos = df[[
        'a_o', 'departamento', 'municipio',
        'id_tiempo', 'id_geografico',
        'poblaci_n_5_16', 'tasa_matriculaci_n_5_16',
        'cobertura_neta', 'cobertura_bruta'
    ]].copy()

    st.success(f"✅ Tabla de hechos construida con {tabla_hechos.shape[0]:,} registros.")
    st.dataframe(tabla_hechos.head())

    # Guardar para otras pestañas
    st.session_state['df_clean'] = tabla_hechos
    st.session_state['tabla_hechos'] = tabla_hechos
    st.session_state['dim_geo'] = dim_geo
    st.session_state['dim_tiempo'] = dim_tiempo

    # 📊 4. Estadísticas por Año
    st.markdown("### 📈 4. Estadísticas Descriptivas por Año")
    resumen = (
        tabla_hechos
        .groupby('a_o')[['poblaci_n_5_16', 'tasa_matriculaci_n_5_16', 'cobertura_neta', 'cobertura_bruta']]
        .agg(['mean', 'std', 'min', 'max', 'median'])
        .round(2)
        .sort_index()
    )
    st.dataframe(resumen)

    # 📉 5. Evolución de la Cobertura Neta
    st.markdown("### 📊 5. Evolución de la Cobertura Neta Promedio")
    cobertura_por_año = (
        tabla_hechos
        .groupby('a_o')['cobertura_neta']
        .mean()
        .reset_index()
    )

    fig = px.line(
        cobertura_por_año,
        x='a_o',
        y='cobertura_neta',
        markers=True,
        title="Cobertura Neta Promedio por Año",
        labels={'a_o': 'Año', 'cobertura_neta': 'Cobertura Neta (%)'},
        color_discrete_sequence=['#002855']
    )

    fig.update_layout(
        xaxis=dict(dtick=1),
        yaxis=dict(range=[0, 110]),
        template="simple_white"
    )
    st.plotly_chart(fig, use_container_width=True)


