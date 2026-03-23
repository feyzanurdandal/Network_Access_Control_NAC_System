-- -- 1. Kimlik Doğrulama Tablosu (Authentication)
-- -- Kullanıcı adı ve şifrelerin/MAC adreslerinin tutulduğu yer
-- CREATE TABLE radcheck (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(64) NOT NULL DEFAULT '',
--     attribute VARCHAR(64) NOT NULL DEFAULT '',
--     op CHAR(2) NOT NULL DEFAULT '==',
--     value VARCHAR(253) NOT NULL DEFAULT ''
-- );
-- CREATE INDEX radcheck_username ON radcheck (username);

-- -- 2. Kullanıcı Yanıt Tablosu
-- -- Kullanıcıya özel dönülecek yanıtlar (Örn: özel bir mesaj)
-- CREATE TABLE radreply (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(64) NOT NULL DEFAULT '',
--     attribute VARCHAR(64) NOT NULL DEFAULT '',
--     op CHAR(2) NOT NULL DEFAULT '=',
--     value VARCHAR(253) NOT NULL DEFAULT ''
-- );

-- -- 3. Kullanıcı-Grup İlişkisi
-- -- Bir kullanıcının 'admin', 'employee' veya 'guest' olduğunu belirler
-- CREATE TABLE radusergroup (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(64) NOT NULL DEFAULT '',
--     groupname VARCHAR(64) NOT NULL DEFAULT '',
--     priority INT NOT NULL DEFAULT 1
-- );

-- -- 4. Grup Yanıt Tablosu (Authorization/VLAN)
-- -- Örn: 'guest' grubuna VLAN 10, 'admin' grubuna VLAN 20 ataması burada yapılır
-- CREATE TABLE radgroupreply (
--     id SERIAL PRIMARY KEY,
--     groupname VARCHAR(64) NOT NULL DEFAULT '',
--     attribute VARCHAR(64) NOT NULL DEFAULT '',
--     op CHAR(2) NOT NULL DEFAULT '=',
--     value VARCHAR(253) NOT NULL DEFAULT ''
-- );

-- -- 5. Hesap Yönetimi Tablosu (Accounting)
-- -- Kim ne kadar süre bağlı kaldı, ne kadar veri indirdi/yükledi?
-- CREATE TABLE radacct (
--     radacctid BIGSERIAL PRIMARY KEY,
--     acctsessionid VARCHAR(64) NOT NULL DEFAULT '',
--     acctuniqueid VARCHAR(32) NOT NULL DEFAULT '',
--     username VARCHAR(64) NOT NULL DEFAULT '',
--     groupname VARCHAR(64) NOT NULL DEFAULT '',
--     nasipaddress VARCHAR(15),
--     nasportid VARCHAR(32) DEFAULT NULL,
--     acctstarttime TIMESTAMP WITH TIME ZONE,
--     acctupdatetime TIMESTAMP WITH TIME ZONE,
--     acctstoptime TIMESTAMP WITH TIME ZONE,
--     acctsessiontime BIGINT DEFAULT NULL,
--     acctauthentic VARCHAR(32) DEFAULT NULL,
--     acctinputoctets BIGINT DEFAULT NULL,
--     acctoutputoctets BIGINT DEFAULT NULL,
--     calledstationid VARCHAR(50) NOT NULL DEFAULT '',
--     callingstationid VARCHAR(50) NOT NULL DEFAULT '',
--     terminatecause VARCHAR(32) NOT NULL DEFAULT ''
-- );

CREATE TABLE radcheck (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    attribute VARCHAR(64) NOT NULL DEFAULT 'Cleartext-Password',
    op CHAR(2) NOT NULL DEFAULT '==',
    value VARCHAR(253) NOT NULL
);

CREATE TABLE radusergroup (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL,
    groupname VARCHAR(64) NOT NULL,
    priority INT NOT NULL DEFAULT 1
);

CREATE TABLE radgroupreply (
    id SERIAL PRIMARY KEY,
    groupname VARCHAR(64) NOT NULL,
    attribute VARCHAR(64) NOT NULL,
    op CHAR(2) NOT NULL DEFAULT '=',
    value VARCHAR(253) NOT NULL
);

CREATE TABLE radacct (
    radacctid BIGSERIAL PRIMARY KEY,
    acctsessionid VARCHAR(64) NOT NULL,
    acctuniqueid VARCHAR(32) NOT NULL,
    username VARCHAR(64) NOT NULL,
    groupname VARCHAR(64) DEFAULT '',
    nasipaddress VARCHAR(15), -- INET yerine VARCHAR [cite: 54]
    acctstarttime TIMESTAMP WITH TIME ZONE,
    acctupdatetime TIMESTAMP WITH TIME ZONE,
    acctstoptime TIMESTAMP WITH TIME ZONE,
    acctsessiontime BIGINT,
    acctinputoctets BIGINT,
    acctoutputoctets BIGINT
);