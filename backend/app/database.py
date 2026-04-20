from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, Text
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:

    DATABASE_URL = "sqlite+aiosqlite:///./sentinel.db"
    print("⚠️ Usando base de datos por defecto (SQLite)")

engine = create_async_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()


class ThreatLog(Base):

    __tablename__ = "threats"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(45), nullable=False)

    threat_level = Column(String(20), default="HIGH")
    location = Column(String(100))
    status = Column(String(20), default="BLOCKED")
    description = Column(String(255))
    ai_analysis = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=func.now())


class User(Base):
    __tablename__ = "users"  # Añade siempre el nombre de la tabla
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)  # Corregido: era 'id', no 'd'
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(
        String(255), nullable=False
    )  # Aquí guardaremos el resultado de get_password_hash()
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="analyst")


async def save_threat(ip: str, loc: str):
    async with AsyncSessionLocal() as session:

        async with session.begin():
            new_threat = ThreatLog(ip_address=ip, location=loc)
            session.add(new_threat)
        await session.commit()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
