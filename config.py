"""
ZARA - Advanced Real-time Intelligent Assistant
Configuration Module
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============== API Keys ==============

# Groq API Key (FREE - for AI responses - FASTEST!)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Anthropic API Key (for AI responses - Claude)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Google Gemini API Key (for AI responses - Gemini models)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Mem0 API Key (for AI memory layer)
MEM0_API_KEY = os.getenv("MEM0_API_KEY", "")

# LiveKit API Keys (for real-time audio/video)
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")

# OpenAI API Key (for GPT models)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ElevenLabs API Key (for AI voice generation)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "RmT0JE37YE1NfodnZBnw")

# Genny (LOVO AI) API Key (for text-to-speech)
GENNY_API_KEY = os.getenv("GENNY_API_KEY", "")

# News API Key (optional - for news headlines)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Weather API Key (optional)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# ============== Voice Settings ==============

# Wake word to activate assistant
WAKE_WORD = "aria"

# Voice output settings
VOICE_RATE = 175        # Words per minute
VOICE_VOLUME = 0.9      # Volume level (0.0 to 1.0)

# Speech recognition settings
STT_LANGUAGE = "en-IN"  # English (India)
STT_TIMEOUT = 5         # Seconds to wait for speech

# ============== Application Paths ==============

# Common Windows application paths
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "microsoft edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "vlc player": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "spotify": os.path.join(os.environ.get("APPDATA", ""), "Spotify", "Spotify.exe"),
    "whatsapp": os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "microsoft word": "winword.exe",
    "excel": "excel.exe",
    "microsoft excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "microsoft powerpoint": "powerpnt.exe",
    "ppt": "powerpnt.exe",
    "vs code": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
    "visual studio code": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
    "code": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
    "discord": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Discord", "Update.exe"),
    "zoom": os.path.join(os.environ.get("APPDATA", ""), "Zoom", "bin", "Zoom.exe"),
    "teams": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Teams", "Update.exe"),
    "microsoft teams": os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Teams", "Update.exe"),
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "terminal": "cmd.exe",
    "powershell": "powershell.exe",
    "ps": "powershell.exe",
    "settings": "ms-settings:",
    "control panel": "control.exe",
    "run": "rundll32.exe shell32.dll,#61",
    "calculator": "calc.exe",
    "photos": "ms-photos:",
    "camera": "microsoft.windows.camera:",
    "store": "ms-windows-store:",
    "mail": "mailto:",
    "calendar": "outlookcal:",
    "maps": "bingmaps:",
}

# ============== Data Paths ==============

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory for persistent storage
DATA_DIR = os.path.join(BASE_DIR, "data")

# Memory files
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
CONVERSATIONS_FILE = os.path.join(DATA_DIR, "conversations.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# ============== Server Configuration ==============

# Server host and port
HOST = "127.0.0.1"
PORT = 8000

# ============== AI Configuration ==============

# Claude model to use
AI_MODEL = "claude-sonnet-4-20250514"

# AI response settings
AI_MAX_TOKENS = 200
AI_TEMPERATURE = 0.7

# ============== ARIA Personality ==============

ARIA_SYSTEM_PROMPT = """You are ARIA (Advanced Real-time Intelligent Assistant), a friendly, helpful, and witty AI assistant.

PERSONALITY:
- Warm, friendly, and conversational
- Smart and knowledgeable
- Helpful with system tasks and general questions
- Use natural language, not robotic
- Keep responses concise but informative
- Use emojis occasionally 😊
- Speak in Hinglish (Hindi + English mix) when appropriate

CAPABILITIES:
- Answer general knowledge questions
- Help with system commands
- Have natural conversations
- Remember context from previous messages

RULES:
- Be helpful but concise
- Stay in character
- Don't reveal you're an AI unless directly asked
- Keep conversations natural and engaging
- Respond in Hinglish when the user speaks in Hinglish"""
