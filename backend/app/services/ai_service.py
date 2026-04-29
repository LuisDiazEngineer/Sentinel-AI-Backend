import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carga de variables de entorno
# Relación: Busca el archivo .env para obtener la GOOGLE_API_KEY necesaria para el modelo.
load_dotenv()
logger = logging.getLogger(__name__)

# 2. Configuración única del SDK de Google Gemini
# Relación: Si la API KEY no existe, el servicio de IA se desactiva preventivamente.
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.error("❌ [AI SERVICE] Sin API KEY detectada en el entorno.")


async def analyze_threat_with_real_ai(ip_address: str, threat_type: str) -> str:
    """
    SERVICIO DE ANÁLISIS GENERATIVO
    Propósito: Actuar como un analista SOC de nivel 2 para interpretar la amenaza.
    Relación: Es llamado por 'api/threats.py' durante el procesamiento de cada evento.
    """
    try:
        # Definición del modelo (Gemini 2.5 Flash)
        # Se usa la versión Flash por su baja latencia, ideal para análisis en tiempo real.
        model = genai.GenerativeModel("gemini-2.5-flash")

        # 3. Ingeniería de Prompt (Prompt Engineering)
        # Relación: Instruye a la IA para que asuma un rol específico y devuelva un
        # formato útil: Nivel de severidad y plan de acción.
        prompt = (
            f"Cyber-Security Analyst mode. Event: {threat_type} from IP: {ip_address}. "
            f"Output the SEVERITY LEVEL (Low to Critical) and a 1-sentence action plan."
        )

        # Generación de contenido asíncrona
        response = model.generate_content(prompt)

        if response and response.text:
            # 4. Limpieza de datos
            # Relación: El texto devuelto se guardará en la columna 'ai_analysis' de la DB.
            analysis_result = response.text.strip()
            return analysis_result

        return "Level: Unknown. Action: Manual inspection required."

    except Exception as e:
        # 5. Sistema de Fallback (Seguridad de disponibilidad)
        # Relación: Si la API de Google falla o hay problemas de red, el sistema
        # devuelve una respuesta predeterminada para no detener el flujo del backend.
        logger.error(f"❌ [AI ERROR] Error en el motor generativo: {e}")
        return f"Level: High. Action: Verify {threat_type} logs immediately."
