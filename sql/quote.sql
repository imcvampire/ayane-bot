CREATE TABLE quotes (
    id serial NOT NULL PRIMARY KEY,
    author varchar(25) NOT NULL UNIQUE,
    content text NOT NULL
);
