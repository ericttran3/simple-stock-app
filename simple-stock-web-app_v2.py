import pandas as pd
import plotly.graph_objs as go
import altair as alt
import streamlit as st
import yfinance as yf
import datetime
import time
from dateutil.relativedelta import relativedelta # to add days or years


###################################################################################################################
# Page Layout Settings
###################################################################################################################

# Set Page Layout
st.set_page_config(
    page_title="Simple Stock App",
    page_icon = "💲",
    initial_sidebar_state="expanded",
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

# Web Scraping Wikipedia
# Choose an Index: S&P 500, DIJA, Nasdaq Composite, Nikkei 225, FTSE 100
# S&P 500 = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
# DIJA 30 = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average#Components'
# Nasdaq = 'https://en.wikipedia.org/wiki/Nasdaq-100#Components'
# Russell 1000 = 'https://en.wikipedia.org/wiki/Russell_1000_Index'

# Execute Main Function
def main():
    # Set Variables
    start_exec = time.time()
    start = datetime.date(2016, 1, 1)
    end = datetime.date.today()

    # App title
    st.markdown('''
    # Simple Stock App
    A stock app to research stocks and track performance over time. This tool is used for educational purposes only and does not provide any financial investment advice. Do your own research and due dilligence before buying or selling stocks. Invest at your own risk. This data is updated every 1 hour and may be delayed.
    ''')

    # Sidebar
    st.sidebar.image('../assets/stock-market-xsmall.png')
    st.sidebar.markdown('''
    ## Navigation
    - Select start and end dates for historical data
    - Select a stock ticker by typing in the box
    - Expand accordions to see additional data
    - Charts are interactive. Zoom in, zoom out. Double click to reset
    ''')
    st.sidebar.subheader('Query Parameters')

    # Variables
    with st.sidebar.beta_container():
        start = datetime.date(2016, 1, 1)
        end = datetime.date.today()

        col1, col2 = st.beta_columns(2)
        start_date = col1.date_input("Start date", start)
        end_date = col2.date_input("End date", end)

    # Call function to pull in NASDAQ stock data
    ticker_list = get_data()

    # Show dataframe
    expander_bar = st.beta_expander("Show NASDAQ Stock List")
    with expander_bar.beta_container():
        sector = ticker_list['Sector'].unique()
        selected_sector = expander_bar.selectbox('Sector', sector)
        df_selected_sector = ticker_list[ticker_list['Sector'] == selected_sector]
        expander_bar.text('Data Dimensions: {} rows and {} columns.'.format(df_selected_sector.shape[0],df_selected_sector.shape[1]))
        expander_bar.dataframe(df_selected_sector)
    
    st.write("")

    # Get ticker symbol from list of available tickers
    ticker_symbol = ticker_list[['Symbol', 'Name']]
    ticker_symbol['Name'] = ticker_list['Symbol'] + " | " + ticker_list['Name']

    records = ticker_symbol.to_dict("records")

    # selected_Data = st.selectbox("Select from df", options=records, format_func=)
    #st.write(selected_Data)

    tickerSymbol = st.sidebar.selectbox('Stock Ticker', ticker_symbol['Name']) # Select ticker symbol

    sb_placeholder = st.sidebar.empty()
    sb_placeholder.text('Processing...')

    tickerSymbol = tickerSymbol.split(" | ")[0]

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
    | Sector | {sector} | A sector is an area of the economy in which businesses share the same or a related product or service. |
    | Industry | {industry} | The term industry refers to a series of companies that operate in a similar business sphere, and its categorization is more narrow. |
    | Country | {country} | The country the company was originated or does business in. |
    | Market Cap | {market_cap} | Market capitalization refers to the total dollar market value of a company's outstanding shares of stock. Commonly referred to as "market cap," it is calculated by multiplying the total number of a company's outstanding shares by the current market price of one share. |
    | Beta | {beta} | Beta is a measure of the volatility—or systematic risk—of a security or portfolio compared to the market as a whole.  |    
    | P/E Ratio | {pe_ratio} | The price-to-earnings ratio (P/E ratio) is the ratio for valuing a company that measures its current share price relative to its per-share earnings (EPS). The price-to-earnings ratio is also sometimes known as the price multiple or the earnings multiple.  |    
    | EPS | {eps} | Earnings per share (EPS) is calculated as a company's profit divided by the outstanding shares of its common stock. The resulting number serves as an indicator of a company's profitability.  |    
    | PEG Ratio | {peg_ratio} | The price/earnings to growth ratio (PEG ratio) is a stock's price-to-earnings (P/E) ratio divided by the growth rate of its earnings for a specified time period. The PEG ratio is used to determine a stock's value while also factoring in the company's expected earnings growth, and it is thought to provide a more complete picture than the more standard P/E ratio.  |    
    | P/S Ratio | {price_to_sale} | The price-to-sales (P/S) ratio is a valuation ratio that compares a company’s stock price to its revenues. It is an indicator of the value that financial markets have placed on each dollar of a company’s sales or revenues.  |    
    | P/B Ratio | {price_to_book} | Companies use the price-to-book ratio (P/B ratio) to compare a firm's market capitalization to its book value. It's calculated by dividing the company's stock price per share by its book value per share (BVPS).  |    
    | EV/R | {enterprise_value} | The enterprise value-to-revenue multiple (EV/R) is a measure of the value of a stock that compares a company's enterprise value to its revenue. EV/R is one of several fundamental indicators that investors use to determine whether a stock is priced fairly.  |    
    | EBITDA/EV | {ebitda} | The EBITDA/EV multiple is a financial valuation ratio that measures a company's return on investment (ROI).   |    
    | Profit Margin | {profit}  | A metric used to gauge how a company or business makes money. Expressed as percentage, profit margin indicatses how many cents of profit has been generated for each dollar of sale. |    
    | Net Income | {net_income} | Net income (NI), also called net earnings, is calculated as sales minus cost of goods sold, selling, general and administrative expenses, operating expenses, depreciation, interest, taxes, and other expenses.  |    
    | Dividend Yield | {dividend_yield} | The dividend yield–displayed as a percentage–is the amount of money a company pays shareholders for owning a share of its stock divided by its current stock price.  |    
    | Dividend Rate | {dividend_rate} | Dividend rate, expressed as a percentage or yield, is a financial ratio that shows how much a company pays out in dividends each year relative to its stock price.  |    
    | Payout Ratio | {payout} | The payout ratio, also known as the dividend payout ratio, shows the percentage of a company's earnings paid out as dividends to shareholders.  |    
    | Forward EPS | {forward_eps} | Forward earnings are an estimate of a company's earnings for upcoming periods. Forward earnings project future revenues, margins, tax rates, and other financial data. |    
    | Trailing PE | {trailing_pe} | Trailing price-to-earnings (P/E) is a relative valuation multiple that is based on the last 12 months of actual earnings. It is calculated by taking the current stock price and dividing it by the trailing earnings per share (EPS) for the past 12 months.  |    
    | Forward PE | {forward_pe} | Forward price-to-earnings (forward P/E) is a version of the ratio of price-to-earnings (P/E) that uses forecasted earnings for the P/E calculation.  |    
    | Earnings Growth | {earnings_growth} | Growth rates are used to express the annual change in a variable as a percentage. Growth rates can be beneficial in assessing a company’s performance and to predict future performance.  |    
    | Volume | {volume} | Volume is the number of shares of a security traded between its daily open and close. Trading volume, and changes to volume over the course of time, are important inputs for technical traders.  |    
    | Shares Outstanding | {shares_outstanding} | Shares outstanding refer to a company's stock currently held by all its shareholders, including share blocks held by institutional investors and restricted shares owned by the company’s officers and insiders.  |    
    | Shares Float | {shares_float} | Floating stock refers to the number of shares a company has available to trade in the open market. To calculate a company's floating stock, subtract its restricted stock and closely held shares from its total number of outstanding shares.  |    
    | % Held by Insiders | {pct_insiders} | Insiders are a company's officers, directors, relatives, or anyone else with access to key company information before it's made available to the public. By watching the trading activity of corporate insiders and large institutional investors, it's easier to get a sense of a stock's prospects. |    
    | % Held by Institutions | {pct_institutions} | An institutional investor is a company or organization that invests money on behalf of other people. Mutual funds, pensions, and insurance companies are examples.  |    
    | Shares Short | {shares_short} | A short, or a short position, is created when a trader sells a security first with the intention of repurchasing it or covering it later at a lower price.   |    
    | Shares Short Ratio | {shares_short_ratio} | The short Interest ratio is a simple formula that divides the number of shares short in a stock by the stock's average daily trading volume. The short interest ratio is a quick way to see how heavily shorted a stock may be versus its trading volume. |    
    | Short Percent to Float | {short_pct_float} |  When a company's short interest is high (above 40%), it frequently means a large portion of investors anticipate the shares will go down in value and are looking to profit from the decline or are using the short as a hedge against a possible decline. |    
    | Shares Short Previous Month | {shares_short_pm} |  The number of shares that were shorted in the previous month. This metric can serves as a market sentiment indicator for investors. |    
    """.format(sector=sector,industry=industry, country=country, market_cap=market_cap, beta=beta,
                pe_ratio=pe_ratio, eps=eps, peg_ratio=peg_ratio, price_to_sale=price_to_sale, price_to_book=price_to_book,
                enterprise_value=enterprise_value, ebitda=ebitda, profit=profit, net_income=net_income, dividend_yield=dividend_yield,
                dividend_rate=dividend_rate, payout=payout, forward_eps=forward_eps, trailing_pe=trailing_pe,
                forward_pe=forward_pe, earnings_growth=earnings_growth, volume=volume, shares_outstanding=shares_outstanding,
                shares_float=shares_float, pct_insiders=pct_insiders, pct_institutions=pct_institutions,
                shares_short=shares_short, shares_short_ratio=shares_short_ratio, short_pct_float=short_pct_float,
                shares_short_pm=shares_short_pm
    ))
    expander_bar.write("")

    expander_bar = st.beta_expander("Additional Information")
    expander_bar.write(tickerData.info)

    # Get historical stock price for the data range with periods 
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) # get the historical prices for this ticker
    tickerDf['Date'] = tickerDf.index
    tickerDf['Year'] = pd.DatetimeIndex(tickerDf.index).year

    get_visualizations(tickerDf)


def get_visualizations(tickerDf):

    # Time Series Line Chart
    with st.beta_container():
        st.write("""
        ### Closing Price
        """)
        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Date'], empty='none')

        line = alt.Chart(tickerDf).mark_line(interpolate='basis').encode(
            x=alt.X("Date", axis=alt.Axis(title='')),
            y=alt.X('Close', axis=alt.Axis(title='')),
            color=alt.Color('Year')
        )

        selectors = alt.Chart(tickerDf).mark_point().encode(
            x="Date",
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        text = line.mark_text(align='center', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'Close', alt.value(' '))
        )

        rules = alt.Chart(tickerDf).mark_rule(color='gray').encode(
            x="Date",
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        chart = alt.layer(
            line, selectors, points, rules, text
            ).interactive()

        st.altair_chart(chart, use_container_width=True)
        
    # Time Series Volume Chart
    with st.beta_container():
        st.write("""
        ### Volume
        """)
        nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Date'], empty='none')

        bar = alt.Chart(tickerDf).mark_bar(interpolate='basis').encode(
            x=alt.X("Date", axis=alt.Axis(title='')),
            y=alt.X('Volume', axis=alt.Axis(format='#', title='')),
            color=alt.Color('Year')
        )

        selectors = alt.Chart(tickerDf).mark_point().encode(
            x="Date",
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        points = bar.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        text = bar.mark_text(align='center', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'Volume', alt.value(' '))
        )

        rules = alt.Chart(tickerDf).mark_rule(color='gray').encode(
            x="Date",
        ).transform_filter(
            nearest
        )

        # Put the five layers into a chart and bind the data
        chart = alt.layer(
            bar, selectors, points, rules, text
            ).interactive()

        st.altair_chart(chart, use_container_width=True)
    

    # Scatter Flot
    with st.beta_container():
        st.write("""
        ### Volume x Price
        """)
        scatter_chart = st.altair_chart(
            alt.Chart(tickerDf).mark_circle(size=60).encode(
                x=alt.X("Volume", axis=alt.Axis(title='')),
                y=alt.X('Close', axis=alt.Axis(title='')),
                color='Year',
                tooltip=['Volume', 'Close', 'Year', 'Date']
        ), use_container_width=True)


    # Candlesticks OHLC
    with st.beta_container():
        st.write("""
        ### Candlesticks (OHLC)
        """)
        base = alt.Chart(tickerDf).encode(
        alt.X('Date', axis=alt.Axis(labelAngle=0, title='')),
        color=alt.condition("datum.Open <= datum.Close",alt.value("#06982d"), alt.value("#ae1325")),
        tooltip=['Date', 'Open', 'High', 'Low', 'Close']
        )

        chart = alt.layer(
            base.mark_rule().encode(alt.Y('Low', title='', scale=alt.Scale(zero=False)), 
                                    alt.Y2('High')),
            base.mark_bar().encode(alt.Y('Open', title=''), 
                                    alt.Y2('Close')),
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

        fig = go.Figure()

def get_credits():
    st.write("")
    # st.markdown("Made with ♡ by [Eric Tran](https://ericttran.com)")      
    st.markdown('This app is maintained by Eric Tran. You can learn more about me at [www.ericttran.com](https://www.ericttran.com).')
                  

if __name__ == "__main__":
    main()