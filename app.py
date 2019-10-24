
# COMPLETELY UNTESTED

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

import databaseUtils

import sqlite3

app = Flask(__name__)

DB_FILE="storyGame.db"

db = sqlite3.connect(DB_FILE, check_same_thread = False)
cursor = db.cursor()

databaseUtils.createUsersDB()

# This code skeleton is just for the logging in part, not for the
# actual page part.
# Also, here both the login and register forms
# are just on the main route instead of being on their separate pages.
# This is for simplicity, I think doing that would require two more routes.
# We could change it later if we think it looks better.

def successfulRegistration(username1,password,email):
    passValid = len(password) > 0
    emailValid = len(email) > 0 and email.count('@') == 1
    usernameValid = db.execute("{} NOT IN (users|username)".format(username1))
    return passValid and emailValid and usernameValid

def successfulLogin(username, password):
    try:
        return password == db.execute("SELECT password FROM users WHERE username = {}".format(username))
    except:
        return False

def loggedIn():
    try:
        return session['loggedIn']
    except:
        session['loggedIn'] = False
        return session['loggedIn']

# ///////////////////////////////////////

@app.route('/')
def landing():
    # form for login
    # button redirecting to register route
    if loggedIn():
        return redirect(url_for('/main'))
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/processRegistration')
def processRegistration():
    if successfulRegistration(request.args.get('username'), request.args.get('password'), request.args.get('email')):
        print ("Ran successfulRegistration")
        databaseUtils.addToUserDB(request.args.get('username')
                               , request.args.get('password')
                               , request.args.get('email'))
        return redirect(url_for('main'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing'))

@app.route('/login')
def login():
    if successfulLogin(request.args.get('username'), request.args.get('password')): # function is a placeholder
        session['loggedIn'] = true
        session['username'] = request.args.get('username')
        session['password'] = request.args.get('password')
        return redirect(url_for('main()'))
    else:
        flash("Registration Failed")
        return redirect(url_for('landing'))

@app.route('/main')
def main():
    return render_template('main.html') # other elements here in future,
                                        # like dropdown forms

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/add')
def add():
    return render_template('add.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
