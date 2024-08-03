import time
import snappy
import sqlite3
from prometheus_pb2 import WriteRequest, TimeSeries, Label, Sample
import requests

def create_sample(metric_name, server, id, timestamp, value):
    ts = TimeSeries()
    ts.labels.add(name="__name__", value=metric_name)
    ts.labels.add(name="server", value=server)
    ts.labels.add(name="id", value=id)
    ts.samples.add(value=value, timestamp=timestamp)
    return ts

def fetch_metrics_from_db(last_timestamp):
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, metric, server, id, value FROM metrics WHERE timestamp > ? ORDER BY timestamp ASC", (last_timestamp,))
    rows = c.fetchall()
    conn.close()
    return rows

def push_to_prometheus(metrics):
    url = "http://localhost:9090/api/v1/write"
    headers = {
        'Content-Type': 'application/x-protobuf',
        'Content-Encoding': 'snappy'
    }

    try:
        compressed_data = snappy.compress(metrics.SerializeToString())
        response = requests.post(url, data=compressed_data, headers=headers)
        response.raise_for_status()
        print(f"Successfully pushed data to Prometheus: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error pushing data to Prometheus: {e}")
        if response.content:
            print("Response content:", response.content)

def generate_and_push_metrics():
    last_timestamp = 0  # Start with the earliest possible timestamp
    try:
        while True:
            rows = fetch_metrics_from_db(last_timestamp)
            if rows:
                metrics = WriteRequest()
                for row in rows:
                    timestamp, metric_name, server, id, value = row
                    metrics.timeseries.extend([create_sample(metric_name, server, id, timestamp, value)])
                push_to_prometheus(metrics)
                last_timestamp = rows[-1][0]  # Update the last timestamp to the most recent one
            time.sleep(5)  # Wait for 5 seconds before fetching the next set of metrics

    except KeyboardInterrupt:
        print("Metric generation stopped.")

if __name__ == "__main__":
    generate_and_push_metrics()
