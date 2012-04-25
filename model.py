import sqlite3

class OrderDB:
    def __init__(self, db_path=':memory:'):
        """initialize the database connection"""
        try:
            self.db_connection = sqlite3.connect(db_path)
        except sqlite3.Error, e:
            print "Cannot connect to database: {}",format(db_path)
            print "Error: {}".format(e.args[0])

    def add_book(self, isbn13, title, binding, location, pub_name, authors = None):
        """add a new book to the database"""
        BOOK_INSERT_QUERY = """
        INSERT INTO books
        (isbn13, title, binding_id, location_id, pub_id)
        SELECT
        :isbn13, :title, binding_id, location_id, pub_id
        FROM bindings, publishers ON pub_name IS :pub_name,
        locations ON location IS :location
        WHERE binding IS :binding
        LIMIT 1;
        """
        AUTHOR_INSERT_QUERY = """
        INSERT INTO authors (author, book_id)
        SELECT
        ?, book_id
        FROM books
        WHERE isbn13 IS ?
        LIMIT 1;
        """
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