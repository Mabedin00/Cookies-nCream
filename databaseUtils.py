#Functions for database
import sqlite3

DB_FILE="storyGame.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
cursor = db.cursor()


def addToUserDB(userusername, password, email):
    db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT);")
