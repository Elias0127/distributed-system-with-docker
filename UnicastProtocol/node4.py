import socket
import sys


node_id = "node4"


def connect_to_server(host, port):
    """
    Connect to the server.
    Args:
        host (str): The server's host address.
        port (int): The server's port number.
    Returns:
        socket.socket or None: The client's socket if connection is successful, None otherwise.
    """
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        node_socket.connect((host, port))
        print(f"{node_id} connected to server at {host}:{port}")
        return node_socket
    except socket.error as e:
        print(f"{node_id} error connecting to server: {e}", file=sys.stderr)
        return None


def send_message_to(node_socket, recipient_id, message):
    """
    Send a message to a specific recipient.
    Args:
        node_socket (socket.socket): The client's socket.
        recipient_id (str): The ID of the recipient node.
        message (str): The message to send.
    """
    full_message = f"{node_id}:{recipient_id}:{message}"
    node_socket.send(full_message.encode('utf-8'))


def main():
    server_hostname = 'server'
    port = 12345

    server_ip = socket.gethostbyname(server_hostname)
    node_socket = connect_to_server(server_ip, port)

    if node_socket:
        try:
            # Example sending a message to node2 from this node
            send_message_to(node_socket, "node2", "Hello from nodeX!")

            while True:
                response = node_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"{node_id} received message: {response}")
                else:
                    break
        except Exception as e:
            print(f"{node_id} error during communication: {e}", file=sys.stderr)
        finally:
            node_socket.close()
            print(f"{node_id} disconnected from server")


if __name__ == "__main__":
    main()
