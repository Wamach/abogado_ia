# 🤖 Despacho Jurídico Automatizado - Sistema Completo

## 📋 Descripción General

Sistema integral de despacho jurídico virtual que integra múltiples tecnologías de IA y automatización para ofrecer servicios legales completos. Implementado por etapas para máxima funcionalidad y escalabilidad.

## 🏗️ Arquitectura del Sistema

```
🏢 DESPACHO JURÍDICO AUTOMATIZADO
├── 📱 ETAPA 1: Chatbot Offline (Puerto 8000)
│   ├── Consultas básicas automatizadas
│   ├── Sistema de agendamiento de citas
│   ├── Base de conocimiento legal
│   └── Interface web responsive
│
├── 🔗 ETAPA 1.5: Integraciones Webhook (Puerto 8002)
│   ├── WhatsApp Business Cloud API
│   ├── Facebook Messenger
│   ├── Verificación de tokens
│   └── Logging de conversaciones
│
├── 🧠 ETAPA 2: Sistema IA Legal (Puerto 7860)
│   ├── Análisis de sentimientos
│   ├── Clasificación de casos legales
│   ├── Extracción de entidades (NER)
│   ├── Generación de documentos
│   └── Interface Gradio avanzada
│
└── 🔮 ETAPA 3: Predicción de Sentencias (Puerto 8003)
    ├── Análisis predictivo con ML
    ├── Evaluación de probabilidades
    ├── Recomendaciones estratégicas
    ├── Factores de riesgo
    └── Estimación de tiempos
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- **Python 3.9+** instalado
- **Node.js 14+** (opcional, para desarrollo avanzado)
- **Git** para clonar el repositorio
- **Ngrok** (opcional, para webhooks públicos)

### Instalación Rápida

1. **Clonar el repositorio:**
```bash
git clone https://github.com/usuario/abogado_ia.git
cd abogado_ia
```

2. **Ejecutar sistema completo:**
```bash
# Windows
iniciar_sistema_completo.bat

# O manualmente:
python -m venv venv
venv\Scripts\activate
cd backend
pip install -r requirements.txt
```

## 🌐 URLs y Puertos del Sistema

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| **Chatbot Offline** | 8000 | http://localhost:8000 | API principal del chatbot |
| **Frontend Web** | - | `frontend/index.html` | Interface web principal |
| **Webhook Integration** | 8002 | http://localhost:8002 | WhatsApp y Messenger |
| **Predicción IA** | 8003 | http://localhost:8003 | Sistema de predicción |
| **Gradio IA Legal** | 7860 | http://localhost:7860 | Interface IA avanzada |
| **API Docs** | 8000 | http://localhost:8000/docs | Documentación Swagger |

## 📊 Funcionalidades por Etapa

### 🤖 ETAPA 1: Chatbot Offline
- ✅ **Chatbot Inteligente**: Respuestas predefinidas sobre servicios legales
- ✅ **Agendamiento de Citas**: Sistema completo de reservas
- ✅ **Base de Conocimiento**: Información sobre costos y servicios
- ✅ **Interface Moderna**: Frontend responsive con Bootstrap 5
- ✅ **Base de Datos**: SQLite para persistencia offline
- ✅ **API RESTful**: Endpoints documentados con FastAPI

**Endpoints Principales:**
- `POST /chat` - Conversación con el chatbot
- `POST /agendar_cita` - Agendar nueva cita
- `GET /citas` - Listar citas programadas
- `GET /disponibilidad` - Verificar horarios disponibles

### 🔗 ETAPA 1.5: Integraciones Webhook
- ✅ **WhatsApp Business**: Integración completa con Cloud API
- ✅ **Facebook Messenger**: Webhook y respuestas automáticas
- ✅ **Verificación de Tokens**: Seguridad para webhooks
- ✅ **Logging Avanzado**: Registro de todas las conversaciones
- ✅ **Estadísticas**: Dashboard de interacciones

**Configuración Requerida:**
```env
WHATSAPP_TOKEN=your_access_token
WHATSAPP_VERIFY_TOKEN=your_verify_token
MESSENGER_PAGE_TOKEN=your_page_token
```

### 🧠 ETAPA 2: Sistema IA Legal
- ✅ **Análisis de Sentimientos**: Evaluación emocional de consultas
- ✅ **Clasificación Automática**: 6 categorías legales principales
- ✅ **Extracción de Entidades**: NER para documentos legales
- ✅ **Generación de Texto**: Resúmenes y documentos automáticos
- ✅ **Interface Gradio**: Dashboard interactivo para análisis
- ✅ **Modelos Hugging Face**: Transformers especializados

**Modelos Utilizados:**
- Sentiment: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- NER: `mrm8488/bert-spanish-cased-finetuned-ner`
- Classification: `dccuchile/bert-base-spanish-wwm-uncased`
- Generation: `microsoft/DialoGPT-medium`

### 🔮 ETAPA 3: Predicción de Sentencias
- ✅ **Análisis Predictivo**: ML para probabilidades de éxito
- ✅ **Evaluación de Casos**: Factores de riesgo automatizados
- ✅ **Recomendaciones**: Estrategias legales sugeridas
- ✅ **Estimación de Tiempos**: Duración probable del proceso
- ✅ **Dashboard Avanzado**: Interface web para predicciones
- ✅ **Base de Datos**: Historial y estadísticas de predicciones

## 📁 Estructura del Proyecto

```
abogado_ia/
├── 📄 README.md                    # Documentación principal
├── 📄 README_ETAPA1.md            # Documentación Etapa 1
├── ⚙️ iniciar_chatbot.bat         # Script de inicio simple
├── ⚙️ iniciar_sistema_completo.bat # Script de inicio completo
│
├── 🔧 backend/                     # Servicios del backend
│   ├── 🐍 chatbot_offline.py      # Chatbot principal (Puerto 8000)
│   ├── 🔗 webhook_integrations.py # Webhooks (Puerto 8002)
│   ├── 🔮 predict_api.py          # Predicción (Puerto 8003)
│   ├── 📄 requirements.txt        # Dependencias Python
│   └── ⚙️ .env                    # Variables de entorno
│
├── 🎨 frontend/                    # Interfaces web
│   ├── 🌐 index.html              # Interface principal
│   ├── 📊 prediction.html         # Interface de predicción
│   ├── 🤖 chatbot.js              # Lógica del chat
│   ├── 📅 calendario.js           # Sistema de citas
│   └── 📊 prediction.js           # Lógica de predicción
│
├── 🧠 etapa2/                      # Sistema IA avanzado
│   └── 🐍 legal_ai_gradio.py      # Gradio IA (Puerto 7860)
│
└── 📋 .github/                     # Documentación técnica
    ├── 📄 base.md                  # Especificaciones originales
    └── 📄 instructions/            # Instrucciones detalladas
