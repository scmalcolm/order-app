DROP TABLE IF EXISTS order_quantities;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS ship_methods;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS publishers;
DROP TABLE IF EXISTS bindings;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS distributors;

CREATE TABLE distributors (
    dist_id     INTEGER   PRIMARY KEY,
    dist_name   TEXT      NOT NULL UNIQUE,
    address     TEXT,
    phone       TEXT,
    fax         TEXT,
    email       TEXT,
    sales_rep   TEXT,
    account_no  TEXT
);

CREATE TABLE ship_methods (
    ship_id       INTEGER   PRIMARY KEY,
    ship_method   TEXT      NOT NULL UNIQUE
);

CREATE TABLE orders (
    order_id    INTEGER   PRIMARY KEY,
    po          TEXT      NOT NULL UNIQUE,
    order_date  TEXT      NOT NULL DEFAULT CURRENT_DATE,
    ship_id     INTEGER   NOT NULL REFERENCES ship_methods ON DELETE RESTRICT,
    comment     TEXT      DEFAULT "",
    dist_id     INTEGER   NOT NULL REFERENCES distributors ON DELETE RESTRICT
);

CREATE TABLE publishers (
    pub_id      INTEGER   PRIMARY KEY,
    pub_name    TEXT      NOT NULL UNIQUE
);

CREATE TABLE locations (
    location_id   INTEGER   PRIMARY KEY,
    location      TEXT      NOT NULL UNIQUE
);

CREATE TABLE bindings (
    binding_id    INTEGER   PRIMARY KEY,
    binding       TEXT      NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id       INTEGER   PRIMARY KEY,
    isbn13        TEXT(13)  NOT NULL UNIQUE,
    title         TEXT      NOT NULL,
    binding_id    INTEGER   NOT NULL REFERENCES bindings   ON DELETE RESTRICT,
    location_id   INTEGER   NOT NULL REFERENCES locations  ON DELETE RESTRICT,
    pub_id        INTEGER   NOT NULL REFERENCES publishers ON DELETE RESTRICT
);

CREATE TABLE authors (
    author    TEXT    NOT NULL,
    book_id   INTEGER NOT NULL REFERENCES books ON DELETE CASCADE,
    PRIMARY KEY ( author, book_id )
);

CREATE TABLE order_quantities (
    order_id    INTEGER   NOT NULL REFERENCES orders ON UPDATE CASCADE,
    book_id     INTEGER   NOT NULL REFERENCES books  ON UPDATE CASCADE,
    quantity    INTEGER   NOT NULL,
    PRIMARY KEY ( order_id, book_id )
);
