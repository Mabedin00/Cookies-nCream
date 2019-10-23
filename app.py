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
    if loggedIn():
        return redirect(url_for('/main'))
    return render_template('index.html')

@app.route('/register')
    return render_template('register.html')
@app.route('process')
def process():
    if successfulLogin(): # function is a placeholder
        addToUserDB(request.args.get('username')
                  , request.args.get('password')
                  , request.args.get('email'))
        return redirect(url_for('main()'))
    else:
        flash("Registration Failed")
        return redirect(url_for('landing()'))

@app.route('/login')
def login():
    if successfulLogin(): # function is a placeholder
        return redirect(url_for('main()'))
    else:
        flash("Login Failed")
        return redirect(url_for('landing()'))

@app.route('/main')
def main():
    return render_template('main.html') # other elements here in future,
                                        # like dropdown forms
