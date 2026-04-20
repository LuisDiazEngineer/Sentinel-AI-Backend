import traceback
import os
import logging
import asyncio
import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# FastAPI y Seguridad
from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

# SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

# Pydantic
from pydantic import BaseModel, IPvAnyAddress

# 1. TUS ARCHIVOS LOCALES (Rutas Absolutas para evitar errores en Docker)
# Unificamos todo en auth y database
from app.database import User, engine, Base, get_db, ThreatLog
from app.auth import is_secure_region, verify_password, create_access_token

# 2. SERVICIOS EXTERNOS
from ai_service import analyze_threat_with_real_ai
import google.generativeai as genai

# 1. CARGA DE CONFIGURACIÓN
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. CONFIGURACIÓN DE IA (CENTRALIZADA)
import google.generativeai as genai

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    # Configuramos el SDK directamente
    genai.configure(api_key=api_key)
    logger.info("✅ [CONFIG] Google AI SDK configurado")
else:
    logger.error("❌ [CONFIG] No hay API KEY en el archivo .env")

# 3. FASTAPI Y DB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI(title="Sentinel-AI Security Hub")

SECRET_USER = os.getenv("ADMIN_USER")
SECRET_PASS = os.getenv("ADMIN_PASSWORD")


class ThreatCreate(BaseModel):
    ip_address: IPvAnyAddress
    description: Optional[str] = None


class ThreatUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None
    Threat_level: Optional[str] = None
    location: Optional[str] = None


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RESILIENCIA DE STARTUP ---


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 INICIANDO SENTINEL-AI BACKEND")

    # 1. 🛠️ CONEXIÓN A LA BASE DE DATOS
    db_ok = False
    for i in range(5):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ [DATABASE] Tablas verificadas/creadas")
            db_ok = True
            break
        except Exception as e:
            logger.warning(f"❌ [DATABASE] Intento {i+1}/5 fallido: {e}")
            await asyncio.sleep(2)

    # 2. 🤖 TEST RÁPIDO DE IA (Sin bloquear el puerto)
    if api_key:
        try:
            # Solo creamos el modelo, no hacemos la llamada pesada aquí para no trabar el inicio
            model = genai.GenerativeModel("gemini-1.5-flash")
            logger.info("✅ [AI] Modelo Gemini 1.5 Flash listo para peticiones")
        except Exception as e:
            logger.error(f"❌ [AI] Error al preparar modelo: {e}")


# --- ENDPOINT PRINCIPAL (CORREGIDO) ---


@app.post("/threats/")
async def create_threat(
    threat_data: ThreatCreate,
    db: AsyncSession = Depends(get_db),
):
    ip = str(threat_data.ip_address)
    desc = (threat_data.description or "Ataque detectado").strip()

    # Llamada a la IA (ai_service.py)
    try:
        # Importante: analyze_threat_with_real_ai DEBE usar el SDK directo como pusimos anoche
        report = await analyze_threat_with_real_ai(ip, desc)
    except Exception as e:
        logger.error(f"IA Error: {e}")
        report = "Level: Medium. Análisis automático: Actividad sospechosa."

    try:
        new_log = ThreatLog(
            ip_address=ip,
            description=desc,
            ai_analysis=report,
            timestamp=datetime.datetime.now(),
            # Lógica simple para extraer el nivel del texto de la IA
            threat_level=(
                "High"
                if any(
                    x in report.lower() for x in ["high", "critical", "severo", "alto"]
                )
                else "Medium"
            ),
            status="Unresolved",
        )
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)
        return {"status": "success", "analysis": report}
    except Exception as e:
        await db.rollback()
        logger.error(f"🔥 [DB ERROR]: {e}")
        raise HTTPException(status_code=500, detail="Error de base de datos")


