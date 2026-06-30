from app.ingestion.embedder import embed_query
from app.retrieval.vectorstore import query_chunks
from app.retrieval.reranker import rerank
from app.rag.prompt import build_prompt
from app.auth.rbac import get_user_namespaces, check_restricted_query
from app.models.database import RoleEnum
from typing import List, Dict, Optional
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LOW_CONFIDENCE_THRESHOLD = 55.0


def run_rag(
    query: str,
    role: RoleEnum,
    domain: Optional[str] = None,
    chat_history: Optional[List[Dict]] = None
) -> Dict:

    # 1. Check restriction
    restricted_hits = check_restricted_query(query)
    is_restricted = len(restricted_hits) > 0

    # 2. Namespaces
    namespaces = get_user_namespaces(role)

    # 3. 🚨 ALERT (separate)
    raise_alert = (
        is_restricted and 
        role not in [RoleEnum.executive, RoleEnum.admin]
    )

    if raise_alert:
        print(f"🚨 ALERT: Restricted access attempt | Role: {role} | Query: {query}")

    # 4. Block response if restricted
    blocked = raise_alert

    # 5. Embed
    query_embedding = embed_query(query)

    # 6. Retrieve + rerank
    chunks = query_chunks(
        query_embedding=query_embedding,
        namespaces=namespaces,
        domain=domain,
        top_k=20
    )

    chunks = rerank(query, chunks, top_k=5)

    scored_chunks = [c for c in chunks if c.get("rerank_score", 0) > 1.0]


    # 7. Confidence — use rerank_score directly (already 0-100)
    if scored_chunks:
        avg_confidence = round(
            sum(c.get("rerank_score", 0) for c in scored_chunks) / len(scored_chunks), 1
        )
    elif chunks:
        avg_confidence = round(chunks[0].get("rerank_score", 0), 1)
    else:
        avg_confidence = 0

    LOW_CONFIDENCE_THRESHOLD = 40.0  # sigmoid-normalized scores work at this threshold
    low_confidence = avg_confidence < LOW_CONFIDENCE_THRESHOLD

    # 🎫 Ticket ONLY for low confidence
    raise_ticket = low_confidence and not blocked

    # 8. LLM (only if not blocked)
    if not blocked:
        prompt = build_prompt(
            query=query,
            chunks=chunks,
            chat_history=chat_history or [],
            role=role.value
        )

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.1
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"LLM error: {str(e)}"
    else:
        answer = "I'm sorry, this information is confidential and outside your access level."

    # 9. Low confidence message
    if low_confidence and not blocked:
        answer = (
            "I'm not fully confident about this answer based on the available data. "
            "Please verify or raise a support request.\n\n"
            + answer
        )

    # 10. Sources
    sources = [{
        "document": c["source"],
        "page": c["page"],
        "version": c["version"],
        "score": round(c.get("rerank_score", c["score"]), 2),
        "namespace": c["namespace"]
    } for c in chunks] if not blocked else []

    

    return {
    "answer": answer,
    "sources": sources,
    "confidence": round(avg_confidence, 1) if not blocked else 0,
    "is_restricted": is_restricted,
    "low_confidence": low_confidence if not blocked else False,
    "raise_alert": raise_alert,
    "raise_ticket": raise_ticket,
    "restricted_keywords": restricted_hits,  # ← add this line
    "chunks_found": len(chunks) if not blocked else 0
}


