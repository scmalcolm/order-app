import sqlite3
from db_helper import prepare_test_database, connect
from ..model import *

test_db_path = "db/test.sqlite3"
BOOK_QUERY   = "SELECT * FROM book_view WHERE book_id IS ?;"
AUTHOR_QUERY = "SELECT * FROM authors   WHERE book_id IS ?;"
BOOK_ID_QUERY = "SELECT book_id FROM books WHERE isbn13 IS ?;"
BOOK_PROPERTIES = set(['isbn13', 'title', 'binding', 'location', 'pub_name'])

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
        book    = con.execute(BOOK_QUERY,   [book_id]).fetchone()
        authors = con.execute(AUTHOR_QUERY, [book_id]).fetchall()
    result = {}
    if book is not None:
        result = {key: book[key] for key in book.keys() if not key == 'book_id'}
    result['authors'] = [row['author'] for row in authors]
    return result

def check_book_details(book_id, expected):
    actual = get_book_details(book_id)
    if expected is None:
        return actual == {'authors': []}
    print "Expected: {}".format(expected)
    print "Actual:   {}".format(actual)
    return  expected == actual

def test_model_init():
    db = OrderDB()
    db = OrderDB(test_db_path)

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
    'title'     : 'Cuba',
    'binding'   : 'Paper',
    'location'  : 'History',
    'pub_name'  : 'Oxford',
    'authors'   : ['Neal Stephenson']}

    book_id = get_book_id('9780061474095')
    db = OrderDB(test_db_path)
    db.update_book(old_isbn13 = '9780061474095', **TEST_PARAMS)
    assert check_book_details(book_id, TEST_PARAMS)

def test_book_update_individual_fields():
    TEST_PARAMS = {
    'isbn13'    : '9780061474097',
    'title'     : 'Out of Print',
    'binding'   : 'Spiral',
    'location'  : 'Philosophy',
    'pub_name'  : 'Penguin',
    'authors'   : ['Neal Stephenson']}

    book_id = get_book_id('9780061474096')
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
        update('9780061474096', TEST_PARAMS[key])
        expected_values[key] = TEST_PARAMS[key]
        assert check_book_details(book_id, expected_values)

def test_book_delete():
    TEST_PARAMS = {'isbn13': '9780061474097'}

    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert book_id is not None
    db = OrderDB(test_db_path)
    db.delete_book(TEST_PARAMS['isbn13'])
    assert check_book_details(book_id, None)
