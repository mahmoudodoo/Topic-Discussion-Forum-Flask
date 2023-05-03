/* Claim, similar to topic. */
DROP TABLE IF EXISTS claim;
CREATE TABLE claim (
    claimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- CLaim ID number
    topic INTEGER NOT NULL REFERENCES topic(topicID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of claim
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK of poisting user
    creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   -- Time topic was created
    updateTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,      -- Last time a reply was added
    text TEXT NOT NULL                                   -- Actual text
);


DROP TABLE IF EXISTS claimToClaimType;
CREATE TABLE claimToClaimType (
    claimRelTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    claimRelType TEXT NOT NULL
);
INSERT INTO claimToClaimType VALUES (1, "Opposed");
INSERT INTO claimToClaimType VALUES (2, "Equivalent");


DROP TABLE IF EXISTS claimToClaim;
CREATE TABLE claimToClaim (
    claimRelID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                        -- Claim relationship ID
    first INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of first related claim
    second INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of second related claim
    claimRelType INTEGER NOT NULL REFERENCES claimToClaimType(claimRelTypeID) ON DELETE CASCADE ON UPDATE CASCADE,
                                                                                            -- FK of type of relation
    /* Specify that there can't be several relationships between the same pair of two claims */
    CONSTRAINT claimToClaimUnique UNIQUE (first, second)
);

