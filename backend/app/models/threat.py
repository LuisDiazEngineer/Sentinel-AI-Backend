from sqlalchemy import Column, Float, Integer, String, DateTime, Text
from datetime import datetime
from db.base import Base


class ThreatLog(Base):
    """
    MODELO DE AMENAZAS (ThreatLog)
    Optimizado para evitar errores de persistencia 500.
    """

    __tablename__ = "threats"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(50), nullable=False)
    threat_level = Column(String(50), nullable=False, default="Low")
    description = Column(String(500))  # Un poco más de espacio

    ai_analysis = Column(Text, nullable=True)

    # Aumentamos a 50 para evitar "Value too long"
    status = Column(String(50), default="LOGGED")

    # --- CAMPOS DE ENRIQUECIMIENTO ---
    risk_score = Column(Integer, default=0)
    country_code = Column(String(10), nullable=True)  # PE, US, etc.
    city = Column(String(150), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    isp = Column(String(255), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
