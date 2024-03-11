import socket


def main():
    message = b"Hello, nodes! This is a broadcast from the master server."
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_socket.sendto(message, ('<broadcast>', 12345))
    print("Server broadcasted a message to all nodes")


if __name__ == '__main__':
    main()
