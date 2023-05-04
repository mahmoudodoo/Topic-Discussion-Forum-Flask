/* Replies can be made to either claims or other replies, so create a table to store the common parts of a
   reply (the text, poster, etc) separately from their relationship to other content.
 */
DROP TABLE IF EXISTS replyText;
CREATE TABLE replyText (
    replyTextID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                           -- Reply ID
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK of posting user
    creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,                                                   -- Posting time
    text TEXT NOT NULL                                                                -- Text of reply
);

/* Store the relationships of claims to replies. */
DROP TABLE IF EXISTS replyToClaimType;
CREATE TABLE replyToClaimType (
    claimReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    claimReplyType TEXT NOT NULL
);
INSERT INTO replyToClaimType VALUES (1, "Clarification");
INSERT INTO replyToClaimType VALUES (2, "Supporting Argument");
INSERT INTO replyToClaimType VALUES (3, "Counterargument");

DROP TABLE IF EXISTS replyToClaim;
CREATE TABLE replyToClaim (
    replyToClaimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                       -- Relationship ID
    reply INTEGER NOT NULL REFERENCES replyText (replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,   -- FK of related reply
    claim INTEGER NOT NULL REFERENCES claim (claimID) ON DELETE CASCADE ON UPDATE CASCADE,           -- FK of related claim
    replyToClaimRelType INTEGER NOT NULL REFERENCES replyToClaimType(claimReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE -- FK of relation type
);


/* Store the relationship of replies to other replies.
   Note that we use the replyText row as the FK for the "parent" reply (ie, the one this is a response to),
   because we do not know if it is a replyToClaim or another replyToReply.
   */
DROP TABLE IF EXISTS replyToReplyType;
CREATE TABLE replyToReplyType (
    replyReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    replyReplyType TEXT NOT NULL
);
INSERT INTO replyToReplyType VALUES (1, "Evidence");
INSERT INTO replyToReplyType VALUES (2, "Support");
INSERT INTO replyToReplyType VALUES (3, "Rebuttal");


DROP TABLE IF EXISTS replyToReply;
CREATE TABLE replyToReply (
    replyToReplyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                         -- Relationship ID
    reply INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,
    parent INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,
    replyToReplyRelType INTEGER NOT NULL REFERENCES replyToReplyType(replyReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE
)



