import sqlite3

class OrderDB:
    def __init__(self, db_path=':memory:'):
        """initialize the database connection"""
        with sqlite3.connect(db_path) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute('PRAGMA foreign_keys = ON;')
            self.db_connection = connection

    def get_book(self, isbn13):
        """rereive a book record from the database"""
        AUTHOR_QUERY = "SELECT * FROM author_view WHERE isbn13 IS ?;"
        BOOK_QUERY   = "SELECT * FROM book_view WHERE isbn13 IS ?;"
        with self.db_connection as con:
            book    = con.execute(BOOK_QUERY,   [isbn13]).fetchone()
            authors = con.execute(AUTHOR_QUERY, [isbn13]).fetchall()
        result = {}
        if book is not None:
            result = {key: book[key] for key in book.keys()}
        result['authors'] = [row['author'] for row in authors]
        return result

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

    def update_book(self, **params):
        """update a book record"""
        BOOK_UPDATE_SQL = """UPDATE book_view SET
        isbn13 = :isbn13,
        title = :title,
        binding = :binding,
        location = :location,
        pub_name = :pub_name
        WHERE isbn13 is :old_isbn13;"""
        
        with self.db_connection as connection:
            connection.execute(BOOK_UPDATE_SQL, params)

    def update_isbn(self, old_isbn13, isbn13):
        """update a book's 13-digit isbn"""
        UPDATE_SQL = "UPDATE book_view SET isbn13 = ? WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(UPDATE_SQL, (isbn13, old_isbn13))

    def update_title(self, old_isbn13, title):
        """update a book's title"""
        UPDATE_SQL = "UPDATE book_view SET title = ? WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(UPDATE_SQL, (title, old_isbn13))

    def update_binding(self, old_isbn13, binding):
        """update a book's binding"""
        UPDATE_SQL = "UPDATE book_view SET binding = ? WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(UPDATE_SQL, (binding, old_isbn13))

    def update_location(self, old_isbn13, location):
        """update a book's location"""
        UPDATE_SQL = "UPDATE book_view SET location = ? WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(UPDATE_SQL, (location, old_isbn13))

    def update_publisher(self, old_isbn13, publisher):
        """update a book's publisher"""
        UPDATE_SQL = "UPDATE book_view SET pub_name = ? WHERE isbn13 IS ?;"
        with self.db_connection as connection:
            connection.execute(UPDATE_SQL, (publisher, old_isbn13))