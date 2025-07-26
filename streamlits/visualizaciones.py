import streamlit as st
import plotly.express as px

COLOR_SCALE = 'YlOrRd'

def show_visualization_tab():
    st.title("📊 Visualizaciones Interactivas")

    if 'df_clean' not in st.session_state:
        st.warning("Primero limpia y transforma los datos.")
        return

    df = st.session_state['df_clean']

    # ------------------------- Gráfico 1 --------------------------
    st.subheader("Evolución de la Cobertura Neta en Colombia (promedio anual)")
    fig = px.line(
        df.groupby('a_o')['cobertura_neta'].mean().reset_index(),
        x='a_o', y='cobertura_neta',
        title="Cobertura neta promedio por año",
        labels={"cobertura_neta": "Cobertura Neta (%)", "a_o": "Año"},
        markers=True
    )
    fig.update_traces(line=dict(color='firebrick'), marker=dict(size=6))
    st.plotly_chart(fig, use_container_width=True)

    # ------------------------- Gráfico 2 --------------------------
    st.subheader("📍 Tasa de Matriculación por Departamento")
    fig2 = px.bar(
        df.groupby('departamento')['tasa_matriculaci_n_5_16'].mean().sort_values(ascending=False).reset_index(),
        x='departamento', y='tasa_matriculaci_n_5_16',
        title="Tasa de matriculación promedio por departamento",
        labels={"tasa_matriculaci_n_5_16": "Tasa Matriculación (%)"},
        color='tasa_matriculaci_n_5_16',
        color_continuous_scale=COLOR_SCALE
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

    # ------------------------- Gráfico 3 --------------------------
    st.subheader("📈 Serie de Tiempo por Departamento")

    df['departamento'] = df['departamento'].str.strip().str.title()
    opciones_departamentos = sorted(df['departamento'].unique())

    valores_defecto = [d for d in ["Bogotá", "Antioquia", "Valle Del Cauca"] if d in opciones_departamentos]

    departamentos_seleccionados = st.multiselect(
        "Selecciona uno o más departamentos para analizar su cobertura neta en el tiempo",
        options=opciones_departamentos,
        default=valores_defecto
    )

    if departamentos_seleccionados:
        df_filtrado = df[df['departamento'].isin(departamentos_seleccionados)]
        fig3 = px.line(
            df_filtrado,
            x='a_o', y='cobertura_neta',
            color='departamento',
            markers=True,
            title="Cobertura neta a lo largo del tiempo por departamento",
            labels={"cobertura_neta": "Cobertura Neta (%)", "a_o": "Año"}
        )
        st.plotly_chart(fig3, use_container_width=True)



