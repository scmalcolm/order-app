import sqlite3
from ..db_helper import prepare_test_database, execute_sql, row_to_dict

test_db = None

def setup():
    """create in-memory database"""
    global test_db
    test_db = prepare_test_database()

def teardown():
    """destroy in-memory database"""
    test_db.close()

def valid(action, params, query, expected):
    if action is not None:
        execute_sql(test_db, action, params)
    query_result = execute_sql(test_db, query, params)
    print "\nExpected: {}\nResult: {}".format(expected, query_result)
    return query_result == expected

def test_connection():
    with test_db:
        result = test_db.execute("SELECT SQLITE_VERSION();").fetchone()
    assert result[0] == "3.7.12"

def test_data_present():
    QUERY = "SELECT fax FROM distributors WHERE dist_name IS 'Oxford';"
    with test_db:
        result = test_db.execute(QUERY).fetchone()
    assert result[0] == "(555)555-0002"

def test_book_view():
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    EXPECTED = {
        'isbn13': '9780199535569',
        'title': 'Pride and Prejudice',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford'}
    assert valid(None, EXPECTED, QUERY, [EXPECTED]), "Should return book info"

def test_book_view_insert():
    ACTION = """INSERT INTO book_view VALUES
    (:isbn13, :title, :binding, :location, :pub_name);"""
    EXPECTED = {
        'isbn13': '9780199535544',
        'title': 'Northanger Abbey the book',
        'binding': 'Cloth',
        'location': 'History',
        'pub_name': 'Penguin'}
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    assert valid(ACTION, EXPECTED, QUERY, [EXPECTED]), "Book should be inserted in db"

def test_book_view_update():
    ACTION = """UPDATE book_view SET
    isbn13 = :isbn13, title = :title, binding = :binding, location = :location, pub_name = :pub_name
    WHERE isbn13 = :old_isbn13;"""
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    PARAMS = {
        'isbn13': '9780199535545',
        'title': 'Northanger Abbey',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford',
        'old_isbn13': '9780199535544'}
    EXPECTED = {
        'isbn13': '9780199535545',
        'title': 'Northanger Abbey',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford'}
    assert valid(ACTION, PARAMS, QUERY, [EXPECTED]), "values should be updated"

def test_book_view_delete():
    ACTION = "DELETE FROM book_view WHERE isbn13 IS :isbn13;"
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    PARAMS = {'isbn13': '97801995355'}
    assert valid(ACTION, PARAMS, QUERY, []), "book should be deleted"

def test_order_headers():
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {'po': '1A2100'}
    EXPECTED = {
        'po': '1A2100',
        'order_date': '2012-01-01',
        'ship_method': 'Usual Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders'}
    assert valid(None, PARAMS, QUERY, [EXPECTED]), "View should have order info"

def test_order_headers_insert():
    ACTION = """INSERT INTO order_headers VALUES
    (:po, :order_date, :ship_method, :dist_name, :comment);"""
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {
        'po': '1A2101',
        'order_date': '2012-01-01',
        'ship_method': 'Air',
        'dist_name': 'Penguin',
        'comment': 'Extra Backorders'}
    EXPECTED = {
        'po': '1A2101',
        'order_date': '2012-01-01',
        'ship_method': 'Air',
        'dist_name': 'Penguin',
        'comment': 'Extra Backorders'}
    assert valid(ACTION, PARAMS, QUERY, [EXPECTED]), "Order should be inserted"

def test_order_headers_update():
    ACTION = """UPDATE order_headers SET
        po = :po,
        order_date = :order_date,
        ship_method = :ship_method,
        dist_name = :dist_name,
        comment = :comment
        WHERE po is :old_po;"""
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {
        'po': '1A2102',
        'order_date': '2010-01-01',
        'ship_method': 'UPS',
        'dist_name': 'Oxford',
        'comment': 'Nonsense',
        'old_po': '1A2101'}
    EXPECTED = {
        'po': '1A2102',
        'order_date': '2010-01-01',
        'ship_method': 'UPS',
        'dist_name': 'Oxford',
        'comment': 'Nonsense'}
    assert valid(ACTION, PARAMS, QUERY, [EXPECTED]), "Order info should have updated"

def test_order_headers_delete():
    ACTION = "DELETE FROM order_headers WHERE po IS :po;"
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {'po': '1A2102'}
    assert valid(ACTION, PARAMS, QUERY, []), "Order header should be deleted"

def test_order_entries():
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': "1A2100"}
    EXPECTED = {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5}
    assert valid(None, PARAMS, QUERY, [EXPECTED]), "View should have order quantity"

def test_order_entries_insert():
    ACTION = "INSERT INTO order_entries VALUES (:po, :isbn13, :quantity);"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 3}
    EXPECTED = [
        {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5},
        {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 3}]
    assert valid(ACTION, PARAMS, QUERY, EXPECTED), "Should have a second entry"

def test_order_entries_update():
    ACTION = "UPDATE order_entries SET quantity = :quantity WHERE isbn13 IS :isbn13 AND po IS :po;"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 19}
    EXPECTED = [
        {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5},
        {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 19}]
    assert valid(ACTION, PARAMS, QUERY, EXPECTED), "Second entry should be updated"

def test_order_entries_delete():
    ACTION = "DELETE FROM order_entries WHERE isbn13 IS :isbn13 and po IS :po;"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167'}
    EXPECTED = [{'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5}]
    assert valid(ACTION, PARAMS, QUERY, EXPECTED), "second entry should be deleted"
