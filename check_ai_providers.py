#!/usr/bin/env python3
"""
AI Provider Health Check & Setup Verification
Tests all configured AI providers and reports status
"""

import os
import sys
import asyncio
import httpx
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)


class Colors:
    """ANSI color codes"""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_status(name, status, message=""):
    """Print colored status"""
    icon = f"{Colors.GREEN}✅{Colors.RESET}" if status else f"{Colors.RED}❌{Colors.RESET}"
    status_text = f"{Colors.GREEN}OK{Colors.RESET}" if status else f"{Colors.RED}FAIL{Colors.RESET}"
    print(f"  {icon} {name:20} {status_text:10} {message}")


def print_header(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.RESET}")


async def check_environment():
    """Check if required environment variables are set"""
    print_header("1️⃣  ENVIRONMENT CONFIGURATION")
    
    vars_to_check = {
        "KIMI_API_KEY": "Kimi/Moonshot API Key (Primary)",
        "GROQ_API_KEY": "Groq API Key (Fallback)",
        "OPENROUTER_API_KEY": "OpenRouter API Key (Optional)",
        "OLLAMA_BASE_URL": "Ollama Base URL (Optional)",
    }
    
    configured = {}
    for var, description in vars_to_check.items():
        value = os.getenv(var)
        if value:
            # Show first 8 chars + asterisks for keys
            if "KEY" in var or "TOKEN" in var:
                display = f"{value[:8]}{'*' * (len(value) - 8)}"
            else:
                display = value
            print_status(description, True, f"({display})")
            configured[var] = value
        else:
            print_status(description, False, "(not set)")
    
    return configured


async def check_kimi(api_key):
    """Check Kimi/Moonshot API"""
    print_header("2️⃣  KIMI/MOONSHOT (Primary Provider)")
    
    if not api_key:
        print_status("Kimi API Key", False, "(not configured)")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "moonshot-v1",
                    "messages": [{"role": "user", "content": "Respond with 'OK'"}],
                    "temperature": 0.3,
                    "max_tokens": 10,
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("choices"):
                    print_status("Kimi API", True, f"(model: moonshot-v1)")
                    return True
                else:
                    print_status("Kimi API", False, "(no response)")
                    return False
            elif response.status_code == 429:
                print_status("Kimi API", False, "(rate limited 429) - try again later")
                return False
            else:
                error = response.text[:100]
                print_status("Kimi API", False, f"(error {response.status_code})")
                return False
                
    except Exception as e:
        print_status("Kimi API", False, f"({str(e)[:50]})")
        return False


async def check_groq(api_key):
    """Check Groq API"""
    print_header("3️⃣  GROQ (Fallback Provider)")
    
    if not api_key:
        print_status("Groq API Key", False, "(not configured)")
        print(f"  Get a free key: https://console.groq.com")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": "Respond with 'OK'"}],
                    "temperature": 0.3,
                    "max_tokens": 10,
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("choices"):
                    print_status("Groq API", True, f"(model: llama-3.3-70b-versatile)")
                    return True
                else:
                    print_status("Groq API", False, "(no response)")
                    return False
            elif response.status_code == 401:
                print_status("Groq API", False, "(invalid API key 401)")
                return False
            elif response.status_code == 429:
                print_status("Groq API", False, "(rate limited 429)")
                return False
            else:
                print_status("Groq API", False, f"(error {response.status_code})")
                return False
                
    except Exception as e:
        print_status("Groq API", False, f"({str(e)[:50]})")
        return False


