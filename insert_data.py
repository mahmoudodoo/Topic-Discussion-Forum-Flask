import sqlite3

connection = sqlite3.connect('database/database.db')

cur = connection.cursor()


# Insert 5 users to the user table
cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,lastVisit) VALUES (?, ?, ?, ?)",
            ('user1', '123456', True, 12)
            )
cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,lastVisit) VALUES (?, ?, ?, ?)",
            ('user2', '123456', True, 1)
            )
cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,lastVisit) VALUES (?, ?, ?, ?)",
            ('user3', '123456', True, 13)
            )
cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,lastVisit) VALUES (?, ?, ?, ?)",
            ('user4', '123456', True, 20)
            )
cur.execute("INSERT INTO user (userName, passwordHash,isAdmin,lastVisit) VALUES (?, ?, ?, ?)",
            ('user5', '123456', True, 23)
            )

# Insert 10 topics to the topic table
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 1', 1,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 2', 3,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 3', 2,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 4', 3,'IT')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 5', 1,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 6', 5,'Travel')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 7', 3,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 8', 5,'IT')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 9', 2,'Sport')
            )
cur.execute("INSERT INTO topic (topicName, postingUser, category) VALUES (?, ?, ?)",
            ('Topic 10',1,'Sport')
            )


# Insert 6 clames to the claim table
import secrets
# Declaring names, verbs and nouns
names=["You","I","They","He","She","Robert","Steve"]
verbs=["was", "is", "are", "were"]
nouns=["playing cricket.", "watching television.", "singing.", "fighting.", "cycling."]
a=(secrets.choice(names)) # generate a random word inside 'a' variable from names list
b=(secrets.choice(verbs)) # generate a random word inside 'b' variable from verbs list
c=(secrets.choice(nouns)) # generate a random word inside 'c' variable from nouns list

cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (2,4,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))


cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (4,2,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))

cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (7,1,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))


cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (5,3,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))

cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (2,5,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))

cur.execute("INSERT INTO claim (topic, postingUser, text) VALUES (?, ?, ?)",
            (8,1,f"{a} {b} {c}")
            )

a=(secrets.choice(names))
b=(secrets.choice(verbs))
c=(secrets.choice(nouns))


connection.commit()
connection.close()