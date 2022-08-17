# Authentication routes help keep data safe / deter hackers
# Using Blueprint to route site path
# To reference what a Blueprint Object is https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint

# Comes from UserLoginForm Class in forms.py which takes in (email and password)
from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

# imports for flask login 
from flask_login import login_user, logout_user, LoginManager, current_user, login_required

# looks into auth_templates folder
auth = Blueprint('auth', __name__, template_folder='auth_templates')

# SIGN UP ROUTE
# the methods GET and POST are to get and receive data from the browser
@auth.route('/signup', methods = ['GET', 'POST'])

# UserLoginForm is imported from forms.py
def signup():
    form = UserLoginForm()

# use try and except to handle errors
# if statement asks if the browser is trying to post data, continue if the form is submitted
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

# User class is from models.py and includes the data passed in on forms.py as part of its creation
            user = User(email, password = password)

# this will add the user to the database
            db.session.add(user)
            db.session.commit()


# The flash message with show in terminal
# Then the user will be redirected back to home page
            flash(f'You have successfully created a user account {email}', 'User-created')
            return redirect(url_for('site.home'))

# Allows us to take care of errors if our user inputs the wrong data
# Also takes care if our FlaskForms and wtforms throws errors.
# renders sign_up.html and pass in form (which is userloginform) as our form which gets injected into the html
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)


# SIGN IN ROUTE
# Similar to the get / post of sign up above.
@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

# logged_user asks our user class to save the current user's name as a variable, if nothing comes back, user doesn't exist
# if if statement is run and doesn't have data, it will go on to else statement and deny access to user.
# login_user is a function that comes from flask_login import 
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You logged in!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('You do not have access to this content.', 'auth-failed')
# url_for will figure out where the url of something is to locate the document (auth.signin)
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please Check your Form')
    return render_template('sign_in.html', form=form)

# LOG OUT ROUTE
# Logs users out with the function logout, and sends them back to the homepage
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))

    