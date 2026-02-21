@echo off
setlocal enabledelayedexpansion
title Bible Quiz Automation

:: Change directory to where the script is located
cd /d %~dp0

:: Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
set LOG_FILE=logs\startup_error.log

echo 🚀 Starting Bible Quiz Automation Setup...
echo [Log trace started in %LOG_FILE%]

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not found on your system.
    echo.
    echo To run this application, you need to install Python 3.10 or higher.
    echo Please download it from: https://www.python.org/downloads/
    echo 💡 IMPORTANT: Check "[X] Add Python to PATH" during installation.
    pause
    exit /b
)

:: 2. Check for Configuration and Credentials
if not exist "credentials.json" (
    echo ❌ ERROR: 'credentials.json' is missing in the project root.
    echo.
    echo Please follow the guide in 'docs/setup/google-cloud/CREDENTIALS_SETUP.md' 
    echo to get your Google API credentials.
    pause
    exit /b
)

if not exist ".env" (
    if exist ".env.example" (
        echo ⚠️ Configuration file (.env) is missing. Creating from template...
        copy .env.example .env >nul
        echo 📝 ACTION REQUIRED: Please edit '.env' with your Spreadsheet IDs.
        pause
        exit /b
    )
)

:: 3. Check for Microsoft Edge WebView2 (Required for Desktop Mode)
:: Most Windows 11 machines have this, but it's a common failure point.
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3C47117-6014-45B9-9E67-550996898F70}" /v pv >nul 2>&1
if %errorlevel% neq 0 (
    reg query "HKCU\Software\Microsoft\EdgeUpdate\Clients\{F3C47117-6014-45B9-9E67-550996898F70}" /v pv >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Microsoft Edge WebView2 Runtime is not detected.
        echo This is required to show the app window.
        echo.
        echo Please download and install the "Evergreen Standalone Installer" from:
        echo 👉 https://developer.microsoft.com/en-us/microsoft-edge/webview2/
        echo.
        pause
    )
)

:: 4. Setup/Check Virtual Environment
if not exist "venv" (
    echo 📦 [1/3] Creating virtual environment...
    python -m venv venv 2>>%LOG_FILE%
    if !errorlevel! neq 0 (
        echo ❌ Failed to create virtual environment. Check %LOG_FILE%
        pause
        exit /b
    )
)

:: 5. Activate and Install Dependencies
echo 🔄 [2/3] Updating dependencies...
call venv\Scripts\activate 2>>%LOG_FILE%
if !errorlevel! neq 0 (
    echo ❌ Failed to activate environment.
    pause
    exit /b
)

python -m pip install --upgrade pip --quiet 2>>%LOG_FILE%
pip install -r requirements.txt --quiet 2>>%LOG_FILE%
if !errorlevel! neq 0 (
    echo ❌ Failed to install dependencies. Check your internet and %LOG_FILE%
    pause
    exit /b
)

:: 6. Launch Application
echo 📖 [3/3] Launching Bible Quiz Application...
set PYTHONPATH=.

:: We run with 'python' to see the console if it crashes, 
:: but redirect stderr to our log file as well.
python src\interfaces\ui\standalone.py 2>>%LOG_FILE%

if !errorlevel! neq 0 (
    echo.
    echo ❌ The application crashed. 
    echo Please check the error details in: %LOG_FILE%
    echo.
    pause
) else (
    echo.
    echo ✅ Application Closed Successfully.
    :: If it closed successfully, we can clean up the log
    if exist %LOG_FILE% del %LOG_FILE%
)

deactivate
pause
