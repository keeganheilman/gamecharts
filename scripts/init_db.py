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
    conn_sql_string = secrets['default_connection_string']

    conn = psycopg2.connect(conn_sql_string,connect_timeout=3)
    # Is setting the ISOLATION_LEVEL_AUTOCOMMIT necessary?
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True
    cursor = conn.cursor()
    
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'db.sql')) as f:
        sql_create_db_stmt = f.read()
    
    # what is the best practice for handling the SQL CREATE and DROP DATABASE statements with psycopg2?
    # cursor.execute(sql.SQL(sql_create_db_stmt)) # Error while connecting to PostgreSQL DROP DATABASE cannot run inside a transaction block
    # ref: https://stackoverflow.com/questions/18389124/simulate-create-database-if-not-exists-for-postgresql
    # currently hard-coding the creation of the database. would prefer to be able to read in statements from SQL document; will require change.
    cursor.execute(sql.SQL("SELECT 'CREATE DATABASE gamechartsdb' WHERE NOT EXISTS (SELECT FROM pg_catalog.pg_database WHERE datname = 'gamechartsdb')")) # This works?!
    cursor.close()
    conn.close()

    # Connect to the new database, gamechartsDB.
    conn_sql_string = secrets['gamechartsdb_connection_string']
    conn = psycopg2.connect(conn_sql_string,connect_timeout=3)
    # Is setting the ISOLATION_LEVEL_AUTOCOMMIT necessary?
    # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    conn.autocommit = True
    cursor = conn.cursor()
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'schema.sql')) as f:
        sql_create_tables = f.read()
    cursor.execute(sql.SQL(sql_create_tables))

    # INSERT example plays
    # id SERIAL,
    # created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    # description TEXT NOT NULL,
    # PRIMARY KEY(id)
    cursor.execute("INSERT INTO plays (description) VALUES (%s)",
            ('C.Kupp 16 yd. pass from M.Stafford (M.Gay kick) (18-97, 9:33)',)
            )

    cursor.execute("INSERT INTO plays (description) VALUES (%s)",
            ('D.Samuel 44 yd. pass from J.Garoppolo (R.Gould kick) (4-75, 2:36)',)
            )


    conn.close()

except (Exception, Error) as Error:
       print("Error while connecting to PostgreSQL", Error)

