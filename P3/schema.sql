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
