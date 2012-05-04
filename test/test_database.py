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
    assert result[0] == "3.7.10"

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
    with test_db:
        result = test_db.execute(QUERY, EXPECTED).fetchone()
    for (key, value) in EXPECTED.iteritems():
        assert value == result[key]

def test_book_view_insert():
    INSERT = """INSERT INTO book_view
    (isbn13, title, binding, location, pub_name)
    VALUES
    (:isbn13, :title, :binding, :location, :pub_name);"""
    EXPECTED = {
        'isbn13': '9780199535544',
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
    UPDATE = """UPDATE book_view SET
    isbn13 = :isbn13, title = :title, binding = :binding, location = :location, pub_name = :pub_name
    WHERE isbn13 = :old_isbn13;"""
    EXPECTED = {
        'isbn13': '9780199535545',
        'title': 'Northanger Abbey',
        'binding': 'Paper',
        'location': 'Fiction',
        'pub_name': 'Oxford',
        'old_isbn13': '9780199535544'}
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    with test_db:
        test_db.execute(UPDATE, EXPECTED)
        result = test_db.execute(QUERY, EXPECTED).fetchone()
    for (key, value) in EXPECTED.iteritems():
        if key == 'old_isbn13':
            continue
        assert value == result[key]

def test_book_view_delete():
    DELETE = "DELETE FROM book_view WHERE isbn13 IS :isbn13;"
    QUERY = "SELECT * FROM book_view WHERE isbn13 IS :isbn13;"
    PARAMS = {'isbn13': '97801995355'}
    with test_db:
        test_db.execute(DELETE, PARAMS)
        result = test_db.execute(QUERY, PARAMS).fetchone()
    assert result is None

def test_order_headers():
    QUERY = "SELECT * FROM order_headers WHERE po IS :po;"
    EXPECTED = {
        'po': '1A2100',
        'order_date': '2012-01-01',
        'ship_method': 'Ususal Means',
        'dist_name': 'Oxford',
        'address': '123 fake street',
        'phone': '(555)555-0001',
        'fax': '(555)555-0002',
        'account_no': '42',
        'sales_rep': 'Steve',
        'comment': 'No Backorders'}
    result = execute_sql(test_db, QUERY, EXPECTED)
    assert result is not None and len(result) == 1
    result = row_to_dict(result[0])
    assert result == EXPECTED