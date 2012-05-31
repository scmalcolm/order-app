INSERT INTO distributors
    (dist_name, address, phone, fax, email, sales_rep, account_no)
    VALUES
    ("Oxford", "123 fake street", "(555)555-0001", "(555)555-0002", "oxford@dev.null", "Steve", "42");
INSERT INTO distributors
    (dist_name, address, phone, fax, email, sales_rep, account_no)
    VALUES
    ("Penguin", "1554 UK Road", "(555)555-0011", "(555)555-0012", "penguin@dev.null", "Susan", "bmbr01");

INSERT INTO ship_methods (ship_method) VALUES ("Usual Means");
INSERT INTO ship_methods (ship_method) VALUES ("UPS");
INSERT INTO ship_methods (ship_method) VALUES ("Air");

INSERT INTO publishers (pub_name) VALUES ("Fordham");
INSERT INTO publishers (pub_name) VALUES ("Oxford");
INSERT INTO publishers (pub_name) VALUES ("Penguin");
INSERT INTO publishers (pub_name) VALUES ("Anansi");
INSERT INTO publishers (pub_name) VALUES ("William Morrow");

INSERT INTO locations (location) VALUES ("Fiction");
INSERT INTO locations (location) VALUES ("History");
INSERT INTO locations (location) VALUES ("Philosophy");

INSERT INTO bindings (binding) VALUES ("Paper");
INSERT INTO bindings (binding) VALUES ("Cloth");
INSERT INTO bindings (binding) VALUES ("Spiral");

INSERT INTO book_view VALUES
    ("9780199535569", "Pride and Prejudice", "Paper", "Fiction", "Oxford");
INSERT INTO book_view VALUES
    ("9780199537167", "Frankenstein", "Paper", "Fiction", "Oxford");
INSERT INTO book_view VALUES
    ("9780140430325", "New Grub Street", "Paper", "Fiction", "Penguin");

INSERT INTO author_view VALUES ("9780199535569", "Jane Austen");
INSERT INTO author_view VALUES ("9780199537167", "Mary Shelley");
INSERT INTO author_view VALUES ("9780140430325", "George Gissing");

INSERT INTO order_headers VALUES
    ("1A2100", date("2012-01-01"), "Usual Means", "Oxford", "No Backorders");
INSERT INTO order_headers VALUES
    ("2A2100", date("2012-01-02"), "UPS", "Oxford", "No Backorders");
INSERT INTO order_headers VALUES
    ("1C2100", date("2012-03-01"), "Usual Means", "Oxford", "No Backorders");
INSERT INTO order_headers VALUES
    ("1C2101", date("2012-03-01"), "Usual Means", "Oxford", "No Backorders");
INSERT INTO order_headers VALUES
    ("1C2200", date("2012-03-01"), "Usual Means", "Oxford", "No Backorders");
INSERT INTO order_headers VALUES
    ("1C2201", date("2012-03-01"), "Usual Means", "Oxford", "No Backorders");

INSERT INTO order_entries VALUES ("1A2100", "9780199535569", 5);
INSERT INTO order_entries VALUES ("2A2100", "9780199535569", 3);
INSERT INTO order_entries VALUES ("2A2100", "9780199537167", 25);
INSERT INTO order_entries VALUES ("1C2100", "9780199537167", 10);
INSERT INTO order_entries VALUES ("1C2101", "9780199537167", 1);
INSERT INTO order_entries VALUES ("1C2200", "9780199535569", 3);
INSERT INTO order_entries VALUES ("1C2200", "9780199537167", 25);
INSERT INTO order_entries VALUES ("1C2201", "9780199535569", 3);
INSERT INTO order_entries VALUES ("1C2201", "9780199537167", 25);
