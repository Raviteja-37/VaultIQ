import chromadb
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client


def get_collection(namespace: str):
    client = get_client()

    return client.get_or_create_collection(
        name=f"vaultiq_{namespace}",
        metadata={
            "hnsw:space": "cosine",
            "hnsw:construction_ef": 200,
            "hnsw:M": 32
        },
        embedding_function=None
    )


def add_chunks(chunks: List[Dict], namespace: str, version: str = "v1.0"):
    from app.ingestion.embedder import embed_texts

    collection = get_collection(namespace)

    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]

    metadatas = [{
        "source": c["source"],
        "page": str(c["page"]),
        "namespace": namespace,
        "version": version,
        "chunk_index": str(c["chunk_index"])
    } for c in chunks]

    print(f"Generating embeddings for {len(chunks)} chunks...")
    embeddings = embed_texts(documents)  # ensure normalized inside this function

    batch_size = 100
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i + batch_size],
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size]
        )

    print(f"Added {len(chunks)} chunks to namespace '{namespace}'")


def query_chunks(
    query_embedding: List[float],
    namespaces: List[str],
    domain: str = None,
    top_k: int = 5
) -> List[Dict]:

    results = []

    # retrieve more initially for better ranking
    fetch_k = max(top_k * 4, 20)

    search_namespaces = [domain] if (domain and domain in namespaces) else namespaces

    for namespace in search_namespaces:
        try:
            collection = get_collection(namespace)
            count = collection.count()

            if count == 0:
                continue

            res = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(fetch_k, count),
                include=["documents", "metadatas", "distances"]
            )

            for doc, meta, dist in zip(
                res["documents"][0],
                res["metadatas"][0],
                res["distances"][0]
            ):
                # ✅ FIXED similarity calculation
                similarity = 1 / (1 + dist)

                results.append({
                    "text": doc,
                    "source": meta.get("source", "Unknown"),
                    "page": meta.get("page", "?"),
                    "namespace": namespace,
                    "version": meta.get("version", "v1.0"),
                    "score": round(similarity * 100, 2)
                })

        except Exception as e:
            print(f"Warning: Could not query namespace '{namespace}': {e}")
            continue

    # sort by score
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]


def list_documents(namespace: str) -> List[str]:
    try:
        collection = get_collection(namespace)
        result = collection.get(include=["metadatas"])

        if not result["metadatas"]:
            return []

        return list(set(m["source"] for m in result["metadatas"]))

    except:
        return []