```

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

```env
# === CONFIGURACIÓN BÁSICA ===
DATABASE_URL=sqlite:///./despacho.db
HOST=0.0.0.0
DEBUG=True

# === WEBHOOKS ===
WHATSAPP_TOKEN=your_whatsapp_token
WHATSAPP_VERIFY_TOKEN=verify_token_123
MESSENGER_PAGE_TOKEN=your_messenger_token
MESSENGER_VERIFY_TOKEN=verify_messenger_123

# === PUERTOS ===
CHATBOT_PORT=8000
WEBHOOK_PORT=8002
PREDICTION_PORT=8003
GRADIO_PORT=7860

# === NGROK (OPCIONAL) ===
NGROK_CHATBOT_URL=https://your-url.ngrok.io
NGROK_WEBHOOK_URL=https://your-webhook.ngrok.io
```

### Configuración de Ngrok para Webhooks

1. **Instalar Ngrok:**
```bash
# Descargar desde: https://ngrok.com/download
# O usar chocolatey: choco install ngrok
```

2. **Exponer servicios:**
```bash
# Terminal 1: Exponer webhooks
ngrok http 8002

# Terminal 2: Exponer chatbot (opcional)
ngrok http 8000
```

3. **Configurar en Meta Developers:**
- WhatsApp: Usar URL de ngrok + `/webhook/whatsapp`
- Messenger: Usar URL de ngrok + `/webhook/messenger`

## 📱 Integración con Redes Sociales

### WhatsApp Business Cloud API

1. **Crear App en Meta Developers**
2. **Configurar WhatsApp Business**
3. **Obtener tokens de acceso**
4. **Configurar webhook**: `https://tu-ngrok-url.ngrok.io/webhook/whatsapp`
5. **Verificar con token configurado**

### Facebook Messenger

1. **Crear página de Facebook**
2. **Crear App en Meta Developers**
3. **Configurar Messenger**
4. **Configurar webhook**: `https://tu-ngrok-url.ngrok.io/webhook/messenger`
5. **Obtener permisos necesarios**

## 🧪 Testing y Desarrollo

### Testing de APIs

```bash
# Test chatbot
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mensaje": "Hola, necesito ayuda legal"}'

# Test predicción
curl -X POST http://localhost:8003/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_caso": "civil",
    "descripcion": "Conflicto contractual",
    "complejidad": "media",
    "evidencias": ["contratos", "correspondencia"]
  }'

# Test webhook stats
curl http://localhost:8002/webhook/stats
```

### Monitoreo de Servicios

```bash
# Verificar estado de servicios
curl http://localhost:8000/health  # Chatbot
curl http://localhost:8002/health  # Webhooks  
curl http://localhost:8003/health  # Predicción
```

## 📊 Base de Datos

### Esquemas Principales

**Citas (chatbot_offline.py):**
- `citas`: id, nombre, email, telefono, fecha, tipo_servicio, descripcion
- `conversaciones`: id, usuario_id, mensaje, respuesta, timestamp

**Webhooks (webhook_integrations.py):**
- `webhook_messages`: id, platform, sender_id, message, response, timestamp

**Predicciones (predict_api.py):**
- `case_predictions`: id, tipo_caso, descripcion, probabilidad_exito, etc.
- `historical_cases`: id, tipo_caso, resultado, tiempo_resolucion, etc.

## 🚀 Despliegue en Producción

