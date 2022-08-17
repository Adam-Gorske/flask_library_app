# Creates an extra function to check tokens for rightful access to data
# Also creates an encoder for our JSON content to keep it secure
# We could pull in the Book class, but we don't need it here

from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from models import User


# checks to see if 'x-access-token' is in our headers for our API calls
# helps us modify the token so we can use it for access to our data
# if it's not able to, it'll send back an error
# args and kwargs allows us to add more data to the process as long as we run the function
def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

# Checks the instances of json are decimals, then changes them to strings we can use later
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)