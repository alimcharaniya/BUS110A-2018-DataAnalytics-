# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///OS_Employee.db'

# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    # posts = db.session.query(BlogPost).all()

    test = db.session.query(Employee).all()
    names = ["alim", "sahand", "christian"]
    return render_template('index.html', name=test)  # render a template


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        # print request.form

        user = Employee.query.filter_by(FirstName=request.form['username']).first()
        actualPass = user.Password

        if (actualPass == request.form['password']):
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')  # render a template



@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# connect to database
def connect_db():
    return sqlite3.connect('OS_Employee.db')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)