from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# 1. Lo que pides para crear un usuario (Admin/Analista)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)  # La pedimos para hashearla después
    role: str = Field(default="analyst")  # "admin" o "analyst"


# 2. Lo que la API devuelve (Para el Dashboard)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Esto permite que Pydantic lea modelos de SQLAlchemy


# 3. Lo que necesitas para el Token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
