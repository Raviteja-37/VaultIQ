from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_pages
from app.retrieval.vectorstore import add_chunks
from typing import Optional
import os

def ingest_document(
    file_path: str,
    namespace: str,
    version: str = "v1.0"
) -> dict:
    print(f"\n📄 Ingesting: {os.path.basename(file_path)}")
    print(f"   Namespace : {namespace}")
    print(f"   Version   : {version}")

    # Step 1: Load
    pages = load_document(file_path)
    print(f"   Pages loaded: {len(pages)}")

    # Step 2: Chunk
    chunks = chunk_pages(pages)
    print(f"   Chunks created: {len(chunks)}")

    # Step 3: Store in ChromaDB (uses text directly — ChromaDB embeds internally)
    add_chunks(chunks, namespace, version)

    return {
        "file"      : os.path.basename(file_path),
        "namespace" : namespace,
        "pages"     : len(pages),
        "chunks"    : len(chunks),
        "version"   : version,
        "status"    : "success"
    }

def ingest_folder(folder_path: str, namespace: str, version: str = "v1.0") -> list:
    results = []
    supported = {".pdf", ".docx", ".txt"}

    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        if ext in supported:
            file_path = os.path.join(folder_path, filename)
            try:
                result = ingest_document(file_path, namespace, version)
                results.append(result)
            except Exception as e:
                results.append({
                    "file"  : filename,
                    "status": "failed",
                    "error" : str(e)
                })

    return results