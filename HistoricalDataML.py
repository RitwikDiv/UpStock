#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 19:38:57 2017

@author: ANAND
"""

import matplotlib.pyplot as plt
from pathlib import Path
import ondemand
import requests
import pandas as pd
from pandas.compat import StringIO
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
from sklearn.svm import SVR

url = 'https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv'
sp500 = pd.read_csv(StringIO(requests.get(url).text))
sp500_tickers = sp500['Symbol'].tolist()

od = ondemand.OnDemandClient(api_key='barcharthackathon')

url = "http://ondemand.websol.barchart.com/getHistory.csv"
def make_querystr(ticker):
    return {
    "symbol": ticker,
    "type": "daily",
    "startDate": "20150101",
    "endDate":"20170101",
    "interval":"1",
    "order":"asc",
    "sessionFilter":"EFK",
    "splits":"true÷nds=true",
    "volume":"sum",
    "nearby":"1",
    "exchange":"NYSE,AMEX,NASDAQ",
    "backAdjust":"false",
    "daysToExpiration":"1",
    "contractRoll":"expiration",
    "apikey":"barcharthackathon"}

'''
path = Path('./history/')
path.mkdir()

def download(ticker):
    response = requests.get(url, params=make_querystr(ticker), stream=True)
    
    # Throw an error for bad status codes
    response.raise_for_status()
    
    with open(path / '{}.csv'.format(ticker), 'wb') as handle:
        for block in response.iter_content(4096):
            handle.write(block)
            
    print('done with {}'.format(ticker))


pool = mp.Pool(processes=32)
pool.map(download, sp500_tickers)
'''

companyName = input("Enter the company's code for which you want to analyse the stock market price: ")

df = pd.read_csv("./history/{}.csv".format(companyName), parse_dates = True, index_col = 1)
df = df.iloc[:, [1,2,3,4,5,6]]

dates= df["tradingDay"].tolist()
for i in range(len(dates)):
    dates[i] = int(dates[i].replace("-", ""))
prices = df["close"].tolist()


def predict_price(dates, prices, x):
	'''
	Builds predictive model and graphs it
	This function creates 3 models, each of them will be a type of support vector machine.
	A support vector machine is a linear seperator. It takes data that is already classified and tries
	to predict a set of unclassified data.
	So if we only had two data classes it would look like this
	It will be such that the distances from the closest points in each of the two groups is farthest away.
	When we add a new data point in our graph depending on which side of the line it is we could classify it
	accordingly with the label. However, in this program we are not predicting a class label, so we don't
	need to classify instead we are predicting the next value in a series which means we want to use regression.
	SVM's can be used for regression as well. The support vector regression is a type of SVM that uses the space between
	data points as a margin of error and predicts the most likely next point in a dataset.
	The predict_prices returns predictions from each of our models
	
	'''
	dates = np.reshape(dates,(len(dates), 1)) # converting to matrix of n X 1
	
	# Linear support vector regression model. 
	# Takes in 3 parameters: 
	# 	1. kernel: type of svm
	# 	2. C: penalty parameter of the error term
	# 	3. gamma: defines how far too far is.

	# Two things are required when using an SVR, a line with the largest minimum margin
	# and a line that correctly seperates as many instances as possible. Since we can't have both,
	# C determines how much we want the latter.

	# Next we make a polynomial SVR because in mathfolklore, the no free lunch theorum states that there are no guarantees for one optimization to work better
	# than the other. So we'll try both.

	# Finally, we create one more SVR using a radial basis function. RBF defines similarity to be the eucledian distance between two inputs
	# If both are right on top of each other, the max similarity is one, if too far it is a ze
	svr_lin = SVR(kernel= 'linear', C= 1e3) # 1e3 denotes 1000
	svr_poly = SVR(kernel= 'poly', C= 1e3, degree= 2)
	svr_rbf = SVR(kernel= 'rbf', C= 1e3, gamma= 0.1) # defining the support vector regression models
	
	svr_rbf.fit(dates, prices) # fitting the data points in the models
	svr_lin.fit(dates, prices)
	svr_poly.fit(dates, prices)

	# This plots the initial data points as black dots with the data label and plot
	# each of our models as well


	plt.scatter(dates, prices, color= 'black', label= 'Data') # plotting the initial datapoints 
	# The graphs are plotted with the help of SVR object in scikit-learn using the dates matrix as our parameter.
	# Each will be a distinct color and and give them a distinct label.
	plt.plot(dates, svr_rbf.predict(dates), color= 'red', label= 'RBF model') # plotting the line made by the RBF kernel
	plt.plot(dates,svr_lin.predict(dates), color= 'green', label= 'Linear model') # plotting the line made by linear kernel
	plt.plot(dates,svr_poly.predict(dates), color= 'blue', label= 'Polynomial model') # plotting the line made by polynomial kernel
	plt.xlabel('Date') # Setting the x-axis
	plt.ylabel('Price') # Setting the y-axis
	plt.title('Support Vector Regression') # Setting title
	plt.legend() # Add legend
	plt.show() # To display result on screen

	return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0] # returns predictions from each of our models


predicted_price = predict_price(dates, prices, 29)

print('The predicted prices are:', predicted_price)
