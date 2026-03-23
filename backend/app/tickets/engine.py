from sqlalchemy.orm import Session
from app.models.database import Ticket, TicketStatusEnum
from app.models.schemas import TokenData
from datetime import datetime
from typing import List, Dict
import uuid
import json

CATEGORY_KEYWORDS = {
    "loan"      : ["loan", "emi", "restructure", "mortgage", "credit"],
    "kyc"       : ["kyc", "document", "identity", "verification"],
    "account"   : ["account", "balance", "statement", "savings", "current"],
    "payment"   : ["payment", "transfer", "neft", "rtgs", "upi", "nach"],
    "complaint" : ["complaint", "issue", "problem", "wrong", "error"],
}

TEAM_MAP = {
    "loan"      : "Loans & Restructuring Team",
    "kyc"       : "KYC & Compliance Team",
    "account"   : "Account Services Team",
    "payment"   : "Payments Team",
    "complaint" : "Customer Grievance Team",
    "general"   : "General Support Team",
}

def categorize_query(query: str) -> tuple:
    query_lower = query.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            return category, TEAM_MAP[category]
    return "general", TEAM_MAP["general"]

def generate_ticket_number() -> str:
    import random
    return f"TKT-{random.randint(1000, 9999)}"

def raise_ticket(
    db: Session,
    user: TokenData,
    query: str,
    chat_history: List[Dict],
    confidence: float
) -> Ticket:
    category, assigned_team = categorize_query(query)

    ticket = Ticket(
        id              = str(uuid.uuid4()),
        ticket_number   = generate_ticket_number(),
        customer_id     = user.user_id,
        customer_email  = user.email,
        original_query  = query,
        chat_transcript = json.dumps(chat_history or []),
        category        = category,
        assigned_team   = assigned_team,
        status          = TicketStatusEnum.open,
        confidence      = confidence,
        created_at      = datetime.utcnow()
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    print(f"🎫 TICKET RAISED: {ticket.ticket_number}")
    print(f"   Customer : {user.email}")
    print(f"   Query    : '{query}'")
    print(f"   Team     : {assigned_team}")
    print(f"   Confidence was: {confidence}%")

    return ticket