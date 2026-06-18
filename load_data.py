# import pandas as pd
# import os

# base = r"C:\Users\rkjai\OneDrive\Desktop\coding\Python\StockPriceAnalyzer"

# df = pd.read_csv(os.path.join(base, "StockPrices.csv"))

# print(df["Symbol"].unique())
import pandas as pd
import pyodbc

# ==========================

# SQL CONNECTION

# ==========================

conn = pyodbc.connect(
"DRIVER={ODBC Driver 17 for SQL Server};"
"SERVER=localhost\SQLEXPRESS;"
"DATABASE=StockPriceAnalyzer;"
"Trusted_Connection=yes;"
)

cursor = conn.cursor()

# ==========================

# LOAD CSV FILES

# ==========================

companies = pd.read_csv("Companies.csv")
prices = pd.read_csv("StockPrices.csv")
analysis = pd.read_csv("StockAnalysis.csv")
market = pd.read_csv("MarketIndex.csv")

# ==========================

# COMPANIES

# ==========================

for _, row in companies.iterrows():
 cursor.execute("""
INSERT INTO Companies
VALUES (?, ?, ?, ?)
""",
int(row["CompanyID"]),
str(row["Symbol"]),
str(row["CompanyName"]),
str(row["Sector"])
)

# ==========================

# STOCK PRICES

# ==========================

for _, row in prices.iterrows():
 cursor.execute("""
INSERT INTO StockPrices
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
int(row["PriceID"]),
str(row["Symbol"]),
row["TradeDate"],
float(row["OpenPrice"]),
float(row["HighPrice"]),
float(row["LowPrice"]),
float(row["ClosePrice"]),
int(row["Volume"])
)

# ==========================

# STOCK ANALYSIS

# ==========================

for _, row in analysis.iterrows():
 cursor.execute("""
INSERT INTO StockAnalysis
VALUES (?, ?, ?, ?, ?)
""",
str(row["Symbol"]),
float(row["HighestPrice"]),
float(row["LowestPrice"]),
float(row["AveragePrice"]),
int(row["TotalVolume"])
)

# ==========================

# MARKET INDEX

# ==========================

for _, row in market.iterrows():
 cursor.execute("""
INSERT INTO MarketIndex
VALUES (?, ?, ?)
""",
row["Date"],
float(row["Nifty50"]),
float(row["Sensex"])
)

conn.commit()

print("Data Loaded Successfully!")

cursor.close()
conn.close()
