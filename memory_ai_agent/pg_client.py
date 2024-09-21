import psycopg
from psycopg.rows import dict_row


DB_PARAMS = {
    'dbname': "momory_agent",
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}


def connect_db():
    conn = psycopg.connect(**DB_PARAMS)
    return conn


def fetch_conversations():
    conn = connect_db()
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute('SELECT * FROM conversations')
        conversations = cursor.fetchall()
    conn.close()
    return conversations


def store_conversation(prompt, response):
    conn = connect_db()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO conversations (timestamp, prompt, response) VALUES (CURRENT_TIMESTAMP, %s, %s)',
            (prompt, response)
        )
        conn.commit()
    conn.close()
