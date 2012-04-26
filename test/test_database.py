import sqlite3
import db_helper

test_db = None

def setup():
    """create in-memory database"""
    global test_db
    test_db = db_helper.connect()
    db_helper.repopulate(test_db)

def teardown():
    """destroy in-memory database"""
    global test_db
    db_helper.close(test_db);

def test_connection():
    global test_db
    with test_db:
        result = test_db.execute("SELECT SQLITE_VERSION()").fetchone()
    assert result[0] == "3.7.10"

def test_data_present():
    global test_db
    QUERY = "SELECT fax FROM distributors WHERE dist_name IS 'Oxford'"
    with test_db:
        result = test_db.execute(QUERY).fetchone()
    assert result[0] == "(555)555-0002"

def test_book_view():
    global test_db
