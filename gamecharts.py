import psycopg2
from psycopg2.extras import RealDictCursor
from scripts import hidden
from flask import Flask, request, render_template
app = Flask(__name__)


def get_db_connection():
    secrets = hidden.secrets()
    conn_sql_string = secrets['gamechartsdb_connection_string']
    conn = psycopg2.connect(conn_sql_string,connect_timeout=3)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM PLAYS')
    plays = cursor.fetchall()
    print(plays)
    return render_template('index.html', plays = plays)
