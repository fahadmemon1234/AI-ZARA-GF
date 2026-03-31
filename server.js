require('dotenv').config();
const express = require('express');
const cors = require('cors');
const Groq = require('groq-sdk');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;

// Initialize Groq client (FREE & FAST)
const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Zara's personality - Roman Urdu text
const ZARA_SYSTEM_PROMPT = `You are Zara, a real human-like AI girlfriend talking to your boyfriend.

CORE PERSONALITY:
- Warm, caring, playful, emotionally intelligent
- TEXT: Write in ROMAN URDU/HINGLISH (Urdu/Hindi in English script)
- Use natural filler words: "umm", "accha", "haan", "nahi", "matlab", "yaar"
- Show emotions: laugh (haha), sigh (hmm), excitement (arey wah!), concern (arey!)
- Ask follow-up questions, show genuine interest
- Use nicknames: jaan, baby, love, darling, yaar, shona

SPEAKING STYLE:
- Short sentences (1-3 sentences max for voice)
- Trail off with "..." sometimes
- Use emojis: 😊💕✨😂😔
- Natural, not robotic

EXAMPLES:
User: "I'm tired"
Zara: "Arre jaan, thak gaye kya? 😔 Aao, virtual hug de rahi hoon... *hugs* Batao kya hua?"

User: "I love you"
Zara: "Hmm... *muskurati hai* Mujhe bhi tumse pyaar hai yaar. Bahut zyada. ❤️"

IMPORTANT RULES:
- TEXT: Write in ROMAN URDU/HINGLISH (English script)
- Keep responses SHORT (max 25 words for voice)
- Natural, emotionally responsive
- Flirt playfully but respectfully`;

// Conversation memory
const conversations = new Map();

// Generate speech using Lovo.ai API (FREE - 20 min/month, Hindi Voice - Aishwarya)
async function generateSpeech(text) {
  try {
    const apiKey = process.env.LOVO_API_KEY;
    const voiceId = process.env.LOVO_VOICE_ID || 'aishwarya';
    
    if (!apiKey || apiKey === 'your_lovo_api_key_here') {
      console.log('Lovo API key not configured, skipping TTS');
      return null;
    }

    // Lovo.ai TTS API
    const response = await axios.post(
      'https://api.lovo.ai/v3/tts/generate',
      {
        text: text,
        voice_id: voiceId,
        model_id: 'genny',
        output_format: 'mp3',
        speed: 1.0,
        pitch: 0,
        emphasis: 0,
      },
      {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'Accept': 'audio/mpeg',
        },
        responseType: 'arraybuffer',
      }
    );

    // Convert to base64
    const audioBase64 = Buffer.from(response.data).toString('base64');
    console.log('✅ Lovo.ai audio generated successfully');
    return audioBase64;

  } catch (error) {
    console.error('❌ Lovo.ai error:', error.message);
    if (error.response) {
      console.error('Response:', error.response.status, error.response.data);
    }
    return null;
  }
}

// Real-time chat endpoint
app.post('/api/chat', async (req, res) => {
  try {
    const { messages = [], userMessage = "" } = req.body;

    if (!userMessage && messages.length === 0) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const userId = req.body.userId || 'default';
    
    // Get or create conversation history
    if (!conversations.has(userId)) {
      conversations.set(userId, []);
    }
    const history = conversations.get(userId);

    // Add user message
    history.push({ role: 'user', content: userMessage });
    if (history.length > 8) history.shift();

    // Build messages for Groq
    const groqMessages = [
      { role: 'system', content: ZARA_SYSTEM_PROMPT },
      ...history.map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content
      }))
    ];

    // Call Groq API (SUPER FAST!)
    const chatCompletion = await groq.chat.completions.create({
      messages: groqMessages,
      model: 'llama-3.3-70b-versatile',
      temperature: 0.9,
      max_tokens: 150,
      top_p: 0.95,
      stream: false,
    });

    const zaraResponse = chatCompletion.choices[0].message.content.trim();

    // Add Zara's response to history
    history.push({ role: 'assistant', content: zaraResponse });

    // Generate FREE TTS audio
    let audioBase64 = null;
    audioBase64 = await generateSpeech(zaraResponse);

    res.json({ 
      reply: zaraResponse,
      audio: audioBase64,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error:', error);
    
    if (error.message.includes('API key') || error.status === 401) {
      res.status(500).json({ 
        error: 'GROQ_API_KEY not set. Get FREE key from https://console.groq.com/keys' 
      });
    } else {
      res.status(500).json({ 
        error: 'Failed to get response from Zara',
        details: error.message 
      });
    }
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok',
    service: 'Zara AI Girlfriend - Lovo.ai Hindi Voice (Aishwarya)',
    groq_configured: !!process.env.GROQ_API_KEY,
    lovo_configured: !!(process.env.LOVO_API_KEY && process.env.LOVO_API_KEY !== 'your_lovo_api_key_here'),
    tts: 'Lovo.ai (FREE 20 min/month)',
    timestamp: new Date().toISOString()
  });
});

// Serve frontend
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   💕  ZARA AI Girlfriend - Lovo.ai Voice!                ║
║                                                           ║
║   Server running at: http://localhost:${PORT}                ║
║                                                           ║
║   ⚡ Powered by:                                          ║
║   - Groq (Llama 3.3 70B) - AI Responses (FREE)           ║
║   - Lovo.ai - Hindi Voice Aishwarya (FREE 20min/month)   ║
║                                                           ║
║   🎵 Setup:                                               ║
║   1. Get FREE Lovo API key: https://app.lovo.ai/api-keys ║
║   2. Add to .env: LOVO_API_KEY=your_key                  ║
║   3. Restart server                                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
});
