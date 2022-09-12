# Brains of app. Flask runs from here
# Reference for Application Object (app = Flask(__name__)) https://flask.palletsprojects.com/en/2.2.x/api/#application-object
# imports Flask class
from flask import Flask

# imports Config class from config file
from config import Config

# imports site from the file routes.py in folder site
# site has the routes for home and profile
from .site.routes import site

# imports auth from the file routes.py in authentication folder
# routes.py has the routes for sign up / sign in / log out
from .authentication.routes import auth

# imports api from the file routes.py in api folder
# routes.py has the routes for api
from .api.routes import api

# These all assist in data migration between our app and browser
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma

# CORS is to avoid Cross-Site Request Forgery (Common way for hackers to access data)
from flask_cors import CORS
# JSONEncoder helps encode the JSON data
from helpers import JSONEncoder


# creates an instance of the Flask class
# __name__ argument is a shortcut for flask to look for resources such as templates and static files
app = Flask(__name__)

# register site blueprint (from the site import above) to app
# will allow us to run site when our app runs
app.register_blueprint(site)

# register auth blueprint (from the .authentication.routes import above) to app
# will allow us to run auth when our app runs
app.register_blueprint(auth)

# register api blueprint (from .api.routes import above) to app
# will run api when our app runs
app.register_blueprint(api)

# runs json encoder to protect data
app.json_encoder = JSONEncoder

# allows us to run Config from config file
# reference for configuring from Python files https://flask.palletsprojects.com/en/2.2.x/config/#configuring-from-python-files
app.config.from_object(Config)

# These initiate the database and run the login manager
# Also, get app ready to upload and modify the database tables using migrate
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)
cors = CORS(app)