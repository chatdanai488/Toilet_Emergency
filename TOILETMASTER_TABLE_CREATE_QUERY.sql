CREATE TABLE dbo.Alerts (
    fAlertNo INT IDENTITY(1,1) PRIMARY KEY,
    fAlertDate DATETIME NOT NULL,
    fAlertLoc CHAR(50) NOT NULL,
    fAlertId CHAR(15) NOT NULL,
    fAlertStatus INT NOT NULL
);


CREATE TABLE dbo.FloorMapTb (
    fRowNo INT IDENTITY(1,1) PRIMARY KEY,
    fDate DATETIME NOT NULL,
    fMapId INT NOT NULL,
    fMapName VARCHAR(100) NOT NULL,
    fMapIp VARCHAR(100) NOT NULL,
    fMapRmrk VARCHAR(500) NOT NULL,
    fCoordsX1 FLOAT,
    fCoordsY1 FLOAT,
    fCoordsX2 FLOAT,
    fCoordsY2 FLOAT,
    fMapMode NVARCHAR(200) NOT NULL,
    fImg VARCHAR(100) NOT NULL,
    fColor VARCHAR(100) NOT NULL
);


CREATE TABLE dbo.LocTb (
    fRowNo INT IDENTITY(1,1) PRIMARY KEY,
    fDate VARCHAR(40) NOT NULL,
    fStdId CHAR(8) NOT NULL,
    fLat REAL,
    fLong REAL,
    fAlt REAL,
    fImg VARCHAR(100) NOT NULL,
    fPlace NVARCHAR(40) NOT NULL,
    fStat CHAR(1) NOT NULL
);

CREATE TABLE dbo.FloorTb (
    No INT IDENTITY(1,1) PRIMARY KEY,
    MapId INT NOT NULL,
    MapName NVARCHAR(MAX) NOT NULL,
    DateCrt DATETIME NOT NULL,
    DateChg DATETIME NOT NULL,
    PicPath NVARCHAR(MAX) NOT NULL,
    chkbox VARCHAR(50) NOT NULL
);