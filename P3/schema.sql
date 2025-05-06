DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS restaurant;

CREATE TABLE restaurant (
    restaurant_id INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    street_name TEXT NOT NULL,
    apt_number TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    cuisine_type TEXT,
    FOREIGN KEY (zip_code) REFERENCES neighborhood_zip(zip_code)
);

DROP TABLE IF EXISTS restaurant_phone;

CREATE TABLE restaurant_phone (
    restaurant_id INTEGER,
    phone_number TEXT,
    PRIMARY KEY (restaurant_id, phone_number),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id),
    CHECK (phone_number LIKE '___-___-____')
);

DROP TABLE IF EXISTS review;

CREATE TABLE review (
    user_id TEXT,
    restaurant_id INTEGER,
    date_time DATETIME,
    text TEXT,
    score REAL CHECK (score BETWEEN 0.0 AND 5.0),
    PRIMARY KEY (user_id, date_time),
    FOREIGN KEY (user_id) REFERENCES customer(username),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
);
