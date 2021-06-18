from urllib.parse import uses_fragment
from altair.vegalite.v4.schema.channels import Tooltip
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import altair as alt
import streamlit as st
import yfinance as yf
from yfinance import ticker
import cufflinks as cf
import datetime
import time
from dateutil.relativedelta import relativedelta # to add days or years


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
start = datetime.date(2016, 1, 1)
end = datetime.date.today()
plt.style.use('ggplot')

# Web Scraping Wikipedia
# S&P 500 = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
# DIJA 30 = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
# Nasdaq = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
# Russell 1000 = 'https://en.wikipedia.org/wiki/Russell_1000_Index'

# Execute Main Function
def main():

    start_exec = time.time()

    # App title
    st.markdown('''
    # Stock Price App
    A simple stock app to research stocks and track prices over time. This tool is used for educational purposes only and does not provide any financial investment advice. Do your own research and due dilligence before purchasing stocks. Invest at your own risk.
    ''')
    # Choose an Index: S&P 500, DIJA, Nasdaq Composite, Nikkei 225, FTSE 100

    # Sidebar
    st.sidebar.title('Navigation')
    st.sidebar.header('Query Parameters')

    # Variables
    with st.sidebar.beta_container():
        start = datetime.date(2016, 1, 1)
        end = datetime.date.today()

        col1, col2 = st.beta_columns(2)
        start_date = col1.date_input("Start date", start)
        end_date = col2.date_input("End date", end)

    # Call function to pull in NASDAQ stock data
    ticker_list = get_data()
    expander_bar = st.beta_expander("Show NASDAQ Stock List")
    expander_bar.text('Data Dimensions: {} rows and {} columns.'.format(ticker_list.shape[0],ticker_list.shape[1]))
    expander_bar.dataframe(ticker_list)
    
    
    st.write("")

    # Get ticker symbol from list of available tickers
    tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_list['Symbol']) # Select ticker symbol

    sb_placeholder = st.sidebar.empty()
    sb_placeholder.text('Processing...')

    # Call function to return historical price and volume data for ticker
    get_ticker_data(tickerSymbol, start_date, end_date)

    # Call function to give shoutout to development team!
    get_credits()

    sb_placeholder.text("Execution time: {} seconds".format(round(time.time() - start_exec,2)))

    return None

@st.cache
def get_data():
    data = pd.read_csv('https://raw.githubusercontent.com/ericttran3/yfinance-web-scraper/main/data/nasdaq-stock-tickers.csv')
    #df = data[data['Market Cap'] > 0].sort_values('Market Cap', ascending=False) # Filter for companies with market cap greater than 0
    return data

