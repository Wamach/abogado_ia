---
applyTo: '**'
---

# Instrucciones para Desarrollo - Despacho Jurídico Virtual con IA

## Conocimiento del Dominio

### Contexto del Proyecto
- **Proyecto**: Despacho jurídico virtual con implementación de bots y modelos de IA
- **Objetivo**: Automatizar y asistir en procesos legales mediante inteligencia artificial
- **Usuarios**: Abogados, asistentes legales, clientes del despacho
- **Alcance**: Sistema completo desde entorno local hasta integración con WhatsApp, Facebook y modelo de predicción de sentencias

### Arquitectura del Sistema
```
despacho-automatizado/
├── backend/
│   ├── chatbot_api.py          # API principal del chatbot
│   ├── citas_api.py            # Gestión de citas y agenda
│   ├── predict_api.py          # Modelo de predicción de sentencias
│   ├── webhook_whatsapp.py     # Integración WhatsApp Business
│   ├── webhook_messenger.py    # Integración Facebook Messenger
│   ├── .env                    # Variables de entorno
│   └── requirements.txt        # Dependencias Python
├── frontend/
│   ├── index.html              # Interface web principal
│   ├── chatbot.js             # Cliente del chatbot
│   ├── calendario.js          # Sistema de citas
│   └── prediccion.js          # Interface predicción sentencias
├── data/
│   ├── citas.db               # Base de datos SQLite
│   └── models/                # Modelos de IA locales
└── config/
    ├── ngrok-config.yml       # Configuración túneles
    └── docker-compose.yml     # Containerización
```

### Terminología Legal Clave
- Utilizar terminología jurídica precisa y consistente
- Respetar la nomenclatura legal de la jurisdicción correspondiente
- Implementar validaciones para documentos legales estándar
- Considerar diferentes tipos de procedimientos: civil, penal, laboral, mercantil

## Estándares de Codificación

### Arquitectura y Patrones
- **Microservicios**: Separar funcionalidades por dominio legal
- **Clean Architecture**: Mantener separación clara entre capas
- **Repository Pattern**: Para acceso a datos legales
- **Factory Pattern**: Para creación de documentos legales específicos
- **Observer Pattern**: Para notificaciones de cambios en casos

### Convenciones de Nomenclatura
- **Variables y funciones**: camelCase en español cuando sea apropiado
- **Clases**: PascalCase con nombres descriptivos del contexto legal
- **Constantes**: UPPER_SNAKE_CASE
- **Archivos**: kebab-case para componentes, PascalCase para clases

### Comentarios y Documentación
- Documentar todas las funciones que manejen datos sensibles
- Incluir referencias a artículos legales relevantes cuando sea aplicable
- Usar JSDoc/docstrings para APIs que interactúen con sistemas legales

## Seguridad y Privacidad (OWASP)

### Top 10 OWASP 2021 - Implementación Obligatoria

#### A01:2021 – Broken Access Control
- Implementar autenticación robusta para todos los endpoints
- Validar permisos basados en roles (abogado, asistente, cliente)
- Principio de menor privilegio para acceso a expedientes
- Logs detallados de acceso a información confidencial

#### A02:2021 – Cryptographic Failures
- Cifrado AES-256 para datos en reposo
- TLS 1.3 mínimo para datos en tránsito
- Hash seguro (bcrypt/Argon2) para contraseñas
- Gestión segura de claves de cifrado
- Cifrado específico para documentos legales confidenciales

#### A03:2021 – Injection
- Sanitización estricta de todas las entradas
- Prepared statements para consultas SQL
- Validación de entrada para formularios legales
- Escape de caracteres especiales en documentos generados

#### A04:2021 – Insecure Design
- Threat modeling para cada módulo del sistema legal
- Secure by design desde el primer sprint
- Validación de integridad para documentos legales
- Análisis de riesgos para datos de clientes

