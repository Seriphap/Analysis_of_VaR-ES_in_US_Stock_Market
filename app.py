#api_key = "UXKJLZ71WIHNK84C"

import streamlit as st
from datetime import datetime, timedelta
from data_loader import load_price_data
from risk_metrics import calculate_var_es
from plotter import plot_histogram_with_risk_lines
from plotter import plot_candlestick
import pandas as pd


st.set_page_config(page_title="Analysis of Value at Risk (VaR) and Expected Shortfall (ES) in the U.S. Stock Market", layout="wide")
st.markdown("## 📈 Analysis of Value at Risk (VaR) and Expected Shortfall (ES) in the U.S. Stock Market")


# Sidebar Inputs
st.sidebar.header("Configuration")
data_source = st.sidebar.radio("Select Data Source", ["Example Stock Price data","Upload CSV","API"])

uploaded_file = None
prices_df = None
if data_source == "Example Stock Price data":
        st.sidebar.text("Note: The stock price is updated in Sep2025 ")
        stock_selection = st.sidebar.selectbox("Select Data Source", ["MSFT_day", "MSFT_week", "MSFT_month", "BABA_day", "BABA_week","BABA_month","AAPL_day","AAPL_week","AAPL_month","IBM_day","IBM_week","IBM_month"])
        prices_df = pd.read_csv(f"data/{stock_selection}.csv", parse_dates=True, index_col=0)
elif data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])
    st.sidebar.text("Note: makesure your format is correct or you can see and download the correct format in options of Example Stock Price data")
    if uploaded_file is not None:
        prices_df = pd.read_csv(uploaded_file, parse_dates=True, index_col=0)
elif data_source == "API":
    symbol = st.sidebar.text_input("Asset Symbol (e.g. AAPL, MSFT)", "AAPL")
    interval = st.sidebar.selectbox("Interval (investment frequency)", ["Daily", "Weekly", "Monthly"])
    api_key = st.sidebar.text_input("Alpha Vantage API Key", type="password")
    #st.sidebar.text("UXKJLZ71WIHNK84C") you can use my API as well but it's free API then limit is 25 requests per day.
    st.sidebar.text("link to get free KPI 25 requests per day")
    st.sidebar.markdown("https://www.alphavantage.co/support/#api-key")
    if symbol and api_key:
        prices_df = load_price_data(symbol, interval, api_key)
    else:
        st.info("Please enter both asset symbol and API key.")
 

# Load and process data
if prices_df is not None and not prices_df.empty:
    with st.expander("📊 Raw Price Data"):
        st.markdown(f"### Table of Historical price")
        st.dataframe(prices_df)

    with st.expander("📊 Chart Price Data"):
        # 👉 Candlestick (เรียกจาก plotter.py)
        if data_source == "Upload CSV" or data_source == "Example Stock Price data" :
            symbol = ""
            interval = ""
        fig = plot_candlestick(prices_df, symbol=symbol, interval=interval, add_volume=True)
        st.plotly_chart(fig, use_container_width=True)

    # ใช้ราคาปิดปรับแล้วถ้ามี ไม่งั้นใช้ราคาปิดธรรมดา
    if "Adj Close" in prices_df.columns:
        prices = prices_df["Adj Close"]
    elif "Close" in prices_df.columns:
        prices = prices_df["Close"]
    else:
        st.error("No valid price column found.")
        st.stop()
    returns = prices.pct_change().dropna().squeeze()
    #returns = prices.resample("W").last().pct_change().dropna()
    #returns  = prices.resample("M").last().pct_change().dropna()

    st.subheader("Range selection for calculating the investment period")
    st.text("If the frequency is monthly investment (1 time/month), please select range longer than 2 years")
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.today() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", value=datetime.today())

    # กรองช่วงเวลา
    filtered_returns = returns[(returns.index >= pd.to_datetime(start_date)) & (returns.index <= pd.to_datetime(end_date))]

    with st.expander("📊 Price Data (after select invesment period)"):
        st.markdown(f"### Table of Historical price from {start_date} to {end_date} ")
        st.dataframe(filtered_returns)

    if filtered_returns.empty:
        st.warning("No return data available for the selected asset and time range.")
    else:
        st.subheader(f"📊 Risk Metrics")
        st.text(f"Name: {symbol}, Investment Frequency: {interval}")
        col1, col2, = st.columns(2)
        with col1:
            investment_amount = st.number_input("Investment Amount", min_value=100, value=500, step=500)
        with col2:    
            confidence_level = st.slider("Confidence Level (%)",90, 99, 95)
            
        var, es = calculate_var_es(filtered_returns, confidence_level / 100)
        expected_return = filtered_returns.mean()

        if var is None or es is None:
            st.warning("Cannot calculate VaR and ES due to insufficient return data.")
        else:
            adjusted_var = var * investment_amount
            adjusted_es = es * investment_amount
            adjusted_expected_return = filtered_returns.mean() * investment_amount
            adjusted_returns = filtered_returns * investment_amount

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"VaR ({confidence_level}%)", value=f"{var:.4f}")
            with col2:
                st.metric(label=f"Expected Shortfall ({confidence_level}%)", value=f"{es:.4f}")
            with col3:
                st.metric(label=f"Expected Return", value=f"{expected_return:.4f}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"VaR of invertment amount ({confidence_level}%)", value=f"{adjusted_var:,.2f}")
            with col2:
                st.metric(label=f"ES of invertment amount ({confidence_level}%)", value=f"{adjusted_es:,.2f}")
            with col3:
                st.metric(label=f"Expected Return of invertment amount ({confidence_level}%) ", value=f"{adjusted_expected_return:.2f}")

        st.markdown(f"##### 📉 Histogram of Returns from {start_date} to {end_date}")
        col1, col2 = st.columns(2)
        with col1:
            st.text("Return per a unit of money")
            st.plotly_chart(plot_histogram_with_risk_lines(filtered_returns,var,es), use_container_width=True)
        with col2:
            st.text(f"Return per invertment amount ({investment_amount})")
            st.plotly_chart(plot_histogram_with_risk_lines(adjusted_returns, adjusted_var,adjusted_es), use_container_width=True)

else:
    st.error("Failed to load data or no data available for the selected range.")



