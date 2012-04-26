import sqlite3
from db_helper import prepare_test_database

test_db = None

def setup():
    """create in-memory database"""
    global test_db
    test_db = prepare_test_database()

def teardown():
    """destroy in-memory database"""
    global test_db
    test_db.close()

def test_connection():
    global test_db
    with test_db:
        result = test_db.execute("SELECT SQLITE_VERSION()").fetchone()
    assert result[0] == "3.7.10"

def test_data_present():
    global test_db
    QUERY = "SELECT fax FROM distributors WHERE dist_name IS 'Oxford';"
    with test_db:
        result = test_db.execute(QUERY).fetchone()
    assert result[0] == "(555)555-0002"

def test_book_view():
    global test_db
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    EXPECTED = {
        'isbn13': '9780199535569',
        'title': 'Pride and Prejudice',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford'}
    with test_db:
        result = test_db.execute(QUERY, EXPECTED).fetchone()
    for (key, value) in EXPECTED.iteritems():
        assert value == result[key]

def test_book_view_insert():
    global test_db
    INSERT = """INSERT INTO book_view
    (isbn13, title, binding, location, pub_name)
    VALUES
    (:isbn13, :title, :binding, :location, :pub_name);"""
    EXPECTED = {
        'isbn13': '9780199535545',
        'title': 'Northanger Abbey the book',
        'binding': 'Cloth',
        'location': 'History',
        'pub_name': 'Penguin'}
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    with test_db:
        test_db.execute(INSERT, EXPECTED)
        result = test_db.execute(QUERY, EXPECTED).fetchone()
    for (key, value) in EXPECTED.iteritems():
        assert value == result[key]

def test_book_view_update():
    global test_db
    UPDATE = """UPDATE book_view SET
    title = :title, binding = :binding, location = :location, pub_name = :pub_name
    WHERE isbn13 = :isbn13;"""
    EXPECTED = {
        'isbn13': '9780199535545',
        'title': 'Northanger Abbey',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford'}
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    with test_db:
        test_db.execute(UPDATE, EXPECTED)
        result = test_db.execute(QUERY, EXPECTED).fetchone()
    for (key, value) in EXPECTED.iteritems():
        assert value == result[key]