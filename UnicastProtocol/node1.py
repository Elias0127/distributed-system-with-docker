import socket
import sys
import time

node_id = "node1"


def connect_to_server(host, port):
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
    full_message = f"{node_id}:{recipient_id}:{message}"
    node_socket.send(full_message.encode('utf-8'))


def main():
    server_hostname = 'server'
    port = 12345

    server_ip = socket.gethostbyname(server_hostname)
    node_socket = connect_to_server(server_ip, port)

    if node_socket:
        try:
            time.sleep(5)  # Wait for 5 seconds to ensure node2 is registered
            send_message_to(node_socket, "node2", "Hello from node1!")

            # Node1 receives a message from node2 (or any other node)
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
