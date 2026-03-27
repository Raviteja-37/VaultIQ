from app.models.database import SessionLocal, AuditLog, SecurityAlert, Ticket, create_tables

def reset_demo_data():
    create_tables()
    db = SessionLocal()

    # Count before
    logs    = db.query(AuditLog).count()
    alerts  = db.query(SecurityAlert).count()
    tickets = db.query(Ticket).count()
    print(f"Before: {logs} logs, {alerts} alerts, {tickets} tickets")

    # Clear all three tables
    db.query(AuditLog).delete()
    db.query(SecurityAlert).delete()
    db.query(Ticket).delete()
    db.commit()
    db.close()

    print("✅ Cleared: audit logs, security alerts, tickets")
    print("✅ Users and documents untouched")

if __name__ == "__main__":
    reset_demo_data()