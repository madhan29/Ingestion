import time
import random
import snappy
from prometheus_pb2 import WriteRequest, TimeSeries, Label, Sample
import requests

def create_sample(metric_name, server, id, timestamp, value):
    ts = TimeSeries()
    ts.labels.add(name="__name__", value=metric_name)
    ts.labels.add(name="server", value=server)
    ts.labels.add(name="id", value=id)
    ts.samples.add(value=value, timestamp=timestamp)
    return ts

def generate_metrics(base_timestamp):
    metrics = WriteRequest()
    for i in range(10):  # Generate 10 metrics for testing
        metric_name = random.choice(["store", "state"])
        server = f"server-{random.randint(1, 10)}"
        id = f"id-{random.randint(1, 100)}"
        value = random.uniform(0, 100)
        timestamp = base_timestamp + i  # Ensure strictly increasing timestamps
        metrics.timeseries.extend([create_sample(metric_name, server, id, timestamp, value)])
    return metrics

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

if __name__ == "__main__":
    base_timestamp = int(time.time() * 1000)  # Convert to milliseconds
    metrics = generate_metrics(base_timestamp)
    push_to_prometheus(metrics)
