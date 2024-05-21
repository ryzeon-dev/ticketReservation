create table event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    event_date TEXT,
    price FLOAT
);

create table user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT,
    password TEXT
);

create table token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER,
    token TEXT
);

create table reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event INTEGER,
    user INTEGER
);

create table payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation INTEGER,
    account TEXT,
    price FLOAT
);
