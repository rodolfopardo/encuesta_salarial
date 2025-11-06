"""
Constantes del proyecto Encuesta Salarial
"""

# Colores de Perfil Humano (según los logos)
COLORS = {
    'azul': '#2E5090',
    'verde': '#00A651',
    'rojo': '#ED1C24',
    'amarillo': '#FDB913',
    'gris': '#3D5A6C'
}

# Mapeo de nombres de columnas largas a nombres cortos
COLUMN_MAPPING = {
    # Información de la empresa
    'Marca temporal': 'timestamp',
    'Puntuación': 'puntuacion',
    'Clasificación por RUBRO 🏭': 'rubro',
    'Clasificación por TAMAÑO (Dotación)  👥': 'tamano',

    # Proyecciones salariales
    '¿Qué % de AUMENTO SALARIAL estima dar la empresa en TODO el año 2025 (Ene - Dic) para empleados fuera de convenio?': 'aumento_salarial_2025_pct',
    '¿Cuantos aumentos salariales estima dar en todo el año 2025 para empleados fuera de convenio?': 'cantidad_aumentos_2025',
    '¿Cual fue el % total de AUMENTO salarial ACUMULADO de Enero a Agosto 2025 para empleados fuera de convenio?': 'aumento_acumulado_2025',
    '¿Cuál es el indicador con el cual prevé dar los aumentos la empresa a lo largo del 2025?': 'indicador_aumentos',
    'En caso de tomar otro indicador para otorgar los aumentos salariales, indicar cual --->': 'otro_indicador',

    # Empleo
    '¿Tiene previsto la empresa ⬆️ incorporar nuevos puestos (crecimiento de empleo) fuera de convenio? ': 'prevision_incorporacion',
    '¿Tiene previsto la empresa ⬇️ reducir puestos (caída del empleo) fuera de convenio? ': 'prevision_reduccion',
    '¿Qué % Rotación tuvo la empresa entre Enero y Agosto 2025?  Indicador de entrada y salida de empleados (fuera de convenio). Incluye a todas las personas que dejan la organización (por renuncia, despido, jubilación, etc.) sobre el total de empleados. Indice de Rotación = Empleado que dejan la empresa / (empleados al inicio + empleados al final) / 2': 'rotacion_2025_pct',
}

# Cargos (salarios) - Mapeo simplificado
CARGOS_MAPPING = {
    # Gerencia General
    '👤 CEO / GERENTE GENERAL: Responsabilidad de definir a donde se va a dirigir la empresa en un corto, medio y largo plazo, entre otras muchas tareas. Fijar una serie de objetivos que marcan el rumbo y el trabajo de la organización. Definir e implementar la estrategia de la empresa. Asegurar el cumplimento de los resultados económicos y financieros requeridos por los accionistas de la empresa [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0] ': 'salario_ceo',
    '👤 ASISTENTE DE GERENTE GENERAL: Responsabilidad de llevar agenda laboral del Gerente General y su equipo de gerentes / directores. Gestionar y  atender llamadas, correos, correspondencia, participación de eventos, etc. Participar de las reuniones de directorio, armar presentaciones, gestionar sala y equipos. Coordinar viajes, pasajes, traslados y estadías [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0] ': 'salario_asistente_gg',

    # Comercial
    'DIRECTOR COMERCIAL: Responsabilidad de idear e implementar estrategias comerciales de acuerdo a los objetivos de la empresa reportando al Gerente General. Realizar el análisis y estudios de mercado, creando planes de expansión, desarrollo de negocios, etc. Tiene a cargo el area de Ventas y Marketing y Comercio Exterior. [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_director_comercial',
    'GERENTE DE VENTAS: Responsabilidad por cumplir los objetivos y lograr el crecimiento comercial fijado por la dirección de la empresa. Diseñar e implementar el plan comercial, las acciones con los clientes, presencia en los diferentes canales, identificar los nuevos mercados y análisis de la competencia. [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_gerente_ventas',
    'JEFE DE VENTAS: Responsabilidad de supervisar las actividades comerciales de los vendedores para cumplir con los objetivos de venta y las metas de crecimiento. Gestionar el CRM, asistir a los comerciales y acompañarlos a las visitas de los principales clientes para detectar oportunidades de negocios e interiorizarse de los movimientos del mercado. [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_jefe_ventas',
    'EJECUTIVO DE VENTAS: Responsabilidad por cumplir las metas de ventas, generando relaciones con los clientes activos y potenciales, visitas comerciales, envío y seguimiento de cotizaciones, cobranzas, etc.  [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_ejecutivo_ventas',
    'ANALISTA E-COMMERCE:  Responsabilidad de Administrar y mantener actualizados los productos y precios de la tienda online. Gestionar las diferentes promociones. Analizar las métricas de los resultados de las acciones en diferentes acciones online. Analizar la competencia y oportunidades. Controlar los reviews y opiniones de clientes. Dar rápida resolución a reclamos y responder preguntas a través de las diferentes plataformas. [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_analista_ecommerce',
    'ANALISTA DE FACTURACION:  Responsabilidad de emitir facturas, notas de débito y crédito y gestionar él envió digital a clientes. Elaborar reportes de gestión. Atender reclamos y consultas de clientes externos, con el fin de garantizar la transparencia del proceso de facturación. [Escribir el SUELDO BRUTO MENSUAL ej. 100000 sin puntos ni comas / En caso de no tener alguna posición similar en la empresa escribir el valor -> 0]. Para puestos comerciales con sueldo fijo + variable, deberás completar el total de salario bruto sumando el fijo + un promedio o target de la parte variable.': 'salario_analista_facturacion',
}

