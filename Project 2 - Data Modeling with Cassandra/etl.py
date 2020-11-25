import os
import glob
import csv
from cassandra.cluster import Cluster
from cql_queries import *


def get_filepath_list(filepath: str):
    """ 
    Returns a list of files path for a given directory.
    
        Parameters: - subdir: str - the directory name
    """
    for root, dirs, files in os.walk(filepath):
        files_path_list = glob.glob(os.path.join(root, '*'))
        
    return files_path_list


def read_csv(filepath: str):
    """ 
    Returns a list of rows from a CSV file.
    
        Parameters: - filepath: str - the filepath from the CSV file
    """
    data_rows_list = []
    with open(filepath, 'r', encoding='utf8', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # skips the first row (header)
        
        for row in csvreader:
            data_rows_list.append(row)
            
    return data_rows_list


def to_csv(data: list, root: str, filename: str, header: list = None):
    """ 
    Writes data to CSV file.
    
        Parameters: - data: list - list of data rows
                    - root: str - root directory where the file will be stored
                    - filename: str - the name of the CSV file
                    - header: list - list of column names for the CSV file (optional)
    """
    csv.register_dialect('dialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    
    filepath = root + '/' + filename + '.csv'
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, dialect='dialect')
        if header:
            writer.writerow(header)
        
        for row in data:
            if row[0] == '':
                continue
            writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], \
                             row[8], row[12], row[13], row[16]))


def preprocess_files(root: str, directory: str, filename: str):
    """ 
    - Gets the list of files path for the given directory.
    - Reads each CSV from the file path list and append it to a list.
    - Preprocess the data by filtering some fields and stored it in a CSV file.
        
        Parameters: - root: str - the working directory path 
                    - directory: str - the directory name that contains the event data
                    - filename: str - the name of the new CSV file
    """
    path = root + '/' + directory
    files_path_list = get_filepath_list(path)
    full_data_rows_list = []
    for filepath in files_path_list:
        full_data_rows_list.extend(read_csv(filepath))
                    
    header = ['artist', 'firstName', 'gender', 'itemInSession', \
              'lastName', 'length', 'level', 'location', 'sessionId', \
              'song', 'userId']
    
    to_csv(full_data_rows_list, root, filename, header)
    

def process_data(session: Cluster.connect, filepath: str):
    """
    - Reads the CSV file from `filepath` row by row.
    - Extracts data for `song_info_by_session` table.
    - Inserts records into `song_info_by_session` table row by row
    using `song_info_by_session_table_insert` query.
    - Extracts data for `song_user_info_by_user_session` table.
    - Inserts records into `song_user_info_by_user_session` table row by row
    using `song_user_info_by_user_session_table_insert` query.
    - Extracts data for `user_info_by_given_song` table.
    - Inserts records into `user_info_by_given_song` table row by row
    using `user_info_by_given_song_table_insert` query.
    
        Parameters: - session: Cluster.connect - the current Cassandra's session
                    - filepath: str - the new CSV filepath
    """
    with open(filepath, 'r', encoding='utf8', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # skips first row (header)
        
        for row in csvreader:
            if row[0] == '':
                continue
                
            song_info_by_session_row = [int(row[8]), int(row[3]), row[0], row[9], float(row[5])]
            session.execute(song_info_by_session_table_insert, song_info_by_session_row)
            
            song_user_info_by_user_session_row = \
            [int(row[10]), int(row[8]), int(row[3]), row[0], row[9], row[1], row[4]]
            session.execute(song_user_info_by_user_session_table_insert, song_user_info_by_user_session_row)
            
            user_info_by_given_song_row = [row[9], int(row[10]), row[1], row[4]]
            session.execute(user_info_by_given_song_table_insert, user_info_by_given_song_row)
            

def main():
    """
    - Establishes connection with the sparkify keyspace and gets session to it.
    - Process the new CSV file.
    - Shutdown session and cluster.
    """
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    
    session.set_keyspace("sparkify")
    
    directory = 'event_data'
    filename = 'event_datafile_new'
    
    preprocess_files(root=os.getcwd(), directory=directory, filename=filename)
    
    filepath = os.getcwd() + '/' + filename + '.csv'
    process_data(session, filepath)
        
    session.shutdown()
    cluster.shutdown()
    

if __name__== '__main__':
    main()