async def check_ollama(base_url="http://localhost:11434"):
    """Check Ollama local API"""
    print_header("4️⃣  OLLAMA (Local Provider)")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check if Ollama is running
            response = await client.get(f"{base_url}/api/tags")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                if models:
                    model_names = [m.get("name", "unknown")[:30] for m in models[:3]]
                    models_str = ", ".join(model_names)
                    print_status("Ollama Service", True, f"(running)")
                    print_status("Available Models", True, f"({models_str}...)")
                    
                    # Try to call a model
                    if models:
                        model_name = models[0].get("name")
                        try:
                            chat_response = await client.post(
                                f"{base_url}/api/chat",
                                json={
                                    "model": model_name,
                                    "messages": [{"role": "user", "content": "Hi"}],
                                    "stream": False,
                                },
                                timeout=30.0
                            )
                            if chat_response.status_code == 200:
                                print_status("Chat Test", True, f"(model: {model_name[:20]})")
                                return True
                            else:
                                print_status("Chat Test", False, f"(error {chat_response.status_code})")
                                return False
                        except Exception as e:
                            print_status("Chat Test", False, f"({str(e)[:40]})")
                            return False
                else:
                    print_status("Ollama Service", False, "(no models installed)")
                    print(f"  Install a model: ollama pull llama3.1:8b")
                    return False
            else:
                print_status("Ollama Service", False, f"(error {response.status_code})")
                return False
                
    except Exception as e:
        print_status("Ollama Service", False, f"({str(e)[:40]})")
        print(f"  Is Ollama running? Start with: ollama serve")
        return False


async def check_openrouter(api_key):
    """Check OpenRouter API"""
    print_header("5️⃣  OPENROUTER (Alternative Provider)")
    
    if not api_key:
        print_status("OpenRouter API Key", False, "(not configured - optional)")
        print(f"  Get a key: https://openrouter.ai")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Hi"}],
                    "temperature": 0.3,
                    "max_tokens": 10,
                },
            )
            
            if response.status_code == 200:
                print_status("OpenRouter API", True, f"(model: gpt-3.5-turbo)")
                return True
            else:
                print_status("OpenRouter API", False, f"(error {response.status_code})")
                return False
                
    except Exception as e:
        print_status("OpenRouter API", False, f"({str(e)[:40]})")
        return False


async def main():
    """Run all checks"""
    print(f"\n{Colors.BOLD}🤖 AI Provider Health Check{Colors.RESET}")
    print(f"Checking all configured AI providers...\n")
    
    # Check environment
    configured = await check_environment()
    
    # Check providers
    kimi_ok = False
    groq_ok = False
    ollama_ok = False
    openrouter_ok = False
    
    if configured.get("KIMI_API_KEY"):
        kimi_ok = await check_kimi(configured.get("KIMI_API_KEY"))
    
    if configured.get("GROQ_API_KEY"):
        groq_ok = await check_groq(configured.get("GROQ_API_KEY"))
    
    ollama_url = configured.get("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_ok = await check_ollama(ollama_url)
    
    if configured.get("OPENROUTER_API_KEY"):
        openrouter_ok = await check_openrouter(configured.get("OPENROUTER_API_KEY"))
    
    # Summary
    print_header("📊 SUMMARY")
    
    working = sum([kimi_ok, groq_ok, ollama_ok, openrouter_ok])
    print(f"\n{Colors.BOLD}Providers Working: {working}/4{Colors.RESET}\n")
    
    if working == 0:
        print(f"{Colors.RED}❌ NO PROVIDERS CONFIGURED!{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Next Steps:{Colors.RESET}")
        print("1. Get a Kimi API key: https://platform.moonshot.cn/")
        print("2. Get a Groq API key: https://console.groq.com")
        print("3. Or install Ollama locally: https://ollama.ai")
        print("4. Add to .env file:")
        print("   KIMI_API_KEY=sk-xxxxx")
        print("   GROQ_API_KEY=gsk_xxxxx")
        print("   OLLAMA_BASE_URL=http://localhost:11434")
        sys.exit(1)
    
    elif working >= 2:
        print(f"{Colors.GREEN}✅ SYSTEM READY!{Colors.RESET}")
        print("\nYour Super Manager AI is configured and ready to use.")
        print("The system will use providers in this priority order:")
        if kimi_ok:
            print("  1. Kimi/Moonshot (Primary)")
        if groq_ok:
            print("  2. Groq (Fallback)")
        if openrouter_ok:
            print("  3. OpenRouter (Alternative)")
        if ollama_ok:
            print("  4. Ollama (Local)")
        print("\nAutomatic failover is enabled.")
        sys.exit(0)
    
    else:
        print(f"{Colors.YELLOW}⚠️  SYSTEM PARTIALLY READY{Colors.RESET}")
        print(f"\nOnly {working} provider working. Recommend adding more for reliability.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
