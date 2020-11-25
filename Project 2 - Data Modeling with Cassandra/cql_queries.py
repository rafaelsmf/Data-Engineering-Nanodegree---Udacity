### DROP TABLES
song_info_by_session_table_drop = \
"DROP TABLE IF EXISTS song_info_by_session;"

song_user_info_by_user_session_table_drop = \
"DROP TABLE IF EXISTS song_user_info_by_user_session;"

user_info_by_given_song_table_drop = \
"DROP TABLE IF EXISTS user_info_by_given_song;"


### CREATE TABLES
song_info_by_session_table_create = ("""
CREATE TABLE IF NOT EXISTS song_info_by_session (
sessionId int, itemInSession int, artist text, song text, length float,
PRIMARY KEY (sessionId, itemInSession)
);
""")

song_user_info_by_user_session_table_create = ("""
CREATE TABLE IF NOT EXISTS song_user_info_by_user_session (
userId int, sessionId int, itemInSession int, artist text, song text, firstName text, lastName text, 
PRIMARY KEY ((userId, sessionId), itemInSession)
);
""")

user_info_by_given_song_table_create = ("""
CREATE TABLE IF NOT EXISTS user_info_by_given_song (
song text, userId int, firstName text, lastName text,
PRIMARY KEY (song, userId)
);
""")


### INSERT RECORDS
song_info_by_session_table_insert = ("""
INSERT INTO song_info_by_session (sessionId, itemInSession, artist, song, length)
VALUES (%s, %s, %s, %s, %s);
""")

song_user_info_by_user_session_table_insert = ("""
INSERT INTO song_user_info_by_user_session (userId, sessionId, itemInSession, artist, song, firstName, lastName)
VALUES (%s, %s, %s, %s, %s, %s, %s);
""")

user_info_by_given_song_table_insert = ("""
INSERT INTO user_info_by_given_song (song, userId, firstName, lastName)
VALUES (%s, %s, %s, %s);
""")


### SELECT STATEMENTS
# QUERY 1
song_info_by_session_table_select = ("""
SELECT artist, song, length 
FROM song_info_by_session
WHERE sessionId=%s AND itemInSession=%s;
""")

# QUERY 2
song_user_info_by_user_session_table_select = ("""
SELECT artist, song, firstName, lastName
FROM song_user_info_by_user_session
WHERE userId=%s AND sessionId=%s;
""")

# QUERY 3
user_info_by_given_song_table_select = ("""
SELECT firstName, lastName 
FROM user_info_by_given_song
WHERE song=%s;
""")


### QUERY LISTS
drop_table_queries = \
[song_info_by_session_table_drop, song_user_info_by_user_session_table_drop, user_info_by_given_song_table_drop]

create_table_queries = \
[song_info_by_session_table_create, song_user_info_by_user_session_table_create, user_info_by_given_song_table_create]