# Áreas funcionales para organizar cargos (según clusterización actualizada)
AREAS_FUNCIONALES = {
    'Gerencia General': ['ceo'],
    'Comercial': ['director_comercial', 'gerente_ventas', 'jefe_ventas', 'ejecutivo_ventas',
                  'analista_facturacion', 'atencion_cliente'],
    'Comercio Exterior': ['gerente_comex', 'responsable_comex', 'asistente_comex'],
    'Turismo y Gastronomía': ['jefe_hospitalidad', 'guia_turismo', 'jefe_alimentos_bebidas',
                               'chef_ejecutivo', 'jefe_salon', 'gerente_ops_hotel',
                               'jefe_recepcion_hotel', 'recepcionista_hotel', 'concierge'],
    'Administración y Finanzas': ['director_admin_finanzas', 'gerente_admin_conta',
                                   'jefe_admin_conta', 'analista_contabilidad',
                                   'jefe_impuestos', 'analista_impuestos', 'jefe_finanzas',
                                   'analista_cuentas_pagar', 'empleado_administrativo',
                                   'jefe_creditos_cobranzas', 'analista_cobranzas',
                                   'jefe_control_gestion', 'analista_control_gestion',
                                   'auditor_interno', 'recepcionista'],
    'Operaciones': ['director_operaciones', 'gerente_planta', 'jefe_produccion',
                    'ingeniero_procesos', 'supervisor_produccion', 'analista_produccion',
                    'jefe_bodega', 'supervisor_bodega', 'gerente_agricola', 'ingeniero_agronomo',
                    'supervisor_fincas', 'jefe_laboratorio', 'analista_laboratorio', 'gerente_enologia'],
    'Supply Chain': ['gerente_supply_chain', 'jefe_planificacion', 'jefe_logistica',
                     'analista_logistica', 'supervisor_depositos', 'jefe_compras',
                     'gerente_compras', 'comprador_analista'],
    'Mantenimiento y Calidad': ['gerente_mantenimiento', 'jefe_mantenimiento', 'supervisor_mantenimiento',
                                'tecnico_mantenimiento', 'gerente_calidad', 'jefe_calidad',
                                'analista_calidad', 'tecnico_calidad'],
    'Higiene y Seguridad': ['responsable_sustentabilidad', 'gerente_seguridad', 'jefe_seguridad',
                            'tecnico_seguridad'],
    'Ingeniería y Proyectos': ['jefe_ingenieria', 'ingeniero_proyectos', 'asistente_proyecto',
                               'jefe_obra', 'supervisor_obra'],
    'RRHH': ['director_rrhh', 'gerente_rrhh', 'jefe_rrhh', 'responsable_liquidacion',
             'analista_admin_personal', 'jefe_seleccion', 'analista_seleccion',
             'analista_capacitacion'],
    'IT': ['director_it', 'gerente_it', 'jefe_desarrollo', 'programador',
           'analista_funcional', 'jefe_redes', 'tecnico_redes',
           'jefe_soporte', 'analista_helpdesk'],
    'Marketing': ['gerente_marketing', 'jefe_marketing', 'analista_marketing', 'analista_ecommerce', 'diseñador_grafico'],
    'Pasante': ['pasante', 'joven_profesional']
}

