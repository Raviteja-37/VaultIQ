from sentence_transformers import CrossEncoder
import math

_model = None

def get_reranker():
    global _model
    if _model is None:
        print("⏳ Loading reranker model...")
        _model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        print("✅ Reranker loaded!")
    return _model

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def rerank(query: str, chunks: list, top_k: int = 5):
    if not chunks:
        return []

    model = get_reranker()
    pairs = [(query, c["text"]) for c in chunks]
    raw_scores = model.predict(pairs)

    for i, raw in enumerate(raw_scores):
        # Convert logit to 0-100 probability using sigmoid
        chunks[i]["rerank_score"] = round(sigmoid(float(raw)) * 100, 2)

    chunks.sort(key=lambda x: x["rerank_score"], reverse=True)
    return chunks[:top_k]