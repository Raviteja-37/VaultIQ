from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print("⏳ Loading embedding model (first time only, ~30 seconds)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded!")
    return _model

def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()

def embed_query(query: str) -> List[float]:
    model = get_model()
    embedding = model.encode([query])
    return embedding[0].tolist()