#Functions for database
import sqlite3

DB_FILE="storyGame.db"

def createUsersDB():
    db = sqlite3.connect(DB_FILE)
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT);")
    db.commit()
    db.close()

def addToUserDB(userUsername, userPassword, userEmail):
    db = sqlite3.connect(DB_FILE)
    db.execute("INSERT INTO users VALUES ('{}', '{}', '{}');".format(userUsername, userPassword, userEmail))
    db.commit()
    db.close()

def createStory(title):
    db = sqlite3.connect(DB_FILE)
    db.execute("CREATE TABLE IF NOT EXISTS {} (author TEXT PRIMARY KEY, entry TEXT);".format(title))
    db.commit()
    db.close()

def addToStoryDB(title, author, entry):
    db = sqlite3.connect(DB_FILE)
    db.execute("INSERT INTO {} VALUES ('{}', '{}');".format(title, author, entry))
    db.commit()
    db.close()

def searchForAuthor(username): #session['username']
    db = sqlite3.connect(DB_FILE)
    # get list of all stories
    masterList = list(db.execute("SELECT name FROM sqlite_master WHERE type='table';"))[1:]
    editedStories = []
    for story in masterList:
        story = story[0]
        # returns the user's username if the user has edited the story
        command = "SELECT author FROM {} WHERE EXISTS(SELECT * FROM {} WHERE author = '{}');"
        command = command.format(story, story, username)
        if len(list(db.execute(command))) != 0 and username == list(db.execute(command))[0][0]:
            # if they did, append that story to the list of stories they've edited
            editedStories.append(story)
    print (editedStories)
    db.commit()
    db.close()
