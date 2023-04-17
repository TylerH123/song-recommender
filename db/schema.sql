PRAGMA foreign_keys = ON;

CREATE TABLE users(
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20),
    password VARCHAR(256)
);

CREATE TABLE songs(
    sid INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(256)
);

CREATE TABLE favorites(
    uid INTEGER, 
    sid INTEGER,
    state VARCHAR(256), 
    PRIMARY KEY (uid, sid),
    FOREIGN KEY (uid) REFERENCES users (uid)
        ON DELETE CASCADE, 
    FOREIGN KEY (sid) REFERENCES songs (sid)
        ON DELETE CASCADE
)