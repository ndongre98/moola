import json
import pymongo
import train

client = pymongo.MongoClient('mongodb+srv://admin:hello@moola.wwfq4.mongodb.net/sample?retryWrites=true&w=majority')
db = client.db
users = db.users
stocks = db.stocks

def findUser(username):
	user = users.find_one({'username' : username})
	return (user != None)

def addUser(username, password):
	new_user = {
	  "username": username,
	  "password": password,
	}
	users.insert_one(new_user)

def addSentiment(query):
	stocks = db.stocks
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