# backend/app/db/session.py
import asyncio
from app.core.security import get_password_hash
from app.models.user import User
from app.core.config import settings
from db.base import AsyncSessionLocal


async def create_admin():
    """
    SCRIPT DE SEMILLADO (Seed Script)
    Propósito: Crear el primer usuario administrador para poder loguearse en el sistema.
    Relación: Se conecta con 'models/user.py' para saber qué campos insertar.
    """
    async with AsyncSessionLocal() as db:
        # 1. Obtención de datos seguros
        # Relación: Extrae las credenciales del .env mediante 'settings' para no exponerlas.
        username = settings.ADMIN_USER
        password = settings.ADMIN_PASSWORD

        # 2. Cifrado de seguridad
        # Relación: Usa 'get_password_hash' para nunca guardar la clave en texto plano.
        hashed_password = get_password_hash(password)

        # 3. Creación de la instancia del usuario
        # EL ARREGLO: Aquí añadiste el campo 'email', cumpliendo con la restricción 'nullable=False'
        # que definiste en el modelo de SQLAlchemy. Sin esto, la base de datos rechazaría el registro.
        admin = User(
            username=username,
            email="admin@sentinel.ai",  # Email institucional por defecto
            hashed_password=hashed_password,
            is_active=True,
            role="admin",
        )

        try:
            # 4. Persistencia en la base de datos
            db.add(admin)
            await db.commit()
            print(f"🚀 Usuario {username} creado con éxito.")
        except Exception as e:
            # 5. Manejo de errores y reversión (Rollback)
            # Relación: Si el usuario ya existe, el rollback limpia la sesión para evitar bloqueos.
            print(f"❌ Error al insertar: {e}")
            await db.rollback()


if __name__ == "__main__":
    # Ejecuta la función de forma asíncrona desde la terminal
    asyncio.run(create_admin())
