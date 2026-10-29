"""
02_fallbacks.py
Automatic fallbacks — agar ek model fail ho jaye, next try karo.
Groq ke andar bhi multiple models hain, so fallback useful hai.
"""

from config import GROQ_LLAMA_70B, GROQ_LLAMA_8B, GROQ_MIXTRAL
from llm_gateway import completion, _litellm_completion


def main():
    print("=" * 60)
    print("🛡️  Test 1: Real primary (70B) with fallbacks")
    print("=" * 60)

    result = completion(
        prompt="What is an LLM Gateway?",
        model=GROQ_LLAMA_70B,
        fallbacks=[GROQ_LLAMA_8B, GROQ_MIXTRAL],
    )
    print(f"📝 Response:     {result['text'][:150]}...")
    print(f"🤖 Actual model: {result['model_used']}")

    print("\n" + "=" * 60)
    print("🛡️  Test 2: Fake primary (will fail) → fallback saves it")
    print("=" * 60)

    fake_result = completion(
        prompt="What is an LLM Gateway?",
        model="groq/fake-nonexistent-model-9999",
        fallbacks=[GROQ_LLAMA_70B, GROQ_LLAMA_8B],
    )
    print(f"✅ App still got a response!")
    print(f"📝 Response:     {fake_result['text'][:150]}...")
    print(f"🤖 Actual model: {fake_result['model_used']}  (fallback rescued! 🎉)")


if __name__ == "__main__":
    main()


    