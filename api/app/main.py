# from fastapi import FastAPI, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# import redis.asyncio as redis
# import os
# from passlib.context import CryptContext

# from .database import get_db
# from . import models, schemas

# app = FastAPI(title="S3M NAC Policy Engine")

# # Şifre Hashing Ayarları (PDF Madde 3.3 uyarınca plaintext yasaktır)
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Redis Bağlantısı (Rate-limiting ve session cache için)
# redis_client = redis.from_url(
#     f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379/0", 
#     encoding="utf-8", 
#     decode_responses=True
# )

# # 1. AUTHENTICATION (Kimlik Doğrulama)
# @app.post("/auth", response_model=schemas.RadiusResponse)
# async def authenticate(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
#     # Rate Limiting Kontrolü (PDF Madde 3.2)
#     retry_key = f"retries:{request.username}"
#     retries = await redis_client.get(retry_key)
#     if retries and int(retries) >= 5:
#         return {"status": "reject", "attributes": {"Reply-Message": "Too many failed attempts"}}

#     # Veritabanında kullanıcıyı ara
#     result = await db.execute(select(models.RadCheck).where(models.RadCheck.username == request.username))
#     user = result.scalars().first()

#     if not user:
#         # MAB Kontrolü (Eğer şifre yoksa MAC adresiyle kontrol et)
#         if request.calling_station_id:
#             # Burada MAC tablosu kontrol edilebilir, basitlik için reject dönüyoruz
#             return {"status": "reject", "attributes": {"Reply-Message": "Unknown Device"}}
#         return {"status": "reject", "attributes": {"Reply-Message": "User not found"}}

#     # Şifre Doğrulama (Bcrypt)
#     if not pwd_context.verify(request.password, user.value):
#         await redis_client.incr(retry_key)
#         await redis_client.expire(retry_key, 300) # 5 dakika blokla
#         return {"status": "reject", "attributes": {"Reply-Message": "Invalid credentials"}}

#     # Başarılı giriş: Retry sayacını sıfırla
#     await redis_client.delete(retry_key)
#     return {"status": "accept", "attributes": {"Reply-Message": f"Welcome {request.username}"}}

# # 2. AUTHORIZATION (Yetkilendirme - VLAN Atama)
# @app.post("/authorize", response_model=schemas.RadiusResponse)
# async def authorize(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
#     # Kullanıcının grubunu bul (admin, employee, guest)
#     group_query = await db.execute(
#         select(models.RadUserGroup).where(models.RadUserGroup.username == request.username)
#     )
#     user_group = group_query.scalars().first()
    
#     group_name = user_group.groupname if user_group else "guest"

#     # Gruba ait VLAN ve politika özniteliklerini getir (PDF Madde 3.3)
#     attrs_query = await db.execute(
#         select(models.RadGroupReply).where(models.RadGroupReply.groupname == group_name)
#     )
#     group_attrs = attrs_query.scalars().all()

#     response_attrs = {attr.attribute: attr.value for attr in group_attrs}
#     return {"status": "accept", "attributes": response_attrs}

# # 3. ACCOUNTING (Hesap Yönetimi)
# @app.post("/accounting")
# async def accounting(request: schemas.AccountingRequest, db: AsyncSession = Depends(get_db)):
#     # Yeni oturum kaydı veya güncelleme (PDF Madde 3.4)
#     new_acct = models.RadAcct(
#         username=request.username,
#         acctsessionid=request.session_id,
#         nasipaddress=request.nas_ip,
#         acctstarttime=None if request.status_type != "Start" else "now()", # Örnek mantık
#         acctinputoctets=request.input_octets,
#         acctoutputoctets=request.output_octets,
#         acctsessiontime=request.session_time
#     )
#     db.add(new_acct)
    
#     # Aktif oturumu Redis'te sakla (PDF Madde 3.4)
#     session_key = f"active_session:{request.username}"
#     if request.status_type in ["Start", "Interim-Update"]:
#         await redis_client.set(session_key, request.session_id, ex=3600)
#     else:
#         await redis_client.delete(session_key)

#     await db.commit()
#     return {"status": "success"}

# # 4. MONITORING (Kullanıcı ve Oturum Sorgulama)
# @app.get("/users")
# async def list_users(db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(models.RadCheck))
#     return result.scalars().all()

# @app.get("/sessions/active")
# async def active_sessions():
#     keys = await redis_client.keys("active_session:*")
#     return {"active_sessions_count": len(keys), "users": [k.split(":")[1] for k in keys]}


from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import redis.asyncio as redis
import os
from passlib.context import CryptContext

from .database import get_db
from . import models, schemas

app = FastAPI(title="S3M NAC Policy Engine")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

redis_client = redis.from_url(
    f"redis://:{os.getenv('REDIS_PASSWORD')}@redis:6379/0", 
    decode_responses=True
)

@app.post("/auth", response_model=schemas.RadiusResponse)
async def authenticate(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.RadCheck).where(models.RadCheck.username == request.username))
    user = result.scalars().first()
    if not user or not pwd_context.verify(request.password, user.value):
        return {"status": "reject", "attributes": {"Reply-Message": "Giris Basarisiz"}}
    return {"status": "accept", "attributes": {"Reply-Message": "Hos geldiniz"}}

@app.post("/authorize", response_model=schemas.RadiusResponse)
async def authorize(request: schemas.AuthRequest, db: AsyncSession = Depends(get_db)):
    group_query = await db.execute(select(models.RadUserGroup).where(models.RadUserGroup.username == request.username))
    user_group = group_query.scalars().first()
    group_name = user_group.groupname if user_group else "guest"
    
    attrs_query = await db.execute(select(models.RadGroupReply).where(models.RadGroupReply.groupname == group_name))
    response_attrs = {attr.attribute: attr.value for attr in attrs_query.scalars().all()}
    return {"status": "accept", "attributes": response_attrs}

@app.post("/accounting")
async def accounting(request: schemas.AccountingRequest, db: AsyncSession = Depends(get_db)):
    # KRITIK: 'now()' yerine Python datetime nesnesi gönderiliyor
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
    db.add(new_acct)
    await db.commit()
    return {"status": "success"}