import prometheus_pb2

def decode_protobuf(filename):
    with open(filename, 'rb') as f:
        serialized_data = f.read()

    write_request = prometheus_pb2.WriteRequest()
    write_request.ParseFromString(serialized_data)
    return write_request

def main():
    write_request = decode_protobuf('serialized_data.bin')
    print(write_request)

if __name__ == "__main__":
    main()
