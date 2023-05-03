import sqlite3

connection = sqlite3.connect('database/database.db')


with open('database/schemas/users.sql') as f:
    connection.executescript(f"""{f.read()}""")

with open('database/schemas/topics.sql') as f:
    connection.executescript(f"""{f.read()}""")

with open('database/schemas/replies.sql') as f:
    connection.executescript(f"""{f.read()}""")

with open('database/schemas/claims.sql') as f:
    connection.executescript(f"""{f.read()}""")


connection.commit()
connection.close()