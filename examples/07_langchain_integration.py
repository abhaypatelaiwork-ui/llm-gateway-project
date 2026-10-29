"""
08_langchain_integration.py
LangChain + ChatLiteLLM — plug the gateway into any LangChain chain.
"""

from langchain_litellm import ChatLiteLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import GROQ_LLAMA_70B, GROQ_LLAMA_8B


def main():
    print("=" * 60)
    print("🔗 LangChain + LiteLLM Integration")
    print("=" * 60)

    # Build a chat model routed through LiteLLM → Groq
    llm = ChatLiteLLM(model=GROQ_LLAMA_70B, temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI tutor named KrishGPT. Be concise."),
        ("user", "{question}"),
    ])

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({"question": "What is an LLM Gateway in 3 bullets?"})
    print(f"\n📝 Answer:\n{answer}")

    # ---- Fallback chain in LangChain ----
    print("\n" + "=" * 60)
    print("🛡️  LangChain with fallbacks")
    print("=" * 60)

    primary = ChatLiteLLM(model="groq/fake-model")   # will fail
    fallback1 = ChatLiteLLM(model=GROQ_LLAMA_70B, temperature=0.2)
    fallback2 = ChatLiteLLM(model=GROQ_LLAMA_8B, temperature=0.2)

    robust = primary.with_fallbacks([fallback1, fallback2])
    chain2 = prompt | robust | StrOutputParser()

    result = chain2.invoke({"question": "What are the top 3 benefits of an LLM Gateway?"})
    print(f"\n📝 Response (from fallback):\n{result}")


if __name__ == "__main__":
    main()