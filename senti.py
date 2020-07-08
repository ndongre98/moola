import json
import pymongo
import train

client = pymongo.MongoClient('mongodb+srv://admin:hello@moola.wwfq4.mongodb.net/sample?retryWrites=true&w=majority')
db = client.db

def addUser(username, password):
	users = db.users
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
