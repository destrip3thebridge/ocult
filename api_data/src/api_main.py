from flask import Flask, request
import pymysql
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

username = "admin"
password = "83J%y92vwWgAyvJ%DW%YvXB*"
host = "database-ocult.crt8burntnnh.us-east-1.rds.amazonaws.com"
port = 3306

@app.route('/api/v1/resources/users/all', methods=['GET'])
def get_all():
    connection = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor,
                        database = 'ocult'
    )

    cursor = connection.cursor()
    select_users = "SELECT * FROM user"
    cursor.execute(select_users)
    result = cursor.fetchone()
    connection.close()
    return {'users': result}

@app.route('/api/v1/resources/books/authors', methods=['GET'])
def get_count_authors():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT author,count(author) FROM books GROUP BY 1 ORDER BY 2 DESC"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return {'books': result}

@app.route('/api/v1/resources/book/<string:author>', methods=['GET'])
def get_by_author(author):
    author='%'+author+'%'
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books WHERE author LIKE ?"
    result = cursor.execute(select_books, (author,)).fetchall()
    connection.close()
    return {'books': result}

@app.route('/api/v1/resources/book/filter', methods=['GET'])
def filter_table():
    query_parameters = request.get_json()
    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
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
        return "page not found 404"
    query = query[:-4] + ';'
    result = cursor.execute(query, to_filter).fetchall()
    connection.close()
    return {'books': result}


app.run()