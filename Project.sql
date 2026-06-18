CREATE DATABASE StockpriceAnalyzer;

USE StockpriceAnalyzer;


CREATE TABLE Companies (
    CompanyID INT PRIMARY KEY,
    Symbol VARCHAR(20),
    CompanyName VARCHAR(100),
    Sector VARCHAR(50)
);

CREATE TABLE StockPrices (
    PriceID INT PRIMARY KEY,
    Symbol VARCHAR(20),
    TradeDate DATE,
    OpenPrice FLOAT,
    HighPrice FLOAT,
    LowPrice FLOAT,
    ClosePrice FLOAT,
    Volume BIGINT
);

CREATE TABLE MarketIndex (
    Date DATE,
    Nifty50 FLOAT,
    Sensex FLOAT
);

CREATE TABLE StockAnalysis (
    Symbol VARCHAR(20),
    HighestPrice FLOAT,
    LowestPrice FLOAT,
    AveragePrice FLOAT,
    TotalVolume BIGINT
);

CREATE TABLE SectorSummary (
    Sector VARCHAR(50),
    TotalCompanies INT
);

-- Verify Database
SELECT DB_NAME() AS CurrentDatabase;

-- Verify Tables
SELECT * FROM INFORMATION_SCHEMA.TABLES;