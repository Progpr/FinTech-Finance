import streamlit as st
import pandas as pd 
import numpy as np 
import yfinance as yf 
import plotly.express as px

st.title("Stock Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")

# getting data from yahoo finance
data = yf.download(ticker, start = start_date, end=end_date)

# plotting data
fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
st.plotly_chart(fig)


#different tabs
#overview, fundamentals and news
overview_data, fund_data, news_data = st.tabs(["Overview", "Fundamentals", "News"])

with overview_data:
    st.write(f"About {ticker}")

    infos = yf.Ticker(ticker).info

    st.write(infos["longBusinessSummary"])

with fund_data:
    st.write("Fundamentals")

with news_data:
    st.write("News")

