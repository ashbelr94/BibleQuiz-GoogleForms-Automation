@echo off
setlocal enabledelayedexpansion
title Bible Quiz Automation

:: Change directory to where the script is located
cd /d %~dp0

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
set LOG_FILE=logs\startup_error.log

:: Clear previous log
echo --- Startup Log [%DATE% %TIME%] --- > %LOG_FILE%

echo 🚀 Starting Bible Quiz Automation Setup...

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not found on your system.
    echo.
    echo Please install Python 3.10+ from: https://www.python.org/downloads/
    echo 💡 IMPORTANT: Check "[X] Add Python to PATH" during installation.
    pause
    exit /b
)

:: 2. Check for Configuration and Credentials
if not exist "credentials.json" (
    echo ❌ ERROR: 'credentials.json' is missing.
    echo Please follow 'docs/setup/google-cloud/CREDENTIALS_SETUP.md'
    pause
    exit /b
)

:: 3. Setup/Check Virtual Environment
if not exist "venv" (
    echo 📦 [1/3] Creating virtual environment...
    python -m venv venv 2>>%LOG_FILE%
)

:: 4. Activate and Install Dependencies
echo 🔄 [2/3] Updating dependencies...
call venv\Scripts\activate 2>>%LOG_FILE%
if !errorlevel! neq 0 (
    echo ❌ Failed to activate environment.
    type %LOG_FILE%
    pause
    exit /b
)

pip install -r requirements.txt --quiet 2>>%LOG_FILE%
if !errorlevel! neq 0 (
    echo ❌ Failed to install dependencies.
    echo ---- ERROR DETAILS ----
    type %LOG_FILE%
    echo -----------------------
    pause
    exit /b
)

:: 5. Launch Application
echo 📖 [3/3] Launching Bible Quiz Application...
set PYTHONPATH=.

:: Run the standalone app and capture any immediate crash
python src\interfaces\ui\standalone.py 2>>%LOG_FILE%

if !errorlevel! neq 0 (
    echo.
    echo ❌ THE APPLICATION CRASHED.
    echo.
    echo ---- ERROR LOG (from %LOG_FILE%) ----
    type %LOG_FILE%
    echo ---------------------------------------
    echo.
    echo If you see a "JSONDecodeError", your 'credentials.json' might be malformed.
    echo.
    pause
) else (
    echo.
    echo ✅ Application Closed Successfully.
)

deactivate
pause
