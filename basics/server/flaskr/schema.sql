DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS mac;
DROP TABLE IF EXISTS volt;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE room (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  roomname TEXT NOT NULL UNIQUE,
  hash TEXT
);

CREATE TABLE mac (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mac TEXT UNIQUE NOT NULL,
  roomid INTEGER UNIQUE,
  FOREIGN KEY(roomid) REFERENCES room(id)
);

CREATE TABLE volt (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  volt REAL,
  macid INT NOT NULL,
  statusTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (macid) REFERENCES mac(id) 
)