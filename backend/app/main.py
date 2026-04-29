from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, threats
from app.core.config import settings
from sqlalchemy import text
from db.base import engine, Base  # <--- IMPORTANTE: Importamos Base aquí
import app.models as models  # <--- IMPORTANTE: Importamos tus modelos para que SQLAlchemy los reconozca

# Configuración de Logs
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    GESTOR DE CICLO DE VIDA (Lifespan)
    Actualizado para recrear tablas automáticamente en pgAdmin.
    """

    # --- 1. VERIFICACIÓN Y CREACIÓN DE TABLAS ---
    print("🗄️  [SENTINEL-AI] Verificando estructura en PostgreSQL...")
    try:
        # Esta línea recorre tus modelos y crea las tablas si desaparecieron
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ [DB READY] Estructura de tablas verificada/creada.")

        # Ping de cortesía
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ [DB CONNECTION] Handshake exitoso.")
    except Exception as e:
        print(f"❌ [DB ERROR] No se pudo inicializar la base de datos: {e}")

    # --- 2. VERIFICACIÓN DE IA ---
    print("🧠 [SENTINEL-AI] Verificando conexión con Google Gemini...")
    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        # Nota: Asegúrate de que el modelo sea "gemini-1.5-flash" (el 2.5 aún no es estándar)
        print("✅ [IA READY] Motor Gemini configurado.")
    except Exception as e:
        print(f"⚠️ [IA OFFLINE] Error en el motor de IA: {e}")

    yield

    print("🛑 [SENTINEL-AI] Cerrando servicios de forma segura...")


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(threats.router)


@app.get("/")
async def root():
    return {"status": "online", "project": settings.PROJECT_NAME}
