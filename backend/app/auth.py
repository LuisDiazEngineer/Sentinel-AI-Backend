from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


# Configuración de Seguridad
SECRET_KEY = "TU_CLAVE_SECRETA_SUPER_SEGURA"  # En Austin usaríamos variables de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Encripta la contraseña para que ni tú puedas verla en la DB"""
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """Crea el 'pase VIP' (Token) para el usuario"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
