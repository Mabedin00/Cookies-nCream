#Functions for database
import sqlite3

DB_FILE="storyGame.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
cursor = db.cursor()

def createUsersDB():
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT);")

def addToUserDB(userUsername, userPassword, userEmail):
    db.execute("INSERT INTO {} VALUES ('{}', '{}', '{}');".format("users", userUsername, userPassword, userEmail))

def createStory(title):
    db.execute("CREATE TABLE IF NOT EXISTS {} (author TEXT PRIMARY KEY, entry TEXT);".format(title))

def addToStoryDB(title, author, entry):
    db.execute("INSERT INTO {} VALUES ('{}', '{}');".format(title, author, entry))
