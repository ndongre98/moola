from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify
from datetime import datetime as dt
import pymongo
import db
import json

from dotenv import load_dotenv
load_dotenv()
import os
key = os.environ.get("APP_SECRET_KEY")

app = Flask(__name__)
app.secret_key = key

@app.route('/')
def index():
     return render_template(
        'index.html',
        title='Home Page',
        year=dt.now().year,
    )

#TODO: password encryption
@app.route('/login', methods=['POST'])
def login():
    if (db.findUser(request.form['username'], request.form['password'])):
        session['username'] = request.form['username']
        return redirect(url_for('dashboard'))

    #TODO: Have some sort of logic to let user know the username/password was invalid
    print("Cannot find user")
    return 'Invalid username/password combination'

#TODO: registration page
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registration', methods=['POST'])
def registration():
    username = request.form["username"]
    password = request.form["password"]
    print(username, password)
    if (db.userExists(username)):
        return json.dumps({"status" : True})
    db.addUser(username, password)
    session['username'] = request.form['username']
    return json.dumps({"status" : False})

#TODO: route to dashboard
@app.route('/dashboard')
def dashboard():
    concat = (lambda x,y,z: x + "," + y + "," + z)
    if 'username' in session:
        stockList = db.getAllStocks()
        keywords = [{"data_tokens" : concat(elem["name"], elem["symbol"], elem["nickname"]), "name" : elem["name"], "symbol" : elem["symbol"]} for elem in stockList]
        return render_template('dashboard.html', keywords=keywords)
    return "User not logged in"


@app.route('/query_stock_info')
def query_stock_sentiment():
    query = request.args.get("query", '', type=str)
    print("querying...", query)
    senti_response = db.getSentiment(query)
    del senti_response["_id"]
    stock_response = db.findStockChart(query)
    response = {"symbol" : query, "sentiment_analysis" : senti_response, "chart_data" : stock_response}
    return json.dumps(response, default=str)



