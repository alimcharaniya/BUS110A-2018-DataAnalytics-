# import the Flask class from the flask module
from flask import Flask, render_template, json, redirect, \
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

import pandas as pd 
#connect python to xlsx file and tell it which sheet to focus on.
xl = pd.ExcelFile('SalesDataFull.xlsx')

OrdersOnlyData = xl.parse('Orders')

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
    return render_template('index.html', name=test)  # render a template


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/insight-one')
@login_required
def insightOne():
    # print str(idList[1]).encode('utf-8')
    OrdersOnlyData = xl.parse('Orders')
    State_Profit_Col = OrdersOnlyData[['State','Profit']]


    profitsInOrderOfStatesArray =  State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False).values.tolist()[:10]
    statesInOrderOfProfitArray = State_Profit_Col.groupby(by='State').sum().sort_values(by='Profit', ascending = False).index.get_level_values(0).tolist()[:10]
    # print statesInOrderOfProfitArray[:10] #10 states in order
    # print statesInOrderOfProfitArray
    resultsArray = []
    for i in range(10):
        f = (statesInOrderOfProfitArray[i].decode('utf-8'))
        resultsArray.append(f)

    myString = " ".join(resultsArray)

    profitArray = []
    for d in range(10):
        p = (profitsInOrderOfStatesArray[d])
        profitArray.append(p)

    return render_template('insight-one.html', resultsArray=myString, profitArray = profitArray)  # render a template



# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        # print request.form
        try:
            user = Employee.query.filter_by(Email=request.form['username']).first()
            actualPass = user.Password

            if (actualPass == request.form['password']):
                session['logged_in'] = True
                flash('You were logged in.')
                
                return redirect(url_for('home'))
            else:
                error = 'Invalid Credentials. Please try again.'

        except:
            print ("This is an error message!")
            error = 'Invalid Credentials. Please try again.'
    
    return render_template('login.html', error=error)


def insertUserIntoDatabase(fName, lName, email, uid, password):
    print ('INSERTING USER TO DB')
    newUser = Employee(fName, lName, email, password, uid)
    try:
        db.session.add(newUser)
        db.session.commit()
    except:
        db.session.rollback()
        print ('CAUGHT AN ERROR!!')
        return False; 
    finally:
        db.session.close()  # optional, depends on use case

    return True


def checkInputs(email, uid, password):
     # 1. check if email address contains one '@' sign 
    if '@' in email: 
        print ('yes... email contains @ sign')
    else:
        return False

    #2. check if uid has more than 4 characters AND is only numbers
    if (len(uid) > 3):
        if(uid.isdigit() == False):
            return False
    else:
        return False; 
    
    #3. check if password has more than 5 characters 
    if (len(password) < 5):
        return False
    
    # If no triggers are hit, return true
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        # User submits info for a new user..
        # We know all fields exist bc the log is implemented in front end
        fName = request.form['fName'] #safe to assume this is provided
        lName = request.form['lName'] #safe to assume this is provided
        email = request.form['email'] #check if valid email 
        uid = request.form['id'] #4 number minimum, no letters.
        password = request.form['pass']

        if(checkInputs(email, uid, password)):
            didInsert = insertUserIntoDatabase(fName, lName, email, uid, password)

            if(didInsert == False):
                print ('FAILED TO INSERT')
                error = 'User with that data already exists'
                return render_template('register.html', error = error)  # render a template
            else:
                print ('SUCCESSFUL INSERT')   
                error = 'SUCCESSFULLY ADDED NEW EMPLOYEE' 
                return render_template('register.html', error = error)  # render a template

        else:
            print ('NO, TELL THE USER TO CHECK THEIR INPUTS...')
            error = 'You must enter a valid email, numbers only for employee ID and minimum 4 characters, at least 6 characters for password...'

            return render_template('register.html', error = error)  # render a template

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



