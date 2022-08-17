# Reference for configuration handling https://flask.palletsprojects.com/en/2.2.x/config/
# AKA Flask environment variables
# PART 1 of what Needs to be setup before the app runs
# so the app, CLI, and browser are all able to communicate with each other

# import os (operating systems interface) allows us to interface with CLI 
import os

# imports functionality for loading .env file (which is the second part needed to run this file)
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Flask has a config object with loaded configuration values. We can change them to what we want.
class Config():
    '''
        Set config variables for the flask app
        using environment variables where available.
        Otherwise create the config variables if not done already.
    '''

    # When we create these, we need to create an .env file with some extras in it so these will run.
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Connects SQLAlchemy to our database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_NOTIFICAITONS = False