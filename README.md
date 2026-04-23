# 🛡️ Sentinel-AI

**Sistema de Monitoreo de Ciberseguridad en Tiempo Real**

Sentinel-AI es una plataforma de análisis de amenazas que simula, detecta y visualiza ataques de red en tiempo real. Diseñado como un sistema full-stack, integra backend, frontend y lógica de clasificación de riesgo para ofrecer una visión clara del estado de seguridad de un entorno.

---

## 🚀 Características principales

* 📡 **Monitoreo en tiempo real** de amenazas (SQL Injection, Brute Force, DDoS, etc.)
* 🌍 **Geolocalización de IPs** para visualizar origen de ataques
* 📊 **Dashboard interactivo** con mapa global y feed de incidentes
* ⚠️ **Clasificación de riesgo dinámica** basada en comportamiento
* 🔐 **Autenticación segura** con JWT
* 🐳 **Contenerización con Docker** para despliegue reproducible
* 🤖 **Simulación de ataques** mediante script automatizado
* 📈 **Estado del sistema (System Health)** en tiempo real

---

## 🧠 Arquitectura del sistema

El sistema sigue una arquitectura modular basada en servicios:

* **Backend:** API REST construida con FastAPI
* **Frontend:** Dashboard interactivo desarrollado con React
* **Base de datos:** PostgreSQL
* **Infraestructura:** Docker & Docker Compose

```bash
[Attack Simulator] → [FastAPI Backend] → [PostgreSQL]
                                 ↓
                           [React Frontend]
```

---

## ⚙️ Tecnologías utilizadas

### Backend

* Python
* FastAPI
* Pydantic
* JWT Authentication

### Frontend

* React
* JavaScript
* HTML5 & CSS3
* Bootstrap

### Base de Datos

* PostgreSQL

### DevOps & Herramientas

* Docker / Docker Compose
* Git & GitHub

---

## 🧪 Simulación de ataques

El sistema incluye un script que genera tráfico simulado con distintos tipos de ataques:

* SQL Injection
* SSH Brute Force
* Port Scanning
* Accesos no autorizados
* DDoS

Esto permite probar el comportamiento del sistema en escenarios cercanos a producción.

---

## ⚠️ Lógica de clasificación de riesgo

El sistema calcula el nivel de riesgo en base a múltiples factores:

* Tipo de ataque
* Frecuencia de eventos
* Repetición de IP
* Comportamiento sospechoso

Esto permite priorizar incidentes críticos y mejorar la toma de decisiones.

---

## 🔐 Autenticación

El acceso al sistema está protegido mediante JWT:

* Login seguro
* Generación de token
* Protección de endpoints

---

## 📊 Funcionalidades del Dashboard

* Nivel global de amenaza (%)
* Mapa de ataques en tiempo real
* Feed de incidentes con nivel de riesgo
* Estado de servicios (Docker, DB, AI Engine)
* Botón de respuesta rápida: **Emergency Lockdown**

---

## 🧪 Testing

Se implementaron pruebas básicas para validar:

* Autenticación
* Creación de amenazas
* Endpoints críticos

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sentinel-ai.git
cd sentinel-ai
```

### 2. Configurar variables de entorno

Crear un archivo `.env`:

```env
ADMIN_USER=admin
ADMIN_PASSWORD=1234
```

---

### 3. Ejecutar con Docker

```bash
docker-compose up --build
```

---

### 4. Acceder al sistema

* Frontend: http://localhost:3000
* Backend: http://localhost:8000

---

## 🎯 Objetivo del proyecto

Este proyecto fue desarrollado con el objetivo de:

* Simular un sistema real de ciberseguridad
* Aplicar buenas prácticas de desarrollo backend/frontend
* Integrar múltiples tecnologías en un entorno funcional
* Demostrar capacidades técnicas para entornos profesionales

---

## 📌 Posibles mejoras futuras

* Procesamiento asíncrono con colas de mensajes
* Integración con herramientas de logging (ELK Stack)
* Machine Learning para detección avanzada
* Despliegue en la nube (AWS / GCP)
* Sistema de alertas en tiempo real

---

## 👨‍💻 Autor

**Luis Díaz**
Desarrollador de Software Junior

---

## ⭐ Notas finales

Sentinel-AI no es solo una demostración visual, sino una base funcional para un sistema de monitoreo de amenazas, con enfoque en escalabilidad, análisis y visualización en tiempo real.

---
