from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base


class ThreatLog(Base):
    # ⚠️ IMPORTANTE: Usa el mismo nombre que en database.py
    __tablename__ = "threats"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)
    threat_level = Column(String(20), nullable=False, default="MEDIUM")
    description = Column(String(255))

    # Usamos Text para el análisis de la IA por si Gemini escribe mucho
    ai_analysis = Column(Text, nullable=True)
    status = Column(String(20), default="PENDING")

    # 🆕 CAMPOS SENIOR
    risk_score = Column(Integer, default=0)
    country_code = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    isp = Column(String(150), nullable=True)

    # UTC es el estándar para servidores (Austin usa UTC en sus logs de Google)
    timestamp = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="analyst")
