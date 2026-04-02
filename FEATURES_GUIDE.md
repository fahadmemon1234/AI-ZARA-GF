# 🎯 ARIA (Zara) - Complete Features Guide

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Voice Commands](#voice-commands)
3. [Text Commands](#text-commands)
4. [Quick Actions](#quick-actions)
5. [System Automation](#system-automation)
6. [AI Conversation](#ai-conversation)
7. [Settings & Configuration](#settings)

---

## 🚀 Quick Start

### Step 1: Start Server
```bash
cd "D:\Fahad Project\AI-Driven\zara-ai"
python main.py
```

### Step 2: Open Browser
```
http://localhost:8000
```

### Step 3: Start Chatting!
- **Type** in the input box
- **Or click** 🎤 mic button and speak
- **Or click** any quick action button

---

## 🎤 Voice Commands

### How to Use:
1. Click **🎤 Mic Button**
2. **Speak** your command
3. **Auto-sends** after you finish speaking
4. **Zara replies** with voice automatically

### Voice Command Examples:

| Say This | Zara Does |
|----------|-----------|
| "Hey Zara" | Greets you back |
| "I love you" | Says she loves you too |
| "I'm tired" | Comforts you |
| "Tell me a joke" | Tells a joke |
| "Good morning" | Morning greeting |
| "Good night" | Night greeting |
| "You're amazing" | Thanks you |
| "I had a bad day" | Comforts you |

---

## 💬 Text Commands

### How to Use:
1. **Type** in the input box
2. **Press Enter** or click **Send**
3. **Zara replies** automatically with voice

### Text Command Examples:

#### **Casual Conversation:**
```
"Hey"
"How are you?"
"What's up?"
"I miss you"
"You're beautiful"
```

#### **Emotional:**
```
"I love you"
"I'm sad"
"I'm happy"
"I'm stressed"
"Comfort me"
```

#### **Questions:**
```
"What time is it?"
"What's the date?"
"Tell me something interesting"
```

---

## ⚡ Quick Actions

### Pre-made Buttons (Click to Use):

| Button | What It Does |
|--------|--------------|
| 👋 **Say Hi** | "Hey Zara" |
| 💕 **Check In** | "How are you?" |
| ❤️ **Love** | "I love you" |
| 😄 **Joke** | "Tell me a joke" |
| 😔 **Comfort Me** | "I had a bad day" |
| 🌟 **Compliment** | "You're amazing" |
| 👗 **Flirt** | "What are you wearing" |
| ☀️ **Good Morning** | Morning greeting |
| 🌙 **Good Night** | Night greeting |

---

## 🤖 System Automation Features

### Voice + Text Commands for System Control:

#### **Power & System:**
```
"Shutdown computer"
"Restart computer"
"Go to sleep"
"Lock computer"
"Battery status"
"System status"
```

#### **Applications:**
```
"Open Chrome"
"Open Notepad"
"Open Spotify"
"Close Chrome"
"Is Chrome running?"
```

#### **Volume Control:**
```
"Volume up"
"Volume down"
"Mute"
"Set volume to 50"
```

#### **Brightness:**
```
"Brightness up"
"Brightness down"
"Set brightness to 70"
```

#### **Media Control:**
```
"Play Bohemian Rhapsody on YouTube"
"Play Lo-Fi on Spotify"
"Next track"
"Pause music"
"Stop music"
```

#### **Windows:**
```
"Minimize window"
"Maximize window"
"Close window"
"Show desktop"
"Switch to Chrome"
```

#### **Screenshots:**
```
"Take screenshot"
"Read screen text"
```

#### **Files:**
```
"Open Documents"
"Open Downloads"
"Open Pictures"
```

#### **Information:**
```
"News"
"Tech news"
"Pakistan news"
"Weather in Lahore"
"What time is it?"
"What's the date?"
"Search Python tutorials"
```

---

## 💕 AI Conversation (Girlfriend Mode)

### How It Works:
- Zara responds like a **real girlfriend**
- Uses **English only** (no Hindi/Hinglish)
- **Ultra-realistic voice** (ElevenLabs Bella)
- **Auto-speaks** every response
- **Remembers** your conversations

### Conversation Starters:

```
"Hey Zara, how was your day?"
"I had a rough day at work"
"Do you love me?"
"What do you think about me?"
"Tell me something sweet"
"I need a hug"
"You make me happy"
```

### Zara's Personality:
- ✅ Warm & caring
- ✅ Playful & flirty
- ✅ Emotionally supportive
- ✅ Uses cute nicknames (babe, baby, honey, sweetie)
- ✅ Remembers what you tell her
- ✅ Ultra-realistic human-like voice

---

## 🎤 Voice Settings

### Current Configuration:
- **Voice:** Bella (Ultra-realistic female)
- **Model:** eleven_flash_v2_5 (Most advanced)
- **Quality:** Ultra-realistic & human-like
- **Auto-Speak:** Enabled (always speaks)
- **Language:** English only

### Voice Features:
- ✅ Emotional & expressive
- ✅ Natural breathing & pauses
- ✅ Human-like intonation
- ✅ Speaker boost for clarity
- ✅ Auto-plays on every response

---

## 🌸 UI Features

### Pink Girly Theme:
- **Background:** Dark pink/purple gradient
- **Accent Colors:** Hot pink (#ff69b4)
- **Avatar:** Animated with pulse rings
- **Waveform:** 30 bars animate when speaking
- **Chat Bubbles:** Pink/purple gradient

### Responsive Design:
- ✅ Works on desktop
- ✅ Works on tablet
- ✅ Works on mobile
- ✅ Auto-adjusts for screen size

---

## ⚙️ Settings & Configuration

### API Keys (in .env file):

| Service | Purpose | Status |
|---------|---------|--------|
| **Groq** | AI Chat (Llama 3.3) | ✅ Configured |
| **Gemini** | Backup AI | ✅ Configured |
| **ElevenLabs** | Ultra-realistic voice | ✅ Configured |
| **LiveKit** | Real-time AV | ✅ Configured |

### How to Change Voice:
1. Open `.env` file
2. Change `ELEVENLABS_VOICE_ID`:
   - `EXAVITQu4vr4xnSDxMaL` (Bella - Current)
   - `pNInz5obgJUvV3kV6PdQ` (Sarah)
   - `jBpfuIE2acCO8z3wKNLl` (Domi)
3. Restart server

### How to Change Theme:
1. Open `public/index.html`
2. Edit CSS variables in `:root`
3. Change colors:
   ```css
   --accent-pink: #ff69b4;  /* Change this */
   --bg-primary: #1a0a1a;   /* Change this */
   ```

---

## 🐛 Troubleshooting

### Voice Not Working:
1. Check browser permissions (allow audio)
2. Check ElevenLabs API key in `.env`
3. Check console for errors (F12)

### Mic Not Working:
1. Use Chrome or Edge browser
2. Allow microphone permission
3. Check mic is not muted

### Zara Not Responding:
1. Check server is running (`python main.py`)
2. Check API keys in `.env`
3. Refresh browser page

### Duplicate Messages:
- Already fixed! (Send only once after voice ends)

---

## 📊 Feature Summary

| Feature | Status | How to Use |
|---------|--------|------------|
| **Voice Input** | ✅ | Click 🎤 mic button |
| **Voice Output** | ✅ | Auto-speaks every reply |
| **Text Chat** | ✅ | Type and press Enter |
| **Quick Actions** | ✅ | Click preset buttons |
| **System Control** | ✅ | Say/type commands |
| **AI Conversation** | ✅ | Chat naturally |
| **Memory** | ✅ | Remembers conversations |
| **Auto-Greeting** | ✅ | Greets on page load |
| **Pink Theme** | ✅ | Girly pink/purple UI |
| **Responsive** | ✅ | Works on all devices |

---

## 🎯 Best Practices

1. **Use Chrome/Edge** for best voice recognition
2. **Allow microphone** permission when asked
3. **Allow audio** playback in browser
4. **Keep server running** while using
5. **Check console** (F12) for debugging

---

## 💡 Pro Tips

1. **Voice is faster** than typing - use mic button
2. **Quick actions** for common phrases
3. **Be natural** - talk like to a real person
4. **Check logs** in console for debugging
5. **Customize** `.env` for different voices

---

## 📞 Support

If you need help:
1. Check console (F12) for errors
2. Check `.env` file has valid API keys
3. Check server is running
4. Refresh browser page

---

**Enjoy chatting with Zara! 💕🎤**
