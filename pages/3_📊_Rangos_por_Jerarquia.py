"""
Página 3: Rangos Salariales por Jerarquía
Análisis comparativo de sueldos por nivel jerárquico: CEO, Director, Gerente, Jefe
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Configuración de página
st.set_page_config(
    page_title="Rangos por Jerarquía - Encuesta Salarial 2do Semestre 2025",
    page_icon="📊",
    layout="wide"
)

# Colores de Perfil Humano
COLORS = {
    'azul': '#2E5090',
    'verde': '#00A651',
    'rojo': '#ED1C24',
    'amarillo': '#FDB913',
    'gris': '#3D5A6C'
}

# Cargar datos
@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent
    csv_path = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    df = pd.read_csv(csv_path)
    return df

def format_currency(value):
    """Formatea valores monetarios"""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.0f}".replace(",", ".")

def calcular_estadisticas_jerarquia(df, categoria_tamano=None):
    """
    Calcula estadísticas por jerarquía (CEO, Director, Gerente, Jefe)
    """
    # Mapeo de cargos por jerarquía (nombres correctos según columnas del CSV)
    jerarquias = {
        'CEO': ['salario_ceo'],
        'DIRECTOR': [
            'salario_director_comercial',
            'salario_director_admin_finanzas',
            'salario_director_rrhh',
            'salario_director_operaciones',
            'salario_director_it'  # Corregido: era 'sistemas'
        ],
        'GERENTE': [
            'salario_gerente_ventas',
            'salario_gerente_admin_conta',  # Corregido: era 'admin'
            'salario_gerente_rrhh',
            'salario_gerente_planta',  # Corregido: era 'operaciones' y 'produccion'
            'salario_gerente_it',  # Corregido: era 'sistemas'
            'salario_gerente_marketing',
            'salario_gerente_supply_chain',  # Corregido: era 'logistica'
            'salario_gerente_enologia',
            'salario_gerente_agricola',
            'salario_gerente_compras',
            'salario_gerente_mantenimiento',
            'salario_gerente_calidad',
            'salario_gerente_comex',
            'salario_gerente_ops_hotel',
            'salario_gerente_seguridad'
        ],
        'JEFE': [
            'salario_jefe_ventas',
            'salario_jefe_admin_conta',  # Corregido
            'salario_jefe_rrhh',
            'salario_jefe_compras',
            'salario_jefe_desarrollo',  # Corregido: IT, era 'sistemas'
            'salario_jefe_marketing',
            'salario_jefe_produccion',
            'salario_jefe_logistica',
            'salario_jefe_finanzas',
            'salario_jefe_impuestos',
            'salario_jefe_creditos_cobranzas',
            'salario_jefe_control_gestion',
            'salario_jefe_bodega',
            'salario_jefe_laboratorio',
            'salario_jefe_planificacion',
            'salario_jefe_mantenimiento',
            'salario_jefe_calidad',
            'salario_jefe_seguridad',
            'salario_jefe_ingenieria',
            'salario_jefe_obra',
            'salario_jefe_seleccion',
            'salario_jefe_hospitalidad',
            'salario_jefe_alimentos_bebidas',
            'salario_jefe_salon',
            'salario_jefe_recepcion_hotel',
            'salario_jefe_redes',
            'salario_jefe_soporte'
        ]
    }

    resultados = {}

    # Filtrar por tamaño si se especifica
    df_filtrado = df.copy()
    if categoria_tamano:
        df_filtrado = df_filtrado[df_filtrado['categoria_tamano'] == categoria_tamano]

    for jerarquia, columnas in jerarquias.items():
        # Concatenar todos los salarios de esta jerarquía
        salarios = []
        for col in columnas:
            if col in df_filtrado.columns:
                valores = pd.to_numeric(df_filtrado[col], errors='coerce').dropna()
                # Filtrar valores > 0 (0 = dato faltante)
                valores = valores[valores > 0]
                salarios.extend(valores.tolist())

        if salarios:
            salarios_series = pd.Series(salarios)
            resultados[jerarquia] = {
                'P25': salarios_series.quantile(0.25),
                'P50': salarios_series.quantile(0.50),
                'P75': salarios_series.quantile(0.75),
                'Promedio': salarios_series.mean(),
                'Count': len(salarios)
            }

    return resultados

def main():
    st.title("📊 Rangos Salariales por Jerarquía")
    st.markdown("Análisis comparativo de sueldos por nivel jerárquico")
    st.markdown("---")

    # Cargar datos
    df = load_data()

    # Calcular estadísticas
    stats_grande = calcular_estadisticas_jerarquia(df, 'Grande')
    stats_pyme = calcular_estadisticas_jerarquia(df, 'Pyme')

    # ============ TABLA: EMPRESAS GRANDES ============
    st.markdown("## 🏢 Sueldo Bruto Mensual (Empresas Grandes)")
    st.markdown("**Grande 201 → 500+**")

    if stats_grande:
        # Crear DataFrame para tabla
        tabla_grande = []
        for jerarquia in ['CEO', 'DIRECTOR', 'GERENTE', 'JEFE']:
            if jerarquia in stats_grande:
                tabla_grande.append({
                    'Métrica': jerarquia,
                    'Percentil 25': format_currency(stats_grande[jerarquia]['P25']),
                    'Percentil 50': format_currency(stats_grande[jerarquia]['P50']),
                    'Percentil 75': format_currency(stats_grande[jerarquia]['P75']),
                    'Promedio': format_currency(stats_grande[jerarquia]['Promedio'])
                })

        df_tabla_grande = pd.DataFrame(tabla_grande)
        st.dataframe(df_tabla_grande, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ============ TABLA: EMPRESAS PYMES ============
    st.markdown("## 🏪 Sueldo Bruto Mensual (Empresas Pymes)")
    st.markdown("**Pyme 1 → 200**")

    if stats_pyme:
        # Crear DataFrame para tabla
        tabla_pyme = []
        for jerarquia in ['CEO', 'DIRECTOR', 'GERENTE', 'JEFE']:
            if jerarquia in stats_pyme:
                tabla_pyme.append({
                    'Métrica': jerarquia,
                    'Percentil 25': format_currency(stats_pyme[jerarquia]['P25']),
                    'Percentil 50': format_currency(stats_pyme[jerarquia]['P50']),
                    'Percentil 75': format_currency(stats_pyme[jerarquia]['P75']),
                    'Promedio': format_currency(stats_pyme[jerarquia]['Promedio'])
                })

        df_tabla_pyme = pd.DataFrame(tabla_pyme)
        st.dataframe(df_tabla_pyme, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ============ TABLA: COMPARATIVA GRANDE VS PYME ============
    st.markdown("## 📊 Grande V.S. Pyme")
    st.markdown("**Diferencia porcentual en Percentil 50 (Mediana)**")

    if stats_grande and stats_pyme:
        comparativa = []
        for jerarquia in ['CEO', 'DIRECTOR', 'GERENTE', 'JEFE']:
            if jerarquia in stats_grande and jerarquia in stats_pyme:
                p50_grande = stats_grande[jerarquia]['P50']
                p50_pyme = stats_pyme[jerarquia]['P50']

                if p50_pyme > 0:
                    diferencia_pct = ((p50_grande - p50_pyme) / p50_pyme) * 100
                    comparativa.append({
                        'Jerarquía': jerarquia,
                        'Diferencia %': f"{diferencia_pct:.0f}%"
                    })

        df_comparativa = pd.DataFrame(comparativa)

        # Mostrar como tabla horizontal
        st.dataframe(
            df_comparativa.set_index('Jerarquía').T,
            use_container_width=True
        )

    st.markdown("---")

    # ============ GRÁFICO COMPARATIVO ============
    st.markdown("## 📈 Visualización Comparativa: Grande vs Pyme")

    if stats_grande and stats_pyme:
        jerarquias_orden = ['CEO', 'DIRECTOR', 'GERENTE', 'JEFE']

        fig = go.Figure()

        # Agregar barras para cada percentil
        for percentil in ['P25', 'P50', 'P75']:
            valores_grande = []
            valores_pyme = []

            for jer in jerarquias_orden:
                if jer in stats_grande:
                    valores_grande.append(stats_grande[jer][percentil])
                else:
                    valores_grande.append(0)

                if jer in stats_pyme:
                    valores_pyme.append(stats_pyme[jer][percentil])
                else:
                    valores_pyme.append(0)

            # Barras para Empresas Grandes
            fig.add_trace(go.Bar(
                name=f'Grande {percentil}',
                x=jerarquias_orden,
                y=valores_grande,
                marker_color=COLORS['azul'],
                opacity=0.9 if percentil == 'P50' else 0.6,
                text=[format_currency(v) for v in valores_grande],
                textposition='auto',
                showlegend=(percentil == 'P50')
            ))

        fig.update_layout(
            title="Comparativa Salarial: Percentil 50 (Mediana)",
            xaxis_title="Jerarquía",
            yaxis_title="Salario Bruto Mensual ($)",
            barmode='group',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ============ MÉTRICAS DESTACADAS ============
    st.markdown("## 🎯 Insights Destacados")

    col1, col2, col3, col4 = st.columns(4)

    if stats_grande and 'CEO' in stats_grande:
        with col1:
            st.metric(
                label="CEO Grande (P50)",
                value=format_currency(stats_grande['CEO']['P50']),
                delta=f"{stats_grande['CEO']['Count']} empresas"
            )

    if stats_pyme and 'CEO' in stats_pyme:
        with col2:
            st.metric(
                label="CEO Pyme (P50)",
                value=format_currency(stats_pyme['CEO']['P50']),
                delta=f"{stats_pyme['CEO']['Count']} empresas"
            )

    if stats_grande and 'GERENTE' in stats_grande:
        with col3:
            st.metric(
                label="Gerente Grande (P50)",
                value=format_currency(stats_grande['GERENTE']['P50']),
                delta=f"{stats_grande['GERENTE']['Count']} respuestas"
            )

    if stats_pyme and 'GERENTE' in stats_pyme:
        with col4:
            st.metric(
                label="Gerente Pyme (P50)",
                value=format_currency(stats_pyme['GERENTE']['P50']),
                delta=f"{stats_pyme['GERENTE']['Count']} respuestas"
            )

    st.markdown("---")

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem 0;'>
            <p><strong>Perfil Humano</strong> - Encuesta Salarial 2do Semestre 2025 (10ma Edición)</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
