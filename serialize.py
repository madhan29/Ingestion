import snappy
import prometheus_pb2

# Read the compressed data
with open('debug_data.bin', 'rb') as f:
    compressed_data = f.read()

# Decompress the data
data = snappy.uncompress(compressed_data)

# Parse the data using protobuf
write_request = prometheus_pb2.WriteRequest()
write_request.ParseFromString(data)

# Print the parsed data for inspection
print(write_request)
