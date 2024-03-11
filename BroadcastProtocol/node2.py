import socket


def main():
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    node_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    node_socket.bind(('0.0.0.0', 12345))
    print("Node2 listening for broadcast messages")

    while True:
        message, _ = node_socket.recvfrom(1024)
        print(f"Node2 received broadcast message: {message.decode('utf-8')}", flush=True)


if __name__ == '__main__':
    main()
