@echo off
setlocal enabledelayedexpansion

title OFFERPROOF - Demo Launcher

echo ==============================================================================
echo                      OFFERPROOF - Verification Platform
echo             "Don't trust the offer. Verify the evidence."
echo ==============================================================================
echo.
echo Initializing environment checks for hackathon demo launch...
echo.

:: 1. Resolve repository directories relative to this script
set "ROOT_DIR=%~dp0"
set "BACKEND_DIR=%ROOT_DIR%backend"
set "FRONTEND_DIR=%ROOT_DIR%frontend"
set "VENV_DIR=%BACKEND_DIR%\.venv"

:: 2. Check if required directories exist
if not exist "%BACKEND_DIR%" (
    echo [ERROR] Backend directory not found at: "%BACKEND_DIR%"
    echo Please make sure you are running this script from the OFFERPROOF project root.
    goto :error_exit
)

if not exist "%FRONTEND_DIR%" (
    echo [ERROR] Frontend directory not found at: "%FRONTEND_DIR%"
    echo Please make sure you are running this script from the OFFERPROOF project root.
    goto :error_exit
)

:: 3. Check for Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo Make sure to check the option "Add Python to PATH" during installation.
    goto :error_exit
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set "PY_VER=%%i"
echo [OK] Python detected: %PY_VER%

:: 4. Check for Node.js installation
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js was not found in your system PATH.
    echo Please install Node.js - v18 or higher recommended - from https://nodejs.org/
    goto :error_exit
)
for /f "tokens=*" %%i in ('node --version 2^>^&1') do set "NODE_VER=%%i"
echo [OK] Node.js detected: %NODE_VER%

:: 5. Check for npm installation
where npm >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] npm was not found in your system PATH.
    echo Please install npm - included with Node.js - from https://nodejs.org/
    goto :error_exit
)
for /f "tokens=*" %%i in ('npm --version 2^>^&1') do set "NPM_VER=%%i"
echo [OK] npm detected: v%NPM_VER%

echo.
echo ==============================================================================
echo Preparing Backend (FastAPI + Python Virtual Environment)
echo ==============================================================================

:: Check if Python virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment at "%VENV_DIR%"...
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create Python virtual environment.
        goto :error_exit
    )
    echo Virtual environment created successfully.
    set "INSTALL_BACKEND_DEPS=1"
) else (
    echo [OK] Python virtual environment already exists.
)

:: Quick test if key backend packages are installed
"%VENV_DIR%\Scripts\python.exe" -c "import fastapi, uvicorn, pymupdf, pydantic, httpx" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Installing backend dependencies from requirements.txt...
    "%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
    "%VENV_DIR%\Scripts\pip.exe" install -r "%BACKEND_DIR%\requirements.txt"
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to install backend dependencies.
        goto :error_exit
    )
    echo [OK] Backend dependencies installed successfully.
) else (
    echo [OK] Backend dependencies verified.
)

echo.
echo ==============================================================================
echo Preparing Frontend (React + Vite + Tailwind CSS)
echo ==============================================================================

if not exist "%FRONTEND_DIR%\node_modules" (
    echo Installing frontend dependencies via npm install...
    pushd "%FRONTEND_DIR%"
    call npm install
    if %ERRORLEVEL% neq 0 (
        popd
        echo [ERROR] Failed to install frontend dependencies.
        goto :error_exit
    )
    popd
    echo [OK] Frontend dependencies installed successfully.
) else (
    echo [OK] Frontend node_modules already present.
)

echo.
echo ==============================================================================
echo Starting OFFERPROOF Services
echo ==============================================================================

:: 1. Launch FastAPI Backend in a separate window
echo Starting Backend API on http://127.0.0.1:8000 ...
start "OFFERPROOF - Backend API (FastAPI)" cmd /k "cd /d "%BACKEND_DIR%" && call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

:: 2. Launch Vite Frontend in a separate window
echo Starting Frontend UI on http://localhost:5173 ...
start "OFFERPROOF - Frontend Web UI (Vite)" cmd /k "cd /d "%FRONTEND_DIR%" && npm run dev"

:: 3. Wait briefly for servers to initialize
echo Waiting for servers to initialize...
timeout /t 4 /nobreak >nul 2>&1

:: 4. Launch Default Web Browser
echo Opening OFFERPROOF in your default browser...
start http://localhost:5173

echo.
echo ==============================================================================
echo                       OFFERPROOF IS NOW RUNNING
echo ==============================================================================
echo.
echo  - Frontend Dashboard:       http://localhost:5173
echo  - Backend Interactive Docs: http://127.0.0.1:8000/docs
echo  - Backend Health Endpoint:  http://127.0.0.1:8000/api/v1/health
echo.
echo ------------------------------------------------------------------------------
echo Quick Demo Guide:
echo   1. The browser window should open to http://localhost:5173 automatically.
echo   2. Click the "Demo Walkthrough" button in the hero section.
echo   3. Click "Analyze & Verify Opportunity" to see the full analysis.
echo   4. Inspect the High Caution verdict, evidence chips, and click "Print / Save PDF".
echo.
echo How to Stop the Application:
echo   Close both opened terminal windows ("OFFERPROOF - Backend API" and
echo   "OFFERPROOF - Frontend Web UI") or press Ctrl+C in each terminal window.
echo.
echo Troubleshooting:
echo   - If port 8000 is occupied, check if an existing uvicorn process is running.
echo   - If port 5173 is occupied, Vite will automatically select 5174.
echo   - No API keys are required: deterministic rule fallback runs automatically.
echo ==============================================================================
echo.
pause
goto :eof

:error_exit
echo.
echo [FAILED] Unable to start OFFERPROOF demo. Please check the error messages above.
echo.
pause
exit /b 1

