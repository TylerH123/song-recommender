PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(256)
);

CREATE TABLE songs(
    sid VARCHAR(256) PRIMARY KEY,
    title VARCHAR(256)
);

CREATE TABLE favorites(
    username VARCHAR(20), 
    sid INTEGER,
    state VARCHAR(256), 
    PRIMARY KEY (username, sid),
    FOREIGN KEY (username) REFERENCES users (username)
        ON DELETE CASCADE, 
    FOREIGN KEY (sid) REFERENCES songs (sid)
        ON DELETE CASCADE
)