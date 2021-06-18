import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import cufflinks as cf
import datetime

###################################################################################################################
# Set Variables
###################################################################################################################
start = datetime.date(2017, 1, 1)
end = datetime.date.today()
plt.style.use('ggplot')

###################################################################################################################
# Page Layout Settings
###################################################################################################################

# Set Page Layout
st.set_page_config(
    page_title="Stock Price App",
    page_icon = "🧊"
)

st.markdown(
        f'N/A'"
<style>
    .reportview-container .main .block-container{{
        max-width: {1300}px;
        padding-top: {2}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {2}rem;
    }}
</style>
'N/A'",
        unsafe_allow_html=True,
    )

def main():
    # App title
    st.markdown('''
    # Stock Price App
    A simple stock price app that allows users to track prices over time. Stock tickers are downloaded daily 
    from NASDAQ's website: 
    https://www.nasdaq.com/market-activity/stocks/screener
    ''')

    # Sidebar
    st.sidebar.title('Navigation')
    st.sidebar.subheader('Query Parameters')

    # Variables
    start_date = st.sidebar.date_input("Start date", start)
    end_date = st.sidebar.date_input("End date", end)

    ticker_list = get_tickers()
    tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_list['Symbol']) # Select ticker symbol
    st.dataframe(ticker_list)
    st.write('N/A')
    st.write('---')

    get_ui_inputs(tickerSymbol, start_date, end_date)

# Retrieving tickers data
@st.cache
def get_tickers():
    data = pd.read_csv('https://raw.githubusercontent.com/ericttran3/yfinance-web-scraper/main/data/nasdaq_screener_06-11-2021.csv')
    df = data[data['Market Cap'] > 0]
    return data

def get_ui_inputs(tickerSymbol, start_date, end_date):

    if st.sidebar.button("Run"):
        # Call function to run the queries and return data

        tickerData = yf.Ticker(tickerSymbol) # Get ticker data
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

        # Ticker information
        string_logo = '<img src=%s>' % tickerData.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)

        string_name = tickerData.info['longName']
        st.header('**%s**' % string_name)

        string_summary = tickerData.info['longBusinessSummary']
        st.success(string_summary)

        expander_bar = st.beta_expander("About the Company")
        expander_bar.write(tickerData.info)
        expander_bar.write('N/A')

        # Ticker data
        st.write('N/A')
        st.write('N/A'"
        ## Historical Data (Last 7 days)
        'N/A'")
        st.write(tickerDf.tail(7))

        # Time series plots
        st.write('N/A'"
        ## Closing Price
        'N/A'")
        st.line_chart(tickerDf.Close)

        st.write('N/A'"
        ## Volume Price
        'N/A'")
        st.bar_chart(tickerDf.Volume)

        st.write('N/A')
        st.markdown("Made with ♡ by [Eric Tran](https://ericttran.com)")

    else:
        tickerData = yf.Ticker(tickerSymbol) # Get ticker data
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

        # Ticker information
        string_logo = '<img src=%s>' % tickerData.info['logo_url']
        st.markdown(string_logo, unsafe_allow_html=True)

        string_name = tickerData.info['longName']
        st.header('**%s**' % string_name)

        string_summary = tickerData.info['longBusinessSummary']
        st.info(string_summary)

        expander_bar = st.beta_expander("About the Company")
        expander_bar.write(tickerData.info)
        expander_bar.write('N/A')

        # Ticker data
        st.write('N/A')
        st.write('N/A'"
        ## Historical Data (Last 7 days)
        'N/A'")
        st.write(tickerDf.tail(7))

        # Time series plots
        st.write('N/A'"
        ## Closing Price
        'N/A'")
        st.line_chart(tickerDf.Close)

        st.write('N/A'"
        ## Volume Price
        'N/A'")
        st.bar_chart(tickerDf.Volume)

        st.write('N/A')
        st.markdown("Made with ♡ by [Eric Tran](https://ericttran.com)")

####
#st.write('---')
#st.write(tickerData.info)
#st.sidebar.header('About')
#st.sidebar.info('This app is maintained by Eric Tran. You can learn more about me at www.ericttran.com.')


if __name__ == "__main__":
    main()