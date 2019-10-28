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
    # returns a list with two booleans, the first saying if username is valid
    # and the second saying if pass is valid
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
    # returns a list with three booleans, the first saying if username is valid,
    # the second saying if pass is valid, and the third if email is valid
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
        # main is the route which allows viewing, adding stories, etc.
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

# below are the three main routes of forms:
# 1. viewAll -> view all entries of a selected story
# 2. processAppendView -> view latest entry of unedited story
    # 2a. If the user wants to add to the story, that is processed by appendToStory
# 3. addForm -> add a new story
    # 3a. If the user wants to add a story, that is processed by addPage

@app.route('/viewAll')
def viewAll():
    # user could be directed here either by viewAll form
    # in which case session['story'] would be None, or by
    # appendToStory, in which case request.get.args('story')
    # would be None.
    # this sets story to the arg that isn't None. If they are
    # both None, there's an error
    if request.args.get('story') == None:
        story = session['story']
    if session['story'] == None:
        story = request.args.get('story')
    if session['story'] != None and request.args.get('story') != None:
        story = session['story']
    if request.args.get('story') == None and session['story'] == None:
        flash("You can't view nothing")
        return redirect(url_for('main'))
    return render_template('viewAll.html'
                         , title = story
                         , text = story)

@app.route('/processAppendView')
def processAppendView():
    # if they tried to view an unedited story without selecting an option from the dropdown
    if request.args.get('story') == None:
        flash("You can't add to nothing")
        return redirect(url_for('main'))
    session['story'] = request.args.get('story')
    return render_template('append.html',
                           story = session['story'],
                           text = databaseUtils.getLatestEntry(session['story']))
@app.route('/appendToStory')
def appendToStory():
    story = session['story']
    databaseUtils.addToStoryDB(story, session['username'], request.args.get('newText'))
    return redirect(url_for('viewAll'))

@app.route('/addForm')
def addForm():
    return render_template('add.html')
@app.route('/addPage')
def addPage():
    # createStory returns a boolean which is true or false depending on if the story name is taken
    # if it is not, it creates the story table
    if databaseUtils.createStory(request.args.get('storyTitle')):
        session['story'] = request.args.get('storyTitle')
        databaseUtils.addToStoryDB(request.args.get('storyTitle'), session['username'], request.args.get('text'))
        return render_template('viewAll.html',
                                title = request.args.get('storyTitle'),
                                text = databaseUtils.getLatestEntry(request.args.get('storyTitle')))
    else:
        flash("Story name already taken")
        return redirect(url_for('main'))

@app.route('/logout')
def help():
    session['loggedIn'] = False
    flash('You have been logged out')
    return redirect(url_for('landing'))

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.debug = True
    app.run()
