@echo off
echo ========================================
echo   DESPACHO JURIDICO AUTOMATIZADO
echo   Sistema Completo - Todas las Etapas
echo ========================================
echo.

echo [1/6] Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    pause
    exit /b 1
)

echo [2/6] Activando entorno virtual...
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo [3/6] Instalando dependencias...
cd backend
pip install -r requirements.txt

echo [4/6] Iniciando servicios del sistema...

echo.
echo === INICIANDO CHATBOT OFFLINE (Puerto 8000) ===
start "Chatbot Offline" cmd /k "uvicorn chatbot_offline:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 >nul

echo === INICIANDO WEBHOOKS (Puerto 8002) ===
start "Webhook Integrations" cmd /k "python webhook_integrations.py"
timeout /t 3 >nul

echo === INICIANDO PREDICCION DE SENTENCIAS (Puerto 8003) ===
start "Prediction API" cmd /k "python predict_api.py"
timeout /t 3 >nul

cd ..\etapa2

echo === INICIANDO SISTEMA IA LEGAL GRADIO (Puerto 7860) ===
start "Legal AI Gradio" cmd /k "python legal_ai_gradio.py"
timeout /t 3 >nul

cd ..\frontend

echo [5/6] Abriendo interfaces web...
timeout /t 5 >nul

echo === ABRIENDO FRONTEND WEB ===
start "" "index.html"

echo === ABRIENDO DOCUMENTACION API ===
start "" "http://localhost:8000/docs"

echo === ABRIENDO SISTEMA IA LEGAL ===
start "" "http://localhost:7860"

echo [6/6] Sistema iniciado completamente!
echo.
echo ========================================
echo   SERVICIOS ACTIVOS:
echo ========================================
echo   🤖 Chatbot Offline:     http://localhost:8000
echo   📱 Webhook Integration: http://localhost:8002  
echo   🔮 Prediccion API:      http://localhost:8003
echo   🧠 Sistema IA Legal:    http://localhost:7860
echo   🌐 Frontend Web:        frontend/index.html
echo   📚 API Docs:            http://localhost:8000/docs
echo ========================================
echo.
echo Presiona cualquier tecla para abrir ngrok (opcional)...
pause >nul

echo.
echo ========================================
echo   CONFIGURACION NGROK (OPCIONAL)
echo ========================================
echo   Para usar webhooks de WhatsApp/Messenger:
echo   1. Instala ngrok: https://ngrok.com/
echo   2. Ejecuta: ngrok http 8002
echo   3. Copia la URL publica
echo   4. Configura en Meta Developers Console
echo ========================================
echo.

choice /c YN /m "Deseas abrir la configuracion de ngrok"
if %errorlevel%==1 (
    echo Iniciando ngrok para webhooks...
    start "Ngrok Webhooks" cmd /k "ngrok http 8002"
    
    echo Iniciando ngrok para chatbot...
    start "Ngrok Chatbot" cmd /k "ngrok http 8000"
)

echo.
echo ========================================
echo   SISTEMA COMPLETAMENTE OPERATIVO
echo ========================================
echo   Todas las etapas del proyecto estan funcionando
echo   Revisa las ventanas abiertas para monitorear
echo ========================================
pause
