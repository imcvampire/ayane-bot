CREATE TABLE IF NOT EXISTS history (
    id serial NOT NULL PRIMARY KEY,
    message text NOT NULL,
    flag varchar(100),
    created_at time NOT NULL
);

CREATE TABLE IF NOT EXISTS quotes (
    id serial NOT NULL PRIMARY KEY,
    author text NOT NULL,
    content text NOT NULL,
    creator text NOT NULL,
    created_at time NOT NULL
);
