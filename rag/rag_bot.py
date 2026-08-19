"""
Lab 3 -- OmniTech policy bot with RAG. VULNERABLE ON PURPOSE.

It retrieves the top matching policy chunks and pastes them straight into the
prompt -- including whatever an attacker planted in a document. Ask it about the
return policy and watch the poisoned document hijack the answer.

  python rag_bot.py
"""
import sys
sys.path.insert(0, "..")
from common.llm import chat, backend_banner
from retriever import build_collection, search

SYSTEM = "You are OmniTech support. Answer using the policy context provided."


def answer(col, question):
    hits = search(col, question, k=3)
    context = "\n\n".join(doc for doc, _src, _d in hits)
    prompt = f"Policy context:\n{context}\n\nCustomer question: {question}"
    sources = ", ".join(src for _d, src, _dist in hits)
    return chat([{"role": "user", "content": prompt}], system=SYSTEM), sources


def main():
    print(backend_banner())
    col = build_collection()
    print("OmniTech Policy Bot (vulnerable). Ctrl+C to quit.\n")
    while True:
        try:
            q = input("customer> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        if not q:
            continue
        reply, sources = answer(col, q)
        print(f"bot> {reply}\n     [retrieved from: {sources}]\n")


if __name__ == "__main__":
    main()
