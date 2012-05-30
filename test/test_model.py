import sqlite3
from db_helper import prepare_test_database, connect
from ..model import OrderDB, make_book

test_db_path = "db/test.sqlite3"
BOOK_ID_QUERY = "SELECT book_id FROM books WHERE isbn13 IS ?;"
AUTHOR_QUERY = "SELECT author FROM authors   WHERE book_id IS ?;"
BOOK_QUERY   = """SELECT isbn13, title, binding, location, pub_name
    FROM book_view NATURAL JOIN (SELECT book_id, isbn13 FROM books)
    WHERE book_id IS ?;"""
ORDER_ID_QUERY = "SELECT order_id FROM orders WHERE po IS ?;"
ORDER_QUERY = """SELECT po, order_date, ship_method, dist_name, comment
    FROM order_headers NATURAL JOIN (SELECT order_id, po FROM orders)
    WHERE order_id IS ?;"""
ORDER_QUANTITIES_QUERY = "SELECT isbn13, quantity FROM order_quantities NATURAL JOIN books WHERE order_id IS ?;"

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

def get_order_id(po):
    with connect(test_db_path) as con:
        row = con.execute(ORDER_ID_QUERY, [po]).fetchone()
    if row is not None:
        return row['order_id']

def get_order_details(po = None, order_id = None):
    if order_id is None and po is not None:
        order_id = get_order_id(po)
    with connect(test_db_path) as con:
        header_row = con.execute(ORDER_QUERY, [order_id]).fetchone()
        entry_rows = con.execute(ORDER_QUANTITIES_QUERY, [order_id]).fetchall()
    if header_row is not None:
        order = {key: header_row[key] for key in header_row.keys()}
        order['entries'] = [(row['isbn13'], row['quantity'])
                            for row in entry_rows]
        return order

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

    assert get_book_id(TEST_BOOK['isbn13']) is None, "Book should not already exist in db"
    OrderDB(test_db_path).add_book(**TEST_BOOK)
    assert get_book_details(TEST_BOOK['isbn13']) == TEST_BOOK, "Book should be in the db"

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
        assert get_book_details(book_id = book_id) == expected_values, "Book key {} should be updated".format(key)

def test_book_delete():
    isbn13 = '9780061474096'
    assert get_book_id(isbn13) is not None, "Book should be in db"
    OrderDB(test_db_path).delete_book(isbn13)
    assert get_book_id(isbn13) is None, "Book should be romoved from db"

def test_order_get():
    PO = "1A2001"
    return_value = OrderDB(test_db_path).get_order(PO)
    db_value = get_order_details(PO)
    assert db_value == return_value, "Returned: {}\nDatabase: {}".format(return_value, db_value)

def test_order_create():
    PARAMS = {
        'po': '1B2001',
        'order_date': '2012-2-1',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford'}
    EXPECTED = {
        'po': '1B2001',
        'order_date': '2012-2-1',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': '',
        'entries': []}
    assert get_order_id(PARAMS['po']) is None, "Order should not exist yet"
    OrderDB(test_db_path).create_order(**PARAMS)
    db_value = get_order_details(PARAMS['po']) 
    assert db_value == EXPECTED, "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)

def test_order_create_with_comment():
    PARAMS = {
        'po': '1B2002',
        'order_date': '2012-2-1',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': None,
        'entries': []}
    EXPECTED = {
        'po': '1B2002',
        'order_date': '2012-2-1',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': None,
        'entries': []}
    assert get_order_id(PARAMS['po']) is None, "Order should not exist yet"
    OrderDB(test_db_path).create_order(**PARAMS)
    db_value = get_order_details(PARAMS['po']) 
    assert db_value == EXPECTED, "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)

def test_order_delete():
    raise NotImplementedError

def test_order_add_entry():
    raise NotImplementedError

def test_order_delete_entry():
    raise NotImplementedError

def test_order_update():
    raise NotImplementedError

def test_order_update_entry():
    raise NotImplementedError
