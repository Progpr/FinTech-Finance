import streamlit as st
import config
import helpers
from iex import IEXstock
from datetime import datetime
import requests

st.sidebar.title("Stock Dashboard")

# User input for company name
company_name = st.sidebar.text_input("Company Name", "")

if company_name:
    # Request to the IEX Cloud search endpoint to find the stock symbol
    search_url = f"https://api.iex.cloud/v1/search/{company_name}?token={config.IEX_P_KEY}"
    search_response = requests.get(search_url)
    search_results = search_response.json()

    if search_results:
        # Display the stock symbols found
        st.sidebar.write("Stock Symbols Found:")
        for result in search_results:
            st.sidebar.write(f"Symbol: {result['symbol']}, Company Name: {result['securityName']}")

        selected_symbol = st.sidebar.selectbox("Select a Symbol", [result['symbol'] for result in search_results])
        stock = IEXstock(config.IEX_P_KEY,selected_symbol)

        screen = st.sidebar.selectbox("Select View", ['Overview', 'Fundamentals','News'])

        st.title(screen)


        if screen=='Overview':
            logo = stock.get_logo()
            company_info = stock.get_company_info()


            col1, col2 = st.columns(2)

            with col1:
                st.image(logo['url'])

            for company_data in company_info:
                    with col2:
                        st.subheader(company_data.get('companyName'))
                        st.subheader("Industry")
                        st.write(company_data.get('industry'))
                        st.subheader("CEO")
                        st.write(company_data.get('ceo'))
                        st.subheader("Description")
                        st.write(company_data.get('longDescription'))



        if screen=='Fundamentals':
            stats = stock.get_stats()

            st.header('Ratios')

            col1, col2 = st.columns(2)

            with col1:
                st.subheader('P/E')
                st.write(stats['peRatio'])
                st.subheader('Forward P/E')
                st.write(stats['forwardPERatio'])
                st.subheader('PEG Ratio')
                st.write(stats['pegRatio'])
                st.subheader('Price to Sales')
                st.write(stats['priceToSales'])
                st.subheader('Price to Book')
                st.write(stats['priceToBook'])
            with col2:
                st.subheader('Revenue')
                st.write(helpers.format_number(stats['revenue']))
                st.subheader('Cash')
                st.write(helpers.format_number(stats['totalCash']))
                st.subheader('Debt')
                st.write(helpers.format_number(stats['currentDebt']))
                st.subheader('200 Day Moving Average')
                st.write(stats['day200MovingAvg'])
                st.subheader('50 Day Moving Average')
                st.write(stats['day50MovingAvg'])

            fundamentals=stock.get_fundamentals()

            for quarter in fundamentals:
                st.header(f"Q{quarter['fiscalQuarter']} {quarter['fiscalYear']}")
                st.subheader('Filing Date')
                st.write(quarter['filingDate'])
                st.subheader('Revenue')
                st.write(helpers.format_number(quarter['revenue']))
                st.subheader('Net Income')
                st.write(helpers.format_number(quarter['incomeNet']))

            st.header("Dividends")

            dividends = stock.get_dividends()

            for dividend in dividends:
                st.write(dividend['paymentDate'])
                st.write(dividend['amount'])


        if screen=="News":
            news = stock.get_company_news()

            for article in news:
                st.subheader(article['headline'])
                dt = datetime.utcfromtimestamp(article['datetime']/1000).isoformat()
                st.write(f"Posted by {article['source']} at {dt}")
                st.write(article['url'])
                st.write(article['summary'])
                st.image(article['image'])
