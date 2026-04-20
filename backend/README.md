# 🛡️ Sentinel-AI - BACKEND 🤖

**Análisis de Amenazas con IA Generativa | Protocolo ZL1**

Sentinel-AI es un ecosistema de ciberseguridad diseñado para detectar y analizar ataques de red en tiempo real. Utiliza modelos de lenguaje de última generación para transformar logs técnicos en reportes de seguridad comprensibles.

---

## 🏗️ Arquitectura y Decisiones Técnicas

Para este proyecto, decidí implementar una arquitectura robusta basada en las siguientes herramientas:

* **FastAPI (Backend)**: Elegido por su alto rendimiento y soporte nativo para operaciones asíncronas, ideal para manejar peticiones de IA sin bloquear el servidor.
* **PostgreSQL & SQLAlchemy**: Utilicé una base de datos relacional para garantizar la integridad de los logs y SQLAlchemy para una gestión de datos eficiente y segura.
* **Docker & Docker Compose**: Contenericé todo el ecosistema para que cualquier desarrollador pueda levantarlo con un solo comando, asegurando que las versiones de la base de datos y la API sean siempre las correctas.
* **Pydantic**: Fundamental para la validación de esquemas de datos (IPs y descripciones), asegurando que solo información válida llegue a la IA.
* **LangChain**: Utilizado para la orquestación de prompts y la estructuración de la memoria de la IA, permitiendo que Gemini analice las amenazas siguiendo un formato de reporte de seguridad profesional.

---

## 📂 Estructura del Proyecto

Basado en la organización modular, el código se divide de la siguiente manera:

* **main.py**: Punto de entrada de la aplicación y configuración de FastAPI.
* **models.py**: Definición de las tablas de la base de datos (PostgreSQL).
* **ai_service.py**: Lógica de integración con el SDK de Google Gemini.
* **auth.py**: Gestión de seguridad y generación de Tokens OAuth2.
* **tester.py**: Script de automatización que simula ataques cada 60 segundos.
* **test_models.py**: Script de pruebas unitarias para validar la conexión con PostgreSQL.
* **Dockerfile**: Configuración para la contenerización del backend usando python:3.11-slim.
* **processor.py**: Capa de lógica de negocio encargada de procesar datos y formatear peticiones para la IA.

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Preparar el Entorno
Crea un archivo .env en la carpeta raíz con tus claves.

### 2. Instalación Inicial con Docker
Comando: docker-compose up --build

### 3. Simular Amenazas
En una terminal nueva, ejecuta el tester para empezar a poblar el dashboard:
Comando: python tester.py

---

## 🔍 Comandos de Diagnóstico y Control Avanzado

* **Monitoreo de Logs en Vivo**: docker-compose logs -f backend
* **Verificación de Contenedores Activos**: docker ps
* **Acceso a la Terminal del Contenedor**: docker exec -it <container_id> /bin/bash
* **Reinicio Rápido de Servicio**: docker-compose restart backend

---

## 🔑 Gestión de Variables de Entorno y Seguridad

### 1. La Librería: python-dotenv
Se implementó para cargar las claves de forma segura sin exponerlas en el código fuente.
Instalación: pip install python-dotenv

### 2. Implementación en el Código
Importar load_dotenv de la librería dotenv y usar os.getenv para llamar las variables.

### 3. El Escudo de Seguridad: .gitignore
El archivo .env está incluido en el .gitignore para evitar filtraciones en GitHub.

### 4. Variables Requeridas en el .env
GOOGLE_API_KEY=tu_clave_de_gemini_aqui
ADMIN_USER=tu_usuario_de_acceso
ADMIN_PASSWORD=tu_contraseña_segura
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/sentinel_db

---

## 📸 Evidencias de Funcionamiento

### Dashboard de Control
![Dashboard Sentinel-AI](./assets/dashboard_preview.png)

---

> **¿Por qué lo hice así?** En lugar de una aplicación simple, busqué crear un flujo de datos profesional. El mayor reto fue la integración de la IA; ajusté la versión del SDK de Google para asegurar estabilidad en entornos Docker y apliqué modularidad para facilitar el mantenimiento y escalamiento, pensando siempre en estándares de nivel industrial.