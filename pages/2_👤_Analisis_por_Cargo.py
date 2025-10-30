"""
Página 2: Análisis por Cargo
Estadísticas detalladas de salarios por posición
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analytics.estadisticas import EstadisticasSalariales
from src.utils.descripciones_cargos import get_descripcion

# Configuración de página
st.set_page_config(
    page_title="Análisis por Cargo - Encuesta Salarial 2do Semestre 2025",
    page_icon="👤",
    layout="wide"
)

# CSS para hacer las métricas responsive
st.markdown("""
<style>
    /* Hacer que las métricas sean responsive */
    [data-testid="stMetricValue"] {
        font-size: clamp(1rem, 2.5vw, 2rem) !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        white-space: normal !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: clamp(0.8rem, 1.5vw, 1rem) !important;
    }

    /* Mejorar el spacing de las columnas */
    [data-testid="column"] {
        padding: 0 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Colores de Perfil Humano
COLORS = {
    'azul': '#2E5090',
    'verde': '#00A651',
    'rojo': '#ED1C24',
    'amarillo': '#FDB913',
    'gris': '#3D5A6C',
    'grande': '#2E5090',  # Azul para empresas grandes
    'pyme': '#00A651'      # Verde para pymes
}

# Cargar datos
@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent
    csv_path = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    df = pd.read_csv(csv_path)
    return df

@st.cache_resource
def calcular_estadisticas(df):
    """Calcula estadísticas para todos los cargos"""
    stats_calc = EstadisticasSalariales(df)
    stats_calc.calcular_todos_los_cargos()
    return stats_calc

def format_currency(value):
    """Formatea valores monetarios"""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.0f}".replace(",", ".")

