# Used for creating classes that we'll use repeatedly to populate our databases

# writes sql queries into python for us
from flask_sqlalchemy import SQLAlchemy
# handles the sql database migrations
from flask_migrate import Migrate
# universally unique identifiers helps create a unique id for users (similar to a primary key)
import uuid 
from datetime import datetime
# wekzeug is a security package and password_hash hides what a user's password is from us
from werkzeug.security import generate_password_hash, check_password_hash
# User mixin makes sure LoginManager works properly https://flask-login.readthedocs.io/en/latest/#flask_login.UserMixin
from flask_login import UserMixin
# helps users log in and stay logged in https://flask-login.readthedocs.io/en/latest/
from flask_login import LoginManager
# validates data and helps us upload data to the database https://marshmallow.readthedocs.io/en/stable/
from flask_marshmallow import Marshmallow 
# generates secure random numbers (for security token)
import secrets

# set variables for class instantiation so they're easier to use in User class below
# LoginManager comes from flask_login
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

# It requests the user id from our User class (helpful for seeing if users are logged in or not)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    '''
        db (SQLAlchemy().column) will create new columns for the variable
        then each time our User class gets instantiated, 
        it adds the given data to the column mentioned.
    '''
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

# This init will pass all of the parameters into the class
# most of them default to empty ''
    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

# this calls on the secrets import to generate a token
# We pass in the 24 character length as an integer during __init__ above
# token_hex returns a random text string in hexadecimal
    def set_token(self, length):
        return secrets.token_hex(length)

# Sets a unique id number we'll use as a primary key (follow it up to the class attribute id)
    def set_id(self):
        return str(uuid.uuid4())

# Makes it so database owner can't see the user's password
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

# Prints out the message in the terminal
    def __repr__(self):
        return f'User {self.email} has been added to the database'



class Book(db.Model):
    '''
        db (SQLAlchemy().column) will create new columns for the variable
        then each time our Book class gets instantiated, 
        it adds the given data to the column mentioned.
        
        This class is what we will be saving into our database, and allow
        users to look at it later.
    '''
    id = db.Column(db.String, primary_key = True)
    isbn = db.Column(db.String(20))
    author_name = db.Column(db.String(50))
    book_title = db.Column(db.String(100))
    copyright_date = db.Column(db.String(10))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, isbn, author_name, book_title, copyright_date, user_token, id = ''):
        self.id = self.set_id()
        self.isbn = isbn
        self.author_name = author_name
        self.book_title = book_title
        self.copyright_date = copyright_date
        self.user_token = user_token


    def __repr__(self):
        return f'The following book has been added to the inventory: {self.book_title}'

# secrets.token_urlsafe() returns a url-safe text string
    def set_id(self):
        return (secrets.token_urlsafe())

# Calls on marshmallow to help upload data to database and validate it
# fields must match parameters of Book Class
# meta class is a class of a class that defines how a class behaves
class BookSchema(ma.Schema):
    class Meta:
        fields = ['id', 'isbn','author_name','book_title', 'copyright_date']

book_schema = BookSchema()
books_schema = BookSchema(many=True)