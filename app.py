# COMPLETELY UNTESTED

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

import databaseUtils

import sqlite3

app = Flask(__name__)

DB_FILE="storyGame.db"

db = sqlite3.connect(DB_FILE)

db.commit()
db.close()

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
    # usernameValid = db.execute("{} NOT IN (users|username)".format(username1))
    return passValid and emailValid # and usernameValid

def successfulLogin(username1, password1):
    db = sqlite3.connect(DB_FILE)
    try:
        userPass = list(db.execute("SELECT password FROM users WHERE username = '" + username1 + "';"))[0][0]
        db.commit()
        db.close()
        return password1 == userPass
    except:
        db.commit()
        db.close()
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
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/processRegistration')
def processRegistration():
    if successfulRegistration(request.args.get('username'), request.args.get('password'), request.args.get('email')):
        session['loggedIn'] = True
        databaseUtils.addToUserDB(request.args.get('username'), request.args.get('password'), request.args.get('email'))
        return redirect(url_for('main'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing'))

@app.route('/login')
def login():
    if successfulLogin(request.args.get('username'), request.args.get('password')):
        session['loggedIn'] = True
        session['username'] = request.args.get('username')
        return redirect(url_for('main'))
    else:
        flash("Registration Failed")
        return redirect(url_for('landing'))

@app.route('/main')
def main():
    print (session['username'])
    databaseUtils.searchForAuthor(session['username'])
    return render_template('main.html') # other elements here in future,
                                        # like dropdown forms

@app.route('/logout')
def help():
    session['loggedIn'] = False
    return redirect(url_for('landing'))

@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/addForm')
def addForm():
    return render_template('add.html')
@app.route('/addPage')
def addPage():
    databaseUtils.createStory(request.args.get('storyTitle'))
    databaseUtils.addToStoryDB(request.args.get('storyTitle'), session['username'], request.args.get('text'))
    return render_template('view.html',
                            title = request.args.get('storyTitle'),
                            text = request.args.get('text'))

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
