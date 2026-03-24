from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from .database import Base

# 1. KIMLIK DOGRULAMA (AUTHENTICATION) TABLOSU
# Bu model, RADIUS sunucusunun kullanıcıyı tanımak için baktığı ilk yerdir.
class RadCheck(Base):
    __tablename__ = "radcheck"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, index=True)
    attribute = Column(String(64), nullable=False, default="Cleartext-Password") 
    op = Column(String(2), nullable=False, default="==") 
    value = Column(String(253), nullable=False) 

#2. KULLANICI-GRUP ILISKISI (AUTHORIZATION)
# Kullanıcının hangi yetki seviyesine (Admin, Guest vb.) sahip olduğunu belirler.
class RadUserGroup(Base):
    __tablename__ = "radusergroup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, index=True) 
    groupname = Column(String(64), nullable=False) 
    priority = Column(Integer, default=1) 

# 3. GRUP YANIT TABLOSU (AUTHORIZATION - VLAN ATAMA)
# Gruplara atanacak dinamik ag politikalarının (VLAN ID gibi) tanımlandıgı yerdir.
class RadGroupReply(Base):
    __tablename__ = "radgroupreply"
    id = Column(Integer, primary_key=True, index=True)
    groupname = Column(String(64), nullable=False, index=True) 
    attribute = Column(String(64), nullable=False)
    op = Column(String(2), nullable=False, default="=") 
    value = Column(String(253), nullable=False) 

# 4. HESAP YÖNETIMI TABLOSU (ACCOUNTING)
# Ag kullanım verilerini ve oturum detaylarını saklayan denetim (audit) logudur.
class RadAcct(Base):
    __tablename__ = "radacct"
    radacctid = Column(BigInteger, primary_key=True, index=True)
    acctsessionid = Column(String(64), nullable=False) 
    acctuniqueid = Column(String(32), nullable=False) 
    username = Column(String(64), nullable=False, index=True) 
    groupname = Column(String(64), nullable=False, default="") 
    nasipaddress = Column(String(15)) 
    acctstarttime = Column(DateTime(timezone=True)) 
    acctupdatetime = Column(DateTime(timezone=True)) 
    acctstoptime = Column(DateTime(timezone=True)) 
    acctsessiontime = Column(BigInteger) 
    acctinputoctets = Column(BigInteger) 
    acctoutputoctets = Column(BigInteger) 