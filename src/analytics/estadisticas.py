"""
Módulo de cálculos estadísticos para la Encuesta Salarial
Calcula percentiles, medias y segmentaciones por tamaño de empresa
"""

import pandas as pd
import numpy as np
from pathlib import Path


class EstadisticasSalariales:
    """Calcula estadísticas de salarios por cargo y segmentación"""

    def __init__(self, df_normalizado):
        self.df = df_normalizado
        self.stats_por_cargo = {}
        self.stats_por_rubro = {}

    def calcular_percentiles_cargo(self, columna_salario, segmentar_por_tamano=True):
        """
        Calcula P25, P50 (mediana), P75 y promedio para un cargo específico

        Args:
            columna_salario: nombre de la columna de salario (ej: 'salario_ceo')
            segmentar_por_tamano: si True, calcula por Grande/Pyme

        Returns:
            dict con estadísticas
        """
        stats = {}

        if segmentar_por_tamano and 'categoria_tamano' in self.df.columns:
            # Estadísticas por tamaño
            for tamano in ['Grande', 'Pyme']:
                df_seg = self.df[self.df['categoria_tamano'] == tamano]
                salarios = pd.to_numeric(df_seg[columna_salario], errors='coerce').dropna()

                if len(salarios) > 0:
                    stats[tamano] = {
                        'P25': salarios.quantile(0.25),
                        'P50': salarios.quantile(0.50),  # Mediana
                        'P75': salarios.quantile(0.75),
                        'Promedio': salarios.mean(),
                        'Desv_Std': salarios.std(),
                        'Min': salarios.min(),
                        'Max': salarios.max(),
                        'Count': len(salarios)
                    }
                else:
                    stats[tamano] = None

        # Estadísticas generales (sin segmentar)
        salarios_general = pd.to_numeric(self.df[columna_salario], errors='coerce').dropna()

        if len(salarios_general) > 0:
            stats['General'] = {
                'P25': salarios_general.quantile(0.25),
                'P50': salarios_general.quantile(0.50),
                'P75': salarios_general.quantile(0.75),
                'Promedio': salarios_general.mean(),
                'Desv_Std': salarios_general.std(),
                'Min': salarios_general.min(),
                'Max': salarios_general.max(),
                'Count': len(salarios_general)
            }
        else:
            stats['General'] = None

        return stats

    def calcular_todos_los_cargos(self):
        """Calcula estadísticas para todos los cargos"""
        print("Calculando estadísticas para todos los cargos...")

        salary_columns = [col for col in self.df.columns if col.startswith('salario_')]

        for col in salary_columns:
            cargo_nombre = col.replace('salario_', '').replace('_', ' ').title()
            stats = self.calcular_percentiles_cargo(col)

            if stats.get('General') and stats['General']['Count'] >= 1:  # Mínimo 1 respuesta
                self.stats_por_cargo[col] = {
                    'nombre': cargo_nombre,
                    'stats': stats
                }

        print(f"✓ Estadísticas calculadas para {len(self.stats_por_cargo)} cargos")
        return self

    def get_top_cargos(self, n=10):
        """Obtiene los N cargos con más respuestas"""
        cargo_counts = []

        for cargo, data in self.stats_por_cargo.items():
            count = data['stats']['General']['Count']
            cargo_counts.append({
                'cargo': cargo,
                'nombre': data['nombre'],
                'count': count
            })

        df_counts = pd.DataFrame(cargo_counts)
        return df_counts.sort_values('count', ascending=False).head(n)

    def analizar_aumentos_salariales(self):
        """Analiza las proyecciones de aumentos salariales"""
        stats = {}

        if 'aumento_salarial_2025_pct' in self.df.columns:
            # Distribución de aumentos (son categóricos, no numéricos)
            aumentos = self.df['aumento_salarial_2025_pct'].dropna()
            stats['aumentos_2025'] = aumentos.value_counts().to_dict()

        if 'cantidad_aumentos_2025' in self.df.columns:
            cant_aumentos = self.df['cantidad_aumentos_2025'].dropna()
            stats['cantidad_aumentos'] = cant_aumentos.value_counts().to_dict()

        if 'rotacion_2025_pct' in self.df.columns:
            rotacion = self.df['rotacion_2025_pct'].dropna()
            stats['rotacion'] = rotacion.value_counts().to_dict()

        return stats

    def analizar_beneficios(self):
        """Analiza la distribución de beneficios"""
        beneficios = {}

        benef_columns = [col for col in self.df.columns if col.startswith('benef_')]

        for col in benef_columns:
            if 'categoria_tamano' in self.df.columns:
                beneficios[col] = {
                    'Grande': self.df[self.df['categoria_tamano'] == 'Grande'][col].value_counts(normalize=True).to_dict(),
                    'Pyme': self.df[self.df['categoria_tamano'] == 'Pyme'][col].value_counts(normalize=True).to_dict(),
                }
            else:
                beneficios[col] = self.df[col].value_counts(normalize=True).to_dict()

        return beneficios

    def crear_tabla_resumen(self, cargos_seleccionados=None):
        """
        Crea una tabla resumen con estadísticas de cargos seleccionados

        Args:
            cargos_seleccionados: lista de nombres de columnas de salarios

        Returns:
            DataFrame con resumen
        """
        if cargos_seleccionados is None:
            # Top 20 cargos
            top_cargos = self.get_top_cargos(20)
            cargos_seleccionados = top_cargos['cargo'].tolist()

        resumen = []

        for cargo in cargos_seleccionados:
            if cargo in self.stats_por_cargo:
                data = self.stats_por_cargo[cargo]
                stats_gen = data['stats'].get('General')
                stats_grande = data['stats'].get('Grande')
                stats_pyme = data['stats'].get('Pyme')

                row = {
                    'Cargo': data['nombre'],
                    'Respuestas': stats_gen['Count'] if stats_gen else 0,
                }

                if stats_gen:
                    row.update({
                        'P25_General': stats_gen['P25'],
                        'P50_General': stats_gen['P50'],
                        'P75_General': stats_gen['P75'],
                        'Promedio_General': stats_gen['Promedio'],
                    })

                if stats_grande:
                    row.update({
                        'P25_Grande': stats_grande['P25'],
                        'P50_Grande': stats_grande['P50'],
                        'P75_Grande': stats_grande['P75'],
                    })

                if stats_pyme:
                    row.update({
                        'P25_Pyme': stats_pyme['P25'],
                        'P50_Pyme': stats_pyme['P50'],
                        'P75_Pyme': stats_pyme['P75'],
                    })

                # Calcular brecha entre Grande y Pyme
                if stats_grande and stats_pyme:
                    brecha_p50 = ((stats_grande['P50'] - stats_pyme['P50']) / stats_pyme['P50'] * 100)
                    row['Brecha_Grande_Pyme_%'] = brecha_p50

                resumen.append(row)

        return pd.DataFrame(resumen)

    def exportar_estadisticas(self, output_path):
        """Exporta todas las estadísticas a un archivo Excel"""
        print(f"\nExportando estadísticas a {output_path}...")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Tabla resumen de cargos
            df_resumen = self.crear_tabla_resumen()
            df_resumen.to_excel(writer, sheet_name='Resumen_Cargos', index=False)

            # Top cargos
            df_top = self.get_top_cargos(30)
            df_top.to_excel(writer, sheet_name='Top_Cargos', index=False)

            # Análisis de aumentos
            stats_aumentos = self.analizar_aumentos_salariales()
            if stats_aumentos:
                df_aumentos = pd.DataFrame([stats_aumentos])
                df_aumentos.to_excel(writer, sheet_name='Analisis_Aumentos', index=False)

        print("✓ Estadísticas exportadas")
        return self


def main():
    """Función principal"""
    base_path = Path(__file__).parent.parent.parent
    csv_path = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    output_excel = base_path / 'data' / 'processed' / 'estadisticas_salarios.xlsx'

    # Cargar datos normalizados
    print("Cargando datos normalizados...")
    df = pd.read_csv(csv_path)
    print(f"✓ Datos cargados: {len(df)} empresas")

    # Calcular estadísticas
    stats = EstadisticasSalariales(df)
    stats.calcular_todos_los_cargos()

    # Mostrar top cargos
    print("\n" + "="*60)
    print("TOP 10 CARGOS CON MÁS RESPUESTAS")
    print("="*60)
    print(stats.get_top_cargos(10))

    # Exportar a Excel
    stats.exportar_estadisticas(output_excel)

    print("\n✅ Análisis estadístico completado!")


if __name__ == "__main__":
    main()
