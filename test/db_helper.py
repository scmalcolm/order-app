import sqlite3

schema_file = 'db/create_tables.sql'
view_file = 'db/create_views.sql'
test_data_file = 'test/test_data.sql'

def connect(db = ":memory:"):
    with sqlite3.connect(db) as connection:
        connection.row_factory = sqlite3.Row
        return connection

def close(connection):
    """close a db connection"""
    if connection:
        connection.close();

def prepare_test_database(db = ":memory:"):
    """prepare the test database and return a connection"""
    with open(schema_file) as f:
        create_tables_sql = f.read()
    with open(test_data_file) as f:
        insert_data_sql = f.read()
    with open(view_file) as f:
        create_views_sql = f.read()

    with sqlite3.connect(db) as connection:
        connection.row_factory = sqlite3.Row
        connection.executescript(create_tables_sql)
        connection.executescript(insert_data_sql)
        connection.executescript(create_views_sql)
        return connection
