# Location and rules of the server
# Allows two machines to talk to each other

# jsonify will reformat our data into json so we can use it with Python and JS
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

# url_prefix means we need api in front of our end slug.
api = Blueprint('api',__name__, url_prefix='/api')

# allows us to pull data into insomnia
@api.route('/getdata')
def getdata():
    return {'cat': 'dog'}

# This will post book data to the database (on insomnia) -- mimics another back end app requesting data with our flask app
# token is required to send the data
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    copyright_date = request.json['copyright_date']
    user_token = current_user_token.token

# Tells us in the terminal if everything up to this point has worked.
    print(f'BIG TESTER: {current_user_token.token}')

# Instantiates the Book class with the data we just pulled from the json
    book = Book(isbn, author_name, book_title, copyright_date, user_token = user_token )

# puts all the info into the database
    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)


# Gets all the book data from our database and displays it in Insomnia in json format
@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# If we want a specific book we can call it with an id number
# We're querying by id number, then returning the data that query grabs
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# Get all the data from our query by the passed in ID
# save them all to a book, and then individually rewrite them
# We have to manually update the JSON piece
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.isbn = request.json['isbn']
    book.author_name = request.json['author_name']
    book.book_title = request.json['book_title']
    book.copyright_date = request.json['copyright_date']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Delete books by id
# If we didn't do it by id we'd delete the whole database
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)