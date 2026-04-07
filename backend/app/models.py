from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class ThreatLog(Base):
    __tablename__ = "threat_logs"  # Nombre de la tabla en Postgres

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    threat_level = Column(String, nullable=False)  # LOW, MEDIUM, CRITICAL
    description = Column(String)
    status = Column(String, default="PENDING")  # PENDING, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)
