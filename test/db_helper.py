import sqlite3

schema_file = 'db/create_tables.sql'
test_data_file = 'test/test_data.sql'

def connect(db = ":memory:"):
    """return a db connection"""
    connection = None
    try:
        connection = sqlite3.connect(db)
        connection.row_factory = sqlite3.Row
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]
    return connection

def close(connection):
    """close a db connection"""
    if connection:
        connection.close();

def repopulate(connection):
    """recreate the test db from file"""
    test_data = None
    schema = None
    with open(schema_file) as f:
        schema = f.read()
    with open(test_data_file) as f:
        insert_data = f.read()
    try:
        connection.executescript(schema)
        connection.executescript(insert_data)
    except sqlite3.Error, e:
        print "Cannot repopulate test database!"
        print "Error: %s" % e.args[0]
    else:
        connection.commit()