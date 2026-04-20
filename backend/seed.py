import requests
import time
import random
import os
import logging
from dotenv import load_dotenv

# 1. Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# 2. Carga de configuración desde tu nuevo .env
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USER", "ldiaz")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Machumay2026$")

# OJO AQUÍ: Aunque en el .env de la DB diga 'db',
# el tester desde tu PC debe apuntar a la IP donde corre FastAPI
BASE_URL = "http://127.0.0.1:8000"


def get_access_token():
    """Obtiene el token Bearer usando tus nuevas credenciales del .env"""
    url = f"{BASE_URL}/token"
    # Asegúrate de que tu backend use OAuth2 con PasswordRequestForm
    data = {"username": ADMIN_USER, "password": ADMIN_PASSWORD}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            logger.info("🔑 [AUTH] Token obtenido para ldiaz.")
            return token
        else:
            logger.error(
                f"❌ [AUTH] Error {response.status_code}: Revisa tus credenciales en el .env"
            )
            return None
    except Exception as e:
        logger.error(f"❌ [AUTH] No se pudo conectar al servidor: {e}")
        return None


def send_dynamic_threat(token):
    """Envía la amenaza a la ruta /threats/ que es la que estamos usando"""
    url = f"{BASE_URL}/threats/"  # Ajustado para coincidir con el Dashboard
    headers = {"Authorization": f"Bearer {token}"}

    scenarios = [
        {"desc": "Inyección SQL detectada en bypass", "type": "Critical"},
        {"desc": "Fuerza bruta sobre usuario root", "type": "High"},
        {"desc": "DDoS sync flood desde botnet", "type": "Critical"},
        {"desc": "Escaneo de vulnerabilidades persistente", "type": "Low"},
    ]

    selected = random.choice(scenarios)
    payload = {
        "ip_address": f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}",
        "description": f"{selected['desc']} - Verificado por Protocolo ZL1",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            logger.info(f"🛡️ [SENTINEL] Inserción exitosa: {payload['ip_address']}")
            return True
        return False
    except Exception as e:
        logger.error(f"❌ [CONN] Error: {e}")
        return False


if __name__ == "__main__":
    logger.info("🚀 [SENTINEL-AI] Tester sincronizado con .env")
    token = get_access_token()

    while True:
        if token and send_dynamic_threat(token):
            print("✅ Amenaza inyectada. Esperando 10s para la siguiente...")
            time.sleep(
                10
            )  # Bajé el tiempo a 10s para que veas el Dashboard llenarse rápido
        else:
            token = get_access_token()
            time.sleep(5)
