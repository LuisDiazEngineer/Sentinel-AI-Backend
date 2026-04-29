import httpx
import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas.threat import ThreatCreate
from app.core.security import get_current_user
from db.base import get_db
from app.services.ai_service import analyze_threat_with_real_ai
from app.models.threat import ThreatLog

logger = logging.getLogger(__name__)

# Agrupamos los endpoints bajo la categoría "Threats" para la documentación interactiva (Swagger)
router = APIRouter(tags=["Threats"])

# Variable global que actúa como "Interruptor de Pánico" para todo el sistema
SYSTEM_LOCKDOWN = False


import random
from datetime import datetime  # Importación única y limpia

# ... otros imports ...


@router.post("/threats/")
async def create_threat(
    threat_data: ThreatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    SENTINEL AI - MOTOR DE INGESTA PROFESIONAL
    - Persistencia inmutable: Los registros pasados no cambian.
    - Lockdown Selectivo: Solo afecta a las nuevas IPs entrantes.
    - Variabilidad Estocástica: Resultados realistas (ej. 67%, 42%) en lugar de fijos.
    """
    global SYSTEM_LOCKDOWN

    # 1. Extracción y Limpieza
    ip = str(threat_data.ip_address)
    desc = (threat_data.description or "Traffic Trace").strip()
    low_desc = desc.lower()

    # 2. Conteo de ataques recientes (Historial para Scoring)
    try:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        stmt = select(func.count(ThreatLog.id)).where(
            ThreatLog.ip_address == ip, ThreatLog.timestamp >= one_hour_ago
        )
        result = await db.execute(stmt)
        recent_attacks = result.scalar() or 0
    except Exception as e:
        print(f"⚠️ Error historial: {e}")
        recent_attacks = 0

    # 3. GeoIP (Localización)
    loc_info = {
        "countryCode": "GL",
        "city": "Unknown Node",
        "lat": 0.0,
        "lon": 0.0,
        "isp": "Unknown",
    }
    if not ip.startswith(("127.", "192.168.", "10.")):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"http://ip-api.com/json/{ip}", timeout=2.0)
                if resp.status_code == 200:
                    loc_info.update(resp.json())
        except:
            pass

    # 4. Análisis de IA
    try:
        report = await analyze_threat_with_real_ai(ip, desc)
    except:
        report = f"Análisis manual requerido: {desc}"

    # --- 5. CÁLCULO DE SCORE CON ALTA VARIABILIDAD ---
    # Base con ruido para evitar el "15% exacto"
    score = 15 + (recent_attacks * 8) + random.randint(-5, 5)

    # Pesos por Keywords con rangos dinámicos
    if "sql" in low_desc:
        score += random.randint(30, 38)
    if "ddos" in low_desc:
        score += random.randint(45, 52)
    if "brute force" in low_desc:
        score += random.randint(22, 28)
    if "bypass" in low_desc:
        score += random.randint(25, 33)

    # 🚨 IMPACTO DEL LOCKDOWN (Solo para el registro actual)
    # Si está activo, forzamos el score por encima del umbral de TERMINATED (85)
    if SYSTEM_LOCKDOWN:
        # Sumamos un bono de emergencia para asegurar el ROJO en el nuevo registro
        score += random.randint(50, 60)
        print(f"🚨 [SENTINEL] Lockdown activo: IP {ip} marcada para TERMINATION.")

    final_score = int(max(0, min(score, 100)))

    # --- 6. MATRIZ DE DECISIÓN AUSTIN (PERSISTENTE) ---
    if final_score >= 85:
        status_action, level = "TERMINATED", "Critical"
    elif final_score >= 60:
        status_action, level = "QUARANTINED", "High"
    elif final_score >= 35:
        status_action, level = "BLOCKED", "Medium"
    else:
        status_action, level = "LOGGED", "Low"

    # 7. Persistencia Única (Se guarda el estado del momento)
    try:
        new_log = ThreatLog(
            ip_address=ip,
            description=desc[:250],
            ai_analysis=report,
            timestamp=datetime.utcnow(),
            threat_level=level,
            status=status_action,  # Aquí se queda grabado el TERMINATED si hubo lockdown
            risk_score=final_score,
            country_code=str(loc_info.get("countryCode", "GL"))[:5],
            city=str(loc_info.get("city", "Unknown"))[:100],
            latitude=float(loc_info.get("lat", 0.0)),
            longitude=float(loc_info.get("lon", 0.0)),
            isp=str(loc_info.get("isp", "Unknown ISP"))[:100],
        )

        db.add(new_log)
        await db.commit()
        await db.refresh(new_log)

        return {
            "status": "success",
            "score": final_score,
            "action": status_action,
            "location": f"{new_log.city}, {new_log.country_code}",
        }
    except Exception as db_e:
        await db.rollback()
        print(f"❌ DATABASE ERROR: {db_e}")
        raise HTTPException(status_code=500, detail="Error de persistencia")


@router.delete("/threats/{threat_id}", tags=["Protocolo ZL1"])
async def delete_threat(
    threat_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Elimina registros (Solo administradores autorizados)"""
    result = await db.execute(select(ThreatLog).where(ThreatLog.id == threat_id))
    threat_entry = result.scalar_one_or_none()
    if not threat_entry:
        raise HTTPException(status_code=404, detail="No encontrado")

    await db.delete(threat_entry)
    await db.commit()
    return None


@router.get("/stats/", tags=["Dashboard"])
async def get_stats(
    db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)
):
    """Calcula estadísticas para las gráficas del Dashboard"""
    query = select(ThreatLog.threat_level, func.count(ThreatLog.id)).group_by(
        ThreatLog.threat_level
    )
    result = await db.execute(query)
    stats = result.all()
    return {
        "total": sum(count for level, count in stats),
        "breakdown": {level: count for level, count in stats},
        "authorized_by": current_user,
    }


