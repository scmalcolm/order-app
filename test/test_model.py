import sqlite3
from db_helper import prepare_test_database, connect
from ..model import *

test_db = "db/test.sqlite3"

def setup():
    global test_db
    prepare_test_database(test_db)

def get_book_id(isbn13):
    global test_db
    BOOK_ID_QUERY = "SELECT book_id FROM books WHERE isbn13 IS ?;"
    
    with connect(test_db) as con:
        row = con.execute(BOOK_ID_QUERY, [isbn13]).fetchone()
    return row['book_id']

def assert_book_details(book_id, params = {}, keys_to_skip = []):
    global test_db

    BOOK_QUERY   = "SELECT * FROM book_view WHERE book_id IS ?;"
    AUTHOR_QUERY = "SELECT * FROM authors   WHERE book_id IS ?;"
    
    with connect(test_db) as con:
        book    = con.execute(BOOK_QUERY,   [book_id]).fetchone()
        authors = con.execute(AUTHOR_QUERY, [book_id]).fetchall()

    for key, expected in params.iteritems():
        if key in keys_to_skip or key == 'authors':
            continue
        assert book[key] == expected

    if 'authors' in params:
        assert authors.sort() == params['authors'].sort()
    
def test_model_init():
    db = OrderDB()
    db = OrderDB(test_db)

def test_book_insert():
    global test_db

    TEST_PARAMS = {
    'isbn13': "9780061474095",
    'title': 'Anathem',
    'binding': 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow',
    'authors': ['Neal Stephenson']}

    db = OrderDB(test_db)
    db.add_book(**TEST_PARAMS)

    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert_book_details(book_id, TEST_PARAMS)

def test_book_update():
    global test_db

    TEST_PARAMS = {
    'old_isbn13': "9780061474095",
    'isbn13': "9780061474096",
    'title': 'Anathem',
    'binding': 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow',
    'authors': ['Neal Stephenson']}

    book_id = get_book_id(TEST_PARAMS['old_isbn13'])

    db = OrderDB(test_db)
    db.update_book(**TEST_PARAMS)

    assert_book_details(book_id, TEST_PARAMS, ['old_isbn13'])

def test_book_delete():
    global test_db

    TEST_PARAMS = {'isbn13': '9780061474096'}

    BOOK_QUERY   = "SELECT * FROM book_view WHERE book_id IS ?;"
    AUTHOR_QUERY = "SELECT * FROM authors   WHERE book_id IS ?;"

    book_id = get_book_id(TEST_PARAMS['isbn13'])

    db = OrderDB(test_db)
    db.delete_book(TEST_PARAMS['isbn13'])

    with connect(test_db) as con:
        books = [row for row in con.execute(BOOK_QUERY, [book_id])]
        authors = [row for row in con.execute(AUTHOR_QUERY, [book_id])]

    assert len(books) == len(authors) == 0