from typing import List, Dict

def chunk_pages(
    pages: List[Dict],
    chunk_size: int = 800,
    overlap: int = 150
) -> List[Dict]:
    chunks = []
    chunk_id = 0

    for page in pages:
        text = page["text"]
        words = text.split()

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_text = " ".join(words[start:end])

            if chunk_text.strip():
                chunks.append({
                    "chunk_id"   : f"{page['source']}_chunk_{chunk_id}",
                    "text"       : chunk_text,
                    "source"     : page["source"],
                    "page"       : page["page"],
                    "file_path"  : page["file_path"],
                    "chunk_index": chunk_id
                })
                chunk_id += 1

            start += chunk_size - overlap

    return chunks