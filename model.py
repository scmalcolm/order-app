import sqlite3

class OrderDB:
    def __init__(self, db_path=':memory:'):
        """initialize the database connection"""
        try:
            self.db_connection = sqlite3.connect(db_path)
        except sqlite3.Error, e:
            print "Cannot connect to database: %s" % db_path
            print "Error: %s" % e.args[0]
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
        query_params = {
        'isbn13': isbn13,
        'title': title,
        'binding': binding,
        'location': location,
        'pub_name': pub_name
        }
        print 'Begin book insert: {}'.format(repr(query_params))
        try:
            cur = self.db_connection.cursor()
            cur.execute(BOOK_INSERT_QUERY, query_params)
        except sqlite3.Error, e:
            print "Cannot insert book: %s" % isbn13
            print "Error: %s" % e.args[0]
        else:
            self.db_connection.commit()
