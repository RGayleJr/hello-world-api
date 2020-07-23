""" Following tutorial found at programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#lesson-goals
"""

import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id' : 0,
     'title' : 'A Fire Upon the Deep',
     'author' : 'Vernor Vinge',
     'first_sentence' : 'The coldsleep itself was dreamless.',
     'year_published' : '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'} 
]

@app.route('/', methods=['GET'])
def home():
    return """<h1>Distant Reading Archive</h1>
    <p>This site is a prototype API for distant reading of science fiction nocels.</p>"""

@app.route('v1/resources/books/all', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('v1/resources/books', methods=['GET'])
def get_book():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please speicify an id"
    
    results = []
    for book in books:
        if book['id'] == id:
            results.append(book)
    return jsonify(results)

app.run()