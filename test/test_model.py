import sqlite3
from db_helper import prepare_test_database, connect
from ..model.object import OrderDB

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
        entry_tuples = [(row['isbn13'], row['quantity']) for row in entry_rows]
        order['entries'] = set(entry_tuples)
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
    PARAMS = {
        'old_isbn13': '9780192807069',
        'isbn13'    : '9780061474096',
        'title'     : 'Out of Print',
        'binding'   : 'Spiral',
        'location'  : 'Philosophy',
        'pub_name'  : 'Penguin'}
    EXPECTED_BEFORE = {
        'isbn13'    : "9780192807069",
        'title'     : "Six Tragedies",
        'binding'   : "Paper",
        'location'  : "Classics",
        'pub_name'  : "Oxford",
        'authors'   : ['Seneca']}
    EXPECTED_AFTER = {
        'isbn13'    : '9780061474096',
        'title'     : 'Out of Print',
        'binding'   : 'Spiral',
        'location'  : 'Philosophy',
        'pub_name'  : 'Penguin',
        'authors'   : ['Seneca']}
    db_value = get_book_details(PARAMS['old_isbn13'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED_BEFORE, db_value)
    assert db_value == EXPECTED_BEFORE, "Book should exist"
    OrderDB(test_db_path).update_book(**PARAMS)
    db_value = get_book_details(PARAMS['isbn13']) 
    print "Expected: {}\nDatabase: {}".format(EXPECTED_AFTER, db_value)
    assert db_value == EXPECTED_AFTER, "Book should be altered"
    
def test_book_delete():
    isbn13 = '9780441172719'
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
        'entries': set()}
    assert get_order_id(PARAMS['po']) is None, "Order should not exist yet"
    OrderDB(test_db_path).create_order(**PARAMS)
    db_value = get_order_details(PARAMS['po']) 
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED

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
        'entries': set()}
    assert get_order_id(PARAMS['po']) is None, "Order should not exist yet"
    OrderDB(test_db_path).create_order(**PARAMS)
    db_value = get_order_details(PARAMS['po'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED

def test_order_add_entry():
    PARAMS = {
        'po': '1C2100',
        'isbn13': "9780199535569",
        'quantity': 8}
    ENTRIES_BEFORE = set([('9780199537167', 10)])
    ENTRIES_AFTER  = set([('9780199537167', 10),
                          (PARAMS['isbn13'], PARAMS['quantity'])])
    EXPECTED = {
        'po': '1C2100',
        'order_date': '2012-03-01',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders',
        'entries': ENTRIES_BEFORE}
    db_value = get_order_details(PARAMS['po'])
    assert db_value == EXPECTED, "New entry should not exist yet"
    EXPECTED['entries'] = ENTRIES_AFTER
    OrderDB(test_db_path).add_order_entry(**PARAMS)
    db_value = get_order_details(PARAMS['po'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED

def test_order_update():
    PARAMS = {
        'old_po': '1C2101',
        'po': '1C0102',
        'order_date': '2010-03-01',
        'ship_method': 'UPS',
        'dist_name': 'Penguin',
        'comment': 'Pack poorly'}
    EXPECTED = {
        'po': '1C0102',
        'order_date': '2010-03-01',
        'ship_method': 'UPS',
        'dist_name': 'Penguin',
        'comment': 'Pack poorly',
        'entries': set([('9780199537167', 1)])}
    assert get_order_id(PARAMS['old_po']) is not None, "Order should exist already"
    OrderDB(test_db_path).update_order(**PARAMS)
    db_value = get_order_details(PARAMS['po'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED

def test_order_update_entry():
    PARAMS = {
        'po': '1C2200',
        'old_isbn13': "9780199535569",
        'isbn13': "9780140430325",
        'quantity': 7}
    ENTRIES_BEFORE = set([("9780199535569", 3),
                          ("9780199537167", 25)])
    ENTRIES_AFTER  = set([("9780140430325", 7),
                          ("9780199537167", 25)])
    EXPECTED = {
        'po': '1C2200',
        'order_date': '2012-03-01',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders',
        'entries': ENTRIES_BEFORE}
    db_value = get_order_details(PARAMS['po'])
    assert db_value == EXPECTED, "Entry should exist already"
    OrderDB(test_db_path).update_order_entry(**PARAMS)
    db_value = get_order_details(PARAMS['po'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED

def test_order_delete_entry():
    PARAMS = {
        'po': '1C2201',
        'isbn13': '9780199537167'}
    ENTRIES_BEFORE = set([("9780199535569", 3),
                          ("9780199537167", 25)])
    ENTRIES_AFTER  = set([("9780199535569", 3)])
    EXPECTED = {
        'po': '1C2201',
        'order_date': '2012-03-01',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders',
        'entries': ENTRIES_BEFORE}
    db_value = get_order_details(PARAMS['po'])
    assert db_value == EXPECTED, "Entry should exist already"
    OrderDB(test_db_path).delete_order_entry(**PARAMS)
    EXPECTED['entries'] = ENTRIES_AFTER
    db_value = get_order_details(PARAMS['po'])
    print "Expected: {}\nDatabase: {}".format(EXPECTED, db_value)
    assert db_value == EXPECTED, "Entry should be deleted"

def test_order_delete():
    PARAMS = {'po': '1A2100'}
    EXPECTED = {
        'po': '1A2100',
        'order_date': '2012-01-01',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders',
        'entries': set([("9780199535569", 5)])}
    db_value = get_order_details(PARAMS['po'])
    assert db_value == EXPECTED, "Order should exist already"
    OrderDB(test_db_path).delete_order(**PARAMS)
    assert get_order_id(PARAMS['po']) == None, "Entry should be deleted"
