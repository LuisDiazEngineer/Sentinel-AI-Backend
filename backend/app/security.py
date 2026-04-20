import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# 1. CONFIGURACIÓN DE SEGURIDAD
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "tu_llave_secreta_super_segura_zl1")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 2. PROTOCOLO DE REGIONES (Sentinel)
# Aquí definimos las zonas que el sistema rechazará automáticamente
RISK_ZONES = ["Latam_High_Risk", "Region_X", "Region_Y"]


def is_secure_region(region: str) -> bool:
    """
    Verifica si la petición viene de una zona permitida.
    Si la región es 'Latam_High_Risk' o similar, el acceso será denegado.
    """
    if not region:
        # Por seguridad, si no hay región definida, podrías marcarlo como inseguro
        # o permitirlo según tu preferencia. Aquí lo bloqueamos si es vacío.
        return False

    if region in RISK_ZONES:
        print(f"🚨 BLOQUEO: Intento de acceso desde zona no segura: {region}")
        return False

    return True


# 3. FUNCIONES DE HASHING Y TOKEN
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
