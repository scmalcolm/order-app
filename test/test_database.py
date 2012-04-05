import sqlite3
import sys
from nose.tools import with_setup

con = None

def setup():
    """create in-memory database"""
    global con

    schema = None
    with open("db/create_tables.sql") as f:
        schema = f.read()
    try:
        con = sqlite3.connect(':memory:')
        con.executescript(schema)
        con.commit()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]

def teardown():
    """destroy in-memory database"""
    global con

    if con:
        con.close();
        con = None

def populate_db():
    """insert test data"""
    global con

    data = None
    with open("db/test_data.sql") as f:
        data = f.read()
    try:
        con.executescript(data)
        con.commit()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]

def depopulate_db():
    """dump test data"""
    global con

    data = """DELETE FROM order_quantities;
            DELETE FROM orders;
            DELETE FROM ship_methods;
            DELETE FROM authors;
            DELETE FROM locations;
            DELETE FROM publishers;
            DELETE FROM bindings;
            DELETE FROM books;
            DELETE FROM distributors;"""

    try:
        con.executescript(data)
        con.commit()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]

def test_connection():
    global con
    try:
        cur = con.cursor()
        cur.execute("SELECT SQLITE_VERSION()")
        result = cur.fetchone()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]
    assert result[0] == "3.7.10"

