import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configuración única del SDK
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    logger.error("❌ [AI SERVICE] Sin API KEY.")


async def analyze_threat_with_real_ai(ip_address: str, threat_type: str) -> str:
    """
    Analiza la amenaza y devuelve el 'threat_level' con su recomendación.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # El prompt le pide a la IA que genere el LEVEL
        prompt = (
            f"Cyber-Security Analyst mode. Event: {threat_type} from IP: {ip_address}. "
            f"Output the SEVERITY LEVEL (Low to Critical) and a 1-sentence action plan."
        )

        response = model.generate_content(prompt)

        if response and response.text:
            # Esto es lo que se guardará como tu threat_level
            analysis_result = response.text.strip()
            return analysis_result

        return "Level: Unknown. Action: Manual inspection required."

    except Exception as e:
        logger.error(f"❌ [AI ERROR] {e}")
        return f"Level: High. Action: Verify {threat_type} logs immediately."
