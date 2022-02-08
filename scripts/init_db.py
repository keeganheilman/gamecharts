import os
import sys
import psycopg2
from psycopg2 import Error


# ref: https://stackoverflow.com/questions/34484066/create-a-postgres-database-using-python
# Use the psycopg2.sql module instead of string concatenation 
# in order to avoid sql injection attacks.
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



# Import hidden will fail when ...
try:
    import hidden
    secrets = hidden.secrets()
    sql_string = secrets['connection_string']

    conn = psycopg2.connect(sql_string,connect_timeout=3)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True
    cursor = conn.cursor()
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'db.sql')) as f:
        sql_create_db_stmt = f.read()
    
    cursor.execute(sql.SQL(sql_create_db_stmt)) # Error while connecting to PostgreSQL DROP DATABASE cannot run inside a transaction block
    # cursor.execute(sql.SQL("DROP DATABASE GAMECHARTSDB")) # This works?!

    conn.close()

except (Exception, Error) as Error:
       print("Error while connecting to PostgreSQL", Error)

