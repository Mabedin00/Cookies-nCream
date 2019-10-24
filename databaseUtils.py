#Functions for database
import sqlite3

DB_FILE="storyGame.db"

def createUsersDB():
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT);")
    db.commit()
    db.close()

def addToUserDB(userUsername, userPassword, userEmail):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    db.execute("INSERT INTO users VALUES ('{}', '{}', '{}');".format(userUsername, userPassword, userEmail))
    db.commit()
    db.close()

def createStory(title):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS {} (author TEXT PRIMARY KEY, entry TEXT);".format(title))
    db.commit()
    db.close()

def addToStoryDB(title, author, entry):
    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    db.execute("INSERT INTO {} VALUES ('{}', '{}');".format(title, author, entry))
    db.commit()
    db.close()
