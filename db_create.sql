-- Executed only once

CREATE DATABASE IF NOT EXISTS cpv;

CREATE USER IF NOT EXISTS `cpv`@`%`;
ALTER USER `cpv`@`%`IDENTIFIED BY ; --pass in keepass;
GRANT SELECT, INSERT, UPDATE, DELETE, DROP ON cpv.* TO `cpv`@`%`;
FLUSH PRIVILEGES;

-- if running on docker connect with hostname and port
-- mysql -h localhost -P 3306 --protocol=tcp -u cpv -p

CREATE TABLE `cpv`.`key_values` (
  `key` VARCHAR(18) NOT NULL,
  `value` VARCHAR(45) NULL,
  PRIMARY KEY (`key`));


CREATE TABLE IF NOT EXISTS `cpv`.`params_main` (
  `emi_master` VARCHAR(8) NOT NULL,
  `parameter` VARCHAR(30) NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `dataformat` VARCHAR(12) NULL,
  `range_min` DECIMAL NOT NULL,
  `range_max` DECIMAL NOT NULL,
  PRIMARY KEY (`emi_master`, `parameter`));

CREATE TABLE IF NOT EXISTS `cpv`.`params_special` (
  `emi_master` VARCHAR(8) NOT NULL,
  `emi_parent` VARCHAR(8) NOT NULL,
  `emi_sub` VARCHAR(8) NOT NULL,
  `parameter` VARCHAR(30) NOT NULL,
  `subemi_name` VARCHAR(30) NOT NULL,
  `groupid` INT NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  `description` VARCHAR(45) NOT NULL,
  `agg_function` VARCHAR(12) NOT NULL,
  `dataformat` VARCHAR(12) NULL,
  `range_min` DECIMAL NOT NULL,
  `range_max` DECIMAL NOT NULL,
  PRIMARY KEY (`emi_master`, `emi_parent`, `emi_sub`, `parameter`, `subemi_name`));

CREATE TABLE IF NOT EXISTS `cpv`.`params_values` (
  `PO` VARCHAR(10) NOT NULL,
  `family` VARCHAR(30) NOT NULL,
  `area` VARCHAR(12) NOT NULL,
  `parameter` VARCHAR(64) NOT NULL,
  `value` VARCHAR(30) NOT NULL,
  `unit` VARCHAR(16) NULL,
  `inputdate` DATETIME NOT NULL,
  `range_min` DECIMAL NOT NULL,
  `range_max` DECIMAL NOT NULL,
  PRIMARY KEY (`PO`, `family`, `area`, `parameter`));

CREATE TABLE `cpv`.`process_orders` (
  `process_order` VARCHAR(10) NOT NULL,
  `batch` VARCHAR(12) NOT NULL,
  `material` VARCHAR(12) NOT NULL,
  `description` VARCHAR(256) NOT NULL,
  `launch_date` DATETIME NOT NULL,
  `order_quantity` DECIMAL NOT NULL,
  `order_unit` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`process_order`));