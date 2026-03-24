from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import redis.asyncio as redis
import os
from passlib.context import CryptContext

from .database import get_db
from . import models, schemas

# FastAPI Uygulaması: Merkezi Politika Motoru (Policy Engine)
app = FastAPI(title="S3M NAC Policy Engine")

# Güvenlik: Şifrelerin açık metin olarak tutulmaması için Bcrypt hashing 
# mekanizmasını yapılandırıyoruz
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Performans: Aktif oturum takibi ve rate-limiting için Redis bağlantısını kuruyoruz
redis_client = redis.from_url(
    f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379/0", 
    decode_responses=True
)

# 1. KIMLIK DOGRULAMA (AUTHENTICATION) [/auth]
# Kullanıcının kimliğini (Username/Password) doğrular
@app.post("/auth", response_model=schemas.RadiusResponse)
async def authenticate(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
    # Veritabanından kullanıcıyı sorgula.
    result = await db.execute(select(models.RadCheck).where(models.RadCheck.username == request.username))
    user = result.scalars().first()
    
    # Bcrypt ile şifre doğrulaması yaparak güvenliği sağlıyoruz.
    if not user or not pwd_context.verify(request.password, user.value):
        return {"status": "reject", "attributes": {"Reply-Message": "Giris Basarisiz"}}
    
    return {"status": "accept", "attributes": {"Reply-Message": "Hos geldiniz"}}

# 2. YETKILENDIRME (AUTHORIZATION) [/authorize]
# Kullanıcının grubuna göre VLAN ve ağ politikalarını belirler
@app.post("/authorize", response_model=schemas.RadiusResponse)
async def authorize(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
    # Kullanıcının dahil olduğu grubu (admin, employee, guest) tespit et.
    group_query = await db.execute(select(models.RadUserGroup).where(models.RadUserGroup.username == request.username))
    user_group = group_query.scalars().first()
    group_name = user_group.groupname if user_group else "guest"
    
    # Tespit edilen gruba ait VLAN gibi RADIUS özniteliklerini çek.
    attrs_query = await db.execute(select(models.RadGroupReply).where(models.RadGroupReply.groupname == group_name))
    response_attrs = {attr.attribute: attr.value for attr in attrs_query.scalars().all()}
    
    return {"status": "accept", "attributes": response_attrs}

# 3. HESAP YÖNETIMI (ACCOUNTING) [/accounting]
# Oturum verilerini (Start, Stop, Interim) kaydeder ve veri tüketimini izler
@app.post("/accounting")
async def accounting(request: schemas.AccountingRequest, db: AsyncSession = Depends(get_db)):
    now = datetime.now()
    
    new_acct = models.RadAcct(
        username=request.username,
        acctsessionid=request.session_id,
        acctuniqueid=f"{request.username}_{request.session_id}"[:32],
        nasipaddress=request.nas_ip,
        acctstarttime=now if request.status_type == "Start" else None,
        acctstoptime=now if request.status_type == "Stop" else None,
        acctupdatetime=now,
        acctinputoctets=request.input_octets,
        acctoutputoctets=request.output_octets,
        acctsessiontime=request.session_time
    )
    
    # Veriyi kalıcı olarak PostgreSQL'e kaydediyoruz.
    db.add(new_acct)
    await db.commit()
    
    return {"status": "success"}