from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# 1. Creamos el motor de la base de datos (Se creará un archivo llamado sentinel.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sentinel.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Sesión para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Clase base para nuestros modelos
Base = declarative_base()


# 4. El Modelo: Así se verá tu tabla de amenazas detectadas
class ThreatLog(Base):
    __tablename__ = "threat_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    threat_level = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# 5. Función para crear las tablas físicamente
def create_tables():
    Base.metadata.create_all(bind=engine)
