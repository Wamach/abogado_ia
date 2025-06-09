# 🔧 Guía de Instalación y Configuración Rápida

## 📋 Estado Actual del Sistema

**✅ Componentes Disponibles:**
- ✅ Etapa 1: Chatbot Offline (Puerto 8000)
- ✅ Etapa 1.5: Sistema de Webhooks (Puerto 8002)  
- ✅ Etapa 2: Predicción de Sentencias IA (Puerto 8003)
- ✅ Frontend Web Completo
- ✅ Dashboard de Monitoreo

**⚠️ Estado Detectado:**
- ✅ Python 3.11.9 disponible (via `py` launcher)
- ⚠️ Dependencias pueden no estar instaladas
- ⚠️ Servicios no están ejecutándose actualmente

## 🚀 Instalación Paso a Paso

### 1. Instalar Dependencias

```bash
# Navegar al directorio del proyecto
cd c:\Users\USER\GitHub\abogado_ia\backend

# Instalar dependencias mínimas para comenzar
py -m pip install fastapi uvicorn pydantic

# Instalar dependencias completas
py -m pip install -r requirements.txt
```

### 2. Verificar Instalación

```bash
# Ejecutar script de testing
cd c:\Users\USER\GitHub\abogado_ia
py test_sistema.py
```

### 3. Iniciar Servicios

**Opción A: Manual (Recomendado para testing)**
```bash
# Terminal 1 - Chatbot Principal
cd c:\Users\USER\GitHub\abogado_ia\backend
py chatbot_offline.py

# Terminal 2 - Sistema de Webhooks  
cd c:\Users\USER\GitHub\abogado_ia\backend
py webhook_integrations.py

# Terminal 3 - Predicción IA
cd c:\Users\USER\GitHub\abogado_ia\backend  
py predict_api.py
```

**Opción B: Automático**
```bash
# Ejecutar launcher completo
iniciar_sistema_completo.bat
```

## 🌐 URLs de Acceso

| Servicio | URL | Estado |
|----------|-----|---------|
| **Frontend Principal** | `file:///c:/Users/USER/GitHub/abogado_ia/frontend/index.html` | ✅ Disponible |
| **Dashboard Sistema** | `file:///c:/Users/USER/GitHub/abogado_ia/frontend/dashboard.html` | ✅ Disponible |
| **Predicción IA** | `file:///c:/Users/USER/GitHub/abogado_ia/frontend/prediction.html` | ✅ Disponible |
| **Chatbot API** | `http://localhost:8000` | ⚠️ Requiere inicio |
| **Webhook API** | `http://localhost:8002` | ⚠️ Requiere inicio |
| **Prediction API** | `http://localhost:8003` | ⚠️ Requiere inicio |
| **API Docs** | `http://localhost:8000/docs` | ⚠️ Requiere inicio |

## 🧪 Testing Rápido

### Test 1: Verificar Sistema
```bash
py test_sistema.py
```

### Test 2: Probar Chatbot
```bash
# Después de iniciar chatbot_offline.py
curl http://localhost:8000/
```

### Test 3: Probar Predicción
```bash
# Después de iniciar predict_api.py
curl http://localhost:8003/health
```

## 📱 Configuración de Webhooks (Opcional)

### Para WhatsApp Business:
1. Editar `backend/.env`
2. Agregar tokens reales:
```env
WHATSAPP_TOKEN=tu_token_real
WHATSAPP_VERIFY_TOKEN=tu_token_verificacion
```

### Para Facebook Messenger:
1. Configurar en Meta Developers
2. Actualizar `backend/.env`:
```env
MESSENGER_PAGE_TOKEN=tu_page_token
MESSENGER_VERIFY_TOKEN=tu_verify_token
```

## 🔍 Resolución de Problemas

### Error: "Módulo no encontrado"
```bash
py -m pip install nombre_del_modulo
```

### Error: "Puerto ocupado"
```bash
# Cambiar puerto en el archivo correspondiente
# O terminar proceso existente
taskkill /f /im python.exe
```

### Error: "No se puede conectar"
- Verificar que los servicios estén ejecutándose
- Revisar firewall de Windows
- Confirmar puertos disponibles

## 📊 Arquitectura del Sistema

```
🏢 DESPACHO JURÍDICO AUTOMATIZADO
├── 📱 FRONTEND (HTML/JS)
│   ├── index.html (Chat principal)
│   ├── prediction.html (IA Legal)
│   └── dashboard.html (Monitoreo)
│
├── 🤖 BACKEND APIs (FastAPI)
│   ├── chatbot_offline.py (Puerto 8000)
│   ├── webhook_integrations.py (Puerto 8002)
│   └── predict_api.py (Puerto 8003)
│
└── 🗄️ DATOS (SQLite)
    ├── despacho.db (Citas y conversaciones)
    ├── webhook_messages.db (Integraciones)
    └── predictions.db (IA Predicciones)
```

## ⚡ Inicio Rápido (5 minutos)

1. **Instalar dependencias básicas:**
   ```bash
   cd backend && py -m pip install fastapi uvicorn pydantic requests
   ```

2. **Iniciar chatbot:**
   ```bash
   py chatbot_offline.py
   ```

3. **Abrir frontend:**
   - Abrir `frontend/index.html` en el navegador
   - Probar chat con: "Hola, ¿qué servicios ofrecen?"

4. **Verificar funcionamiento:**
   - Ir a `http://localhost:8000/docs` para ver API
   - Usar dashboard en `frontend/dashboard.html`

## 📞 Soporte

- **Logs del sistema:** Revisar consola de cada servicio
- **Testing:** Ejecutar `py test_sistema.py`
- **Documentación:** Ver `README_SISTEMA_COMPLETO.md`
- **Configuración:** Revisar archivos `.env`

---

> **💡 Tip:** Para desarrollo, ejecuta servicios por separado en terminales diferentes para ver logs individuales.
