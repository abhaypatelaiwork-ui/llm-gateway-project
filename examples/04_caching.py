"""
04_caching.py
Same question 2 baar — pehli call API, dusri call cache se (fast + free).
"""

from config import GROQ_LLAMA_70B
from llm_gateway import completion, enable_cache


def main():
    print("=" * 60)
    print("⚡ Caching Demo")
    print("=" * 60)

    enable_cache("local")

    prompt = "What does LLM stand for? Answer in one line."

    # First call — hits Groq API
    r1 = completion(prompt=prompt, model=GROQ_LLAMA_70B, caching=True)
    print(f"\n❄️  First call (API):   {r1['latency_sec']}s — {r1['text']}")

    # Second call — from cache
    r2 = completion(prompt=prompt, model=GROQ_LLAMA_70B, caching=True)
    print(f"⚡ Second call (cache): {r2['latency_sec']}s — {r2['text']}")

    speedup = r1['latency_sec'] / max(r2['latency_sec'], 0.001)
    print(f"\n🚀 Speedup: {speedup:.1f}x faster (and ZERO cost on 2nd call!)")


if __name__ == "__main__":
    main()