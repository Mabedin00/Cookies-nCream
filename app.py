# COMPLETELY UNTESTED

from flask import Flask, render_template, request, redirect, url_for, flash

@app.route('/')
def landing():
    # form for login
    # button redirecting to register route
    if loggedIn():
        # loggedIn function checks if user is logged in (refer to previous hw on login)
        return redirect(url_for('/main'))
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/processRegistration')
def processRegistration():
    if successfulRegistration():
        # checks if the username is unique, and if there are entries for password and email
        addToDB(users, request.args.get('username')
                     , request.args.get('password')
                     , request.args.get('email'))
    else:
        flash("Registration Failed")
        return redirect(url_for('landing()'))
    return redirect(url_for('main()'))

@app.route('/login')
def login():
    if successfulLogin():
        # checks if username and pass are in users db
        return redirect(url_for('main()'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing()'))

@app.route('/main')
def main():
    # button to logout
    return render_template('main.html') # other elements here in future,
                                        # like dropdown forms
