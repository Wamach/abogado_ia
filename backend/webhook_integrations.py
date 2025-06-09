"""
Integraciones de Webhooks para WhatsApp y Facebook Messenger
===========================================================
Sistema que maneja webhooks de WhatsApp Business Cloud API y Facebook Messenger
para integrar el chatbot con redes sociales.

Funcionalidades:
- Webhook para WhatsApp Business Cloud API
- Webhook para Facebook Messenger
- Verificación de tokens
- Envío de respuestas automáticas
- Logging de conversaciones
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import sqlite3
import json
import hmac
import hashlib
import os
from datetime import datetime
from typing import Dict, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Webhook Integrations - Despacho Jurídico",
    description="Integraciones con WhatsApp y Facebook Messenger",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de entorno (configurar en .env)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")
MESSENGER_PAGE_TOKEN = os.getenv("MESSENGER_PAGE_TOKEN", "")
MESSENGER_VERIFY_TOKEN = os.getenv("MESSENGER_VERIFY_TOKEN", "test_verify_token")
MESSENGER_APP_SECRET = os.getenv("MESSENGER_APP_SECRET", "")

# URL del chatbot local
CHATBOT_URL = "http://localhost:8000/chat"

# Modelos de datos
class WhatsAppMessage(BaseModel):
    object: str
    entry: list

class MessengerMessage(BaseModel):
    object: str
    entry: list

def init_webhook_db():
    """Inicializar base de datos para webhooks"""
    conn = sqlite3.connect('webhook_conversations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhook_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_webhook_message(platform: str, sender_id: str, message: str, response: str = ""):
    """Guardar mensaje de webhook en la base de datos"""
    try:
        conn = sqlite3.connect('webhook_conversations.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO webhook_messages (platform, sender_id, message, response)
            VALUES (?, ?, ?, ?)
        ''', (platform, sender_id, message, response))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error guardando mensaje: {e}")

async def get_chatbot_response(message: str) -> str:
    """Obtener respuesta del chatbot local"""
    try:
        response = requests.post(
            CHATBOT_URL,
            json={"mensaje": message},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("respuesta", "Lo siento, no pude procesar tu consulta.")
        else:
            return "Servicio temporalmente no disponible. Por favor intenta más tarde."
            
    except Exception as e:
        logger.error(f"Error obteniendo respuesta del chatbot: {e}")
        return "Lo siento, hay un problema técnico. Contacta directamente con nosotros."

def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """Enviar mensaje via WhatsApp Business Cloud API"""
    if not WHATSAPP_TOKEN:
        logger.error("Token de WhatsApp no configurado")
        return False
    
    url = f"https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {
            "body": message
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error enviando WhatsApp: {e}")
        return False

def send_messenger_message(sender_id: str, message: str) -> bool:
    """Enviar mensaje via Facebook Messenger"""
    if not MESSENGER_PAGE_TOKEN:
        logger.error("Token de Messenger no configurado")
        return False
    
    url = f"https://graph.facebook.com/v17.0/me/messages"
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "recipient": {"id": sender_id},
        "message": {"text": message},
        "access_token": MESSENGER_PAGE_TOKEN
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error enviando Messenger: {e}")
        return False

# === WEBHOOKS DE WHATSAPP ===

@app.get("/webhook/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Verificación del webhook de WhatsApp"""
    if hub_mode == "subscribe" and hub_verify_token == WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook de WhatsApp verificado exitosamente")
        return int(hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Token de verificación inválido")

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """Webhook para recibir mensajes de WhatsApp"""
    try:
        body = await request.json()
        logger.info(f"Webhook WhatsApp recibido: {json.dumps(body, indent=2)}")
        
        if body.get("object") == "whatsapp_business_account":
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        value = change.get("value", {})
                        
                        # Procesar mensajes entrantes
                        for message in value.get("messages", []):
                            phone_number = message.get("from")
                            message_text = message.get("text", {}).get("body", "")
                            
                            if phone_number and message_text:
                                # Obtener respuesta del chatbot
                                response = await get_chatbot_response(message_text)
                                
                                # Guardar en base de datos
                                save_webhook_message("whatsapp", phone_number, message_text, response)
                                
                                # Enviar respuesta
                                if send_whatsapp_message(phone_number, response):
                                    logger.info(f"Respuesta enviada a WhatsApp: {phone_number}")
                                else:
                                    logger.error(f"Error enviando respuesta a WhatsApp: {phone_number}")
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error procesando webhook WhatsApp: {e}")
        raise HTTPException(status_code=500, detail="Error procesando webhook")

# === WEBHOOKS DE FACEBOOK MESSENGER ===

@app.get("/webhook/messenger")
async def verify_messenger_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Verificación del webhook de Messenger"""
    if hub_mode == "subscribe" and hub_verify_token == MESSENGER_VERIFY_TOKEN:
        logger.info("Webhook de Messenger verificado exitosamente")
        return int(hub_challenge)
    else:
        raise HTTPException(status_code=403, detail="Token de verificación inválido")

@app.post("/webhook/messenger")
async def messenger_webhook(request: Request):
    """Webhook para recibir mensajes de Facebook Messenger"""
    try:
        body = await request.json()
        logger.info(f"Webhook Messenger recibido: {json.dumps(body, indent=2)}")
        
        if body.get("object") == "page":
            for entry in body.get("entry", []):
                for messaging in entry.get("messaging", []):
                    sender_id = messaging.get("sender", {}).get("id")
                    message = messaging.get("message", {})
                    message_text = message.get("text", "")
                    
                    if sender_id and message_text:
                        # Obtener respuesta del chatbot
                        response = await get_chatbot_response(message_text)
                        
                        # Guardar en base de datos
                        save_webhook_message("messenger", sender_id, message_text, response)
                        
                        # Enviar respuesta
                        if send_messenger_message(sender_id, response):
                            logger.info(f"Respuesta enviada a Messenger: {sender_id}")
                        else:
                            logger.error(f"Error enviando respuesta a Messenger: {sender_id}")
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error procesando webhook Messenger: {e}")
        raise HTTPException(status_code=500, detail="Error procesando webhook")

# === ENDPOINTS ADMINISTRATIVOS ===

@app.get("/webhook/stats")
async def get_webhook_stats():
    """Obtener estadísticas de conversaciones por webhook"""
    try:
        conn = sqlite3.connect('webhook_conversations.db')
        cursor = conn.cursor()
        
        # Estadísticas por plataforma
        cursor.execute('''
            SELECT platform, COUNT(*) as total_messages,
                   COUNT(DISTINCT sender_id) as unique_users
            FROM webhook_messages
            GROUP BY platform
        ''')
        
        platform_stats = cursor.fetchall()
        
        # Mensajes recientes
        cursor.execute('''
            SELECT platform, sender_id, message, response, timestamp
            FROM webhook_messages
            ORDER BY timestamp DESC
            LIMIT 20
        ''')
        
        recent_messages = cursor.fetchall()
        
        conn.close()
        
        return {
            "platform_stats": [
                {"platform": row[0], "total_messages": row[1], "unique_users": row[2]}
                for row in platform_stats
            ],
            "recent_messages": [
                {
                    "platform": row[0],
                    "sender_id": row[1],
                    "message": row[2],
                    "response": row[3],
                    "timestamp": row[4]
                }
                for row in recent_messages
            ]
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")

@app.get("/health")
async def health_check():
    """Verificar estado del servicio"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "whatsapp_configured": bool(WHATSAPP_TOKEN),
        "messenger_configured": bool(MESSENGER_PAGE_TOKEN)
    }

# Inicializar base de datos al arrancar
init_webhook_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
