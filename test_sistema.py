#!/usr/bin/env python3
"""
Script de Testing y Validación del Sistema Completo
=================================================
Verifica que todos los componentes del despacho jurídico virtual estén funcionando correctamente.

Fases de Testing:
1. Verificación de dependencias
2. Testing de APIs individuales
3. Testing de integraciones
4. Validación de fronted
5. Testing de webhooks (simulado)
6. Reporte final
"""

import subprocess
import sys
import os
import requests
import time
import json
from pathlib import Path

class SistemaTester:
    def __init__(self):
        self.results = {
            'dependencies': {},
            'apis': {},
            'integrations': {},
            'frontend': {},
            'webhooks': {},
            'overall': 'PENDING'
        }
        self.base_path = Path(__file__).parent
        
    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print(f"{'='*50}")
        
    def print_step(self, step, status, details=""):
        icons = {"OK": "✅", "ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️"}
        print(f"{icons.get(status, '•')} {step}: {status}")
        if details:
            print(f"   {details}")
            
    def check_dependencies(self):
        """Verificar que todas las dependencias estén instaladas"""
        self.print_header("VERIFICACIÓN DE DEPENDENCIAS")
        
        dependencies = [
            'fastapi', 'uvicorn', 'pydantic', 'requests', 
            'sklearn', 'pandas', 'numpy', 'sqlite3'
        ]
        
        for dep in dependencies:
            try:
                if dep == 'sklearn':
                    import sklearn
                elif dep == 'sqlite3':
                    import sqlite3
                else:
                    __import__(dep)
                self.print_step(f"Dependencia {dep}", "OK")
                self.results['dependencies'][dep] = True
            except ImportError:
                self.print_step(f"Dependencia {dep}", "ERROR", "No instalada")
                self.results['dependencies'][dep] = False
                
    def check_file_structure(self):
        """Verificar estructura de archivos"""
        self.print_header("ESTRUCTURA DE ARCHIVOS")
        
        required_files = {
            'backend/chatbot_offline.py': 'Chatbot principal',
            'backend/webhook_integrations.py': 'Sistema de webhooks',
            'backend/predict_api.py': 'API de predicciones',
            'frontend/index.html': 'Frontend principal',
            'frontend/prediction.html': 'Interface de predicción',
            'frontend/dashboard.html': 'Dashboard del sistema',
            'backend/.env': 'Configuración'
        }
        
        for file_path, description in required_files.items():
            full_path = self.base_path / file_path
            if full_path.exists():
                self.print_step(f"{description}", "OK", f"Encontrado: {file_path}")
            else:
                self.print_step(f"{description}", "ERROR", f"Faltante: {file_path}")
                
    def test_apis_individually(self):
        """Probar cada API por separado"""
        self.print_header("TESTING INDIVIDUAL DE APIs")
        
        # Test Chatbot API (Puerto 8000)
        self.print_step("Iniciando Chatbot API", "INFO", "Puerto 8000...")
        try:
            # Intentar conectar primero
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code == 200:
                self.print_step("Chatbot API", "OK", "Respondiendo correctamente")
                self.results['apis']['chatbot'] = True
            else:
                self.print_step("Chatbot API", "WARNING", f"Status code: {response.status_code}")
                self.results['apis']['chatbot'] = False
        except requests.exceptions.ConnectionError:
            self.print_step("Chatbot API", "ERROR", "No se puede conectar - ¿Está ejecutándose?")
            self.results['apis']['chatbot'] = False
        except Exception as e:
            self.print_step("Chatbot API", "ERROR", str(e))
            self.results['apis']['chatbot'] = False
            
        # Test Webhook API (Puerto 8002)
        try:
            response = requests.get("http://localhost:8002/health", timeout=5)
            if response.status_code == 200:
                self.print_step("Webhook API", "OK", "Puerto 8002 activo")
                self.results['apis']['webhook'] = True
            else:
                self.print_step("Webhook API", "WARNING", f"Status code: {response.status_code}")
                self.results['apis']['webhook'] = False
        except requests.exceptions.ConnectionError:
            self.print_step("Webhook API", "ERROR", "Puerto 8002 no activo")
            self.results['apis']['webhook'] = False
        except Exception as e:
            self.print_step("Webhook API", "ERROR", str(e))
            self.results['apis']['webhook'] = False
            
        # Test Prediction API (Puerto 8003)
        try:
            response = requests.get("http://localhost:8003/health", timeout=5)
            if response.status_code == 200:
                self.print_step("Prediction API", "OK", "Puerto 8003 activo")
                self.results['apis']['prediction'] = True
            else:
                self.print_step("Prediction API", "WARNING", f"Status code: {response.status_code}")
                self.results['apis']['prediction'] = False
        except requests.exceptions.ConnectionError:
            self.print_step("Prediction API", "ERROR", "Puerto 8003 no activo")
            self.results['apis']['prediction'] = False
        except Exception as e:
            self.print_step("Prediction API", "ERROR", str(e))
            self.results['apis']['prediction'] = False
    
    def test_chatbot_functionality(self):
        """Probar funcionalidades específicas del chatbot"""
        self.print_header("TESTING FUNCIONAL DEL CHATBOT")
        
        if not self.results['apis'].get('chatbot', False):
            self.print_step("Chatbot Funcional", "ERROR", "API no disponible")
            return
            
        # Test mensaje básico
        try:
            test_data = {
                "mensaje": "Hola, ¿qué servicios ofrecen?",
                "usuario_id": "test_user"
            }
            response = requests.post(
                "http://localhost:8000/chat", 
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'respuesta' in data and data['respuesta']:
                    self.print_step("Chat Básico", "OK", "Respuesta recibida")
                    self.results['integrations']['chat'] = True
                else:
                    self.print_step("Chat Básico", "ERROR", "Respuesta vacía")
                    self.results['integrations']['chat'] = False
            else:
                self.print_step("Chat Básico", "ERROR", f"Status: {response.status_code}")
                self.results['integrations']['chat'] = False
                
        except Exception as e:
            self.print_step("Chat Básico", "ERROR", str(e))
            self.results['integrations']['chat'] = False
            
    def test_prediction_functionality(self):
        """Probar funcionalidades de predicción"""
        self.print_header("TESTING PREDICCIÓN DE SENTENCIAS")
        
        if not self.results['apis'].get('prediction', False):
            self.print_step("Predicción Funcional", "ERROR", "API no disponible")
            return
            
        # Test predicción básica
        try:
            test_case = {
                "tipo_caso": "civil",
                "descripcion": "Demanda por incumplimiento de contrato de compraventa",
                "monto_disputa": 50000,
                "complejidad": "media",
                "evidencias": ["contratos", "testigos"],
                "antecedentes": "Sin antecedentes previos",
                "jurisdiccion": "civil"
            }
            
            response = requests.post(
                "http://localhost:8003/predict",
                json=test_case,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'probabilidad_exito' in data:
                    self.print_step("Predicción IA", "OK", f"Probabilidad: {data['probabilidad_exito']:.2%}")
                    self.results['integrations']['prediction'] = True
                else:
                    self.print_step("Predicción IA", "ERROR", "Formato de respuesta incorrecto")
                    self.results['integrations']['prediction'] = False
            else:
                self.print_step("Predicción IA", "ERROR", f"Status: {response.status_code}")
                self.results['integrations']['prediction'] = False
                
        except Exception as e:
            self.print_step("Predicción IA", "ERROR", str(e))
            self.results['integrations']['prediction'] = False
    
    def test_frontend_files(self):
        """Verificar archivos del frontend"""
        self.print_header("TESTING FRONTEND")
        
        frontend_files = [
            'frontend/index.html',
            'frontend/prediction.html', 
            'frontend/dashboard.html',
            'frontend/chatbot.js',
            'frontend/prediction.js'
        ]
        
        for file_path in frontend_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                # Verificar contenido mínimo
                content = full_path.read_text(encoding='utf-8')
                if len(content) > 100:  # Archivo no vacío
                    self.print_step(f"Archivo {file_path}", "OK", f"Tamaño: {len(content)} chars")
                    self.results['frontend'][file_path] = True
                else:
                    self.print_step(f"Archivo {file_path}", "WARNING", "Archivo muy pequeño")
                    self.results['frontend'][file_path] = False
            else:
                self.print_step(f"Archivo {file_path}", "ERROR", "No encontrado")
                self.results['frontend'][file_path] = False
                
    def test_database_functionality(self):
        """Probar funcionalidad de base de datos"""
        self.print_header("TESTING BASE DE DATOS")
        
        try:
            import sqlite3
            
            # Test crear conexión temporal
            test_db = self.base_path / "test_db.sqlite"
            conn = sqlite3.connect(test_db)
            cursor = conn.cursor()
            
            # Test crear tabla básica
            cursor.execute("""
                CREATE TABLE test_table (
                    id INTEGER PRIMARY KEY,
                    test_data TEXT
                )
            """)
            
            # Test insertar datos
            cursor.execute("INSERT INTO test_table (test_data) VALUES (?)", ("test_value",))
            conn.commit()
            
            # Test leer datos
            cursor.execute("SELECT test_data FROM test_table WHERE id = 1")
            result = cursor.fetchone()
            
            if result and result[0] == "test_value":
                self.print_step("SQLite", "OK", "Base de datos funcional")
                self.results['integrations']['database'] = True
            else:
                self.print_step("SQLite", "ERROR", "Error en operaciones básicas")
                self.results['integrations']['database'] = False
                
            conn.close()
            test_db.unlink()  # Eliminar archivo de prueba
            
        except Exception as e:
            self.print_step("SQLite", "ERROR", str(e))
            self.results['integrations']['database'] = False
    
    def simulate_webhook_tests(self):
        """Simular tests de webhooks"""
        self.print_header("SIMULACIÓN DE WEBHOOKS")
        
        # Verificar que el archivo de webhooks exista y tenga contenido válido
        webhook_file = self.base_path / "backend" / "webhook_integrations.py"
        if webhook_file.exists():
            content = webhook_file.read_text()
            if "whatsapp" in content.lower() and "messenger" in content.lower():
                self.print_step("Código Webhooks", "OK", "Estructura encontrada")
                self.results['webhooks']['structure'] = True
            else:
                self.print_step("Código Webhooks", "WARNING", "Estructura incompleta")
                self.results['webhooks']['structure'] = False
        else:
            self.print_step("Código Webhooks", "ERROR", "Archivo no encontrado")
            self.results['webhooks']['structure'] = False
            
        # Verificar configuración en .env
        env_file = self.base_path / "backend" / ".env"
        if env_file.exists():
            env_content = env_file.read_text()
            if "WHATSAPP_TOKEN" in env_content and "MESSENGER_PAGE_TOKEN" in env_content:
                self.print_step("Configuración Webhooks", "OK", "Variables encontradas")
                self.results['webhooks']['config'] = True
            else:
                self.print_step("Configuración Webhooks", "WARNING", "Configuración incompleta")
                self.results['webhooks']['config'] = False
        else:
            self.print_step("Configuración Webhooks", "ERROR", "Archivo .env no encontrado")
            self.results['webhooks']['config'] = False
            
    def generate_report(self):
        """Generar reporte final"""
        self.print_header("REPORTE FINAL DEL SISTEMA")
        
        total_tests = 0
        passed_tests = 0
        
        # Contar resultados
        for category, tests in self.results.items():
            if category == 'overall':
                continue
            for test, result in tests.items():
                total_tests += 1
                if result:
                    passed_tests += 1
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Determinar status general
        if success_rate >= 90:
            overall_status = "EXCELENTE"
            status_icon = "🟢"
        elif success_rate >= 75:
            overall_status = "BUENO"
            status_icon = "🟡"
        elif success_rate >= 50:
            overall_status = "REGULAR"
            status_icon = "🟠"
        else:
            overall_status = "CRÍTICO"
            status_icon = "🔴"
            
        self.results['overall'] = overall_status
        
        print(f"\n{status_icon} ESTADO GENERAL: {overall_status}")
        print(f"📊 Tests pasados: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Detalles por categoría
        print(f"\n📋 RESUMEN POR CATEGORÍAS:")
        for category, tests in self.results.items():
            if category == 'overall':
                continue
            category_passed = sum(1 for result in tests.values() if result)
            category_total = len(tests)
            category_rate = (category_passed / category_total) * 100 if category_total > 0 else 0
            print(f"  • {category.upper()}: {category_passed}/{category_total} ({category_rate:.0f}%)")
            
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        
        if not any(self.results['dependencies'].values()):
            print("  🔧 Instalar dependencias: py -m pip install -r backend/requirements.txt")
            
        if not any(self.results['apis'].values()):
            print("  🚀 Iniciar servicios: ejecutar iniciar_sistema_completo.bat")
            
        if not self.results['webhooks']['config']:
            print("  ⚙️ Configurar webhooks: editar backend/.env con tokens reales")
            
        print(f"\n📁 Archivos de configuración importantes:")
        print(f"  • backend/.env - Configuración del sistema")
        print(f"  • backend/requirements.txt - Dependencias Python")
        print(f"  • iniciar_sistema_completo.bat - Launcher del sistema")
        
        # Guardar reporte en archivo
        report_file = self.base_path / "test_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Reporte guardado en: {report_file}")
        
    def run_all_tests(self):
        """Ejecutar todos los tests"""
        print("🚀 INICIANDO TESTING COMPLETO DEL SISTEMA")
        print("=" * 60)
        
        self.check_dependencies()
        self.check_file_structure()
        self.test_database_functionality()
        self.test_apis_individually()
        self.test_chatbot_functionality()
        self.test_prediction_functionality()
        self.test_frontend_files()
        self.simulate_webhook_tests()
        self.generate_report()

def main():
    """Función principal"""
    tester = SistemaTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
