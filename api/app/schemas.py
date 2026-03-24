from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, Annotated
from pydantic.functional_validators import BeforeValidator

# Hata Yönetimi
def coerce_to_int(v: Any) -> int:
    if v is None or v == "":
        return 0
    return int(v)

# Sayısal alanlar için özel bir tip tanımlıyoruz.
FlexibleInt = Annotated[int, BeforeValidator(coerce_to_int)]

#KIMLIK DOGRULAMA SEMASI (AUTHENTICATION)
class AuthRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    # RADIUS öznitelikleri tire içerdiği için 'alias' kullanarak eşleştiriyoruz.
    username: str = Field(..., alias="User-Name")
    password: Optional[str] = Field(None, alias="User-Password")
    calling_station_id: Optional[str] = Field(None, alias="Calling-Station-Id")

# standart yanıt yapısı.
class RadiusResponse(BaseModel):
    status: str          
    attributes: Dict[str, str] = {} 

# HESAP YÖNETIMI SEMASI (ACCOUNTING)
class AccountingRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(..., alias="User-Name")
    status_type: str = Field(..., alias="Acct-Status-Type") # Start, Stop, Interim 
    session_id: str = Field(..., alias="Acct-Session-Id")
    nas_ip: str = Field(..., alias="NAS-IP-Address")
    
    # FlexibleInt kullanarak boş gelen trafik verilerini 0 olarak işliyoruz.
    input_octets: FlexibleInt = Field(0, alias="Acct-Input-Octets")    
    output_octets: FlexibleInt = Field(0, alias="Acct-Output-Octets") 
    session_time: FlexibleInt = Field(0, alias="Acct-Session-Time")   

# IZLEME SEMASI (MONITORING)
class UserInfo(BaseModel):
    # ORM modellerinden (SQLAlchemy) doğrudan veri çekebilmek için aktif ediyoruz.
    model_config = ConfigDict(from_attributes=True)
    username: str
    groupname: Optional[str] = None
    is_active: bool = False