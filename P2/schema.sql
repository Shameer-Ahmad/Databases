
CREATE TABLE restaurant (
    restaurant_ID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    street_name TEXT NOT NULL,
    apt_number TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    cuisine_type TEXT,
    FOREIGN KEY (zip_code) REFERENCES neighborhood_zip(zip_code)
);

CREATE TABLE restaurant_phone (
    restaurant_ID INTEGER,
    phone_number TEXT,
    PRIMARY KEY (restaurant_ID, phone_number),
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(restaurant_ID),
    CHECK (phone_number LIKE '___-___-____')
);

CREATE TABLE owner_admin (
    owner_ID INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    middle_initial TEXT,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE owner_phone (
    owner_ID INTEGER,
    phone_number TEXT,
    PRIMARY KEY (owner_ID, phone_number),
    FOREIGN KEY (owner_ID) REFERENCES owner_admin(owner_ID),
    CHECK (phone_number LIKE '___-___-____')
);

CREATE TABLE event (
    event_ID INTEGER PRIMARY KEY,
    date_time DATETIME,
    capacity INTEGER CHECK (capacity > 0)
);

CREATE TABLE menu_item (
    restaurant_ID INTEGER,
    item_name TEXT,
    cuisine_type TEXT,
    description TEXT,
    PRIMARY KEY (restaurant_ID, item_name),
    FOREIGN KEY (restaurant_ID) REFERENCES restaurant(restaurant_ID)
);

CREATE TABLE review (
    user_ID TEXT,
    date_time DATETIME,
    text TEXT,
    score REAL CHECK (score BETWEEN 0.0 AND 5.0),
    PRIMARY KEY (user_ID, date_time),
    FOREIGN KEY (user_ID) REFERENCES customer(username)
);

CREATE TABLE neighborhood (
    neighborhood_name TEXT PRIMARY KEY,
    common_cuisines TEXT,
    description TEXT
);

CREATE TABLE neighborhood_zip (
    neighborhood_name TEXT,
    zip_code TEXT NOT NULL,
    PRIMARY KEY (neighborhood_name, zip_code),
    FOREIGN KEY (neighborhood_name) REFERENCES neighborhood(neighborhood_name)
);

CREATE TABLE customer (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL CHECK (LENGTH(password) >= 8),
    first_name TEXT NOT NULL,
    middle_initial TEXT,
    last_name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    street_name TEXT NOT NULL,
    apt_number TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    date_of_birth DATE,
    FOREIGN KEY (zip_code) REFERENCES neighborhood_zip(zip_code),
    CHECK (zip_code >= '02108' AND zip_code <= '02467')
);

CREATE TABLE customer_phone (
    username TEXT,
    phone_number TEXT,
    PRIMARY KEY (username, phone_number),
    FOREIGN KEY (username) REFERENCES customer(username),
    CHECK (phone_number LIKE '___-___-____')
);
