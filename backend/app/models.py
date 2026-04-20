from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base  # Asegúrate del punto si está en la misma carpeta


class ThreatLog(Base):
    __tablename__ = "threat_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    threat_level = Column(String, nullable=False)
    description = Column(String)
    ai_analysis = Column(String)  # ✅ Crítico para el reporte de la IA
    status = Column(String, default="PENDING")

    # Usamos DateTime simple para evitar el error de "timezone offset"
    timestamp = Column(DateTime(timezone=False), default=datetime.utcnow)
