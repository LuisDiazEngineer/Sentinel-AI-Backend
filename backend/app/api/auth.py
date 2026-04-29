from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from db.base import get_db
from app.core.security import create_access_token, verify_password, is_secure_region
from app.models.user import User  # Referencia al modelo de usuario en la DB
from sqlalchemy.future import select
from db.base import get_db

# <--- Importante: traelo de models

# Definición del router para agrupar los endpoints de autenticación bajo el tag "Authentication"
router = APIRouter(tags=["Authentication"])


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # Recibe username y password del estándar OAuth2
    db: AsyncSession = Depends(get_db),  # Inyecta la sesión asíncrona de PostgreSQL
    x_region: str = Header(None),  # Captura la región desde los headers de la petición
):
    """
    ENDPOINT DE LOGIN (SENTINEL PROTOCOL)
    Propósito: Validar identidad y región para emitir un Token JWT de acceso.
    """

    # 1. Validar Protocolo Sentinel (Seguridad Geográfica)
    # Relación: Usa 'is_secure_region' para bloquear accesos fuera de zonas permitidas (ej. Austin, Texas).
    if not is_secure_region(x_region):
        raise HTTPException(
            status_code=403, detail="Acceso denegado: Región no segura."
        )

    # 2. Buscar usuario en la DB
    # Relación: Realiza una consulta asíncrona al modelo 'User' definido en la base de datos.
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    # 3. Verificar credenciales
    # Relación: 'verify_password' compara el password plano con el hash de la DB usando Bcrypt.
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # 4. Generar Token JWT
    # Relación: Crea un token firmado que el Frontend guardará para autorizar futuras peticiones.
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
