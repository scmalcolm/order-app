DROP VIEW IF EXISTS order_headers;
DROP VIEW IF EXISTS order_entries;
DROP VIEW IF EXISTS book_view;

CREATE VIEW order_headers AS
SELECT DISTINCT
    po, order_date, ship_method, dist_name,
    address, phone, fax, account_no, sales_rep, comment, order_id
FROM 
    orders       NATURAL JOIN
    distributors NATURAL JOIN
    ship_methods;

CREATE VIEW order_entries AS
SELECT
    po, isbn13, title, quantity, pub_name, binding, order_id
FROM
    books            NATURAL JOIN
    orders           NATURAL JOIN
    order_quantities NATURAL JOIN
    publishers       NATURAL JOIN
    bindings;

CREATE VIEW book_view AS
SELECT
    isbn13, title, binding, location, pub_name
FROM
    books       NATURAL JOIN
    bindings    NATURAL JOIN
    locations   NATURAL JOIN
    publishers;


