from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Enum, Float, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vaultiq.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class RoleEnum(str, enum.Enum):
    customer   = "customer"
    ops_staff  = "ops_staff"
    compliance = "compliance"
    manager    = "manager"
    admin      = "admin"
    executive  = "executive"

class TicketStatusEnum(str, enum.Enum):
    open       = "open"
    inprogress = "inprogress"
    resolved   = "resolved"
    closed     = "closed"

class User(Base):
    __tablename__ = "users"
    id              = Column(String, primary_key=True)
    email           = Column(String, unique=True, nullable=False, index=True)
    full_name       = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role            = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.customer)
    department      = Column(String, nullable=True)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id              = Column(String, primary_key=True)
    user_id         = Column(String, nullable=False, index=True)
    user_email      = Column(String, nullable=False)
    user_role       = Column(String, nullable=False)
    query           = Column(Text, nullable=False)
    domain          = Column(String, nullable=True)
    answer_summary  = Column(Text, nullable=True)
    sources_cited   = Column(Text, nullable=True)   # JSON string
    confidence      = Column(Float, default=0.0)
    is_restricted   = Column(Boolean, default=False)
    low_confidence  = Column(Boolean, default=False)
    chunks_found    = Column(Integer, default=0)
    timestamp       = Column(DateTime, default=datetime.utcnow, index=True)

class SecurityAlert(Base):
    __tablename__ = "security_alerts"
    id                  = Column(String, primary_key=True)
    triggered_by_id     = Column(String, nullable=False)
    triggered_by_email  = Column(String, nullable=False)
    triggered_by_role   = Column(String, nullable=False)
    department          = Column(String, nullable=True)
    query               = Column(Text, nullable=False)
    restricted_keywords = Column(String, nullable=False)
    manager_notified    = Column(Boolean, default=False)
    is_reviewed         = Column(Boolean, default=False)
    timestamp           = Column(DateTime, default=datetime.utcnow, index=True)

class Ticket(Base):
    __tablename__ = "tickets"
    id              = Column(String, primary_key=True)
    ticket_number   = Column(String, unique=True, nullable=False)
    customer_id     = Column(String, nullable=False)
    customer_email  = Column(String, nullable=False)
    original_query  = Column(Text, nullable=False)
    chat_transcript = Column(Text, nullable=True)   # JSON string
    category        = Column(String, default="general")
    assigned_team   = Column(String, default="support")
    status          = Column(Enum(TicketStatusEnum), default=TicketStatusEnum.open)
    confidence      = Column(Float, default=0.0)
    resolution_note = Column(Text, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)