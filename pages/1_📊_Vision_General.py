"""
Página 1: Visión General de la Encuesta Salarial
Análisis agregado de participación, aumentos, beneficios y tendencias
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Configuración de página
st.set_page_config(
    page_title="Visión General - Encuesta Salarial 2do Semestre 2025",
    page_icon="📊",
    layout="wide"
)

# Colores vibrantes de Perfil Humano
COLORS = {
    'azul': '#2E5090',
    'verde': '#00A651',
    'rojo': '#ED1C24',
    'amarillo': '#FDB913',
    'naranja': '#F68B1F',
    'violeta': '#8E44AD',
    'gris': '#3D5A6C'
}

# Paleta vibrante para gráficos
COLOR_PALETTE = ['#ED1C24', '#00A651', '#FDB913', '#2E5090', '#F68B1F',
                 '#8E44AD', '#3498DB', '#E74C3C', '#2ECC71', '#F39C12']

# Cargar datos
@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent
    csv_path = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    df = pd.read_csv(csv_path)
    return df

def acortar_texto(texto, max_len=30):
    """Acorta textos largos para mejor visualización"""
    if pd.isna(texto):
        return texto
    texto = str(texto)
    if len(texto) > max_len:
        return texto[:max_len-3] + '...'
    return texto

def main():
    st.title("📊 Visión General de la Encuesta")
    st.markdown("Análisis agregado de participación, proyecciones y beneficios")
    st.markdown("---")

    # Cargar datos
    df = load_data()

    # Sidebar con filtros
    with st.sidebar:
        st.header("🔍 Filtros")

        # Filtro por tamaño
        if 'categoria_tamano' in df.columns:
            tamanos_disponibles = ['Todos'] + sorted(df['categoria_tamano'].dropna().unique().tolist())
            filtro_tamano = st.selectbox(
                "Tamaño de Empresa",
                tamanos_disponibles,
                help="Filtra empresas por cantidad de empleados"
            )
        else:
            filtro_tamano = 'Todos'

        # Filtro por rubro - usar versión corta si existe
        rubro_col = 'rubro_corto' if 'rubro_corto' in df.columns else 'rubro'
        if rubro_col in df.columns:
            rubros_disponibles = ['Todos'] + sorted(df[rubro_col].dropna().unique().tolist())
            filtro_rubro = st.selectbox(
                "Rubro",
                rubros_disponibles,
                help="Filtra empresas por sector de actividad"
            )
        else:
            filtro_rubro = 'Todos'

        st.markdown("---")
        st.info("💡 Los filtros se aplicarán a todas las visualizaciones de esta página.")

    # Aplicar filtros
    df_filtered = df.copy()

    if filtro_tamano != 'Todos':
        df_filtered = df_filtered[df_filtered['categoria_tamano'] == filtro_tamano]

    if filtro_rubro != 'Todos':
        df_filtered = df_filtered[df_filtered[rubro_col] == filtro_rubro]

    # Mostrar información de filtros aplicados
    if filtro_tamano != 'Todos' or filtro_rubro != 'Todos':
        st.success(f"📌 Mostrando datos para: **{len(df_filtered)}** empresas (de {len(df)} total)")

    # ============ SECCIÓN 1: PARTICIPACIÓN ============
    st.markdown("## 📍 Participación en la Encuesta")

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de rubros mejorado
        if rubro_col in df_filtered.columns:
            st.markdown("### Clasificación por Rubro")

            rubro_counts = df_filtered[rubro_col].value_counts().reset_index()
            rubro_counts.columns = ['Rubro', 'Cantidad']

            # Tomar solo top 10 rubros
            rubro_counts = rubro_counts.head(10)

            fig_rubro = px.pie(
                rubro_counts,
                values='Cantidad',
                names='Rubro',
                title='Distribución por Rubro de Empresa',
                color_discrete_sequence=COLOR_PALETTE,
                hole=0.3  # Donut chart
            )
            fig_rubro.update_traces(
                textinfo='none',  # Sin labels visibles
                hovertemplate='<b>%{label}</b><br>Empresas: %{value}<br>Porcentaje: %{percent}<extra></extra>',
                marker=dict(line=dict(color='white', width=2))
            )
            fig_rubro.update_layout(
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )

            st.plotly_chart(fig_rubro, use_column_width=True)

    with col2:
        # Gráfico de tamaños mejorado
        if 'categoria_tamano' in df_filtered.columns:
            st.markdown("### Clasificación por Tamaño")

            tamano_counts = df_filtered['categoria_tamano'].value_counts().reset_index()
            tamano_counts.columns = ['Tamaño', 'Cantidad']

            colors_tamano = {
                'Grande': COLORS['azul'],
                'Pyme': COLORS['verde'],
                'Otro': COLORS['gris']
            }

            fig_tamano = px.pie(
                tamano_counts,
                values='Cantidad',
                names='Tamaño',
                title='Distribución por Tamaño de Empresa',
                color='Tamaño',
                color_discrete_map=colors_tamano,
                hole=0.3
            )
            fig_tamano.update_traces(
                textinfo='none',  # Sin labels visibles
                hovertemplate='<b>%{label}</b><br>Empresas: %{value}<br>Porcentaje: %{percent}<extra></extra>',
                marker=dict(line=dict(color='white', width=2))
            )
            fig_tamano.update_layout(
                height=500,
                showlegend=True
            )

            st.plotly_chart(fig_tamano, use_column_width=True)

    st.markdown("---")

    # ============ SECCIÓN 2: AUMENTOS SALARIALES ============
    st.markdown("## 💰 Proyecciones de Aumentos Salariales 2025")

    col1, col2 = st.columns(2)

    with col1:
        if 'aumento_salarial_2025_pct' in df_filtered.columns:
            st.markdown("### % de Aumento Estimado para 2025")

            aumentos = df_filtered['aumento_salarial_2025_pct'].dropna()
            aumento_counts = aumentos.value_counts().reset_index()
            aumento_counts.columns = ['Rango', 'Cantidad']

            # Ordenar por rango y acortar textos largos
            order = ['< 6%', '6 - 10 %', '11 - 15%', '16 - 20 %', '21 - 25%', '26 - 30%',
                     '31 - 35%', '36 - 40%', '41 - 45%', '46 - 50%', '51 - 55%',
                     '56 - 60%', '> 60%', 'No tenemos definido el aumento total para el 2025 (lo veremos mes a mes)']

            # Acortar la opción larga
            aumento_counts['Rango'] = aumento_counts['Rango'].replace({
                'No tenemos definido el aumento total para el 2025 (lo veremos mes a mes)': 'Sin definir'
            })

            aumento_counts['order'] = aumento_counts['Rango'].apply(
                lambda x: order.index(x) if x in order else (order.index('No tenemos definido el aumento total para el 2025 (lo veremos mes a mes)') if x == 'Sin definir' else 999)
            )
            aumento_counts = aumento_counts.sort_values('order').head(10)

            fig_aumentos = px.bar(
                aumento_counts,
                x='Rango',
                y='Cantidad',
                title='Distribución de Aumentos Proyectados',
                color='Cantidad',
                color_continuous_scale=['#FDB913', '#ED1C24']
            )
            fig_aumentos.update_traces(
                hovertemplate='<b>%{x}</b><br>Empresas: %{y}<br>Porcentaje: %{y:.1f}%<extra></extra>'
            )
            fig_aumentos.update_layout(
                xaxis_tickangle=0,
                height=450,
                showlegend=False,
                xaxis_title="Rango de Aumento",
                yaxis_title="Número de Empresas"
            )
            # Wrap x labels
            fig_aumentos.update_xaxes(tickmode='linear')

            st.plotly_chart(fig_aumentos, use_column_width=True)

    with col2:
        if 'cantidad_aumentos_2025' in df_filtered.columns:
            st.markdown("### Cantidad de Aumentos Estimados en el Año")

            cant_aumentos = df_filtered['cantidad_aumentos_2025'].dropna()
            cant_counts = cant_aumentos.value_counts().reset_index()
            cant_counts.columns = ['Cantidad', 'Empresas']

            # Acortar textos largos
            cant_counts['Cantidad'] = cant_counts['Cantidad'].apply(lambda x: acortar_texto(str(x), 25))

            fig_cant = px.pie(
                cant_counts,
                values='Empresas',
                names='Cantidad',
                title='Número de Aumentos Planificados',
                color_discrete_sequence=COLOR_PALETTE,
                hole=0.3
            )
            fig_cant.update_traces(
                textinfo='none',  # Sin labels visibles
                hovertemplate='<b>%{label}</b><br>Empresas: %{value}<br>Porcentaje: %{percent}<extra></extra>',
                marker=dict(line=dict(color='white', width=2))
            )
            fig_cant.update_layout(height=450)

            st.plotly_chart(fig_cant, use_column_width=True)

    st.markdown("---")

    # ============ SECCIÓN 3: ROTACIÓN ============
    st.markdown("## 🔄 Rotación de Personal")

    if 'rotacion_2025_pct' in df_filtered.columns:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            rotacion = df_filtered['rotacion_2025_pct'].dropna()
            rot_counts = rotacion.value_counts().head(8).reset_index()
            rot_counts.columns = ['Rango', 'Cantidad']

            # Acortar textos largos
            rot_counts['Rango_corto'] = rot_counts['Rango'].apply(lambda x: acortar_texto(str(x), 20))

            # ORIENTACIÓN HORIZONTAL para mejor legibilidad
            fig_rot = px.bar(
                rot_counts,
                y='Rango_corto',
                x='Cantidad',
                title='Distribución del % de Rotación (Enero-Agosto 2025)',
                color='Cantidad',
                color_continuous_scale=['#00A651', '#2E5090'],
                orientation='h'  # HORIZONTAL
            )
            fig_rot.update_traces(
                hovertemplate='<b>%{y}</b><br>Empresas: %{x}<extra></extra>'
            )
            fig_rot.update_layout(
                xaxis_title="Número de Empresas",
                yaxis_title="Rango de Rotación",
                height=450,
                showlegend=False
            )

            st.plotly_chart(fig_rot, use_column_width=True)

    st.markdown("---")

    # ============ SECCIÓN 4: PROYECCIONES DE EMPLEO ============
    st.markdown("## 📈 Proyecciones de Empleo")

    col1, col2 = st.columns(2)

    with col1:
        if 'prevision_incorporacion' in df_filtered.columns:
            st.markdown("### ⬆️ Incorporación de Nuevos Puestos")

            incorp = df_filtered['prevision_incorporacion'].dropna()
            incorp_counts = incorp.value_counts().reset_index()
            incorp_counts.columns = ['Respuesta', 'Cantidad']

            # Acortar respuestas largas
            incorp_counts['Respuesta_corta'] = incorp_counts['Respuesta'].apply(lambda x: acortar_texto(str(x), 25))

            # ORIENTACIÓN HORIZONTAL
            fig_incorp = px.bar(
                incorp_counts,
                y='Respuesta_corta',
                x='Cantidad',
                title='¿Planea incorporar nuevos puestos?',
                color='Cantidad',
                color_continuous_scale=['#00A651', '#2E5090'],
                orientation='h'
            )
            fig_incorp.update_traces(
                hovertemplate='<b>%{y}</b><br>Empresas: %{x}<extra></extra>'
            )
            fig_incorp.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Número de Empresas",
                yaxis_title=""
            )

            st.plotly_chart(fig_incorp, use_column_width=True)

    with col2:
        if 'prevision_reduccion' in df_filtered.columns:
            st.markdown("### ⬇️ Reducción de Puestos")

            reduc = df_filtered['prevision_reduccion'].dropna()
            reduc_counts = reduc.value_counts().reset_index()
            reduc_counts.columns = ['Respuesta', 'Cantidad']

            # Acortar respuestas largas
            reduc_counts['Respuesta_corta'] = reduc_counts['Respuesta'].apply(lambda x: acortar_texto(str(x), 25))

            # ORIENTACIÓN HORIZONTAL
            fig_reduc = px.bar(
                reduc_counts,
                y='Respuesta_corta',
                x='Cantidad',
                title='¿Planea reducir puestos?',
                color='Cantidad',
                color_continuous_scale=['#ED1C24', '#FDB913'],
                orientation='h'
            )
            fig_reduc.update_traces(
                hovertemplate='<b>%{y}</b><br>Empresas: %{x}<extra></extra>'
            )
            fig_reduc.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Número de Empresas",
                yaxis_title=""
            )

            st.plotly_chart(fig_reduc, use_column_width=True)

    st.markdown("---")

    # ============ SECCIÓN 5: BENEFICIOS ============
    st.markdown("## 🎁 Beneficios Ofrecidos")

    tab1, tab2 = st.tabs(["💵 Beneficios Monetarios", "⏰ Beneficios de Tiempo"])

    with tab1:
        st.markdown("### Beneficios Monetarios más Comunes")

        # SOLO beneficios monetarios (que NO son de tiempo)
        benef_monetarios_nombres = ['medicina_prepaga', 'reintegro_medicamentos', 'prestamos',
                                    'almuerzo', 'gimnasio', 'gift_card', 'red_descuentos',
                                    'descuento_productos', 'combustible', 'cochera',
                                    'auto_gerentes', 'auto_vendedores', 'gastos_auto',
                                    'tarjeta_credito', 'colegio', 'pension', 'pago_dolares',
                                    'posgrados', 'coaching', 'idiomas', 'internet']

        benef_cols = [col for col in df_filtered.columns
                      if col.startswith('benef_') and
                      any(mon in col for mon in benef_monetarios_nombres)]

        if benef_cols:
            benef_data = []

            for col in benef_cols:
                if col not in df_filtered.columns:
                    continue

                # Filtrar valores que son headers (con emojis)
                valores = df_filtered[col].dropna()
                valores = valores[~valores.str.contains('💵|⏰', na=False)]

                if len(valores) == 0:
                    continue

                # Contar diferentes formas de "Si"
                si_count = 0
                if 'medicina_prepaga' in col:
                    # Para medicina prepaga: contar "Otorgamos..." como Si
                    si_count = valores.str.contains('Otorgamos', case=False, na=False).sum()
                else:
                    # Para otros: contar "Si"
                    si_count = (valores == 'Si').sum()

                total = len(valores)

                if total > 0 and si_count > 0:
                    pct = (si_count / total) * 100
                    benef_name = col.replace('benef_', '').replace('_', ' ').title()
                    benef_data.append({
                        'Beneficio': benef_name[:30],  # Acortar
                        'Porcentaje': pct,
                        'Empresas': si_count
                    })

            if benef_data:
                df_benef = pd.DataFrame(benef_data)
                df_benef = df_benef.sort_values('Porcentaje', ascending=True)  # Mostrar TODOS

                fig_benef = px.bar(
                    df_benef,
                    x='Porcentaje',
                    y='Beneficio',
                    orientation='h',
                    title='% de Empresas que Ofrecen cada Beneficio',
                    color='Porcentaje',
                    color_continuous_scale=['#FDB913', '#00A651'],
                    custom_data=['Empresas']
                )
                fig_benef.update_traces(
                    hovertemplate='<b>%{y}</b><br>Empresas: %{customdata[0]}<br>Porcentaje: %{x:.1f}%<extra></extra>'
                )
                # Altura dinámica basada en cantidad de beneficios
                altura = max(450, len(df_benef) * 30)
                fig_benef.update_layout(
                    height=altura,
                    showlegend=False,
                    xaxis_title="Porcentaje de Empresas",
                    yaxis_title=""
                )

                st.plotly_chart(fig_benef, use_column_width=True)
        else:
            st.info("No hay datos de beneficios disponibles con los filtros actuales")

    with tab2:
        st.markdown("### Beneficios de Tiempo más Comunes")

        # SOLO beneficios de tiempo
        benef_tiempo_nombres = ['vacaciones_adicionales', 'home_office', 'dia_flex',
                                'cumpleanos', 'maternidad', 'paternidad',
                                'after_office', 'integracion']

        benef_tiempo_cols = [col for col in df_filtered.columns
                             if col.startswith('benef_') and
                             any(tiempo in col for tiempo in benef_tiempo_nombres)]

        if benef_tiempo_cols:
            benef_tiempo_data = []

            for col in benef_tiempo_cols:
                if col not in df_filtered.columns:
                    continue

                # Filtrar valores que son headers (con emojis)
                valores = df_filtered[col].dropna()
                valores = valores[~valores.str.contains('💵|⏰', na=False)]

                if len(valores) == 0:
                    continue

                # Contar "Si"
                si_count = (valores == 'Si').sum()
                total = len(valores)

                if total > 0 and si_count > 0:
                    pct = (si_count / total) * 100
                    benef_name = col.replace('benef_', '').replace('_', ' ').title()
                    benef_tiempo_data.append({
                        'Beneficio': benef_name[:30],
                        'Porcentaje': pct,
                        'Empresas': si_count
                    })

            if benef_tiempo_data:
                df_benef_tiempo = pd.DataFrame(benef_tiempo_data)
                df_benef_tiempo = df_benef_tiempo.sort_values('Porcentaje', ascending=True)  # Mostrar TODOS

                fig_benef_tiempo = px.bar(
                    df_benef_tiempo,
                    x='Porcentaje',
                    y='Beneficio',
                    orientation='h',
                    title='% de Empresas que Ofrecen cada Beneficio',
                    color='Porcentaje',
                    color_continuous_scale=['#2E5090', '#00A651'],
                    custom_data=['Empresas']
                )
                fig_benef_tiempo.update_traces(
                    hovertemplate='<b>%{y}</b><br>Empresas: %{customdata[0]}<br>Porcentaje: %{x:.1f}%<extra></extra>'
                )
                # Altura dinámica basada en cantidad de beneficios
                altura_tiempo = max(450, len(df_benef_tiempo) * 30)
                fig_benef_tiempo.update_layout(
                    height=altura_tiempo,
                    showlegend=False,
                    xaxis_title="Porcentaje de Empresas",
                    yaxis_title=""
                )

                st.plotly_chart(fig_benef_tiempo, use_column_width=True)
        else:
            st.info("No hay datos de beneficios de tiempo disponibles con los filtros actuales")

    st.markdown("---")

    # ============ SECCIÓN 6: BONIFICACIONES ============
    st.markdown("## 🎁 Bonificaciones por Nivel Jerárquico")
    st.markdown("Los bonus están expresados en cantidad de sueldos mensuales")

    # Columnas de bonus
    bonus_cols = {
        'Gerente General': '🎁 Bonus GERENTE GENERAL (Los bonus estan expresados en cantidad de sueldos mensuales)',
        'Directores': 'bonus_directores',
        'Gerentes': 'bonus_gerentes',
        'Jefes': 'bonus_jefes',
        'Supervisores': 'bonus_supervisores',
        'Analistas': 'bonus_analistas'
    }

    # Función para extraer número de texto como "4 sueldos", "1,5 sueldos", etc.
    def extraer_numero_bonus(texto):
        import re
        if pd.isna(texto):
            return None
        texto = str(texto).lower()
        # Si dice "no tenemos asignado", retornar 0
        if 'no tenemos asignado' in texto:
            return 0
        # Buscar patrones como "4 sueldos", "1,5 sueldos", "1/2 sueldo"
        # Primero buscar fracciones como 1/2
        match_fraccion = re.search(r'(\d+)/(\d+)', texto)
        if match_fraccion:
            numerador = float(match_fraccion.group(1))
            denominador = float(match_fraccion.group(2))
            return numerador / denominador
        # Buscar números decimales con coma o punto
        match = re.search(r'(\d+[,.]?\d*)', texto)
        if match:
            numero = match.group(1).replace(',', '.')
            return float(numero)
        return None

    # Verificar si existen las columnas de bonus
    bonus_data = []
    for nivel, col_name in bonus_cols.items():
        if col_name in df_filtered.columns:
            # Obtener valores y convertir de texto a número
            valores_raw = df_filtered[col_name].dropna()
            bonus_values = valores_raw.apply(extraer_numero_bonus).dropna()
            # Filtrar los 0 (no asignado) para el cálculo de estadísticas
            bonus_values_sin_cero = bonus_values[bonus_values > 0]

            if len(bonus_values_sin_cero) > 0:
                bonus_data.append({
                    'Nivel': nivel,
                    'Promedio': bonus_values_sin_cero.mean(),
                    'Mediana (P50)': bonus_values_sin_cero.median(),
                    'Mínimo': bonus_values_sin_cero.min(),
                    'Máximo': bonus_values_sin_cero.max(),
                    'Empresas': len(bonus_values_sin_cero),
                    'Sin Bonus': (bonus_values == 0).sum()
                })

    if bonus_data:
        col1, col2 = st.columns(2)

        with col1:
            # Tabla de bonificaciones
            df_bonus = pd.DataFrame(bonus_data)
            df_bonus['Promedio'] = df_bonus['Promedio'].apply(lambda x: f"{x:.1f}")
            df_bonus['Mediana (P50)'] = df_bonus['Mediana (P50)'].apply(lambda x: f"{x:.1f}")
            df_bonus['Mínimo'] = df_bonus['Mínimo'].apply(lambda x: f"{x:.1f}")
            df_bonus['Máximo'] = df_bonus['Máximo'].apply(lambda x: f"{x:.1f}")

            st.markdown("### Estadísticas de Bonificaciones")
            st.dataframe(df_bonus, use_container_width=True, hide_index=True)

        with col2:
            # Gráfico de barras
            df_bonus_plot = pd.DataFrame(bonus_data)

            fig_bonus = px.bar(
                df_bonus_plot,
                x='Nivel',
                y='Promedio',
                title='Promedio de Bonificaciones por Nivel Jerárquico',
                color='Promedio',
                color_continuous_scale=['#FDB913', '#ED1C24'],
                custom_data=['Empresas', 'Mediana (P50)']
            )
            fig_bonus.update_traces(
                hovertemplate='<b>%{x}</b><br>Promedio: %{y:.1f} sueldos<br>Mediana: %{customdata[1]:.1f} sueldos<br>Empresas: %{customdata[0]}<extra></extra>'
            )
            fig_bonus.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Nivel Jerárquico",
                yaxis_title="Cantidad de Sueldos Mensuales"
            )

            st.plotly_chart(fig_bonus, use_container_width=True)

        # Métricas destacadas
        st.markdown("### 📊 Bonificaciones Destacadas")
        cols = st.columns(len(bonus_data))
        for idx, row in enumerate(bonus_data):
            with cols[idx]:
                st.metric(
                    label=row['Nivel'],
                    value=f"{row['Promedio']:.1f} sueldos",
                    delta=f"{row['Empresas']} empresas"
                )
    else:
        st.info("No hay datos de bonificaciones disponibles con los filtros actuales")

    st.markdown("---")

    # Footer
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem 0;'>
            <p><strong>Perfil Humano</strong> - Encuesta Salarial 2do Semestre 2025 (10ma Edición)</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
