from flask import Flask, render_template, request, redirect, url_for, flash, session
import os, databaseUtils, sqlite3

app = Flask(__name__)
DB_FILE = "storyGame.db"
databaseUtils.createUsersDB()

def successfulRegistration(username,password,email):
    passValid = len(password) > 0
    emailValid = len(email) > 0 and email.count('@') == 1
    db = sqlite3.connect(DB_FILE)
    # see if username is already taken
    try:
        command = "SELECT username FROM {} WHERE username = '{}';".format('users', username)
        usernameValid != len(list(db.execute(command)))
    except:
        return False
    db.commit()
    db.close()
    return passValid and emailValid and usernameValid

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
        session['username'] = request.args.get('username')
        databaseUtils.addToUserDB(request.args.get('username'), request.args.get('password'), request.args.get('email'))
        return redirect(url_for('main'))
    else:
        flash("Registration Failed")
        return redirect(url_for('register'))

@app.route('/login')
def login():
    if successfulLogin(request.args.get('username'), request.args.get('password')):
        session['loggedIn'] = True
        session['username'] = request.args.get('username')
        return redirect(url_for('main'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing'))

@app.route('/main')
def main():
    return render_template('main.html',
    username = session['username'],
    editedStories = databaseUtils.searchForAuthor(session['username'])[0],
    unEditedStories = databaseUtils.searchForAuthor(session['username'][1]))
    # searchForAuthor returns a list with two elements, the first element is
    # editedStories and the second is unEditedStories

@app.route('/logout')
def help():
    session['loggedIn'] = False
    flash('You have been logged out')
    return redirect(url_for('landing'))

@app.route('/viewLatest')
def viewLatest():
    return render_template('viewLatest.html'
    , title = "hi"
    , text = "hello")

@app.route('/viewAll')
def viewAll():
    return render_template('viewAll.html'
    , title = "hi"
    , text = "hello")

@app.route('/addForm')
def addForm():
    return render_template('add.html')
@app.route('/addPage')
def addPage():
    databaseUtils.createStory(request.args.get('storyTitle'))
    databaseUtils.addToStoryDB(request.args.get('storyTitle'), session['username'], request.args.get('text'))
    return render_template('viewAll.html',
                            title = request.args.get('storyTitle'),
                            text = request.args.get('text'))

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
