import flask
from flask import request, jsonify
import sqlite3

from flask import json
from flask.helpers import make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATABASE = "links.sqlite"


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except sqlite3.error as err:
        print(err)
    return conn


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    cur = db_connection().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET'])
def index():
    return '<h1>Server working</h1>'


@app.route('/api/visited_links', methods=['POST'])
def visited_links():
    conn = db_connection()
    cursor = conn.cursor()
    try:
        res = request.data
        return {"status": "ok"}
    except sqlite3.Error as err:
        return {"status": "err", "error": err}


@app.route('/api/visited_domains', methods=['GET'])
def visited_domains():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor = conn.execute("SELECT * FROM link")
            rows = cursor.fetchall()
            domains = []
            for row in rows:
                domains.append(row['title'])
            if(domains is not None):
                return {"domains": domains, "status": "ok"}
        except sqlite3.Error as err:
            return {"status": "err", "error":err}


if __name__ == '__main__':
    app.run()
