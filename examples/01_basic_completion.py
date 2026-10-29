"""
01_basic_completion.py
Simplest example — one function, one Groq model.
"""

from config import check_keys, GROQ_LLAMA_70B, GROQ_LLAMA_8B
from llm_gateway import completion


def main():
    print("=" * 60)
    print("🔵 Basic Completion — Groq 70B")
    print("=" * 60)

    result = completion(
        prompt="Explain RAG in one sentence.",
        model=GROQ_LLAMA_70B,
    )

    print(f"\n📝 Response: {result['text']}")
    print(f"🤖 Model:    {result['model_used']}")
    print(f"⏱️  Latency: {result['latency_sec']}s")
    print(f"💰 Cost:     ${result['cost_usd']:.8f}")

    print("\n" + "=" * 60)
    print("🟢 Fast Model — Groq 8B")
    print("=" * 60)

    result2 = completion(
        prompt="Explain RAG in one sentence.",
        model=GROQ_LLAMA_8B,
    )
    print(f"\n📝 Response: {result2['text']}")
    print(f"⏱️  Latency: {result2['latency_sec']}s")


if __name__ == "__main__":
    check_keys()
    main()