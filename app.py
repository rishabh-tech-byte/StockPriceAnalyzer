import streamlit as st
import pandas as pd
import pyodbc
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG
st.set_page_config(
page_title="Stock Price Analyzer",
page_icon="📈",
layout="wide"
)
# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():

    # companies = pd.read_csv("Companies.csv")
    # prices = pd.read_csv("StockPrices.csv")
    # analysis = pd.read_csv("StockAnalysis.csv")
    # market = pd.read_csv("MarketIndex.csv")

    # prices["TradeDate"] = pd.to_datetime(prices["TradeDate"])
    # market["Date"] = pd.to_datetime(market["Date"])
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=StockPriceAnalyzer;"
        "Trusted_Connection=yes;"
    )

    companies = pd.read_sql(
        "SELECT * FROM Companies",
        conn
    )

    prices = pd.read_sql(
        "SELECT * FROM StockPrices",
        conn
    )

    analysis = pd.read_sql(
        "SELECT * FROM StockAnalysis",
        conn
    )

    market = pd.read_sql(
        "SELECT * FROM MarketIndex",
        conn
    )

    conn.close()

    prices["TradeDate"] = pd.to_datetime(prices["TradeDate"])
    market["Date"] = pd.to_datetime(market["Date"])
    return companies, prices, analysis, market

 
companies, prices, analysis, market = load_data()

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("📈 Stock Price Analyzer")

page = st.sidebar.radio(
"Navigation",
[
"Dashboard",
"Stock Analysis",
"Compare Stocks",
"Market Overview",
"Database Explorer"
]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Project:
    Python + SQL + Streamlit

    Stocks:
    TCS
    INFY
    RELIANCE
    HDFCBANK
    WIPRO
    """
)
# ==========================================
# DASHBOARD
# ==========================================
if page == "Dashboard":
    st.title("📊 Stock Market Dashboard")

    highest_price = prices["HighPrice"].max()
    total_volume = prices["Volume"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🏢 Companies",
        len(companies)
    )

    c2.metric(
        "📊 Records",
        len(prices)
    )

    c3.metric(
        "🏭 Sectors",
        companies["Sector"].nunique()
    )

    c4.metric(
        "💰 Highest Price",
        round(highest_price, 2)
    )

    st.markdown("---")

    st.subheader("📋 Companies Information")

    st.dataframe(
        companies,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🏭 Sector Distribution")

    sector_count = companies["Sector"].value_counts()

    fig_sector = px.bar(
        x=sector_count.index,
        y=sector_count.values,
        color=sector_count.values,
        labels={
            "x": "Sector",
            "y": "Companies"
        },
        title="Companies by Sector"
    )

    st.plotly_chart(
        fig_sector,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📈 Market Snapshot")

    col1, col2 = st.columns(2)

    with col1:

        fig_nifty = px.line(
            market,
            x="Date",
            y="Nifty50",
            markers=True,
            title="Nifty50 Trend"
        )

        st.plotly_chart(
            fig_nifty,
            use_container_width=True
        )

    with col2:

        fig_sensex = px.line(
            market,
            x="Date",
            y="Sensex",
            markers=True,
            title="Sensex Trend"
        )

        st.plotly_chart(
            fig_sensex,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("📊 Dataset Summary")

    summary = pd.DataFrame({
        "Metric": [
            "Total Companies",
            "Total Records",
            "Total Volume"
        ],
        "Value": [
            len(companies),
            len(prices),
            total_volume
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True
    )
#Stock Analysis
elif page == "Stock Analysis":

    st.title("📈 Stock Analysis")

    stock = st.selectbox(
        "Select Stock",
        sorted(prices["Symbol"].unique())
    )
    stock_df = prices[
        prices["Symbol"] == stock
    ]

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Highest Price",
        round(stock_df["HighPrice"].max(), 2)
    )

    c2.metric(
        "Lowest Price",
        round(stock_df["LowPrice"].min(), 2)
    )

    c3.metric(
        "Average Close",
        round(stock_df["ClosePrice"].mean(), 2)
    )

    c4.metric(
        "Total Volume",
        int(stock_df["Volume"].sum())
    )

    st.markdown("---")

    st.subheader(f"📉 Closing Price Trend - {stock}")

    fig_price = px.line(
        stock_df,
        x="TradeDate",
        y="ClosePrice",
        markers=True,
        title=f"{stock} Closing Price"
    )

    fig_price.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader(f"📊 Volume Trend - {stock}")

    fig_volume = px.bar(
        stock_df,
        x="TradeDate",
        y="Volume",
        color="Volume",
        title=f"{stock} Trading Volume"
    )

    st.plotly_chart(
        fig_volume,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📋 Stock Records")

    st.dataframe(
        stock_df,
        use_container_width=True
    )
    csv = stock_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Stock Data",
        csv,
        f"{stock}_data.csv",
        "text/csv"
    )
# ==========================================
# COMPARE STOCKS
# ==========================================
elif page == "Compare Stocks":

    st.title("📊 Compare Stocks")

    col1, col2 = st.columns(2)

    with col1:
        stock1 = st.selectbox(
            "Select First Stock",
            sorted(prices["Symbol"].unique()),
            key="stock1"
        )

    with col2:
        stock2 = st.selectbox(
            "Select Second Stock",
            sorted(prices["Symbol"].unique()),
            index=1,
            key="stock2"
        )

    df1 = prices[prices["Symbol"] == stock1]
    df2 = prices[prices["Symbol"] == stock2]

    st.markdown("---")

    fig_compare = px.line(
        title=f"{stock1} vs {stock2}"
    )

    fig_compare.add_scatter(
        x=df1["TradeDate"],
        y=df1["ClosePrice"],
        mode="lines+markers",
        name=stock1
    )

    fig_compare.add_scatter(
        x=df2["TradeDate"],
        y=df2["ClosePrice"],
        mode="lines+markers",
        name=stock2
    )

    fig_compare.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )

    st.markdown("---")

    comparison = pd.DataFrame({
        "Stock": [stock1, stock2],
        "Highest Price": [
            round(df1["HighPrice"].max(), 2),
            round(df2["HighPrice"].max(), 2)
        ],
        "Lowest Price": [
            round(df1["LowPrice"].min(), 2),
            round(df2["LowPrice"].min(), 2)
        ],
        "Average Close": [
            round(df1["ClosePrice"].mean(), 2),
            round(df2["ClosePrice"].mean(), 2)
        ],
        "Total Volume": [
            int(df1["Volume"].sum()),
            int(df2["Volume"].sum())
        ]
    })

    st.subheader("📋 Comparison Table")

    st.dataframe(
        comparison,
        use_container_width=True
    )
elif page == "Market Overview":

    st.title("📈 Market Overview")

    fig1 = px.line(
        market,
        x="Date",
        y="Nifty50",
        markers=True,
        title="Nifty50 Trend"
    )
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(
        market,
        x="Date",
        y="Sensex",
        markers=True,
        title="Sensex Trend"
    )
    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.dataframe(
        market,
        use_container_width=True
    )
elif page == "Database Explorer":
  st.title("🗄 Database Explorer")

table = st.selectbox(
    "Select Table",
    [
        "Companies",
        "StockPrices",
        "StockAnalysis",
        "MarketIndex"
    ]
)
if table == "Companies":
    st.dataframe(companies)

elif table == "StockPrices":
    st.dataframe(prices)

elif table == "StockAnalysis":
    st.dataframe(analysis)
elif table == "MarketIndex":
    st.dataframe(market)



