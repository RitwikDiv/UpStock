# -*- coding: utf-8 -*-
from datetime import datetime
import calendar
import requests
import ondemand
import pandas as pd
from pandas.compat import StringIO
od = ondemand.OnDemandClient(api_key='barcharthackathon')
states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

'''
url = "http://ondemand.websol.barchart.com/getNews.json"

url2 = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
sp500 = pd.read_csv(StringIO(requests.get(url2).text))
sp500_tickers = sp500['Symbol'].tolist()

def make_querystr(ticker):
    return {"apikey":"keith",
            "symbols":ticker,
            "sources":"AP",
            "displayType":"full"
            }
'''
ticker = input("Enter the company you want stock and company details for: ")

url = "http://ondemand.websol.barchart.com/getIncomeStatements.json"

symbol = ticker
income = od.income_statements(symbol, 'Quarter', count=1)['results'][0]
company = od.profile(symbol)['results'][0]
company_name = company['exchangeName']

url2 = "http://ondemand.websol.barchart.com/getFinancialHighlights.csv"

querystring = {"symbols":symbol,"fields":"lastQtrEPS,annualEPS,ttmEPS,sharesOutstanding,ttmNetIncome","apikey":"barcharthackathon"}
r = requests.request("GET", url2, params=querystring)
df = pd.read_csv(StringIO(r.text))

date = datetime.strptime(income['date'], '%Y-%m-%d')
weekday = calendar.day_name[date.weekday()]

from jinja2 import Template
from ballpark import business

Introtemplate = Template("""
COMPANY INTRO:
CHICAGO (AP) - {{ company_name }} ({{ ticker }}) on {{ weekday }} reported fiscal third-quarter net income of ${{ net_income }}.
{{ company_name }}, {{ state }}-based company said it's earnings, adjusted for non-recurring costs, came to ${{ lastQtrEPS }} per share. The results beat Wall Street expectations. 
{{ company_name}} also posted revenue of ${{ total_revenue }} Million in the period, also exceeding Street forecasts. 
The company also posted a dividend rate of {{an_dividend_rate}}% with a divided yeild of {{dividend_yield}}% """)

prefixes = {6: ' million'}  # ...fill in the rest
intro = Introtemplate.render(
    company_name=company_name,
    ticker=symbol,
    weekday=weekday,
    lastQtrEPS = df["lastQtrEPS"][0],
    total_revenue = df["annualRevenue"][0],
    dividend_yield = df["annualDividendYield"][0],
    an_dividend_rate = df["annualDividendRate"][0],
    net_income=business(income['netIncome'], prefixes=prefixes),
    state=states[company['state']]
)
print(intro)

url3 = "http://ondemand.websol.barchart.com/getQuote.csv"

querystring = {"symbols": symbol,"fields":"ask,bid, open, high, low, close,impliedVolatility, numTrades,fiftyTwoWkHigh,fiftyTwoWkLow","mode":"R","apikey":"barcharthackathon"}
r = requests.request("GET", url3, params=querystring)
df_quotes = pd.read_csv(StringIO(r.text))


Quotetemplate = Template("""
THE STOCKS PERFORMANCE WITH EXPLANATION:
CHICAGO (AP)- {{ company_name}} ({{ticker}}) on {{weekday}} has the following results:
The ({{ticker}}) stock opened today with ${{opening}} and is currently going at ${{last_price}} which gives a net change of {{percent_change}}%.
The low is at ${{low}} while the highest point of the day so far is ${{high}}. The 52 week high and lows are ${{fiftytwoWkhigh}} and ${{fiftytwowklow}}. 
The volatility of stock is {{volatility}}. Volatility refers to the degree of variation of a trading price changes over time. Higher the value the more susceptible to huge swings the stock is.
""")
prefixes = {6: ' million'}  # ...fill in the rest
quote = Quotetemplate.render(
    company_name=company_name,
    ticker=symbol,
    weekday=weekday,
    opening = df_quotes["open"][0],
    last_price = df_quotes["lastPrice"][0],
    percent_change = df_quotes["percentChange"][0],
    low = df_quotes["low"][0],
    high = df_quotes["high"][0],
    fiftytwoWkhigh = df_quotes["fiftyTwoWkHigh"][0],
    fiftytwowklow = df_quotes["fiftyTwoWkLow"][0],
    volatility = df_quotes["impliedVolatility"][0],
)
print(quote)

#stocks and sectors in stocks
#C
