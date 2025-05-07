DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('customer', 'owner')) NOT NULL,
    is_logged BOOLEAN NOT NULL DEFAULT 0
);

