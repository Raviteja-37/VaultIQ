import fitz  # PyMuPDF
from docx import Document
from pathlib import Path
from typing import List, Dict

def load_pdf(file_path: str) -> List[Dict]:
    doc = fitz.open(file_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "text": text,
                "page": i + 1,
                "source": Path(file_path).name,
                "file_path": file_path
            })
    doc.close()
    return pages

def load_docx(file_path: str) -> List[Dict]:
    doc = Document(file_path)
    full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return [{
        "text": full_text,
        "page": 1,
        "source": Path(file_path).name,
        "file_path": file_path
    }]

def load_txt(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().strip()
    return [{
        "text": text,
        "page": 1,
        "source": Path(file_path).name,
        "file_path": file_path
    }]

def load_document(file_path: str) -> List[Dict]:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")