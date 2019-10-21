# COMPLETELY UNTESTED

from flask import Flask, render_template, request, redirect, url_for, flash

# This code skeleton is just for the logging in part, not for the
# actual page part.
# Also, here both the login and register forms
# are just on the main route instead of being on their separate pages.
# This is for simplicity, I think doing that would require two more routes.
# We could change it later if we think it looks better.

@app.route('/')
def landing():
    # form for login
    # button redirecting to register route
    if loggedIn(): # function is a placeholder
        return redirect(url_for('/main'))
    return render_template('index.html')

@app.route('/register')
def register():
    if successfulRegistration(): # function is a placeholder, may have to use
                                 # try-catch in the future
        addToDB(users, request.args.get('username')
                     , request.args.get('password')
                     , request.args.get('email'))
    else:
        flash("Registration Failed")
        return redirect(url_for('landing()'))
    return redirect(url_for('main()'))

@app.route('/login')
def login():
    if successfulLogin(): # function is a placeholder
        return redirect(url_for('main()'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing()'))

@app.route('/main')
def main():
    # button to logout
    return render_template('main.html') # other elements here in future,
                                        # like dropdown forms
