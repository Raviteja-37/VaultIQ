from app.ingestion.embedder import embed_query
from app.retrieval.vectorstore import query_chunks
from app.rag.prompt import build_prompt
from app.auth.rbac import get_user_namespaces, check_restricted_query
from app.models.database import RoleEnum
from typing import List, Dict, Optional
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

LOW_CONFIDENCE_THRESHOLD = 50.0

def run_rag(
    query: str,
    role: RoleEnum,
    domain: Optional[str] = None,
    chat_history: Optional[List[Dict]] = None
) -> Dict:

    # 1. Check for restricted keywords
    restricted_hits = check_restricted_query(query)
    is_restricted = len(restricted_hits) > 0

    # 2. Get allowed namespaces for this role
    namespaces = get_user_namespaces(role)

    # 3. If restricted + not executive/admin → block
    if is_restricted and role not in [RoleEnum.executive, RoleEnum.admin]:
        return {
            "answer"            : "I'm sorry, this information is confidential and outside your access level.",
            "sources"           : [],
            "confidence"        : 0,
            "is_restricted"     : True,
            "restricted_keywords": restricted_hits,
            "raise_ticket"      : False,
            "low_confidence"    : False,
            "chunks_found"      : 0
        }

    # 4. Embed the query
    query_embedding = embed_query(query)

    # 5. Retrieve relevant chunks from ChromaDB
    chunks = query_chunks(
        query_embedding=query_embedding,
        namespaces=namespaces,
        domain=domain,
        top_k=5
    )

    # 6. Check confidence
    avg_confidence = (
        sum(c["score"] for c in chunks) / len(chunks)
        if chunks else 0
    )
    low_confidence = avg_confidence < LOW_CONFIDENCE_THRESHOLD or len(chunks) == 0

    # 7. Build prompt
    prompt = build_prompt(
        query=query,
        chunks=chunks,
        chat_history=chat_history or [],
        role=role.value
    )

    # 8. Call Groq (llama3 is free and fast)
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

    # 9. Format sources
    sources = [{
        "document" : c["source"],
        "page"     : c["page"],
        "version"  : c["version"],
        "score"    : c["score"],
        "namespace": c["namespace"]
    } for c in chunks]

    return {
        "answer"        : answer,
        "sources"       : sources,
        "confidence"    : round(avg_confidence, 1),
        "is_restricted" : False,
        "low_confidence": low_confidence,
        "raise_ticket"  : low_confidence,
        "chunks_found"  : len(chunks)
    }