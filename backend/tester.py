import requests
import random
import time
import logging
import os
from dotenv import load_dotenv

# Cargar configuración desde .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración sensible desde variables de entorno
BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# 🌍 Pool de IPs Globales para "pintar" el mapa con diversidad
GLOBAL_SITES = [
    {"ip": "151.101.129.140", "city": "New York"},
    {"ip": "212.58.244.70", "city": "London"},
    {"ip": "202.5.221.66", "city": "Tokyo"},
    {"ip": "80.58.61.250", "city": "Madrid"},
    {"ip": "200.221.2.45", "city": "Sao Paulo"},
    {"ip": "1.1.1.1", "city": "Sydney"},
    {"ip": "103.21.244.0", "city": "Mumbai"},
    {"ip": "41.222.1.1", "city": "Johannesburg"},
    {"ip": "161.185.160.93", "city": "Austin"},  # ¡No podía faltar Texas!
    {"ip": "190.235.12.34", "city": "Lima"},
]

ATTACK_PAYLOADS = [
    "SQL Injection attempt on /v1/auth/login",
    "Brute Force attack - SSH Port 22",
    "Critical: DDoS Syn Flood detected",
    "Suspicious XSS payload in headers",
    "Path Traversal: attempt to access /etc/shadow",
]


def get_token():
    """Autenticación automática usando credenciales del .env"""
    url = f"{BASE_URL}/token"
    if not ADMIN_USER or not ADMIN_PASSWORD:
        logger.error("❌ ERROR: ADMIN_USER o ADMIN_PASSWORD no definidos en .env")
        return None

    data = {"username": ADMIN_USER, "password": ADMIN_PASSWORD}
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logger.info(f"🔑 Sesión iniciada para el analista: {ADMIN_USER}")
            return response.json().get("access_token")
        return None
    except Exception as e:
        logger.error(f"❌ Error conectando al servidor: {e}")
        return None


def generate_random_ip():
    return ".".join(map(str, (random.randint(1, 254) for _ in range(4))))


def start_simulation():
    token = get_token()
    if not token:
        return

    headers = {"Authorization": f"Bearer {token}"}
    print("-" * 50)
    print("🛰️  SENTINEL AI - SIMULADOR DE CIBERATAQUES GLOBALES")
    print("-" * 50)

    try:
        while True:
            # Lógica de selección de IP
            if random.random() < 0.7:
                target = random.choice(GLOBAL_SITES)
                ip = target["ip"]
            else:
                ip = generate_random_ip()

            payload = {"ip_address": ip, "description": random.choice(ATTACK_PAYLOADS)}

            try:
                res = requests.post(
                    f"{BASE_URL}/threats/", json=payload, headers=headers
                )

                if res.status_code == 200:
                    data = res.json()
                    # Imprimimos el resultado con formato de consola de seguridad
                    print(
                        f"[ALERT] IP: {ip.ljust(15)} | Loc: {data.get('location', 'Unknown').ljust(25)} | Risk: {data.get('score')}%"
                    )
                elif res.status_code == 401:
                    logger.warning("🔄 Token expirado. Renovando acceso...")
                    token = get_token()
                    headers = {"Authorization": f"Bearer {token}"}
                else:
                    print(f"⚠️ Error {res.status_code}: {res.text}")

            except Exception as e:
                logger.error(f"📡 Error de red: {e}")

            # Pausa para respetar la API de GeoIP y simular tiempo real
            time.sleep(random.randint(4, 8))

    except KeyboardInterrupt:
        print("\n🛑 Simulación finalizada por el analista.")


if __name__ == "__main__":
    start_simulation()
