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
    if row is not None:
        return row['book_id']

def get_book_details(isbn13 = None, book_id = None):
    if book_id is None and isbn13 is not None:
        book_id = get_book_id(isbn13)
    with connect(test_db_path) as con:
        book_row    = con.execute(BOOK_QUERY,   [book_id]).fetchone()
        author_rows = con.execute(AUTHOR_QUERY, [book_id]).fetchall()
    if book_row is not None:
        book = {key: book_row[key] for key in book_row.keys()}
        book['authors'] = [row['author'] for row in author_rows]
        return book

def check_book_details(book_id, expected):
    actual = get_book_details(book_id)
    print "Expected: {}".format(expected)
    print "Actual:   {}".format(actual)
    return  expected == actual

def test_book_get():
    ISBN = '9780199535569'
    result = OrderDB(test_db_path).get_book(ISBN)
    assert get_book_details(ISBN) == result, "Returned values should match db contents"

def test_book_insert():
    TEST_BOOK = {
        'isbn13'  : '9780061474095',
        'title'   : 'Anathem',
        'binding' : 'Cloth',
        'location': 'Fiction',
        'pub_name': 'William Morrow',
        'authors' : ['Neal Stephenson']}

    assert(get_book_id(TEST_BOOK['isbn13']) is None,
           "Book should not already exist in db")
    OrderDB(test_db_path).add_book(**TEST_BOOK)
    assert(get_book_details(TEST_BOOK['isbn13']) == TEST_BOOK,
           "Book should be in the db")

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
    expected_values = get_book_details(OLD_ISBN)
    db = OrderDB(test_db_path)
    updates = [
        ('title', db.update_title),
        ('binding', db.update_binding),
        ('pub_name', db.update_publisher),
        ('location', db.update_location),
        ('isbn13', db.update_isbn)]
    for key, update in updates:
        update(OLD_ISBN, TEST_PARAMS[key])
        expected_values[key] = TEST_PARAMS[key]
        assert(get_book_details(book_id = book_id) == expected_values,
               "Book key {} should be updated".format(key))

def test_book_delete():
    isbn13 = '9780061474096'
    assert get_book_id(isbn13) is not None, "Book should be in db"
    OrderDB(test_db_path).delete_book(isbn13)
    assert get_book_id(isbn13) is None, "Book should be romoved from db"
