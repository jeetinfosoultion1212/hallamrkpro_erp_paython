@echo off
title HallmarkPro ERP
cd /d "%~dp0"
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
echo Installing/updating dependencies...
python -m pip install -r requirements.txt --quiet
echo Launching HallmarkPro...
python main.py
if errorlevel 1 (
    echo Application crashed. Check errors above.
    pause
)
