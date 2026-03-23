from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import create_tables
from app.auth.router import router as auth_router
from app.rag.router import router as chat_router
from app.audit.router import router as audit_router
from app.alerts.router import router as alerts_router
from app.tickets.router import router as tickets_router

app = FastAPI(title="VaultIQ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(audit_router)
app.include_router(alerts_router)
app.include_router(tickets_router)

@app.get("/")
def root():
    return {"message": "VaultIQ API is running!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}