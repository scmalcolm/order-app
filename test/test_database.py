import sqlite3
import db_helper

test_db = None

def setup():
    """create in-memory database"""
    global test_db
    test_db = db_helper.connect()


def teardown():
    """destroy in-memory database"""
    global test_db
    db_helper.close(test_db);

def test_connection():
    global test_db
    try:
        cur = test_db.cursor()
        cur.execute("SELECT SQLITE_VERSION()")
        result = cur.fetchone()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]
    assert result[0] == "3.7.10"

def test_data_present():
    global test_db
    db_helper.repopulate(test_db)
    try:
        cur = test_db.cursor()
        cur.execute("SELECT fax FROM distributors WHERE dist_name IS 'Oxford'")
        result = cur.fetchone()
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]
    assert result[0] == "(555)555-0002"