#### A05:2021 – Security Misconfiguration
- Configuraciones seguras por defecto
- Revisión regular de permisos de servidor
- Desactivar características innecesarias
- Headers de seguridad obligatorios (HSTS, CSP, etc.)

#### A06:2021 – Vulnerable Components
- Auditoría regular de dependencias (npm audit, OWASP Dependency Check)
- Actualización proactiva de librerías
- Monitoreo de CVEs en componentes usados
- Lista blanca de librerías aprobadas para uso legal

#### A07:2021 – Identification and Authentication Failures
- Autenticación multifactor obligatoria
- Políticas de contraseña robustas
- Gestión segura de sesiones
- Bloqueo temporal tras intentos fallidos
- Rotación regular de credenciales de servicio

#### A08:2021 – Software and Data Integrity Failures
- Verificación de integridad de documentos legales
- Firma digital para documentos críticos
- Backup cifrado y verificación de integridad
- Control de versiones para cambios en expedientes

#### A09:2021 – Security Logging and Monitoring Failures
- Logs de todas las acciones en expedientes
- Monitoreo en tiempo real de accesos anómalos
- Alertas para acciones críticas (descarga masiva, acceso fuera de horario)
- Retención de logs según normativa legal

#### A10:2021 – Server-Side Request Forgery (SSRF)
- Validación estricta de URLs en integraciones
- Lista blanca de servicios externos permitidos
- Sanitización de parámetros de red
- Monitoreo de requests salientes

### Consideraciones Adicionales de Seguridad Legal

#### Protección de Datos Personales
- Cumplimiento GDPR/LOPD según jurisdicción
- Anonimización de datos para entrenar modelos IA
- Derecho al olvido implementado
- Consentimiento explícito para uso de datos

#### Trazabilidad y Auditoría
- Cadena de custodia digital para evidencias
- Timestamps criptográficos para documentos
- Logs inmutables de cambios en expedientes
- Firma digital de abogados responsables

## IA y Machine Learning

### Implementación de Bots
- **Procesamiento de Lenguaje Natural**: Para análisis de documentos legales
- **Clasificación Automática**: Categorización de casos por área legal
- **Extracción de Entidades**: Identificación de fechas, nombres, montos en documentos
- **Generación de Documentos**: Templates legales con IA generativa

### Consideraciones Éticas IA
- Transparencia en decisiones automatizadas
- Supervisión humana obligatoria para decisiones críticas
- Sesgo en modelos: evaluación regular y corrección
- Explicabilidad de decisiones del sistema

### Datos de Entrenamiento
- Anonimización completa antes del entrenamiento
- Validación legal de datasets utilizados
- Versionado de modelos y datasets
- Evaluación continua de precisión legal

## Frameworks y Tecnologías Preferidas

### Backend
- **Node.js/TypeScript** o **Python** para APIs
- **Express.js/FastAPI** para servicios web
- **PostgreSQL/MongoDB** con cifrado para datos
- **Redis** para caché (datos no sensibles únicamente)

### Frontend
- **React/Vue.js** con TypeScript
- **Material-UI/Tailwind** para UI consistente
- **Formik/React Hook Form** para formularios legales
- **PDF.js** para visualización de documentos

### DevOps y Monitoreo
- **Docker** para containerización
- **Kubernetes** para orquestación
- **SIEM** para monitoreo de seguridad
- **Vault** para gestión de secretos

## Testing y Calidad

### Tipos de Testing Obligatorios
- **Unit Tests**: Cobertura mínima 80%
- **Integration Tests**: Para workflows legales completos
- **Security Tests**: SAST/DAST en CI/CD
- **Penetration Testing**: Trimestral para sistemas críticos

### Validación Legal
- Testing de documentos generados por abogados
- Validación de cálculos legales (intereses, multas, etc.)
- Verificación de compliance con normativas

## Compliance y Normativas

### Regulaciones Aplicables
- Secreto profesional abogado-cliente
- Normativas de protección de datos locales
- Regulaciones específicas del colegio de abogados
- ISO 27001 como framework de referencia

