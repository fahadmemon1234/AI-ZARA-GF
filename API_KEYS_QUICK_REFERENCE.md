# 🔑 ARIA API Keys - Quick Reference

## ✅ Check Your .env File

Open `.env` in your project root and add your API keys:

```env
# REQUIRED (Choose at least one)
ANTHROPIC_API_KEY=sk-ant-00-your-key-here

# RECOMMENDED (FREE - Great backup!)
GEMINI_API_KEY=your-gemini-key-here

# OPTIONAL (But awesome!)
ELEVENLABS_API_KEY=your-elevenlabs-key-here  # Ultra-realistic voice
MEM0_API_KEY=your-mem0-key-here              # Long-term memory
LIVEKIT_API_KEY=your-livekit-key-here        # Real-time audio/video
OPENAI_API_KEY=sk-your-openai-key-here       # Advanced AI
```

---

## 🆓 Get FREE Keys (5 minutes each)

| API | Free Tier | Get Key | Time |
|-----|-----------|---------|------|
| **Gemini** | 1,500/day | [Get Key](https://makersuite.google.com/app/apikey) | 3 min |
| **Anthropic** | ~100/day | [Get Key](https://console.anthropic.com) | 5 min |
| **ElevenLabs** | 10k chars/month | [Get Key](https://elevenlabs.io/app/settings/api-keys) | 3 min |
| **Mem0** | 1,000 memories | [Get Key](https://app.mem0.ai/api-keys) | 3 min |
| **LiveKit** | 1,000 min/month | [Get Key](https://cloud.livekit.io) | 5 min |
| **OpenAI** | $5 credit | [Get Key](https://platform.openai.com/api-keys) | 10 min |

---

## 🚀 Quick Test

After adding keys, test with:

```bash
python -c "from modules.multi_api_manager import MultiAPIManager; api = MultiAPIManager(); print(api.get_status())"
```

Expected output shows which APIs are available:
```json
{
  "anthropic": {"available": true},
  "google": {"available": true},
  "openai": {"available": false},
  "elevenlabs": {"available": true},
  "livekit": {"available": false},
  "mem0": {"available": true}
}
```

---

## 💡 Minimum Setup

For basic ARIA functionality:

```env
ANTHROPIC_API_KEY=sk-ant-...
```

For best experience:

```env
ANTHROPIC_API_KEY=sk-ant-...    # Main AI
GEMINI_API_KEY=...               # Backup AI (FREE!)
ELEVENLABS_API_KEY=...           # Better voice
```

---

## 🎯 Usage Examples

### Chat with AI
```python
from modules.multi_api_manager import MultiAPIManager
api = MultiAPIManager()

# Auto-select best available AI
result = api.chat("Hello!")
print(result['reply'])
```

### Generate Realistic Voice
```python
# ElevenLabs (better than pyttsx3!)
audio = api.elevenlabs_tts("Welcome to ARIA!")
```

### Add Memory
```python
api.mem0_add_memory("user123", "My name is Waseem")
memories = api.mem0_get_memories("user123")
```

---

## ⚠️ Troubleshooting

**All APIs show as unavailable?**
- Check `.env` file exists
- Verify keys are correct (no typos)
- Restart Python/terminal
- Run: `pip install -r requirements.txt`

**"Module not found" error?**
```bash
pip install google-generativeai openai mem0ai livekit livekit-api
```

---

## 📞 Need Help?

- Full guide: `API_SETUP.md`
- Integration docs: `API_INTEGRATION_SUMMARY.md`
- Main README: `README.md`

---

**Add your keys and enjoy multi-AI features! 🎉**
