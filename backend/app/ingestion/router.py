from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, RoleEnum
from app.auth.rbac import require_roles
from app.ingestion.pipeline import ingest_document
from app.retrieval.vectorstore import list_documents
import shutil, os, uuid

router = APIRouter(prefix="/documents", tags=["Document Management"])

UPLOAD_DIR = "data/documents"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
NAMESPACES = ["public", "sop", "compliance", "hr", "internal", "executive"]

@router.post("/upload")
async def upload_document(
    file     : UploadFile = File(...),
    namespace: str        = Form(...),
    version  : str        = Form("v1.0"),
    current_user = Depends(require_roles([RoleEnum.admin])),
    db: Session  = Depends(get_db)
):
    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{ext}' not supported. Use PDF, DOCX, or TXT."
        )

    # Validate namespace
    if namespace not in NAMESPACES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid namespace. Choose from: {NAMESPACES}"
        )

    # Save file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Ingest into ChromaDB
    try:
        result = ingest_document(file_path, namespace, version)
        return {
            "message"  : "Document uploaded and ingested successfully",
            "file"     : file.filename,
            "namespace": namespace,
            "version"  : version,
            "chunks"   : result["chunks"],
            "pages"    : result["pages"],
            "status"   : "success"
        }
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@router.get("/list")
def list_all_documents(
    current_user = Depends(require_roles([
        RoleEnum.admin, RoleEnum.manager, RoleEnum.executive
    ])),
):
    all_docs = {}
    for ns in NAMESPACES:
        try:
            docs = list_documents(ns)
            if docs:
                all_docs[ns] = docs
        except:
            pass
    return all_docs

@router.delete("/delete")
def delete_document(
    namespace: str,
    filename : str,
    current_user = Depends(require_roles([RoleEnum.admin]))
):
    from app.retrieval.vectorstore import get_collection
    try:
        collection = get_collection(namespace)
        results = collection.get(where={"source": filename})
        if results["ids"]:
            collection.delete(ids=results["ids"])
            return {"message": f"Deleted {len(results['ids'])} chunks of '{filename}' from '{namespace}'"}
        return {"message": "Document not found in vector store"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))