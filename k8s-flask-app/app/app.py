from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS visits (count INT);')
    cur.execute('INSERT INTO visits (count) VALUES (1);')
    conn.commit()
    cur.execute('SELECT COUNT(*) FROM visits;')
    visits = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"Hello! You've visited this page {visits} times."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
