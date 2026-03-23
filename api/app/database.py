import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükle
load_dotenv()

# Veritabanı URL'sini al (PostgreSQL 18 bağlantısı için) 
# Önemli: SQLAlchemy asenkron yapı için 'postgresql+asyncpg://' formatını bekler.
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 1. Engine Oluşturma: Veritabanı ile fiziksel bağlantıyı yönetir.
# echo=True geliştirme aşamasında SQL sorgularını terminalde görmeni sağlar.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 2. SessionMaker: Her istek geldiğinde veritabanına yeni bir "oturum" açar.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# 3. Base Sınıfı: Veritabanı modellerimizin (tabloların) miras alacağı ana sınıf.
class Base(DeclarativeBase):
    pass

# 4. Dependency (Bağımlılık): FastAPI endpoint'lerinde veritabanı oturumunu yönetir.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()