# Network Access Control (NAC) System with AAA Architecture

Bu proje, staj değerlendirme ödevi kapsamında geliştirilmiş; RADIUS protokolünü kullanarak temel düzeyde çalışan bir **Network Access Control (NAC)** sistemidir[cite: 11]. Sistem; kimlik doğrulama (Authentication), yetkilendirme (Authorization) ve hesap yönetimi (Accounting) süreçlerini merkezi bir **Policy Engine** üzerinden yönetir.

## Kullanılan Teknolojiler

Tüm altyapı Docker Compose ile orkestre edilmektedir:
* **FreeRADIUS 3.2-server:** RADIUS sunucusu; Auth, Authz ve Acct portlarını yönetir.
* **FastAPI (Python 3.13):** RESTful Policy Engine olarak görev yapar.
* **PostgreSQL 18-alpine:** Kullanıcı, NAS ve accounting verilerinin saklandığı ilişkisel veritabanı.
* **Redis 8-alpine:** Oturum önbellekleme ve rate-limiting mekanizması.

##  Öne Çıkan Özellikler

* **Güvenli Kimlik Doğrulama:** Kullanıcı şifreleri Bcrypt algoritması ile hash'lenerek saklanır (Plaintext kabul edilmez).
* **Dinamik Yetkilendirme:** Kullanıcı gruplarına (admin, employee, guest) göre otomatik VLAN ataması yapılır.
* **Gelişmiş Accounting:** Oturum başlangıç, ara ve bitiş paketleri işlenerek veri tüketimi (octets) ve süre takibi yapılır.
* **Rate-Limiting:** Hatalı giriş denemelerine karşı Redis tabanlı koruma sağlanır.
* **Konteyner Orkestrasyonu:** Servisler arası iletişim dedicated ağ, healthcheck ve volume mount yapıları ile yönetilir.

##  Kurulum ve Çalıştırma

Sistemi ayağa kaldırmak için bilgisayarınızda Docker ve Docker Compose yüklü olmalıdır.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/feyzanurdandal/Network_Access_Control_NAC_System.git](https://github.com/feyzanurdandal/Network_Access_Control_NAC_System.git)
    cd Network_Access_Control_NAC_System
    ```

2.  **Yapılandırma (.env):**
    `.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değişkenleri tanımlayın.
    ```bash
    cp .env.example .env
    ```

3.  **Sistemi Başlatın:**
    Aşağıdaki komut ile tüm servisleri (Postgres, Redis, API, FreeRADIUS) ayağa kaldırın:
    ```bash
    docker-compose up -d --build
    ```

## Test Senaryoları

Sistem, FreeRADIUS ile birlikte gelen araçlar kullanılarak test edilebilir:

* **Authentication (PAP) Testi:**
    ```bash
    docker exec -it nac_freeradius radtest kullanici sifre localhost 0 testing123
    ```

* **Accounting (Start/Stop) Testi:**
    ```bash
    echo "User-Name=[kullanici],Acct-Status-Type=Start,Acct-Session-Id=123,NAS-IP-Address=127.0.0.1" | docker exec -i nac_freeradius radclient -x localhost:1813 acct testing123
    ```

## API Endpoints

FastAPI Policy Engine üzerinden aşağıdaki uç noktalara erişilebilir:

* `POST /auth`: Kullanıcı doğrulama ve sonuç dönme.
* `POST /authorize`: VLAN ve yetkilendirme öznitelikleri dönme.
* `POST /accounting`: Oturum verisi kaydetme (PostgreSQL).
* `GET /users`: Kullanıcı listesi ve durum bilgisi.
* `GET /sessions/active`: Aktif oturumları sorgulama (Redis).

##  Proje Yapısı

```text
.
├── api/                # FastAPI Uygulaması (Dockerfile, app/, requirements.txt)
├── db/                 # Veritabanı (init.sql)
├── freeradius/         # FreeRADIUS Konfigürasyonları ve Dockerfile
├── docs/               # Mimari Diyagramlar
├── docker-compose.yml  # Mikroservis Orkestrasyonu
└── .env.example        # Örnek Environment Variables