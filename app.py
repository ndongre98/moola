from flask import Flask, abort, redirect, url_for, render_template, request, session, jsonify
from datetime import datetime as dt
import pymongo
import db
import json

app = Flask(__name__)
app.secret_key = b'9\xbb\xa7\xac\xac\xbci?\xe4\xc3\x13\xb8y\xf0\xd2!'

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
    if (db.findUser(request.form['username'])):
    	session['username'] = request.form['username']
    	return redirect(url_for('dashboard'))
        #hashed = request.form['pass'].encode('utf-8')
        #if bcrypt.hashpw(hashed, login_user['password']) == login_user['password']:
        # if request.form['pass'] == login_user['password']: 
        #     session['username'] = request.form['username']
        #     return redirect(url_for('index'))

    #TODO: Have some sort of logic to let user know the username/password was invalid
    print("Cannot find user")
    return 'Invalid username/password combination'


#TODO: registration page

#TODO: route to dashboard
@app.route('/dashboard')
def dashboard():
	if 'username' in session:
		return render_template('dashboard.html')

	return "User not logged in"


@app.route('/query_stock_sentiment')
def query_stock_sentiment():
    query = request.args.get("query", '', type=str).lower()
    response = db.getSentiment(query)
    del response["_id"]
    return json.dumps(response, default=str)




