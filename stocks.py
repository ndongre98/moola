import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from dotenv import load_dotenv
import datetime as dt
load_dotenv()
import os
api_key = os.environ["API_KEY"]

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"
headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': api_key
	}

def getChart(symbol):
	query = {"interval":"1d","region":"US","symbol":symbol,"lang":"en","range":"5y"}
	data = requests.request("GET", url, headers=headers, params=query).json()
	timestamps = data["chart"]["result"][0]["timestamp"]
	prices = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
	chartData = [[timestamps[i]*1000, prices[i]] for i in range(len(prices))]	
	return chartData

def readChart():
	with open('res.json') as f:
		data = json.load(f)
		timestamps = data["chart"]["result"][0]["timestamp"]
		prices = data["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]
		chartData = [[timestamps[i]*1000, prices[i]] for i in range(len(prices))]	
		return chartData

def scrapeData(query, start, end):
	base_url = 'https://finance.yahoo.com/quote/{}/history?period1={}&period2={}&interval=1d&filter=history&frequency=1d'
	url = base_url.format(query, start, end)
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'lxml')
	table = soup.find_all('table')[0] 
	df = pd.read_html(str(table))[0]
	df = df[['Date', 'Adj Close**']]
	df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
	df['Date'] = (df['Date'] - dt.date(1970,1,1)).dt.total_seconds()
	dates = df.values.tolist()[:-1]
	return [[int(elem[0]), float(elem[1])] for elem in dates]


