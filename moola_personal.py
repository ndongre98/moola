from flask import Flask, render_template, url_for, request, session, redirect
import pymongo
import bcrypt
import json
import datetime
#from flask_pymongo import PyMongo

app = Flask(__name__)

connection = pymongo.MongoClient('mongodb+srv://admin:hello!@moola.wwfq4.mongodb.net/sample?retryWrites=true&w=majority')
print("connected!!")

# mongo = connection['moola']
# mongo.authenticate('moola_user', 'th2017')

#app.config['MONGO_DBNAME'] = 'moola'
#app.config['MONGO_HOST']
#app.config['MONGO_URI'] = 'mongodb://moola_user:h2017@ds131320.mlab.com:31320/moola'

#mongo = PyMongo(app)

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('loggedin'))

    return render_template('index.html')

@app.route('/loggedin', methods=['POST', 'GET'])
def loggedin():
    if request.method == 'POST':
        balance = mongo.db.users.distinct('balance', {'username' : session['username']})
        if 'deposit' in request.form:
            mongo.db.users.find_one_and_update({'username' : session['username']},
                { '$inc' : {'balance' : int(request.form['damt'])}})
            depos = mongo.db.users.distinct('deposits', {'username' : session['username']})
            check = False
            for d in depos:
                if d[0] == request.form['ddate']:
                    d[1] = d[1] + int(request.form['damt'])
                    check = True
            if check==False:
                mongo.db.users.find_one_and_update({'username' : session['username']},
                    { '$push' : {'deposits' : [request.form['ddate'], int(request.form['damt'])] }})
            else:
                mongo.db.users.find_one_and_update({'username' : session['username']},
                    { '$set' : {'deposits' : depos}})
        if 'withdrawal' in request.form:
            if balance[0] - int(request.form['wamt']) < 0:
                return "Withdrawal amount is too much!"
            mongo.db.users.find_one_and_update({'username' : session['username']},
                { '$inc' : {'balance' : -1 * int(request.form['wamt'])}})
            wdraw = mongo.db.users.distinct('withdrawals', {'username' : session['username']})
            check = False
            for w in wdraw:
                if w[0] == request.form['wdate']:
                    w[1] = w[1] + int(request.form['wamt'])
                    check = True
            if check == False:
                mongo.db.users.find_one_and_update({'username' : session['username']},
                    {'$push' : {'withdrawals' : [request.form['wdate'], int(request.form['wamt'])] }})
            else:
                mongo.db.users.find_one_and_update({'username' : session['username']},
                    { '$set' : {'withdrawals' : wdraw }})
    wdraw = mongo.db.users.distinct('withdrawals', {'username' : session['username']})
    for w in wdraw:
        w[0] = (((datetime.datetime.strptime(w[0], '%Y-%m-%d'))-datetime.datetime(1970,1,1)).total_seconds()) * 1000
    with open("static/withdrawals.JSON", 'w') as outfile:
        json.dump(wdraw, outfile)
    depos = mongo.db.users.distinct('deposits', {'username' : session['username']})
    for d in depos:
        d[0] = (((datetime.datetime.strptime(d[0], '%Y-%m-%d'))-datetime.datetime(1970,1,1)).total_seconds()) * 1000
    with open("static/deposits.JSON", 'w') as outfile:
        json.dump(depos, outfile)
    return render_template('loggedin.html', balance = mongo.db.users.distinct('balance', {'username' : session['username']})) 

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username' : request.form['username']})

    if login_user:
        #hashed = request.form['pass'].encode('utf-8')
        #if bcrypt.hashpw(hashed, login_user['password']) == login_user['password']:
        if request.form['pass'] == login_user['password']: 
            session['username'] = request.form['username']
            return redirect(url_for('index'))
    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'first_name' : request.form['fname'], 'last_name' : request.form['lname'], 
                        'username' : request.form['username'], 'password' : request.form['pass'], 'balance' : 0,
                        'withdrawals' : [], 'deposits' : [],
                        'address' : {'street_number' : request.form['hnum'],
                        'street_name' : request.form['street'], 'city' : request.form['city'],
                        'state' : request.form['state'], 'zipcode' : request.form['zip']}})
            session['username'] = request.form['username']
            return redirect(url_for('index'))       
        return 'That username already exists!'
    return render_template('register.html')

if __name__ == '__main__':
   app.secret_key = 'secret!!!'
   app.run(debug=True)