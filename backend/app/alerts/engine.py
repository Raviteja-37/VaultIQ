from sqlalchemy.orm import Session
from app.models.database import SecurityAlert, User, RoleEnum
from app.models.schemas import TokenData
from datetime import datetime
import uuid

def fire_security_alert(
    db: Session,
    user: TokenData,
    query: str,
    restricted_keywords: list
):
    alert = SecurityAlert(
        id                  = str(uuid.uuid4()),
        triggered_by_id     = user.user_id,
        triggered_by_email  = user.email,
        triggered_by_role   = user.role.value,
        department          = user.department,
        query               = query,
        restricted_keywords = ", ".join(restricted_keywords),
        manager_notified    = True,
        timestamp           = datetime.utcnow()
    )
    db.add(alert)
    db.commit()

    print(f"🚨 SECURITY ALERT: {user.email} [{user.role}] tried to access restricted info")
    print(f"   Query: '{query}'")
    print(f"   Keywords: {restricted_keywords}")
    print(f"   Dept: {user.department}")

    return alert