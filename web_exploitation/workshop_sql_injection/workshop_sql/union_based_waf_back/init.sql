CREATE DATABASE IF NOT EXISTS ctfdb;
USE ctfdb;

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    description VARCHAR(255)
);

INSERT INTO products (name, description) VALUES
    ('Rubber Duck', 'A classic debugging companion'),
    ('Mechanical Keyboard', 'Clicky and satisfying'),
    ('Coffee Mug', 'CTF enjoyer, caffeine addict edition');

-- Secret table the player must reach via UNION SELECT, in a DIFFERENT
-- table so it can't be dumped by querying `products` alone.
CREATE TABLE IF NOT EXISTS secret_flags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    flag VARCHAR(255)
);

INSERT INTO secret_flags (flag) VALUES ('SC2{uN10n_byp4ss3s_w3ak_w4f_f1lt3rs}');

CREATE USER IF NOT EXISTS 'ctfuser'@'%' IDENTIFIED BY 'ctfpass';
GRANT ALL PRIVILEGES ON ctfdb.* TO 'ctfuser'@'%';
FLUSH PRIVILEGES;