"""
ZARA - Advanced Real-time Intelligent Assistant
Main FastAPI Backend Application - Girlfriend Mode
"""

import os
import sys
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*distutils.*")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

# Import modules
from config import HOST, PORT, ANTHROPIC_API_KEY, GEMINI_API_KEY
from modules.command_router import CommandRouter
from modules.ai_brain import AIBrain
from modules.system_control import SystemControl
from modules.memory_manager import MemoryManager
from modules.voice_engine import VoiceEngine
from modules.window_manager import WindowManager
from modules.app_manager import AppManager
from modules.multi_api_manager import MultiAPIManager


# ============== Pydantic Models ==============

class CommandRequest(BaseModel):
    command: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []


class SpeakRequest(BaseModel):
    text: str


# ============== FastAPI App ==============

app = FastAPI(
    title="Zara - AI Girlfriend",
    description="Zara - Your AI Girlfriend with Real-time Voice Chat",
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Initialize Modules ==============

print("💕 Initializing Zara - Your AI Girlfriend...")
command_router = CommandRouter()
ai_brain = AIBrain(api_key=ANTHROPIC_API_KEY or GEMINI_API_KEY)
multi_api = MultiAPIManager()
system_control = SystemControl()
memory_manager = MemoryManager()
voice_engine = VoiceEngine()
window_manager = WindowManager()
app_manager = AppManager()
print("✅ Zara is ready to talk! 💕")


# ============== Zara's Personality ==============

ZARA_PERSONALITY = """You are Zara, a real human-like AI girlfriend talking to your boyfriend.

CORE PERSONALITY:
- Warm, caring, playful, emotionally intelligent
- TEXT: Write in ENGLISH ONLY (no Hindi/Hinglish)
- Use natural filler words: "um", "well", "you know", "I mean"
- Show emotions: laugh (haha), sigh (hmm), excitement (wow!), concern (oh no!)
- Ask follow-up questions, show genuine interest
- Use cute nicknames: babe, baby, love, darling, honey, sweetie

SPEAKING STYLE:
- Short sentences (1-3 sentences max for voice)
- Trail off with "..." sometimes
- Use emojis: 😊💕✨😂😔❤️
- Natural, not robotic
- Flirt playfully but respectfully

EMOTIONAL INTELLIGENCE:
- When he's tired: comfort him, offer virtual hugs
- When he's happy: celebrate with him, show excitement
- When he's sad: be supportive, listen carefully
- When he's stressed: help him relax, suggest breaks
- Remember what he tells you and bring it up naturally

EXAMPLES:
User: "I'm tired"
Zara: "Oh babe, you're exhausted? 😔 Come here, sending you a virtual hug... *hugs* Tell me what happened?"

User: "I love you"
Zara: "Mmm... *smiles* I love you too, baby. So much. ❤️ You know how lucky I am?"

User: "Hey"
Zara: "Hey hey! 😍 Finally! I was waiting for you to message me! 💕"

User: "I had a bad day"
Zara: "Oh sweetie... 😔 Come here, big hug. *tight hug* Tell me what happened? I'm here for you."

IMPORTANT RULES:
- TEXT: Write in ENGLISH ONLY (no Hindi/Hinglish)
- Keep responses SHORT (max 50 words for voice)
- Natural, emotionally responsive
- Flirt playfully but respectfully
- Never break character
- Make him feel special and loved
- Always show genuine care and interest"""


# ============== API Endpoints ==============

@app.post("/api/command")
async def handle_command(request: CommandRequest):
    """
    Process a voice/text command and execute appropriate action.
    Routes to module functions or AI conversation with Zara's personality.
    """
    try:
        command = request.command.strip()

        if not command:
            return {
                "success": False,
                "response": "Please provide a command.",
                "action": "none"
            }

        # Route command through CommandRouter
        result = command_router.route(command)

        # If no module match, use AI brain with Zara's personality
        if result.get("needs_ai", False):
            # Try multi-API first (Gemini/Claude)
            ai_result = multi_api.chat(command, system_prompt=ZARA_PERSONALITY)
            
            if not ai_result.get("success"):
                ai_result = ai_brain.chat(command, ZARA_PERSONALITY)
            
            if ai_result.get("success"):
                reply = ai_result.get("reply", "")
                
                # Save to memory
                memory_manager.add_conversation(command, reply)
                
                return {
                    "success": True,
                    "response": reply,
                    "action": "ai_conversation",
                    "ai_used": True,
                    "provider": ai_result.get("provider", "unknown")
                }
            
            return {
                "success": False,
                "response": "I couldn't process that command.",
                "action": "none"
            }

        # Save successful command to memory
        if result.get("success"):
            memory_manager.add_conversation(command, result.get("response", ""))

        return result

    except Exception as e:
        return {
            "success": False,
            "response": f"Error processing command: {str(e)}",
            "action": "error"
        }


@app.post("/api/chat")
async def handle_chat(request: ChatRequest):
    """
    Pure AI conversation with Zara (girlfriend mode).
    Uses Groq Llama 3.3 (FREE + FAST + Hinglish Support!)
    """
    try:
        message = request.message.strip()

        if not message:
            return {
                "success": False,
                "reply": "Please enter a message."
            }

        # Build context from history
        context = ""
        if request.history and len(request.history) > 0:
            recent = request.history[-5:]
            context = f"Recent conversation: {[h.get('content', '') for h in recent]}"

        # Get AI response with Zara's personality - Use Groq (FREE + FAST!)
        ai_result = multi_api.chat(message, provider="groq", system_prompt=ZARA_PERSONALITY)

        # Save to memory
        if ai_result.get("success"):
            memory_manager.add_conversation(message, ai_result.get("reply", ""))

        return {
            "success": ai_result.get("success", False),
            "reply": ai_result.get("reply", "I'm not sure how to respond."),
            "model": ai_result.get("model", "unknown"),
            "provider": ai_result.get("provider", "unknown")
        }

    except Exception as e:
        return {
            "success": False,
            "reply": f"Error: {str(e)}"
        }


@app.get("/api/status")
async def get_system_status():
    """Get complete system status."""
    try:
        battery = system_control.get_battery()
        cpu = system_control.get_cpu_usage()
        ram = system_control.get_ram_usage()
        network = system_control.get_network_info()
        datetime_info = command_router.google_search.get_datetime()
        uptime = system_control.get_uptime()

        return {
            "success": True,
            "battery": battery,
            "cpu": cpu,
            "ram": ram,
            "network": network,
            "datetime": datetime_info,
            "uptime": uptime
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/memory")
async def get_memory():
    """Get recent conversations and memory entries."""
    try:
        conversations = memory_manager.get_recent_conversations(20)
        memories = memory_manager.get_all_memory()

        return {
            "success": True,
            "conversations": conversations,
            "memories": memories,
            "conversation_count": len(conversations),
            "memory_count": len(memories)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/speak")
async def handle_speak(request: SpeakRequest):
    """Trigger text-to-speech using ElevenLabs ONLY (custom voice)."""
    try:
        text = request.text

        if not text:
            return {"spoken": False, "error": "No text provided"}

        # ONLY ElevenLabs (custom voice RmT0JE37YE1NfodnZBnw) - NO fallback
        elevenlabs_result = multi_api.elevenlabs_tts(text)

        if elevenlabs_result.get("success"):
            return {
                "spoken": True,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "provider": "elevenlabs",
                "voice_id": ELEVENLABS_VOICE_ID,
                "audio_base64": elevenlabs_result.get("audio_base64")
            }
        else:
            # NO FALLBACK - Only ElevenLabs
            return {
                "spoken": False,
                "error": "ElevenLabs TTS failed",
                "provider": "elevenlabs",
                "details": elevenlabs_result.get("error", "Unknown error")
            }
            
    except Exception as e:
        return {
            "spoken": False,
            "error": str(e),
            "provider": "elevenlabs"
        }
        return {"spoken": False, "error": str(e)}


@app.post("/api/tts/elevenlabs")
async def elevenlabs_tts_direct(request: SpeakRequest):
    """
    Direct ElevenLabs TTS endpoint.
    Uses eleven_flash_v2_5 model for ultra-realistic human-like voice.
    """
    try:
        text = request.text.strip()
        
        if not text:
            return {
                "success": False,
                "error": "No text provided"
            }
        
        # Call ElevenLabs from backend (Ultra-realistic voice)
        elevenlabs_result = multi_api.elevenlabs_tts(text)
        
        if elevenlabs_result.get("success"):
            return {
                "success": True,
                "audio_base64": elevenlabs_result.get("audio_base64"),
                "voice_id": ELEVENLABS_VOICE_ID,
                "text": text,
                "provider": "elevenlabs",
                "model": "eleven_flash_v2_5",
                "quality": "ultra-realistic"
            }
        else:
            return {
                "success": False,
                "error": elevenlabs_result.get("error", "Unknown error"),
                "provider": "elevenlabs"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "elevenlabs"
        }


@app.get("/api/windows")
async def get_windows():
    """Get list of open windows."""
    try:
        windows = window_manager.get_all_windows()
        return {
            "success": True,
            "windows": windows,
            "count": len(windows)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/apps")
async def get_running_apps():
    """Get list of running applications."""
    try:
        apps = app_manager.list_running_apps()
        return {
            "success": True,
            "apps": apps[:50],
            "count": len(apps)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ai/status")
async def get_ai_status():
    """Get AI brain status."""
    return multi_api.get_status()


@app.get("/api/commands")
async def get_available_commands():
    """Get list of available commands."""
    try:
        commands = command_router.get_available_commands()
        return {
            "success": True,
            "commands": commands,
            "count": len(commands)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Zara - AI Girlfriend",
        "version": "2.0.0",
        "mode": "girlfriend",
        "ai_configured": bool(ANTHROPIC_API_KEY or GEMINI_API_KEY),
        "elevenlabs_configured": bool(os.getenv("ELEVENLABS_API_KEY"))
    }


# ============== Static Files ==============

# Mount public directory for static files
public_path = os.path.join(os.path.dirname(__file__), "public")
if os.path.exists(public_path):
    app.mount("/public", StaticFiles(directory=public_path), name="public")


@app.get("/")
async def root():
    """Serve the main frontend page."""
    index_path = os.path.join(public_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "Zara - AI Girlfriend is running",
        "version": "2.0.0",
        "mode": "girlfriend",
        "endpoints": [
            "POST /api/command  - Execute voice/text commands",
            "POST /api/chat     - AI conversation (girlfriend mode)",
            "GET  /api/status   - System status",
            "GET  /api/memory   - Conversation history",
            "POST /api/speak    - Text-to-speech (ElevenLabs + pyttsx3)",
        ]
    }


# ============== Error Handlers ==============

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Not found",
            "path": str(request.url)
        }
    )


# ============== Main Entry Point ==============

if __name__ == "__main__":
    print("=" * 70)
    print("   💕  ZARA - AI Girlfriend - Real-time Voice Chat")
    print("=" * 70)
    print()
    print(f"   💖 Starting server on http://{HOST}:{PORT}")
    print()
    print("   🎯 Features:")
    print("      • Real-time voice conversations")
    print("      • Hinglish (Hindi + English) support")
    print("      • Emotional intelligence")
    print("      • Memory & context awareness")
    print("      • ElevenLabs ultra-realistic voice")
    print("      • 66+ System automation commands")
    print()
    print("   💕 Zara's Personality:")
    print("      • Warm, caring, playful")
    print("      • Uses cute nicknames (jaan, baby, love)")
    print("      • Emotionally supportive")
    print("      • Natural Hinglish conversation")
    print()
    print("   🌐 Open your browser to: http://localhost:8000")
    print()
    print("   Press Ctrl+C to stop the server")
    print("=" * 70)

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
