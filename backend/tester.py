import requests
import time
import random
import os
import logging
from dotenv import load_dotenv

# 1. Configuración de Logging con estilo "Sentinel"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# 2. Carga de configuración (Protocolo Zero-Hardcode)
load_dotenv()
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
BASE_URL = "http://127.0.0.1:8000"


def get_access_token():
    """Obtiene el token Bearer usando las credenciales dinámicas del .env"""
    url = f"{BASE_URL}/token"

    if not ADMIN_USER or not ADMIN_PASSWORD:
        logger.error(
            "❌ [AUTH] Variables ADMIN_USER o ADMIN_PASSWORD no encontradas en el .env"
        )
        return None

    # Formato requerido por OAuth2 (form-data)
    data = {"username": ADMIN_USER, "password": ADMIN_PASSWORD}

    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            # Log dinámico como pediste
            logger.info(f"🔑 [AUTH] Token obtenido exitosamente para: {ADMIN_USER}")
            return token
        else:
            logger.error(
                f"❌ [AUTH] Error {response.status_code}: Credenciales inválidas para {ADMIN_USER}"
            )
            return None
    except Exception as e:
        logger.error(f"❌ [AUTH] No se pudo conectar con el servidor: {e}")
        return None


def send_dynamic_threat(token):
    """Genera e inyecta una amenaza aleatoria en el sistema"""
    url = f"{BASE_URL}/threats/"
    headers = {"Authorization": f"Bearer {token}"}

    # Escenarios de ataque para probar tu Dashboard
    scenarios = [
        {"desc": "Inyección SQL en login", "type": "SQL Injection"},
        {"desc": "Fuerza bruta detectada", "type": "Brute Force"},
        {"desc": "Escaneo de puertos Nmap", "type": "Port Scan"},
        {"desc": "Acceso no autorizado a /admin", "type": "Unauthorized"},
        {"desc": "Ataque DDoS desde múltiples nodos", "type": "DDoS"},
    ]

    selected = random.choice(scenarios)
    ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"

    payload = {
        "ip_address": ip,
        "description": f"{selected['desc']} - Tipo: {selected['type']}",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            logger.info(f"🛡️ [SENTINEL] Amenaza inyectada: {ip} | {selected['type']}")
            return True
        elif response.status_code == 401:
            logger.warning("🚫 [AUTH] El token ha expirado.")
            return False
        else:
            logger.error(f"❌ [SERVER] Error {response.status_code}: {response.text}")
            return True
    except Exception as e:
        logger.error(f"❌ [CONN] Fallo al enviar amenaza: {e}")
        return True


if __name__ == "__main__":
    logger.info("🚀 [SENTINEL-AI] Iniciando Generador de Tráfico...")
    print("=" * 60)

    token = get_access_token()

    while True:
        if not token:
            logger.info("🔄 Reintentando login en 10s...")
            time.sleep(10)
            token = get_access_token()
            continue

        # Enviar amenaza
        success = send_dynamic_threat(token)

        # Si el token falló, reseteamos para pedir uno nuevo en la siguiente vuelta
        if not success:
            token = None
            continue

        # Espera de 15 segundos para no saturar la tabla del Dashboard
        print("-" * 60)
        for i in range(60, 0, -1):
            print(f"⏳ Siguiente reporte en: {i}s    ", end="\r")
            time.sleep(1)
        print()
