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

    with db_helper.connect(test_db) as con:
        books = [row for row in con.execute(BOOK_QUERY, TEST_PARAMS)]
        authors = [row for row in con.execute(AUTHOR_QUERY, TEST_PARAMS)]
    
    assert books is not None and len(books) == 1

    for param, expected in TEST_PARAMS.iteritems():
        if param == 'authors':
            continue
        result = books[0][param]
        print 'Param: {}, Expected: {}, Result: {}'.format(param, expected, result)
        assert expected == result

    assert authors is not None and len(authors) == 1

    author_names = [row['author'] for row in authors]
    for author in TEST_PARAMS['authors']:
        author_names.remove(author)
    assert len(author_names) == 0
