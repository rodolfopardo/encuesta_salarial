"""
Dashboard Interactivo - Encuesta Salarial 1er Semestre 2025
Perfil Humano - 9na Edición
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Encuesta Salarial 2do Semestre 2025 - Perfil Humano",
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
        /* Personalizar el título del sidebar */
        [data-testid="stSidebarNav"] {
            padding-top: 2rem;
        }
        [data-testid="stSidebarNav"]::before {
            content: "Perfil Humano";
            display: block;
            font-size: 1.5rem;
            font-weight: bold;
            color: #2E5090;
            padding: 1rem 1rem 0.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        /* Ocultar todos los posibles elementos que contengan "app" */
        [data-testid="stSidebarNav"] > ul > li:first-child,
        [data-testid="stSidebarNav"] ul li:first-child,
        [data-testid="stSidebarNav"] a:first-child,
        section[data-testid="stSidebar"] > div:first-child {
            display: none !important;
        }
        /* Ocultar elemento padre del primer link */
        [data-testid="stSidebarNav"] > div > ul > li:first-child {
            display: none !important;
        }
        </style>
        <script>
        // Función más agresiva para ocultar "app"
        function hideAppLabel() {
            // Buscar en todo el sidebar
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (!sidebar) return;

            // Buscar todos los elementos de texto
            const walker = document.createTreeWalker(
                sidebar,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );

            let node;
            while(node = walker.nextNode()) {
                if (node.textContent.trim().toLowerCase() === 'app') {
                    // Ocultar el elemento padre
                    let parent = node.parentElement;
                    while (parent && parent !== sidebar) {
                        if (parent.tagName === 'A' || parent.tagName === 'LI' || parent.tagName === 'DIV') {
                            parent.style.display = 'none';
                            break;
                        }
                        parent = parent.parentElement;
                    }
                }
            }
        }

        // Ejecutar inmediatamente y cada 500ms
        hideAppLabel();
        setInterval(hideAppLabel, 500);

        // También ejecutar cuando cambie el DOM
        const observer = new MutationObserver(hideAppLabel);
        observer.observe(document.body, { childList: true, subtree: true });
        </script>
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
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #3D5A6C;">2do Semestre 2025 - 10ma Edición</p>', unsafe_allow_html=True)

    # Cargar logos si existen
    logos = load_logos()
    if logos:
        col_left, col_center, col_right = st.columns([1, 2, 1])
        with col_center:
            if 'logo1.jpeg' in logos:
                st.image(logos['logo1.jpeg'], use_column_width=True)

    st.markdown("---")

    # Información sobre la encuesta anónima
    st.markdown("""
    <div style='background-color: #F0F2F6; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2E5090; margin-bottom: 2rem;'>
        <h3 style='color: #2E5090; margin-top: 0;'>📋 Sobre esta Encuesta</h3>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
            Esta encuesta salarial es de carácter <strong>ANÓNIMA, CONFIDENCIAL y GRATUITA</strong>.
        </p>
        <p style='font-size: 1rem; line-height: 1.6;'>
            Tiene como objetivo poder analizar y comparar los salarios de puestos Directivos,
            Gerenciales, Jefaturas y Analistas de las diferentes empresas de CUYO en los
            diferentes rubros, tamaños y sectores.
        </p>
        <p style='font-size: 1rem; line-height: 1.6;'>
            Estas empresas también participan de un grupo de WhatsApp donde intercambian
            conocimientos, experiencias e información. <strong>Si querés ser parte contactanos.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sección de contacto y servicios
    st.markdown("""
    <div style='background-color: #E8F4F0; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #00A651; margin-bottom: 2rem;'>
        <h3 style='color: #00A651; margin-top: 0;'>💼 ¿Te gustaría recibir asesoramiento en cómo diseñar una estrategia salarial?</h3>
        <ul style='font-size: 1rem; line-height: 1.8;'>
            <li>Análisis de Equidad salarial interna</li>
            <li>Análisis de Competitividad externa</li>
            <li>Estrategia de Pago para puestos Claves</li>
            <li>Desarrollo de un plan de Beneficios</li>
        </ul>
        <p style='font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 1rem;'><strong>Contactanos por WhatsApp:</strong></p>
        <div style='display: flex; gap: 1rem; flex-wrap: wrap;'>
            <a href='https://wa.me/5492615103396?text=Hola%20Lorena,%20me%20interesa%20recibir%20asesoramiento%20sobre%20estrategia%20salarial'
               target='_blank'
               style='display: inline-flex; align-items: center; gap: 0.5rem; background-color: #25D366; color: white; padding: 0.8rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1rem; transition: all 0.3s;'>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                Lorena Henriquez
            </a>
            <a href='https://wa.me/5492616933163?text=Hola%20Gastón,%20me%20interesa%20recibir%20asesoramiento%20sobre%20estrategia%20salarial'
               target='_blank'
               style='display: inline-flex; align-items: center; gap: 0.5rem; background-color: #25D366; color: white; padding: 0.8rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 1rem; transition: all 0.3s;'>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                </svg>
                Gastón Kovalenko
            </a>
        </div>
        <p style='font-size: 0.9rem; margin-top: 1rem; color: #666;'>
            📧 También por email:
            <a href='mailto:lorena.henriquez@perfil-humano.com' style='color: #2E5090;'>lorena.henriquez@perfil-humano.com</a> |
            <a href='mailto:gaston.kovalenko@perfil-humano.com' style='color: #2E5090;'>gaston.kovalenko@perfil-humano.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Descripción
    st.markdown("""
    ### Bienvenido al Dashboard Interactivo de la Encuesta Salarial

    Esta herramienta te permite explorar de manera interactiva los resultados de la **10ma Edición** de la
    Encuesta Salarial realizada por **Perfil Humano** en el 2do Semestre de 2025.

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
            <p>Encuesta Salarial 2do Semestre 2025 (10ma Edición)</p>
            <p style='font-size: 0.9rem;'>Desarrollado por Rodolfo Pardo para Perfil Humano</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
