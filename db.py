import json
import pymongo
import train
import bcrypt
import stocks as st
from dotenv import load_dotenv
load_dotenv()
import os
db_key = os.environ.get("MONGO_KEY")

client = pymongo.MongoClient(db_key)
db = client.db
users = db.users
stocks = db.stocks
stockMap = db.stockMap
stockCharts = db.stockCharts

def getDB():
	return db

def findUser(username, password):
	user = users.find_one({'username' : username})
	return user and bcrypt.checkpw(password.encode('utf-8'), user["password"])

def addUser(username, password):
	hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	new_user = {
	  "username": username,
	  "password": hashed,
	}
	users.insert_one(new_user)

def addSentiment(query):
	analysis_obj = train.train(query)
	if (analysis_obj):
		stocks.insert_one(analysis_obj)
	else:
		print("Error: did not receive obj")

def getSentiment(query):
	res = stocks.find_one({"name" : query})
	if (res):
		return res
	else:
		print("Couldn't find ", query, " in db")
		addSentiment(query)
		return stocks.find_one({"name" : query})

def findStockSymbol(query):
	name_res = stockMap.find({"name": {"$regex": query, "$options" : 'i'}})
	sym_res = stockMap.find({"symbol": {"$regex": query, "$options" : 'i'}})
	nick_res = stockMap.find({"nickname": {"$regex": query, "$options" : 'i'}})
	name_res_list = [entry for entry in name_res]
	sym_res_list = [entry for entry in sym_res]
	nick_res_list = [entry for entry in nick_res]
	res = set(name_res_list + sym_res_list + nick_res_list)
	return res[0]

def getAllStocks():
	res = stockMap.find()
	return [{"symbol" : entry["symbol"], "name" : entry["name"], "nickname" : entry["nickname"]} for entry in res]

def addStockChart(symbol):
	chartData = st.readChart()
	elem = {"symbol" : symbol, "data" : chartData}
	stockCharts.insert_one(elem)

def findStockChart(symbol):
	res = stockCharts.find_one({"symbol" : symbol})
	if (res):
		return res["data"]
	else:
		print("Couldn't find stock data for ", symbol, " in db")
		addStockChart(symbol)
		return stockCharts.find_one({"symbol" : symbol})


