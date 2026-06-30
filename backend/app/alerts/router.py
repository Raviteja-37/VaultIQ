from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database import get_db, SecurityAlert, RoleEnum
from app.auth.rbac import require_roles
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/alerts", tags=["Security Alerts"])

class AlertOut(BaseModel):
    id: str
    triggered_by_email: str
    triggered_by_role: str
    department: Optional[str]
    query: str
    restricted_keywords: str
    manager_notified: bool
    is_reviewed: bool
    timestamp: datetime
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AlertOut])
def get_alerts(
    current_user=Depends(require_roles([RoleEnum.manager, RoleEnum.admin, RoleEnum.executive])),
    db: Session = Depends(get_db)
):
    return db.query(SecurityAlert).order_by(desc(SecurityAlert.timestamp)).limit(100).all()

@router.patch("/{alert_id}/review")
def mark_reviewed(
    alert_id: str,
    current_user=Depends(require_roles([RoleEnum.manager, RoleEnum.admin, RoleEnum.executive])),
    db: Session = Depends(get_db)
):
    alert = db.query(SecurityAlert).filter(SecurityAlert.id == alert_id).first()
    if alert:
        alert.is_reviewed = True
        db.commit()
    return {"status": "reviewed"}