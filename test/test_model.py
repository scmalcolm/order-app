import sqlite3
from db_helper import prepare_test_database, connect
from ..model import OrderDB, make_book

test_db_path = "db/test.sqlite3"
BOOK_ID_QUERY = "SELECT book_id FROM books WHERE isbn13 IS ?;"
AUTHOR_QUERY = "SELECT author FROM authors   WHERE book_id IS ?;"
BOOK_QUERY   = """SELECT isbn13, title, binding, location, pub_name
    FROM book_view NATURAL JOIN (SELECT book_id, isbn13 FROM books)
    WHERE book_id IS ?;"""

def setup():
    prepare_test_database(test_db_path)

def get_book_id(isbn13):
    with connect(test_db_path) as con:
        row = con.execute(BOOK_ID_QUERY, [isbn13]).fetchone()
    if row is None: return None
    return row['book_id']

def get_book_details(book_id):
    assert book_id is not None
    with connect(test_db_path) as con:
        book_row    = con.execute(BOOK_QUERY,   [book_id]).fetchone()
        author_rows = con.execute(AUTHOR_QUERY, [book_id]).fetchall()
    return make_book(book_row, author_rows)

def check_book_details(book_id, expected):
    actual = get_book_details(book_id)
    print "Expected: {}".format(expected)
    print "Actual:   {}".format(actual)
    return  expected == actual

def test_model_init():
    db = OrderDB()
    db = OrderDB(test_db_path)

def test_book_get():
    TEST_PARAMS = {'isbn13': '9780199535569'}
    book_id = get_book_id(TEST_PARAMS['isbn13'])
    db = OrderDB(test_db_path)
    reported_values = db.get_book(**TEST_PARAMS)
    assert check_book_details(book_id, reported_values) 

def test_book_insert():
    TEST_PARAMS = {
    'isbn13'  : '9780061474095',
    'title'   : 'Anathem',
    'binding' : 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow',
    'authors' : ['Neal Stephenson']}

    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert book_id is None
    db = OrderDB(test_db_path)
    db.add_book(**TEST_PARAMS)
    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert check_book_details(book_id, TEST_PARAMS)

def test_book_update():
    TEST_PARAMS = {
                    'isbn13'    : '9780061474096',
                    'title'     : 'Out of Print',
                    'binding'   : 'Spiral',
                    'location'  : 'Philosophy',
                    'pub_name'  : 'Penguin',
                    'authors'   : ['Neal Stephenson']}
    OLD_ISBN = '9780061474095'
    book_id = get_book_id(OLD_ISBN)
    expected_values = get_book_details(book_id)
    db = OrderDB(test_db_path)
    updates = [
    ('title', db.update_title),
    ('binding', db.update_binding),
    ('pub_name', db.update_publisher),
    ('location', db.update_location),
    ('isbn13', db.update_isbn)]
    for key, update in updates:
        print "Update {}".format(key)
        update(OLD_ISBN, TEST_PARAMS[key])
        expected_values[key] = TEST_PARAMS[key]
        assert check_book_details(book_id, expected_values)

def test_book_delete():
    TEST_PARAMS = {'isbn13': '9780061474096'}

    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert book_id is not None
    db = OrderDB(test_db_path)
    db.delete_book(TEST_PARAMS['isbn13'])
    assert check_book_details(book_id, None)
