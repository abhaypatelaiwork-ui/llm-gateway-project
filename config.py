"""
config.py
Central configuration for the LLM Gateway.
Yahan pe saare model names, aliases, aur routing rules define hain.

Benefits:
- Ek jagah pe sab model names → easily switch kar sakte ho
- Code touch karne ki zaroorat nahi, sirf yahan change karo
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 🔑 API KEYS (env se load hote hain)
# ============================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def check_keys() -> dict:
    """Print which keys are available."""
    status = {
        "Groq":      bool(GROQ_API_KEY),
        "OpenAI":    bool(OPENAI_API_KEY),
        "Anthropic": bool(ANTHROPIC_API_KEY),
        "Gemini":    bool(GEMINI_API_KEY),
    }
    print("🔑 API Key Status:")
    for name, ok in status.items():
        print(f"   {name:<10}: {'✅ loaded' if ok else '❌ missing'}")
    return status


# ============================================================
# 🤖 MODEL NAMES
# ============================================================

# --- Groq models (aapke paas ye hain) ---
GROQ_LLAMA_70B  = "groq/openai/gpt-oss-120b"   # best general purpose
GROQ_LLAMA_8B   = "groq/openai/gpt-oss-20b"      # super fast, cheap
GROQ_MIXTRAL    = "groq/openai/gpt-oss-20b"        # long context
# GROQ_GEMMA      = "groq/gemma2-9b-it"              # small & fast

# --- OpenAI models (optional — agar key hai to) ---
OPENAI_GPT4O      = "gpt-4o"
OPENAI_GPT4O_MINI = "gpt-4o-mini"

# --- Anthropic / Gemini (optional) ---
CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
GEMINI_FLASH  = "gemini/gemini-1.5-flash"


# ============================================================
# 🎯 DEFAULT FALLBACK CHAINS
# Sirf Groq use karke bhi multi-model fallback possible hai
# (different Groq models = different rate limits)
# ============================================================

# For general purpose tasks — try 70B first, then 8B
DEFAULT_FALLBACK_CHAIN = [
    GROQ_LLAMA_70B,
    GROQ_LLAMA_8B,
    GROQ_MIXTRAL,
]

# If you later add OpenAI, replace above with:
# DEFAULT_FALLBACK_CHAIN = [GROQ_LLAMA_70B, OPENAI_GPT4O_MINI, GROQ_LLAMA_8B]


# ============================================================
# 🔀 SMART ROUTER — Task-based model mapping
# App "code"/"summary"/"general" bolega, router model pick karega
# ============================================================

TASK_ROUTING = {
    "code":    [GROQ_LLAMA_70B, GROQ_LLAMA_8B],     # 70B better at code
    "summary": [GROQ_LLAMA_8B, GROQ_LLAMA_70B],     # 8B fast & cheap for summaries
    "general": [GROQ_LLAMA_70B, GROQ_MIXTRAL],      # 70B for general
}


# ============================================================
# 🌐 ROUTER ALIASES (for litellm.Router)
# ============================================================

def get_router_model_list():
    """
    Returns model_list for litellm.Router.
    Alias names ("fast-cheap", "smart-coding") → actual Groq models.
    """
    return [
        {
            "model_name": "fast-cheap",
            "litellm_params": {
                "model": GROQ_LLAMA_8B,
                "api_key": GROQ_API_KEY,
            },
            "model_info": {"id": "groq-llama-8b"},
        },
        {
            "model_name": "smart-coding",
            "litellm_params": {
                "model": GROQ_LLAMA_70B,
                "api_key": GROQ_API_KEY,
            },
            "model_info": {"id": "groq-llama-70b"},
        },
        {
            "model_name": "balanced",
            "litellm_params": {
                "model": GROQ_MIXTRAL,
                "api_key": GROQ_API_KEY,
            },
            "model_info": {"id": "groq-mixtral"},
        },
    ]