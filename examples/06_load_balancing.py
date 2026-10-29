"""
05_smart_routing.py
Router with aliases — "fast-cheap" / "smart-coding" / "balanced".
App abstract naam bolegi, router actual Groq model pick karega.
"""

from config import get_router_model_list
from llm_gateway import Router


def main():
    print("=" * 60)
    print("🔀 Smart Routing Demo")
    print("=" * 60)

    router = Router(model_list=get_router_model_list())

    # Fast & cheap
    r1 = router.completion(
        model="fast-cheap",
        messages=[{"role": "user", "content": "Summarize: AI is changing software."}],
    )
    print(f"\n⚡ fast-cheap   ({r1._hidden_params.get('model_id', '?')}):")
    print(f"   {r1.choices[0].message.content[:150]}")

    # Smart coding
    r2 = router.completion(
        model="smart-coding",
        messages=[{"role": "user", "content": "Write a Python function to reverse a string."}],
    )
    print(f"\n🧠 smart-coding ({r2._hidden_params.get('model_id', '?')}):")
    print(f"   {r2.choices[0].message.content[:300]}")

    # Balanced
    r3 = router.completion(
        model="balanced",
        messages=[{"role": "user", "content": "Explain quantum computing in 2 lines."}],
    )
    print(f"\n⚖️  balanced     ({r3._hidden_params.get('model_id', '?')}):")
    print(f"   {r3.choices[0].message.content[:200]}")


if __name__ == "__main__":
    main()