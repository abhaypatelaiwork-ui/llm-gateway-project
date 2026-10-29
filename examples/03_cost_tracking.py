"""
03_cost_tracking.py
Har call ka exact USD cost — LiteLLM ka pricing database use hota hai.
"""

from config import GROQ_LLAMA_70B
from llm_gateway import completion


def main():
    print("=" * 60)
    print("💰 Cost Tracking Demo")
    print("=" * 60)

    prompts = [
        "Write a haiku about AI.",
        "Explain transformers in 2 lines.",
        "What is 2+2?",
    ]

    total = 0.0
    for i, p in enumerate(prompts, 1):
        r = completion(prompt=p, model=GROQ_LLAMA_70B, max_tokens=100)
        print(f"\n[{i}] {p}")
        print(f"    Response: {r['text'][:100]}")
        print(f"    Tokens:   in={r['response'].usage.prompt_tokens}, "
              f"out={r['response'].usage.completion_tokens}")
        print(f"    Cost:     ${r['cost_usd']:.8f}")
        total += r['cost_usd']

    print(f"\n💵 Total spent on {len(prompts)} calls: ${total:.8f}")


if __name__ == "__main__":
    main()