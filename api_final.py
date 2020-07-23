""" Following tutorial found at programminghistorian.org/en/lessons/creating-apis-with-python-and-flask#lesson-goals
"""

import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
    <p>A prototype API for distant reading of science fiction novels.</p>'''

def create_cursor(database):
    conn = sqlite3.connect(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    return cur

@app.route('/v1/resources/books/all', methods=['GET'])
def get_books():
    cur = create_cursor('books.db')
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found</p>", 404

@app.route('/v1/resources/books', methods=['GET'])
def api_filter():
    query_params = request.args
    id = query_params.get('id')
    published = query_params.get('published')
    author = query_params.get('author')
    
    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    cur = create_cursor('books.db')
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

if __name__ == '__main__':
    app.run()