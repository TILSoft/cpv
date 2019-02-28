-- Executed only once

CREATE DATABASE IF NOT EXISTS cpv;

CREATE USER IF NOT EXISTS 'cpv'@'localhost';
ALTER USER 'cpv'@'localhost'IDENTIFIED BY ; --needs password added;
GRANT SELECT, INSERT, DELETE ON cpv.* TO 'cpv'@'localhost';
FLUSH PRIVILEGES;

-- if running on docker connect with hostname and port
-- mysql -h localhost -P 3306 --protocol=tcp -u cpv -p

