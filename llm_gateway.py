"""
llm_gateway.py
The main gateway module — saare examples isko import karke use karenge.

Ye ek thin wrapper hai LiteLLM ke upar jo:
- Unified completion() deta hai (with fallbacks baked in)
- Cost tracking karta hai
- Guardrails apply karta hai (optional)
- Logging karta hai
"""

import time
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

import litellm
litellm.suppress_debug_info = True

from litellm import completion as _litellm_completion
from litellm import completion_cost

from config import DEFAULT_FALLBACK_CHAIN, GROQ_LLAMA_70B


# ============================================================
# 🎯 MAIN COMPLETION FUNCTION
# ============================================================

def completion(
    prompt: str,
    model: str = None,
    fallbacks: list = None,
    caching: bool = False,
    max_tokens: int = 500,
    temperature: float = 0.7,
    user: str = None,
    **kwargs,
):
    """
    Unified completion with automatic fallbacks, cost tracking.

    Args:
        prompt: User's question
        model: Primary model (defaults to GROQ_LLAMA_70B)
        fallbacks: List of fallback model names
        caching: Enable caching?
        max_tokens: Max output tokens
        temperature: 0-1
        user: Tag the call for cost attribution

    Returns:
        dict with keys: response, cost_usd, latency_sec, model_used
    """
    model = model or GROQ_LLAMA_70B
    fallbacks = fallbacks or DEFAULT_FALLBACK_CHAIN

    messages = [{"role": "user", "content": prompt}]

    start = time.time()
    response = _litellm_completion(
        model=model,
        messages=messages,
        fallbacks=fallbacks,
        caching=caching,
        max_tokens=max_tokens,
        temperature=temperature,
        user=user,
        **kwargs,
    )
    latency = time.time() - start

    try:
        cost = completion_cost(completion_response=response)
    except Exception:
        cost = 0.0

    return {
        "response":   response,
        "text":       response.choices[0].message.content,
        "model_used": response.model,
        "cost_usd":   cost,
        "latency_sec": round(latency, 2),
    }


# ============================================================
# 💰 ENABLE CACHING (one-time setup — kisi bhi example se pehle chalao)
# ============================================================

def enable_cache(cache_type: str = "local"):
    """
    Enable LiteLLM caching.
    cache_type: "local" (in-memory) or "redis"
    """
    from litellm.caching import Cache
    litellm.cache = Cache(type=cache_type)
    print(f"✅ Caching enabled: {cache_type}")


# ============================================================
# 📊 REGISTER LOGGING CALLBACK
# ============================================================

_call_logs = []

def _log_success(kwargs, completion_response, start_time, end_time):
    _call_logs.append({
        "model":         kwargs.get("model"),
        "prompt":        kwargs["messages"][-1]["content"][:60],
        "input_tokens":  completion_response.usage.prompt_tokens,
        "output_tokens": completion_response.usage.completion_tokens,
        "latency_sec":   round((end_time - start_time).total_seconds(), 2),
        "user":          kwargs.get("user", "anonymous"),
    })

def enable_logging():
    """Register the logging callback."""
    litellm.success_callback = [_log_success]
    print("✅ Logging enabled. Access logs via get_logs()")

def get_logs():
    """Return all logged calls."""
    return _call_logs


# ============================================================
# 🚀 CONVENIENCE EXPORTS
# ============================================================

from litellm import Router

__all__ = [
    "completion",
    "Router",
    "completion_cost",
    "enable_cache",
    "enable_logging",
    "get_logs",
    "litellm",
]