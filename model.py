import sqlite3

class OrderDB:
    def __init__(self, db_path=':memory:'):
        """initialize the database connection"""
        with sqlite3.connect(db_path) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute('PRAGMA foreign_keys = ON;')
            self.db_connection = connection

    def add_book(self, isbn13, title, binding, location, pub_name, authors = None):
        """add a new book to the database"""
        BOOK_INSERT_QUERY = """INSERT INTO book_view
        (isbn13, title, binding, location, pub_name)
        VALUES
        (:isbn13, :title, :binding, :location, :pub_name);"""
        AUTHOR_INSERT_QUERY = """INSERT INTO authors
        (author, book_id)
        SELECT
        ?, book_id
        FROM books WHERE isbn13 IS ? LIMIT 1;"""
        query_params = {
        'isbn13': isbn13,
        'title': title,
        'binding': binding,
        'location': location,
        'pub_name': pub_name
        }
        print 'Begin book insertion: {}'.format(repr(query_params))
        try:
            with self.db_connection as connection:
                connection.execute(BOOK_INSERT_QUERY, query_params)   
                connection.executemany(AUTHOR_INSERT_QUERY, [(n, isbn13) for n in authors])
                print 'Book insert successful.'
        except sqlite3.Error, e:
            print "Error: {}".format(e.args[0])

    def delete_book(self, isbn13):
        """remove a book from the database"""
        BOOK_DELETE_QUERY = "DELETE FROM books WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(BOOK_DELETE_QUERY, [isbn13])

    def update_book(self, **params):
        """update a book record"""
        BOOK_UPDATE_QUERY = """UPDATE book_view SET
        isbn13 = :isbn13,
        title = :title,
        binding = :binding,
        location = :location,
        pub_name = :pub_name
        WHERE isbn13 is :old_isbn13;"""
        
        with self.db_connection as connection:
            connection.execute(BOOK_UPDATE_QUERY, params)

