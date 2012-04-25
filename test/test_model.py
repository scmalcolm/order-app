import sqlite3
import db_helper
from ..model import *

def test_model_init():
    db = OrderDB()

def test_book_insert():
    test_db = "db/test.sqlite3"
    con = db_helper.connect(test_db)
    db_helper.repopulate(con)
    con.commit()
    con.close()

    BOOK_PARAMS = {
    'isbn13': "9780061474095",
    'title': 'Anathem',
    'binding': 'Cloth',
    'location': 'Fiction',
    'pub_name': 'William Morrow'}

    db = OrderDB(test_db)
    db.add_book(**BOOK_PARAMS)

    con = db_helper.connect(test_db)
    try:
        cur = con.cursor()
        cur.execute('SELECT * FROM books NATURAL JOIN publishers NATURAL JOIN bindings NATURAL JOIN locations WHERE isbn13 is :isbn13', BOOK_PARAMS)
        #cur.execute('SELECT * FROM books NATURAL JOIN publishers')
        con.commit()
        rows = cur.fetchall()
    except sqlite3.Error, e:
        print "Insertion test failure"
        print "Error: %s" % e.args[0]
    assert rows is not None
    print '{} rows'.format(repr(len(rows)))
    assert len(rows) == 1
    got_expected_result = True
    for row in rows:
        for column_name in BOOK_PARAMS.keys():
            expected = BOOK_PARAMS[column_name]
            try:
                result = row[column_name]
            except IndexError, e:
                result = None
            print 'Column: {}, Expected: {}, Result: {}'.format(column_name, expected, result)
            if not expected == result:
                got_expected_result = False
    assert got_expected_result

