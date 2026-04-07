from dotenv import load_dotenv

# Importa función para cargar variables de entorno desde archivo .env

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# create_async_engine → crea conexión async a la BD
# AsyncSession → sesiones async para consultas

from sqlalchemy.orm import declarative_base, sessionmaker

# declarative_base → base para definir modelos (tablas)
# sessionmaker → crea sesiones de BD

from sqlalchemy import Column, Integer, String, DateTime, func, Text

# Tipos de columnas y funciones SQL

import datetime  # Manejo de fechas (aunque aquí casi no se usa directamente)
import os  # Manejo de rutas y variables del sistema

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Obtiene la ruta absoluta del archivo actual (carpeta donde está este script)

dotenv_path = os.path.join(BASE_DIR, ".env")
# Construye la ruta completa al archivo .env

load_dotenv(dotenv_path)
# Carga las variables del archivo .env al entorno


DATABASE_URL = os.getenv("DATABASE_URL")
# Obtiene la URL de la base de datos desde variable de entorno


if not DATABASE_URL:
    # Si NO existe DATABASE_URL en el entorno

    DATABASE_URL = "sqlite+aiosqlite:///./sentinel.db"
    # Usa SQLite como base de datos por defecto

    print("⚠️ Usando base de datos por defecto (SQLite)")
    # Mensaje de advertencia


engine = create_async_engine(DATABASE_URL, echo=True)
# Crea el motor de conexión async a la BD
# echo=True → imprime las consultas SQL en consola (debug)


AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
# Crea una fábrica de sesiones:
# bind=engine → usa ese motor
# class_=AsyncSession → sesiones async
# expire_on_commit=False → evita que los datos se borren tras commit


Base = declarative_base()
# Base para definir modelos (tablas de la BD)


class ThreatLog(Base):
    # Define el modelo (tabla en la BD)

    __tablename__ = "threats"
    # Nombre de la tabla en la BD

    __table_args__ = {"extend_existing": True}
    # Permite modificar tabla si ya existe (evita errores)

    id = Column(Integer, primary_key=True, index=True)
    # ID único, clave primaria

    ip_address = Column(String(45), nullable=False)
    # IP del atacante (máx 45 chars), obligatorio

    threat_level = Column(String(20), default="HIGH")
    # Nivel de amenaza (por defecto HIGH)

    location = Column(String(100))
    # Ubicación del atacante

    status = Column(String(20), default="BLOCKED")
    # Estado (bloqueado, activo, etc.)

    description = Column(String(255))
    # Descripción del ataque

    ai_analysis = Column(Text, nullable=True)
    # Resultado del análisis de IA (puede ser nulo)

    timestamp = Column(DateTime, default=func.now())
    # Fecha/hora automática al crear registro


async def save_threat(ip: str, loc: str):
    # Función async para guardar una amenaza en la BD

    async with AsyncSessionLocal() as session:
        # Abre una sesión de BD

        async with session.begin():
            # Inicia transacción

            new_threat = ThreatLog(ip_address=ip, location=loc)
            # Crea objeto con datos

            session.add(new_threat)
            # Agrega a la sesión (pendiente de guardar)

        await session.commit()
        # Guarda cambios en la BD


async def init_db():
    # Función para inicializar la base de datos

    async with engine.begin() as conn:
        # Abre conexión

        await conn.run_sync(Base.metadata.create_all)
        # Crea tablas si no existen


async def get_db():
    # Función generadora para obtener sesión de BD (usada en FastAPI)

    async with AsyncSessionLocal() as session:
        # Abre sesión

        yield session
        # Devuelve la sesión al endpoint (dependency injection)
