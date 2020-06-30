from flask import Flask, abort, redirect, url_for, render_template, request
from datetime import datetime as dt
import pymongo

client = pymongo.MongoClient('mongodb+srv://admin:hello@moola.wwfq4.mongodb.net/sample?retryWrites=true&w=majority')
db = client.db
users = db.users
# sampleUser = {
#   "username": "sample",
#   "password": "password",
# }
# people.insert_one(sampleUser)


app = Flask(__name__)

@app.route('/')
def index():
     return render_template(
        'index.html',
        title='Home Page',
        year=dt.now().year,
    )

@app.route('/login', methods=['POST'])
def login():
    users = db.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
    	print("found user!")
        #hashed = request.form['pass'].encode('utf-8')
        #if bcrypt.hashpw(hashed, login_user['password']) == login_user['password']:
        # if request.form['pass'] == login_user['password']: 
        #     session['username'] = request.form['username']
        #     return redirect(url_for('index'))
    print("Cannot find user")
    return 'Invalid username/password combination'