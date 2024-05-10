CREATE TABLE snip_key (
    id          SERIAL PRIMARY KEY,
    key         TEXT UNIQUE,
    create_time TIMESTAMP,
    update_time TIMESTAMP,
    password    TEXT
);

CREATE TABLE snip_value (
    id          SERIAL PRIMARY KEY,
    key_id      INTEGER REFERENCES snip_key (id),
    value       TEXT,
    update_time TIMESTAMP
);