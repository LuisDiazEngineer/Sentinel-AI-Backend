from pydantic import BaseModel, Field
from typing import Optional


class ThreatCreate(BaseModel):
    """
    ESQUEMA DE CREACIÓN (Data Ingestion)
    Relación: Define qué datos debe enviar el simulador o el analista al crear una amenaza.
    """

    ip_address: str
    description: Optional[str] = None

    # ge=0 (Greater than or equal), le=100 (Less than or equal)
    # Relación: Valida que el score esté siempre en el rango permitido (0-100).
    risk_score: Optional[int] = Field(default=0, ge=0, le=100)

    country_code: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    isp: Optional[str] = None


class ThreatUpdate(BaseModel):
    """
    ESQUEMA DE ACTUALIZACIÓN (Patching)
    Relación: Se usa cuando un analista quiere cambiar el estado o nivel de una amenaza
    que ya existe en la base de datos. Todos los campos son opcionales.
    """

    status: Optional[str] = None
    description: Optional[str] = None
    threat_level: Optional[str] = None
    risk_score: Optional[int] = 0
    country_code: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    isp: Optional[str] = None


class Config:
    """
    CONFIGURACIÓN DE ATRIBUTOS
    Relación: Permite que Pydantic lea los datos directamente desde los objetos
    de SQLAlchemy (ORMs), facilitando la conversión de DB a JSON.
    """

    from_attributes = True
