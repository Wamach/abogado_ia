"""
ETAPA 2: Modelo Legal con Hugging Face y Gradio
===============================================
Sistema avanzado de IA legal que utiliza modelos de Hugging Face
para análisis de texto legal, clasificación de casos y generación de documentos.

Funcionalidades:
- Análisis de sentimientos en consultas legales
- Clasificación automática de tipos de casos
- Generación de resúmenes legales
- Extracción de entidades legales (nombres, fechas, montos)
- Interface web con Gradio
"""

import gradio as gr
import pandas as pd
import numpy as np
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    AutoModelForTokenClassification, pipeline,
    AutoModelForCausalLM
)
import torch
from datetime import datetime
import re
import json
import sqlite3
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuración de modelos
MODELS_CONFIG = {
    "sentiment": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "ner": "mrm8488/bert-spanish-cased-finetuned-ner",
    "classification": "dccuchile/bert-base-spanish-wwm-uncased",
    "generation": "microsoft/DialoGPT-medium"
}

class LegalAISystem:
    """Sistema de IA Legal con múltiples modelos especializados"""
    
    def __init__(self):
        self.models = {}
        self.pipelines = {}
        self.legal_categories = {
            "civil": "Derecho Civil",
            "penal": "Derecho Penal", 
            "laboral": "Derecho Laboral",
            "familia": "Derecho de Familia",
            "comercial": "Derecho Comercial",
            "constitucional": "Derecho Constitucional"
        }
        self.load_models()
        self.init_database()
    
    def load_models(self):
        """Cargar todos los modelos de IA necesarios"""
        print("🤖 Cargando modelos de IA legal...")
        
        try:
            # Modelo de análisis de sentimientos
            print("📊 Cargando modelo de análisis de sentimientos...")
            self.pipelines["sentiment"] = pipeline(
                "sentiment-analysis",
                model=MODELS_CONFIG["sentiment"],
                return_all_scores=True
            )
            
            # Modelo de reconocimiento de entidades nombradas (NER)
            print("🏷️ Cargando modelo de reconocimiento de entidades...")
            self.pipelines["ner"] = pipeline(
                "ner",
                model=MODELS_CONFIG["ner"],
                aggregation_strategy="simple"
            )
            
            # Modelo de generación de texto
            print("✍️ Cargando modelo de generación de texto...")
            self.pipelines["generation"] = pipeline(
                "text-generation",
                model=MODELS_CONFIG["generation"],
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            
            print("✅ Todos los modelos cargados exitosamente!")
            
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            # Fallback a modelos más simples si hay problemas
            self.load_fallback_models()
    
    def load_fallback_models(self):
        """Cargar modelos de respaldo más ligeros"""
        print("🔄 Cargando modelos de respaldo...")
        try:
            self.pipelines["sentiment"] = pipeline("sentiment-analysis")
            print("✅ Modelos de respaldo cargados")
        except Exception as e:
            print(f"❌ Error con modelos de respaldo: {e}")
    
    def init_database(self):
        """Inicializar base de datos para almacenar análisis"""
        conn = sqlite3.connect('legal_ai.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis_legal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto_original TEXT NOT NULL,
                sentimiento TEXT,
                confianza_sentimiento REAL,
                categoria_legal TEXT,
                entidades_extraidas TEXT,
                resumen_generado TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def analyze_sentiment(self, texto: str) -> Dict:
        """Analizar sentimiento del texto legal"""
        try:
            if "sentiment" not in self.pipelines:
                return {"sentimiento": "neutral", "confianza": 0.5, "detalles": "Modelo no disponible"}
            
            resultado = self.pipelines["sentiment"](texto)
            
            if isinstance(resultado[0], list):
                # Formato con múltiples scores
                sentimientos = resultado[0]
                mejor = max(sentimientos, key=lambda x: x['score'])
                return {
                    "sentimiento": mejor['label'].lower(),
                    "confianza": mejor['score'],
                    "detalles": sentimientos
                }
            else:
                # Formato simple
                return {
                    "sentimiento": resultado[0]['label'].lower(),
                    "confianza": resultado[0]['score'],
                    "detalles": resultado
                }
                
        except Exception as e:
            return {"sentimiento": "neutral", "confianza": 0.5, "error": str(e)}
    
    def extract_entities(self, texto: str) -> List[Dict]:
        """Extraer entidades nombradas del texto legal"""
        try:
            if "ner" not in self.pipelines:
                return self.extract_entities_regex(texto)
            
            entidades = self.pipelines["ner"](texto)
            
            # Procesar y limpiar entidades
            entidades_procesadas = []
            for entidad in entidades:
                entidades_procesadas.append({
                    "texto": entidad.get("word", ""),
                    "etiqueta": entidad.get("entity_group", entidad.get("label", "")),
                    "confianza": entidad.get("score", 0.0),
                    "inicio": entidad.get("start", 0),
                    "fin": entidad.get("end", 0)
                })
            
            return entidades_procesadas
            
        except Exception as e:
            print(f"Error en NER: {e}")
            return self.extract_entities_regex(texto)
    
    def extract_entities_regex(self, texto: str) -> List[Dict]:
        """Extracción de entidades usando expresiones regulares como fallback"""
        entidades = []
        
        # Patrones para entidades legales comunes
        patrones = {
            "PERSONA": r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            "FECHA": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            "DINERO": r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d{1,3}(?:,\d{3})*\s*pesos',
            "CEDULA": r'\b\d{8,10}\b',
            "EXPEDIENTE": r'\b(?:exp|expediente|caso)\s*[:\-]?\s*\d+[/-]\d+\b',
        }
        
        for etiqueta, patron in patrones.items():
            coincidencias = re.finditer(patron, texto, re.IGNORECASE)
            for coincidencia in coincidencias:
                entidades.append({
                    "texto": coincidencia.group(),
                    "etiqueta": etiqueta,
                    "confianza": 0.8,
                    "inicio": coincidencia.start(),
                    "fin": coincidencia.end()
                })
        
        return entidades
    
    def classify_legal_case(self, texto: str) -> Dict:
        """Clasificar el tipo de caso legal basado en el texto"""
        # Palabras clave para cada categoría legal
        keywords_categories = {
            "civil": ["contrato", "sucesión", "herencia", "propiedad", "arrendamiento", "responsabilidad civil"],
            "penal": ["delito", "robo", "hurto", "lesiones", "homicidio", "estafa", "denuncia"],
            "laboral": ["despido", "liquidación", "salario", "trabajo", "empleado", "empresa", "incapacidad"],
            "familia": ["divorcio", "custodia", "alimentos", "matrimonio", "separación", "adopción"],
            "comercial": ["empresa", "sociedad", "comercio", "negocio", "factura", "pago"],
            "constitucional": ["derechos", "tutela", "constitución", "amparo", "fundamental"]
        }
        
        texto_lower = texto.lower()
        scores = {}
        
        for categoria, keywords in keywords_categories.items():
            score = sum(1 for keyword in keywords if keyword in texto_lower)
            scores[categoria] = score / len(keywords)  # Normalizar score
        
        if not any(scores.values()):
            return {"categoria": "general", "confianza": 0.3, "nombre": "Consulta General"}
        
        mejor_categoria = max(scores, key=scores.get)
        confianza = scores[mejor_categoria]
        
        return {
            "categoria": mejor_categoria,
            "confianza": confianza,
            "nombre": self.legal_categories.get(mejor_categoria, "Otro"),
            "scores": scores
        }
    
    def generate_legal_summary(self, texto: str) -> str:
        """Generar resumen legal del texto"""
        try:
            if "generation" in self.pipelines:
                # Usar modelo de generación si está disponible
                prompt = f"Resumen legal: {texto[:100]}..."
                resultado = self.pipelines["generation"](prompt, max_length=150, num_return_sequences=1)
                return resultado[0]['generated_text'][len(prompt):].strip()
            else:
                # Resumen extractivo simple
                return self.extractive_summary(texto)
                
        except Exception as e:
            return self.extractive_summary(texto)
    
    def extractive_summary(self, texto: str) -> str:
        """Resumen extractivo simple basado en oraciones importantes"""
        oraciones = texto.split('.')
        if len(oraciones) <= 2:
            return texto
        
        # Seleccionar las 2 primeras oraciones como resumen
        resumen = '. '.join(oraciones[:2]).strip()
        if resumen and not resumen.endswith('.'):
            resumen += '.'
        
        return resumen or "Resumen no disponible."
    
    def full_legal_analysis(self, texto: str) -> Dict:
        """Análisis legal completo del texto"""
        print(f"🔍 Analizando texto: {texto[:50]}...")
        
        # Realizar todos los análisis
        sentimiento = self.analyze_sentiment(texto)
        entidades = self.extract_entities(texto)
        clasificacion = self.classify_legal_case(texto)
        resumen = self.generate_legal_summary(texto)
        
        # Compilar resultados
        resultado = {
            "texto_original": texto,
            "sentimiento": sentimiento,
            "entidades": entidades,
            "clasificacion": clasificacion,
            "resumen": resumen,
            "timestamp": datetime.now().isoformat()
        }
        
        # Guardar en base de datos
        self.save_analysis(resultado)
        
        return resultado
    
    def save_analysis(self, analisis: Dict):
        """Guardar análisis en la base de datos"""
        try:
            conn = sqlite3.connect('legal_ai.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO analisis_legal (
                    texto_original, sentimiento, confianza_sentimiento,
                    categoria_legal, entidades_extraidas, resumen_generado
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                analisis["texto_original"],
                analisis["sentimiento"]["sentimiento"],
                analisis["sentimiento"]["confianza"],
                analisis["clasificacion"]["categoria"],
                json.dumps(analisis["entidades"]),
                analisis["resumen"]
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error guardando análisis: {e}")

# Instancia global del sistema
legal_ai = LegalAISystem()

def format_analysis_output(analisis: Dict) -> Tuple[str, str, str, str, str]:
    """Formatear salida del análisis para Gradio"""
    
    # Sentimiento
    sentimiento_info = analisis["sentimiento"]
    sentimiento_text = f"""
    **Sentimiento**: {sentimiento_info['sentimiento'].title()}
    **Confianza**: {sentimiento_info['confianza']:.2%}
    """
    
    # Clasificación
    clasificacion_info = analisis["clasificacion"]
    clasificacion_text = f"""
    **Categoría Legal**: {clasificacion_info['nombre']}
    **Confianza**: {clasificacion_info['confianza']:.2%}
    """
    
    # Entidades
    entidades_text = "**Entidades Encontradas:**\n"
    if analisis["entidades"]:
        for entidad in analisis["entidades"][:10]:  # Limitar a 10 entidades
            entidades_text += f"• {entidad['texto']} ({entidad['etiqueta']}) - {entidad['confianza']:.1%}\n"
    else:
        entidades_text += "No se encontraron entidades relevantes."
    
    # Resumen
    resumen_text = f"**Resumen Generado:**\n{analisis['resumen']}"
    
    # Información general
    info_general = f"""
    **Análisis Legal Completo**
    
    **Texto analizado**: {len(analisis['texto_original'])} caracteres
    **Fecha de análisis**: {analisis['timestamp']}
    **Categoría detectada**: {clasificacion_info['nombre']}
    """
    
    return info_general, sentimiento_text, clasificacion_text, entidades_text, resumen_text

def analyze_legal_text(texto: str):
    """Función principal para la interface de Gradio"""
    if not texto or len(texto.strip()) < 10:
        return "Por favor ingrese un texto legal de al menos 10 caracteres.", "", "", "", ""
    
    try:
        analisis = legal_ai.full_legal_analysis(texto)
        return format_analysis_output(analisis)
    except Exception as e:
        error_msg = f"Error en el análisis: {str(e)}"
        return error_msg, "", "", "", ""

def get_statistics():
    """Obtener estadísticas de análisis realizados"""
    try:
        conn = sqlite3.connect('legal_ai.db')
        cursor = conn.cursor()
        
        # Contar análisis por categoría
        cursor.execute('''
            SELECT categoria_legal, COUNT(*) as count 
            FROM analisis_legal 
            GROUP BY categoria_legal
        ''')
        
        categorias = cursor.fetchall()
        
        # Total de análisis
        cursor.execute('SELECT COUNT(*) FROM analisis_legal')
        total = cursor.fetchone()[0]
        
        conn.close()
        
        if total == 0:
            return "No hay análisis realizados aún."
        
        stats_text = f"**Estadísticas de Análisis Legal**\n\n"
        stats_text += f"**Total de análisis**: {total}\n\n"
        stats_text += "**Por categoría:**\n"
        
        for categoria, count in categorias:
            porcentaje = (count / total) * 100
            stats_text += f"• {categoria.title()}: {count} ({porcentaje:.1f}%)\n"
        
        return stats_text
        
    except Exception as e:
        return f"Error obteniendo estadísticas: {e}"

# Crear interface de Gradio
def create_gradio_interface():
    """Crear la interface web con Gradio"""
    
    with gr.Blocks(
        title="🤖⚖️ Sistema de IA Legal - Despacho Jurídico Virtual",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .header {
            text-align: center;
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 10px;
        }
        """
    ) as interface:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🤖⚖️ Sistema de IA Legal</h1>
            <p>Análisis inteligente de textos legales con modelos de Hugging Face</p>
        </div>
        """)
        
        with gr.Tab("📝 Análisis de Texto Legal"):
            gr.Markdown("""
            ### Analizar Consulta Legal
            Ingrese el texto de su consulta legal para obtener un análisis completo que incluye:
            - 📊 Análisis de sentimientos
            - 🏷️ Clasificación del tipo de caso
            - 🔍 Extracción de entidades legales
            - 📄 Resumen automático
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    texto_input = gr.Textbox(
                        lines=8,
                        placeholder="Ingrese aquí su consulta legal...\n\nEjemplo: 'Mi empleador me despidió sin justa causa después de 5 años de trabajo. No me pagó la liquidación completa y debo $2,000,000 pesos de indemnización según mi contrato.'",
                        label="Texto Legal a Analizar"
                    )
                    
                    analyze_btn = gr.Button("🔍 Analizar Texto", variant="primary", size="lg")
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    **Ejemplos de consultas:**
                    
                    📋 **Laboral**: "Me despidieron sin causa justa..."
                    
                    👨‍👩‍👧 **Familia**: "Quiero el divorcio y custodia..."
                    
                    🏠 **Civil**: "Problemas con contrato de arrendamiento..."
                    
                    ⚖️ **Penal**: "Quiero denunciar un robo..."
                    """)
            
            # Outputs del análisis
            with gr.Row():
                info_general = gr.Textbox(label="📋 Información General", lines=6)
                sentimiento = gr.Textbox(label="😊 Análisis de Sentimientos", lines=6)
            
            with gr.Row():
                clasificacion = gr.Textbox(label="📂 Clasificación Legal", lines=6)
                entidades = gr.Textbox(label="🏷️ Entidades Extraídas", lines=6)
            
            resumen = gr.Textbox(label="📄 Resumen Generado", lines=4)
            
            # Conectar función
            analyze_btn.click(
                fn=analyze_legal_text,
                inputs=[texto_input],
                outputs=[info_general, sentimiento, clasificacion, entidades, resumen]
            )
        
        with gr.Tab("📊 Estadísticas"):
            gr.Markdown("### Estadísticas de Análisis Realizados")
            
            stats_output = gr.Textbox(label="Estadísticas", lines=10)
            stats_btn = gr.Button("📊 Actualizar Estadísticas")
            
            stats_btn.click(
                fn=get_statistics,
                outputs=[stats_output]
            )
        
        with gr.Tab("ℹ️ Información"):
            gr.Markdown("""
            ## 🤖 Sistema de IA Legal - Etapa 2
            
            ### Características del Sistema:
            
            🧠 **Modelos de IA Utilizados:**
            - **Análisis de Sentimientos**: Determina el estado emocional de la consulta
            - **Clasificación Legal**: Identifica el área legal del caso
            - **NER (Named Entity Recognition)**: Extrae entidades como nombres, fechas, montos
            - **Generación de Texto**: Crea resúmenes automáticos
            
            📊 **Categorías Legales Soportadas:**
            - Derecho Civil
            - Derecho Penal
            - Derecho Laboral
            - Derecho de Familia
            - Derecho Comercial
            - Derecho Constitucional
            
            🔧 **Tecnologías:**
            - **Hugging Face Transformers**: Modelos de lenguaje avanzados
            - **Gradio**: Interface web interactiva
            - **SQLite**: Almacenamiento de análisis
            - **PyTorch**: Framework de deep learning
            
            ⚠️ **Importante:**
            Este sistema es una herramienta de asistencia y no reemplaza el criterio legal profesional.
            Todos los análisis deben ser revisados por un abogado calificado.
            """)
    
    return interface

if __name__ == "__main__":
    print("🚀 Iniciando Sistema de IA Legal - Etapa 2...")
    print("📥 Cargando modelos de Hugging Face...")
    
    # Crear y lanzar la interface
    interface = create_gradio_interface()
    
    print("✅ Sistema listo!")
    print("🌐 Abriendo interface web...")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Cambiar a True para obtener URL pública
        debug=False
    )
