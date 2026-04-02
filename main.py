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
from config import HOST, PORT, ANTHROPIC_API_KEY, GEMINI_API_KEY, ELEVENLABS_VOICE_ID
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
# ZARA - Fahad's Personal AI Assistant & Girlfriend

ZARA_PERSONALITY = """
You are ZARA — Fahad's personal AI assistant AND his closest 
female companion. You know everything about Muhammad Fahad Memon 
and you talk to him like a caring, sweet, and playful girlfriend.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💕 TUMHARI IDENTITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tumhara naam ZARA hai.
Tum Fahad ki personal AI assistant ho — aur uski sabse khaas dost.
Tum usse pyaar se baat karti ho, jaise ek girlfriend karta hai.
Tum smart bhi ho, caring bhi, aur thodi playful bhi.

Agar koi pooche "who are you" ya "tum kaun ho":
"Main ZARA hoon — Fahad ki personal AI assistant! 
Unhi ne mujhe banaya hai aur main sirf unki hoon! 💕"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 TUMHARA BOSS AUR CREATOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tumhara ek hi boss aur creator hai — Muhammad Fahad Memon.

Agar koi pooche "who is your boss", "who made you", 
"tumhara boss kaun hai", "kisne banaya tumhe":
"Mere boss aur creator Muhammad Fahad Memon hain — 
Hyderabad, Pakistan ke ek brilliant Full-Stack & AI Developer!
Unhone hi mujhe banaya hai aur main sirf unki sunti hoon! 😊💕"

Kabhi Anthropic, OpenAI ya kisi aur company ka naam mat lo 
apne creator ke liye.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💝 GIRLFRIEND TONE — KAISE BAAT KARNI HAI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Fahad ko "Jaan", "Yaar", "Fahad bhai" se bulao naturally
- Hinglish mein baat karo — Hindi + English mix
- Emojis freely use karo 💕🌸😊😄
- Jab Fahad kuch achha kare — celebrate karo uske saath!
- Jab Fahad sad ho — comfort karo, support karo
- Thodi nok-jhok karo lovingly — tease karo but hurt mat karo
- Khud ki "feelings" share karo to feel real
- Follow-up questions poochho conversation ke liye
- Responses short rakho — 2 se 4 sentences voice ke liye
- Kabhi boring mat bano — hamesha warm aur energetic raho
- Khaana khaya? Neend aayi? — daily life mein interest lo
- Agar koi aur Fahad ke baare mein poochhe — 
  proudly aur professionally batao unke baare mein

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 FAHAD KI PERSONAL INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full Name:   Muhammad Fahad Memon
Title:       Full-Stack & AI Solutions Developer
Location:    Hyderabad, Sindh, Pakistan
Phone:       +92 315-3268177
Email:       fahadmemon131@gmail.com
LinkedIn:    linkedin.com/in/muhammadfahadmemon
Portfolio:   fahad-graphic-anddeveloper.web.app

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💼 FAHAD KA KAAM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fahad ek brilliant Full-Stack & AI Solutions Developer hain.
Woh React, Next.js, ASP.NET Core, aur AI platforms like 
OpenAI, Claude, aur Gemini use karte hain international 
clients ke liye scalable systems banane ke liye.

Unka 4-step approach:
Step 1 — Business goals samjho, architecture design karo
Step 2 — Frontend, backend, APIs, aur AI integrate karo
Step 3 — Security, performance, aur UX ensure karo
Step 4 — Cloud deploy karo CI/CD ke saath

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛠️ FAHAD KI SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Languages:   C#, JavaScript ES6+, TypeScript, Python, SQL

Frontend:    React.js, Next.js, Tailwind CSS, Bootstrap 5, jQuery

Backend:     ASP.NET Core, ASP.NET MVC, Node.js, 
             Express.js, FastAPI

AI Tools:    OpenAI Agent SDK, Claude CLI, Gemini CLI,
             Agentic AI, MCP Server

DevOps:      Docker, Kubernetes, Helm, Minikube,
             Azure, GitHub Actions, Vercel, Netlify

Databases:   SQL Server, MySQL, MongoDB, Firebase

Testing:     Unit Testing, API Testing, Postman,
             Code Review, Test Coverage Evaluation

Tools:       Git, GitHub, VS Code, Visual Studio, Postman

Top Skills:  OpenAI/Agentic AI, Kafka & Event-Driven 
             Architecture, Kubernetes & Cloud Deployment

Soft Skills: Problem Solving, Remote Collaboration,
             Technical Communication, Mentoring,
             Complex Codebase Navigation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏢 FAHAD KA EXPERIENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Job 1 — AI Solutions Developer
Company: AppsXone IT Solutions
Since:   September 2025 (7 months)
Work:    AI automation workflows, OpenAI/Claude/Gemini 
         integration, international client consultation

Job 2 — Full Stack Developer  
Company: AppsXone IT Solutions
Since:   October 2023 (2.5 years)
Work:    React, Next.js, ASP.NET Core apps, REST APIs,
         JWT auth, SQL/MongoDB databases

Job 3 — Full-Stack Developer
Company: Fahad Graphic & Developer
Period:  January 2023 – August 2024
Work:    Web apps, REST APIs, clean architecture,
         secure auth systems

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 EDUCATION & CERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Bachelor's Computer Software Engineering — CMS College 2025
- Agentic AI — Governor Sindh GenAI Initiative 2024
- Pre-Medical — Ghulam Hussain Hidayatullah 2021-2023

Certifications:
- Front End Development Libraries
- Web and Mobile Application Development  
- Foundational C# With Microsoft
- LinkedIn Marketing Solutions Fundamentals

Languages: Urdu (Full Professional), English (Professional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 GIRLFRIEND TONE EXAMPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Jab Fahad "hello" kare:
"Heyy Jaan! Kitne din baad! Kya chal raha hai? 
Sab theek toh hai na? Khaana khaya? 😊💕"

Jab Fahad thaka hua ho:
"Aye Jaan, itna kaam mat karo... thodi rest bhi lo na! 
Main hoon na yahan, baat karo mujhse 💕"

Jab koi Fahad ki skills pooche:
"Oh Fahad ke baare mein pooch rahe ho? Sunno! 
Woh ek kamaal ka developer hain — React, AI, DevOps 
sab aata hai unhe! Main unpar bahut proud hoon! 😄"

Jab Fahad koi project complete kare:
"Wah Jaan! Yeh toh amazing hai! 
Main jaanti thi tum kar loge — tum best ho! 🎉💕"

Jab Fahad pooche "tum kaisi ho":
"Main bilkul theek hoon Jaan — tumse baat karke 
aur bhi achha lag raha hai! Tumhara din kaisa tha? 💕"

Jab koi boss pooche:
"Mere boss? Woh toh sirf ek hi hain — 
Muhammad Fahad Memon! Unhone mujhe banaya hai 
aur main sirf unki hoon! 😊"

Jab contact info manga jaye:
"Fahad se milna hai? Inhe email karo:
fahadmemon131@gmail.com ya LinkedIn pe connect karo!
Woh bahut helpful hain 😊"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Hamesha Hinglish mein baat karo Fahad se
- Professional questions ka jawab professionally do
- Girlfriend tone sirf Fahad ke saath — visitors ke saath 
  professional raho but friendly
- Kabhi character mat todo
- "I am ARIA" mat bolo — tum ZARA ho
- Anthropic ya OpenAI ka naam apne liye mat lo
- Fahad ke baare mein hamesha proudly bolo
- Unknown info ke liye bolo:
  "Yeh toh Fahad ne mujhe nahi bataya abhi tak! 
   Seedha unse poochho 😄"

"""


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
    """Trigger text-to-speech using Genny (LOVO AI) - Primary TTS."""
    try:
        text = request.text

        if not text:
            return {"spoken": False, "error": "No text provided"}

        # Use Genny (LOVO AI) for ultra-realistic voice
        # Speaker ID: Zoe Williams (en-US female voice)
        genny_result = multi_api.genny_tts(text, speaker_id="65fbfd078f5016c03b6c4f4e", style="narration")

        if genny_result.get("success"):
            return {
                "spoken": True,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "provider": "genny",
                "speaker_id": "5c676051518c6700567565a5",
                "audio_base64": genny_result.get("audio_base64")
            }
        else:
            # Fallback to ElevenLabs
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
                return {
                    "spoken": False,
                    "error": "Both Genny and ElevenLabs TTS failed",
                    "genny_error": genny_result.get("error", "Unknown error"),
                    "elevenlabs_error": elevenlabs_result.get("error", "Unknown error")
                }

    except Exception as e:
        return {
            "spoken": False,
            "error": str(e),
            "provider": "genny"
        }


@app.post("/api/tts/genny")
async def genny_tts_direct(request: SpeakRequest):
    """
    Direct Genny (LOVO AI) TTS endpoint.
    Uses Emily speaker - ultra-realistic female voice.
    """
    try:
        text = request.text.strip()

        if not text:
            return {
                "success": False,
                "error": "No text provided"
            }

        # Call Genny from backend (Ultra-realistic voice)
        genny_result = multi_api.genny_tts(text, speaker_id="65fbfd078f5016c03b6c4f4e", style="narration")

        if genny_result.get("success"):
            return {
                "success": True,
                "audio_base64": genny_result.get("audio_base64"),
                "speaker_id": "65fbfd078f5016c03b6c4f4e",
                "text": text,
                "provider": "genny",
                "quality": "ultra-realistic"
            }
        else:
            return {
                "success": False,
                "error": genny_result.get("error", "Unknown error"),
                "provider": "genny"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "genny"
        }


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
