import streamlit as st
import pandas as pd
import requests

API_URL = "https://www.datos.gov.co/resource/nudc-7mev.json?$limit=50000"

def load_data_from_api() -> pd.DataFrame:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

def show_data_tab():
    st.header("📥 Carga de Datos del MEN vía API")

    if st.button("🔄 Cargar datos desde API"):
        with st.spinner("Cargando datos..."):
            df_raw = load_data_from_api()

        if not df_raw.empty:
            st.session_state['df_raw'] = df_raw
            st.success(f"¡Datos cargados con {len(df_raw)} filas!")
            st.dataframe(df_raw.head(10))
        else:
            st.warning("No se pudo cargar información.")
    else:
        st.info("Presiona el botón para cargar datos.")

