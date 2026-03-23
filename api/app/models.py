# from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text
# from sqlalchemy.sql import func
# from .database import Base

# # 1. Kimlik Doğrulama Tablosu (Authentication)
# # PDF Madde 3.6 - radcheck: Kullanıcı kimlik bilgileri [cite: 63]
# class RadCheck(Base):
#     __tablename__ = "radcheck"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(64), nullable=False, index=True)
#     attribute = Column(String(64), nullable=False, default="Cleartext-Password") # Veya 'Crypt-Password'
#     op = Column(String(2), nullable=False, default="==")
#     value = Column(String(253), nullable=False) # Burada hashlenmiş şifre saklanacak 

# # 2. Kullanıcı Yanıt Tablosu
# # PDF Madde 3.6 - radreply: Kullanıcıya dönecek atribütler [cite: 64]
# class RadReply(Base):
#     __tablename__ = "radreply"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(64), nullable=False, index=True)
#     attribute = Column(String(64), nullable=False)
#     op = Column(String(2), nullable=False, default="=")
#     value = Column(String(253), nullable=False)

# # 3. Kullanıcı-Grup İlişkisi
# # PDF Madde 3.6 - radusergroup: Kullanıcı-grup eşleşmeleri [cite: 65]
# class RadUserGroup(Base):
#     __tablename__ = "radusergroup"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(64), nullable=False, index=True)
#     groupname = Column(String(64), nullable=False)
#     priority = Column(Integer, default=1)

# # 4. Grup Yanıt Tablosu (Authorization/VLAN)
# # PDF Madde 3.6 - radgroupreply: Grup bazlı atribütler (VLAN vb.) [cite: 66]
# class RadGroupReply(Base):
#     __tablename__ = "radgroupreply"

#     id = Column(Integer, primary_key=True, index=True)
#     groupname = Column(String(64), nullable=False, index=True)
#     attribute = Column(String(64), nullable=False) # Örn: Tunnel-Private-Group-Id
#     op = Column(String(2), nullable=False, default="=")
#     value = Column(String(253), nullable=False) # Örn: VLAN ID (10, 20 vb.)

# # 5. Hesap Yönetimi Tablosu (Accounting)
# # PDF Madde 3.4 - Oturum verileri, süreler ve veri miktarları [cite: 54, 67]
# class RadAcct(Base):
#     __tablename__ = "radacct"

#     radacctid = Column(BigInteger, primary_key=True, index=True)
#     acctsessionid = Column(String(64), nullable=False, default="")
#     acctuniqueid = Column(String(32), nullable=False, default="")
#     username = Column(String(64), nullable=False, index=True)
#     groupname = Column(String(64), nullable=False, default="")
#     nasipaddress = Column(String(15)) # Network Access Server IP [cite: 54]
#     nasportid = Column(String(32))
#     acctstarttime = Column(DateTime(timezone=True)) # Başlangıç zamanı [cite: 54]
#     acctupdatetime = Column(DateTime(timezone=True))
#     acctstoptime = Column(DateTime(timezone=True)) # Bitiş zamanı [cite: 54]
#     acctsessiontime = Column(BigInteger) # Toplam oturum süresi [cite: 54]
#     acctinputoctets = Column(BigInteger) # Gelen veri (Bytes) [cite: 54]
#     acctoutputoctets = Column(BigInteger) # Giden veri (Bytes) [cite: 54]
#     callingstationid = Column(String(50), nullable=False, default="") # MAC adresi (MAB için kritik) 
#     terminatecause = Column(String(32), nullable=False, default="")


from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from .database import Base

class RadCheck(Base):
    __tablename__ = "radcheck"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, index=True)
    attribute = Column(String(64), nullable=False, default="Cleartext-Password")
    op = Column(String(2), nullable=False, default="==")
    value = Column(String(253), nullable=False)

class RadUserGroup(Base):
    __tablename__ = "radusergroup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, index=True)
    groupname = Column(String(64), nullable=False)
    priority = Column(Integer, default=1)

class RadGroupReply(Base):
    __tablename__ = "radgroupreply"
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String(64), nullable=False, index=True)
    attribute = Column(String(64), nullable=False)
    op = Column(String(2), nullable=False, default="=")
    value = Column(String(253), nullable=False)

class RadAcct(Base):
    __tablename__ = "radacct"
    radacctid = Column(BigInteger, primary_key=True, index=True)
    acctsessionid = Column(String(64), nullable=False)
    acctuniqueid = Column(String(32), nullable=False)
    username = Column(String(64), nullable=False, index=True)
    groupname = Column(String(64), nullable=False, default="")
    nasipaddress = Column(String(15)) # INET yerine String (Hata önleyici) [cite: 54]
    acctstarttime = Column(DateTime(timezone=True))
    acctupdatetime = Column(DateTime(timezone=True))
    acctstoptime = Column(DateTime(timezone=True))
    acctsessiontime = Column(BigInteger)
    acctinputoctets = Column(BigInteger)
    acctoutputoctets = Column(BigInteger)