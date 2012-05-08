INSERT INTO distributors
    (dist_name, address, phone, fax, email, sales_rep, account_no)
    VALUES
    ("Oxford", "123 fake street", "(555)555-0001", "(555)555-0002", "oxford@dev.null", "Steve", "42");
INSERT INTO distributors
    (dist_name, address, phone, fax, email, sales_rep, account_no)
    VALUES
    ("Penguin", "1554 UK Road", "(555)555-0011", "(555)555-0012", "penguin@dev.null", "Susan", "bmbr01");

INSERT INTO ship_methods
    (ship_method)
    VALUES
    ("Ususal Means");
INSERT INTO ship_methods
    (ship_method)
    VALUES
    ("UPS");
INSERT INTO ship_methods
    (ship_method)
    VALUES
    ("Air");

INSERT INTO publishers
    (pub_name)
    VALUES
    ("Fordham");
INSERT INTO publishers
    (pub_name)
    VALUES (
    "Oxford");
INSERT INTO publishers
    (pub_name)
    VALUES
    ("Penguin");
INSERT INTO publishers
    (pub_name)
    VALUES
    ("Anansi");
INSERT INTO publishers
    (pub_name)
    VALUES
    ("William Morrow");

INSERT INTO locations
    (location)
    VALUES
    ("Fiction");
INSERT INTO locations
    (location)
    VALUES
    ("History");
INSERT INTO locations
    (location)
    VALUES
    ("Philosophy");

INSERT INTO bindings
    (binding)
    VALUES
    ("Paper");
INSERT INTO bindings
    (binding)
    VALUES
    ("Cloth");
INSERT INTO bindings
    (binding)
    VALUES
    ("Spiral");

INSERT INTO books
    (isbn13, title, binding_id, location_id, pub_id)
    SELECT
    "9780199535569", "Pride and Prejudice", binding_id, location_id, pub_id
    FROM bindings, publishers ON pub_name IS "Oxford", locations ON location IS "Fiction"
    WHERE binding IS "Paper"
    LIMIT 1;

INSERT INTO books
    (isbn13, title, binding_id, location_id, pub_id)
    SELECT
    "9780199537167", "Frankenstein", binding_id, location_id, pub_id
    FROM bindings, publishers ON pub_name IS "Oxford", locations ON location IS "Fiction"
    WHERE binding IS "Paper"
    LIMIT 1;

INSERT INTO authors
    (author, book_id)
    SELECT
    "Jane Austen", book_id
    FROM books WHERE isbn13 IS "9780199535569"
    LIMIT 1;

INSERT INTO authors
    (author, book_id)
    SELECT
    "Mary Shelley", book_id
    FROM books WHERE isbn13 IS "9780199537167"
    LIMIT 1;

INSERT INTO orders
    (po, order_date, ship_id, comment, dist_id)
    SELECT
    "1A2100", date("2012-01-01"), ship_id, "No Backorders", 1
    FROM ship_methods WHERE ship_method IS "Ususal Means"
    LIMIT 1;

INSERT INTO order_quantities
    (order_id, book_id, quantity)
    SELECT
    order_id, book_id, 5
    FROM orders, books ON isbn13 IS "9780199535569"
    WHERE po IS "1A2100"
    LIMIT 1;