import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import cufflinks as cf
import datetime

###################################################################################################################
# Page Layout Settings
###################################################################################################################

# Set Page Layout
st.set_page_config(
    page_title="Stock Price App",
    page_icon = "💲"
)

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {1300}px;
        padding-top: {2}rem;
        padding-right: {1}rem;
        padding-left: {1}rem;
        padding-bottom: {2}rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

# Set Variables
start = datetime.date(2017, 1, 1)
end = datetime.date.today()
plt.style.use('ggplot')

# Execute Main Function
def main():
    # App title
    st.markdown('''
    # Stock Price App
    A simple stock price app that allows users to track prices over time. 
    ''')
    st.write("")

    # Sidebar
    st.sidebar.title('Navigation')
    st.sidebar.header('Query Parameters')

    # Variables
    start_date = st.sidebar.date_input("Start date", start)
    end_date = st.sidebar.date_input("End date", end)

    ticker_list = get_data()
    st.dataframe(ticker_list)
    with st.beta_expander("About the dataset"):
        st.write('Data updated through: {}'.format('06-11-2021'))
        st.write("""Stock tickers are downloaded daily from NASDAQ's website: https://www.nasdaq.com/market-activity/stocks/screener""")
    st.write("")
    st.write("")

    tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_list['Symbol']) # Select ticker symbol
    get_ticker_data(tickerSymbol, start_date, end_date)
    get_credits()

@st.cache
def get_data():
    data = pd.read_csv('https://raw.githubusercontent.com/ericttran3/yfinance-web-scraper/main/data/nasdaq_screener_06-11-2021.csv')
    #df = data[data['Market Cap'] > 0].sort_values('Market Cap', ascending=False) # Filter for companies with market cap greater than 0
    return data

def get_ticker_data(symbol, start_date, end_date):
    tickerData = yf.Ticker(symbol) # Get ticker data
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) # get the historical prices for this ticker

    # Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.success(string_summary)

    expander_bar = st.beta_expander("About the Company")
    expander_bar.write(tickerData.info)
    expander_bar.write("")

    # Time series plots
    st.write("""
    ## Closing Price
    """)
    st.line_chart(tickerDf.Close)

    st.write("""
    ## Volume Price
    """)
    st.bar_chart(tickerDf.Volume)

def get_credits():
    st.write("")
    st.markdown("Made with ♡ by [Eric Tran](https://ericttran.com)")      
    
             

if __name__ == "__main__":
    main()