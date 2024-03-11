import socket


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 12345))
    print("Broadcast server is listening on port 12345", flush=True)

    while True:
        message, address = server_socket.recvfrom(1024)
        print(f"Received message from {address}: {message.decode('utf-8')}", flush=True)
        # Broadcast the message to all clients 
        server_socket.sendto(message, ('<broadcast>', 12345))


if __name__ == '__main__':
    main()
