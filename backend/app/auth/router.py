from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db, User, RoleEnum
from app.models.schemas import UserCreate, UserOut, LoginRequest, TokenResponse
from app.auth.jwt import create_access_token
from app.auth.rbac import get_current_user, require_roles
from passlib.context import CryptContext
import uuid

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

@router.post("/register", response_model=UserOut)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        id              = str(uuid.uuid4()),
        email           = user_data.email,
        full_name       = user_data.full_name,
        hashed_password = hash_password(user_data.password),
        role            = user_data.role,
        department      = user_data.department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token({
        "user_id"   : user.id,
        "email"     : user.email,
        "role"      : user.role.value,
        "department": user.department,
    })

    return TokenResponse(access_token=token, user=user)

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=list[UserOut])
def list_users(
    current_user=Depends(require_roles([RoleEnum.admin, RoleEnum.executive])),
    db: Session = Depends(get_db)
):
    return db.query(User).all()