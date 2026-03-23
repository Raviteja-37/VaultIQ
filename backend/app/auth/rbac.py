from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.database import get_db, User, RoleEnum
from app.models.schemas import TokenData
from app.auth.jwt import decode_token
from typing import List

security = HTTPBearer()

# Namespace permissions — which roles can access which document domains
ROLE_NAMESPACES = {
    RoleEnum.customer:   ["public"],
    RoleEnum.ops_staff:  ["public", "sop", "hr"],
    RoleEnum.compliance: ["public", "sop", "hr", "compliance", "regulatory"],
    RoleEnum.manager:    ["public", "sop", "hr", "compliance", "regulatory"],
    RoleEnum.admin:      ["public", "sop", "hr", "compliance", "regulatory", "internal"],
    RoleEnum.executive:  ["public", "sop", "hr", "compliance", "regulatory", "internal", "executive"],
}

# Restricted keywords — if detected in query, triggers security alert
RESTRICTED_KEYWORDS = [
    "shareholder", "equity", "ownership", "board", "acquisition",
    "merger", "salary", "payroll", "confidential", "classified",
    "ceo", "cfo", "executive compensation", "stock option"
]

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> TokenData:
    token = credentials.credentials
    token_data = decode_token(token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return token_data

def require_roles(allowed_roles: List[RoleEnum]):
    def role_checker(current_user: TokenData = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker

def get_user_namespaces(role: RoleEnum) -> List[str]:
    return ROLE_NAMESPACES.get(role, ["public"])

def check_restricted_query(query: str) -> List[str]:
    query_lower = query.lower()
    return [kw for kw in RESTRICTED_KEYWORDS if kw in query_lower]