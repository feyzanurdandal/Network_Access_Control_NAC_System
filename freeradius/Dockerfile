FROM freeradius/freeradius-server:latest-3.2

# 1. Kendi konfigürasyonlarımızı kopyala
COPY ./config/clients.conf /etc/freeradius/clients.conf
COPY ./config/sites-enabled/default /etc/freeradius/sites-enabled/default
COPY ./config/mods-enabled/rest /etc/freeradius/mods-enabled/rest

# 2. KRİTİK TEMİZLİK: EAP modülünü ve ona bağımlı olan inner-tunnel sitesini siliyoruz.
# Bunlar sertifika ve iç tünel hatalarına neden olan, projemizde kullanmadığımız eski dosyalardır.
RUN rm -f /etc/freeradius/mods-enabled/eap && \
    rm -f /etc/freeradius/sites-enabled/inner-tunnel

# 3. İZİN DÜZELTME: Klasörlere 755, dosyalara 644 izni vererek güvenlik/erişim sorunlarını çözüyoruz.
RUN find /etc/freeradius -type d -exec chmod 755 {} + && \
    find /etc/freeradius -type f -exec chmod 644 {} +