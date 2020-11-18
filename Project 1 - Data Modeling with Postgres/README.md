# Project: Data Modeling with Postgres

The objective of this project is to create a database on Postgres and to define an ETL pipeline for a startup called Sparkify.

Sparkify's analytics team is interested in understanding what songs their app users are listening to.

To meet the demands of the project, the following tables were created.

## Fact Table
1. **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
- songplay_id: INT, start_time: TIMESTAMP, user_id: INT, level: ENUM('free', 'paid'), song_id: VARCHAR, artist_id: VARCHAR, session_id: INT, location: VARCHAR, user_agent: VARCHAR

## Dimension Table
2. **users** - users in the app
- user_id: INT, first_name: VARCHAR, last_name: VARCHAR, gender: ENUM('F', 'M'), level: ENUM('free', 'paid')

3. **songs** - songs in music database
- song_id: VARCHAR, title: VARCHAR, artist_id: VARCHAR, year: INT, duration: FLOAT

4. **artists** - artists in music database
- artist_id: VARCHAR, name: VARCHAR, location: VARCHAR, latitude: FLOAT, longitude: FLOAT

5. **time** - timestamps of records in **songplays** broken down into specific units
- start_time: TIMESTAMP, hour: INT, day: INT, week: INT, month: INT, year: INT, weekday: VARCHAR

