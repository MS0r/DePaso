DROP TABlE IF EXISTS user;
DROP TABLE IF EXISTS travel;

CREATE TABLE user (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text UNIQUE NOT NULL,
    password text NOT NULL,
    email text UNIQUE NOT NULL,
    location text,
    time_now TIMESTAMP,
    postal integer NOT NULL
);

CREATE TABLE travel (
    id  integer PRIMARY KEY AUTOINCREMENT,
    /*travel's host/driver*/
    user_id integer NOT NULL, 
    price float NOT NULL,
    departure text NOT NULL,
    arrival text NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    departure_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    passengers integer NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES user (id)
);