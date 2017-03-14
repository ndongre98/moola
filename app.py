"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask,render_template
"""import app"""

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/personal')
def personal():
    """Renders the contact page."""
    return render_template(
        'personal.html',
        title='Personal',
        year=datetime.now().year,
        message='Personal Finance'
    )

@app.route('/global')
def global_():
    #Renders the about page.
    return render_template(
        'global.html',
        title='Global',
        year=datetime.now().year,
        message='Global Finance'
    )


"""
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('yahoofinance.html')
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')
"""
