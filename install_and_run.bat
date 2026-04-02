@echo off
title ARIA - AI Voice Assistant Installer & Runner
color 0B

echo ================================================
echo    🤖 ARIA - Auto Install & Run
echo ================================================
echo.
echo This script will:
echo   1. Install all required Python packages
echo   2. Install missing AI API packages
echo   3. Start ARIA server automatically
echo.
echo Please wait... This may take a few minutes.
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed!
    echo    Please install Python 3.8+ from: https://www.python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip --quiet
echo    ✅ pip upgraded
echo.

REM Install base requirements
echo 📥 Installing base requirements...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ⚠️  Some packages failed to install. Trying individually...
) else (
    echo    ✅ Base requirements installed
)
echo.

REM Install missing packages individually
echo 📦 Installing additional packages...

echo    Installing google-generativeai (Gemini AI)...
pip install google-generativeai --quiet

echo    Installing openai (GPT)...
pip install openai --quiet

echo    Installing mem0ai (Memory)...
pip install mem0ai --quiet

echo    Installing livekit (Real-time)...
pip install livekit livekit-api --quiet

echo    ✅ Additional packages installed
echo.

REM Verify installation
echo 🔍 Verifying installation...
python -c "import fastapi; import anthropic; import google.generativeai; import openai; print('✅ All core packages installed!')"
echo.

REM Check .env file
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo    Creating from template...
    copy .env.example .env
    echo    ✅ .env created
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your API keys!
    echo    Get FREE Gemini key: https://makersuite.google.com/app/apikey
    echo.
    pause
)

echo ================================================
echo    🚀 Starting ARIA Server...
echo ================================================
echo.
echo    🌐 Open your browser to: http://localhost:8000
echo.
echo    📡 AI Providers Available:
echo       ✅ Google Gemini (FREE - 1,500/day)
echo       ✅ Anthropic Claude (Optional)
echo       ✅ OpenAI GPT (Optional)
echo       ✅ ElevenLabs Voice (FREE tier)
echo.
echo    🎯 Try these commands:
echo       - "Battery status"
echo       - "What time is it?"
echo       - "Open Chrome"
echo       - "Take screenshot"
echo.
echo    Press Ctrl+C to stop the server
echo ================================================
echo.

python main.py

pause
