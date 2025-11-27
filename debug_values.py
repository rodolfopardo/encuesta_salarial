"""
Debug script to analyze CEO salary values and understand discrepancies
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Load normalized data
df = pd.read_csv('data/processed/encuesta_normalizada.csv')

# Check CEO salaries by company size
print('=== CEO SALARIES BY COMPANY SIZE ===\n')

# Filter Grande companies
df_grande = df[df['categoria_tamano'] == 'Grande']
# Incluir 0s como valores válidos
ceo_grande = pd.to_numeric(df_grande['salario_ceo'], errors='coerce')
ceo_grande = ceo_grande[ceo_grande.notna()]  # Solo eliminar NaN, mantener 0

print(f'Grande Companies: {len(df_grande)}')
print(f'CEO Grande values (non-null): {len(ceo_grande)}')
print(f'CEO Grande P25: ${ceo_grande.quantile(0.25):,.0f}')
print(f'CEO Grande P50: ${ceo_grande.quantile(0.50):,.0f}')
print(f'CEO Grande P75: ${ceo_grande.quantile(0.75):,.0f}')
print(f'CEO Grande Mean: ${ceo_grande.mean():,.0f}')
print(f'\nActual CEO Grande values (sorted):')
for val in sorted(ceo_grande.tolist()):
    print(f'  ${val:,.0f}')

print('\n=== CEO PYME ===\n')
df_pyme = df[df['categoria_tamano'] == 'Pyme']
# Incluir 0s como valores válidos
ceo_pyme = pd.to_numeric(df_pyme['salario_ceo'], errors='coerce')
ceo_pyme = ceo_pyme[ceo_pyme.notna()]  # Solo eliminar NaN, mantener 0

print(f'Pyme Companies: {len(df_pyme)}')
print(f'CEO Pyme values (non-null): {len(ceo_pyme)}')
print(f'CEO Pyme P25: ${ceo_pyme.quantile(0.25):,.0f}')
print(f'CEO Pyme P50: ${ceo_pyme.quantile(0.50):,.0f}')
print(f'CEO Pyme P75: ${ceo_pyme.quantile(0.75):,.0f}')
print(f'CEO Pyme Mean: ${ceo_pyme.mean():,.0f}')
print(f'\nActual CEO Pyme values (sorted):')
for val in sorted(ceo_pyme.tolist()):
    print(f'  ${val:,.0f}')

print('\n=== EXPECTED VALUES FROM EXCEL ===')
print('CEO Grande P50: $19,722,471')
print('CEO Pyme P50: $8,495,353')

print('\n=== CHECKING RAW DATA ===')
df_raw = pd.read_csv('data/raw/encuesta_salarial.csv')
print(f'\nRaw data shape: {df_raw.shape}')
print(f'Raw data columns with CEO: {[col for col in df_raw.columns if "CEO" in col.upper()]}')