### Opción 1: VPS Tradicional

```bash
# 1. Configurar servidor Ubuntu/CentOS
sudo apt update && sudo apt install python3 python3-pip nginx

# 2. Clonar proyecto
git clone https://github.com/usuario/abogado_ia.git
cd abogado_ia

# 3. Configurar entorno
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 4. Configurar servicios systemd
sudo cp deploy/services/*.service /etc/systemd/system/
sudo systemctl enable chatbot-legal.service
sudo systemctl start chatbot-legal.service

# 5. Configurar nginx
sudo cp deploy/nginx/legal-chatbot.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/legal-chatbot.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Opción 2: Docker

```dockerfile
# Dockerfile (crear en raíz del proyecto)
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8002 8003 7860

CMD ["./start_all_services.sh"]
```

```bash
# docker-compose.yml
version: '3.8'
services:
  chatbot:
    build: .
    ports:
      - "8000:8000"
      - "8002:8002"  
      - "8003:8003"
      - "7860:7860"
    environment:
      - DATABASE_URL=sqlite:///./data/despacho.db
    volumes:
      - ./data:/app/data
```

## 📈 Escalabilidad y Mejoras Futuras

### Roadmap Técnico

**🔄 Corto Plazo (1-2 meses):**
- [ ] Implementar autenticación JWT
- [ ] Agregar rate limiting
- [ ] Mejorar logging con ELK Stack
- [ ] Tests automatizados con pytest
- [ ] CI/CD con GitHub Actions

**🚀 Mediano Plazo (3-6 meses):**
- [ ] Migrar a PostgreSQL
- [ ] Implementar microservicios
- [ ] Agregar Redis para caching
- [ ] Sistema de notificaciones push
- [ ] Dashboard administrativo completo

**🌟 Largo Plazo (6+ meses):**
- [ ] Machine Learning avanzado
- [ ] Integración con sistemas ERPs
- [ ] App móvil nativa
- [ ] Inteligencia artificial conversacional avanzada
- [ ] Blockchain para contratos inteligentes

### Optimizaciones de Rendimiento

```python
# Implementar caché Redis
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Caché de respuestas frecuentes
@cache_response(ttl=3600)
def get_legal_response(query):
    # Lógica del chatbot
    pass
```

## 🛡️ Seguridad

### Implementadas
- ✅ Validación de entrada con Pydantic
- ✅ CORS configurado apropiadamente
- ✅ Sanitización básica de datos
- ✅ Verificación de tokens para webhooks

### Por Implementar
- [ ] Autenticación JWT/OAuth2
- [ ] Rate limiting por IP
- [ ] Encriptación de datos sensibles
- [ ] Logs de auditoría
- [ ] Firewall de aplicación web (WAF)

## 📞 Soporte y Mantenimiento

### Logs y Monitoreo

```bash
# Ver logs en tiempo real
tail -f backend/logs/chatbot.log
tail -f backend/logs/webhooks.log
tail -f backend/logs/predictions.log

# Verificar uso de recursos
htop
df -h
netstat -tlnp
```

### Troubleshooting Común

**Problema: Puerto en uso**
```bash
# Encontrar proceso usando puerto
netstat -tlnp | grep :8000
kill -9 PID_DEL_PROCESO
```

**Problema: Modelos de IA no cargan**
```bash
# Verificar espacio en disco
df -h
# Reinstalar transformers
pip install --force-reinstall transformers
```

**Problema: Webhooks no funcionan**
```bash
# Verificar conectividad
curl -X GET "https://tu-ngrok-url.ngrok.io/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=tu_token&hub.challenge=123"
```

## 👥 Contribución

### Cómo Contribuir

1. **Fork del repositorio**
2. **Crear rama feature**: `git checkout -b feature/nueva-funcionalidad`
3. **Hacer cambios y commit**: `git commit -am 'Agregar nueva funcionalidad'`
4. **Push a la rama**: `git push origin feature/nueva-funcionalidad`
5. **Crear Pull Request**

### Estándares de Código

```python
# Usar type hints
def process_legal_query(query: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    pass

# Documentar funciones
def predict_case_outcome(case_data: CaseData) -> PredictionResult:
    """
    Predice el resultado de un caso legal.
    
    Args:
        case_data: Datos del caso legal
        
    Returns:
        Resultado de la predicción con probabilidades
    """
    pass
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **Hugging Face** por los modelos de transformers
- **FastAPI** por el framework web
- **Gradio** por la interfaz de IA
- **Bootstrap** por los componentes UI
- **SQLite** por la base de datos embebida

---

## 📞 Contacto y Soporte

- **Email**: contacto@despachojuridico.com
- **Teléfono**: +57 (1) 234-5678
- **GitHub Issues**: Para reportar bugs o solicitar features
- **Documentación**: Ver carpeta `.github/` para más detalles técnicos

---

> **🚀 ¡Construido con ❤️ y IA para revolucionar los servicios legales!**

Este sistema representa la evolución natural de los despachos jurídicos hacia la era digital, combinando la experiencia legal tradicional con las tecnologías más avanzadas de inteligencia artificial.
