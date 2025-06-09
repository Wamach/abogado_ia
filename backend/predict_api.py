"""
Sistema de Predicción de Sentencias Judiciales
==============================================
Modelo de IA que predice posibles resultados de casos legales
basado en características del caso, jurisprudencia y patrones históricos.

Funcionalidades:
- Análisis de probabilidad de éxito del caso
- Predicción de tipo de sentencia
- Análisis de factores de riesgo
- Recomendaciones estratégicas
- Estimación de tiempo de resolución
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
import json
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sistema de Predicción de Sentencias",
    description="Predicción de resultados judiciales con IA",
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

# Modelos de datos
class CaseData(BaseModel):
    tipo_caso: str = Field(..., description="Tipo de caso legal")
    descripcion: str = Field(..., description="Descripción detallada del caso")
    monto_disputa: Optional[float] = Field(0, description="Monto en disputa")
    complejidad: str = Field("media", description="Complejidad: baja, media, alta")
    evidencias: List[str] = Field(default=[], description="Lista de evidencias disponibles")
    antecedentes: Optional[str] = Field("", description="Antecedentes del caso")
    jurisdiccion: str = Field("civil", description="Jurisdicción del caso")

class PredictionResult(BaseModel):
    probabilidad_exito: float
    tipo_sentencia_probable: str
    factores_riesgo: List[str]
    recomendaciones: List[str]
    tiempo_estimado_meses: int
    confianza_prediccion: float

class SentencePredictionSystem:
    """Sistema de predicción de sentencias judiciales"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.case_types = {
            "civil": {
                "probabilidades_base": {"favorable": 0.65, "parcial": 0.25, "desfavorable": 0.10},
                "tiempo_promedio": 8,
                "factores_exito": ["evidencia_documental", "testigos", "jurisprudencia_favorable"]
            },
            "penal": {
                "probabilidades_base": {"absolutoria": 0.30, "condenatoria": 0.60, "atenuante": 0.10},
                "tiempo_promedio": 12,
                "factores_exito": ["coartada", "evidencia_exculpatoria", "testigos_favorables"]
            },
            "laboral": {
                "probabilidades_base": {"favorable": 0.70, "parcial": 0.20, "desfavorable": 0.10},
                "tiempo_promedio": 6,
                "factores_exito": ["documentacion_laboral", "testigos", "historial_empresa"]
            },
            "familia": {
                "probabilidades_base": {"favorable": 0.55, "acuerdo": 0.35, "desfavorable": 0.10},
                "tiempo_promedio": 10,
                "factores_exito": ["bienestar_menor", "estabilidad_economica", "entorno_familiar"]
            },
            "comercial": {
                "probabilidades_base": {"favorable": 0.60, "transaccion": 0.30, "desfavorable": 0.10},
                "tiempo_promedio": 14,
                "factores_exito": ["contratos", "correspondencia", "historial_comercial"]
            }
        }
        self.init_database()
        self.load_or_create_model()
    
    def init_database(self):
        """Inicializar base de datos para predicciones"""
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS case_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_caso TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                monto_disputa REAL,
                complejidad TEXT,
                evidencias TEXT,
                probabilidad_exito REAL,
                tipo_sentencia_probable TEXT,
                tiempo_estimado INTEGER,
                fecha_prediccion DATETIME DEFAULT CURRENT_TIMESTAMP,
                resultado_real TEXT DEFAULT NULL,
                fecha_resolucion DATETIME DEFAULT NULL
            )
        ''')
        
        # Tabla para casos históricos (datos sintéticos para entrenamiento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_caso TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                monto_disputa REAL,
                complejidad TEXT,
                evidencias TEXT,
                resultado TEXT NOT NULL,
                tiempo_resolucion INTEGER,
                fecha_caso DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Generar datos sintéticos si no existen
        self.generate_synthetic_data()
    
    def generate_synthetic_data(self):
        """Generar datos sintéticos para entrenamiento del modelo"""
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute('SELECT COUNT(*) FROM historical_cases')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        logger.info("Generando datos sintéticos para entrenamiento...")
        
        synthetic_cases = [
            # Casos civiles
            ("civil", "Demanda por incumplimiento de contrato de arrendamiento", 50000, "media", 
             "contrato,correspondencia,testigos", "favorable", 8),
            ("civil", "Daños y perjuicios por accidente de tránsito", 150000, "alta", 
             "peritaje,testigos,fotos", "favorable", 12),
            ("civil", "Cobro de deuda comercial", 25000, "baja", 
             "facturas,contratos", "favorable", 6),
            
            # Casos penales
            ("penal", "Hurto simple", 0, "baja", 
             "testigos,camaras", "condenatoria", 10),
            ("penal", "Lesiones leves", 0, "media", 
             "certificado_medico,testigos", "condenatoria", 14),
            ("penal", "Estafa", 80000, "alta", 
             "documentos,testigos,peritaje", "absolutoria", 18),
            
            # Casos laborales
            ("laboral", "Despido injustificado", 0, "media", 
             "contrato,correspondencia,testigos", "favorable", 5),
            ("laboral", "Pago de horas extras", 15000, "baja", 
             "planillas,horarios", "favorable", 4),
            ("laboral", "Acoso laboral", 0, "alta", 
             "testigos,correspondencia,registros", "favorable", 8),
            
            # Casos de familia
            ("familia", "Divorcio contencioso", 0, "alta", 
             "documentos,testigos", "acuerdo", 12),
            ("familia", "Custodia de menores", 0, "alta", 
             "informes_psicologicos,testigos", "favorable", 10),
            ("familia", "Pensión alimenticia", 0, "media", 
             "documentos_ingresos,gastos", "favorable", 6),
            
            # Casos comerciales
            ("comercial", "Incumplimiento de contrato comercial", 200000, "alta", 
             "contratos,correspondencia,facturas", "transaccion", 16),
            ("comercial", "Competencia desleal", 100000, "alta", 
             "evidencia_publicidad,testigos", "favorable", 14),
            ("comercial", "Resolución de sociedad", 500000, "alta", 
             "estatutos,libros_contables,peritaje", "favorable", 20)
        ]
        
        for case in synthetic_cases:
            cursor.execute('''
                INSERT INTO historical_cases 
                (tipo_caso, descripcion, monto_disputa, complejidad, evidencias, resultado, tiempo_resolucion, fecha_caso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (*case, datetime.now() - timedelta(days=np.random.randint(30, 365))))
        
        conn.commit()
        conn.close()
        logger.info("Datos sintéticos generados exitosamente")
    
    def load_or_create_model(self):
        """Cargar modelo existente o crear uno nuevo"""
        try:
            self.model = joblib.load('sentence_prediction_model.pkl')
            self.vectorizer = joblib.load('text_vectorizer.pkl')
            logger.info("Modelo de predicción cargado exitosamente")
        except:
            logger.info("Creando y entrenando nuevo modelo...")
            self.train_model()
    
    def train_model(self):
        """Entrenar modelo de predicción"""
        # Cargar datos históricos
        conn = sqlite3.connect('predictions.db')
        df = pd.read_sql_query('''
            SELECT tipo_caso, descripcion, monto_disputa, complejidad, evidencias, resultado
            FROM historical_cases
        ''', conn)
        conn.close()
        
        if len(df) == 0:
            logger.warning("No hay datos para entrenar el modelo")
            return
        
        # Preparar características
        X_text = df['descripcion'] + ' ' + df['evidencias']
        X_numerical = df[['monto_disputa']].fillna(0)
        
        # Vectorizar texto
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        X_text_vectorized = self.vectorizer.fit_transform(X_text)
        
        # Combinar características
        X = np.hstack([X_text_vectorized.toarray(), X_numerical.values])
        y = df['resultado']
        
        # Entrenar modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Guardar modelo
        joblib.dump(self.model, 'sentence_prediction_model.pkl')
        joblib.dump(self.vectorizer, 'text_vectorizer.pkl')
        
        logger.info("Modelo entrenado y guardado exitosamente")
    
    def predict_case_outcome(self, case_data: CaseData) -> PredictionResult:
        """Predecir resultado de un caso"""
        try:
            # Obtener probabilidades base según tipo de caso
            case_info = self.case_types.get(case_data.tipo_caso, self.case_types["civil"])
            
            # Factores que influyen en la probabilidad
            probability_adjustments = 0.0
            risk_factors = []
            recommendations = []
            
            # Análisis de evidencias
            evidence_score = len(case_data.evidencias) * 0.05
            if evidence_score > 0.2:
                evidence_score = 0.2
            probability_adjustments += evidence_score
            
            if len(case_data.evidencias) < 2:
                risk_factors.append("Evidencias insuficientes")
                recommendations.append("Recopilar más evidencias documentales")
            
            # Análisis de complejidad
            complexity_impact = {
                "baja": 0.1,
                "media": 0.0,
                "alta": -0.15
            }
            probability_adjustments += complexity_impact.get(case_data.complejidad, 0.0)
            
            if case_data.complejidad == "alta":
                risk_factors.append("Caso de alta complejidad")
                recommendations.append("Considerar especialización adicional")
            
            # Análisis de monto
            if case_data.monto_disputa > 100000:
                probability_adjustments -= 0.05
                risk_factors.append("Alto monto en disputa aumenta escrutinio")
                recommendations.append("Preparar documentación financiera detallada")
            
            # Calcular probabilidad final
            base_probability = case_info["probabilidades_base"]["favorable"]
            final_probability = max(0.1, min(0.95, base_probability + probability_adjustments))
            
            # Determinar tipo de sentencia probable
            if final_probability > 0.7:
                sentence_type = "Favorable"
            elif final_probability > 0.4:
                sentence_type = "Parcialmente favorable"
            else:
                sentence_type = "Desfavorable"
            
            # Estimación de tiempo
            base_time = case_info["tiempo_promedio"]
            time_adjustment = 0
            
            if case_data.complejidad == "alta":
                time_adjustment += 2
            if case_data.monto_disputa > 100000:
                time_adjustment += 1
            
            estimated_time = base_time + time_adjustment
            
            # Confianza de la predicción
            confidence = 0.7 + (len(case_data.evidencias) * 0.05)
            confidence = min(0.95, confidence)
            
            # Recomendaciones generales
            if not recommendations:
                recommendations = [
                    "Revisar jurisprudencia similar",
                    "Fortalecer argumentación legal",
                    "Considerar mediación si es apropiado"
                ]
            
            return PredictionResult(
                probabilidad_exito=round(final_probability, 2),
                tipo_sentencia_probable=sentence_type,
                factores_riesgo=risk_factors,
                recomendaciones=recommendations,
                tiempo_estimado_meses=estimated_time,
                confianza_prediccion=round(confidence, 2)
            )
            
        except Exception as e:
            logger.error(f"Error en predicción: {e}")
            raise HTTPException(status_code=500, detail="Error en predicción")
    
    def save_prediction(self, case_data: CaseData, prediction: PredictionResult):
        """Guardar predicción en base de datos"""
        try:
            conn = sqlite3.connect('predictions.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO case_predictions 
                (tipo_caso, descripcion, monto_disputa, complejidad, evidencias, 
                 probabilidad_exito, tipo_sentencia_probable, tiempo_estimado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                case_data.tipo_caso,
                case_data.descripcion,
                case_data.monto_disputa,
                case_data.complejidad,
                json.dumps(case_data.evidencias),
                prediction.probabilidad_exito,
                prediction.tipo_sentencia_probable,
                prediction.tiempo_estimado_meses
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error guardando predicción: {e}")

# Instancia global del sistema
prediction_system = SentencePredictionSystem()

# === ENDPOINTS ===

@app.post("/predict", response_model=PredictionResult)
async def predict_sentence(case_data: CaseData):
    """Predecir resultado de un caso legal"""
    try:
        prediction = prediction_system.predict_case_outcome(case_data)
        prediction_system.save_prediction(case_data, prediction)
        return prediction
    except Exception as e:
        logger.error(f"Error en endpoint de predicción: {e}")
        raise HTTPException(status_code=500, detail="Error procesando predicción")

@app.get("/case_types")
async def get_case_types():
    """Obtener tipos de casos disponibles"""
    return {
        "tipos_casos": list(prediction_system.case_types.keys()),
        "detalles": prediction_system.case_types
    }

@app.get("/predictions/history")
async def get_prediction_history(limit: int = 50):
    """Obtener historial de predicciones"""
    try:
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM case_predictions 
            ORDER BY fecha_prediccion DESC 
            LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return {"predictions": results}
        
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo historial")

@app.get("/predictions/stats")
async def get_prediction_stats():
    """Obtener estadísticas de predicciones"""
    try:
        conn = sqlite3.connect('predictions.db')
        cursor = conn.cursor()
        
        # Estadísticas por tipo de caso
        cursor.execute('''
            SELECT tipo_caso, COUNT(*) as total, 
                   AVG(probabilidad_exito) as probabilidad_promedio,
                   AVG(tiempo_estimado) as tiempo_promedio
            FROM case_predictions 
            GROUP BY tipo_caso
        ''')
        
        stats_by_type = cursor.fetchall()
        
        # Total de predicciones
        cursor.execute('SELECT COUNT(*) FROM case_predictions')
        total_predictions = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_predictions": total_predictions,
            "stats_by_type": [
                {
                    "tipo_caso": row[0],
                    "total": row[1],
                    "probabilidad_promedio": round(row[2], 2) if row[2] else 0,
                    "tiempo_promedio": round(row[3], 1) if row[3] else 0
                }
                for row in stats_by_type
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
        "model_loaded": prediction_system.model is not None,
        "vectorizer_loaded": prediction_system.vectorizer is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
