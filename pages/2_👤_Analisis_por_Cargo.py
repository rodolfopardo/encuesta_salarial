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

# PARCHE: Valores hardcodeados para 5 puestos específicos
HARDCODED_STATS = {
    'salario_analista_ecommerce': {
        'nombre': 'Analista Ecommerce',
        'Grande': {
            'P25': 1625000,
            'P50': 1702000,
            'P75': 1853000,
            'Promedio': 1776000,
            'Count': 4
        },
        'Pyme': {
            'P25': 1591001,
            'P50': 1650000,
            'P75': 1718000,
            'Promedio': 1659001,
            'Count': 4
        }
    },
    'salario_analista_facturacion': {
        'nombre': 'Analista Facturacion',
        'Grande': {
            'P25': 1460000,
            'P50': 1520000,
            'P75': 1657700,
            'Promedio': 1548504,
            'Count': 15
        },
        'Pyme': {
            'P25': 1331847,
            'P50': 1400000,
            'P75': 1645500,
            'Promedio': 1486906,
            'Count': 14
        }
    },
    'salario_jefe_salon': {
        'nombre': 'Jefe Salon',
        'Grande': {
            'P25': 1889762,
            'P50': 2040000,
            'P75': 2117500,
            'Promedio': 1967262,
            'Count': 4
        },
        'Pyme': {
            'P25': 1746875,
            'P50': 1781250,
            'P75': 1815625,
            'Promedio': 1781250,
            'Count': 2
        }
    },
    'salario_jefe_creditos_cobranzas': {
        'nombre': 'Jefe Creditos Cobranzas',
        'Grande': {
            'P25': 2600000,
            'P50': 2600000,
            'P75': 3567749,
            'Promedio': 3056717,
            'Count': 3
        },
        'Pyme': {
            'P25': 2222790,
            'P50': 2516873,
            'P75': 2810955,
            'Promedio': 2516873,
            'Count': 3
        }
    },
    'salario_jefe_compras': {
        'nombre': 'Jefe Compras',
        'Grande': {
            'P25': 2787500,
            'P50': 3089000,
            'P75': 3883058,
            'Promedio': 3350740,
            'Count': 10
        },
        'Pyme': {
            'P25': 2785028,
            'P50': 3020918,
            'P75': 3600000,
            'Promedio': 3031042,
            'Count': 6
        }
    }
}

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

        # Selector de área funcional (clusterización actualizada - 15 áreas)
        areas = {
            'Todos los Cargos': cargos_disponibles,
            'Gerencia General': [c for c in cargos_disponibles if c in ['salario_ceo', 'salario_asistente_gg']],
            'Comercial': [c for c in cargos_disponibles if c in [
                'salario_director_comercial', 'salario_gerente_ventas', 'salario_jefe_ventas',
                'salario_ejecutivo_ventas', 'salario_analista_facturacion',
                'salario_atencion_cliente'
            ]],
            'Comercio Exterior': [c for c in cargos_disponibles if c in [
                'salario_gerente_comex', 'salario_responsable_comex', 'salario_asistente_comex'
            ]],
            'Turismo y Gastronomía': [c for c in cargos_disponibles if c in [
                'salario_jefe_hospitalidad', 'salario_guia_turismo', 'salario_jefe_alimentos_bebidas',
                'salario_chef_ejecutivo', 'salario_jefe_salon', 'salario_gerente_ops_hotel',
                'salario_jefe_recepcion_hotel', 'salario_recepcionista_hotel', 'salario_concierge'
            ]],
            'Administración y Finanzas': [c for c in cargos_disponibles if c in [
                'salario_director_admin_finanzas', 'salario_gerente_admin_conta', 'salario_jefe_admin_conta',
                'salario_analista_contabilidad', 'salario_jefe_impuestos', 'salario_analista_impuestos',
                'salario_jefe_finanzas', 'salario_analista_cuentas_pagar', 'salario_empleado_administrativo',
                'salario_jefe_creditos_cobranzas', 'salario_analista_cobranzas', 'salario_jefe_control_gestion',
                'salario_analista_control_gestion', 'salario_auditor_interno', 'salario_recepcionista'
            ]],
            'Operaciones': [c for c in cargos_disponibles if c in [
                'salario_director_operaciones', 'salario_gerente_planta', 'salario_jefe_produccion',
                'salario_ingeniero_procesos', 'salario_supervisor_produccion', 'salario_analista_produccion',
                'salario_jefe_bodega', 'salario_supervisor_bodega', 'salario_gerente_agricola',
                'salario_ingeniero_agronomo', 'salario_supervisor_fincas', 'salario_jefe_laboratorio',
                'salario_analista_laboratorio', 'salario_gerente_enologia'
            ]],
            'Supply Chain': [c for c in cargos_disponibles if c in [
                'salario_gerente_supply_chain', 'salario_jefe_planificacion', 'salario_jefe_logistica',
                'salario_analista_logistica', 'salario_supervisor_depositos', 'salario_jefe_compras',
                'salario_gerente_compras', 'salario_comprador_analista'
            ]],
            'Mantenimiento y Calidad': [c for c in cargos_disponibles if c in [
                'salario_gerente_mantenimiento', 'salario_jefe_mantenimiento', 'salario_supervisor_mantenimiento',
                'salario_tecnico_mantenimiento', 'salario_gerente_calidad', 'salario_jefe_calidad',
                'salario_analista_calidad', 'salario_tecnico_calidad'
            ]],
            'Higiene y Seguridad': [c for c in cargos_disponibles if c in [
                'salario_responsable_sustentabilidad', 'salario_gerente_seguridad', 'salario_jefe_seguridad',
                'salario_tecnico_seguridad'
            ]],
            'Ingeniería y Proyectos': [c for c in cargos_disponibles if c in [
                'salario_jefe_ingenieria', 'salario_ingeniero_proyectos', 'salario_asistente_proyecto',
                'salario_jefe_obra', 'salario_supervisor_obra'
            ]],
            'RRHH': [c for c in cargos_disponibles if c in [
                'salario_director_rrhh', 'salario_gerente_rrhh', 'salario_jefe_rrhh',
                'salario_responsable_liquidacion', 'salario_analista_admin_personal', 'salario_jefe_seleccion',
                'salario_analista_seleccion', 'salario_analista_capacitacion'
            ]],
            'IT': [c for c in cargos_disponibles if c in [
                'salario_director_it', 'salario_gerente_it', 'salario_jefe_desarrollo',
                'salario_programador', 'salario_analista_funcional', 'salario_jefe_redes',
                'salario_tecnico_redes', 'salario_jefe_soporte', 'salario_analista_helpdesk'
            ]],
            'Marketing': [c for c in cargos_disponibles if c in [
                'salario_gerente_marketing', 'salario_jefe_marketing', 'salario_analista_marketing',
                'salario_analista_ecommerce', 'salario_diseñador_grafico'
            ]],
            'Pasante': [c for c in cargos_disponibles if c in ['salario_pasante', 'salario_joven_profesional']],
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
        # PARCHE: Usar valores hardcodeados si es uno de los 5 puestos específicos
        if cargo_seleccionado in HARDCODED_STATS:
            # Obtener datos calculados correctamente para usar "General"
            cargo_data_calculado = stats.stats_por_cargo[cargo_seleccionado]

            cargo_data = {
                'nombre': HARDCODED_STATS[cargo_seleccionado]['nombre'],
                'stats': {
                    'Grande': HARDCODED_STATS[cargo_seleccionado]['Grande'],
                    'Pyme': HARDCODED_STATS[cargo_seleccionado]['Pyme'],
                    'General': cargo_data_calculado['stats']['General']  # Usar cálculo correcto
                }
            }
        else:
            cargo_data = stats.stats_por_cargo[cargo_seleccionado]

        cargo_stats = cargo_data['stats']

        # Título del cargo
        st.markdown(f"## {cargo_data['nombre']}")

        # Advertencia si hay pocas respuestas
        if cargo_stats.get('General') and cargo_stats['General']['Count'] < 5:
            st.warning(f"⚠️ Este cargo tiene solo {cargo_stats['General']['Count']} respuesta(s). Los datos pueden no ser representativos del mercado.")

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
            <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #ddd;'>
                <a href='https://www.identidadcentral.com' target='_blank' style='text-decoration: none;'>
                    <img src='https://www.identidadcentral.com/favicon.png' width='40' style='border-radius: 50%;'>
                </a>
                <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
                    Desarrollado por <a href='https://www.identidadcentral.com' target='_blank' style='color: #2563eb; text-decoration: none; font-weight: bold;'>Identidad Central</a>
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
