USE [master]
GO

/****** Object:  Database [cpv_dev]    Script Date: 14/08/2019 15:11:42 ******/
CREATE DATABASE [cpv_dev]
 CONTAINMENT = NONE
 ON  PRIMARY
( NAME = N'cpv_dev', FILENAME = N'/var/opt/mssql/data/cpv_dev.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON
( NAME = N'cpv_dev_log', FILENAME = N'/var/opt/mssql/data/cpv_dev_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [cpv_dev].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [cpv_dev] SET ANSI_NULL_DEFAULT OFF
GO

ALTER DATABASE [cpv_dev] SET ANSI_NULLS OFF
GO

ALTER DATABASE [cpv_dev] SET ANSI_PADDING OFF
GO

ALTER DATABASE [cpv_dev] SET ANSI_WARNINGS OFF
GO

ALTER DATABASE [cpv_dev] SET ARITHABORT OFF
GO

ALTER DATABASE [cpv_dev] SET AUTO_CLOSE ON
GO

ALTER DATABASE [cpv_dev] SET AUTO_SHRINK ON
GO

ALTER DATABASE [cpv_dev] SET AUTO_UPDATE_STATISTICS ON
GO

ALTER DATABASE [cpv_dev] SET CURSOR_CLOSE_ON_COMMIT OFF
GO

ALTER DATABASE [cpv_dev] SET CURSOR_DEFAULT  GLOBAL
GO

ALTER DATABASE [cpv_dev] SET CONCAT_NULL_YIELDS_NULL OFF
GO

ALTER DATABASE [cpv_dev] SET NUMERIC_ROUNDABORT OFF
GO

ALTER DATABASE [cpv_dev] SET QUOTED_IDENTIFIER OFF
GO

ALTER DATABASE [cpv_dev] SET RECURSIVE_TRIGGERS OFF
GO

ALTER DATABASE [cpv_dev] SET  DISABLE_BROKER
GO

ALTER DATABASE [cpv_dev] SET AUTO_UPDATE_STATISTICS_ASYNC OFF
GO

ALTER DATABASE [cpv_dev] SET DATE_CORRELATION_OPTIMIZATION OFF
GO

ALTER DATABASE [cpv_dev] SET TRUSTWORTHY OFF
GO

ALTER DATABASE [cpv_dev] SET ALLOW_SNAPSHOT_ISOLATION OFF
GO

ALTER DATABASE [cpv_dev] SET PARAMETERIZATION SIMPLE
GO

ALTER DATABASE [cpv_dev] SET READ_COMMITTED_SNAPSHOT OFF
GO

ALTER DATABASE [cpv_dev] SET HONOR_BROKER_PRIORITY OFF
GO

ALTER DATABASE [cpv_dev] SET RECOVERY FULL
GO

ALTER DATABASE [cpv_dev] SET  MULTI_USER
GO

ALTER DATABASE [cpv_dev] SET PAGE_VERIFY CHECKSUM
GO

ALTER DATABASE [cpv_dev] SET DB_CHAINING OFF
GO

ALTER DATABASE [cpv_dev] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF )
GO

ALTER DATABASE [cpv_dev] SET TARGET_RECOVERY_TIME = 60 SECONDS
GO

ALTER DATABASE [cpv_dev] SET DELAYED_DURABILITY = DISABLED
GO

ALTER DATABASE [cpv_dev] SET QUERY_STORE = OFF
GO

ALTER DATABASE [cpv_dev] SET  READ_WRITE
GO

USE [cpv_dev]
GO






/****** Object:  Table [dbo].[key_values]    Script Date: 14/08/2019 15:16:10 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[key_values](
	[keyname] [varchar](45) NOT NULL,
	[value] [varchar](45) NULL,
PRIMARY KEY CLUSTERED
(
	[keyname] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[key_values] ADD  DEFAULT (NULL) FOR [value]
GO





USE [cpv_dev]
GO

/****** Object:  Table [dbo].[params_main]    Script Date: 14/08/2019 15:29:17 ******/
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







USE [cpv_dev]
GO

/****** Object:  Table [dbo].[params_special]    Script Date: 14/08/2019 15:29:33 ******/
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
	[description] [varchar](256) NOT NULL,
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






USE [cpv_dev]
GO

/****** Object:  Table [dbo].[params_values]    Script Date: 14/08/2019 15:29:47 ******/
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









USE [cpv_dev]
GO

/****** Object:  Table [dbo].[process_orders]    Script Date: 19/08/2019 16:04:09 ******/
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
	[order_quantity] [decimal](10, 0) NOT NULL,
	[order_unit] [varchar](2) NOT NULL,
	[strength] [decimal](10, 0) NULL,
PRIMARY KEY CLUSTERED
(
	[process_order] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO












