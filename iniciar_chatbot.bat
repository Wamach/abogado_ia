@echo off
echo ========================================
echo   Despacho Juridico Virtual - Inicio
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instale Python 3.9 o superior
    pause
    exit /b 1
)

echo [INFO] Python detectado correctamente
echo.

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [INFO] Creando entorno virtual de Python...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate

REM Instalar dependencias
echo [INFO] Instalando dependencias...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Iniciando Chatbot Offline
echo ========================================
echo.
echo El chatbot estará disponible en:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo.
echo Para acceder al frontend, abra en su navegador:
echo   frontend/index.html
echo.
echo Presione Ctrl+C para detener el servidor
echo.

REM Iniciar servidor
uvicorn chatbot_offline:app --reload --host 0.0.0.0 --port 8000
