IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Socket_TyGiaVang')
BEGIN
	CREATE DATABASE Socket_TyGiaVang;
END

GO
USE Socket_TyGiaVang
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Account')
BEGIN
	CREATE TABLE Account(
		username nvarchar(50) NOT NULL,
		password nvarchar(50) NOT NULL
	);
END

DECLARE @json_today nvarchar(max)
DECLARE @json_1		nvarchar(max)
DECLARE @json_2		nvarchar(max)
DECLARE @json_3		nvarchar(max)
DECLARE @json_4		nvarchar(max)
DECLARE @json_5		nvarchar(max)
DECLARE @json_6		nvarchar(max)
DECLARE @json_7		nvarchar(max)
DECLARE @json_8		nvarchar(max)
DECLARE @json_9		nvarchar(max)
DECLARE @json_10	nvarchar(max)

-- Thay duong dan toi cac file o day
SELECT @json_today = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_today.json', SINGLE_CLOB) import
SELECT @json_1 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_1.json', SINGLE_CLOB) import
SELECT @json_2 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_2.json', SINGLE_CLOB) import
SELECT @json_3 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_3.json', SINGLE_CLOB) import
SELECT @json_4 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_4.json', SINGLE_CLOB) import
SELECT @json_5 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_5.json', SINGLE_CLOB) import
SELECT @json_6 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_6.json', SINGLE_CLOB) import
SELECT @json_7 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_7.json', SINGLE_CLOB) import
SELECT @json_8 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_8.json', SINGLE_CLOB) import
SELECT @json_9 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_9.json', SINGLE_CLOB) import
SELECT @json_10 = BulkColumn
FROM OPENROWSET (BULK 'D:/DaiHoc/MangMayTinh/SocketProgramming/1_20120176_20120206_20120586/Source/Data/data_10.json', SINGLE_CLOB) import

DROP TABLE IF EXISTS ThongTinVang;

SELECT * INTO ThongTinVang FROM OPENJSON (@json_today, '$.value')					
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_1, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_2, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_3, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_4, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_5, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_6, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_7, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_8, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_9, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

INSERT INTO ThongTinVang (buy, sell, company, brand, updated, brand1, day, id, type, code)
SELECT * FROM OPENJSON(@json_10, '$.value')
WITH
(
	[buy]		nvarchar(50),
	[sell]		nvarchar(50),
	[company]	nvarchar(50),
	[brand]		nvarchar(50),
	[updated]	nvarchar(50),
	[brand1]	nvarchar(50),
	[day]		nvarchar(50),
	[id]		nvarchar(50),
	[type]		nvarchar(50),
	[code]		nvarchar(50)
) 

DELETE FROM ThongTinVang WHERE company = '1Coin'
