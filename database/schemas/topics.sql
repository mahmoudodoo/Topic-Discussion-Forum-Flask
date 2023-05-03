DROP TABLE IF EXISTS topic;
CREATE TABLE topic (
    topicID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Topic's ID number
    topicName TEXT NOT NULL,                             -- Topic's text
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK (foreign key) of posting user
    creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                       -- Time topic was created
    updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,      -- Last time a claim/reply was added
    category TEXT NOT NULL
);
