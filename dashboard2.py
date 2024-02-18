import streamlit as st
import pandas as pd 
import numpy as np 
import yfinance as yf 
import plotly.express as px

st.title("Stock Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start date")
end_date = st.sidebar.date_input("End date")


if not ticker:
    st.subheader("Please enter a ticker")
else:
    try:
        # getting data from yahoo finance
        data = yf.download(ticker, start = start_date, end=end_date)

        # plotting data
        fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
        st.plotly_chart(fig)
    except:
        st.write("Please select a more older start date")


    #different tabs
    #overview, fundamentals and news
    overview_data, fund_data, news_data = st.tabs(["Overview", "Fundamentals", "News"])

    with overview_data:
        info = yf.Ticker(ticker).info

        st.subheader(info["longName"])

        st.write(info["longBusinessSummary"])

    with fund_data:
        st.write("Fundamentals")
        st.write(info)

    with news_data:
        st.write("News")

