"""
Dashboard Interactivo - Encuesta Salarial 1er Semestre 2025
Perfil Humano - 9na Edición
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Encuesta Salarial 2025 - Perfil Humano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar CSS personalizado
def load_css():
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #2E5090;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #00A651;
            font-weight: 600;
            margin-top: 1.5rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 5px solid #2E5090;
        }
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

# Cargar logos
def load_logos():
    base_path = Path(__file__).parent
    logos = {}
    for logo_file in ['logo1.jpeg', 'logo2.jpeg', 'logo3.png']:
        logo_path = base_path / 'assets' / 'logos' / logo_file
        if logo_path.exists():
            logos[logo_file] = str(logo_path)
    return logos

# Cargar datos
@st.cache_data
def load_data():
    base_path = Path(__file__).parent
    csv_path = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    df = pd.read_csv(csv_path)
    return df

def main():
    load_css()

    # Header con logos
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<p class="main-header">📊 Encuesta Salarial</p>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #3D5A6C;">1er Semestre 2025 - 9na Edición</p>', unsafe_allow_html=True)

    # Cargar logos si existen
    logos = load_logos()
    if logos:
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if 'logo1.jpeg' in logos:
                st.image(logos['logo1.jpeg'], use_column_width=True)

    st.markdown("---")

    # Descripción
    st.markdown("""
    ### Bienvenido al Dashboard Interactivo de la Encuesta Salarial

    Esta herramienta te permite explorar de manera interactiva los resultados de la **9na Edición** de la
    Encuesta Salarial realizada por **Perfil Humano** en el 1er Semestre de 2025.

    #### 📌 ¿Qué encontrarás?

    **👈 Navegá por las secciones en el menú lateral:**

    - **📊 Visión General**: Análisis agregado de la encuesta
      - Participación por rubro y tamaño de empresa
      - Proyecciones de aumentos salariales 2025
      - Rotación de personal
      - Beneficios monetarios y de tiempo
      - Bonificaciones por nivel jerárquico

    - **👤 Análisis por Cargo**: Estadísticas detalladas de cada posición
      - Percentiles salariales (P25, P50, P75)
      - Comparativa Grande vs Pyme
      - Distribución de respuestas por tamaño
      - Descripción de responsabilidades

    #### 📈 Características del Dashboard

    - **Filtros Inteligentes**: Segmenta la información por rubro, tamaño de empresa, y más
    - **Visualizaciones Interactivas**: Gráficos dinámicos con Plotly
    - **Comparativas**: Analiza diferencias entre empresas grandes y pymes
    - **Exportación**: Descarga reportes personalizados

    ---
    """)

    # Cargar datos para mostrar estadísticas generales
    df = load_data()

    # Métricas principales
    st.markdown('<p class="sub-header">📊 Estadísticas de Participación</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total de Empresas",
            value=f"{len(df):,}",
            delta="Participantes"
        )

    with col2:
        if 'rubro' in df.columns:
            n_rubros = df['rubro'].nunique()
            st.metric(
                label="Rubros Representados",
                value=n_rubros,
                delta="Sectores"
            )

    with col3:
        if 'categoria_tamano' in df.columns:
            pct_grande = (df['categoria_tamano'] == 'Grande').sum() / len(df) * 100
            st.metric(
                label="Empresas Grandes",
                value=f"{pct_grande:.1f}%",
                delta="200+ empleados"
            )

    with col4:
        if 'categoria_tamano' in df.columns:
            pct_pyme = (df['categoria_tamano'] == 'Pyme').sum() / len(df) * 100
            st.metric(
                label="Empresas Pyme",
                value=f"{pct_pyme:.1f}%",
                delta="1-200 empleados"
            )

    st.markdown("---")

    # Instrucciones finales
    st.info("""
    👉 **Para comenzar tu análisis**, selecciona una de las secciones en el menú lateral izquierdo.
    """)

    st.markdown("---")

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem 0;'>
            <p><strong>Perfil Humano - Búsquedas Estratégicas</strong></p>
            <p>Encuesta Salarial 1er Semestre 2025 (9na Edición)</p>
            <p style='font-size: 0.9rem;'>Dashboard interactivo desarrollado con Streamlit</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