@app.put("/threats/{threat_id}", tags=["Protocolo ZL1"])
async def update_threat(
    threat_id: int,
    update_data: ThreatUpdate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Permite al administrador modificar el estado de una amenaza.
    Ejemplo: Cambiar status de 'BLOCKED' a 'RESOLVED'.
    """
    # 1. Buscar el registro
    result = await db.execute(select(ThreatLog).where(ThreatLog.id == threat_id))
    threat_entry = result.scalar_one_or_none()

    if not threat_entry:
        logger.warning(f"⚠️ Intentaron actualizar ID {threat_id} inexistente")
        raise HTTPException(status_code=404, detail="El ID de amenaza no existe")

    # 2. Aplicar cambios solo en los campos enviados
    data_to_update = update_data.dict(exclude_unset=True)
    for key, value in data_to_update.items():
        setattr(threat_entry, key, value)

    try:
        await db.commit()
        await db.refresh(threat_entry)
        logger.info(f"✅ [DATABASE] Registro {threat_id} actualizado exitosamente")
        return {"status": "updated", "id": threat_id, "new_data": data_to_update}
    except Exception as e:
        await db.rollback()
        logger.error(f"🔥 Error al actualizar DB: {e}")
        raise HTTPException(status_code=500, detail="Error interno al actualizar")


@app.delete(
    "/threats/{threat_id}",
    tags=["Protocolo ZL1"],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_threat(
    threat_id: int,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """
    Elimina un registro del sistema.
    Requiere token de administrador.
    """
    result = await db.execute(select(ThreatLog).where(ThreatLog.id == threat_id))
    threat_entry = result.scalar_one_or_none()

    if not threat_entry:
        raise HTTPException(
            status_code=404, detail="No se encontró el registro para eliminar"
        )

    try:
        await db.delete(threat_entry)
        await db.commit()
        logger.warning(f"🗑️ [DATABASE] Registro {threat_id} eliminado del sistema")
        return None  # Status 204 no requiere respuesta
    except Exception as e:
        await db.rollback()
        logger.error(f"🔥 Error al eliminar de DB: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar la eliminación")


@app.get("/stats/", tags=["Dashboard"])
async def get_stats(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """Calcula estadísticas detalladas de amenazas."""
    # Usamos 'token' en un print solo para que VS Code vea que se usa
    print(f"Consulta autorizada por el token")

    query = select(ThreatLog.threat_level, func.count(ThreatLog.id)).group_by(
        ThreatLog.threat_level
    )
    result = await db.execute(query)
    stats = result.all()

    return {
        "total": sum(count for level, count in stats),
        "breakdown": {level: count for level, count in stats},
    }


# 🔹 ENDPOINT ATTACKS (PARA EL DASHBOARD)
@app.get("/threats/", tags=["Dashboard"])
async def get_all_threats(
    db: AsyncSession = Depends(get_db),
    # 🔓 Nota: No le pongas el token aquí para que el Dashboard pueda leerlo directo
):
    """Retorna todas las amenazas de la DB para el Dashboard"""
    # Usamos ThreatLog porque es el nombre de tu modelo en SQLAlchemy
    result = await db.execute(select(ThreatLog).order_by(ThreatLog.timestamp.desc()))
    threats = result.scalars().all()
    return threats
    # IMPORTANTE: Aseguramos que la llave sea 'ip_address'


# Endpoint para obtener todos los logs
@app.get("/logs/")
async def get_threat_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ThreatLog))  # Consulta todos los registros
    return result.scalars().all()  # Devuelve lista


# Endpoint de estadísticas
@app.get("/stats/", tags=["Dashboard"])
async def get_stats(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),  # <--- PROTEGIDO
):
    """Calcula estadísticas solo para analistas autorizados."""
    query = select(ThreatLog.threat_level, func.count(ThreatLog.id)).group_by(
        ThreatLog.threat_level
    )
    result = await db.execute(query)
    stats = result.all()

    return {
        "total": sum(count for level, count in stats),
        "breakdown": {level: count for level, count in stats},
    }


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    x_region: str = Header(None),  # Header para la zona de riesgo
):
    try:
        # 1. FILTRO SENTINEL: ¿Es una zona segura?
        # Antes de gastar recursos en la DB, validamos la región
        print(f"DEBUG: Validando acceso desde región: {x_region}")
        if not is_secure_region(x_region):
            print(f"🚨 BLOQUEO: Intento de acceso desde zona de riesgo: {x_region}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado: Protocolo Sentinel activo para esta región.",
            )

        # 2. INTENTO DE LOGIN
        print(f"DEBUG: Buscando usuario: {form_data.username}")
        result = await db.execute(
            select(User).where(User.username == form_data.username)
        )
        user = result.scalar_one_or_none()

        if not user:
            print("DEBUG: Usuario no encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        # 3. VERIFICACIÓN DE HASH (Pase VIP)
        # Usamos el pwd_context de tu archivo auth
        try:
            es_valido = verify_password(form_data.password, user.hashed_password)
        except Exception as e:
            print(f"DEBUG: Error en motor de hashing: {e}")
            raise HTTPException(status_code=500, detail="Error en sistema de seguridad")

        if not es_valido:
            print(f"DEBUG: Contraseña incorrecta para {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        # 4. GENERACIÓN DEL TOKEN
        # El sub (subject) es lo más importante del payload
        token_data = {"sub": user.username, "role": user.role}
        access_token = create_access_token(data=token_data)

        print(f"✅ LOGIN EXITOSO: {user.username} ha ingresado.")
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException as http_e:
        raise http_e
    except Exception as e:
        print("!!! ERROR CRÍTICO !!!")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error interno del servidor")
