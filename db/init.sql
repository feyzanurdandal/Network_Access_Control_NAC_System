-- Kimlik Doğrulama Tablosu (Authentication)
-- Kullanıcıların sisteme giriş yaparken kullanılacak kimlik bilgilerini (şifre, MAC vb.) tutar.
CREATE TABLE radcheck (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,            
    attribute VARCHAR(64) NOT NULL DEFAULT 'Cleartext-Password', 
    op CHAR(2) NOT NULL DEFAULT '==',          
    value VARCHAR(253) NOT NULL                
);

-- Kullanıcı-Grup İlişkisi (Authorization)
-- Hangi kullanıcının hangi role (Admin, Guest, Employee) sahip olduğunu belirler.
CREATE TABLE radusergroup (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,      
    groupname VARCHAR(64) NOT NULL,         
    priority INT NOT NULL DEFAULT 1            
);

-- Grup Yanıt Tablosu (Authorization - VLAN Atama)
-- Gruplara atanacak ağ politikalarını tutar.
CREATE TABLE radgroupreply (
    id SERIAL PRIMARY KEY,
    groupname VARCHAR(64) NOT NULL,     
    attribute VARCHAR(64) NOT NULL,           
    op CHAR(2) NOT NULL DEFAULT '=',            
    value VARCHAR(253) NOT NULL                 
);

-- Hesap Yönetimi Tablosu (Accounting)
-- Oturum verilerini, süreleri ve trafik miktarını kayıt altına alır.
CREATE TABLE radacct (
    radacctid BIGSERIAL PRIMARY KEY,      
    acctsessionid VARCHAR(64) NOT NULL,        
    acctuniqueid VARCHAR(32) NOT NULL,     
    username VARCHAR(64) NOT NULL,         
    groupname VARCHAR(64) DEFAULT '',           
    nasipaddress VARCHAR(15),                 
    acctstarttime TIMESTAMP WITH TIME ZONE,   
    acctupdatetime TIMESTAMP WITH TIME ZONE,   
    acctstoptime TIMESTAMP WITH TIME ZONE,  
    acctsessiontime BIGINT,                  
    acctinputoctets BIGINT,          
    acctoutputoctets BIGINT            
);