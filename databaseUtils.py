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
        editedStories.append(list(db.execute("SELECT * FROM {} WHERE author = '{}';".format(story, username))))
    print (editedStories)
    db.commit()
    db.close()
