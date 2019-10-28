#Functions for database
import sqlite3

DB_FILE="storyGame.db"

def createUsersDB():
    db = sqlite3.connect(DB_FILE)
    db.execute("""CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT);""")
    db.commit()
    db.close()

def addToUserDB(userUsername, userPassword, userEmail):
    db = sqlite3.connect(DB_FILE)
    db.execute("""INSERT INTO users VALUES ('{}', '{}', '{}');""".format(userUsername, userPassword, userEmail))
    db.commit()
    db.close()

def createStory(title):
    db = sqlite3.connect(DB_FILE)
    try:
        db.execute("""CREATE TABLE {} (author TEXT PRIMARY KEY, entry TEXT);""".format(title))
        db.commit()
        db.close()
        return True
    except:
        db.commit()
        db.close()
        return False

def addToStoryDB(title, author, entry):
    print(entry)
    db = sqlite3.connect(DB_FILE)
    db.execute("""INSERT INTO {} VALUES ("{}", "{}");""".format(title, author, entry))
    db.commit()
    db.close()

def searchForAuthor(username):
    db = sqlite3.connect(DB_FILE)
    # get list of all stories
    masterList = list(db.execute("""SELECT name FROM sqlite_master WHERE type='table';"""))[1:]
    editedStories = []
    unEditedStories = []
    for story in masterList:
        story = story[0]
        # returns the user's username if the user has edited the story
        command = """SELECT author FROM {} WHERE author = '{}';""".format(story, username)
        # if the list has any elements (i.e. if the user edited the story)
        if len(list(db.execute(command))):
            editedStories.append(story)
        else:
            unEditedStories.append(story)
    return [editedStories, unEditedStories]
    db.commit()
    db.close()

def getEntries(storyName):
    db = sqlite3.connect(DB_FILE)
    allEntries = ""
    command = "SELECT entry FROM {};".format(storyName)
    for entries in list(db.execute(command)):
        allEntries += entries[0] + " "
    return allEntries
    db.commit()
    db.close()

def getLatestEntry(storyName):
    db = sqlite3.connect(DB_FILE)
    command = "SELECT entry FROM {} ORDER BY rowid DESC LIMIT 1;".format(storyName)
    print (list(db.execute(command)))
    return list(db.execute(command))[0][0]
    db.commit()
    db.close()

def successfulRegistration(username,password,email):
    passValid = len(password) > 0
    emailValid = len(email) > 0 and email.count('@') == 1
    db = sqlite3.connect(DB_FILE)
    # see if username is already taken
    command = """SELECT username FROM {} WHERE username = '{}';""".format('users', username)
    usernameValid = not bool(len(list(db.execute(command))))
    db.commit()
    db.close()
    return [usernameValid, passValid, emailValid]

def successfulLogin(username, password):
    db = sqlite3.connect(DB_FILE)
    try:
        userPass = list(db.execute("""SELECT password FROM users WHERE username = '{}';""".format(username)))[0][0]
        db.commit()
        db.close()
        return [True, password == userPass]
    except:
        db.commit()
        db.close()
        userPass = ""
        if len(password) == 0 or len(username) == 0: return [False, False]
        return [False, password == userPass]
