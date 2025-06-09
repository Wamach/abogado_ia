@echo off
echo ========================================
echo   CONFIGURACION INICIAL DEL SISTEMA
echo   Despacho Juridico Automatizado
echo ========================================
echo.

echo [1/7] Verificando requisitos del sistema...

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ PYTHON NO ENCONTRADO
    echo.
    echo Para usar este sistema necesitas Python 3.9 o superior.
    echo.
    echo 📥 OPCIONES DE INSTALACION:
    echo.
    echo 1. AUTOMATICA: Instalar desde Microsoft Store
    echo    - Ejecuta: ms-windows-store://pdp/?productid=9NRWMJP3717K
    echo.
    echo 2. MANUAL: Descargar desde python.org
    echo    - Ve a: https://www.python.org/downloads/
    echo    - Descarga Python 3.9+ para Windows
    echo    - IMPORTANTE: Marca "Add Python to PATH" durante instalacion
    echo.
    echo 3. CHOCOLATEY: Si tienes Chocolatey instalado
    echo    - Ejecuta: choco install python
    echo.
    choice /c 123 /m "Elige una opcion (1=Store, 2=Manual, 3=Chocolatey)"
    
    if %errorlevel%==1 (
        echo Abriendo Microsoft Store...
        start ms-windows-store://pdp/?productid=9NRWMJP3717K
        echo.
        echo Despues de instalar Python, vuelve a ejecutar este script.
        pause
        exit /b 1
    )
    
    if %errorlevel%==2 (
        echo Abriendo python.org...
        start https://www.python.org/downloads/
        echo.
        echo Despues de instalar Python, vuelve a ejecutar este script.
        echo RECUERDA: Marcar "Add Python to PATH" durante la instalacion
        pause
        exit /b 1
    )
    
    if %errorlevel%==3 (
        echo Instalando Python con Chocolatey...
        choco install python -y
        if %errorlevel% neq 0 (
            echo Error: Chocolatey no instalado o fallo la instalacion
            echo Ve a: https://chocolatey.org/install para instalar Chocolatey
            pause
            exit /b 1
        )
        echo Python instalado exitosamente con Chocolatey
        echo Reinicia este script para continuar
        pause
        exit /b 0
    )
) else (
    echo ✅ Python encontrado:
    python --version
)

echo.
echo [2/7] Verificando pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip no encontrado, instalando...
    python -m ensurepip --upgrade
) else (
    echo ✅ pip disponible
)

echo.
echo [3/7] Creando entorno virtual...
if not exist "venv" (
    echo Creando nuevo entorno virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Error creando entorno virtual
        echo Verifica que Python este correctamente instalado
        pause
        exit /b 1
    )
) else (
    echo ✅ Entorno virtual ya existe
)

echo.
echo [4/7] Activando entorno virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Error activando entorno virtual
    echo Intenta eliminar la carpeta "venv" y ejecutar de nuevo
    pause
    exit /b 1
)

echo.
echo [5/7] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [6/7] Instalando dependencias...
cd backend
echo Instalando dependencias del proyecto...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error instalando dependencias
    echo.
    echo Posibles soluciones:
    echo 1. Verificar conexion a internet
    echo 2. Ejecutar como administrador
    echo 3. Usar: pip install --user -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo [7/7] Verificando instalacion...
echo Verificando FastAPI...
python -c "import fastapi; print(f'✅ FastAPI {fastapi.__version__} instalado')" 2>nul
if %errorlevel% neq 0 echo ❌ FastAPI no disponible

echo Verificando Transformers...
python -c "import transformers; print(f'✅ Transformers {transformers.__version__} instalado')" 2>nul
if %errorlevel% neq 0 echo ❌ Transformers no disponible

echo Verificando Gradio...
python -c "import gradio; print(f'✅ Gradio {gradio.__version__} instalado')" 2>nul
if %errorlevel% neq 0 echo ❌ Gradio no disponible

echo Verificando scikit-learn...
python -c "import sklearn; print(f'✅ scikit-learn {sklearn.__version__} instalado')" 2>nul
if %errorlevel% neq 0 echo ❌ scikit-learn no disponible

cd ..

echo.
echo ========================================
echo   ✅ CONFIGURACION COMPLETADA
echo ========================================
echo.
echo 🎉 El sistema esta listo para usar!
echo.
echo 📋 PROXIMOS PASOS:
echo.
echo 1. Ejecutar sistema completo:
echo    👉 iniciar_sistema_completo.bat
echo.
echo 2. Solo chatbot offline:
echo    👉 iniciar_chatbot.bat
echo.
echo 3. Configurar webhooks (opcional):
echo    - Editar backend\.env con tus tokens
echo    - Instalar ngrok para URLs publicas
echo.
echo 🌐 URLS IMPORTANTES:
echo    - Frontend: frontend\index.html
echo    - Chatbot API: http://localhost:8000
echo    - IA Legal: http://localhost:7860
echo    - Prediccion: http://localhost:8003
echo    - API Docs: http://localhost:8000/docs
echo.
echo ========================================

choice /c YN /m "¿Deseas iniciar el sistema ahora?"
if %errorlevel%==1 (
    echo.
    echo Iniciando sistema completo...
    call iniciar_sistema_completo.bat
) else (
    echo.
    echo Sistema configurado. Ejecuta iniciar_sistema_completo.bat cuando estes listo.
)

pause
