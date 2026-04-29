from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# 1. Configuración de Rutas y Carga de Entorno
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BACKEND_DIR, ".env")
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Validación de Seguridad
if not DATABASE_URL:
    raise ValueError("❌ Error: DATABASE_URL no encontrada en el archivo .env")

# 3. Creación del Motor Asíncrono
# Relación: Es el túnel de comunicación entre Python y PostgreSQL.
engine = create_async_engine(DATABASE_URL, echo=False)

# 4. Fábrica de Sesiones (AsyncSessionLocal)
# Relación: Genera las sesiones que usa 'get_db' para cada petición a la API.
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# 5. Clase Base para Modelos
# Relación: De aquí deben heredar todos tus modelos (User, ThreatLog) para que SQLAlchemy los reconozca.
Base = declarative_base()

# --- FUNCIONES DE GESTIÓN ---


async def init_db():
    """
    Inicializador de tablas.
    Relación: Lee todos los modelos heredados de 'Base' y crea las tablas en Postgres si no existen.
    """
    async with engine.begin() as conn:
        # Aquí es donde ocurre la 'magia' de creación automática
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Generador de Sesiones (Dependency Injection).
    Relación: Se usa en los endpoints como Depends(get_db) para dar acceso a la base de datos.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Garantiza que la conexión se cierre al terminar la petición para no saturar el servidor.
            await session.close()
