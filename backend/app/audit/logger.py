from sqlalchemy.orm import Session
from app.models.database import AuditLog
from app.models.schemas import TokenData
from datetime import datetime
from typing import Dict, List
import uuid
import json

def log_query(
    db: Session,
    user: TokenData,
    query: str,
    result: Dict,
    domain: str = None
):
    sources = result.get("sources", [])
    sources_str = json.dumps([
        f"{s['document']} p.{s['page']} ({s['score']}%)"
        for s in sources
    ])

    answer = result.get("answer", "")
    summary = answer[:300] + "..." if len(answer) > 300 else answer

    log = AuditLog(
        id             = str(uuid.uuid4()),
        user_id        = user.user_id,
        user_email     = user.email,
        user_role      = user.role.value,
        query          = query,
        domain         = domain,
        answer_summary = summary,
        sources_cited  = sources_str,
        confidence     = result.get("confidence", 0.0),
        is_restricted  = result.get("is_restricted", False),
        low_confidence = result.get("low_confidence", False),
        chunks_found   = result.get("chunks_found", 0),
        timestamp      = datetime.utcnow()
    )

    db.add(log)
    db.commit()
    return log