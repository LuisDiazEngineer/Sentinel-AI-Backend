# 1. Imagen Base (El sistema operativo)
# Relación: Usamos una versión ligera de Python 3.11 para que el contenedor sea rápido y seguro.
FROM python:3.11-slim

# 2. Directorio de Trabajo
# Relación: Crea una carpeta interna en el contenedor llamada '/app' donde vivirá el proyecto.
WORKDIR /app

# 3. Instalación de Dependencias del Sistema
# Relación: Aquí solucionaste el error de 'bcrypt' que tuviste antes. 
# Al instalar 'build-essential' y 'libffi-dev', permites que Python compile librerías de seguridad.
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Gestión de Dependencias de Python
# Relación: Copiamos solo el archivo de requerimientos primero para aprovechar la 'caché' de Docker.
# Esto hace que si cambias el código pero no las librerías, el despliegue sea mucho más rápido.
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia del Código Fuente
# Relación: Transporta todo tu código de la carpeta 'backend/' de tu PC al interior del contenedor.
COPY backend/ .

# 6. Comando de Ejecución (El motor)
# Relación: Inicia el servidor Uvicorn apuntando a tu aplicación principal (app.main:app).
# Usamos '--host 0.0.0.0' para que el contenedor sea accesible desde fuera.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]