# 💕 ZARA - Your AI Girlfriend & Personal Assistant

**An advanced AI voice assistant with ultra-realistic human-like voice, pink girly theme, and automatic voice chat capabilities.**

![Version](https://img.shields.io/badge/version-3.0.0-pink)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🎤 Ultra-Realistic Voice
- **Voice Model:** ElevenLabs (Most realistic female voices)
- **Technology:** `eleven_flash_v2_5` - Latest & most advanced
- **Quality:** Human-like with natural breathing, pauses & emotions
- **Auto-Speak:** Every response is spoken automatically
- **Language:** English & Hinglish (Hindi + English mix)

### 💕 Girlfriend Personality
- Warm, caring & emotionally supportive
- Playful & flirty (but respectful)
- Uses cute nicknames (babe, baby, honey, sweetie)
- Remembers your conversations
- Auto-greets you when you open the app

### 🌸 Beautiful Pink Theme
- Girly pink/purple gradient UI
- Animated avatar with pulse rings
- 30-bar waveform visualization
- Responsive design (works on all devices)
- Smooth animations & transitions

### 🤖 System Automation (66+ Commands)
- Power control (shutdown, restart, sleep, lock)
- Application management (open/close apps)
- Volume & brightness control
- Media playback (YouTube, Spotify)
- Window management
- Screenshots & OCR
- File operations
- News & weather
- And much more!

### 🎯 Smart Features
- **Voice Input:** Click mic & speak (auto-sends)
- **Voice Output:** Ultra-realistic auto-speak
- **Text Chat:** Type and get voice responses
- **Quick Actions:** One-click common phrases
- **Memory:** Remembers conversations
- **Auto-Greeting:** Greets you on page load

### 🚀 Multi-API Support
- **Anthropic Claude** - Primary AI (Sonnet 4)
- **Google Gemini** - Backup AI
- **OpenAI GPT** - Additional AI option
- **ElevenLabs** - Premium voice generation
- **LiveKit** - Real-time audio communication
- **Mem0** - AI memory layer

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows 10/11
- Microphone (for voice input)
- Speakers (for voice output)

### Installation

**1. Clone or Download the Project**
```bash
cd "D:\Fahad Project\AI-Driven\zara-ai"
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure API Keys**

Edit `.env` file and add your API keys:

```env
# Anthropic (REQUIRED - for AI chat - Claude)
ANTHROPIC_API_KEY=sk_your_key_here

# ElevenLabs (REQUIRED - for ultra-realistic voice)
ELEVENLABS_API_KEY=sk_your_key_here
ELEVENLABS_VOICE_ID=RmT0JE37YE1NfodnZBnw

# Google Gemini (FREE - backup AI)
GEMINI_API_KEY=your_key_here

# OpenAI (OPTIONAL - GPT models)
OPENAI_API_KEY=your_key_here

# LiveKit (OPTIONAL - real-time audio)
LIVEKIT_API_KEY=your_key_here
LIVEKIT_API_SECRET=your_secret_here
LIVEKIT_URL=wss://your-project.livekit.cloud

# Mem0 (OPTIONAL - AI memory)
MEM0_API_KEY=your_key_here
```

**Get FREE API Keys:**
- **Anthropic:** https://console.anthropic.com (~100 requests/day FREE)
- **ElevenLabs:** https://elevenlabs.io/app/settings/api-keys (10k chars/month FREE)
- **Google Gemini:** https://makersuite.google.com/app/apikey (60 req/min FREE)
- **OpenAI:** https://platform.openai.com/api-keys ($5 free credit)
- **LiveKit:** https://cloud.livekit.io (Free tier available)
- **Mem0:** https://app.mem0.ai (Free tier available)

**4. Start Server**
```bash
python main.py
```

**5. Open Browser**
```
http://localhost:8000
```

**6. Start Chatting!**
- Click 🎤 mic button and speak
- Or type in the input box
- Or click quick action buttons
- ZARA will reply with ultra-realistic voice!

---

## 💬 How to Use

### Voice Chat (Recommended)
1. Click **🎤 Mic Button**
2. **Speak** your message
3. **Auto-sends** after you finish
4. **ZARA replies** with voice automatically

### Text Chat
1. **Type** in the input box
2. **Press Enter** or click **Send**
3. **ZARA replies** with voice

### Quick Actions
Just **click** any preset button:
- 👋 Say Hi
- 💕 Check In
- ❤️ Love
- 😄 Joke
- 😔 Comfort Me
- 🌟 Compliment
- ☀️ Good Morning
- 🌙 Good Night

### System Commands
Say or type:
```
"Open Chrome"
"Volume up"
"Take screenshot"
"Battery status"
"Weather in Lahore"
"Play music on YouTube"
```

---

## 🎤 Voice Commands

### Conversation
| Command | Response |
|---------|----------|
| "Hey ZARA" | Warm greeting |
| "I love you" | Love confession |
| "I'm tired" | Comfort & care |
| "Tell me a joke" | Funny joke |
| "Good morning" | Morning greeting |
| "Good night" | Night greeting |

### System Control
| Command | Action |
|---------|--------|
| "Shutdown computer" | Shuts down PC |
| "Restart computer" | Restarts PC |
| "Lock computer" | Locks screen |
| "Battery status" | Shows battery % |
| "Open Chrome" | Opens Chrome |
| "Volume up" | Increases volume |
| "Brightness up" | Increases brightness |
| "Take screenshot" | Captures screen |

---

## 🌸 Theme Customization

### Current Theme: Pink Girly
- **Background:** Dark pink/purple (#1a0a1a)
- **Accent:** Hot pink (#ff69b4)
- **Gradients:** Pink to purple
- **Avatar:** Animated with pink pulse rings

### Change Colors
Edit `public/index.html`:

```css
:root {
    --bg-primary: #1a0a1a;      /* Background */
    --accent-pink: #ff69b4;      /* Accent color */
    --accent-purple: #9b59b6;    /* Secondary */
}
```

---

## 🎯 Voice Settings

### Current Configuration
```python
Model: eleven_flash_v2_5  # Most realistic
Voice: Configurable       # Multiple voice options
Stability: 0.35           # More expressive
Similarity: 0.85          # Faithful to voice
Style: 0.50              # Natural speech patterns
Speaker Boost: Enabled    # Enhanced clarity
```

### Change Voice
Edit `.env`:
```env
# Available Voices:
ELEVENLABS_VOICE_ID=RmT0JE37YE1NfodnZBnw  # Default
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL  # Bella
ELEVENLABS_VOICE_ID=pNInz5obgJUvV3kV6PdQ  # Sarah
ELEVENLABS_VOICE_ID=jBpfuIE2acCO8z3wKNLl  # Domi
```

---

## 📁 Project Structure

```
zara-ai/
├── main.py                    # FastAPI backend
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── .env                       # API keys (DO NOT COMMIT!)
├── .env.example              # Template (safe to share)
├── .gitignore                # Git ignore rules
├── README.md                  # This file
├── FEATURES_GUIDE.md         # Complete feature guide
├── API_SETUP.md              # Complete API setup guide
├── API_INTEGRATION_SUMMARY.md # API integration details
├── modules/                   # All modules
│   ├── __init__.py
│   ├── multi_api_manager.py   # Multi-API manager
│   ├── voice_engine.py        # Voice engine
│   ├── command_router.py      # Command routing
│   ├── ai_brain.py           # AI brain (ZARA persona)
│   ├── memory_manager.py      # Memory management
│   ├── system_control.py      # System automation
│   ├── window_manager.py      # Window management
│   ├── app_manager.py         # App management
│   └── ... (more modules)
├── data/                      # User data (ignored by git)
│   ├── memory.json
│   └── conversations.json
└── public/                    # Frontend
    └── index.html            # Complete UI
```

---

## 🔧 Troubleshooting

### Voice Not Working
1. Check browser permissions (allow audio)
2. Check ElevenLabs API key in `.env`
3. Check console for errors (F12)
4. Refresh browser page

### Mic Not Working
1. Use Chrome or Edge browser
2. Allow microphone permission
3. Check mic is not muted
4. Check Windows sound settings

### ZARA Not Responding
1. Check server is running (`python main.py`)
2. Check API keys in `.env`
3. Check internet connection
4. Refresh browser page

### API Key Errors
1. Get valid API key from provider
2. Update `.env` file
3. Restart server
4. Check console for specific error

---

## 📊 API Limits (FREE Tiers)

| Service | Limit | Cost |
|---------|-------|------|
| **Anthropic Claude** | ~100 requests/day | FREE |
| **ElevenLabs** | 10,000 chars/month | FREE |
| **Google Gemini** | 60 requests/min | FREE |
| **OpenAI** | $5 free credit | FREE |
| **LiveKit** | Free tier available | FREE |
| **Mem0** | Free tier available | FREE |

---

## 🔒 Security

### Safe to Commit
- ✅ Source code
- ✅ HTML/CSS/JS
- ✅ Documentation
- ✅ `.env.example` (template)

### NEVER Commit
- ❌ `.env` (contains API keys!)
- ❌ `data/*.json` (user data)
- ❌ `data/memory.json` (memories)
- ❌ `data/conversations.json` (chat history)

### Git Setup
```bash
git init
git add .
git commit -m "Initial commit - ZARA AI Assistant"
```

`.gitignore` already configured to protect your secrets!

---

## 🎯 Features Summary

| Feature | Status |
|---------|--------|
| **Ultra-Realistic Voice** | ✅ ElevenLabs |
| **Auto-Speak** | ✅ Every response |
| **Voice Input** | ✅ Auto-send after speech |
| **Text Chat** | ✅ With voice replies |
| **Quick Actions** | ✅ 9 preset buttons |
| **System Control** | ✅ 66+ commands |
| **Girlfriend Personality** | ✅ Warm & caring |
| **Memory** | ✅ Remembers conversations |
| **Auto-Greeting** | ✅ Greets on load |
| **Pink Theme** | ✅ Girly UI |
| **Responsive** | ✅ All devices |
| **Waveform** | ✅ 30-bar animation |
| **Multi-API Support** | ✅ 6 AI APIs |
| **Hinglish Support** | ✅ Hindi + English |

---

## 💡 Pro Tips

1. **Use Chrome/Edge** for best voice recognition
2. **Allow microphone** permission when asked
3. **Allow audio** playback in browser
4. **Keep server running** while using
5. **Check console** (F12) for debugging
6. **Use voice input** - it's faster than typing
7. **Customize voice** in `.env` for different voices
8. **Check FEATURES_GUIDE.md** for complete guide
9. **Set up multiple APIs** for backup options

---

## 📞 Support

If you need help:
1. Check console (F12) for errors
2. Check `.env` file has valid API keys
3. Check server is running
4. Refresh browser page
5. Read `FEATURES_GUIDE.md` for detailed guide
6. Read `API_SETUP.md` for API configuration

---

## 🎉 Credits

Built with love using:
- **Anthropic Claude** - Primary AI engine
- **ElevenLabs** - Ultra-realistic voice synthesis
- **Google Gemini** - Backup AI
- **OpenAI GPT** - Additional AI option
- **LiveKit** - Real-time audio communication
- **Mem0** - AI memory layer
- **FastAPI** - Modern Python web framework
- **SpeechRecognition** - Voice input
- **Pyttsx3** - Offline TTS fallback

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 💕 Made with Love

**ZARA - Your AI Girlfriend** 🌸

**Built by Muhammad Fahad Memon**

Enjoy natural, human-like conversations with ultra-realistic voice!

---

**Start chatting now:** http://localhost:8000 🎤💕
