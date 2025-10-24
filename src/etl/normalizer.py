"""
Script de normalización del CSV de la Encuesta Salarial
Convierte columnas con nombres largos a nombres cortos y manejables
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path


class EncuestaNormalizer:
    """Normaliza y limpia los datos de la encuesta salarial"""

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df_raw = None
        self.df_normalized = None
        self.column_mapping = {}

    def load_data(self):
        """Carga el CSV raw"""
        print("Cargando datos...")
        self.df_raw = pd.read_csv(self.csv_path)
        print(f"✓ Datos cargados: {self.df_raw.shape[0]} filas, {self.df_raw.shape[1]} columnas")
        return self

    def generate_column_mapping(self):
        """Genera mapeo automático de columnas largas a cortas"""
        print("\nGenerando mapeo de columnas...")

        mapping = {}
        used_short_names = set()  # Track nombres cortos ya usados

        for col in self.df_raw.columns:
            # Básicas
            if 'Marca temporal' in col:
                mapping[col] = 'timestamp'
            elif 'Puntuación' in col:
                mapping[col] = 'puntuacion'
            elif 'RUBRO' in col:
                mapping[col] = 'rubro'
            elif 'TAMAÑO' in col:
                mapping[col] = 'tamano'

            # Proyecciones y empleo
            elif 'AUMENTO SALARIAL estima dar la empresa en TODO el año 2025' in col:
                mapping[col] = 'aumento_salarial_2025_pct'
            elif 'Cuantos aumentos salariales' in col:
                mapping[col] = 'cantidad_aumentos_2025'
            elif 'AUMENTO salarial ACUMULADO de Enero a Agosto 2025' in col:
                mapping[col] = 'aumento_acumulado_2025'
            elif 'indicador con el cual prevé dar los aumentos' in col:
                mapping[col] = 'indicador_aumentos'
            elif 'otro indicador' in col.lower():
                mapping[col] = 'otro_indicador'
            elif 'incorporar nuevos puestos' in col:
                mapping[col] = 'prevision_incorporacion'
            elif 'reducir puestos' in col:
                mapping[col] = 'prevision_reduccion'
            elif 'Rotación' in col:
                mapping[col] = 'rotacion_2025_pct'

            # Salarios por cargo
            elif 'CEO / GERENTE GENERAL' in col or 'GERENTE GENERAL' in col:
                mapping[col] = 'salario_ceo'
            elif 'ASISTENTE DE GERENTE GENERAL' in col:
                mapping[col] = 'salario_asistente_gg'
            elif 'DIRECTOR COMERCIAL' in col:
                mapping[col] = 'salario_director_comercial'
            elif 'GERENTE DE VENTAS' in col:
                mapping[col] = 'salario_gerente_ventas'
            elif 'JEFE DE VENTAS' in col:
                mapping[col] = 'salario_jefe_ventas'
            elif 'EJECUTIVO DE VENTAS' in col:
                mapping[col] = 'salario_ejecutivo_ventas'
            elif 'ANALISTA E-COMMERCE' in col:
                mapping[col] = 'salario_analista_ecommerce'
            elif 'ANALISTA DE FACTURACION' in col:
                mapping[col] = 'salario_analista_facturacion'
            elif 'GERENTE DE MARKETING' in col:
                mapping[col] = 'salario_gerente_marketing'
            elif 'JEFE DE MARKETING' in col:
                mapping[col] = 'salario_jefe_marketing'
            elif 'ANALISTA DE MARKETING' in col:
                mapping[col] = 'salario_analista_marketing'
            elif 'GERENTE DE COMERCIO EXTERIOR' in col:
                mapping[col] = 'salario_gerente_comex'
            elif 'RESPONSABLE DE COMERCIO EXTERIOR' in col:
                mapping[col] = 'salario_responsable_comex'
            elif 'ASISTENTE DE COMERCIO EXTERIOR' in col:
                mapping[col] = 'salario_asistente_comex'
            elif 'ATENCION AL CLIENTE' in col:
                mapping[col] = 'salario_atencion_cliente'
            elif 'JEFE DE HOSPITALIDAD Y TURISMO' in col:
                mapping[col] = 'salario_jefe_hospitalidad'
            elif 'GUIA DE TURISMO' in col:
                mapping[col] = 'salario_guia_turismo'
            elif 'JEFE DE ALIMENTOS & BEBIDAS' in col:
                mapping[col] = 'salario_jefe_alimentos_bebidas'
            elif 'CHEF EJECUTIVO' in col:
                mapping[col] = 'salario_chef_ejecutivo'
            elif 'JEFE DE SALON' in col or 'Maître' in col:
                mapping[col] = 'salario_jefe_salon'
            elif 'GERENTE DE OPERACIONES (HOTEL)' in col:
                mapping[col] = 'salario_gerente_ops_hotel'
            elif 'JEFE DE RECEPCION (HOTEL)' in col:
                mapping[col] = 'salario_jefe_recepcion_hotel'
            elif 'RECEPCIONISTA (HOTEL)' in col:
                mapping[col] = 'salario_recepcionista_hotel'
            elif 'CONCIERGE (HOTEL)' in col:
                mapping[col] = 'salario_concierge'
            elif 'DIRECTOR DE ADMIN. & FINANZAS' in col:
                mapping[col] = 'salario_director_admin_finanzas'
            elif 'GERENTE DE ADMIN, CONTABILIDAD & IMPUESTOS' in col:
                mapping[col] = 'salario_gerente_admin_conta'
            elif 'JEFE DE ADMINISTRACION & CONTABILIDAD' in col:
                mapping[col] = 'salario_jefe_admin_conta'
            elif 'ANALISTA DE CONTABILIDAD' in col:
                mapping[col] = 'salario_analista_contabilidad'
            elif 'JEFE DE IMPUESTOS' in col:
                mapping[col] = 'salario_jefe_impuestos'
            elif 'ANALISTA DE IMPUESTOS' in col:
                mapping[col] = 'salario_analista_impuestos'
            elif 'JEFE DE FINANZAS' in col:
                mapping[col] = 'salario_jefe_finanzas'
            elif 'ANALISTA DE CUENTAS POR PAGAR' in col:
                mapping[col] = 'salario_analista_cuentas_pagar'
            elif 'EMPLEADO ADMINISTRATIVO' in col or 'DATA ENTRY' in col:
                mapping[col] = 'salario_empleado_administrativo'
            elif 'JEFE DE CREDITOS Y COBRANZAS' in col:
                mapping[col] = 'salario_jefe_creditos_cobranzas'
            elif 'ANALISTA DE COBRANZAS' in col:
                mapping[col] = 'salario_analista_cobranzas'
            elif 'JEFE DE CONTROL DE GESTION' in col:
                mapping[col] = 'salario_jefe_control_gestion'
            elif 'ANALISTA DE CONTROL DE GESTION' in col:
                mapping[col] = 'salario_analista_control_gestion'
            elif 'AUDITOR INTERNO' in col:
                mapping[col] = 'salario_auditor_interno'
            elif 'RECEPCIONISTA:' in col and 'HOTEL' not in col:
                mapping[col] = 'salario_recepcionista'
            elif 'DIRECTOR DE OPERACIONES' in col and 'HOTEL' not in col:
                mapping[col] = 'salario_director_operaciones'
            elif 'GERENTE DE PLANTA' in col or 'OPERACIONES:' in col:
                mapping[col] = 'salario_gerente_planta'
            elif 'JEFE DE PRODUCCION' in col:
                mapping[col] = 'salario_jefe_produccion'
            elif 'INGENIERO DE PROCESOS' in col or 'MEJORA CONTINUA' in col:
                mapping[col] = 'salario_ingeniero_procesos'
            elif 'SUPERVISOR DE PRODUCCION' in col:
                mapping[col] = 'salario_supervisor_produccion'
            elif 'ANALISTA DE PRODUCCION' in col:
                mapping[col] = 'salario_analista_produccion'
            elif 'GERENTE DE ENOLOGIA' in col or '1er Enologo' in col:
                mapping[col] = 'salario_gerente_enologia'
            elif 'JEFE DE BODEGA' in col or '2ndo Enologo' in col:
                mapping[col] = 'salario_jefe_bodega'
            elif 'SUPERVISOR DE BODEGA' in col:
                mapping[col] = 'salario_supervisor_bodega'
            elif 'GERENTE AGRICOLA' in col:
                mapping[col] = 'salario_gerente_agricola'
            elif 'INGENIERO AGRONOMO' in col:
                mapping[col] = 'salario_ingeniero_agronomo'
            elif 'SUPERVISOR DE FINCAS' in col:
                mapping[col] = 'salario_supervisor_fincas'
            elif 'JEFE DE LABORATORIO' in col:
                mapping[col] = 'salario_jefe_laboratorio'
            elif 'ANALISTA DE LABORATORIO' in col:
                mapping[col] = 'salario_analista_laboratorio'
            elif 'GERENTE DE SUPPLY CHAIN' in col:
                mapping[col] = 'salario_gerente_supply_chain'
            elif 'JEFE DE PLANIFICACION' in col:
                mapping[col] = 'salario_jefe_planificacion'
            elif 'JEFE DE LOGISTICA' in col:
                mapping[col] = 'salario_jefe_logistica'
            elif 'ANALISTA DE LOGISTICA' in col:
                mapping[col] = 'salario_analista_logistica'
            elif 'SUPERVISOR DE DEPOSITOS' in col:
                mapping[col] = 'salario_supervisor_depositos'
            elif 'GERENTE DE ABASTECIMIENTO Y COMPRAS' in col:
                mapping[col] = 'salario_gerente_compras'
            elif 'JEFE DE COMPRAS' in col:
                mapping[col] = 'salario_jefe_compras'
            elif 'COMPRADOR' in col or 'ANALISTA DE COMPRAS' in col:
                mapping[col] = 'salario_comprador_analista'
            elif 'GERENTE DE MANTENIMIENTO' in col:
                mapping[col] = 'salario_gerente_mantenimiento'
            elif 'JEFE DE MANTENIMIENTO' in col:
                mapping[col] = 'salario_jefe_mantenimiento'
            elif 'SUPERVISOR DE MANTENIMIENTO' in col:
                mapping[col] = 'salario_supervisor_mantenimiento'
            elif 'TECNICO DE MANTENIMIENTO' in col:
                mapping[col] = 'salario_tecnico_mantenimiento'
            elif 'GERENTE DE ASEGURAMIENTO DE LA CALIDAD' in col:
                mapping[col] = 'salario_gerente_calidad'
            elif 'JEFE DE CALIDAD' in col:
                mapping[col] = 'salario_jefe_calidad'
            elif 'ANALISTA DE CALIDAD' in col:
                mapping[col] = 'salario_analista_calidad'
            elif 'TECNICO DE CALIDAD' in col:
                mapping[col] = 'salario_tecnico_calidad'
            elif 'DISEÑADOR GRAFICO' in col or 'PRODUCTO:' in col:
                mapping[col] = 'salario_diseñador_grafico'
            elif 'SUSTENTABILIDAD' in col or 'MEDIOAMBIENTE' in col:
                mapping[col] = 'salario_responsable_sustentabilidad'
            elif 'GERENTE DE SEGURIDAD & HIGIENE' in col:
                mapping[col] = 'salario_gerente_seguridad'
            elif 'JEFE DE SEGURIDAD & HIGIENE' in col:
                mapping[col] = 'salario_jefe_seguridad'
            elif 'TECNICO DE SEGURIDAD & HIGIENE' in col:
                mapping[col] = 'salario_tecnico_seguridad'
            elif 'JEFE DE INGENIERIA Y PROYECTOS' in col:
                mapping[col] = 'salario_jefe_ingenieria'
            elif 'INGENIERO DE PROYECTOS' in col or 'PROJECT MANAGER' in col:
                mapping[col] = 'salario_ingeniero_proyectos'
            elif 'ASISTENTE DE PROYECTO' in col or 'PROYECTISTA' in col:
                mapping[col] = 'salario_asistente_proyecto'
            elif 'JEFE DE OBRA' in col:
                mapping[col] = 'salario_jefe_obra'
            elif 'SUPERVISOR DE OBRA' in col:
                mapping[col] = 'salario_supervisor_obra'
            elif 'DIRECTOR DE RECURSOS HUMANOS' in col:
                mapping[col] = 'salario_director_rrhh'
            elif 'GERENTE DE RECURSOS HUMANOS' in col:
                mapping[col] = 'salario_gerente_rrhh'
            elif 'JEFE DE RECURSOS HUMANOS' in col or 'HRBP' in col:
                mapping[col] = 'salario_jefe_rrhh'
            elif 'RESPONSABLE DE LIQUIDACION' in col:
                mapping[col] = 'salario_responsable_liquidacion'
            elif 'ANALISTA DE ADMINISTRACION DE PERSONAL' in col:
                mapping[col] = 'salario_analista_admin_personal'
            elif 'JEFE DE SELECCION' in col:
                mapping[col] = 'salario_jefe_seleccion'
            elif 'ANALISTA DE SELECCION' in col:
                mapping[col] = 'salario_analista_seleccion'
            elif 'ANALISTA DE CAPACITACION Y DESARROLLO' in col:
                mapping[col] = 'salario_analista_capacitacion'
            elif 'DIRECTOR DE SISTEMAS & IT' in col:
                mapping[col] = 'salario_director_it'
            elif 'GERENTE DE SISTEMAS & IT' in col:
                mapping[col] = 'salario_gerente_it'
            elif 'JEFE DE DESARROLLO DE SISTEMAS' in col:
                mapping[col] = 'salario_jefe_desarrollo'
            elif 'PROGRAMADOR' in col or 'DESARROLLADOR DE SISTEMAS' in col:
                mapping[col] = 'salario_programador'
            elif 'ANALISTA FUNCIONAL' in col:
                mapping[col] = 'salario_analista_funcional'
            elif 'JEFE DE REDES E INFRAESTRUCTURA' in col:
                mapping[col] = 'salario_jefe_redes'
            elif 'TECNICO DE REDES E INFRAESTRUCTURA' in col:
                mapping[col] = 'salario_tecnico_redes'
            elif 'JEFE DE SOPORTE TECNICO' in col:
                mapping[col] = 'salario_jefe_soporte'
            elif 'ANALISTA HELP DESK' in col:
                mapping[col] = 'salario_analista_helpdesk'
            elif 'JOVEN PROFESIONAL' in col:
                mapping[col] = 'salario_joven_profesional'
            elif 'PASANTE' in col:
                mapping[col] = 'salario_pasante'

            # Bonificaciones
            elif 'Bonus GERENTE GENERAL' in col:
                mapping[col] = 'bonus_gerente_general'
            elif 'Bonus DIRECTORES' in col:
                mapping[col] = 'bonus_directores'
            elif 'Bonus GERENTES' in col:
                mapping[col] = 'bonus_gerentes'
            elif 'Bonus JEFES' in col:
                mapping[col] = 'bonus_jefes'
            elif 'Bonus SUPERVISORES' in col:
                mapping[col] = 'bonus_supervisores'
            elif 'Bonus ANALISTAS' in col:
                mapping[col] = 'bonus_analistas'

            # Beneficios - Medicina
            elif 'Medicina Prepaga' in col:
                mapping[col] = 'benef_medicina_prepaga'
            elif 'reintegro en compra de medicamentos' in col:
                mapping[col] = 'benef_reintegro_medicamentos'
            elif 'Prestamos al personal' in col:
                mapping[col] = 'benef_prestamos'
            elif 'Almuerzo pago' in col or 'Viandas' in col:
                mapping[col] = 'benef_almuerzo'
            elif 'Gimnasio' in col or 'Yoga' in col or 'Mindfulness' in col:
                mapping[col] = 'benef_gimnasio'
            elif 'Gift card' in col or 'Vales de compras' in col:
                mapping[col] = 'benef_gift_card'
            elif 'Red de Descuentos' in col:
                mapping[col] = 'benef_red_descuentos'
            elif 'Descuento en productos de la empresa' in col:
                mapping[col] = 'benef_descuento_productos'
            elif 'Combustible / Transporte' in col:
                mapping[col] = 'benef_combustible'
            elif 'Cochera' in col or 'estacionamiento' in col:
                mapping[col] = 'benef_cochera'
            elif 'Auto compañía para Gerentes' in col:
                mapping[col] = 'benef_auto_gerentes'
            elif 'Auto compañía para Vendedores' in col:
                mapping[col] = 'benef_auto_vendedores'
            elif 'Gastos de Mantenimiento y Seguro de Auto' in col:
                mapping[col] = 'benef_gastos_auto'
            elif 'Tarjeta de Crédito Corporativa' in col:
                mapping[col] = 'benef_tarjeta_credito'
            elif 'Pago de Colegio' in col:
                mapping[col] = 'benef_colegio'
            elif 'Planes de Pensión' in col or 'Seguros de retiro' in col:
                mapping[col] = 'benef_pension'
            elif 'Pago del sueldo en dólares' in col:
                mapping[col] = 'benef_pago_dolares'
            elif 'Pago de Posgrados' in col or 'MBA' in col:
                mapping[col] = 'benef_posgrados'
            elif 'Pago de Sesiones de Coaching' in col:
                mapping[col] = 'benef_coaching'
            elif 'Pago de Clases de Inglés' in col:
                mapping[col] = 'benef_idiomas'
            elif 'Pago de conectividad' in col or 'Internet' in col:
                mapping[col] = 'benef_internet'

            # Beneficios de tiempo
            elif 'Dias adicionales de vacaciones' in col:
                mapping[col] = 'benef_vacaciones_adicionales'
            elif 'Home Office' in col:
                mapping[col] = 'benef_home_office'
            elif 'Día flex' in col:
                mapping[col] = 'benef_dia_flex'
            elif 'cumpleaños libre' in col:
                mapping[col] = 'benef_cumpleanos'
            elif 'Licencia de Maternidad extendida' in col:
                mapping[col] = 'benef_maternidad'
            elif 'Licencia de Paternidad extendida' in col:
                mapping[col] = 'benef_paternidad'
            elif 'after office' in col:
                mapping[col] = 'benef_after_office'
            elif 'Actividades de integración dentro del horario' in col:
                mapping[col] = 'benef_integracion'

            # Comentarios
            elif 'beneficio que tengan implementado' in col:
                mapping[col] = 'comentarios_beneficios'
            elif 'NUEVOS PUESTOS' in col:
                mapping[col] = 'sugerencias_puestos'
            elif 'OTRA INFORMACION' in col:
                mapping[col] = 'comentarios_generales'

            else:
                # Si no matchea nada, crear un nombre genérico
                safe_name = re.sub(r'[^a-zA-Z0-9]', '_', col[:50].lower())
                mapping[col] = safe_name

        # Eliminar columnas que mapean a nombres duplicados (mantener solo la primera)
        short_name_to_orig = {}
        final_mapping = {}

        for orig_col, short_name in mapping.items():
            if short_name not in short_name_to_orig:
                # Primera aparición de este nombre corto
                short_name_to_orig[short_name] = orig_col
                final_mapping[orig_col] = short_name
            else:
                # Ya existe - skip este mapping (no usar esta columna)
                print(f"  ⚠ Skipping duplicado: '{orig_col}' -> '{short_name}' (ya existe)")

        self.column_mapping = final_mapping
        print(f"✓ {len(final_mapping)} columnas mapeadas ({len(mapping) - len(final_mapping)} duplicados eliminados)")
        return self

    def normalize(self):
        """Aplica la normalización al DataFrame"""
        print("\nNormalizando datos...")
        self.df_normalized = self.df_raw.rename(columns=self.column_mapping)

        # Eliminar columnas duplicadas (pandas las renombra con .1, .2, etc.)
        duplicated_cols = [col for col in self.df_normalized.columns
                          if '.1' in col or '.2' in col or '.3' in col or '.4' in col]

        if duplicated_cols:
            print(f"⚠ Eliminando {len(duplicated_cols)} columnas duplicadas:")
            for col in duplicated_cols:
                print(f"  - {col}")
            self.df_normalized = self.df_normalized.drop(columns=duplicated_cols)

        # Convertir salarios a numérico - columna por columna
        salary_columns = [col for col in self.df_normalized.columns if col.startswith('salario_')]

        count = 0
        for col in salary_columns:
            try:
                self.df_normalized.loc[:, col] = pd.to_numeric(self.df_normalized[col], errors='coerce')
                count += 1
            except Exception as e:
                print(f"  Warning: No se pudo convertir {col}: {e}")

        print(f"✓ {count} columnas de salario convertidas a numérico")
        return self

    def clean_data(self):
        """Limpia y prepara los datos"""
        print("\nLimpiando datos...")

        # Reemplazar 0 con NaN en salarios (0 = no tienen ese puesto) - columna por columna
        salary_columns = [col for col in self.df_normalized.columns if col.startswith('salario_')]
        for col in salary_columns:
            self.df_normalized.loc[:, col] = self.df_normalized[col].replace(0, np.nan)

        # Limpiar columnas de tamaño
        if 'tamano' in self.df_normalized.columns:
            self.df_normalized['categoria_tamano'] = self.df_normalized['tamano'].apply(
                lambda x: 'Grande' if x in ['201 - 500 empleados', '+ 500 empleados']
                else ('Pyme' if x in ['1 - 50 empleados', '51 - 200 empleados'] else 'Otro')
            )

        # Limpiar y unificar rubros
        if 'rubro' in self.df_normalized.columns:
            # Normalizar mayúsculas/minúsculas
            self.df_normalized['rubro'] = self.df_normalized['rubro'].str.strip()

            # Unificar duplicados
            rubro_mapping = {
                'Otro rubro': 'Otro Rubro',
                'Gastronomía, Hotelería y Turísmo': 'Gastronomía, Hotelería y Turismo',  # Corregir tilde
            }
            self.df_normalized['rubro'] = self.df_normalized['rubro'].replace(rubro_mapping)

            # Acortar nombres largos para mejor visualización
            rubro_short = {
                'Transporte, Logística, Almacenamiento': 'Transporte y Logística',
                'Energía, Petroleo, Minería, Servicios relacionados': 'Energía y Minería',
                'Gastronomía, Hotelería y Turismo': 'Gastronomía y Turismo',
            }
            self.df_normalized['rubro_corto'] = self.df_normalized['rubro'].replace(rubro_short).fillna(self.df_normalized['rubro'])

        print("✓ Datos limpiados")
        return self

    def save_normalized(self, output_path):
        """Guarda el DataFrame normalizado"""
        print(f"\nGuardando datos normalizados en {output_path}...")
        self.df_normalized.to_csv(output_path, index=False)
        print("✓ Datos guardados")
        return self

    def save_mapping(self, output_path):
        """Guarda el mapeo de columnas"""
        print(f"\nGuardando mapeo de columnas en {output_path}...")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.column_mapping, f, ensure_ascii=False, indent=2)
        print("✓ Mapeo guardado")
        return self

    def get_summary(self):
        """Muestra resumen de los datos"""
        print("\n" + "="*60)
        print("RESUMEN DE DATOS")
        print("="*60)
        print(f"Total de empresas: {len(self.df_normalized)}")
        print(f"\nDistribución por tamaño:")
        if 'categoria_tamano' in self.df_normalized.columns:
            print(self.df_normalized['categoria_tamano'].value_counts())
        print(f"\nDistribución por rubro:")
        if 'rubro' in self.df_normalized.columns:
            print(self.df_normalized['rubro'].value_counts())

        # Contar cuántos salarios hay por cargo
        salary_columns = [col for col in self.df_normalized.columns if col.startswith('salario_')]
        print(f"\nCargos con datos salariales: {len(salary_columns)}")

        # Top 10 cargos con más datos
        salary_counts = self.df_normalized[salary_columns].notna().sum().sort_values(ascending=False)
        print(f"\nTop 10 cargos con más respuestas:")
        for cargo, count in salary_counts.head(10).items():
            print(f"  {cargo}: {count} empresas")

        print("="*60)
        return self


def main():
    """Función principal"""
    # Rutas
    base_path = Path(__file__).parent.parent.parent
    csv_path = base_path / 'data' / 'raw' / 'encuesta_salarial.csv'
    output_csv = base_path / 'data' / 'processed' / 'encuesta_normalizada.csv'
    output_mapping = base_path / 'data' / 'config' / 'mapeo_columnas.json'

    # Crear directorios si no existen
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_mapping.parent.mkdir(parents=True, exist_ok=True)

    # Ejecutar pipeline
    normalizer = EncuestaNormalizer(csv_path)
    normalizer.load_data() \
              .generate_column_mapping() \
              .normalize() \
              .clean_data() \
              .save_normalized(output_csv) \
              .save_mapping(output_mapping) \
              .get_summary()

    print("\n✅ Normalización completada exitosamente!")
    print(f"\nArchivos generados:")
    print(f"  - {output_csv}")
    print(f"  - {output_mapping}")


if __name__ == "__main__":
    main()
