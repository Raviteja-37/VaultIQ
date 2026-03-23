from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from app.models.schemas import TokenData
from app.models.database import RoleEnum
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY    = os.getenv("SECRET_KEY", "fallback_secret_key")
ALGORITHM     = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            user_id   = payload.get("user_id"),
            email     = payload.get("email"),
            role      = payload.get("role"),
            department= payload.get("department")
        )
    except JWTError:
        return None