def main():
    st.title("👤 Análisis Salarial por Cargo")
    st.markdown("Estadísticas detalladas de salarios por posición - P25, P50, P75 y Promedio")
    st.markdown("---")

    # Cargar datos
    df = load_data()

    # Calcular estadísticas
    with st.spinner("Calculando estadísticas de todos los cargos..."):
        stats = calcular_estadisticas(df)

    # Obtener lista de cargos con datos
    cargos_disponibles = list(stats.stats_por_cargo.keys())

    # Crear diccionario de nombres amigables
    cargos_dict = {
        cargo: stats.stats_por_cargo[cargo]['nombre']
        for cargo in cargos_disponibles
    }

    # Sidebar con selectores
    with st.sidebar:
        st.header("Selección de Cargo")

        # Selector de área funcional (opcional)
        areas = {
            'Todos los Cargos': cargos_disponibles,
            'Gerencia General': [c for c in cargos_disponibles if 'ceo' in c or 'asistente_gg' in c],
            'Comercial y Ventas': [c for c in cargos_disponibles if any(x in c for x in ['ventas', 'comercial', 'ejecutivo', 'ecommerce'])],
            'Administración y Finanzas': [c for c in cargos_disponibles if any(x in c for x in ['admin', 'conta', 'finanzas', 'impuestos'])],
            'Recursos Humanos': [c for c in cargos_disponibles if 'rrhh' in c or 'seleccion' in c or 'capacitacion' in c or 'liquidacion' in c],
            'Sistemas y TI': [c for c in cargos_disponibles if any(x in c for x in ['it', 'sistemas', 'programador', 'desarrollo', 'redes', 'soporte'])],
            'Operaciones y Producción': [c for c in cargos_disponibles if any(x in c for x in ['produccion', 'operaciones', 'planta', 'calidad', 'mantenimiento'])],
        }

        area_seleccionada = st.selectbox(
            "Filtrar por Área Funcional",
            list(areas.keys())
        )

        cargos_filtrados = areas[area_seleccionada]

        # Selector de cargo específico
        if cargos_filtrados:
            # Crear opciones con nombres amigables
            opciones_cargo = {cargos_dict[c]: c for c in cargos_filtrados if c in cargos_dict}
            nombre_cargo_seleccionado = st.selectbox(
                "Seleccionar Cargo",
                sorted(opciones_cargo.keys())
            )

            cargo_seleccionado = opciones_cargo[nombre_cargo_seleccionado]
        else:
            st.warning("No hay cargos disponibles para esta área")
            return

        st.markdown("---")

        # Mostrar top cargos
        st.markdown("### Top 10 Cargos con Más Datos")
        top_cargos = stats.get_top_cargos(10)
        for idx, row in top_cargos.iterrows():
            st.markdown(f"**{row['nombre']}**: {row['count']} empresas")

    # ============ CONTENIDO PRINCIPAL ============

    if cargo_seleccionado and cargo_seleccionado in stats.stats_por_cargo:
        cargo_data = stats.stats_por_cargo[cargo_seleccionado]
        cargo_stats = cargo_data['stats']

        # Título del cargo
        st.markdown(f"## {cargo_data['nombre']}")

        # Métricas principales (General)
        if cargo_stats.get('General'):
            st.markdown("### 📊 Estadísticas Generales (Todas las Empresas)")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric(
                    label="P25 (Percentil 25)",
                    value=format_currency(cargo_stats['General']['P25'])
                )

            with col2:
                st.metric(
                    label="P50 (Mediana)",
                    value=format_currency(cargo_stats['General']['P50']),
                    delta="Valor Central"
                )

            with col3:
                st.metric(
                    label="P75 (Percentil 75)",
                    value=format_currency(cargo_stats['General']['P75'])
                )

            with col4:
                st.metric(
                    label="Promedio",
                    value=format_currency(cargo_stats['General']['Promedio'])
                )

            with col5:
                st.metric(
                    label="Respuestas",
                    value=f"{cargo_stats['General']['Count']}",
                    delta="Empresas"
                )

            st.markdown("---")

        # Comparativa Grande vs Pyme
        if cargo_stats.get('Grande') or cargo_stats.get('Pyme'):
            st.markdown("### 📈 Comparativa: Empresas Grandes vs Pymes")

            col1, col2 = st.columns(2)

            with col1:
                # Tabla comparativa
                if cargo_stats.get('Grande') and cargo_stats.get('Pyme'):
                    comparativa_data = []

                    for percentil in ['P25', 'P50', 'P75', 'Promedio']:
                        row = {
                            'Métrica': percentil,
                            'Grande (200+ empleados)': format_currency(cargo_stats['Grande'][percentil]),
                            'Pyme (1-200 empleados)': format_currency(cargo_stats['Pyme'][percentil])
                        }
                        comparativa_data.append(row)

                    df_comp = pd.DataFrame(comparativa_data)
                    st.dataframe(df_comp, use_container_width=True, hide_index=True)

                    # Mostrar brecha salarial
                    brecha = ((cargo_stats['Grande']['P50'] - cargo_stats['Pyme']['P50']) /
                             cargo_stats['Pyme']['P50'] * 100)
                    st.metric(
                        label="Brecha Salarial (P50)",
                        value=f"{brecha:.1f}%",
                        delta="Grande vs Pyme"
                    )

            with col2:
                # Gráfico de barras comparativo
                if cargo_stats.get('Grande') and cargo_stats.get('Pyme'):
                    comparativa_plot = []

                    for percentil in ['P25', 'P50', 'P75']:
                        comparativa_plot.append({
                            'Percentil': percentil,
                            'Grande': cargo_stats['Grande'][percentil],
                            'Pyme': cargo_stats['Pyme'][percentil]
                        })

                    df_plot = pd.DataFrame(comparativa_plot)

                    fig = go.Figure()

                    fig.add_trace(go.Bar(
                        name='Grande (200+ empleados)',
                        x=df_plot['Percentil'],
                        y=df_plot['Grande'],
                        marker_color=COLORS['grande'],
                        customdata=df_plot['Grande'].apply(lambda x: format_currency(x)),
                        hovertemplate='<b>Grande</b><br>%{x}<br>Salario: %{customdata}<extra></extra>'
                    ))

                    fig.add_trace(go.Bar(
                        name='Pyme (1-200 empleados)',
                        x=df_plot['Percentil'],
                        y=df_plot['Pyme'],
                        marker_color=COLORS['pyme'],
                        customdata=df_plot['Pyme'].apply(lambda x: format_currency(x)),
                        hovertemplate='<b>Pyme</b><br>%{x}<br>Salario: %{customdata}<extra></extra>'
                    ))

                    fig.update_layout(
                        title="Comparativa Salarial por Tamaño de Empresa",
                        xaxis_title="Percentil",
                        yaxis_title="Salario Bruto Mensual",
                        barmode='group',
                        height=400,
                        hovermode='x unified'
                    )

                    st.plotly_chart(fig, use_column_width=True)

            st.markdown("---")

        # Distribución de respuestas por tamaño
        if cargo_stats.get('Grande') or cargo_stats.get('Pyme'):
            st.markdown("### 📊 Distribución de Respuestas por Tamaño de Empresa")

            dist_data = []

            if cargo_stats.get('Grande'):
                dist_data.append({
                    'Tamaño': 'Grande (200+)',
                    'Empresas': cargo_stats['Grande']['Count']
                })

            if cargo_stats.get('Pyme'):
                dist_data.append({
                    'Tamaño': 'Pyme (1-200)',
                    'Empresas': cargo_stats['Pyme']['Count']
                })

            if dist_data:
                df_dist = pd.DataFrame(dist_data)

                fig_dist = px.pie(
                    df_dist,
                    values='Empresas',
                    names='Tamaño',
                    title=f'Distribución de Respuestas para {cargo_data["nombre"]}',
                    color='Tamaño',
                    color_discrete_map={
                        'Grande (200+)': COLORS['grande'],
                        'Pyme (1-200)': COLORS['pyme']
                    }
                )
                fig_dist.update_traces(
                    textinfo='none',  # Sin labels visibles
                    hovertemplate='<b>%{label}</b><br>Empresas: %{value}<br>Porcentaje: %{percent}<extra></extra>'
                )
                fig_dist.update_layout(height=400)

                st.plotly_chart(fig_dist, use_column_width=True)

            st.markdown("---")

        # Información adicional del cargo (basada en el nombre de la columna original)
        st.markdown("### 📝 Información del Cargo")

        # Obtener descripción del cargo
        descripcion_cargo = get_descripcion(cargo_seleccionado)

        if descripcion_cargo:
            st.info(f"**{descripcion_cargo['nombre']}**: {descripcion_cargo['descripcion']}")
        else:
            st.info("Información detallada del cargo disponible en el informe completo de la encuesta.")

    else:
        st.warning("Por favor, selecciona un cargo válido en el menú lateral.")

    st.markdown("---")

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem 0;'>
            <p><strong>Perfil Humano</strong> - Encuesta Salarial 2do Semestre 2025 (10ma Edición)</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
