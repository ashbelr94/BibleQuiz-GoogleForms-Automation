@echo off
setlocal
title Bible Quiz Automation

:: Change directory to where the script is located
cd /d %~dp0

echo 🚀 Checking dependencies...
:: Automatically create venv and install requirements if it's the first run
if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Silent install of new dependencies (like pywebview)
echo [2/3] Syncing latest updates...
pip install -r requirements.txt --quiet

echo [3/3] Launching Bible Quiz Application...
set PYTHONPATH=.

:: Using pythonw.exe instead of python.exe (optional) could hide the black console window
:: but we use python.exe here to make it easier to see if anything went wrong.
python src\interfaces\ui\standalone.py

echo.
echo Application Closed.
deactivate
pause
