DROP VIEW IF EXISTS order_headers;
DROP VIEW IF EXISTS order_entries;
DROP VIEW IF EXISTS book_view; 

CREATE VIEW order_headers AS
    SELECT DISTINCT
        po, order_date, ship_method, dist_name, comment
    FROM 
        orders       NATURAL JOIN
        distributors NATURAL JOIN
        ship_methods;

CREATE TRIGGER order_headers_insert INSTEAD OF INSERT ON order_headers BEGIN
    INSERT INTO orders
        (po, order_date, ship_id, dist_id, comment)
        SELECT
        NEW.po, NEW.order_date, ship_id, dist_id, NEW.comment
        FROM
        ship_methods, distributors ON dist_name IS NEW.dist_name
        WHERE ship_method IS NEW.ship_method
        LIMIT 1;
    END;

CREATE TRIGGER order_headers_update INSTEAD OF UPDATE ON order_headers BEGIN
    UPDATE orders SET
    po = NEW.po,
    order_date = NEW.order_date,
    ship_id = (SELECT ship_id FROM ship_methods WHERE ship_method IS NEW.ship_method),
    comment = NEW.comment,
    dist_id = (SELECT dist_id FROM distributors WHERE dist_name IS NEW.dist_name)
    WHERE po is OLD.po;
    END;

CREATE TRIGGER order_headers_delete INSTEAD OF DELETE ON order_headers BEGIN
    DELETE FROM orders WHERE po IS OLD.po;
    END;

CREATE VIEW order_entries AS
    SELECT
        po, isbn13, title, quantity, pub_name, binding
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

CREATE TRIGGER book_view_insert INSTEAD OF INSERT ON book_view BEGIN
    INSERT INTO books
        (isbn13, title, binding_id, location_id, pub_id)
        SELECT
        NEW.isbn13, NEW.title, binding_id, location_id, pub_id
        FROM
        bindings,
        publishers ON pub_name IS NEW.pub_name,
        locations ON location IS NEW.location
        WHERE binding IS NEW.binding
        LIMIT 1;
    END;

CREATE TRIGGER book_view_update INSTEAD OF UPDATE ON book_view BEGIN
    UPDATE books SET
    isbn13 = NEW.isbn13,
    title = NEW.title,
    binding_id = (SELECT binding_id FROM bindings WHERE binding IS NEW.binding),
    location_id = (SELECT location_id FROM locations WHERE location IS NEW.location),
    pub_id = (SELECT pub_id FROM publishers WHERE pub_name IS NEW.pub_name)
    WHERE isbn13 IS OLD.isbn13;
    END;

CREATE TRIGGER book_view_delete INSTEAD OF DELETE ON book_view BEGIN
    DELETE FROM books WHERE isbn13 IS OLD.isbn13;
    END;
