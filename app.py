from flask import Flask, abort, redirect, url_for, render_template, request, session
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
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
    	print("found user!")
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






