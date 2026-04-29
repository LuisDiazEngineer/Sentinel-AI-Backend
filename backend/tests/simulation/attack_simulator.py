import requests
import random
import time
import os
import logging
from dotenv import load_dotenv

# Configuración de logs para ver la actividad de la simulación en la terminal
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# --- CONFIGURACIÓN ---
BASE_URL = "http://127.0.0.1:8000"
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Lista de IPs para simular ataques de diferentes partes del mundo
# He añadido más IPs internacionales para que tu mapa se vea global y profesional
SITES = [
    # 🔴 TERMINATED (Requiere SQL o DDOS + Historial o Lockdown)
    {"ip": "222.186.31.42", "desc": "critical sql injection and ddos attack"},
    {"ip": "91.241.19.84", "desc": "emergency bypass attempt ddos system"},
    # 🟣 QUARANTINED (Ataques serios pero sin llegar al 90%)
    {"ip": "45.146.164.110", "desc": "sql injection attempt on login"},
    {"ip": "103.212.223.15", "desc": "brute force bypass protocol"},
    # 🟠 BLOCKED (Amenazas medias)
    {"ip": "161.185.160.93", "desc": "brute force on port 22"},
    {"ip": "212.58.244.70", "desc": "port scanning activity"},
    # 🔵 LOGGED (Tráfico sospechoso pero leve)
    {"ip": "190.235.12.34", "desc": "unusual traffic pattern"},
    {"ip": "80.58.61.250", "desc": "failed authentication attempt"},
]


def get_token():
    """
    SOLICITUD DE CREDENCIALES (Auth Handshake)
    Relación: Se comunica con 'auth.py' para obtener permiso de reportar ataques.
    Usa el header 'X-Region' para cumplir con el Protocolo Sentinel.
    """
    url = f"{BASE_URL}/token"
    login_data = {"username": ADMIN_USER, "password": ADMIN_PASSWORD}
    headers = {"X-Region": "Texas"}  # Zona autorizada

    try:
        response = requests.post(url, data=login_data, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            logger.error(
                f"❌ Error al obtener token: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        logger.error(f"❌ No hay conexión con el servidor: {e}")
        return None


def start_simulation():
    """
    BUCLE DE ATAQUE SIMULADO
    Propósito: Generar datos constantes para que el Dashboard de React muestre actividad.
    Relación: Envía datos a 'api/threats.py' cada 30 segundos.
    """
    print("\n" + "=" * 60)
    print("🛰️  SENTINEL AI - TRÁFICO EN TIEMPO REAL INICIADO")
    print("=" * 60)

    token = get_token()
    if not token:
        print("🚫 Simulación abortada: No se pudo obtener un token válido.")
        return

    # Preparamos los headers con el Bearer Token para autenticación JWT
    headers = {"Authorization": f"Bearer {token}", "X-Region": "Texas"}

    try:
        while True:
            # Selección aleatoria de una amenaza para simular variabilidad
            target = random.choice(SITES)
            payload = {"ip_address": target["ip"], "description": target["desc"]}

            try:
                # Envío de la amenaza al endpoint principal del Backend
                res = requests.post(
                    f"{BASE_URL}/threats/", json=payload, headers=headers
                )

                if res.status_code == 200:
                    data = res.json()
                    # El backend responde con el score de riesgo calculado por la IA
                    print(
                        f"🔥 [ALERTA] IP: {target['ip'].ljust(15)} | Riesgo: {str(data.get('score')).center(5)}% | Ubicación: {data.get('location')}"
                    )
                elif res.status_code == 401:
                    # Manejo de expiración de sesión: Si el token muere, pide otro
                    logger.warning("🔄 Token expirado. Solicitando uno nuevo...")
                    token = get_token()
                    headers["Authorization"] = f"Bearer {token}"
                else:
                    print(f"⚠️ Error al enviar: {res.status_code} - {res.text}")

            except Exception as e:
                logger.error(f"📡 Error de red: {e}")

            # Pausa controlada para no saturar la API de Google Gemini (Rate Limit)
            time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Simulación detenida por el usuario.")


if __name__ == "__main__":
    start_simulation()
