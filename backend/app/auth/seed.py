from app.models.database import SessionLocal, User, RoleEnum, create_tables
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEMO_USERS = [
    {"email": "customer@demo.com",   "full_name": "Priya Customer",    "password": "demo1234", "role": RoleEnum.customer,   "department": None},
    {"email": "ops@demo.com",        "full_name": "Rahul Ops",         "password": "demo1234", "role": RoleEnum.ops_staff,  "department": "Operations"},
    {"email": "compliance@demo.com", "full_name": "Ananya Compliance",  "password": "demo1234", "role": RoleEnum.compliance, "department": "Compliance"},
    {"email": "manager@demo.com",    "full_name": "Vikram Manager",    "password": "demo1234", "role": RoleEnum.manager,    "department": "Operations"},
    {"email": "admin@demo.com",      "full_name": "Sneha Admin",       "password": "demo1234", "role": RoleEnum.admin,      "department": "IT"},
    {"email": "ceo@demo.com",        "full_name": "Arjun Executive",   "password": "demo1234", "role": RoleEnum.executive,  "department": "Executive"},
]

def seed():
    create_tables()
    db = SessionLocal()
    created = 0
    for u in DEMO_USERS:
        exists = db.query(User).filter(User.email == u["email"]).first()
        if not exists:
            db.add(User(
                id=str(uuid.uuid4()),
                email=u["email"],
                full_name=u["full_name"],
                hashed_password=pwd_context.hash(u["password"]),
                role=u["role"],
                department=u["department"],
            ))
            created += 1
    db.commit()
    db.close()
    print(f"✅ Seeded {created} demo users. All passwords: demo1234")

if __name__ == "__main__":
    seed()