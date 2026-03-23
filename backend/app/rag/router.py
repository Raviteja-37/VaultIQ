from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.rag.chain import run_rag
from app.auth.rbac import get_current_user
from app.models.database import RoleEnum, get_db
from app.audit.logger import log_query
from app.alerts.engine import fire_security_alert

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query       : str
    domain      : Optional[str] = None
    chat_history: Optional[List[Dict]] = []

class ChatResponse(BaseModel):
    answer        : str
    sources       : List[Dict]
    confidence    : float
    is_restricted : bool
    low_confidence: bool
    raise_ticket  : bool
    chunks_found  : int

@router.post("/", response_model=ChatResponse)
def chat(
    request     : ChatRequest,
    current_user = Depends(get_current_user),
    db: Session  = Depends(get_db)
):
    result = run_rag(
        query       = request.query,
        role        = RoleEnum(current_user.role),
        domain      = request.domain,
        chat_history= request.chat_history
    )

    # Fire security alert silently if restricted
    if result.get("is_restricted") and current_user.role not in [
        RoleEnum.executive.value, RoleEnum.admin.value
    ]:
        fire_security_alert(
            db                  = db,
            user                = current_user,
            query               = request.query,
            restricted_keywords = result.get("restricted_keywords", [])
        )

    # Log every query to audit trail
    log_query(
        db     = db,
        user   = current_user,
        query  = request.query,
        result = result,
        domain = request.domain
    )

    return ChatResponse(
        answer        = result["answer"],
        sources       = result["sources"],
        confidence    = result["confidence"],
        is_restricted = result["is_restricted"],
        low_confidence= result.get("low_confidence", False),
        raise_ticket  = result.get("raise_ticket", False),
        chunks_found  = result.get("chunks_found", 0)
    )