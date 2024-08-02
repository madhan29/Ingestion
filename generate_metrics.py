import sqlite3
import time
import random

def create_table():
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS metrics
                 (timestamp INTEGER, metric TEXT, server TEXT, id TEXT, value REAL)''')
    conn.commit()
    conn.close()

def insert_metric(timestamp, metric, server, id, value):
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()
    c.execute("INSERT INTO metrics VALUES (?, ?, ?, ?, ?)", (timestamp, metric, server, id, value))
    conn.commit()
    conn.close()

def generate_random_metrics():
    metrics = ['store', 'state']
    while True:
        timestamp = int(time.time() * 1000)
        for metric in metrics:
            server = f'server-{random.randint(1, 10)}'
            id = f'id-{random.randint(1, 100)}'
            value = random.random() * 100
            insert_metric(timestamp, metric, server, id, value)
        time.sleep(5)

if __name__ == "__main__":
    create_table()
    generate_random_metrics()
