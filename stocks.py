import requests
import json
from dotenv import load_dotenv
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
	print(data)
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