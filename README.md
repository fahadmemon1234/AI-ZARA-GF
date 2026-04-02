# 💕 ZARA - Your AI Girlfriend & Personal Assistant

**An advanced AI voice assistant with ultra-realistic human-like voice, pink girly theme, and automatic voice chat capabilities.**

![Version](https://img.shields.io/badge/version-2.0.0-pink)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

### 🎤 Ultra-Realistic Voice
- **Voice Model:** ElevenLabs Bella (Most realistic female voice)
- **Technology:** `eleven_flash_v2_5` - Latest & most advanced
- **Quality:** Human-like with natural breathing, pauses & emotions
- **Auto-Speak:** Every response is spoken automatically
- **Language:** English only

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
# ElevenLabs (REQUIRED - for ultra-realistic voice)
ELEVENLABS_API_KEY=sk_your_key_here
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL  # Bella voice

# Groq (FREE - for AI chat)
GROQ_API_KEY=gsk_your_key_here

# Google Gemini (FREE - backup AI)
GEMINI_API_KEY=your_key_here
```

**Get FREE API Keys:**
- **ElevenLabs:** https://elevenlabs.io/app/settings/api-keys (10k chars/month FREE)
- **Groq:** https://console.groq.com (Unlimited FREE)
- **Gemini:** https://aistudio.google.com/app/apikey (1,500/day FREE)

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
- Zara will reply with ultra-realistic voice!

---

## 💬 How to Use

### Voice Chat (Recommended)
1. Click **🎤 Mic Button**
2. **Speak** your message
3. **Auto-sends** after you finish
4. **Zara replies** with voice automatically

### Text Chat
1. **Type** in the input box
2. **Press Enter** or click **Send**
3. **Zara replies** with voice

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
| "Hey Zara" | Warm greeting |
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
Voice: Bella              # Ultra-realistic female
Stability: 0.35           # More expressive
Similarity: 0.85          # Faithful to voice
Style: 0.50              # Natural speech patterns
Speaker Boost: Enabled    # Enhanced clarity
```

### Change Voice
Edit `.env`:
```env
# Available Voices:
ELEVENLABS_VOICE_ID=EXAVITQu4vr4xnSDxMaL  # Bella (Current)
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
├── modules/                   # All modules
│   ├── __init__.py
│   ├── multi_api_manager.py   # AI API manager
│   ├── voice_engine.py        # Voice engine
│   ├── command_router.py      # Command routing
│   ├── ai_brain.py           # AI brain (ZARA persona)
│   └── ... (15 more modules)
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

### Zara Not Responding
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
| **ElevenLabs** | 10,000 chars/month | FREE |
| **Groq** | ~30 req/min | FREE |
| **Google Gemini** | 1,500 req/day | FREE |
| **LiveKit** | 1,000 min/month | FREE |

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
git commit -m "Initial commit - Zara AI Girlfriend"
```

`.gitignore` already configured to protect your secrets!

---

## 🎯 Features Summary

| Feature | Status |
|---------|--------|
| **Ultra-Realistic Voice** | ✅ ElevenLabs Bella |
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

---

## 📞 Support

If you need help:
1. Check console (F12) for errors
2. Check `.env` file has valid API keys
3. Check server is running
4. Refresh browser page
5. Read `FEATURES_GUIDE.md` for detailed guide

---

## 🎉 Credits

Built with love using:
- **ElevenLabs** - Ultra-realistic voice synthesis
- **Groq** - Fast AI responses (Llama 3.3)
- **Google Gemini** - Backup AI
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
