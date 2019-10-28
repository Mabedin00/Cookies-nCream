from flask import Flask, render_template, request, redirect, url_for, flash, session
import os, databaseUtils, sqlite3

app = Flask(__name__)
DB_FILE = "storyGame.db"

databaseUtils.createUsersDB()

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

@app.route('/login')
def login():
    loginData = databaseUtils.successfulLogin(request.args.get('username'), request.args.get('password'))
    if not loginData[0]: flash("Username does not exist")
    if not loginData[1]: flash("Password invalid")
    if loginData[0] and loginData[1]:
        session['loggedIn'] = True
        session['username'] = request.args.get('username')
        return redirect(url_for('main'))
    else:
        return redirect(url_for('landing'))

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/processRegistration')
def processRegistration():
    registration = databaseUtils.successfulRegistration(request.args.get('username')
                                                      , request.args.get('password')
                                                      , request.args.get('email'))
    if not registration[0]: flash("Username Taken")
    if not registration[1]: flash("Please enter a password")
    if not registration[2]: flash("Please enter a valid email address")

    if registration[0] and registration[1] and registration[2]:
        session['loggedIn'] = True
        session['username'] = request.args.get('username')
        databaseUtils.addToUserDB(request.args.get('username'), request.args.get('password'), request.args.get('email'))
        return redirect(url_for('main'))
    else:
        return redirect(url_for('register'))

@app.route('/main')
def main():
    return render_template('main.html',
    username = session['username'],
    editedStories = databaseUtils.searchForAuthor(session['username'])[0],
    unEditedStories = databaseUtils.searchForAuthor(session['username'])[1])
    # searchForAuthor returns a list with two elements, the first element is
    # editedStories and the second is unEditedStories

@app.route('/logout')
def help():
    session['loggedIn'] = False
    flash('You have been logged out')
    return redirect(url_for('landing'))

@app.route('/processAppendView')
def processAppendView():
    session['story'] = request.args.get('story')
    if session['story'] == None:
        flash("You can't view nothing")
        return redirect(url_for('main'))
    return render_template('append.html',
                           story = session['story'],
                           text = databaseUtils.getLatestEntry(session['story']))

@app.route('/appendToStory')
def appendToStory():
    story = session['story']
    databaseUtils.addToStoryDB(story, session['username'], request.args.get('newText'))
    return redirect(url_for('viewAll'))


@app.route('/viewAll')
def viewAll():
    if request.args.get('story') == None and session['story'] == None:
        flash("You can't view nothing")
        return redirect(url_for('main'))
    return render_template('viewAll.html'
                         , title = session['story']
                         , text = databaseUtils.getEntries(session['story']))

@app.route('/addForm')
def addForm():
    return render_template('add.html')
@app.route('/addPage')
def addPage():
    if databaseUtils.createStory(request.args.get('storyTitle')):
        databaseUtils.addToStoryDB(request.args.get('storyTitle'), session['username'], request.args.get('text'))
        return render_template('viewAll.html',
                                title = request.args.get('storyTitle'),
                                text = databaseUtils.getLatestEntry(request.args.get('storyTitle')))
    else:
        flash("Story name already taken")
        return redirect(url_for('main'))

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
