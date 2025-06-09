"""
Chatbot Offline para Despacho Jurídico
=====================================
Sistema de chatbot que funciona completamente offline para responder 
preguntas básicas sobre servicios legales, costos y agendar citas.

Funcionalidades:
- Respuestas predefinidas sobre servicios legales
- Información de costos y contacto
- Sistema de agendamiento de citas
- Base de conocimiento legal básica
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import sqlite3
import json
import re
from typing import List, Dict, Optional

app = FastAPI(
    title="Despacho Jurídico - Chatbot Offline",
    description="Chatbot especializado en servicios legales",
    version="1.0.0"
)

# Configurar CORS para permitir requests desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class ChatMessage(BaseModel):
    mensaje: str
    usuario_id: Optional[str] = "anonimo"

class CitaRequest(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    fecha: str  # formato: "YYYY-MM-DD HH:MM"
    tipo_servicio: str
    descripcion: Optional[str] = ""

class ChatResponse(BaseModel):
    respuesta: str
    sugerencias: List[str] = []
    requiere_cita: bool = False

# Base de conocimiento del despacho jurídico
KNOWLEDGE_BASE = {
    "servicios": {
        "civil": {
            "descripcion": "Derecho Civil - Contratos, sucesiones, responsabilidad civil",
            "costo": "Consulta: $200.000 - Representación: desde $500.000",
            "tiempo": "1-6 meses según complejidad"
        },
        "penal": {
            "descripcion": "Derecho Penal - Defensa criminal, delitos menores y graves",
            "costo": "Consulta: $250.000 - Representación: desde $800.000",
            "tiempo": "3-18 meses según proceso"
        },
        "laboral": {
            "descripcion": "Derecho Laboral - Despidos, indemnizaciones, conflictos laborales",
            "costo": "Consulta: $180.000 - Representación: desde $400.000",
            "tiempo": "2-8 meses según caso"
        },
        "familia": {
            "descripcion": "Derecho de Familia - Divorcios, custodia, alimentos",
            "costo": "Consulta: $200.000 - Representación: desde $600.000",
            "tiempo": "4-12 meses según acuerdo"
        }
    },
    "contacto": {
        "direccion": "Calle 123 #45-67, Centro Legal, Bogotá",
        "telefono": "+57 (1) 234-5678",
        "email": "contacto@despachojuridico.com",
        "horarios": "Lunes a Viernes: 8:00 AM - 6:00 PM"
    },
    "preguntas_frecuentes": {
        "primera_consulta": "La primera consulta tiene un costo de $150.000 y dura 1 hora",
        "documentos": "Debe traer cédula, documentos relacionados al caso y poder si aplica",
        "urgencias": "Para urgencias puede llamar al +57 300 123-4567 las 24 horas",
        "formas_pago": "Aceptamos efectivo, transferencia, tarjetas de crédito y financiación"
    }
}

# Patrones de conversación
CONVERSATION_PATTERNS = {
    r'(hola|buenos días|buenas tardes|buenas noches|saludos)': [
        "¡Hola! Bienvenido al Despacho Jurídico Virtual. ¿En qué puedo ayudarte hoy?",
        "Buenos días, soy el asistente virtual del despacho. ¿Qué consulta legal tienes?",
        "¡Saludos! Estoy aquí para ayudarte con tus necesidades legales."
    ],
    r'(servicios|que hacen|areas|especialidades)': [
        "Ofrecemos servicios en las siguientes áreas legales:",
        "Nuestras especialidades incluyen:"
    ],
    r'(costo|precio|cuanto cuesta|tarifa|honorarios)': [
        "Nuestros costos varían según el tipo de servicio:",
        "Te puedo informar sobre nuestras tarifas:"
    ],
    r'(contacto|direccion|telefono|ubicacion|donde)': [
        "Nuestra información de contacto es:",
        "Puedes contactarnos por estos medios:"
    ],
    r'(cita|agendar|reservar|turno|consulta)': [
        "Te puedo ayudar a agendar una cita. Necesito algunos datos.",
        "Perfecto, agendemos tu consulta legal."
    ],
    r'(urgencia|emergencia|urgente)': [
        "Para urgencias legales puedes contactarnos:",
        "En casos urgentes:"
    ]
}

def init_database():
    """Inicializar base de datos SQLite para citas"""
    conn = sqlite3.connect('despacho.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha DATETIME NOT NULL,
            tipo_servicio TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'pendiente',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT,
            mensaje TEXT NOT NULL,
            respuesta TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def analyze_message(mensaje: str) -> Dict:
    """Analizar mensaje del usuario y determinar intención"""
    mensaje_lower = mensaje.lower()
    
    # Detectar patrones de conversación
    for pattern, responses in CONVERSATION_PATTERNS.items():
        if re.search(pattern, mensaje_lower):
            return {
                "pattern": pattern,
                "responses": responses,
                "intent": get_intent_from_pattern(pattern)
            }
    
    return {"pattern": None, "responses": [], "intent": "general"}

def get_intent_from_pattern(pattern: str) -> str:
    """Determinar intención basada en el patrón"""
    intent_map = {
        r'(hola|buenos días|buenas tardes|buenas noches|saludos)': 'saludo',
        r'(servicios|que hacen|areas|especialidades)': 'servicios',
        r'(costo|precio|cuanto cuesta|tarifa|honorarios)': 'costos',
        r'(contacto|direccion|telefono|ubicacion|donde)': 'contacto',
        r'(cita|agendar|reservar|turno|consulta)': 'cita',
        r'(urgencia|emergencia|urgente)': 'urgencia'
    }
    return intent_map.get(pattern, 'general')

def generate_response(mensaje: str, analysis: Dict) -> ChatResponse:
    """Generar respuesta basada en el análisis del mensaje"""
    intent = analysis["intent"]
    
    if intent == "saludo":
        return ChatResponse(
            respuesta=analysis["responses"][0],
            sugerencias=[
                "Ver servicios disponibles",
                "Consultar costos",
                "Agendar una cita",
                "Información de contacto"
            ]
        )
    
    elif intent == "servicios":
        respuesta = analysis["responses"][0] + "\n\n"
        for servicio, info in KNOWLEDGE_BASE["servicios"].items():
            respuesta += f"• **{servicio.title()}**: {info['descripcion']}\n"
        
        return ChatResponse(
            respuesta=respuesta,
            sugerencias=[
                "Ver costos de servicios",
                "Agendar consulta",
                "Más información de contacto"
            ]
        )
    
    elif intent == "costos":
        respuesta = analysis["responses"][0] + "\n\n"
        for servicio, info in KNOWLEDGE_BASE["servicios"].items():
            respuesta += f"• **{servicio.title()}**: {info['costo']}\n"
        
        respuesta += f"\n📋 **Primera consulta**: {KNOWLEDGE_BASE['preguntas_frecuentes']['primera_consulta']}"
        
        return ChatResponse(
            respuesta=respuesta,
            sugerencias=[
                "Agendar primera consulta",
                "Ver formas de pago",
                "Contactar para más información"
            ]
        )
    
    elif intent == "contacto":
        contacto = KNOWLEDGE_BASE["contacto"]
        respuesta = f"""