# Beneficios monetarios
BENEFICIOS_MONETARIOS = [
    '💵  Medicina Prepaga para el empleado y grupo familiar',
    '💵  Reconocimiento de un % de reintegro en compra de medicamentos',
    '💵  Prestamos al personal (para ayuda financiera)',
    '💵  Almuerzo pago (comedor) / Viandas / Vales de almuerzo',
    '💵  Pago cuota de Gimnasio / Clases de Yoga / Mindfulness',
    '💵  Gift card / Vales de compras de mercadería',
    '💵  Red de Descuentos en Comercios asociados',
    '💵  Descuento en productos de la empresa',
    '💵  Combustible / Transporte',
    '💵  Cochera / Facilidad de estacionamiento',
    '💵  Auto compañía para Gerentes / Alta Dirección',
    '💵  Auto compañía para Vendedores / Comerciales',
    '💵  Gastos de Mantenimiento y Seguro de Auto para Gerentes / Alta Dirección',
    '💵  Tarjeta de Crédito Corporativa para Gerentes / Alta Dirección',
    '💵  Pago de Colegio para los hijos',
    '💵  Planes de Pensión / Seguros de retiro',
    '💵  Pago del sueldo en dólares (U$s) ',
    '💵  Pago de Posgrados o MBA para puestos Claves / Profesionales',
    '💵  Pago de Sesiones de Coaching para puestos Claves / Profesionales',
    '💵  Pago de Clases de Inglés u otro idioma',
    '💵  Pago de conectividad de Internet en la casa',
]

# Beneficios de tiempo
BENEFICIOS_TIEMPO = [
    '⏰  Dias adicionales de vacaciones por año',
    '⏰  Home Office (1 o 2 veces por semana)',
    '⏰  Día flex (para trámites personales)',
    '⏰  Dia de cumpleaños libre',
    '⏰  Licencia de Maternidad extendida (adicional a la ley)',
    '⏰  Licencia de Paternidad extendida (adicional a la ley)',
    '⏰  Actividades after office de integración',
    '⏰  Actividades de integración dentro del horario de trabajo',
]

# Bonificaciones
BONIFICACIONES = [
    '🎁 Bonus GERENTE GENERAL (Los bonus estan expresados en cantidad de sueldos mensuales)',
    '🎁 Bonus DIRECTORES (Los bonus estan expresados en cantidad de sueldos mensuales)',
    '🎁 Bonus GERENTES (Los bonus estan expresados en cantidad de sueldos mensuales)',
    '🎁 Bonus JEFES (Los bonus estan expresados en cantidad de sueldos mensuales)',
    '🎁 Bonus SUPERVISORES, COORDINADORES, ENCARGADOS (Los bonus estan expresados en cantidad de sueldos mensuales)',
    '🎁 Bonus ANALISTAS, TECNICOS, EMPLEADOS (Los bonus estan expresados en cantidad de sueldos mensuales)',
]

# Clasificación de tamaños
TAMANOS = {
    'Grande': ['201 - 500 empleados', '+ 500 empleados'],
    'Pyme': ['1 - 50 empleados', '51 - 200 empleados']
}
