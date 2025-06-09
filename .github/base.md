# Instrucciones para el Agent de Copilot: Proyecto "Despacho Jurídico Automatizado"

A continuación, se describen los pasos detallados y ordenados que el Agent de Copilot debe seguir para implementar la solución completa, desde el entorno local hasta la integración con WhatsApp, Facebook y el modelo de predicción de sentencias.

---

## 1. Configuración del Entorno de Desarrollo (Local)

1. **Instalación de herramientas**

   * Instalar Python >= 3.9 y Node.js >= 14.x en la máquina.
   * Confirmar versiones: `python --version` y `node --version`.

2. **Crear entorno virtual de Python**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   pip install --upgrade pip
   ```

3. **Inicializar proyecto Node.js**

   ```bash
   mkdir despacho-automatizado && cd despacho-automatizado
   npm init -y
   npm install express body-parser cors
   ```

4. **Instalar dependencias de Python**

   ```bash
   pip install fastapi uvicorn transformers[torch] sqlite-utils python-dotenv
   ```

5. **Estructura de carpetas**

   ```text
   despacho-automatizado/
   ├── backend/
   │   ├── chatbot_api.py
   │   ├── citas_api.py
   │   ├── .env
   │   └── requirements.txt
   ├── frontend/
   │   ├── index.html
   │   ├── chatbot.js
   │   └── calendario.js
   └── ngrok-config.yml
   ```

---

## 2. API de Chatbot (FastAPI)

1. **Archivo `backend/chatbot_api.py`**:

   * Importar FastAPI, Pydantic, Transformers.
   * Cargar modelo Hugging Face localmente:

     ```python
     from fastapi import FastAPI
     from pydantic import BaseModel
     from transformers import AutoModelForCausalLM, AutoTokenizer

     app = FastAPI()
     tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
     model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-medium')

     class Message(BaseModel):
         user: str

     @app.post('/chat')
     async def chat(msg: Message):
         inputs = tokenizer.encode(msg.user + tokenizer.eos_token, return_tensors='pt')
         outputs = model.generate(inputs, max_length=200)
         response = tokenizer.decode(outputs[0], skip_special_tokens=True)
         return {'bot': response}
     ```

2. **Crear `backend/requirements.txt`**:

   ```
   ```

fastapi
uvicorn
transformers\[torch]
python-dotenv
sqlite-utils

````
3. **Configurar variables de entorno** en `backend/.env` (vacío por ahora):
   ```text
   # Puedes añadir variables como MODEL_PATH o TOKENS en el futuro
````

4. **Ejecutar el servicio**:

   ```bash
   cd backend
   uvicorn chatbot_api:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Probar endpoint**:

   ```bash
   curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"user": "Hola"}'
   ```

---

## 3. API de Gestión de Citas (FastAPI + SQLite)

1. **Archivo `backend/citas_api.py`**:

   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel
   import sqlite_utils

   app = FastAPI()
   db = sqlite_utils.Database('citas.db')
   if 'citas' not in db.table_names():
       db['citas'].create({ 'id': int, 'nombre': str, 'email': str, 'fecha': str }, pk='id')

   class Cita(BaseModel):
       nombre: str
       email: str
       fecha: str  # ISO 8601

   @app.post('/cita')
   async def crear_cita(cita: Cita):
       record = db['citas'].insert(cita.dict())
       return record

   @app.get('/citas')
   async def listar_citas():
       return list(db['citas'].rows)
   ```

2. **Ejecutar** junto a `chatbot_api`: en otro terminal:

   ```bash
   uvicorn citas_api:app --reload --port 8001
   ```

---

## 4. Front-end Web (HTML + JS)

1. **Modificar `frontend/index.html`**:

   * Incluir áreas para chat y calendario.
   * Botón “Enviar” que llame a `chatbot.js`.

2. **Archivo `frontend/chatbot.js`**:

   ```js
   async function enviarPregunta() {
     const input = document.getElementById('userInput');
     const output = document.getElementById('chatOutput');
     const pregunta = input.value.trim(); if (!pregunta) return;
     output.innerHTML += `<p><strong>Tú:</strong> ${pregunta}</p>`;
     const resp = await fetch('http://localhost:8000/chat', {
       method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({ user: pregunta })
     });
     const data = await resp.json();
     output.innerHTML += `<p><strong>Bot:</strong> ${data.bot}</p>`;
     input.value = '';
   }
   ```

3. **Archivo `frontend/calendario.js`**:

   * Inicializar FullCalendar.
   * GET `/citas` para cargar.
   * POST `/cita` al seleccionar fecha.

---

## 5. Exponer APIs con Ngrok

1. **Instalar Ngrok** y configurar `ngrok-config.yml` si es necesario.
2. **Ejecutar túnel**:

   ```bash
   ngrok http 8000 --config=ngrok-config.yml
   ngrok http 8001 --config=ngrok-config.yml
   ```
3. **Copiar URL pública** para configurar webhooks de WhatsApp y Messenger.

---

## 6. Webhook de WhatsApp Business Cloud API

1. **Configurar en Meta Developers**: crear App, agregar WhatsApp.
2. **Obtener token y número de prueba**.
3. **En `backend/chatbot_api.py`** añadir ruta webhook:

   ```python
   @app.post('/webhook_whatsapp')
   async def whatsapp_webhook(payload: dict):
       texto = payload['messages'][0]['text']['body']
       bot = (await chat(Message(user=texto)))['bot']
       # Llamar a la API de WhatsApp para responder usando requests
       return {'status':'ok'}
   ```
4. **Configurar URL de webhook** en consola de Meta con la URL de Ngrok.

---

## 7. Webhook de Facebook Messenger

1. **Configurar página y App** en Meta Developers.
2. **En `backend/chatbot_api.py`**:

   ```python
   @app.get('/webhook_messenger')  # verificación
   def verify_token(...):
       return challenge

   @app.post('/webhook_messenger')
   async def messenger_webhook(payload: dict):
       texto = payload['entry'][0]['messaging'][0]['message']['text']
       bot = (await chat(Message(user=texto)))['bot']
       # Llamar a Graph API para responder
       return {'status':'ok'}
   ```
3. **Registrar webhook** y permisos: `pages_messaging`, `pages_messaging_subscriptions`.

---

## 8. Integración del Modelo de Predicción de Sentencias

1. **Implementar `backend/predict_api.py`** similar a `chatbot_api.py`:

   * POST `/predecir` recibe datos de caso y devuelve probabilidad.
2. **Cargar modelo propio** (transformers, scikit-learn o PyTorch).
3. **JS en Front-end** para llamarlo y mostrar resultados.

---

## 9. Siguientes Pasos y Despliegue

* **Pruebas end-to-end**: chat web, WhatsApp, Messenger, citas y predicción.
* **Migración a VPS** o contenedor cuando sea necesario.
* **Monitoreo y logs** con `sqlite-utils` o integraciones externas.

---

Este guion detallado cubre todos los objetivos iniciales con **costo \$0** y maximiza el uso de software libre y recursos propios.
