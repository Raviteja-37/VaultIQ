from typing import List, Dict

def build_prompt(
    query: str,
    chunks: List[Dict],
    chat_history: List[Dict] = None,
    role: str = "ops_staff"
) -> str:

    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source {i+1}: {chunk['source']}, Page {chunk['page']}, "
            f"Version {chunk['version']}, Confidence {chunk['score']}%]\n"
            f"{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    history_text = ""
    if chat_history:
        recent = chat_history[-4:]
        history_parts = []
        for msg in recent:
            speaker = "User" if msg["role"] == "user" else "Assistant"
            history_parts.append(f"{speaker}: {msg['content']}")
        history_text = "\n".join(history_parts)

    prompt = f"""You are VaultIQ, a secure AI knowledge assistant for banking operations.
You are speaking with a user who has the role: {role.upper()}.

STRICT RULES:
1. Answer ONLY using the provided context below. Do not use outside knowledge.
2. Always cite which source document your answer comes from.
3. If the answer is not in the context, say: "I couldn't find this in the available documents. Consider raising a support ticket or consulting an SME."
4. Never guess or hallucinate. If unsure, say so clearly.
5. Keep answers concise, professional, and banking-appropriate.
6. Always mention the document version and page number in your citation.

CONTEXT FROM KNOWLEDGE BASE:
{context}

{"RECENT CONVERSATION:" + chr(10) + history_text if history_text else ""}

USER QUESTION: {query}

ANSWER (cite your sources):"""

    return prompt