from cassandra.cluster import Cluster
from cql_queries import drop_table_queries, create_table_queries


def create_keyspace():
    """ 
    - Creates and connects to the sparkify keyspace.
    - Returns the cluster and session to sparkify keyspace.
    """
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    
    session.execute("DROP KEYSPACE IF EXISTS sparkify;")
    session.execute("""
    CREATE KEYSPACE sparkify 
    WITH REPLICATION = {
    'class': 'SimpleStrategy', 'replication_factor': 1
    };
    """)
    session.set_keyspace("sparkify")
    
    return cluster, session


def drop_tables(session: Cluster.connect):
    """ 
    - Drops each table using the queries in `drop_table_queries` list.
    
        Parameters: - session: Cluster.connect() - the current Cassandra's session
    """
    for query in drop_table_queries:
        session.execute(query)


def create_tables(session: Cluster.connect):
    """ 
    - Creates each table using the queries in `create_table_queries` list. 
    
        Parameters: - session: Cluster.connect() - the current Cassandra's session
    """
    for query in create_table_queries:
        session.execute(query)

        
def main():
    """ 
    - Drops (if exists) and Creates the sparkify keyspace. 
    - Establishes connection with the sparkify keyspace and set 
    session to it.  
    - Drops all the tables. 
    - Creates all tables needed. 
    - Finally, shut down the session and cluster. 
    """
    cluster, session = create_keyspace()
    drop_tables(session)
    create_tables(session)
    session.shutdown()
    cluster.shutdown()

    
if __name__ == '__main__':
    main()