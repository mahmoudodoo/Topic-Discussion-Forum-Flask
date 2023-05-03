PRAGMA foreign_keys = ON;

/* Users table. */
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Integer user ID / key
    userName TEXT NOT NULL,                            -- Login username
    passwordHash BLOB NOT NULL,                        -- Hashed password (bytes in python)
    isAdmin BOOLEAN NOT NULL,                          -- If user is admin or not. Ignore if not implementing admin
    creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                     -- Time user was created
    lastVisit INTEGER NOT NULL                         -- User's last visit, for showing new content when they return
);