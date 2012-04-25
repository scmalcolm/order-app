import sqlite3
import db_helper
from ..model import *

test_db = "db/test.sqlite3"

def setup():
    global test_db
    con = db_helper.connect(test_db)
    db_helper.repopulate(con)
    con.commit()
    con.close()

def test_model_init():
    db = OrderDB()

def test_book_insert():
    global test_db

    TEST_PARAMS = {
    'isbn13': "9780061474095",
    'title': 'Anathem',
    'binding': 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow',
    'authors': ['Neal Stephenson']}

    BOOK_QUERY = """SELECT * FROM
    books NATURAL JOIN
    publishers NATURAL JOIN
    bindings NATURAL JOIN
    locations
    WHERE isbn13 IS :isbn13;
    """

    AUTHOR_QUERY = """SELECT * FROM
    books NATURAL JOIN
    authors
    WHERE isbn13 IS :isbn13;
    """

    db = OrderDB(test_db)
    db.add_book(**TEST_PARAMS)

    con = db_helper.connect(test_db)
    try:
        cur = con.cursor()
        cur.execute(BOOK_QUERY, TEST_PARAMS)
        book_rows = cur.fetchall()
        cur.execute(AUTHOR_QUERY, TEST_PARAMS)
        author_rows = cur.fetchall()
    except sqlite3.Error, e:
        print "Insertion test failed to retrieve data!"
        print "Error: %s" % e.args[0]
    
    assert book_rows is not None
    assert len(book_rows) == 1
    
    book_columns_are_correct = True
    for row in book_rows:
        for column_name in TEST_PARAMS.keys():
            if column_name == 'authors':
                continue
            expected = TEST_PARAMS[column_name]
            result = row[column_name]
            print 'Column: {}, Expected: {}, Result: {}'.format(column_name, expected, result)
            if not expected == result:
                book_columns_are_correct = False
    assert book_columns_are_correct

    assert author_rows is not None
    assert len(author_rows) == 1

    retrieved_authors = [row['author'] for row in author_rows]
    for author in TEST_PARAMS['authors']:
        retrieved_authors.remove(author)
    assert len(retrieved_authors) == 0
