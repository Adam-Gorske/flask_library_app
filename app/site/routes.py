# Using Blueprint to route site path
# To reference what a Blueprint Object is https://flask.palletsprojects.com/en/2.2.x/api/#flask.Blueprint

from flask import Blueprint, render_template

# creating the site variable allows us to import it into other python files and use all of the data from here
# 'site' looks into our site folder
# folder where our templates are located is 'site_templates'
site = Blueprint('site', __name__, template_folder = 'site_templates')

# The route decorator tells Flask what URL should trigger our function
# On our site at /, the home function will run
# render_template will run the index.html page
@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')