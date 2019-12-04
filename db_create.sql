-- Executed only once

CREATE DATABASE IF NOT EXISTS cpv;

CREATE USER IF NOT EXISTS `cpv`@`%`;
ALTER USER `cpv`@`%`IDENTIFIED BY ; --pass in keepass;
GRANT SELECT, INSERT, UPDATE, DELETE, DROP ON cpv.* TO `cpv`@`%`;
FLUSH PRIVILEGES;

-- if running on docker connect with hostname and port
-- mysql -h localhost -P 3306 --protocol=tcp -u cpv -p

USE [cpv]
GO

CREATE TABLE `key_values` (
  `keyname` varchar(45) NOT NULL,
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`keyname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

USE [cpv]
GO

ALTER TABLE [dbo].[params_main] DROP CONSTRAINT [DF__params_ma__dataf__398D8EEE]
GO

/****** Object:  Table [dbo].[params_main]    Script Date: 10/09/2019 12:33:03 ******/
DROP TABLE [dbo].[params_main]
GO

/****** Object:  Table [dbo].[params_main]    Script Date: 10/09/2019 12:33:03 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[params_main](
	[emi_master] [varchar](8) NOT NULL,
	[parameter] [varchar](30) NOT NULL,
	[family] [varchar](30) NOT NULL,
	[area] [varchar](12) NOT NULL,
	[description] [varchar](45) NOT NULL,
	[dataformat] [varchar](12) NULL,
PRIMARY KEY CLUSTERED 
(
	[emi_master] ASC,
	[parameter] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[params_main] ADD  DEFAULT (NULL) FOR [dataformat]
GO

ALTER TABLE [dbo].[params_special] DROP CONSTRAINT [DF__params_sp__dataf__3C69FB99]
GO

/****** Object:  Table [dbo].[params_special]    Script Date: 10/09/2019 12:33:27 ******/
DROP TABLE [dbo].[params_special]
GO

/****** Object:  Table [dbo].[params_special]    Script Date: 10/09/2019 12:33:27 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[params_special](
	[emi_master] [varchar](8) NOT NULL,
	[emi_parent] [varchar](8) NOT NULL,
	[emi_sub] [varchar](8) NOT NULL,
	[parameter] [varchar](30) NOT NULL,
	[subemi_name] [varchar](30) NOT NULL,
	[description] [varchar](45) NOT NULL,
	[groupid] [int] NOT NULL,
	[area] [varchar](12) NOT NULL,
	[family] [varchar](30) NOT NULL,
	[agg_function] [varchar](12) NOT NULL,
	[dataformat] [varchar](12) NULL,
PRIMARY KEY CLUSTERED 
(
	[emi_master] ASC,
	[emi_parent] ASC,
	[emi_sub] ASC,
	[parameter] ASC,
	[subemi_name] ASC,
	[description] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[params_special] ADD  DEFAULT (NULL) FOR [dataformat]
GO

ALTER TABLE [dbo].[params_values] DROP CONSTRAINT [DF__params_va__toler__4D94879B]
GO

ALTER TABLE [dbo].[params_values] DROP CONSTRAINT [DF__params_va__toler__4CA06362]
GO

ALTER TABLE [dbo].[params_values] DROP CONSTRAINT [DF__params_va__value__4BAC3F29]
GO

ALTER TABLE [dbo].[params_values] DROP CONSTRAINT [DF__params_va__value__4AB81AF0]
GO

ALTER TABLE [dbo].[params_values] DROP CONSTRAINT [DF__params_val__unit__49C3F6B7]
GO

/****** Object:  Table [dbo].[params_values]    Script Date: 10/09/2019 12:33:41 ******/
DROP TABLE [dbo].[params_values]
GO

/****** Object:  Table [dbo].[params_values]    Script Date: 10/09/2019 12:33:41 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[params_values](
	[PO] [varchar](10) NOT NULL,
	[family] [varchar](30) NOT NULL,
	[area] [varchar](12) NOT NULL,
	[parameter] [varchar](64) NOT NULL,
	[value] [varchar](30) NOT NULL,
	[unit] [varchar](16) NULL,
	[inputdate] [datetime] NOT NULL,
	[value_min] [varchar](30) NULL,
	[value_max] [varchar](30) NULL,
	[tolerance_min] [varchar](30) NULL,
	[tolerance_max] [varchar](30) NULL,
PRIMARY KEY CLUSTERED 
(
	[PO] ASC,
	[family] ASC,
	[area] ASC,
	[parameter] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[params_values] ADD  DEFAULT (NULL) FOR [unit]
GO

ALTER TABLE [dbo].[params_values] ADD  DEFAULT (NULL) FOR [value_min]
GO

ALTER TABLE [dbo].[params_values] ADD  DEFAULT (NULL) FOR [value_max]
GO

ALTER TABLE [dbo].[params_values] ADD  DEFAULT (NULL) FOR [tolerance_min]
GO

ALTER TABLE [dbo].[params_values] ADD  DEFAULT (NULL) FOR [tolerance_max]
GO

/****** Object:  Table [dbo].[process_orders]    Script Date: 10/09/2019 12:34:14 ******/
DROP TABLE [dbo].[process_orders]
GO

/****** Object:  Table [dbo].[process_orders]    Script Date: 10/09/2019 12:34:14 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[process_orders](
	[process_order] [varchar](10) NOT NULL,
	[batch] [varchar](12) NOT NULL,
	[material] [varchar](12) NOT NULL,
	[description] [varchar](256) NOT NULL,
	[launch_date] [datetime] NOT NULL,
	[dom] [datetime] NOT NULL,
	[order_quantity] [decimal](12, 4) NOT NULL,
	[order_unit] [varchar](2) NOT NULL,
	[strength] [varchar](16) NULL,
PRIMARY KEY CLUSTERED 
(
	[process_order] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



