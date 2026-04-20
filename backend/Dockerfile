FROM python:3.11-slim

WORKDIR /app

# 1. Instalamos las herramientas de compilación necesarias
# Esto soluciona el problema de bcrypt y conectores de DB
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiamos e instalamos dependencias de Python
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiamos el resto del código
COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]