import streamlit as st
import pandas as pd 
import numpy as np 
import yfinance as yf 
import plotly.express as px

st.title("FinTech Dashboard")
st.subheader("Research about your desired stock by simply typing its stock symbol")
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
        st.subheader("Please select a more older start date")


    #different tabs
    #overview, fundamentals and news
    overview_data, fund_data, news_data = st.tabs(["Overview", "Fundamentals", "News"])

    with overview_data:
        #contents here:
        #company title
        #description
        #industry
        #country
        #ceo - name and title
        #company website

        info = yf.Ticker(ticker).info

        st.subheader(info["longName"])
        
        st.subheader("About")
        st.write(info["longBusinessSummary"])
        
        st.subheader("Industry")
        st.write(info["industryDisp"])

        st.subheader("Location")
        st.write(info["city"])
        st.write(info["country"])
        
        officers = info['companyOfficers']
        ceo = officers[0]
        st.subheader(ceo["title"])
        st.write(ceo["name"])

    with fund_data:
        st.write("Fundamentals")
        st.write(info)

    with news_data:
        news = yf.Ticker(ticker).news

        for items in news:
            st.subheader(items["title"])
            st.write(items["publisher"])
            st.write(items["link"])
            st.write("Related tickers")
            for ticker in items["relatedTickers"]:
                st.write(ticker)
        


