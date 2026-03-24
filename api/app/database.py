import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

#  şifreleri ve URL'ler gibi hassas verileri kaynak koddan ayırmak için .env dosyasını yüklüyoruz.
load_dotenv()

# PostgreSQL 18 Bağlantı Yapılandırması
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 1. ASENKRON MOTOR (Engine): Veritabanı ile fiziksel iletişimi sağlar.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 2. OTURUM FABRİKASI (SessionMaker): Her RADIUS isteği için DB'de yeni bir oturum açar.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. BASE SINIFI (ORM Temeli): Veritabanındaki tablolarımız (radcheck, radacct vb.) 
# bu sınıftan miras alarak Python nesnelerine dönüştürülür.
class Base(DeclarativeBase):
    pass

# 4. DEPENDENCY INJECTION (Bağımlılık Enjeksiyonu)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()