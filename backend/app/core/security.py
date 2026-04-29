import bcrypt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status
from app.core.config import settings
from app.schemas.user import TokenData

# Configuración del esquema OAuth2.
# Relación: Esto le dice a FastAPI que busque el token en el header "Authorization".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- 1. PROTOCOLO DE REGIONES (Sentinel) ---
def is_secure_region(region: str) -> bool:
    """
    Motor de Geofencing: Bloquea el acceso basado en la ubicación geográfica.
    Relación: Se usa en el endpoint de login (auth.py) para validar el header 'x-region'.
    """
    if not region:
        return False
    # Verifica si la región está en la lista negra definida en settings.RISK_ZONES
    if region in settings.RISK_ZONES:
        print(f"🚨 BLOQUEO: Intento de acceso desde zona no segura: {region}")
        return False
    return True


# --- 2. NUEVAS FUNCIONES DE HASHING (Criptografía) ---
def get_password_hash(password: str) -> str:
    """
    Transforma una contraseña plana en un hash irreversible.
    Relación: Se usa al crear usuarios o al inicializar la base de datos (seed).
    """
    pwd_bytes = password.encode("utf-8")
    salt = (
        bcrypt.gensalt()
    )  # Añade un valor aleatorio para evitar ataques de diccionario
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña ingresada contra el hash guardado en la DB.
    Relación: Es la pieza clave del proceso de Login.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception as e:
        print(f"❌ Error crítico verificando password: {e}")
        return False


# --- 3. GESTIÓN DE USUARIO ACTUAL (Middleware de Seguridad) ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validador de Identidad: Extrae y verifica el usuario dentro del Token JWT.
    Relación: Es la dependencia que protege los endpoints en 'threats.py'.
    Si el token es inválido o expiró, el acceso es denegado automáticamente (401).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica el token usando la SECRET_KEY que vive en el .env
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception


# --- 4. GENERACIÓN DE TOKEN (Emisión de Credenciales) ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Crea la 'llave digital' (JWT) que el usuario usará para navegar por la app.
    Relación: Se llama al final de un login exitoso.
    """
    to_encode = data.copy()
    # Define cuánto tiempo será válido el acceso antes de expirar
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})

    # Firma el token para asegurar que nadie pueda alterarlo sin la SECRET_KEY
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
