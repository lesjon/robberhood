CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    hash CHAR(64) NOT NULL,
    text_data TEXT NOT NULL
);