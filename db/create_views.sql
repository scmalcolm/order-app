DROP VIEW IF EXISTS order_headers;
DROP VIEW IF EXISTS order_entries;

CREATE VIEW order_headers AS
SELECT DISTINCT
    po, order_date, ship_method, dist_name,
    address, phone, fax, account_no, sales_rep, comment
FROM 
    orders       NATURAL JOIN
    distributors NATURAL JOIN
    ship_methods;

CREATE VIEW order_entries AS
SELECT
    po, isbn, title, quantity, pub_name, binding
FROM
    books            NATURAL JOIN
    orders           NATURAL JOIN
    order_quantities NATURAL JOIN
    publishers       NATURAL JOIN
    bindings;
