from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database import get_db, AuditLog, RoleEnum
from app.auth.rbac import require_roles
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/audit", tags=["Audit"])

class AuditLogOut(BaseModel):
    id            : str
    user_email    : str
    user_role     : str
    query         : str
    domain        : Optional[str]
    answer_summary: Optional[str]
    sources_cited : Optional[str]
    confidence    : float
    is_restricted : bool
    low_confidence: bool
    chunks_found  : int
    timestamp     : datetime

    class Config:
        from_attributes = True

@router.get("/logs", response_model=List[AuditLogOut])
def get_audit_logs(
    limit       : int = Query(50, le=200),
    offset      : int = Query(0),
    role_filter : Optional[str] = Query(None),
    current_user = Depends(require_roles([
        RoleEnum.manager, RoleEnum.admin, RoleEnum.executive, RoleEnum.compliance
    ])),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog).order_by(desc(AuditLog.timestamp))
    if role_filter:
        query = query.filter(AuditLog.user_role == role_filter)
    return query.offset(offset).limit(limit).all()

@router.get("/restricted", response_model=List[AuditLogOut])
def get_restricted_queries(
    current_user = Depends(require_roles([
        RoleEnum.manager, RoleEnum.admin, RoleEnum.executive
    ])),
    db: Session = Depends(get_db)
):
    return db.query(AuditLog)\
        .filter(AuditLog.is_restricted == True)\
        .order_by(desc(AuditLog.timestamp))\
        .limit(100).all()

@router.get("/unresolved", response_model=List[AuditLogOut])
def get_unresolved_queries(
    current_user = Depends(require_roles([
        RoleEnum.admin, RoleEnum.manager, RoleEnum.executive
    ])),
    db: Session = Depends(get_db)
):
    return db.query(AuditLog)\
        .filter(AuditLog.low_confidence == True)\
        .order_by(desc(AuditLog.timestamp))\
        .limit(100).all()