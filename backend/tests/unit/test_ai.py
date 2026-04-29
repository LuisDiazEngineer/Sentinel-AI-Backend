import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configura tu llave
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Buscando modelos disponibles para tu API Key...")

try:
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(f"✅ Modelo disponible: {m.name}")
except Exception as e:
    print(f"❌ Error al conectar con Google: {e}")
