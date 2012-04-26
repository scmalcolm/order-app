import sqlite3
from db_helper import prepare_test_database, connect
from ..model import *

test_db_path = "db/test.sqlite3"

def setup():
    global test_db_path
    prepare_test_database(test_db_path)

def get_book_id(isbn13):
    global test_db_path
    BOOK_ID_QUERY = "SELECT book_id FROM books WHERE isbn13 IS ?;"
    
    with connect(test_db_path) as con:
        row = con.execute(BOOK_ID_QUERY, [isbn13]).fetchone()
    return row['book_id']

def assert_book_details(book_id, params = {}):
    global test_db_path
    ABSENCE_KEY, SKIP_LIST_KEY = 'no such book', 'skip list'
    keys_to_skip = ['authors', ABSENCE_KEY, SKIP_LIST_KEY]
    keys_to_skip.extend(params.get('skip list', []))
    test_for_absence = params.get(ABSENCE_KEY, False)

    BOOK_QUERY   = "SELECT * FROM book_view WHERE book_id IS ?;"
    AUTHOR_QUERY = "SELECT * FROM authors   WHERE book_id IS ?;"
    
    with connect(test_db_path) as con:
        book    = con.execute(BOOK_QUERY,   [book_id]).fetchone()
        authors = con.execute(AUTHOR_QUERY, [book_id]).fetchall()

    if test_for_absence:
        assert book is None and len(authors) == 0
        return

    for key, expected in params.iteritems():
        if key not in keys_to_skip:
            assert book[key] == expected

    if 'authors' in params:
        assert authors.sort() == params['authors'].sort()
    
def test_model_init():
    db = OrderDB()
    db = OrderDB(test_db_path)

def test_book_insert():
    global test_db_path

    TEST_PARAMS = {
    'isbn13'  : '9780061474095',
    'title'   : 'Anathem',
    'binding' : 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow',
    'authors' : ['Neal Stephenson']}

    db = OrderDB(test_db_path)
    db.add_book(**TEST_PARAMS)

    book_id = get_book_id(TEST_PARAMS['isbn13'])
    assert_book_details(book_id, TEST_PARAMS)

def test_book_update():
    global test_db_path

    TEST_PARAMS = {
    'old_isbn13': '9780061474095',
    'isbn13'    : '9780061474096',
    'title'     : 'Anathem',
    'binding'   : 'Cloth',
    'location'  : 'Fiction',
    'pub_name'  : 'William Morrow',
    'authors'   : ['Neal Stephenson'],
    'skip list' : ['old_isbn13']}

    book_id = get_book_id(TEST_PARAMS['old_isbn13'])

    db = OrderDB(test_db_path)
    db.update_book(**TEST_PARAMS)

    assert_book_details(book_id, TEST_PARAMS)

def test_book_delete():
    global test_db_path

    TEST_PARAMS = {'isbn13': '9780061474096', 'no such book': True}

    book_id = get_book_id(TEST_PARAMS['isbn13'])

    db = OrderDB(test_db_path)
    db.delete_book(TEST_PARAMS['isbn13'])

    assert_book_details(book_id, TEST_PARAMS)