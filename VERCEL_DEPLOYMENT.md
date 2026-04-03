# 🚀 Vercel Deployment Guide for ZARA AI

## ✅ What's Been Updated

Your ZARA AI project is now **Vercel-compatible**! Here's what changed:

### Files Created/Modified:
1. ✅ `vercel.json` - Vercel configuration
2. ✅ `api.py` - Vercel-optimized API entry point (Windows modules disabled)
3. ✅ `.python-version` - Specifies Python 3.12
4. ✅ `requirements-vercel.txt` - Linux-compatible dependencies
5. ✅ `main.py` - Updated to conditionally load Windows modules
6. ✅ `config.py` - Updated to handle Vercel's `/tmp` directory

---

## 📋 Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables** (API Keys):
   ```bash
   vercel env add GROQ_API_KEY
   vercel env add ANTHROPIC_API_KEY
   vercel env add ELEVENLABS_API_KEY
   vercel env add GENNY_API_KEY
   ```

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

### Option 2: Deploy via GitHub Integration

1. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Configure for Vercel deployment"
   git push origin master
   ```

2. **Connect to Vercel**:
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Import your GitHub repository: `fahadmemon1234/AI-ZARA-GF`
   - Vercel will auto-detect the `vercel.json` configuration

3. **Add Environment Variables** in Vercel Dashboard:
   - Go to Project Settings → Environment Variables
   - Add the following:
     ```
     GROQ_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here (optional)
     ELEVENLABS_API_KEY=your_key_here
     GENNY_API_KEY=your_key_here
     ```

4. **Deploy**:
   - Vercel will automatically deploy on every push to `master` branch

---

## 🔑 Required API Keys

At minimum, you need **ONE** of these for AI chat to work:

| API Key | Required? | Purpose | Get Free Key |
|---------|-----------|---------|--------------|
| `GROQ_API_KEY` | ✅ YES (Primary) | AI Chat (FAST + FREE) | https://console.groq.com |
| `ELEVENLABS_API_KEY` | ✅ YES | Voice TTS | https://elevenlabs.io |
| `ANTHROPIC_API_KEY` | ❌ Optional | Backup AI (Claude) | https://console.anthropic.com |
| `GENNY_API_KEY` | ❌ Optional | Premium TTS | https://lovo.ai |
| `GEMINI_API_KEY` | ❌ Optional | Backup AI (Gemini) | https://makersuite.google.com |

---

## 🎯 What Works on Vercel

### ✅ Available Features:
- ✅ AI Chat (Girlfriend mode with Zara's personality)
- ✅ AI Command Processing
- ✅ Text-to-Speech (ElevenLabs + Genny)
- ✅ Memory/Conversation History
- ✅ AI Status Check
- ✅ Health Check
- ✅ Frontend UI (if `public/index.html` exists)

### ❌ Disabled Features (Windows-only):
- ❌ System control (shutdown, restart, etc.)
- ❌ App management (open/close apps)
- ❌ Window management
- ❌ Volume/Brightness control
- ❌ Mouse/Keyboard automation
- ❌ Screenshot tools
- ❌ WhatsApp automation

---

## 🧪 Test Locally Before Deploying

To test the Vercel configuration locally:

```bash
# Install Vercel CLI
npm i -g vercel

# Test build
vercel build

# Test dev server
vercel dev
```

---

## 🔧 Troubleshooting

### Build Fails on Vercel

**Issue**: `ModuleNotFoundError` for Windows packages

**Solution**: The project now uses `api.py` instead of `main.py` for Vercel. Make sure `vercel.json` points to `api.py`.

---

### API Keys Not Working

**Issue**: AI responses fail with "API key not configured"

**Solution**: 
1. Check environment variables are set in Vercel dashboard
2. Redeploy after adding environment variables
3. Verify keys are valid (no extra spaces)

---

### TTS Not Working

**Issue**: Voice generation fails

**Solution**:
1. Ensure `ELEVENLABS_API_KEY` or `GENNY_API_KEY` is set
2. Check API quota hasn't been exceeded
3. Check Vercel function logs for errors

---

### 504 Timeout Error

**Issue**: AI response takes too long

**Solution**: 
- The `maxDuration` is set to 60 seconds in `vercel.json`
- If responses still timeout, consider using Groq (fastest AI option)

---

## 📊 Vercel Function Limits

| Plan | Max Duration | Max Memory | Max Payload |
|------|--------------|------------|-------------|
| **Hobby (Free)** | 10 seconds | 1024 MB | 4.5 MB |
| **Pro** | 60 seconds | 3008 MB | 4.5 MB |

**Note**: Your `vercel.json` sets `maxDuration: 60` which requires Pro plan. For Hobby plan, change it to `10`.

---

## 🎉 Success Checklist

- [ ] `vercel.json` exists and is configured
- [ ] `api.py` exists (Vercel entry point)
- [ ] `.python-version` specifies Python 3.12
- [ ] API keys are set in Vercel environment variables
- [ ] GitHub repository is connected to Vercel
- [ ] Deployment succeeds without errors
- [ ] AI chat endpoint works (`POST /api/chat`)
- [ ] TTS endpoint works (`POST /api/speak`)

---

## 🌐 After Deployment

Your ZARA AI will be available at:
```
https://your-project-name.vercel.app
```

Test endpoints:
- **Home**: `https://your-project.vercel.app/`
- **Health**: `https://your-project.vercel.app/health`
- **Chat**: `POST https://your-project.vercel.app/api/chat`
- **TTS**: `POST https://your-project.vercel.app/api/speak`

---

## 💡 Pro Tips

1. **Use Groq for fastest responses** (FREE and fastest AI)
2. **Monitor Vercel function logs** for debugging
3. **Set up custom domain** in Vercel dashboard
4. **Enable preview deployments** for testing changes
5. **Use Vercel analytics** to track API usage

---

**Need help?** Check Vercel function logs in dashboard: https://vercel.com/dashboard

**Built with 💕 by Muhammad Fahad Memon**
