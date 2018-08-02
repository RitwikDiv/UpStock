# -*- coding: utf-8 -*-

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.summarization import summarize
import requests
import ondemand
import pandas as pd
from pandas.compat import StringIO
od = ondemand.OnDemandClient(api_key='barcharthackathon')

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

ticker = input("Enter the company you want news articles for: ")

r = requests.request('GET', url, params=make_querystr(ticker))

news = r.json()

from bs4 import BeautifulSoup
for i in range(len(news)):
    story_html = news['results'][i]['fullText']
    soup = BeautifulSoup(story_html, 'lxml')
    text = soup.get_text()
    print("Article:  ")
    print(text)
    print("summary:")
    print(news['results'][i]['headline']+ "\n")
    print(summarize(text, 0.1)+ '\n'+ '\n')
    