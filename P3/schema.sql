DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS rsvp;
DROP TABLE IF EXISTS event;

CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('customer', 'owner')) NOT NULL,
    is_logged BOOLEAN NOT NULL DEFAULT 0
);


DROP TABLE IF EXISTS restaurant;

CREATE TABLE restaurant (
    restaurant_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    restaurant_name TEXT NOT NULL,
    street_number TEXT NOT NULL,
    street_name TEXT NOT NULL,
    apt_number TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    cuisine_type TEXT,
    FOREIGN KEY (zip_code) REFERENCES neighborhood_zip(zip_code)
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
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

CREATE TABLE event (
    event_ID INTEGER PRIMARY KEY,
    event_name TEXT,
    date_time DATETIME,
    capacity INTEGER CHECK (capacity > 0)
);


CREATE TABLE rsvp (
    user_ID  INTEGER NOT NULL,
    event_ID INTEGER NOT NULL,
    PRIMARY KEY (user_ID, event_ID),
    FOREIGN KEY (user_ID)  REFERENCES user(id),
    FOREIGN KEY (event_ID) REFERENCES event(event_ID)
);



