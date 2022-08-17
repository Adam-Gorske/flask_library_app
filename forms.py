# This file will run the logic for our forms
# FlaskForm gives us modules to enhance and secure our data collection from our forms
# https://flask-wtf.readthedocs.io/en/0.15.x/quickstart/ 
# StringField makes sure input is string
# PasswordField prevents users from showing password on screen
# SubmitField automatically ties submit time data with other fields

# DataRequired() and Email() run something like regex to make sure we're being given the right data type


from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

# Creates a class UserLoginForm that uses FlaskForm to create variables email, password, and submit_button
# This gets imported into routes.py in the auth_templates folder 
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()