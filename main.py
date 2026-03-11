from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, ThreatLog, create_tables

# Initialize database tables on startup
create_tables()

app = FastAPI()


# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/analyze-threat/")
def analyze_and_save(ip: str, level: str, desc: str, db: Session = Depends(get_db)):
    # 1. Create a new log instance using the ThreatLog model
    new_log = ThreatLog(ip_address=ip, threat_level=level, description=desc)

    # 2. Persist the record in the database (SQLAlchemy handles the INSERT statement)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return {
        "status": "Saved",
        "id": new_log.id,
        "message": "Threat recorded in Sentinel DB",
    }
