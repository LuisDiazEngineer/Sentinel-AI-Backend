from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importe del componente de Seguridad
from fastapi.responses import (
    HTMLResponse,
)  # Importa respuesta HTML (aunque en este código no se usa realmente)
import asyncio  # Librería para manejar tareas asíncronas (esperar sin que se bloquee)
from fastapi import FastAPI, Depends, HTTPException, Request, status
from langchain_google_genai import ChatGoogleGenerativeAI

# Componentes principales del framework FastAPI
from .auth import create_access_token, hash_password

# El punto (.) significa "busca en esta misma carpeta"
from fastapi.responses import (
    JSONResponse,
)  # Permite devolver respuestas en formato JSON
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)  # Sesión asíncrona para interactuar con la base de datos
from sqlalchemy.future import (
    select,
)  # Permite hacer consultas tipo SELECT en SQLAlchemy
from sqlalchemy import func  # Funciones SQL como COUNT(), NOW(), etc.
from pydantic import (
    BaseModel,
)  # Sirve para validar datos de entrada (muy importante en APIs)
from typing import Optional  # Permite definir campos opcionales
from .database import (
    engine,
    Base,
    get_db,
    ThreatLog,
    AsyncSessionLocal,
)  # Importa configuración de BD y modelo
import os, datetime, random  # Librerías estándar (archivos, tiempo, aleatorio)
from fastapi.staticfiles import (
    StaticFiles,
)  # Sirve archivos estáticos (CSS, JS, imágenes)
from fastapi.responses import FileResponse  # Permite devolver archivos como respuesta
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Permite conectar frontend (React) con backend

# Librerías de LangChain (IA)
from langchain_core.prompts import PromptTemplate  # Para crear prompts dinámicos
from langchain_community.llms import FakeListLLM  # Modelo de IA simulado (NO real)
from langchain_core.output_parsers import (
    StrOutputParser,
)  # Convierte la salida de IA en texto plano

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI(title="Sentinel-AI Security Hub")
# Crea la aplicación principal de FastAPI con un nombre (se verá en /docs)

# Middleware CORS (permite que el frontend acceda a la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Solo permite requests desde ese origen (React)
    allow_credentials=True,  # Permite cookies/autenticación
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos los headers
)


# Modelo de datos para recibir amenazas
class ThreatCreate(BaseModel):
    ip_address: str  # Campo obligatorio: IP del atacante
    description: Optional[str] = None  # Campo opcional: descripción del ataque


# Evento que se ejecuta cuando inicia el servidor
@app.on_event("startup")
async def startup_event():
    print("⏳ Iniciando Sentinel-AI: Verificando conexión...")  # Mensaje en consola

    for i in range(5):  # Intenta conectarse a la BD hasta 5 veces
        try:
            async with engine.begin() as conn:  # Abre conexión asíncrona
                await conn.run_sync(Base.metadata.create_all)
                # Crea todas las tablas definidas en los modelos si no existen

            print("[DATABASE] Conexión exitosa y tablas sincronizadas.")
            break  # Si funciona, sale del bucle

        except Exception as e:
            print(f"Intento {i+1} fallido.")  # Muestra intento fallido
            print(f"Motivo técnico {e}")  # Muestra error

            if i < 4:
                print(" Reintentando en 2 segundos...")
                await asyncio.sleep(2)  # Espera 2 segundos antes de reintentar


# Middleware que intercepta TODAS las peticiones HTTP
@app.middleware("http")
async def monitor_and_ban_middleware(request: Request, call_next):
    client_ip = request.client.host  # Obtiene la IP del cliente que hace la request

    # Evita bloquear rutas importantes (home, docs)
    if request.url.path not in ["/", "/docs", "/openapi.json"]:
        async with AsyncSessionLocal() as db:  # Abre sesión de BD
            result = await db.execute(
                select(func.count(ThreatLog.id)).where(
                    ThreatLog.ip_address == client_ip
                )
            )
            # Cuenta cuántas veces esa IP aparece en logs

            if result.scalar() >= 5:  # Si tiene 5 o más ataques registrados
                return JSONResponse(
                    status_code=403,  # Código HTTP: acceso prohibido
                    content={"detail": "IP Banned by Sentinel-AI. Access Denied."},
                )

    return await call_next(request)
    # Si no está bloqueada, deja pasar la request al endpoint correspondiente


