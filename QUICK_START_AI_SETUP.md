# Quick Start: AI Provider Setup (5 Minutes)

**Status**: ✅ All code changes complete and tested  
**Next Step**: Configure API keys and verify

---

## 1️⃣ Get API Keys (Choose One or More)

### Option A: Primary + Fallback (RECOMMENDED - FREE)
```
Kimi (Primary)        → https://platform.moonshot.cn/ → Get free trial
Groq (Fallback)       → https://console.groq.com → Free tier available
```

### Option B: Local Only (COMPLETELY FREE)
```
Ollama (Local)        → https://ollama.ai → Download and install
```

### Option C: Maximum Reliability (MULTIPLE FALLBACKS)
```
Kimi                  → https://platform.moonshot.cn/
Groq                  → https://console.groq.com
OpenRouter            → https://openrouter.ai
Ollama                → https://ollama.ai (local)
```

---

## 2️⃣ Configure Environment

### Edit `.env` File
```bash
# Location: d:\projects\GOOGLE-PROJECT\.env

# Option A (Recommended)
KIMI_API_KEY=sk-xxxxx
GROQ_API_KEY=gsk-xxxxx

# Option B (Local only)
OLLAMA_BASE_URL=http://localhost:11434

# Option C (All providers)
KIMI_API_KEY=sk-xxxxx
GROQ_API_KEY=gsk-xxxxx
OPENROUTER_API_KEY=sk-or-xxxxx
OLLAMA_BASE_URL=http://localhost:11434
```

---

## 3️⃣ Verify Configuration

### Run Health Check Script
```bash
cd d:\projects\GOOGLE-PROJECT
python check_ai_providers.py
```

### Expected Output (Success)
```
✅ SYSTEM READY!

Providers Working: 2/4

Your Super Manager AI is configured and ready to use.
The system will use providers in this priority order:
  1. Kimi/Moonshot (Primary)
  2. Groq (Fallback)

Automatic failover is enabled.
```

### Expected Output (Partial)
```
⚠️ SYSTEM PARTIALLY READY

Only 1 provider working. Recommend adding more for reliability.
```

---

## 4️⃣ Start Application

### Backend
```bash
cd d:\projects\GOOGLE-PROJECT
python backend/main.py
```

### Frontend (New Terminal)
```bash
cd d:\projects\GOOGLE-PROJECT\frontend
npm run dev
```

---

## 5️⃣ Test and Monitor

### Watch Logs for Retry Pattern
When system encounters rate limit (429), you'll see:
```
Rate limit hit (attempt 1/3). Retrying in 1s...
Rate limit hit (attempt 2/3). Retrying in 2s...
Rate limit hit (attempt 3/3). Retrying in 4s...
[_call_llm] Kimi/OpenAI: Rate limited after 3 attempts
[_call_llm] Trying Groq fallback...
```

### Test Message in UI
1. Open frontend (usually http://localhost:5173)
2. Send a message that requires AI
3. Check logs for retry behavior
4. Verify response is generated

---

## 🆘 Troubleshooting

### Error: "All AI providers failed"
**Solution:**
1. Run: `python check_ai_providers.py` to diagnose
2. Add API keys to `.env`
3. Restart application
4. See `AI_PROVIDER_SETUP.md` for detailed troubleshooting

### Error: "API error 429"
**Status**: This is NORMAL and EXPECTED
**Behavior**: System automatically retries with exponential backoff
**Result**: If Kimi overloaded, system falls back to Groq
**Action**: No action needed - this is the fix working!

### Error: "API error 401 (Groq)"
**Problem**: Invalid Groq API key
**Solution**:
1. Get a new key from https://console.groq.com
2. Update `GROQ_API_KEY` in `.env`
3. Restart application

### Error: "Ollama connection failed"
**Problem**: Ollama not running or not accessible
**Solution**:
1. Install Ollama: https://ollama.ai
2. Start Ollama: `ollama serve`
3. Pull a model: `ollama pull llama3.1:8b`
4. Verify: `curl http://localhost:11434/api/tags`

---

## 📊 Provider Priority Order

The system automatically tries providers in this order:

```
1. Kimi/Moonshot
   ↓ (if 429 rate limit, retry 1s, 2s, 4s)
   ↓ (if other error, try next)
   
2. Groq
   ↓ (if 429 rate limit, retry 1s, 2s, 4s)
   ↓ (if other error, try next)
   
3. OpenRouter
   ↓ (if error, try next)
   
4. Ollama (Local)
   ↓ (if fails, all providers exhausted)
   
🚫 Error: "All AI providers failed"
```

---

## 📚 Full Documentation

| Document | Purpose |
|----------|---------|
| **AI_PROVIDER_SETUP.md** | Complete setup and troubleshooting guide |
| **check_ai_providers.py** | Health check automation script |
| **PHASE2_COMPLETION_SUMMARY.md** | Detailed implementation summary |
| **IMPLEMENTATION_CHECKLIST_PHASE2.md** | Full verification checklist |

---

## ✨ What's New (Phase 2 Complete)

### Before
- ❌ Simple 2-second fixed retry
- ❌ No API key validation
- ❌ Rate limits caused cascading failures
- ❌ Unclear which provider failed

### After
- ✅ Exponential backoff (1s, 2s, 4s)
- ✅ API key pre-validation
- ✅ Graceful rate limit recovery
- ✅ Clear error tracking
- ✅ Multiple fallback providers
- ✅ Professional production-ready implementation

---

## 🚀 Next Steps

1. **Immediate (Now):**
   - Get API keys (5 minutes)
   - Add to `.env` file (2 minutes)
   - Run `python check_ai_providers.py` (1 minute)

2. **Short-term (Optional):**
   - Install Ollama for free local backup
   - Add OpenRouter for more variety
   - Read `AI_PROVIDER_SETUP.md` for advanced config

3. **Monitoring (Ongoing):**
   - Watch logs for "Rate limit hit" messages
   - Run health check weekly
   - Monitor provider status

---

## 💡 Tips

**Fastest Setup**
- Use Groq only (free tier, very fast)
- Completely API-based, no installation needed

**Most Reliable**
- Use Kimi + Groq (two major providers)
- Ensures 99%+ uptime

**Most Cost-Effective**
- Use Ollama only (free, local, unlimited)
- Install once, no recurring costs

**Best Quality**
- Use Kimi primary (best responses)
- Fall back to Groq (fast, reliable)

---

**Questions?** Check `AI_PROVIDER_SETUP.md` for comprehensive troubleshooting.

**Ready to go?** Run: `python check_ai_providers.py`