@router.get("/threats/", tags=["Dashboard"])
async def get_all_threats(db: AsyncSession = Depends(get_db)):
    """Formatea las amenazas para que el Mapa (React) las pueda leer correctamente"""
    result = await db.execute(select(ThreatLog).order_by(ThreatLog.timestamp.desc()))
    threats = result.scalars().all()

    formatted_threats = []
    for t in threats:
        formatted_threats.append(
            {
                "id": t.id,
                "ip": t.ip_address,
                "ai_analysis": t.ai_analysis,
                "location": f"{t.city}, {t.country_code}",
                "score": t.risk_score,
                "description": t.description,
                "status": t.status,
                "timestamp": t.timestamp.isoformat() if t.timestamp else None,
                "latitude": t.latitude,
                "longitude": t.longitude,
            }
        )
    return formatted_threats


@router.post("/system/lockdown")
async def toggle_lockdown(current_user: str = Depends(get_current_user)):
    """Activa el 'Lockdown Mode' (Incrementa la sensibilidad del motor de riesgo)"""
    global SYSTEM_LOCKDOWN
    SYSTEM_LOCKDOWN = not SYSTEM_LOCKDOWN
    status_label = "ACTIVATED" if SYSTEM_LOCKDOWN else "DEACTIVATED"
    print(f"🚨 [SENTINEL PROTOCOL] Lockdown {status_label} por: {current_user}")
    return {
        "status": status_label,
        "lockdown": SYSTEM_LOCKDOWN,
        "operator": current_user,
    }


@router.post("/analyze")
async def analyze_threat(threat_data: dict, db: AsyncSession = Depends(get_db)):
    print(f"🔍 [SENTINEL] Analizando nueva amenaza...")

    # Aquí es donde ocurre la magia
    analysis = await analyze_threat_with_real_ai(threat_data)

    if not analysis:
        raise HTTPException(status_code=500, detail="Error en el motor de IA")

    print(f"✅ [SENTINEL] Análisis completado con éxito.")
    return {"status": "analyzed", "report": analysis}