def get_ai_analysis(ip: str, threat_type: str):
    # Configurar la IA Real de Google
    print(os.getenv("GOOGLE_API_KEY"))
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7,
    )

    # Tu plantilla (Template) que ya tenías
    template = """
    System: You are an AI Security Specialist for Sentinel-AI.
    Context: A potential threat has been detected in the network logs.
    IP Address: {ip}
    Threat Category: {threat_type}
    
    Task: Provide a concise technical recommendation (max 3 bullet points) for a DevOps engineer to mitigate this specific threat.
    """

    prompt = PromptTemplate.from_template(template)

    # El Pipeline (La cadena)
    chain = prompt | llm | StrOutputParser()

    # Ejecución real
    return chain.invoke({"ip": ip, "threat_type": threat_type})


# Endpoint raíz ("/")
@app.get("/", response_class=FileResponse)
async def read_index():
    """
    Sirve el archivo index.html del frontend.
    """
    return FileResponse(os.path.join("frontend", "index.html"))
    # Devuelve el archivo HTML principal


# Monta carpeta de archivos estáticos si existe
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    # Permite acceder a archivos como CSS, JS, imágenes
else:
    print("⚠️ Carpeta 'frontend' no encontrada.")


# Endpoint para analizar amenazas con IA
@app.post("/analyze-threat")
async def analyze(threat: ThreatCreate, token: str = Depends(oauth2_scheme)):
    nivel = threat.description or "General Attack"

    analysis = get_ai_analysis(ip=threat.ip_address, threat_type=nivel)

    return {
        "status": "success",
        "ai_report": analysis,
        "debug_info": f"Analizado bajo nivel: {nivel}",
    }


# Endpoint para crear logs de amenazas
@app.post("/logs/", status_code=201)
async def create_threat_log(threat: ThreatCreate, db: AsyncSession = Depends(get_db)):
    try:

        # Detecta ubicación básica según IP (muy simple)
        detected_location = (
            "San Martin de Porres, PE" if "190.235" in threat.ip_address else "Unknown"
        )

        # Cuenta cuántos ataques tiene esa IP
        result = await db.execute(
            select(func.count(ThreatLog.id)).where(
                ThreatLog.ip_address == threat.ip_address
            )
        )
        attack_count = result.scalar()

        # Define prioridad según número de ataques
        priority = "CRITICAL" if attack_count >= 5 else "LOW"

        # Genera recomendación de IA
        ai_recommendation = get_ai_analysis(
            threat.ip_address, threat.description or "General Attack"
        )

        # Crea objeto del log
        new_log = ThreatLog(
            ip_address=threat.ip_address,
            location=detected_location,
            threat_level=priority,
            status="BLOCKED" if attack_count >= 5 else "OPEN",
            description=threat.description or "No details provided",
            ai_analysis=ai_recommendation,
        )

        db.add(new_log)  # Agrega a la sesión
        await db.commit()  # Guarda en la BD
        await db.refresh(new_log)  # Actualiza datos del objeto

        return {
            "message": "Log analyzed by Sentinel-AI",
            "data": {
                "id": new_log.id,
                "ai_report": ai_recommendation,
            },
        }

    except Exception as e:
        await db.rollback()  # Si falla, revierte cambios
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# Endpoint de ejemplo con ataques fake
@app.get("/ataques")
async def obtener_ataques():
    return [
        {"ip": "192.168.1.10", "accion": "Intento de Brute Force"},
        {"ip": "10.0.0.5", "accion": "Escaneo de Puertos"},
        {"ip": "172.16.0.25", "accion": "Inyección SQL Detenida"},
    ]


# Endpoint para obtener todos los logs
@app.get("/logs/")
async def get_threat_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ThreatLog))  # Consulta todos los registros
    return result.scalars().all()  # Devuelve lista


# Endpoint de estadísticas
@app.get("/stats/")
async def get_threat_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ThreatLog.threat_level, func.count(ThreatLog.id)).group_by(
            ThreatLog.threat_level
        )
    )
    stats = result.all()

    return {
        "status": "Sentinel Active",
        "summary": {level: count for level, count in stats},  # Conteo por nivel
        "total_threats": sum(count for level, count in stats),  # Total general
    }


# Endpoint de salud del sistema
@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_db)):
    try:
        await session.execute(select(func.now()))  # Ejecuta consulta simple a BD

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.datetime.now(),  # Hora actual
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unhealthy: {str(e)}")


load_dotenv()  # Carga las variables del archivo .env

# Ahora usas las variables así:
SECRET_USER = os.getenv("ADMIN_USER")
SECRET_PASS = os.getenv("ADMIN_PASSWORD")
MY_GEMINI_KEY = os.getenv("GEMINI_API_KEY")


# 3. El Portal de Acceso (Aquí es donde entra python-multipart)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == SECRET_USER and form_data.password == SECRET_PASS:
        return {"access_token": "sentinel_secret_token", "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas",
        headers={"WWW-Authenticate": "Bearer"},
    )
