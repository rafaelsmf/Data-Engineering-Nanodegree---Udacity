# DROP DATA TYPES
gender_type_drop = "DROP TYPE IF EXISTS gender_type;"
level_type_drop = "DROP TYPE IF EXISTS level_type;"


# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"


# CREATE DATA TYPES
gender_type_create = "CREATE TYPE gender_type AS ENUM('F', 'M');"
level_type_create = "CREATE TYPE level_type AS ENUM('free', 'paid');"


# CREATE TABLES
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id INT PRIMARY KEY, 
first_name VARCHAR (10) NOT NULL, 
last_name VARCHAR (10) NOT NULL, 
gender gender_type NOT NULL, 
level level_type NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id VARCHAR(30) PRIMARY KEY, 
name VARCHAR (100) NOT NULL, 
location VARCHAR (100), 
latitude float, 
longitude float
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id VARCHAR(30) PRIMARY KEY, 
title VARCHAR (70) NOT NULL, 
artist_id VARCHAR(30) NOT NULL, 
year INT NOT NULL, 
duration float NOT NULL, 
FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
); 
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP PRIMARY KEY, 
hour INT NOT NULL, 
day INT NOT NULL, 
week INT NOT NULL, 
month INT NOT NULL, 
year INT NOT NULL, 
weekday VARCHAR(10) NOT NULL
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id SERIAL PRIMARY KEY, 
start_time TIMESTAMP NOT NULL, 
user_id INT, 
level level_type NOT NULL, 
song_id VARCHAR(30), 
artist_id VARCHAR(30), 
session_id INT NOT NULL, 
location VARCHAR (100) NOT NULL, 
user_agent VARCHAR (150) NOT NULL,
FOREIGN KEY (start_time) REFERENCES time (start_time),
FOREIGN KEY (user_id) REFERENCES users (user_id),
FOREIGN KEY (song_id) REFERENCES songs (song_id),
FOREIGN KEY (artist_id) REFERENCES artists (artist_id)
);
""")


# INSERT RECORDS
user_table_insert = ("""
INSERT INTO users (user_id, 
                   first_name, 
                   last_name, 
                   gender, 
                   level
                   ) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level WHERE users.level<>EXCLUDED.level;
""")

artist_table_insert = ("""
CREATE TABLE IF NOT EXISTS tmp_artists (artist_id VARCHAR(30),
                                        name VARCHAR(100),
                                        location VARCHAR(100),
                                        latitude float,
                                        longitude float
                                        );
                                        
COPY tmp_artists FROM %s WITH CSV;
                                        
INSERT INTO artists (artist_id, 
                     name, 
                     location, 
                     latitude, 
                     longitude
                     ) 
SELECT * FROM tmp_artists
ON CONFLICT DO NOTHING;

DROP TABLE tmp_artists;
""")

song_table_insert = ("""
CREATE TABLE IF NOT EXISTS tmp_songs (song_id VARCHAR(30),
                                      title VARCHAR(70),
                                      artist_id VARCHAR(30),
                                      year INT,
                                      duration float
                                      );

COPY tmp_songs FROM %s WITH CSV;

INSERT INTO songs (song_id, 
                   title, 
                   artist_id, 
                   year, 
                   duration
                   ) 
SELECT * FROM tmp_songs
ON CONFLICT DO NOTHING;

DROP TABLE tmp_songs;
""")

time_table_insert = ("""
CREATE TABLE IF NOT EXISTS tmp_time (start_time TIMESTAMP,
                                     hour INT, 
                                     day INT,
                                     week INT,
                                     month INT,
                                     year INT,
                                     weekday VARCHAR(10)
                                     );

COPY tmp_time FROM %s WITH CSV;

INSERT INTO time (start_time, 
                  hour, 
                  day, 
                  week, 
                  month, 
                  year, 
                  weekday
                  ) 
SELECT * FROM tmp_time
ON CONFLICT DO NOTHING;

DROP TABLE tmp_time;
""")

songplay_table_insert = ("""
INSERT INTO songplays (start_time, 
                       user_id, 
                       level, 
                       song_id, 
                       artist_id, 
                       session_id, 
                       location, 
                       user_agent
                       )
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")


# FIND SONGS
song_select = ("""
SELECT song_id, artists.artist_id 
FROM songs INNER JOIN artists 
ON songs.artist_id=artists.artist_id
WHERE title=%s AND name=%s AND duration=%s;
""")


# QUERY LISTS
create_data_type_queries = [gender_type_create, level_type_create]
create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_data_type_queries = [gender_type_drop, level_type_drop]
drop_table_queries = [user_table_drop, artist_table_drop, song_table_drop, time_table_drop, songplay_table_drop]