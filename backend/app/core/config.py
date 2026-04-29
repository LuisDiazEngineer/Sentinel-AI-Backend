from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import List

# 1. Definición de la ruta base del proyecto
# Relación: Permite que el sistema sepa dónde está parado para buscar archivos como el .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    CLASE DE CONFIGURACIÓN GLOBAL (Pydantic)
    Relación: Lee automáticamente el archivo '.env' y valida que existan todas las variables.
    Si falta una variable crítica en el .env, el sistema ni siquiera arrancará (Seguridad Fail-Safe).
    """

    # --- Credenciales de Administrador ---
    ADMIN_USER: str
    ADMIN_PASSWORD: str

    # --- Conexiones y Llaves Secretas ---
    # DATABASE_URL: La ruta de conexión a PostgreSQL.
    # SECRET_KEY: La llave maestra para firmar los Tokens JWT de seguridad.
    DATABASE_URL: str
    SECRET_KEY: str

    # --- Metadatos del Proyecto ---
    PROJECT_NAME: str = "Sentinel AI"
    VERSION: str = "1.0.0"

    # --- Configuración de Tokens ---
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Inteligencia Artificial ---
    # Relación: Esta es la llave que usa 'ai_service.py' para hablar con Gemini.
    GOOGLE_API_KEY: str

    # Configuración de Pydantic para vincular el archivo físico .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Protocolo Sentinel (Zonas de Riesgo) ---
    # Relación: 'security.py' usa esta lista para el bloqueo geográfico (Geofencing).
    # Las definimos aquí para que el equipo de ciberseguridad pueda actualizarlas fácilmente.
    RISK_ZONES: List[str] = ["Russia", "China", "North Korea"]


# Instancia única de configuración (Singleton)
# Relación: Todos los demás archivos importan esta variable 'settings' para usar los datos.
settings = Settings()
