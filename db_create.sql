-- Executed only once

CREATE DATABASE IF NOT EXISTS cpv;

CREATE USER IF NOT EXISTS `cpv`@`%`;
ALTER USER `cpv`@`%`IDENTIFIED BY ; --pass in keepass;
GRANT SELECT, INSERT, UPDATE, DELETE, DROP ON cpv.* TO `cpv`@`%`;
FLUSH PRIVILEGES;

-- if running on docker connect with hostname and port
-- mysql -h localhost -P 3306 --protocol=tcp -u cpv -p

CREATE TABLE `key_values` (
  `keyname` varchar(45) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`keyname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `params_main` (
  `emi_master` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `parameter` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `family` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `area` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dataformat` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`emi_master`,`parameter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `params_special` (
  `emi_master` varchar(8) NOT NULL,
  `emi_parent` varchar(8) NOT NULL,
  `emi_sub` varchar(8) NOT NULL,
  `parameter` varchar(30) NOT NULL,
  `subemi_name` varchar(30) NOT NULL,
  `description` varchar(45) NOT NULL,
  `groupid` int(11) NOT NULL,
  `area` varchar(12) NOT NULL,
  `family` varchar(30) NOT NULL,
  `agg_function` varchar(12) NOT NULL,
  `dataformat` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`emi_master`,`emi_parent`,`emi_sub`,`parameter`,`subemi_name`,`description`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `params_values` (
  `PO` varchar(10) NOT NULL,
  `family` varchar(30) NOT NULL,
  `area` varchar(12) NOT NULL,
  `parameter` varchar(64) NOT NULL,
  `value` varchar(30) NOT NULL,
  `unit` varchar(16) DEFAULT NULL,
  `inputdate` datetime NOT NULL,
  `value_min` varchar(30) DEFAULT NULL,
  `value_max` varchar(30) DEFAULT NULL,
  `tolerance_min` varchar(30) DEFAULT NULL,
  `tolerance_max` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`PO`,`family`,`area`,`parameter`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `process_orders` (
  `process_order` varchar(10) NOT NULL,
  `batch` varchar(12) NOT NULL,
  `material` varchar(12) NOT NULL,
  `description` varchar(256) NOT NULL,
  `launch_date` datetime NOT NULL,
  `order_quantity` decimal(10,0) NOT NULL,
  `order_unit` varchar(2) NOT NULL,
  PRIMARY KEY (`process_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

