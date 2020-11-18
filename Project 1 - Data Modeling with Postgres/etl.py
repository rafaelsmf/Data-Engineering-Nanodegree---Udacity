import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Reads the song file. 
    - Extracts data for artists table and save it to a temporary file.
    - Inserts records into artists table from the respective temporary file using
    `artist_table_insert` query and after that, remove the temporary file.
    - Extracts data for songs table and save it to a temporary file.
    - Inserts records into songs table from the respective temporary file using
    `song_table_insert` query and after that, remove the temporary file.
    
        Parameters:
            - cur: psycopg2.connect.cursor()
            - filepath: str
    """
    df = pd.read_json(filepath, lines=True)
    
    artists_column_labels = ['artist_id', 'artist_name', 'artist_location', 
                             'artist_latitude', 'artist_longitude']
    artists_data = df[artists_column_labels].copy()
    artists_data.drop_duplicates(inplace=True)
    
    tmp_artists_data_filepath = filepath.split('.json')[0] + '_' + 'filtered_artists_data' + '.tmp'
    artists_data.to_csv(tmp_artists_data_filepath, header=False, index=False)
    
    cur.execute(artist_table_insert, (tmp_artists_data_filepath,))
    
    os.remove(tmp_artists_data_filepath)
    
    songs_column_labels = ['song_id', 'title', 'artist_id', 'year', 'duration']
    songs_data = df[songs_column_labels].copy()
    songs_data.drop_duplicates(inplace=True)
    
    tmp_songs_data_filepath = filepath.split('.json')[0] + '_' + 'filtered_songs_data' + '.tmp'
    songs_data.to_csv(tmp_songs_data_filepath, header=False, index=False)
    
    cur.execute(song_table_insert, (tmp_songs_data_filepath,))
    
    os.remove(tmp_songs_data_filepath)
    

def process_log_file(cur, filepath):
    """
    - Reads the log file and filter records by `Next Song` action.
    - Converts the `ts` timestamp column to datetime.
    - Extracts data from `ts` column for time table and save it to a temporary file.
    - Inserts records into time table from the respective temporary file using 
    `time_table_insert` query and after that, remove the temporary file.
    - Extracts data for users table.
    - Inserts records into users table using `user_table_insert` query. 
    - Iterates over each row of the log file associated and find their correspondent
    `song_id` and `artist_id` (IF EXISTS). 
    Then, extracts the remaining data for songplay table.
    - Inserts records into songplay table using `songplay_table_insert` query.
    
        Parameters:
            - cur: psycopg2.connect.cursor()
            - filepath: str
    """
    df = pd.read_json(filepath, lines=True)

    df = df.loc[df['page']=='NextSong']

    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    time_data = list((df['ts'].values, df['ts'].dt.hour.values,
                      df['ts'].dt.day.values, df['ts'].dt.weekofyear.values, 
                      df['ts'].dt.month.values, df['ts'].dt.year.values,
                      df['ts'].dt.day_name().values))
    time_column_labels = list(['timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday'])
    time_df = pd.DataFrame.from_dict({time_column_labels[i]: time_data[i] for i in range(len(time_data))})
    time_df.drop_duplicates(inplace=True)
    
    tmp_time_data_filepath = filepath.split('.json')[0] + '_' + 'filtered_time_data' + '.tmp'
    time_df.to_csv(tmp_time_data_filepath, header=False, index=False)
   
    cur.execute(time_table_insert, (tmp_time_data_filepath,))
   
    os.remove(tmp_time_data_filepath)
       
    users_column_labels = ['userId', 'firstName', 'lastName', 'gender', 'level']
    users_df =  df[users_column_labels].copy()
    
    for row in users_df.values:
        cur.execute(user_table_insert, list(row))
        
    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
       
        songplay_data = (row.ts, row.userId, row.level,\
                         songid, artistid, row.sessionId,\
                         row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Gets all files matching extension from directory.
    - Gets total number of files found.
    - Iterates over files and process.
    
        Parameters:
            - cur: psycopg2.connect.cursor()
            - conn: psycopg2.connect()
            - filepath: str
            - func: Callable[[psycopg2.connect.cursor(), str]]
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets cursor to it.
    - Process song dataset.
    - Process log dataset.
    - Closes connection.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()