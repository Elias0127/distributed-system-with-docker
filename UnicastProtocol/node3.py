import socket
import sys


node_id = "node3"


def connect_to_server(host, port):
    """
    Connect to the server and send a registration message.
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
        # Send registration message
        node_socket.send(f"register:{node_id}".encode('utf-8'))
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
            # Example: node3 sends a message to node1
            send_message_to(node_socket, "node1", "Hello from node3!")

            # Node3 receives a message from node1 (or any other node)
            while True:
                response = node_socket.recv(1024).decode('utf-8')
                if response:
                    sender_id, content = response.split(':', 1)
                    print(f"{node_id} received message from {sender_id}: {content}")

                else:
                    break
        except Exception as e:
            print(f"{node_id} error during communication: {e}", file=sys.stderr)
        finally:
            node_socket.close()
            print(f"{node_id} disconnected from server")


if __name__ == "__main__":
    main()
