"""
Routes and views for the flask application.
"""
from flask import Flask, render_template, url_for, request, session, redirect
import pymongo
import bcrypt
import json
import datetime
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


