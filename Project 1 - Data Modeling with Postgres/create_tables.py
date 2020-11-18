import psycopg2

from sql_queries import (create_data_type_queries, create_table_queries, 
                         drop_data_type_queries, drop_table_queries)


def create_database():
    """
    - Creates and connects to the sparkifydb.
    - Returns the connection and cursor to sparkifydb.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
   
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    conn.close()    
   
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_data_types(cur, conn):
    """
    Drops each data type using the queries in `drop_data_type_queries` list.
    """
    for query in drop_data_type_queries:
        cur.execute(query)
        conn.commit()

        
def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_data_types(cur, conn):
    """
    Creates each data type using the queries in `create_data_type_queries` list.
    """
    for query in create_data_type_queries:
        cur.execute(query)
        conn.commit()
        
        
def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    - Drops all the tables. 
    - Drops all the data types.
    - Creates all data types needed.
    - Creates all tables needed. 
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_data_types(cur, conn)
    drop_tables(cur, conn)
    create_data_types(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()