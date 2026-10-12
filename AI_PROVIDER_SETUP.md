# AI Provider Configuration & Troubleshooting Guide

## Overview
The system uses multiple AI providers with automatic fallback:
1. **Primary**: Kimi/Moonshot (via OpenAI-compatible API)
2. **Fallback 1**: Groq (fast, free tier available)
3. **Fallback 2**: OpenRouter (200+ models)
4. **Fallback 3**: Ollama (local, completely free)

## Required Environment Variables

### Kimi/Moonshot (Primary) - REQUIRED
```bash
# Your Kimi API key from https://platform.moonshot.cn/
KIMI_API_KEY=sk-xxxxx

# Optional: specify Kimi base URL (defaults to Moonshot API)
KIMI_BASE_URL=https://api.moonshot.cn/v1

# Optional: specify Kimi model (defaults to moonshot-v1)
KIMI_MODEL=moonshot-v1
```

### Groq (Fallback) - OPTIONAL but RECOMMENDED
```bash
# Get your free API key from https://console.groq.com
GROQ_API_KEY=gsk_xxxxx

# Optional: specify model (defaults to llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile
```

### OpenRouter (Fallback) - OPTIONAL
```bash
# Get your API key from https://openrouter.ai
OPENROUTER_API_KEY=sk-or-xxxxx

# Optional: specify model (defaults to openai/gpt-3.5-turbo)
AI_MODEL=openai/gpt-3.5-turbo
```

### Ollama (Local Fallback) - OPTIONAL
```bash
# Set Ollama base URL (defaults to http://localhost:11434)
OLLAMA_BASE_URL=http://localhost:11434

# Optional: specify model (defaults to llama3.1:8b)
OLLAMA_MODEL=llama3.1:8b
```

## Setup Instructions

### 1. Fix the Current Error (API Overload)

The current error shows:
- **Kimi**: 429 (overloaded) → API is under heavy load, needs better retry
- **Groq**: 401 (invalid key) → API key is missing or invalid
- **Ollama**: Connection failed → Ollama isn't running

### Solution:

#### A. Verify Kimi/Moonshot Setup
```bash
# Check if KIMI_API_KEY is set
echo $KIMI_API_KEY

# If not set, add to .env:
KIMI_API_KEY=sk-xxxxx  # Replace with your actual key from https://platform.moonshot.cn/
```

#### B. Add Valid Groq API Key
```bash
# Get a free Groq API key from: https://console.groq.com
# Add to .env:
GROQ_API_KEY=gsk_xxxxx  # Replace with your actual key
```

#### C. Enable Ollama (Optional but Recommended)
```bash
# 1. Install Ollama from https://ollama.ai
# 2. Start Ollama service:
ollama serve

# 3. Pull a model:
ollama pull llama3.1:8b

# 4. Verify it's running:
curl http://localhost:11434/api/tags

# 5. Add to .env (if using non-standard port):
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Testing the Setup

### Test Individual Providers

#### 1. Test Kimi/Moonshot
```bash
curl -X POST https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer $KIMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "moonshot-v1",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.3,
    "max_tokens": 100
  }'
```

#### 2. Test Groq
```bash
curl -X POST https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.3
  }'
```

#### 3. Test Ollama (Local)
```bash
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

### Test from Python
```python
import httpx
import asyncio

async def test_providers():
    # Test Ollama
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags")
            print(f"✅ Ollama: {response.status_code}")
    except Exception as e:
        print(f"❌ Ollama: {e}")
    
    # Test Groq
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "hi"}]}
            )
            print(f"✅ Groq: {response.status_code}")
    except Exception as e:
        print(f"❌ Groq: {e}")

asyncio.run(test_providers())
```

## Troubleshooting

### Error: "Kimi/OpenAI: API error 429"
- **Cause**: API is overloaded
- **Solution**: 
  - Wait a few minutes and retry (exponential backoff is now implemented)
  - Use Groq or OpenRouter as fallback
  - Try again with fewer tokens

### Error: "Groq: Groq API error 401"
- **Cause**: Invalid or missing API key
- **Solution**:
  - Verify GROQ_API_KEY is set correctly
  - Get a new key from https://console.groq.com
  - Ensure key has proper permissions

### Error: "Ollama: All connection attempts failed"
- **Cause**: Ollama isn't running or not accessible
- **Solution**:
  - Install Ollama: `brew install ollama` (Mac) or from https://ollama.ai
  - Start Ollama: `ollama serve`
  - Pull a model: `ollama pull llama3.1:8b`
  - Check it's accessible: `curl http://localhost:11434/api/tags`

### Error: "All AI providers failed"
- **Cause**: All providers are down or misconfigured
- **Solutions**:
  1. Verify at least one API key is set (Kimi or Groq)
  2. Check internet connection
  3. Verify API keys are valid (test with curl)
  4. Check Ollama is running if using as fallback
  5. Check logs: `docker logs super-manager` or check local logs

## Monitoring & Logging

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("adaptive_agent")
logger.setLevel(logging.DEBUG)
```

### Check Provider Health
The system logs provider health on startup:
```
[AdaptiveAgent] Initialized - use_openai: True, use_openrouter: False
[AI_ROUTER] Available providers: ['kimi', 'groq', 'ollama']
```

### Monitor Retry Logic
When rate-limited (429), the system logs:
```
Rate limit hit (attempt 1/3). Retrying in 1s...
Rate limit hit (attempt 2/3). Retrying in 2s...
Rate limit hit (attempt 3/3). Retrying in 4s...
```

## Recommended Setup (Free Tier)

### Option 1: Maximum Reliability (All Free)
1. **Kimi**: Free tier at https://platform.moonshot.cn/ 
2. **Groq**: Free tier at https://console.groq.com
3. **Ollama**: Completely free, local
4. **OpenRouter**: Free tier available

### Option 2: Minimum Setup
1. **Ollama** (only) - Completely free, no API keys needed
   - Install and run locally
   - No internet required
   - Fully private

### Option 3: Production
1. **Kimi** (primary) - paid tier
2. **Groq** (fallback) - paid tier for higher limits
3. **OpenRouter** (fallback) - pay per use
4. **Ollama** (local fallback) - free backup

## Advanced Configuration

### Custom Retry Strategy
Edit `backend/core/adaptive_agent.py`:
```python
# Change max_retries parameter (default is 3):
return await self._call_openai(messages, max_retries=5)
```

### Change Provider Priority
Edit the `_call_llm` method to reorder provider attempts:
```python
# 1. Try Kimi (primary)
# 2. Try Ollama (local)
# 3. Try Groq (fallback)
# 4. Try OpenRouter (final fallback)
```

### Custom Models
Edit `.env`:
```bash
# Use different models for different providers
KIMI_MODEL=moonshot-v1  # or moonshot-v1-32k for long context
GROQ_MODEL=mixtral-8x7b-32768  # Larger model from Groq
OLLAMA_MODEL=mistral  # Faster local model
```

## Performance Tips

1. **Use Ollama for local**: Zero API costs, fastest for simple queries
2. **Use Groq for general**: Very fast, free tier available
3. **Use Kimi for complex**: Best quality responses
4. **Use OpenRouter for variety**: 200+ models to choose from

## API Rate Limits

| Provider | Free Tier | Paid | Notes |
|----------|-----------|------|-------|
| Kimi | Limited | $$$ | Best quality |
| Groq | 14k/day | $$ | Very fast |
| OpenRouter | Pay per use | $ | 200+ models |
| Ollama | Unlimited | Free | Local only |

