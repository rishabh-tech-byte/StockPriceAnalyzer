📈 Stock Price Analyzer
🚀 Overview

Stock Price Analyzer is a Python-based dashboard that analyzes stock market data using SQL Server, Streamlit, Pandas, and Plotly.

The project helps users visualize stock performance, compare companies, and monitor market trends through interactive charts.

🛠 Technologies Used
🐍 Python
🗄 SQL Server
📊 Pandas
🌐 Streamlit
📈 Plotly
🔌 PyODBC
✨ Features
📊 Dashboard
Company Summary
Sector Distribution
Nifty50 & Sensex Trends
📈 Stock Analysis
Highest Price
Lowest Price
Average Close Price
Volume Analysis
⚖ Compare Stocks
Compare Two Stocks
Interactive Performance Charts
🌍 Market Overview
Nifty50 Analysis
Sensex Analysis
🗄 Database Explorer
View Database Tables
Explore Stock Records
📂 Project Structure
StockPriceAnalyzer/
│
├── app.py
├── load_data.py
├── Project.sql
├── README.md
├── Companies.csv
├── StockPrices.csv
├── StockAnalysis.csv
├── MarketIndex.csv
└── SectorSummary.csv
▶ Run Project

Install dependencies:

Load data:
python load_data.py
Run application:
streamlit run app.py