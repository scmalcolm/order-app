import sqlite3
from db_helper import prepare_test_database, execute_sql, row_to_dict

test_db = None

def setup():
    """create in-memory database"""
    global test_db
    test_db = prepare_test_database()

def teardown():
    """destroy in-memory database"""
    test_db.close()

def test_connection():
    with test_db:
        result = test_db.execute("SELECT SQLITE_VERSION()").fetchone()
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
    assert execute_sql(test_db, QUERY, EXPECTED) == [EXPECTED]

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
    execute_sql(test_db, ACTION, EXPECTED)
    assert execute_sql(test_db, QUERY, EXPECTED) == [EXPECTED]

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
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == [EXPECTED]

def test_book_view_delete():
    ACTION = "DELETE FROM book_view WHERE isbn13 IS :isbn13;"
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    PARAMS = {'isbn13': '97801995355'}
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == []

def test_order_headers():
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {'po': '1A2100'}
    EXPECTED = {
        'po': '1A2100',
        'order_date': '2012-01-01',
        'ship_method': 'Ususal Means',
        'dist_name': 'Oxford',
        'comment': 'No Backorders'}
    assert execute_sql(test_db, QUERY, EXPECTED) == [EXPECTED]

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
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == [EXPECTED]

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
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == [EXPECTED]

def test_order_headers_delete():
    ACTION = "DELETE FROM order_headers WHERE po IS :po;"
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    PARAMS = {'po': '1A2102'}
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == []

def test_order_entries():
    QUERY = "SELECT * FROM order_entries;"
    EXPECTED = {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5}
    assert execute_sql(test_db, QUERY, {}) == [EXPECTED]

def test_order_entries_insert():
    ACTION = "INSERT INTO order_entries VALUES (:po, :isbn13, :quantity);"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 3}
    EXPECTED = [
        {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5},
        {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 3}]
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == EXPECTED

def test_order_entries_update():
    ACTION = "UPDATE order_entries SET quantity = :quantity WHERE isbn13 IS :isbn13 AND po IS :po;"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 19}
    EXPECTED = [
        {'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5},
        {'po': '1A2100', 'isbn13': '9780199537167', 'quantity': 19}]
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == EXPECTED

def test_order_entries_delecte():
    ACTION = "DELETE FROM order_entries WHERE isbn13 IS :isbn13 and po IS :po;"
    QUERY = "SELECT * FROM order_entries WHERE po IS :po;"
    PARAMS = {'po': '1A2100', 'isbn13': '9780199537167'}
    EXPECTED = [{'po': '1A2100', 'isbn13': '9780199535569', 'quantity': 5}]
    execute_sql(test_db, ACTION, PARAMS)
    assert execute_sql(test_db, QUERY, PARAMS) == EXPECTED
