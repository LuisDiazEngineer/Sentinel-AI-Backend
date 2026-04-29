# 🛡️ Sentinel-AI

**Sentinel-AI** es una plataforma de simulación de ciberseguridad tipo SOC (Security Operations Center) que analiza eventos de red en tiempo real, calcula niveles de riesgo y ejecuta respuestas automáticas ante amenazas.

---

## ⚙️ Arquitectura general

El sistema se organiza en 4 capas:

### 📡 Ingesta de eventos
- Simulador interno de tráfico
- APIs externas (futuras integraciones)

### 🧠 Enriquecimiento de datos
- GeoIP (ubicación, ISP, país)
- Validación de IPs
- Normalización de datos

### 🔍 Motor de análisis y scoring
- Tipo de ataque (DDoS, SQLi, brute force, etc.)
- Patrones de comportamiento
- Análisis con IA (Gemini)
- Reputación histórica de IPs

### 🧾 Decisión y respuesta
- LOGGED → benign event
- QUARANTINED → suspicious event
- TERMINATED → critical threat

---

## 🌐 Simulación del sistema

Generador de tráfico malicioso con:
- IPs globales simuladas
- múltiples tipos de ataques
- comportamiento aleatorio controlado

---

## 🔄 Flujo del sistema

📡 Event Stream → 🧠 Enrichment Layer → 🔍 Detection Engine → 🤖 AI Scoring (Gemini) → 📊 Risk Engine → 🧾 Response System → 🗄 Data Layer (PostgreSQL) → 📈 SOC Dashboard

---

## 🚀 Ejecución del proyecto

### 1. Clonar repositorio
```bash
git clone <repo>
cd sentinel-ai
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

Activar entorno:

Windows (PowerShell):
```bash
.\venv\Scripts\activate
```

Linux / Mac:
```bash
source venv/bin/activate
```

---

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

---

### 4. Variables de entorno
```env
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost/sentinel_db
SECRET_KEY=tu_llave_secreta_aqui
GOOGLE_API_KEY=tu_api_key_de_gemini
ADMIN_USER=ldiaz
ADMIN_PASSWORD=tu_password_segura
```

---

### 5. Inicializar base de datos
```bash
python -m backend.db.session
```

---

### 6. Ejecutar sistema

Backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Simulador:
```bash
python -m backend.tests.simulation.attack_simulator
```

Frontend:
```bash
cd frontend
npm run dev
```

---

## 📊 Estado del proyecto

🟡 En desarrollo activo  
✔ arquitectura definida  
✔ motor de análisis funcional  
🔄 mejoras en IA y frontend  

---

## 👨‍💻 Autor

**Luis Diaz — Backend | IA | Sistemas**

## 🖼️ Recorrido visual y características

---

### 🔐 Sistema de Autenticación Segura
![Login Screen](./screenshots/login.png)

**Funcionalidad:**  
Autenticación segura basada en JWT.

**Detalle Técnico:**  
Validación de credenciales contra base de datos PostgreSQL, con hashing de contraseñas mediante bcrypt. Protección de rutas en el backend usando autenticación basada en tokens.

---

### 🌍 Mapa de Inteligencia de Amenazas en Tiempo Real
![Global Map](./screenshots/dashboard_map.png)

**Funcionalidad:**  
Visualización geoespacial de intentos de intrusión a nivel global.

**Detalle Técnico:**  
Consumo de eventos desde el stream de ingesta, con enriquecimiento mediante GeoIP para obtener coordenadas, ciudades e ISP de origen.

---

### 🧠 Análisis de Riesgo con IA (Gemini)
![AI Report](./screenshots/ai_analysis.png)

**Funcionalidad:**  
Evaluación automática de amenazas y generación de recomendaciones.

**Detalle Técnico:**  
Integración con Gemini 2.5 Flash (LLM), que analiza el payload de los ataques para generar:
- reportes técnicos  
- recomendaciones de mitigación  
- score de riesgo dinámico  

---

### 📊 Monitoreo SOC y Estadísticas
![Stats Panel](./screenshots/stats.png)

**Funcionalidad:**  
Monitoreo en tiempo real del estado del sistema y eventos de seguridad.

**Detalle Técnico:**  
Cálculo dinámico de estados:
- Logged (registrado)  
- Quarantined (cuarentena)  
- Terminated (bloqueado)  

Incluye monitoreo de:
- estado del motor de IA  
- estado de la base de datos  

---

### 🎯 Motor de Scoring Dinámico
![Risk Engine](./screenshots/risk_engine.png)

**Funcionalidad:**  
Clasificación de amenazas con mayor precisión y variabilidad.

**Detalle Técnico:**  
Implementación de un motor heurístico estocástico.  
A diferencia de sistemas estáticos, Sentinel genera valores de riesgo variables (ej. 67%, 42%, 89%), evitando patrones predecibles y permitiendo una clasificación más realista.

---

### 🚨 Protocolo de Lockdown de Emergencia (Tolerancia Cero)
![Lockdown Mode](./screenshots/lockdown.png)

**Funcionalidad:**  
Activación de una política de seguridad agresiva en tiempo real.

**Detalle Técnico:**  
Al activar el modo Lockdown:
- se inyecta un factor de sensibilidad de +50 a nuevas amenazas  
- los eventos se escalan automáticamente a estados críticos (TERMINATED según el riesgo)  
- se mantiene la integridad del historial sin alterar registros previos  

Esto permite contener amenazas activas sin comprometer la trazabilidad del sistema.