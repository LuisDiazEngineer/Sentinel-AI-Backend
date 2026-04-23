from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Boolean, Column, Float, Integer, String, DateTime, func, Text
import os

# 1. Configuración de Rutas (Subimos a la raíz para hallar el .env)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Si tu estructura es backend/app/database.py, subimos dos niveles:
root_env_path = os.path.join(BASE_DIR, "..", "..", ".env")
load_dotenv(root_env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Forzamos error si no hay URL, para no usar SQLite por accidente
if not DATABASE_URL:
    raise ValueError("❌ Error: DATABASE_URL no encontrada en el .env. Revisa la ruta.")

print(f"📡 [DATABASE] Conectando a: {DATABASE_URL.split('@')[-1]}")  # Log seguro

engine = create_async_engine(DATABASE_URL, echo=False)

# 2. El nombre que usaremos en el Seed (AsyncSessionLocal)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()


# --- MODELOS ---
class ThreatLog(Base):
    __tablename__ = "threats"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)
    threat_level = Column(String(20), default="HIGH")
    status = Column(String(20), default="BLOCKED")
    description = Column(String(255))
    ai_analysis = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())
    risk_score = Column(Integer, default=0)
    country_code = Column(String(100))
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    isp = Column(String(150))


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="analyst")


# --- FUNCIONES ---
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
