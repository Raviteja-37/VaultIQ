from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.database import get_db, Ticket, TicketStatusEnum, RoleEnum
from app.auth.rbac import get_current_user, require_roles
from app.tickets.engine import raise_ticket
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/tickets", tags=["Tickets"])

class TicketOut(BaseModel):
    id             : str
    ticket_number  : str
    customer_email : str
    original_query : str
    category       : str
    assigned_team  : str
    status         : str
    confidence     : float
    resolution_note: Optional[str]
    created_at     : datetime

    class Config:
        from_attributes = True

class RaiseTicketRequest(BaseModel):
    query        : str
    chat_history : Optional[List[dict]] = []
    confidence   : float

class UpdateTicketRequest(BaseModel):
    status         : Optional[str] = None
    resolution_note: Optional[str] = None

@router.post("/raise", response_model=TicketOut)
def create_ticket(
    request     : RaiseTicketRequest,
    current_user = Depends(get_current_user),
    db: Session  = Depends(get_db)
):
    ticket = raise_ticket(
        db          = db,
        user        = current_user,
        query       = request.query,
        chat_history= request.chat_history,
        confidence  = request.confidence
    )
    return ticket

@router.get("/my", response_model=List[TicketOut])
def get_my_tickets(
    current_user = Depends(get_current_user),
    db: Session  = Depends(get_db)
):
    return db.query(Ticket)\
        .filter(Ticket.customer_id == current_user.user_id)\
        .order_by(desc(Ticket.created_at))\
        .all()

@router.get("/all", response_model=List[TicketOut])
def get_all_tickets(
    current_user = Depends(require_roles([
        RoleEnum.ops_staff, RoleEnum.manager,
        RoleEnum.admin, RoleEnum.executive
    ])),
    db: Session = Depends(get_db)
):
    return db.query(Ticket)\
        .order_by(desc(Ticket.created_at))\
        .limit(200).all()

@router.patch("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id : str,
    request   : UpdateTicketRequest,
    current_user = Depends(require_roles([
        RoleEnum.ops_staff, RoleEnum.manager,
        RoleEnum.admin, RoleEnum.executive
    ])),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if request.status:
        ticket.status = request.status
    if request.resolution_note:
        ticket.resolution_note = request.resolution_note
    db.commit()
    db.refresh(ticket)
    return ticket