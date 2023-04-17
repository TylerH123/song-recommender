import sqlite3
from flask import g, Flask

app = Flask(__name__)
def get_db():
    """Open a new database connection."""
    if 'sqlite_db' not in g:
        g.sqlite_db = sqlite3.connect("../var/db.sqlite3")
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        g.sqlite_db.execute('PRAGMA foreign_keys = ON')
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.
    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


def get_user(user, pwd):
    """Return user."""
    con = get_db()    
    cur = con.cursor()
    res = cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    return res.fetchone()


def find_user(user):
    """Find user."""
    con = get_db()
    cur = con.cursor()
    res = cur.execute("SELECT * FROM users WHERE username=?", (user,))
    return res.fetchone()


def insert_user(user, pwd):
    """Insert new user into db."""
    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT into users (username, password) VALUES(?, ?)", (user, pwd))
    con.commit()         


def get_songs_at_state(state):
    """Get songs for given state."""
    