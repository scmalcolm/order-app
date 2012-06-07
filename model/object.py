'''
Bob Miller Book Room ordering application

Copyright Simon Malcolm 2012
'''
import sqlite3
from datetime import date

class OrderDB:
    def __init__(self, db_path=':memory:'):
        """initialize the database connection"""
        with sqlite3.connect(db_path) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute('PRAGMA foreign_keys = ON;')
            self.db_connection = connection

    def is_book(self, isbn13):
        QUERY = 'SELECT isbn13 FROM book_view WHERE isbn13 IS ?;'
        with self.db_connection as con:
            count = con.execute(QUERY, [isbn13]).fetchall()
        return len(count) == 1

    def get_book(self, isbn13):
        """rereive a book record from the database"""
        AUTHOR_QUERY = "SELECT * FROM author_view WHERE isbn13 IS ?;"
        BOOK_QUERY   = "SELECT * FROM book_view WHERE isbn13 IS ?;"
        with self.db_connection as con:
            book_row    = con.execute(BOOK_QUERY,   [isbn13]).fetchone()
            author_rows = con.execute(AUTHOR_QUERY, [isbn13]).fetchall()
        return make_book(book_row, author_rows)

    def get_books(self, authors = False):
        """retrieve all books from the database"""
        BOOKS_QUERY = "SELECT * FROM book_view;"
        with self.db_connection as con:
            books = [make_book(row) for row in con.execute(BOOKS_QUERY)]
        return books

    def add_book(self, isbn13, title, binding, location, pub_name, authors = None):
        """add a new book to the database"""
        BOOK_INSERT_SQL = """INSERT INTO book_view VALUES
        (:isbn13, :title, :binding, :location, :pub_name);"""
        AUTHOR_INSERT_SQL = "INSERT INTO author_view VALUES (?, ?);"
        query_params = {
        'isbn13': isbn13,
        'title': title,
        'binding': binding,
        'location': location,
        'pub_name': pub_name
        }
        try:
            with self.db_connection as connection:
                connection.execute(BOOK_INSERT_SQL, query_params)   
                connection.executemany(AUTHOR_INSERT_SQL, [(isbn13, n) for n in authors])
        except sqlite3.Error, e:
            print "Error: {}".format(e.args[0])

    def delete_book(self, isbn13):
        """remove a book from the database"""
        BOOK_DELETE_SQL = "DELETE FROM book_view WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(BOOK_DELETE_SQL, [isbn13])

    def update_book(self, old_isbn13, **new_values):
        template = "UPDATE book_view SET {} WHERE isbn13 IS :old_isbn13;"
        columns = ['isbn13', 'title', 'binding', 'location', 'pub_name']
        updates = []
        params = {'old_isbn13': old_isbn13}
        for column_name in columns:
            if column_name in new_values:
                updates.append("{0} = :{0}".format(column_name))
                params[column_name] = new_values[column_name]
        if len(updates) > 0:
            sql = template.format(', '.join(updates))
            print sql
            print params
            try:
                with self.db_connection as con:
                    con.execute(sql, params)
            except sqlite3.Error, e:
                print "Error: {}".format(e.args[0])

    def get_order(self, po):
        """retrieve order data from the db for the given po"""
        HEADER_QUERY = "SELECT * FROM order_headers WHERE po IS ?;"
        ENTRY_QUERY = "SELECT * FROM order_entries WHERE po IS ?;"
        with self.db_connection as con:
            header_row = con.execute(HEADER_QUERY, [po]).fetchone()
            entry_rows = con.execute(ENTRY_QUERY, [po]).fetchall()
        return make_order(header_row, entry_rows)

    def create_order(self, po, ship_method, dist_name,
                     order_date = None, comment = "", entries = []):
        INSERT_SQL = "INSERT INTO order_headers VALUES (?, ?, ?, ?, ?);"
        ENTRIES_SQL = "INSERT INTO order_entries VALUES (?, ?, ?);"
        if order_date is None:
            order_date = date.today().isoformat()
        with self.db_connection as con:
            con.execute(INSERT_SQL,
                        [po, order_date, ship_method, dist_name, comment])
            if len(entries) > 0:
                con.executemany(ENTRIES_SQL, 
                                [[po, entry['isbn13'], entry['quantity']] for entry in entries])

    def add_order_entry(self, po, isbn13, quantity = 1):
        INSERT_SQL = "INSERT INTO order_entries VALUES (:po, :isbn13, :quantity);"
        with self.db_connection as con:
            con.execute(INSERT_SQL, locals())

    def update_order(self, old_po, **new_values):
        template = "UPDATE order_headers SET {} WHERE po IS :old_po;"
        columns = ['po', 'ship_method', 'dist_name', 'order_date', 'comment']
        updates = []
        params = {'old_po': old_po}
        for column_name in columns:
            if column_name in new_values:
                updates.append("{0} = :{0}".format(column_name))
                params[column_name] = new_values[column_name]
        if len(updates) > 0:
            sql = template.format(', '.join(updates))
            with self.db_connection as con:
                con.execute(sql, params)

    def update_order_entry(self, po, old_isbn13, **new_values):
        template = "UPDATE order_entries SET {} WHERE po IS :po AND isbn13 IS :isbn13;"
        columns = ['isbn13', 'quantity']
        updates = []
        params = {'old_isbn13': old_isbn13, 'po': po}
        for column_name in columns:
            if column_name in new_values:
                updates.append("{0} = :{0}".format(column_name))
                params[column_name] = new_values[column_name]
        if len(updates) > 0:
            sql = template.format(', '.join(updates))
            with self.db_connection as con:
                con.execute(sql, params)

    def delete_order_entry(self, po, isbn13):
        sql = "DELETE FROM order_entries WHERE po IS ? AND isbn13 IS ?;"
        with self.db_connection as con:
            con.execute(sql, [po, isbn13])

    def delete_order(self, po):
        delete_order = "DELETE FROM order_headers WHERE po IS ?;"
        delete_entries = "DELETE FROM order_entries WHERE po IS ?"
        with self.db_connection as con:
            con.execute(delete_entries, [po])
            con.execute(delete_order, [po])

    def publishers(self):
        QUERY = "SELECT pub_name FROM publishers;"
        with self.db_connection as con:
            rows = con.execute(QUERY)
        result = [row['pub_name'] for row in rows]
        return result

    def locations(self):
        QUERY = "SELECT location FROM locations;"
        with self.db_connection as con:
            rows = con.execute(QUERY)
        result = [row['location'] for row in rows]
        return result
    
    def bindings(self):
        QUERY = "SELECT binding FROM bindings;"
        with self.db_connection as con:
            rows = con.execute(QUERY)
        result = [row['binding'] for row in rows]
        return result

def make_book(book_row, author_rows = None):
    if book_row is not None:
        book = {}
        for key in ['isbn13', 'title', 'binding', 'location', 'pub_name']:
            book[key] = book_row[key]
        if author_rows is not None:
            book['authors'] = [row['author'] for row in author_rows]
        return book

def make_order(header_row, entry_rows = None):
    if header_row is not None:
        header_keys = ['po', 'order_date', 'ship_method', 'dist_name', 'comment']
        order = {key: header_row[key] for key in keys}
        if entry_rows is not None:
            entry_keys = ['isbn13', 'quantity']
            order['entries'] = [{key: row[key] for key in entry_keys} for row in entry_rows]
        return order
