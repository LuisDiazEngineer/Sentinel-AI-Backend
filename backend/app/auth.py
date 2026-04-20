import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuración de Logging
logger = logging.getLogger(__name__)

# 1. CONFIGURACIÓN DE SEGURIDAD
# Usamos variables de entorno para nivel profesional (Austin style)
SECRET_KEY = os.getenv("SECRET_KEY", "sentinel_ai_ultra_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. PROTOCOLO DE REGIONES (Filtro de Seguridad)
RISK_ZONES = ["Latam_High_Risk", "Region_X", "Region_Y"]


def is_secure_region(region: Optional[str]) -> bool:
    """
    Verifica si la petición viene de una zona permitida.
    AJUSTE: Si region es None (no enviada), permitimos el paso para pruebas.
    """
    if not region:
        logger.info("ℹ️ Acceso concedido: No se especificó región (Modo Local).")
        return True

    if region in RISK_ZONES:
        logger.error(
            f"🚨 BLOQUEO SENTINEL: Intento de acceso desde zona prohibida: {region}"
        )
        return False

    logger.info(f"✅ Región verificada: {region}")
    return True


# 3. FUNCIONES DE CONTRASEÑA
def hash_password(password: str) -> str:
    """Encripta la contraseña plana."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash de la DB."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"🔥 Error en verificación de hash: {e}")
        return False


# 4. GENERACIÓN DE TOKEN JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera el token de acceso para el usuario."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ Error al generar JWT: {e}")
        raise e