def get_ticker_data(symbol, start_date, end_date):
    tickerData = yf.Ticker(symbol) # Get ticker data

    # Extract Attributes from API Payload
    try:
        logo = tickerData.info['logo_url']
    except:
        logo = None

    try:
        company_name = tickerData.info['longName']
    except:
        company_name = 'N/A'

    try:
        country = tickerData.info['country']
    except:
        country = 'N/A'

    try:
        sector = tickerData.info['sector']
    except:
        sector = 'N/A'

    try:
        industry = tickerData.info['industry']
    except:
        industry = 'N/A'

    try:
        market = tickerData.info['market']
    except:
        market = 'N/A'

    try:
        employees = tickerData.info['fullTimeEmployees']
    except:
        employees = 'N/A'
    
    try:
        website = tickerData.info['website']
    except:
        website = 'N/A'

    # Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)
    st.markdown('''
    Country: `{country}` | Sector: `{sector}` | Industry: `{industry}` | Market: `{market}` | Employees: `{employees}` | Website: `{website}`
    '''.format(country=country, sector=sector, industry=industry, market=market, employees=employees, website=website
    ))
    st.write(tickerData.info['longBusinessSummary'])

    #st.subheader('Ticker Summary')
    expander_bar = st.beta_expander("Ticker Summary")
    with expander_bar.beta_container():
        col1, col2, col3, col4 = st.beta_columns(4)

        # Store values from API call in variables. Add error handling
        try:
            price = tickerData.info['regularMarketPrice']
        except:
            price = ""

        try:
            previous_close = round(tickerData.info['previousClose'],2)
        except:
            previous_close = ""

        try: 
            high = round(tickerData.info['regularMarketDayHigh'],2)
        except:
            high = ""

        try: 
            low = round(tickerData.info['regularMarketDayLow'],2)
        except:
            low = ""      

        try:
            high_52 = round(tickerData.info['fiftyTwoWeekHigh'],2)
        except:
            high_52 = ""
            
        try:
            low_52 = round(tickerData.info['fiftyTwoWeekLow'],2)
        except:
            low_52 = ""

        try:
            change_52 = round(tickerData.info['52WeekChange']*100,2)
        except:
            change_52 = ""                    

        try:
            change_52_snp = round(tickerData.info['SandP52WeekChange']*100,2)
        except:
            change_52_snp = ""   

        try:
            ma_50 = round(tickerData.info['fiftyDayAverage'],2)
        except:
            ma_50 = ""  

        try:
            ma_200 = round(tickerData.info['twoHundredDayAverage'],2)
        except:
            ma_200 = ""               

        try:
            market_cap = tickerData.info['marketCap']
        except:
            market_cap = ""               

        try:
            beta = round(tickerData.info['beta'],2)
        except:
            beta = ""

        try:
            pe_ratio = round(tickerData.info['trailingPE'],2)
        except:
            pe_ratio = ""

        try:
            eps = round(tickerData.info['trailingEps'],2)
        except:
            eps = ""

        try:
            peg_ratio = round(tickerData.info['pegRatio'],2)
        except:
            peg_ratio = ""

        try:
            price_to_sale = round(tickerData.info['priceToSalesTrailing12Months'],2)
        except:
            price_to_book = ""

        try:
            price_to_book = round(tickerData.info['priceToBook'],2)
        except:
            price_to_book = ""

        try:
            enterprise_value = round(tickerData.info['enterpriseToRevenue'],2)
        except:
            enterprise_value = ""

        try:
            ebitda = round(tickerData.info['enterpriseToEbitda'],2)
        except:
            ebitda = ""

        try:
            profit = round(tickerData.info['profitMargins']*100,2)
        except:
            profit = ""

        try:
            net_income = round(tickerData.info['netIncomeToCommon'],2)
        except:
            net_income = ""

        try:
            payout = round(tickerData.info['payoutRatio']*100,2)
        except:
            payout = ""
        
        try:
            dividend_rate = round(tickerData.info['dividendRate'],2)
        except:
            dividend_rate = ""

        try:
            dividend_yield = round(tickerData.info['dividendYield']*100,2)
        except:
            dividend_yield = ""

        try:
            forward_eps = round(tickerData.info['forwardEps'],2)
        except:
            forward_eps = ""

        try:
            trailing_pe = round(tickerData.info['trailingPE'],2)
        except:
            trailing_pe = ""

        try:
            forward_pe = round(tickerData.info['forwardPE'],2)
        except:
            forward_pe = ""
        
        try:
            earnings_growth = round(tickerData.info['earningsQuarterlyGrowth']*100,2)
        except:
            earnings_growth = ""

        try:
            volume = tickerData.info['regularMarketVolume']
        except:
            volume = ""

        try:
            avg_vol_3mo = tickerData.info['averageVolume']
        except:
            avg_vol_3mo = ""

        try:
            avg_vol_10day = tickerData.info['averageVolume10days']
        except:
            avg_vol_10day = ""

        try:
            shares_outstanding = tickerData.info['sharesOutstanding']
        except:
            shares_outstanding = ""

        try:
            shares_float = tickerData.info['floatShares']
        except:
            shares_float = ""

        try:
            pct_insiders = round(tickerData.info['heldPercentInsiders']*100,2)
        except:
            pct_insiders = ""

        try:
            pct_institutions = round(tickerData.info['heldPercentInstitutions']*100,2)
        except:
            pct_institutions = ""

        try:
            shares_short = tickerData.info['sharesShort']
        except:
            shares_short = ""

        try:
            shares_short_ratio = round(tickerData.info['shortRatio'],2)
        except:
            shares_short_ratio = ""

        try:
            short_pct_float = round(tickerData.info['shortPercentOfFloat']*100,2)
        except:
            short_pct_float = ""
        
        try:
            shares_short_pm = tickerData.info['sharesShortPriorMonth']
        except:
            shares_short_pm = ""


        col1.subheader('Technical')
        col1.markdown("""
            |  | |
            | :- | :- | :- |
            | Price | `{price}`            
            | Previous Close | `{previous_close}` 
            | Today's Range | `{low}` - `{high}`
            | 52 Week Range | `{low_52}` - `{high_52}`
            | 52 Week /\ | `{change_52}%` 
            | S&P500 52 /\ | `{change_52_snp}%` 
            | 50 Day MA | `{ma_50}` 
            | 200 Day MA | `{ma_200}` 
            """.format(price=price, previous_close=previous_close, high=high, low=low, high_52=high_52, 
                        low_52=low_52, change_52=change_52, change_52_snp=change_52_snp,  ma_50=ma_50, ma_200=ma_200
        ))

        col2.subheader('Valuation')
        col2.markdown("""
            |  | |
            | :- | :- | :- |
            | Market Cap | `{market_cap}` 
            | Beta | `{beta}` 
            | PE Ratio | `{pe_ratio}` 
            | EPS | `{eps}` 
            | PEG Ratio | `{peg_ratio}`
            | Price to Sale | `{price_to_sale}`
            | Price to Book | `{price_to_book}`
            | Enterprise Value| `{enterprise_value}` 
            | Enterprise EBITDA| `{ebitda}` 
            """.format(market_cap=market_cap, beta=beta, pe_ratio=pe_ratio, eps=eps, peg_ratio=peg_ratio, 
                        price_to_sale=price_to_sale, price_to_book=price_to_book, enterprise_value=enterprise_value, 
                        ebitda=ebitda
        ))

        col3.subheader('Fundamentals')
        col3.markdown("""
            |  | |
            | :- | :- | :- |
            | Profit Margin | `{profit}%` 
            | Net Income | `{net_income}` 
            | Dividend Yield | `{dividend_yield}%`             
            | Dividend Rate | `{dividend_rate}` 
            | Payout Ratio | `{payout}%` 
            | Forward EPS | `{forward_eps}` 
            | Trailing PE | `{trailing_pe}`
            | Forward PE | `{forward_pe}`
            | Earnings Growth | `{earnings_growth}%`
            """.format(profit=profit, net_income=net_income, payout=payout, dividend_rate=dividend_rate, 
                        dividend_yield=dividend_yield, forward_eps=forward_eps, trailing_pe=trailing_pe,
                        forward_pe=forward_pe, earnings_growth=earnings_growth)
        )

        col4.subheader('Holdings')
        col4.markdown("""
            |  | |
            | :- | :- | :- |
            | Volume | `{volume}`             
            | Avg Volume (3Mo) | `{avg_vol_3mo}`
            | Avg Volume (10Day) | `{avg_vol_10day}` 
            | Shares Outstanding | `{shares_outstanding}`
            | Shares Float | `{shares_float}`
            | % Held by Insiders | `{pct_insiders}%`
            | % Held by Institutions | `{pct_institutions}%`
            | Shares Short | `{shares_short}`
            | Shares Short Ratio | `{shares_short_ratio}%`
            | Short Pct Float | `{short_pct_float}%`
            | Shares Short (PM)| `{shares_short_pm}`
            """.format(volume=volume, avg_vol_3mo=avg_vol_3mo, avg_vol_10day=avg_vol_10day, 
                        shares_outstanding=shares_outstanding, shares_float=shares_float, pct_insiders=pct_insiders, 
                        pct_institutions=pct_institutions, shares_short=shares_short, shares_short_ratio=shares_short_ratio, 
                        short_pct_float=short_pct_float, shares_short_pm=shares_short_pm)
        )
        st.write("")
        st.write("")

    expander_bar = st.beta_expander("Data Dictionary")
    expander_bar.markdown("""
    All definitions are provided by [Investopedia](https://www.investopedia.com)

    | Attribute | Value | Definition |
    | :- | :- | :- |
    | Sector | 1 | A sector is an area of the economy in which businesses share the same or a related product or service. |
    | Industry | 2 | The term industry refers to a series of companies that operate in a similar business sphere, and its categorization is more narrow. |
    | Country | 3 | The country the company was originated or does business in. |
    | Market Cap | 4 | Market capitalization refers to the total dollar market value of a company's outstanding shares of stock. Commonly referred to as "market cap," it is calculated by multiplying the total number of a company's outstanding shares by the current market price of one share. |
    | Beta | 5 | Beta is a measure of the volatility—or systematic risk—of a security or portfolio compared to the market as a whole.  |    
    | P/E Ratio | 6 | The price-to-earnings ratio (P/E ratio) is the ratio for valuing a company that measures its current share price relative to its per-share earnings (EPS). The price-to-earnings ratio is also sometimes known as the price multiple or the earnings multiple.  |    
    | EPS | 7 | Earnings per share (EPS) is calculated as a company's profit divided by the outstanding shares of its common stock. The resulting number serves as an indicator of a company's profitability.  |    
    | PEG Ratio | 8 | The price/earnings to growth ratio (PEG ratio) is a stock's price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period. The PEG ratio is used to determine a stock's value while also factoring in the company's expected earnings growth, and it is thought to provide a more complete picture than the more standard P/E ratio.  |    
    | P/S Ratio | 9 | The price-to-sales (P/S) ratio is a valuation ratio that compares a company’s stock price to its revenues. It is an indicator of the value that financial markets have placed on each dollar of a company’s sales or revenues.  |    
    | P/B Ratio | 10 | Companies use the price-to-book ratio (P/B ratio) to compare a firm's market capitalization to its book value. It's calculated by dividing the company's stock price per share by its book value per share (BVPS).  |    
    | EV/R | 11 | The enterprise value-to-revenue multiple (EV/R) is a measure of the value of a stock that compares a company's enterprise value to its revenue. EV/R is one of several fundamental indicators that investors use to determine whether a stock is priced fairly.  |    
    | EBITDA/EV | 12 | The EBITDA/EV multiple is a financial valuation ratio that measures a company's return on investment (ROI).   |    
    | Profit Margin | 13 | A metric used to gauge how a company or business makes money. Expressed as percentage, profit margin indicatses how many cents of profit has been generated for each dollar of sale. |    
    | Net Income | 14 | Net income (NI), also called net earnings, is calculated as sales minus cost of goods sold, selling, general and administrative expenses, operating expenses, depreciation, interest, taxes, and other expenses.  |    
    | Dividend Yield | 15 | The dividend yield–displayed as a percentage–is the amount of money a company pays shareholders for owning a share of its stock divided by its current stock price.  |    
    | Dividend Rate | 16 | Dividend rate, expressed as a percentage or yield, is a financial ratio that shows how much a company pays out in dividends each year relative to its stock price.  |    
    | Payout Ratio | 17 | The payout ratio, also known as the dividend payout ratio, shows the percentage of a company's earnings paid out as dividends to shareholders.  |    
    | Forward EPS | 18 | Forward earnings are an estimate of a company's earnings for upcoming periods. Forward earnings project future revenues, margins, tax rates, and other financial data. |    
    | Trailing PE | 19 | Trailing price-to-earnings (P/E) is a relative valuation multiple that is based on the last 12 months of actual earnings. It is calculated by taking the current stock price and dividing it by the trailing earnings per share (EPS) for the past 12 months.  |    
    | Forward PE | 20 | Forward price-to-earnings (forward P/E) is a version of the ratio of price-to-earnings (P/E) that uses forecasted earnings for the P/E calculation.  |    
    | Earnings Growth | 21 | Growth rates are used to express the annual change in a variable as a percentage. Growth rates can be beneficial in assessing a company’s performance and to predict future performance.  |    
    | Volume | 22 | Volume is the number of shares of a security traded between its daily open and close. Trading volume, and changes to volume over the course of time, are important inputs for technical traders.  |    
    | Shares Outstanding | 23 | Shares outstanding refer to a company's stock currently held by all its shareholders, including share blocks held by institutional investors and restricted shares owned by the company’s officers and insiders.  |    
    | Shares Float | 24 | Floating stock refers to the number of shares a company has available to trade in the open market. To calculate a company's floating stock, subtract its restricted stock and closely held shares from its total number of outstanding shares.  |    
    | % Held by Insiders | 25 | Insiders are a company's officers, directors, relatives, or anyone else with access to key company information before it's made available to the public. By watching the trading activity of corporate insiders and large institutional investors, it's easier to get a sense of a stock's prospects. |    
    | % Held by Institutions | 26 | An institutional investor is a company or organization that invests money on behalf of other people. Mutual funds, pensions, and insurance companies are examples.  |    
    | Shares Short | 27 | A short, or a short position, is created when a trader sells a security first with the intention of repurchasing it or covering it later at a lower price.   |    
    | Shares Short Ratio | 28 | The short Interest ratio is a simple formula that divides the number of shares short in a stock by the stock's average daily trading volume. The short interest ratio is a quick way to see how heavily shorted a stock may be versus its trading volume. |    
    | Short Percent to Float | 29 |  When a company's short interest is high (above 40%), it frequently means a large portion of investors anticipate the shares will go down in value and are looking to profit from the decline or are using the short as a hedge against a possible decline. |    
    | Shares Short Previous Month | 30 |  The number of shares that were shorted in the previous month. This metric can serves as a market sentiment indicator for investors. |    
    | Price | `{price}` | The sector company operates in |
    | Profit Margin | `{profit}` | The sector company operates in |

    \n\n
    """.format(marketcap=market_cap,price=price, profit=profit))
    expander_bar.write("")

    expander_bar = st.beta_expander("About the Company")
    expander_bar.write(tickerData.info)

    # Get historical stock price for the data range with periods 
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) # get the historical prices for this ticker
    tickerDf['Date'] = tickerDf.index
    tickerDf['Year'] = pd.DatetimeIndex(tickerDf.index).year

    get_visualizations(tickerDf)


