-- Executed only once

CREATE DATABASE IF NOT EXISTS cpv;

CREATE USER IF NOT EXISTS 'cpv'@'%';
ALTER USER 'cpv'@'%'IDENTIFIED BY ; --pass in keepass;
GRANT SELECT, INSERT, UPDATE, DELETE ON cpv.* TO 'cpv'@'%';
FLUSH PRIVILEGES;

-- if running on docker connect with hostname and port
-- mysql -h localhost -P 3306 --protocol=tcp -u cpv -p

CREATE TABLE IF NOT EXISTS `cpv`.`params_main` (
  `emi_master` VARCHAR(8) NOT NULL,
  `parameter` VARCHAR(30) NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `dataformat` VARCHAR(12) NULL,
  PRIMARY KEY (`emi_master`, `parameter`));

CREATE TABLE IF NOT EXISTS `cpv`.`params_taggers` (
  `emi_master` VARCHAR(8) NOT NULL,
  `emi_parent` VARCHAR(8) NOT NULL,
  `emi_sub` VARCHAR(8) NOT NULL,
  `parameter` VARCHAR(30) NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`emi_master`, `emi_parent`, `emi_sub`, `parameter`));

CREATE TABLE IF NOT EXISTS `cpv`.`params_aggregate` (
  `emi_master` VARCHAR(8) NOT NULL,
  `emi_parent` VARCHAR(8) NOT NULL,
  `emi_sub` VARCHAR(8) NOT NULL,
  `parameter` VARCHAR(30) NOT NULL,
  `groupid` INT NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `dataformat` VARCHAR(12) NULL,
  `function` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`emi_master`, `emi_parent`, `emi_sub`, `parameter`));