### Auditorías
- Auditorías de seguridad trimestrales
- Revisión de accesos mensual
- Evaluación de riesgos semestral
- Compliance legal anual

## Gestión de Incidentes

### Procedimientos Obligatorios
- Plan de respuesta a incidentes de seguridad
- Notificación inmediata de brechas de datos
- Procedimientos de recuperación de desastres
- Comunicación con clientes afectados

## Instrucciones Específicas para GitHub Copilot

### Configuración del Agente
- **Contexto Legal**: Siempre considerar el marco jurídico aplicable
- **Responsabilidad**: El código generado debe ser revisado por profesionales legales
- **Disclaimer**: Incluir avisos de que la IA es una herramienta de asistencia, no un sustituto del criterio legal humano

### Generación de Código Legal
- Utilizar patrones de diseño específicos para sistemas legales
- Implementar validaciones estrictas para datos legales críticos
- Generar logging detallado para auditorías posteriores
- Incluir metadatos de trazabilidad en documentos generados

### Manejo de Datos Sensibles
- **Cifrado obligatorio** para toda información de clientes
- **Anonimización automática** para datos de prueba
- **Backup cifrado** con retención según normativas legales
- **Control de acceso granular** por expediente y cliente

## Integración con Sistemas Legales

### APIs Externas
- **Registro Civil**: Integración para verificación de identidades
- **Registros Públicos**: Consulta de propiedades y sociedades
- **Poder Judicial**: APIs para consulta de expedientes (donde disponible)
- **Colegios Profesionales**: Verificación de habilitación de abogados

### Interoperabilidad
- Estándares XML para intercambio de documentos legales
- Firma digital compatible con normativas locales
- Timestamp cualificado para documentos críticos
- Formatos estándar para diferentes tipos de documentos

## Workflow de Casos Legales

### Ciclo de Vida del Expediente
1. **Creación**: Validación de datos iniciales, asignación de número único
2. **Investigación**: Recopilación y organización de evidencias
3. **Análisis**: Aplicación de IA para análisis legal preliminar
4. **Estrategia**: Generación de opciones estratégicas basadas en jurisprudencia
5. **Ejecución**: Seguimiento de plazos y notificaciones automáticas
6. **Resolución**: Archivo con trazabilidad completa

### Automatización de Procesos
- **Cálculo automático** de plazos procesales
- **Generación de escritos** basada en templates y IA
- **Notificaciones inteligentes** de vencimientos críticos
- **Análisis de jurisprudencia** relevante automático

## Inteligencia Artificial Especializada

### Modelos de Lenguaje Legal
- **Fine-tuning** con corpus jurídico local
- **Evaluación continua** de precisión legal
- **Supervisión humana** obligatoria para decisiones críticas
- **Explicabilidad** de recomendaciones de IA

### Análisis Predictivo
- **Probabilidad de éxito** en litigios basada en históricos
- **Duración estimada** de procesos judiciales
- **Riesgo de cumplimiento** para contratos
- **Detección de inconsistencias** en documentos

### Procesamiento de Documentos
- **OCR legal especializado** para documentos escaneados
- **Extracción de cláusulas** críticas automática
- **Comparación de contratos** con versiones anteriores
- **Generación automática** de resúmenes ejecutivos

## Métricas y KPIs Legales

### Métricas de Rendimiento
- **Tiempo promedio** de resolución por tipo de caso
- **Tasa de éxito** en litigios por área legal
- **Satisfacción del cliente** medida regularmente
- **Eficiencia operativa** del despacho

### Métricas de Calidad
- **Precisión de IA** en análisis legales
- **Errores evitados** por sistemas automáticos
- **Cumplimiento de plazos** procesales
- **Conformidad regulatoria** evaluada trimestralmente

## Comunicación con Clientes

### Portal del Cliente
- **Acceso seguro** a expedientes personales
- **Notificaciones automáticas** de actualizaciones