def get_visualizations(tickerDf):
    # Time series plots
    st.write("")
    st.write("""
    ### Closing Price
    """)
    st.line_chart(tickerDf.Close)

    st.write("""
    ### Volume Price
    """)
    st.bar_chart(tickerDf.Volume)

    with st.beta_container():
        st.write("""
        ### Volume x Price
        """)
        scatter_chart = st.altair_chart(
            alt.Chart(tickerDf).mark_circle(size=60).encode(
                x='Volume', 
                y='Close', 
                color='Year',
                tooltip=['Volume', 'Close', 'Year', 'Date']
        ))

    fig = go.Figure()

    #Candlestick
    fig.add_trace(go.Candlestick(x=tickerDf.index,
                    open=tickerDf['Open'],
                    high=tickerDf['High'],
                    low=tickerDf['Low'],
                    close=tickerDf['Close'], name = 'market data'))

    # Add titles
    fig.update_layout(
        title='Live share price evolution',
        yaxis_title='Stock Price (USD)')

    st.plotly_chart(fig, use_container_width=True)

def get_credits():
    st.write("")
    #st.markdown("Made with ♡ by [Eric Tran](https://ericttran.com)")      
    #st.sidebar.info('This app is maintained by Eric Tran. You can learn more about me at www.ericttran.com.')
             

if __name__ == "__main__":
    main()


