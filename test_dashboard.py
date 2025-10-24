"""
Script de prueba para verificar que el dashboard funciona
"""
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, 'src')
from analytics.estadisticas import EstadisticasSalariales

print("="*70)
print("   DASHBOARD ENCUESTA SALARIAL 2025 - VERIFICACIÓN")
print("="*70)

# 1. Cargar datos
print("\n1️⃣ CARGANDO DATOS...")
df = pd.read_csv('data/processed/encuesta_normalizada.csv')
print(f"   ✓ {len(df)} empresas cargadas")
print(f"   ✓ {len(df.columns)} columnas procesadas")

# 2. Estadísticas básicas
print("\n2️⃣ ESTADÍSTICAS DE PARTICIPACIÓN:")
if 'categoria_tamano' in df.columns:
    grande = (df['categoria_tamano'] == 'Grande').sum()
    pyme = (df['categoria_tamano'] == 'Pyme').sum()
    otro = (df['categoria_tamano'] == 'Otro').sum()
    print(f"   • Empresas Grandes (200+): {grande} ({grande/len(df)*100:.1f}%)")
    print(f"   • Empresas Pyme (1-200): {pyme} ({pyme/len(df)*100:.1f}%)")
    print(f"   • Otras: {otro}")

if 'rubro' in df.columns:
    n_rubros = df['rubro'].nunique()
    print(f"   • Rubros representados: {n_rubros}")

# 3. Calcular estadísticas de cargos
print("\n3️⃣ CALCULANDO ESTADÍSTICAS POR CARGO...")
stats = EstadisticasSalariales(df)
stats.calcular_todos_los_cargos()
print(f"   ✓ {len(stats.stats_por_cargo)} cargos con datos válidos")

# 4. Top cargos
print("\n4️⃣ TOP 10 CARGOS CON MÁS RESPUESTAS:")
top = stats.get_top_cargos(10)
for idx, row in top.iterrows():
    print(f"   {idx+1:2d}. {row['nombre']:30s} - {row['count']:3d} empresas")

# 5. Ejemplo de estadísticas de un cargo
print("\n5️⃣ EJEMPLO: ESTADÍSTICAS DE CEO/GERENTE GENERAL")
if 'salario_ceo' in stats.stats_por_cargo:
    ceo_stats = stats.stats_por_cargo['salario_ceo']['stats']
    
    if ceo_stats.get('General'):
        print(f"   General (todas las empresas):")
        print(f"      • P25:      ${ceo_stats['General']['P25']:>12,.0f}".replace(',', '.'))
        print(f"      • P50:      ${ceo_stats['General']['P50']:>12,.0f}".replace(',', '.'))
        print(f"      • P75:      ${ceo_stats['General']['P75']:>12,.0f}".replace(',', '.'))
        print(f"      • Promedio: ${ceo_stats['General']['Promedio']:>12,.0f}".replace(',', '.'))
        print(f"      • Respuestas: {ceo_stats['General']['Count']}")
    
    if ceo_stats.get('Grande'):
        print(f"\n   Empresas Grandes (200+ empleados):")
        print(f"      • P50:      ${ceo_stats['Grande']['P50']:>12,.0f}".replace(',', '.'))
        print(f"      • Promedio: ${ceo_stats['Grande']['Promedio']:>12,.0f}".replace(',', '.'))
    
    if ceo_stats.get('Pyme'):
        print(f"\n   Empresas Pyme (1-200 empleados):")
        print(f"      • P50:      ${ceo_stats['Pyme']['P50']:>12,.0f}".replace(',', '.'))
        print(f"      • Promedio: ${ceo_stats['Pyme']['Promedio']:>12,.0f}".replace(',', '.'))
    
    if ceo_stats.get('Grande') and ceo_stats.get('Pyme'):
        brecha = ((ceo_stats['Grande']['P50'] - ceo_stats['Pyme']['P50']) / 
                  ceo_stats['Pyme']['P50'] * 100)
        print(f"\n   💡 Brecha Grande vs Pyme: {brecha:+.1f}%")

# 6. Análisis de aumentos
print("\n6️⃣ PROYECCIONES DE AUMENTOS SALARIALES 2025:")
if 'aumento_salarial_2025_pct' in df.columns:
    aumentos = df['aumento_salarial_2025_pct'].dropna()
    aumentos_dist = aumentos.value_counts().head(5)
    print("   Top 5 rangos de aumento:")
    for rango, count in aumentos_dist.items():
        pct = count/len(aumentos)*100
        print(f"      • {rango:12s}: {count:3d} empresas ({pct:.1f}%)")

print("\n" + "="*70)
print("   ✅ VERIFICACIÓN COMPLETADA - DASHBOARD LISTO PARA EJECUTAR")
print("="*70)
print("\n   Para ejecutar el dashboard completo:")
print("   👉 streamlit run app.py")
print("="*70)
