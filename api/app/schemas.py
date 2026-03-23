# from pydantic import BaseModel, Field
# from typing import Optional, List, Dict

# # 1. Kimlik Doğrulama İsteği (Authentication Request)
# # FreeRADIUS /auth endpoint'ine bu formatta veri gönderir
# class AuthRequest(BaseModel):
#     username: str = Field(..., alias="User-Name")
#     password: Optional[str] = Field(None, alias="User-Password")
#     calling_station_id: Optional[str] = Field(None, alias="Calling-Station-Id") # MAB için MAC adresi

#     class Config:
#         populate_by_name = True

# # 2. Yetkilendirme ve Yanıt (Auth/Authorize Response)
# # Başarılı girişte FreeRADIUS'a döneceğimiz veriler
# class RadiusResponse(BaseModel):
#     status: str # "accept" veya "reject"
#     attributes: Dict[str, str] = {} # Örn: {"Tunnel-Private-Group-Id": "10"}

# # 3. Hesap Yönetimi İsteği (Accounting Request)
# # PDF Madde 3.4 - Oturum verilerinin işlenmesi için
# class AccountingRequest(BaseModel):
#     username: str = Field(..., alias="User-Name")
#     status_type: str = Field(..., alias="Acct-Status-Type") # Start, Interm-Update, Stop
#     session_id: str = Field(..., alias="Acct-Session-Id")
#     nas_ip: str = Field(..., alias="NAS-IP-Address")
#     input_octets: int = Field(0, alias="Acct-Input-Octets")
#     output_octets: int = Field(0, alias="Acct-Output-Octets")
#     session_time: int = Field(0, alias="Acct-Session-Time")

#     class Config:
#         populate_by_name = True

# # 4. Kullanıcı Görüntüleme (API Dışa Aktarım)
# # PDF Madde 3.5 - /users ve /sessions/active için
# class UserInfo(BaseModel):
#     username: str
#     group: Optional[str] = None
#     is_active: bool = False

#     class Config:
#         from_attributes = True


from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, Annotated
from pydantic.functional_validators import BeforeValidator

# Boş metinleri ("") veya None değerlerini 0'a çeviren yardımcı fonksiyon
def coerce_to_int(v: Any) -> int:
    if v is None or v == "":
        return 0
    return int(v)

FlexibleInt = Annotated[int, BeforeValidator(coerce_to_int)]

class AuthRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    username: str = Field(..., alias="User-Name")
    password: Optional[str] = Field(None, alias="User-Password")
    calling_station_id: Optional[str] = Field(None, alias="Calling-Station-Id")

class RadiusResponse(BaseModel):
    status: str 
    attributes: Dict[str, str] = {}

class AccountingRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    username: str = Field(..., alias="User-Name")
    status_type: str = Field(..., alias="Acct-Status-Type")
    session_id: str = Field(..., alias="Acct-Session-Id")
    nas_ip: str = Field(..., alias="NAS-IP-Address")
    input_octets: FlexibleInt = Field(0, alias="Acct-Input-Octets")
    output_octets: FlexibleInt = Field(0, alias="Acct-Output-Octets")
    session_time: FlexibleInt = Field(0, alias="Acct-Session-Time")

class UserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    groupname: Optional[str] = None
    is_active: bool = False
