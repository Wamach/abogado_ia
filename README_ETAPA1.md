# 🤖 ETAPA 1: Chatbot Offline con Gestión de Citas

## 📋 Descripción

Chatbot completamente offline para el despacho jurídico que proporciona:
- ✅ Respuestas automáticas sobre servicios legales
- ✅ Información de costos y contacto
- ✅ Sistema de agendamiento de citas
- ✅ Base de conocimiento legal básica
- ✅ Interface web moderna y responsive

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución Automática (Windows)
```bash
# Doble click en el archivo:
iniciar_chatbot.bat
```

### Opción 2: Ejecución Manual

1. **Crear entorno virtual:**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Instalar dependencias:**
```bash
cd backend
pip install -r requirements.txt
```

3. **Iniciar servidor:**
```bash
uvicorn chatbot_offline:app --reload --host 0.0.0.0 --port 8000
```

4. **Abrir frontend:**
```
Abrir archivo: frontend/index.html en su navegador
```

## 🌐 URLs de Acceso

- **Frontend Web**: `file:///[ruta]/frontend/index.html`
- **API Backend**: `http://localhost:8000`
- **Documentación API**: `http://localhost:8000/docs`
- **Chat Endpoint**: `http://localhost:8000/chat`
- **Citas Endpoint**: `http://localhost:8000/agendar_cita`

## 🎯 Funcionalidades del Chatbot

### Consultas Soportadas:
- **Servicios**: "¿Qué servicios ofrecen?"
- **Costos**: "¿Cuánto cuesta una consulta?"
- **Contacto**: "¿Cuál es su dirección?"
- **Citas**: "Quiero agendar una cita"
- **Urgencias**: "Tengo una urgencia legal"

### Servicios Legales:
- **Derecho Civil**: Contratos, sucesiones, responsabilidad civil
- **Derecho Penal**: Defensa criminal, delitos menores y graves
- **Derecho Laboral**: Despidos, indemnizaciones, conflictos laborales
- **Derecho de Familia**: Divorcios, custodia, alimentos

## 🗃️ Base de Datos

El sistema usa SQLite local con las siguientes tablas:
- `citas`: Almacena las citas agendadas
- `conversaciones`: Registra todas las interacciones del chat

## 🔧 Estructura del Proyecto

```
despacho-automatizado/
├── backend/
│   ├── chatbot_offline.py     # API principal del chatbot
│   ├── requirements.txt       # Dependencias Python
│   └── .env                   # Variables de entorno
├── frontend/
│   ├── index.html            # Interface web principal
│   ├── chatbot.js           # Lógica del chat
│   └── calendario.js        # Sistema de citas
├── iniciar_chatbot.bat      # Script de inicio automático
└── README_ETAPA1.md         # Esta documentación
```

## 📱 Características de la Interface

- **Responsive Design**: Compatible con móviles y desktop
- **Chat en Tiempo Real**: Conversación fluida con el bot
- **Sugerencias Inteligentes**: Botones de respuesta rápida
- **Formulario de Citas**: Agendamiento integrado
- **Información de Servicios**: Tarjetas informativas
- **Validación de Datos**: Verificación en tiempo real

## 🛠️ Tecnologías Utilizadas

### Backend:
- **FastAPI**: Framework web moderno
- **SQLite**: Base de datos local
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

### Frontend:
- **HTML5/CSS3**: Estructura y diseño
- **JavaScript Vanilla**: Lógica de interacción
- **Bootstrap 5**: Framework CSS
- **Font Awesome**: Iconos

## 🔍 API Endpoints

### Chat
```http
POST /chat
Content-Type: application/json

{
  "mensaje": "Hola, ¿qué servicios ofrecen?",
  "usuario_id": "user_123"
}
```

### Agendar Cita
```http
POST /agendar_cita
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "3001234567",
  "fecha": "2025-06-15 10:00",
  "tipo_servicio": "civil",
  "descripcion": "Consulta sobre contrato"
}
```

### Horarios Disponibles
```http
GET /horarios_disponibles/2025-06-15
```

## 📊 Monitoreo y Logs

- Las conversaciones se almacenan en la base de datos
- Los logs del servidor aparecen en la consola
- La base de datos se crea automáticamente al iniciar

## 🔮 Próximos Pasos (Etapa 2)

- Integración con Hugging Face para IA avanzada
- Implementación de Gradio para interface de modelos
- Análisis de sentimientos en consultas
- Predicción de tipos de casos legales
- Generación automática de documentos básicos

## 📞 Soporte

Para problemas técnicos:
1. Verificar que Python 3.9+ esté instalado
2. Confirmar que el puerto 8000 esté disponible
3. Revisar los logs en la consola para errores
4. Asegurar que todos los archivos estén en las rutas correctas

---

> **Nota**: Este es un sistema completamente offline que no requiere conexión a internet una vez instalado.
