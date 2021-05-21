import sqlite3

conn = sqlite3.connect("links.sqlite")

cursor = conn.cursor()

query = """CREATE TABLE link (
    id integer PRIMARY KEY,
    title text NOT NULL
)"""

cursor.execute(query)