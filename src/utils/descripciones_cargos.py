"""
Descripciones de cargos extraídas del Excel original
Mapeo de columnas normalizadas a descripciones
"""

DESCRIPCIONES_CARGOS = {
    'salario_ceo': {
        'nombre': 'CEO / Gerente General',
        'descripcion': 'Responsabilidad de definir a dónde se va a dirigir la empresa en un corto, medio y largo plazo. Fijar objetivos que marcan el rumbo y el trabajo de la organización. Definir e implementar la estrategia de la empresa. Asegurar el cumplimiento de los resultados económicos y financieros requeridos por los accionistas.'
    },
    'salario_asistente_gg': {
        'nombre': 'Asistente de Gerente General',
        'descripcion': 'Responsabilidad de llevar agenda laboral del Gerente General y su equipo de gerentes/directores. Gestionar y atender llamadas, correos, correspondencia, participación de eventos, etc. Participar de las reuniones de directorio, armar presentaciones, gestionar sala y equipos. Coordinar viajes, pasajes, traslados y estadías.'
    },
    'salario_director_comercial': {
        'nombre': 'Director Comercial',
        'descripcion': 'Responsabilidad de definir la estrategia comercial de la empresa, supervisar equipos comerciales y de ventas, establecer objetivos de ventas y asegurar su cumplimiento. Reporta directamente a la Gerencia General.'
    },
    'salario_gerente_ventas': {
        'nombre': 'Gerente de Ventas',
        'descripcion': 'Responsabilidad por cumplir los objetivos y lograr el crecimiento comercial fijado por la dirección de la empresa. Diseñar e implementar el plan comercial, las acciones con los clientes, presencia en los diferentes canales.'
    },
    'salario_jefe_ventas': {
        'nombre': 'Jefe de Ventas',
        'descripcion': 'Responsabilidad de supervisar al equipo de vendedores, gestionar la cartera de clientes, definir estrategias de ventas y asegurar el cumplimiento de objetivos comerciales del área.'
    },
    'salario_ejecutivo_ventas': {
        'nombre': 'Ejecutivo de Ventas',
        'descripcion': 'Responsabilidad de gestionar cartera de clientes, realizar visitas comerciales, cerrar ventas, mantener relaciones con clientes y cumplir con los objetivos de ventas asignados.'
    },
    'salario_analista_ecommerce': {
        'nombre': 'Analista de E-commerce',
        'descripcion': 'Responsabilidad de gestionar plataformas de comercio electrónico, análisis de métricas digitales, optimización de conversión y coordinación con áreas de marketing y logística.'
    },
    'salario_analista_facturacion': {
        'nombre': 'Analista de Facturación',
        'descripcion': 'Responsabilidad de emisión de facturas, gestión de comprobantes, control de documentación comercial y coordinación con áreas de administración y ventas.'
    },
    'salario_gerente_marketing': {
        'nombre': 'Gerente de Marketing',
        'descripcion': 'Responsabilidad de diseñar e implementar la estrategia de marketing, gestión de marca, campañas publicitarias, análisis de mercado y coordinación con agencias externas.'
    },
    'salario_jefe_marketing': {
        'nombre': 'Jefe de Marketing',
        'descripcion': 'Responsabilidad de ejecutar el plan de marketing, gestión de redes sociales, coordinación de campañas, análisis de resultados y supervisión del equipo de marketing.'
    },
    'salario_analista_marketing': {
        'nombre': 'Analista de Marketing',
        'descripcion': 'Responsabilidad de análisis de datos de mercado, seguimiento de campañas, gestión de contenidos, investigación de mercado y apoyo en la ejecución del plan de marketing.'
    },
    'salario_gerente_admin_conta': {
        'nombre': 'Gerente de Administración y Contabilidad',
        'descripcion': 'Responsabilidad de gestionar el área administrativa y contable de la empresa, supervisar cierres contables, reportes financieros, presupuestos y cumplimiento normativo.'
    },
    'salario_jefe_admin_conta': {
        'nombre': 'Jefe de Administración y Contabilidad',
        'descripcion': 'Responsabilidad de supervisar procesos administrativos y contables, controlar registraciones, estados contables y coordinación con auditorías.'
    },
    'salario_analista_contabilidad': {
        'nombre': 'Analista de Contabilidad',
        'descripcion': 'Responsabilidad de ejecutar y analizar el proceso completo de la contabilidad: análisis de cuentas, ingreso y pago de facturas, rendiciones de gastos, preparación de estados contables.'
    },
    'salario_jefe_impuestos': {
        'nombre': 'Jefe de Impuestos',
        'descripcion': 'Responsabilidad de gestionar el cumplimiento de obligaciones fiscales, liquidación de impuestos, presentación de declaraciones juradas y asesoramiento tributario.'
    },
    'salario_analista_impuestos': {
        'nombre': 'Analista de Impuestos',
        'descripcion': 'Responsabilidad de cálculo y liquidación de impuestos, preparación de DDJJ, control de retenciones y percepciones, y análisis de normativa fiscal.'
    },
    'salario_jefe_finanzas': {
        'nombre': 'Jefe de Finanzas',
        'descripcion': 'Responsabilidad de gestión de tesorería, análisis financiero, control de flujo de fondos, negociación con bancos y planificación financiera.'
    },
    'salario_analista_cuentas_pagar': {
        'nombre': 'Analista de Cuentas a Pagar',
        'descripcion': 'Responsabilidad de gestión de pagos a proveedores, control de facturas, conciliaciones bancarias y registro de operaciones.'
    },
    'salario_empleado_administrativo': {
        'nombre': 'Empleado Administrativo',
        'descripcion': 'Responsabilidad de tareas administrativas generales, atención telefónica, gestión de archivos, coordinación de trámites y apoyo a diferentes áreas.'
    },
    'salario_jefe_creditos_cobranzas': {
        'nombre': 'Jefe de Créditos y Cobranzas',
        'descripcion': 'Responsabilidad de gestión de cartera de clientes, análisis de crédito, seguimiento de cobranzas, negociación de deudas y minimización de morosidad.'
    },
    'salario_analista_cobranzas': {
        'nombre': 'Analista de Cobranzas',
        'descripcion': 'Responsabilidad de seguimiento de pagos, contacto con clientes morosos, gestión de reclamos y coordinación con áreas comerciales.'
    },
    'salario_director_rrhh': {
        'nombre': 'Director de Recursos Humanos',
        'descripcion': 'Responsabilidad de definir la estrategia de gestión de personas, desarrollo organizacional, clima laboral, compensaciones y beneficios.'
    },
    'salario_gerente_rrhh': {
        'nombre': 'Gerente de Recursos Humanos',
        'descripcion': 'Responsabilidad de implementar políticas de RRHH, procesos de selección, capacitación, evaluación de desempeño y relaciones laborales.'
    },
    'salario_jefe_rrhh': {
        'nombre': 'Jefe de Recursos Humanos',
        'descripcion': 'Responsabilidad de coordinar procesos de RRHH, administración de personal, legajos, contratos y gestión de beneficios.'
    },
    'salario_responsable_liquidacion': {
        'nombre': 'Responsable de Liquidación de Sueldos',
        'descripcion': 'Responsabilidad de liquidación mensual de sueldos, cálculo de cargas sociales, presentación de DDJJ y cumplimiento de obligaciones laborales.'
    },
    'salario_analista_admin_personal': {
        'nombre': 'Analista de Administración de Personal',
        'descripcion': 'Responsabilidad de gestión de legajos, control de ausentismo, registro de novedades y coordinación con liquidación de sueldos.'
    },
    'salario_jefe_seleccion': {
        'nombre': 'Jefe de Selección',
        'descripcion': 'Responsabilidad de liderar procesos de reclutamiento y selección, entrevistas, evaluaciones y onboarding de nuevos colaboradores.'
    },
    'salario_analista_seleccion': {
        'nombre': 'Analista de Selección',
        'descripcion': 'Responsabilidad de búsqueda de candidatos, screening de CVs, coordinación de entrevistas y evaluaciones psicotécnicas.'
    },
    'salario_analista_capacitacion': {
        'nombre': 'Analista de Capacitación',
        'descripcion': 'Responsabilidad de diseño e implementación de programas de capacitación, detección de necesidades, coordinación de formaciones y evaluación de resultados.'
    },
    'salario_director_it': {
        'nombre': 'Director de Sistemas / IT',
        'descripcion': 'Responsabilidad de definir la estrategia tecnológica de la empresa, transformación digital, ciberseguridad e innovación tecnológica.'
    },
    'salario_gerente_it': {
        'nombre': 'Gerente de Sistemas / IT',
        'descripcion': 'Responsabilidad de gestión de infraestructura tecnológica, proyectos de IT, soporte técnico y seguridad informática.'
    },
    'salario_jefe_desarrollo': {
        'nombre': 'Jefe de Desarrollo',
        'descripcion': 'Responsabilidad de liderar equipos de desarrollo de software, gestión de proyectos tecnológicos y arquitectura de sistemas.'
    },
    'salario_programador': {
        'nombre': 'Programador / Desarrollador',
        'descripcion': 'Responsabilidad de desarrollo de software, programación, testing, mantenimiento de aplicaciones y documentación técnica.'
    },
    'salario_analista_funcional': {
        'nombre': 'Analista Funcional',
        'descripcion': 'Responsabilidad de relevamiento de requerimientos, análisis funcional, documentación de procesos y coordinación con desarrollo.'
    },
    'salario_jefe_redes': {
        'nombre': 'Jefe de Redes',
        'descripcion': 'Responsabilidad de gestión de infraestructura de redes, conectividad, seguridad perimetral y administración de servidores.'
    },
    'salario_tecnico_redes': {
        'nombre': 'Técnico de Redes',
        'descripcion': 'Responsabilidad de configuración de equipos de red, mantenimiento de conectividad, troubleshooting y soporte técnico.'
    },
    'salario_jefe_soporte': {
        'nombre': 'Jefe de Soporte Técnico',
        'descripcion': 'Responsabilidad de coordinar equipo de soporte, gestión de tickets, resolución de incidentes y service desk.'
    },
    'salario_analista_helpdesk': {
        'nombre': 'Analista de Help Desk',
        'descripcion': 'Responsabilidad de atención de usuarios, resolución de problemas técnicos, gestión de tickets y soporte remoto.'
    },
    'salario_director_operaciones': {
        'nombre': 'Director de Operaciones',
        'descripcion': 'Responsabilidad de definir estrategia operativa, optimización de procesos productivos, supply chain y gestión de calidad.'
    },
    'salario_gerente_planta': {
        'nombre': 'Gerente de Planta',
        'descripcion': 'Responsabilidad de gestión integral de planta productiva, cumplimiento de objetivos de producción, seguridad y calidad.'
    },
    'salario_jefe_produccion': {
        'nombre': 'Jefe de Producción',
        'descripcion': 'Responsabilidad de planificación y control de producción, supervisión de líneas productivas y optimización de procesos.'
    },
    'salario_supervisor_produccion': {
        'nombre': 'Supervisor de Producción',
        'descripcion': 'Responsabilidad de supervisión de operarios, control de calidad en línea, cumplimiento de estándares de producción.'
    },
    'salario_gerente_supply_chain': {
        'nombre': 'Gerente de Supply Chain',
        'descripcion': 'Responsabilidad de gestión de cadena de suministro, planificación de demanda, inventarios y coordinación logística.'
    },
    'salario_jefe_logistica': {
        'nombre': 'Jefe de Logística',
        'descripcion': 'Responsabilidad de coordinar operaciones logísticas, distribución, transporte y gestión de depósitos.'
    },
    'salario_analista_logistica': {
        'nombre': 'Analista de Logística',
        'descripcion': 'Responsabilidad de planificación de despachos, coordinación de transportes, seguimiento de entregas y gestión documental.'
    },
    'salario_supervisor_depositos': {
        'nombre': 'Supervisor de Depósitos',
        'descripcion': 'Responsabilidad de supervisión de operaciones de almacén, control de inventarios, recepción y despacho de mercadería.'
    },
    'salario_gerente_compras': {
        'nombre': 'Gerente de Compras',
        'descripcion': 'Responsabilidad de definir estrategia de compras, negociación con proveedores, gestión de contratos y optimización de costos.'
    },
    'salario_jefe_compras': {
        'nombre': 'Jefe de Compras',
        'descripcion': 'Responsabilidad de gestión de órdenes de compra, cotizaciones, homologación de proveedores y control de calidad.'
    },
    'salario_comprador_analista': {
        'nombre': 'Comprador / Analista de Compras',
        'descripcion': 'Responsabilidad de solicitar cotizaciones, negociar condiciones, emitir órdenes de compra y seguimiento de entregas.'
    },
    'salario_gerente_calidad': {
        'nombre': 'Gerente de Calidad',
        'descripcion': 'Responsabilidad de implementar sistema de gestión de calidad, auditorías, certificaciones y mejora continua.'
    },
    'salario_jefe_calidad': {
        'nombre': 'Jefe de Calidad',
        'descripcion': 'Responsabilidad de control de calidad en procesos, análisis de no conformidades, acciones correctivas y documentación.'
    },
    'salario_gerente_mantenimiento': {
        'nombre': 'Gerente de Mantenimiento',
        'descripcion': 'Responsabilidad de planificación de mantenimiento preventivo y correctivo, gestión de repuestos y optimización de equipos.'
    },
    'salario_jefe_mantenimiento': {
        'nombre': 'Jefe de Mantenimiento',
        'descripcion': 'Responsabilidad de coordinar tareas de mantenimiento, gestión de órdenes de trabajo y supervisión de técnicos.'
    },
    'salario_supervisor_mantenimiento': {
        'nombre': 'Supervisor de Mantenimiento',
        'descripcion': 'Responsabilidad de supervisión de trabajos de mantenimiento, control de seguridad y coordinación con producción.'
    },
    'salario_tecnico_mantenimiento': {
        'nombre': 'Técnico de Mantenimiento',
        'descripcion': 'Responsabilidad de ejecución de mantenimiento preventivo y correctivo, reparaciones, diagnóstico de fallas.'
    },
    'salario_joven_profesional': {
        'nombre': 'Joven Profesional',
        'descripcion': 'Posición para recién graduados o con poca experiencia laboral. Responsabilidad de apoyo en proyectos, análisis y tareas específicas del área asignada.'
    },
    'salario_pasante': {
        'nombre': 'Pasante',
        'descripcion': 'Estudiante universitario o terciario que realiza prácticas profesionales en la empresa, con responsabilidades de apoyo y aprendizaje.'
    }
}


def get_descripcion(columna_salario):
    """
    Obtiene la descripción de un cargo a partir de la columna de salario

    Args:
        columna_salario: nombre de la columna (ej: 'salario_ceo')

    Returns:
        dict con 'nombre' y 'descripcion' o None si no se encuentra
    """
    return DESCRIPCIONES_CARGOS.get(columna_salario)
