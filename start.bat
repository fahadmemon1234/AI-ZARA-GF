@echo off
title ARIA - AI Voice Assistant
color 0B

echo ================================================
echo    🤖  ARIA - Advanced Real-time Intelligent Assistant
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo    Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo    ✅ Virtual environment created!
) else (
    echo    ✅ Virtual environment found
)
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/update dependencies
echo 📥 Installing/Updating dependencies...
echo    This may take a few minutes on first run...
pip install -r requirements.txt --quiet --disable-pip-version-check
echo    ✅ Dependencies installed!
echo.

REM Check .env file
if not exist ".env" (
    echo ⚠️  WARNING: .env file not found!
    echo    Copy .env.example to .env and add your API key.
    echo.
    echo    1. Copy .env.example to .env
    echo    2. Edit .env and add your ANTHROPIC_API_KEY
    echo    3. Get your FREE key from: https://console.anthropic.com
    echo.
    pause
)

echo ================================================
echo    🚀 Starting ARIA Server...
echo ================================================
echo.
echo    🌐 Open your browser to: http://localhost:8000
echo.
echo    📡 Available endpoints:
echo       • /              - Frontend UI
echo       • /api/command   - Voice/text commands
echo       • /api/chat      - AI conversation
echo       • /api/status    - System status
echo       • /health        - Health check
echo.
echo    🎯 Features:
echo       • 66+ Voice Commands
echo       • Claude AI Integration
echo       • System Automation
echo       • WhatsApp Messaging
echo       • Media Control
echo       • File Management
echo       • Screenshots & OCR
echo       • PDF Tools
echo.
echo    Press Ctrl+C to stop the server
echo ================================================
echo.

python main.py

pause
