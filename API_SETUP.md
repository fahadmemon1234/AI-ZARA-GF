# 🔑 ARIA - Complete API Setup Guide

This guide shows you how to get FREE API keys for all AI services supported by ARIA.

---

## 📋 Table of Contents

1. [Anthropic Claude](#anthropic-claude)
2. [Google Gemini](#google-gemini)
3. [OpenAI GPT](#openai-gpt)
4. [ElevenLabs Voice](#elevenlabs-voice)
5. [LiveKit Real-Time](#livekit-real-time)
6. [Mem0 Memory](#mem0-memory)
7. [Quick Comparison](#quick-comparison)

---

## 🤖 Anthropic Claude

**Best for**: Natural conversations, reasoning, coding

### Get FREE API Key:

1. **Visit**: https://console.anthropic.com
2. **Sign up** with email or Google account
3. **Verify** your email
4. Go to **API Keys** section
5. Click **"Create Key"**
6. **Copy** the key (starts with `sk-ant-`)
7. Add to `.env`:
   ```env
   ANTHROPIC_API_KEY=sk-ant-...your-key-here
   ```

### Free Tier:
- ~100 requests/day free
- Claude 3.5 Sonnet model
- Fast responses

### Usage in ARIA:
```python
from modules.multi_api_manager import MultiAPIManager

api = MultiAPIManager()
result = api.claude_chat("Hello, how are you?")
print(result['reply'])
```

---

## 🌟 Google Gemini

**Best for**: Multi-modal tasks, images + text, Google integration

### Get FREE API Key:

1. **Visit**: https://makersuite.google.com/app/apikey
2. **Sign in** with Google account
3. Click **"Create API Key"**
4. Select your project (or create new)
5. **Copy** the key
6. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   ```

### Free Tier:
- 60 requests/minute
- 1,500 requests/day
- Gemini Pro model
- Completely FREE!

### Usage in ARIA:
```python
api = MultiAPIManager()
result = api.gemini_chat("Explain quantum physics")
print(result['reply'])
```

---

## 🧠 OpenAI GPT

**Best for**: Advanced reasoning, GPT-4, large context

### Get API Key:

1. **Visit**: https://platform.openai.com/api-keys
2. **Sign up** with email
3. **Verify** phone number
4. Go to **API Keys** section
5. Click **"Create new secret key"**
6. **Copy** the key (starts with `sk-`)
7. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-...your-key-here
   ```

### Free Trial:
- $5 free credit for new accounts
- GPT-3.5-turbo: Very cheap
- GPT-4: More expensive

### Usage in ARIA:
```python
api = MultiAPIManager()
result = api.openai_chat("Write a poem", model="gpt-3.5-turbo")
print(result['reply'])
```

---

## 🎤 ElevenLabs Voice

**Best for**: Ultra-realistic AI voices, better than pyttsx3

### Get FREE API Key:

1. **Visit**: https://elevenlabs.io/app/settings/api-keys
2. **Sign up** with email or Google
3. Go to **Profile** → **API Keys**
4. **Copy** your API key
5. Add to `.env`:
   ```env
   ELEVENLABS_API_KEY=your_elevenlabs_key_here
   ELEVENLABS_VOICE_ID=Rachel  # or any voice ID
   ```

### Free Tier:
- 10,000 characters/month
- 3 custom voices
- Commercial use allowed
- Ultra-realistic quality

### Available Voices:
- **Rachel**: Calm, professional female
- **Domi**: Energetic female
- **Bella**: Warm female
- **Adam**: Deep male
- **Josh**: Conversational male

### Usage in ARIA:
```python
api = MultiAPIManager()

# Generate speech
result = api.elevenlabs_tts("Hello, I am ARIA!")
if result['success']:
    # Save or play audio_base64
    print("Audio generated!")

# Get available voices
voices = api.get_elevenlabs_voices()
print(voices['voices'])
```

---

## 📹 LiveKit Real-Time

**Best for**: Voice/video calls, real-time communication

### Get FREE API Keys:

1. **Visit**: https://cloud.livekit.io
2. **Sign up** with GitHub or email
3. **Create new project**
4. Go to **Settings** → **API Keys**
5. Click **"Create API Key"**
6. **Copy** both Key and Secret
7. Add to `.env`:
   ```env
   LIVEKIT_API_KEY=your_livekit_key_here
   LIVEKIT_API_SECRET=your_livekit_secret_here
   LIVEKIT_URL=wss://your-project.livekit.cloud
   ```

### Free Tier:
- 1,000 minutes/month
- Unlimited participants
- HD quality
- Screen sharing

### Usage in ARIA:
```python
api = MultiAPIManager()

# Generate room token
token_info = api.generate_livekit_token(
    room_name="meeting-room",
    participant_name="John"
)
if token_info['success']:
    print(f"Token: {token_info['token']}")
    print(f"URL: {token_info['url']}")
```

---

## 💾 Mem0 Memory

**Best for**: Long-term AI memory, personalized conversations

### Get FREE API Key:

1. **Visit**: https://app.mem0.ai/api-keys
2. **Sign up** with email
3. Go to **API Keys** section
4. Click **"Create Key"**
5. **Copy** the key
6. Add to `.env`:
   ```env
   MEM0_API_KEY=your_mem0_key_here
   ```

### Free Tier:
- 1,000 memories
- Unlimited searches
- Perfect for personal AI

### Usage in ARIA:
```python
api = MultiAPIManager()

# Add memory
api.mem0_add_memory(
    user_id="user123",
    message="My name is Waseem and I like pizza"
)

# Get memories
memories = api.mem0_get_memories(user_id="user123")
print(memories['memories'])

# Search memories
results = api.mem0_search(user_id="user123", query="favorite food")
print(results['results'])
```

---

## ⚡ Quick Comparison

| Service | Free Tier | Best For | Setup Time |
|---------|-----------|----------|------------|
| **Anthropic** | ~100/day | Conversations | 5 min |
| **Google Gemini** | 1,500/day | Multi-modal | 3 min |
| **OpenAI** | $5 credit | Advanced tasks | 10 min |
| **ElevenLabs** | 10k chars/month | Voice generation | 3 min |
| **LiveKit** | 1,000 min/month | Real-time AV | 5 min |
| **Mem0** | 1,000 memories | AI memory | 3 min |

---

## 🚀 Recommended Setup

For **best experience** with ARIA:

### Minimum (Required):
```env
ANTHROPIC_API_KEY=sk-ant-...  # Main AI
```

### Recommended (Better):
```env
ANTHROPIC_API_KEY=sk-ant-...  # Main AI
GEMINI_API_KEY=...            # Backup AI
ELEVENLABS_API_KEY=...        # Better voice
```

### Complete (Best):
```env
ANTHROPIC_API_KEY=sk-ant-...  # Main AI
GEMINI_API_KEY=...            # Backup AI
OPENAI_API_KEY=sk-...         # Advanced tasks
ELEVENLABS_API_KEY=...        # Ultra-realistic voice
LIVEKIT_API_KEY=...           # Real-time features
LIVEKIT_API_SECRET=...
LIVEKIT_URL=...
MEM0_API_KEY=...              # Long-term memory
```

---

## 🔧 Testing Your APIs

After adding keys to `.env`, run:

```bash
python test_modules.py
```

Or test individual APIs:

```python
from modules.multi_api_manager import MultiAPIManager

api = MultiAPIManager()

# Check all APIs
status = api.get_status()
print(status)

# Test chat
result = api.chat("Hello!", provider="auto")
print(f"AI Response: {result['reply']}")
```

---

## 💡 Tips

1. **Start with FREE tiers** - All services have generous free plans
2. **Use Gemini as backup** - Completely free, good quality
3. **ElevenLabs for voice** - Much better than pyttsx3
4. **Mem0 for memory** - Better than local JSON files
5. **Monitor usage** - Set up billing alerts

---

## 🆘 Troubleshooting

### "API key not valid"
- Check for typos
- Ensure no extra spaces
- Verify key format matches expected format

### "Quota exceeded"
- Check your usage dashboard
- Wait for reset (usually daily/monthly)
- Upgrade plan if needed

### "Module not found"
```bash
pip install -r requirements.txt
```

---

## 📞 Support Links

- **Anthropic**: https://support.anthropic.com
- **Google Gemini**: https://support.google.com
- **OpenAI**: https://help.openai.com
- **ElevenLabs**: https://elevenlabs.io/docs
- **LiveKit**: https://docs.livekit.io
- **Mem0**: https://docs.mem0.ai

---

**Get your FREE keys and start using ARIA with multiple AI providers! 🎉**
