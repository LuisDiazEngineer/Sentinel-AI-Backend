import asyncio
import os
from sqlalchemy import select
from dotenv import load_dotenv

# Importamos la configuración oficial de tu app
# Asegúrate de que la ruta coincida con tu estructura (backend.app)
# Cambiamos SessionLocal por AsyncSessionLocal
from backend.app.database import AsyncSessionLocal, engine, Base
from backend.app.models import User
from backend.app.auth import hash_password

# Cargamos el .env desde la raíz
load_dotenv()


async def seed_system():
    print("🚀 [SENTINEL-AI] Iniciando proceso de Provisión...")

    # 1. Verificación de seguridad de la URL
    db_url = str(engine.url)
    print(f"🔗 Conectando a: {db_url}")

    if "sqlite" in db_url:
        print(
            "❌ ERROR CRÍTICO: El sistema detectó SQLite pero se requiere PostgreSQL."
        )
        print(
            "Revisa que tu .env tenga 'localhost' en lugar de 'db' si corres esto fuera de Docker."
        )
        return

    try:
        # 2. Crear las tablas en PostgreSQL
        async with engine.begin() as conn:
            print("🛠️ Sincronizando tablas en la base de datos...")
            await conn.run_sync(Base.metadata.create_all)

        # 3. Insertar el Administrador
        async with AsyncSessionLocal() as db:
            admin_user = os.getenv("ADMIN_USER")
            admin_pass = os.getenv("ADMIN_PASSWORD")

            # Buscamos si ya existe para evitar errores de duplicado
            result = await db.execute(select(User).filter(User.username == admin_user))
            user_exists = result.scalars().first()

            if not user_exists:
                print(f"👤 Creando cuenta raíz: {admin_user}...")
                new_user = User(
                    username=admin_user,
                    email=f"{admin_user}@sentinel.ai",
                    hashed_password=hash_password(admin_pass),
                    is_active=True,
                )
                db.add(new_user)
                await db.commit()
                print("✅ [SUCCESS] Usuario administrador inyectado correctamente.")
            else:
                print(f"ℹ️ [SKIP] El usuario '{admin_user}' ya existe en PostgreSQL.")

    except Exception as e:
        print(f"🔥 ERROR DE CONEXIÓN: {e}")
        print(
            "\n💡 Tip de Ingeniero: Si el error es 'Connection Refused', asegúrate de que:"
        )
        print("1. Tu contenedor de Postgres esté corriendo.")
        print(
            "2. En el .env uses 'localhost:5432' (no 'db:5432') si corres el script desde Windows."
        )


if __name__ == "__main__":
    asyncio.run(seed_system())