📍 **Dirección**: {contacto['direccion']}
📞 **Teléfono**: {contacto['telefono']}
📧 **Email**: {contacto['email']}
🕒 **Horarios**: {contacto['horarios']}
        """
        
        return ChatResponse(
            respuesta=respuesta,
            sugerencias=[
                "Agendar cita",
                "Ver servicios",
                "Consultar costos"
            ]
        )
    
    elif intent == "cita":
        return ChatResponse(
            respuesta="Te ayudo a agendar tu cita. Por favor proporciona los siguientes datos:",
            sugerencias=[
                "Nombre completo",
                "Email de contacto", 
                "Teléfono",
                "Fecha preferida",
                "Tipo de consulta"
            ],
            requiere_cita=True
        )
    
    elif intent == "urgencia":
        return ChatResponse(
            respuesta=f"🚨 **Para urgencias legales**:\n{KNOWLEDGE_BASE['preguntas_frecuentes']['urgencias']}",
            sugerencias=[
                "Agendar cita regular",
                "Ver servicios",
                "Información de contacto"
            ]
        )
    
    else:
        return ChatResponse(
            respuesta="Entiendo tu consulta. ¿Podrías ser más específico? Te puedo ayudar con información sobre servicios, costos, agendar citas o datos de contacto.",
            sugerencias=[
                "Ver servicios legales",
                "Consultar costos",
                "Agendar una cita",
                "Información de contacto"
            ]
        )

@app.on_event("startup")
async def startup_event():
    init_database()

@app.get("/")
async def root():
    return {
        "mensaje": "Despacho Jurídico Virtual - Chatbot API",
        "version": "1.0.0",
        "status": "online"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(mensaje: ChatMessage):
    """Endpoint principal del chatbot"""
    try:
        # Analizar mensaje
        analysis = analyze_message(mensaje.mensaje)
        
        # Generar respuesta
        response = generate_response(mensaje.mensaje, analysis)
        
        # Guardar conversación
        conn = sqlite3.connect('despacho.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversaciones (usuario_id, mensaje, respuesta) VALUES (?, ?, ?)",
            (mensaje.usuario_id, mensaje.mensaje, response.respuesta)
        )
        conn.commit()
        conn.close()
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando mensaje: {str(e)}")

@app.post("/agendar_cita")
async def agendar_cita(cita: CitaRequest):
    """Endpoint para agendar citas"""
    try:
        # Validar fecha
        fecha_cita = datetime.strptime(cita.fecha, "%Y-%m-%d %H:%M")
        if fecha_cita < datetime.now():
            raise HTTPException(status_code=400, detail="La fecha debe ser futura")
        
        # Verificar disponibilidad (simplificado)
        conn = sqlite3.connect('despacho.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT COUNT(*) FROM citas WHERE DATE(fecha) = DATE(?) AND estado != 'cancelada'",
            (fecha_cita,)
        )
        citas_existentes = cursor.fetchone()[0]
        
        if citas_existentes >= 8:  # Máximo 8 citas por día
            raise HTTPException(status_code=400, detail="No hay disponibilidad para esa fecha")
        
        # Insertar cita
        cursor.execute('''
            INSERT INTO citas (nombre, email, telefono, fecha, tipo_servicio, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (cita.nombre, cita.email, cita.telefono, fecha_cita, cita.tipo_servicio, cita.descripcion))
        
        cita_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "cita_id": cita_id,
            "mensaje": f"Cita agendada exitosamente para {fecha_cita.strftime('%d/%m/%Y a las %H:%M')}",
            "detalles": {
                "fecha": fecha_cita.isoformat(),
                "servicio": cita.tipo_servicio,
                "id": cita_id
            }
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use: YYYY-MM-DD HH:MM")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error agendando cita: {str(e)}")

@app.get("/citas")
async def listar_citas():
    """Endpoint para listar citas (admin)"""
    try:
        conn = sqlite3.connect('despacho.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, email, telefono, fecha, tipo_servicio, descripcion, estado, created_at
            FROM citas 
            ORDER BY fecha ASC
        ''')
        
        citas = []
        for row in cursor.fetchall():
            citas.append({
                "id": row[0],
                "nombre": row[1],
                "email": row[2],
                "telefono": row[3],
                "fecha": row[4],
                "tipo_servicio": row[5],
                "descripcion": row[6],
                "estado": row[7],
                "created_at": row[8]
            })
        
        conn.close()
        return {"citas": citas}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo citas: {str(e)}")

@app.get("/horarios_disponibles/{fecha}")
async def horarios_disponibles(fecha: str):
    """Obtener horarios disponibles para una fecha específica"""
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        
        # Horarios de trabajo: 8:00 AM a 6:00 PM
        horarios_trabajo = []
        for hora in range(8, 18):
            horarios_trabajo.append(f"{hora:02d}:00")
        
        # Obtener citas existentes
        conn = sqlite3.connect('despacho.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT TIME(fecha) FROM citas WHERE DATE(fecha) = ? AND estado != 'cancelada'",
            (fecha_obj.date(),)
        )
        
        horarios_ocupados = [row[0][:5] for row in cursor.fetchall()]  # Formato HH:MM
        conn.close()
        
        # Filtrar horarios disponibles
        horarios_disponibles = [h for h in horarios_trabajo if h not in horarios_ocupados]
        
        return {
            "fecha": fecha,
            "horarios_disponibles": horarios_disponibles,
            "horarios_ocupados": horarios_ocupados
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use: YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo horarios: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
