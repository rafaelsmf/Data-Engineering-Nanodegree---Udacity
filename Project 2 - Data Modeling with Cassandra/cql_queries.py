### DROP TABLES
session_history_table_drop = "DROP TABLE IF EXISTS session_history;"
user_history_table_drop = "DROP TABLE IF EXISTS user_history;"
song_history_table_drop = "DROP TABLE IF EXISTS song_history;"


### CREATE TABLES
session_history_table_create = ("""
CREATE TABLE IF NOT EXISTS session_history (
sessionId int, itemInSession int, artist text, song text, length float,
PRIMARY KEY (sessionId, itemInSession)
);
""")

user_history_table_create = ("""
CREATE TABLE IF NOT EXISTS user_history (
userId int, sessionId int, itemInSession int, artist text, song text, firstName text, lastName text, 
PRIMARY KEY (userId, sessionId, itemInSession)
);
""")

song_history_table_create = ("""
CREATE TABLE IF NOT EXISTS song_history (
song text, sessionId int, itemInSession int, firstName text, lastName text,
PRIMARY KEY (song, sessionId, itemInSession)
);
""")


### INSERT RECORDS
session_history_table_insert = ("""
INSERT INTO session_history (sessionId, itemInSession, artist, song, length)
VALUES (%s, %s, %s, %s, %s);
""")

user_history_table_insert = ("""
INSERT INTO user_history (userId, sessionId, itemInSession, artist, song, firstName, lastName)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

song_history_table_insert = ("""
INSERT INTO song_history (song, sessionId, itemInSession, firstName, lastName)
VALUES (%s, %s, %s, %s, %s);
""")


### SELECT STATEMENTS
# QUERY 1
session_history_table_select = ("""
SELECT artist, song, length 
FROM session_history
WHERE sessionId=%s AND itemInSession=%s;
""")

# QUERY 2
user_history_table_select = ("""
SELECT artist, song, firstName, lastName
FROM user_history
WHERE userId=%s AND sessionId=%s;
""")

# QUERY 3
song_history_table_select = ("""
SELECT firstName, lastName 
FROM song_history
WHERE song=%s;
""")


### QUERY LISTS
drop_table_queries = [session_history_table_drop, user_history_table_drop, song_history_table_drop]
create_table_queries = [session_history_table_create, user_history_table_create, song_history_table_create]
